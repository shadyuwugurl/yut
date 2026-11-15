#!/usr/bin/env python3
"""Default mix: hand-authored rows plus the curated seed. Procedural sample stays out."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from generate import counts_of, split_rows, write_jsonl  # noqa: E402
from safety import exact_hash  # noqa: E402


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> None:
    rows = []
    for path in sorted((HERE / "authored").glob("*.jsonl")):
        rows.extend(load_jsonl(path))
    rows.extend(load_jsonl(HERE / "seed.jsonl"))
    kept = [r for r in rows if r.get("meta", {}).get("source") in {"authored", "seed"}]
    dropped = len(rows) - len(kept)
    seen = set()
    unique = []
    for row in kept:
        digest = exact_hash(row["messages"])
        if digest in seen:
            continue
        seen.add(digest)
        unique.append(row)
    train, val = split_rows(unique, 0.1)
    out = HERE / "final"
    write_jsonl(out / "train.jsonl.gz", train)
    write_jsonl(out / "val.jsonl.gz", val)
    report = {
        "mix": "authored+seed",
        "excluded": "sample/ procedural draw",
        "dropped_source": dropped,
        "deduped": len(kept) - len(unique),
        "val_ratio": 0.1,
        **counts_of(unique),
        "train": counts_of(train),
        "val": counts_of(val),
    }
    (out / "counts.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"final rows={len(unique)} train={len(train)} val={len(val)} deduped={len(kept) - len(unique)}")


if __name__ == "__main__":
    main()
