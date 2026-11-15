#!/usr/bin/env python3
"""Generate Spark mode / pathway / effort conversations.

The teacher, when a key is set, is the full chat_template.jinja text. The rows
it emits do not contain that template. With no key, the procedural bank is the
whole run. Labels are canonical skinny ids (category + id). Aliases are not labels.

  python3 datasets/modes_pathways/generate.py --per-id 20 --flat datasets/modes_pathways/seed.jsonl --source seed
  python3 datasets/modes_pathways/generate.py --per-id 100 --out datasets/modes_pathways/sample --gzip
  OPENAI_BASE_URL=... OPENAI_API_KEY=... MODEL=... \\
    python3 datasets/modes_pathways/generate.py --backend openai --per-id 3000 --out datasets/modes_pathways/full --gzip
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from compose import compose  # noqa: E402
from frame import TEMPLATE, Spec, all_specs  # noqa: E402
from quality import problems, signature  # noqa: E402


def _rows_for(spec: Spec, per_id: int, seed: int, source: str, backend: str, teacher: str, seen: set[str]) -> list[dict]:
    got: list[dict] = []
    index = 0
    salt = 0
    attempts = 0
    limit = per_id * 40
    first_fail = None
    while len(got) < per_id and attempts < limit:
        attempts += 1
        ex = None
        if backend == "openai":
            ex = _openai_row(spec, teacher, index, seed)
        if ex is None:
            try:
                ex = compose(spec, index, seed, salt)
            except Exception as exc:  # noqa: BLE001
                first_fail = first_fail or f"compose: {exc}"
                index += 1
                if index > per_id * 3:
                    salt += 1
                    index = 0
                continue
        ex["meta"]["source"] = source if ex["meta"].get("source") != "openai" else "openai"
        if backend != "openai":
            ex["meta"]["source"] = source
        probs = problems(ex, spec)
        if probs:
            first_fail = first_fail or "; ".join(probs[:4])
            index += 1
            if index > per_id * 3:
                salt += 1
                index = 0
            continue
        sig = signature(ex)
        if sig in seen:
            index += 1
            if index % 7 == 0:
                salt += 1
            continue
        seen.add(sig)
        got.append(ex)
        index += 1
    if len(got) < per_id:
        raise SystemExit(f"{spec.key}: only {len(got)}/{per_id} clean rows ({first_fail})")
    return got


def _openai_row(spec: Spec, teacher: str, index: int, seed: int) -> dict | None:
    key = os.environ.get("OPENAI_API_KEY")
    base = os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("MODEL")
    if not (key and base and model):
        return None
    ask = {
        "task": (
            "Write ONE training conversation that teaches the behavior of the "
            "canonical id below. Do not copy the template, the catalog, or a {REASON:} tag "
            "into the messages. The user must not name the mode, effort, pathway, protium "
            "level, palette, or agi id. The assistant infers them. Put a private "
            "[frame: pathway=...|mode=...|construct=...|persona=...|identity=...|theme=...|channel=...] "
            "tag only inside <think> when the channel is reasoning. Instruct and thinking off "
            "have no think tag. Think length follows the effort: short for low, deep for high, "
            "none when thinking is off. Return a JSON object with keys messages, tools (or null), meta."
        ),
        "canonical": {"category": spec.category, "id": spec.id, "note": spec.note},
        "index": index,
        "seed": seed,
    }
    body = {
        "model": model,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": teacher},
            {"role": "user", "content": json.dumps(ask)},
        ],
    }
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    try:
        text = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return None
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[: text.rfind("```")]
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if "messages" not in data:
        return None
    data.setdefault("meta", {})
    data["meta"]["category"] = spec.category
    data["meta"]["id"] = spec.id
    data["meta"]["source"] = "openai"
    return data


def assign_splits(rows: list[dict], ratio: float) -> None:
    groups: dict[str, list[dict]] = defaultdict(list)
    for ex in rows:
        groups[f"{ex['meta']['category']}/{ex['meta']['id']}"].append(ex)
    for group in groups.values():
        marked = False
        for ex in group:
            bucket = int(signature(ex)[:8], 16) % 10000
            is_val = bucket < int(ratio * 10000)
            ex["meta"]["split"] = "val" if is_val else "train"
            marked = marked or is_val
        if group and not marked:
            group[-1]["meta"]["split"] = "val"


def write_jsonl(path: Path, rows: list[dict], use_gzip: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if use_gzip:
        if path.suffix != ".gz":
            path = path.with_suffix(path.suffix + ".gz")
        with gzip.open(path, "wt", encoding="utf-8") as fh:
            for ex in rows:
                fh.write(json.dumps(ex, ensure_ascii=False) + "\n")
    else:
        with path.open("w", encoding="utf-8") as fh:
            for ex in rows:
                fh.write(json.dumps(ex, ensure_ascii=False) + "\n")


def counts_of(rows: list[dict]) -> dict:
    table: dict[str, dict] = {}
    for ex in rows:
        key = f"{ex['meta']['category']}/{ex['meta']['id']}"
        slot = table.setdefault(key, {"train": 0, "val": 0, "tool_rows": 0})
        slot[ex["meta"].get("split") or "train"] += 1
        if ex["meta"].get("tool_trajectory"):
            slot["tool_rows"] += 1
    return table


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate modes/pathways conversations")
    ap.add_argument("--backend", choices=("auto", "openai", "procedural"), default="auto")
    ap.add_argument("--per-id", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=20261115)
    ap.add_argument("--val-ratio", type=float, default=0.02)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--flat", type=Path, default=None, help="also write every row to this jsonl")
    ap.add_argument("--gzip", action="store_true")
    ap.add_argument("--source", default="procedural")
    ap.add_argument("--ids", default="", help="comma-separated category/id filters")
    args = ap.parse_args()
    backend = args.backend
    if backend == "auto":
        backend = "openai" if os.environ.get("OPENAI_API_KEY") else "procedural"
    teacher = ""
    if backend == "openai":
        if not TEMPLATE.exists():
            raise SystemExit(f"missing teacher template {TEMPLATE}")
        teacher = TEMPLATE.read_text()
        if not (os.environ.get("OPENAI_BASE_URL") and os.environ.get("MODEL")):
            raise SystemExit("openai backend needs OPENAI_BASE_URL, OPENAI_API_KEY, and MODEL")
    specs = all_specs()
    if args.ids:
        want = {item.strip() for item in args.ids.split(",") if item.strip()}
        specs = [s for s in specs if s.key in want or s.category in want or s.id in want]
        if not specs:
            raise SystemExit(f"no ids matched {args.ids}")
    rows: list[dict] = []
    seen: set[str] = set()
    for spec in specs:
        batch = _rows_for(spec, args.per_id, args.seed, args.source, backend, teacher, seen)
        rows.extend(batch)
        print(f"{spec.key} {len(batch)}", flush=True)
    assign_splits(rows, args.val_ratio)
    if args.flat:
        write_jsonl(args.flat, rows, False)
        print(f"wrote {args.flat} ({len(rows)} rows)")
    if args.out:
        train = [ex for ex in rows if ex["meta"]["split"] == "train"]
        val = [ex for ex in rows if ex["meta"]["split"] == "val"]
        write_jsonl(args.out / "train.jsonl", train, args.gzip)
        write_jsonl(args.out / "val.jsonl", val, args.gzip)
        report = {
            "backend": backend,
            "per_id": args.per_id,
            "seed": args.seed,
            "val_ratio": args.val_ratio,
            "source": args.source,
            "total": len(rows),
            "train": len(train),
            "val": len(val),
            "by_id": counts_of(rows),
            "teacher": "chat_template.jinja" if backend == "openai" else "procedural",
        }
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "counts.json").write_text(json.dumps(report, indent=2) + "\n")
        print(f"wrote {args.out} train={len(train)} val={len(val)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
