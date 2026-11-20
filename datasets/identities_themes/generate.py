#!/usr/bin/env python3
"""Generate identity and theme chats labeled with skinny-v1 ids.

Backend:
  auto        OpenAI-compatible teacher if OPENAI_API_KEY is set, else procedural
  openai      teacher only (OPENAI_BASE_URL, OPENAI_API_KEY, MODEL)
  procedural  no key; handwritten clause banks

The teacher sees verbatim text from the full chat template. The saved row does
not. meta.category + meta.id are canonical. Aliases, including every Josie
wording, are inputs only.

  python3 datasets/identities_themes/generate.py --backend procedural --per-id 3000 --out-dir datasets/identities_themes/out
  python3 datasets/identities_themes/generate.py --backend procedural --per-id 100 --out-dir datasets/identities_themes/sample --val-ratio 0.05
  OPENAI_BASE_URL=... OPENAI_API_KEY=... MODEL=... \\
    python3 datasets/identities_themes/generate.py --backend openai --per-id 3000 --teacher-scope slice --out-dir datasets/identities_themes/out-teacher
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from canonical import file_sha256, load_canon, taxonomy_path  # noqa: E402
from procedural import check_bank, generate_id, quotas, rng_for  # noqa: E402
from registry import SPECS  # noqa: E402
from safety import check_record, exact_hash  # noqa: E402
from teacher import OpenAITeacher, TeacherError, brief_for, parse_messages, system_for  # noqa: E402


def val_target(n: int, ratio: float) -> int:
    if n == 0 or ratio <= 0:
        return 0
    k = int(round(n * ratio))
    if n >= 20:
        k = max(1, k)
    return min(k, max(1, n // 5) if n >= 5 else 1)


def split_rows(rows: list[dict], ratio: float) -> tuple[list[dict], list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["meta"]["key"]].append(row)
    train, val = [], []
    for group in groups.values():
        scored = sorted(group, key=lambda r: exact_hash(r["messages"]))
        n_val = val_target(len(scored), ratio)
        chosen = set(id(r) for r in scored[:n_val])
        for row in scored:
            (val if id(row) in chosen else train).append(row)
    train.sort(key=lambda r: (r["meta"]["key"], exact_hash(r["messages"])))
    val.sort(key=lambda r: (r["meta"]["key"], exact_hash(r["messages"])))
    return train, val


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "wt", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def counts_of(rows: list[dict]) -> dict:
    by = Counter(r["meta"]["key"] for r in rows)
    shapes = Counter((r["meta"]["key"], r["meta"]["shape"]) for r in rows)
    aliases = Counter(r["meta"].get("input_alias") or "" for r in rows if r["meta"]["id"] == "josie")
    return {
        "rows": len(rows),
        "per_id": dict(sorted(by.items())),
        "shapes": {f"{k[0]}:{k[1]}": v for k, v in sorted(shapes.items())},
        "josie_input_alias": {k: v for k, v in sorted(aliases.items()) if k},
    }


def select_pairs(canon, arg: str) -> list[tuple[str, str]]:
    if arg.strip() == "all":
        return canon.training_pairs()
    out = []
    for part in arg.split(","):
        part = part.strip()
        if not part:
            continue
        if "/" in part:
            cat, token = part.split("/", 1)
            cat, id_, _alias = canon.resolve(token, cat)
        else:
            cat, id_, _alias = canon.resolve(part)
        if id_ == "none":
            raise SystemExit("none is the unset dial, not a generation target")
        out.append((cat, id_))
    return out


def procedural_rows(canon, pairs, per_id: int, seed: int, source: str) -> tuple[list[dict], dict]:
    seen: set[str] = set()
    prefixes: set[str] = set()
    rows = []
    rejected = {}
    for _cat, id_ in pairs:
        spec = SPECS[id_]
        made, stats = generate_id(canon, spec, per_id, rng_for(seed, id_), SPECS, source, seen, prefixes)
        rows.extend(made)
        if stats:
            rejected[id_] = stats
        print(f"{id_}: {len(made)}", flush=True)
    return rows, rejected


def teacher_rows(canon, pairs, per_id: int, seed: int, scope: str) -> tuple[list[dict], dict]:
    """Fill the same shape quotas by asking the teacher for each planned row.

    Labels are applied here from the plan. The model's text is only the chat.
    If a completion fails the walls, it is dropped and retried.
    """
    from procedural import build_one

    teacher = OpenAITeacher.from_env()
    seen: set[str] = set()
    prefixes: set[str] = set()
    rows = []
    rejected: dict[str, dict] = {}
    for _cat, id_ in pairs:
        spec = SPECS[id_]
        rng = rng_for(seed, id_)
        need = quotas(per_id)
        made = {k: [] for k in need}
        stats: dict[str, int] = {}
        attempts = 0
        while any(len(made[k]) < need[k] for k in need) and attempts < per_id * 8:
            attempts += 1
            shape = next(k for k in ("single", "multi", "shift", "combo") if len(made[k]) < need[k])
            plan_row = build_one(canon, spec, shape, rng, SPECS, "teacher")
            if plan_row is None:
                continue
            plan = {
                "shape": shape,
                "identity": plan_row["meta"]["identity"],
                "theme": plan_row["meta"]["theme"],
                "input_alias": plan_row["meta"].get("input_alias"),
                "switch_from": (plan_row["meta"].get("switch_from") or {}).get("id"),
                "switch_to": (plan_row["meta"].get("switch_to") or {}).get("id"),
                "direction": (
                    "Inhabit the situation. Do not name the frame. "
                    "The procedural sketch of the situation, which you may improve but must not contradict on safety, was: "
                    + plan_row["messages"][0]["content"][:400]
                ),
            }
            try:
                raw = teacher.complete(system_for(plan, scope), brief_for(plan))
                messages = parse_messages(raw)
            except (TeacherError, json.JSONDecodeError, ValueError) as exc:
                stats[type(exc).__name__] = stats.get(type(exc).__name__, 0) + 1
                continue
            record = dict(plan_row)
            record["messages"] = messages
            record["meta"] = dict(plan_row["meta"])
            record["meta"]["source"] = "teacher"
            record["meta"]["think"] = any("<think>" in m["content"] for m in messages if m["role"] == "assistant")
            # Align effort with whether the teacher actually thought.
            if record["meta"]["think"] and record["meta"]["frame"]["thinking_effort"] == "off":
                record["meta"]["frame"]["thinking_effort"] = "low"
                record["meta"]["frame"]["pathway"] = "s1"
            if not record["meta"]["think"]:
                record["meta"]["frame"]["thinking_effort"] = "off"
                record["meta"]["frame"]["pathway"] = "s1"
            reason = check_record(record, canon)
            if reason:
                stats[reason] = stats.get(reason, 0) + 1
                continue
            digest = exact_hash(messages)
            if digest in seen:
                stats["dup"] = stats.get("dup", 0) + 1
                continue
            seen.add(digest)
            prefixes.add(digest)
            made[shape].append(record)
        got = [r for k in ("single", "multi", "shift", "combo") for r in made[k]]
        if len(got) < per_id:
            raise SystemExit(f"{id_}: teacher produced {len(got)}/{per_id}; rejects={stats}")
        rows.extend(got)
        if stats:
            rejected[id_] = stats
        print(f"{id_}: {len(got)}", flush=True)
    return rows, rejected


def main() -> None:
    p = argparse.ArgumentParser(description="Generate identity/theme chats with skinny-v1 labels")
    p.add_argument("--backend", choices=["auto", "openai", "procedural"], default="auto")
    p.add_argument("--per-id", type=int, default=3000)
    p.add_argument("--ids", default="all", help="all, or comma list of canonical ids or aliases")
    p.add_argument("--seed", type=int, default=6210)
    p.add_argument("--val-ratio", type=float, default=0.02)
    p.add_argument("--out-dir", type=Path, default=HERE / "out")
    p.add_argument("--joined", type=Path, default=None, help="write one jsonl instead of a train/val split")
    p.add_argument("--teacher-scope", choices=["slice", "full"], default="slice")
    p.add_argument("--source-tag", choices=["procedural", "seed", "teacher"], default=None)
    p.add_argument("--self-check", action="store_true", help="build 2 per id in memory and validate")
    args = p.parse_args()
    if args.per_id < 1:
        raise SystemExit("--per-id must be >= 1")
    canon = load_canon()
    check_bank(SPECS)
    pairs = select_pairs(canon, args.ids)
    missing = [id_ for _c, id_ in pairs if id_ not in SPECS]
    if missing:
        raise SystemExit(f"no voice bank for {missing}")
    known = {id_ for _c, id_ in canon.training_pairs()}
    extra = [id_ for id_ in SPECS if id_ not in known]
    if extra and args.ids == "all":
        raise SystemExit(f"voice bank has ids that are not training targets: {extra}")
    if args.self_check:
        procedural_rows(canon, pairs, 2, args.seed, "procedural")
        print("self-check ok", len(pairs), "ids")
        return
    backend = args.backend
    if backend == "auto":
        backend = "openai" if os.environ.get("OPENAI_API_KEY") else "procedural"
        print(f"backend auto -> {backend}", flush=True)
    source = args.source_tag or ("teacher" if backend == "openai" else "procedural")
    if backend == "openai":
        rows, rejected = teacher_rows(canon, pairs, args.per_id, args.seed, args.teacher_scope)
    elif backend == "procedural":
        rows, rejected = procedural_rows(canon, pairs, args.per_id, args.seed, source)
    else:
        raise SystemExit(backend)
    report = {
        "taxonomy": canon.version,
        "taxonomy_path": str(canon.path),
        "taxonomy_sha256": file_sha256(taxonomy_path()),
        "snapshot_commit": "f32e5448fe87e17b3ede90271379f60e1035f2ad",
        "backend": backend,
        "teacher_scope": args.teacher_scope if backend == "openai" else None,
        "per_id": args.per_id,
        "seed": args.seed,
        "val_ratio": args.val_ratio,
        "rejected": rejected,
        **counts_of(rows),
    }
    if args.joined:
        write_jsonl(args.joined, rows)
        report_path = args.joined.with_suffix(args.joined.suffix + ".counts.json")
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.joined} ({len(rows)} rows)")
        return
    train, val = split_rows(rows, args.val_ratio)
    out = args.out_dir
    write_jsonl(out / "train.jsonl.gz", train)
    write_jsonl(out / "val.jsonl.gz", val)
    preview = []
    seen = set()
    for row in rows:
        k = row["meta"]["key"]
        if k not in seen:
            seen.add(k)
            preview.append(row)
    write_jsonl(out / "preview.jsonl", preview)
    report["train"] = counts_of(train)
    report["val"] = counts_of(val)
    (out / "counts.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} train={len(train)} val={len(val)}")


if __name__ == "__main__":
    main()
