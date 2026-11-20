#!/usr/bin/env python3
"""Train/val split of authored rows plus the seed. The procedural sample stays in sample/ and is not mixed in."""
from __future__ import annotations

import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHORED = HERE / "authored"
SEED = HERE / "seed.jsonl"
OUT = HERE / "final"


def _read_jsonl(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def main() -> int:
    rows = []
    seen = set()
    for path in sorted(AUTHORED.glob("*.jsonl")):
        for ex in _read_jsonl(path):
            sig = json.dumps(ex["messages"], ensure_ascii=False, sort_keys=True)
            if sig in seen:
                continue
            seen.add(sig)
            ex["meta"]["origin"] = "authored"
            rows.append(ex)
    authored_n = len(rows)
    if SEED.exists():
        for ex in _read_jsonl(SEED):
            sig = json.dumps(ex["messages"], ensure_ascii=False, sort_keys=True)
            if sig in seen:
                continue
            seen.add(sig)
            ex["meta"]["origin"] = "seed"
            rows.append(ex)
    groups = defaultdict(list)
    for ex in rows:
        groups[f"{ex['meta']['category']}/{ex['meta']['id']}"].append(ex)
    for group in groups.values():
        marked = False
        for i, ex in enumerate(group):
            blob = json.dumps(ex["messages"], ensure_ascii=False, sort_keys=True)
            bucket = int(hashlib.sha256(blob.encode()).hexdigest()[:8], 16) % 10000
            # Prefer authored rows in val when the group is mixed, but keep the hash rule.
            is_val = bucket < 200  # 2%
            ex["meta"]["split"] = "val" if is_val else "train"
            marked = marked or is_val
        if group and not marked:
            group[0]["meta"]["split"] = "val"
    train = [ex for ex in rows if ex["meta"]["split"] == "train"]
    val = [ex for ex in rows if ex["meta"]["split"] == "val"]
    OUT.mkdir(parents=True, exist_ok=True)
    for name, part in (("train.jsonl.gz", train), ("val.jsonl.gz", val)):
        with gzip.open(OUT / name, "wt", encoding="utf-8") as fh:
            for ex in part:
                fh.write(json.dumps(ex, ensure_ascii=False) + "\n")
    by = {}
    for ex in rows:
        key = f"{ex['meta']['category']}/{ex['meta']['id']}"
        slot = by.setdefault(key, {"train": 0, "val": 0, "authored": 0, "seed": 0})
        slot[ex["meta"]["split"]] += 1
        slot[ex["meta"]["origin"]] += 1
    report = {
        "mix": "authored + seed",
        "excluded": "datasets/modes_pathways/sample (procedural)",
        "authored": authored_n,
        "total": len(rows),
        "train": len(train),
        "val": len(val),
        "by_id": by,
    }
    (OUT / "counts.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"final authored={authored_n} total={len(rows)} train={len(train)} val={len(val)} ids={len(by)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
