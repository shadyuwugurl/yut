#!/usr/bin/env python3
"""Generate construct and persona conversations in HF chat JSONL.

Labels are skinny-v1 canonical ids (category + id). Aliases are inputs:
``--id spoon`` stores ``meta.id = research`` and ``meta.alias_input = spoon``.

Backends
  procedural   no API key; hand-written templates x situation bank
  llm          OpenAI-compatible teacher (OPENAI_BASE_URL, OPENAI_API_KEY, MODEL)
               The teacher sees the full-template card. Saved rows do not.

Examples
  # authored exemplars (about 20 per id)
  python3 datasets/constructs_personas/generate.py --emit-seeds \\
      --out datasets/constructs_personas/seed.jsonl --seed 11

  # sample batch, ~100 per id, gzipped train/val
  python3 datasets/constructs_personas/generate.py --backend procedural --n 100 \\
      --out datasets/constructs_personas/sample --seed 11 \\
      --avoid datasets/constructs_personas/seed.jsonl

  # full run Charlie sized, teacher model
  OPENAI_BASE_URL=https://host/v1 OPENAI_API_KEY=... MODEL=... \\
  python3 datasets/constructs_personas/generate.py --backend llm --n 3000 \\
      --out datasets/constructs_personas/full --seed 11 --workers 8

  # same scale with no key, procedural fallback
  python3 datasets/constructs_personas/generate.py --backend procedural --n 3000 \\
      --out datasets/constructs_personas/full --seed 11
"""
from __future__ import annotations

import argparse
import gzip
import json
import random
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cp.filters import NearDup, example_fingerprint, visible_text  # noqa: E402
from cp.llm_backend import generate_llm_one  # noqa: E402
from cp.procedural import (  # noqa: E402
    all_specs,
    generate_for,
    spec_for,
    stable_split,
    _partners,
)
from cp.taxonomy import items, resolve  # noqa: E402


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    opener = gzip.open if path.suffix == ".gz" else open
    rows = []
    with opener(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _write_jsonl(path: Path, rows: list[dict], gzip_file: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if gzip_file:
        if path.suffix != ".gz":
            path = path.with_suffix(path.suffix + ".gz")
        with gzip.open(path, "wt", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    else:
        with path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _selected(names: list[str] | None) -> list[dict]:
    specs = all_specs()
    if not names:
        return specs
    want = set()
    for name in names:
        if "/" in name:
            cat, ident, _alias = resolve(name.split("/", 1)[1], category=name.split("/", 1)[0])
        else:
            cat, ident, _alias = resolve(name)
        want.add((cat, ident))
    return [spec for spec in specs if (spec["category"], spec["id"]) in want]


def _alias_for(name: str | None, spec: dict):
    if not name or name in {spec["id"], f"{spec['category']}/{spec['id']}"}:
        return None
    _cat, ident, alias = resolve(name, category=spec["category"] if "/" not in name else None)
    if ident != spec["id"]:
        return None
    return alias


def _preload(dedupe: NearDup, rows: list[dict], category: str, ident: str) -> None:
    for row in rows:
        meta = row.get("meta") or {}
        if meta.get("category") != category or meta.get("id") != ident:
            continue
        parts = []
        for msg in row.get("messages") or []:
            if msg.get("role") == "system":
                continue
            content = msg.get("content") or ""
            parts.append(visible_text(content) if msg.get("role") == "assistant" else content)
        text = "\n".join(parts)
        fp = example_fingerprint(row)
        dedupe.add(text, fp)


def _llm_rows(spec: dict, n: int, *, seed: int, alias_input, dedupe: NearDup) -> list[dict]:
    rng = random.Random(f"llm|{seed}|{spec['id']}")
    partners = _partners(spec)
    out = []
    attempt = 0
    while len(out) < n and attempt < n * 8:
        attempt += 1
        pattern = rng.choices(
            ["single", "multi", "switch", "blend", "stay"],
            weights=[0.34, 0.24, 0.18, 0.14, 0.10],
            k=1,
        )[0]
        partner = partners[attempt % len(partners)] if partners else None
        try:
            ex = generate_llm_one(
                spec, pattern, variant=attempt, alias_input=alias_input, partner=partner,
            )
        except Exception as exc:  # noqa: BLE001 — keep a long run alive
            print(f"llm {spec['id']} attempt {attempt}: {exc}", file=sys.stderr)
            continue
        if ex is None:
            continue
        text = "\n".join(
            visible_text(m["content"]) if m["role"] == "assistant" else m["content"]
            for m in ex["messages"] if m["role"] != "system"
        )
        fp = example_fingerprint(ex)
        if dedupe.too_close(text, fp):
            continue
        dedupe.add(text, fp)
        out.append(ex)
    return out


def _counts(rows: list[dict]) -> dict:
    counter = Counter((r["meta"]["category"], r["meta"]["id"], r["meta"]["pattern"]) for r in rows)
    by_id = Counter((r["meta"]["category"], r["meta"]["id"]) for r in rows)
    return {
        "rows": len(rows),
        "per_id": {f"{cat}/{ident}": n for (cat, ident), n in sorted(by_id.items())},
        "per_pattern": {f"{cat}/{ident}/{pat}": n for (cat, ident, pat), n in sorted(counter.items())},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--backend", choices=("procedural", "llm"), default="procedural")
    parser.add_argument("--n", type=int, default=3000, help="target rows per id (default 3000)")
    parser.add_argument("--emit-seeds", action="store_true", help="write the authored exemplar set (20 per id unless --n is set)")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--ids", nargs="*", help="canonical ids or aliases; default is every construct and persona")
    parser.add_argument("--id", dest="one", help="one id or alias (alias is recorded, not used as the label)")
    parser.add_argument("--val-ratio", type=float, default=0.05)
    parser.add_argument("--avoid", type=Path, help="JSONL/JSONL.GZ of rows that must not be repeated")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--gzip", action="store_true", help="force gzip (directories gzip when the split is large)")
    args = parser.parse_args()

    names = list(args.ids or [])
    if args.one:
        names.append(args.one)
    specs = _selected(names or None)
    if args.emit_seeds and args.n == 3000:
        per_id = 20
    else:
        per_id = args.n

    avoid_rows = _read_jsonl(args.avoid) if args.avoid else []

    def one_spec(spec: dict) -> list[dict]:
        alias = None
        if args.one and len(specs) == 1:
            _c, _i, alias = resolve(args.one)
        dedupe = NearDup()
        _preload(dedupe, avoid_rows, spec["category"], spec["id"])
        if args.backend == "llm" and not args.emit_seeds:
            rows = _llm_rows(spec, per_id, seed=args.seed, alias_input=alias, dedupe=dedupe)
        else:
            rows = generate_for(
                spec, per_id,
                seed=args.seed,
                source="seed" if args.emit_seeds else "procedural",
                alias_input=alias,
                diversify=not args.emit_seeds,
                dedupe=dedupe,
            )
        print(f"{spec['category']}/{spec['id']}: {len(rows)}", file=sys.stderr)
        return rows

    if args.backend == "llm" and not args.emit_seeds and args.workers > 1:
        all_rows = []
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(one_spec, spec) for spec in specs]
            for future in as_completed(futures):
                all_rows.extend(future.result())
    else:
        all_rows = []
        for spec in specs:
            all_rows.extend(one_spec(spec))

    if args.emit_seeds or args.out.suffix == ".jsonl":
        _write_jsonl(args.out, all_rows, gzip_file=False)
        print(f"wrote {len(all_rows)} rows to {args.out}")
        return

    train, val = stable_split(all_rows, args.val_ratio)
    big = len(all_rows) * 800 > 1_000_000
    gzip_file = args.gzip or big
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    train_path = out / ("train.jsonl.gz" if gzip_file else "train.jsonl")
    val_path = out / ("val.jsonl.gz" if gzip_file else "val.jsonl")

    def dump(path: Path, rows: list[dict]) -> None:
        if path.suffix == ".gz":
            with gzip.open(path, "wt", encoding="utf-8") as handle:
                for row in rows:
                    handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        else:
            path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

    dump(train_path, train)
    dump(val_path, val)
    summary = {
        "taxonomy": "skinny-v1",
        "backend": "seed" if args.emit_seeds else args.backend,
        "target_per_id": per_id,
        "train": _counts(train),
        "val": _counts(val),
        "ids": [f"{it['category']}/{it['id']}" for it in items()],
    }
    (out / "counts.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(train)} train and {len(val)} val under {out}")


if __name__ == "__main__":
    main()
