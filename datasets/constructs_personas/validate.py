#!/usr/bin/env python3
"""Validate construct/persona JSONL.

Checks schema, skinny-v1 canonical ids (aliases are not labels), role order,
think-block shape, private frame tags, and trigger-keyword leaks in user
text and visible assistant text.

  python3 datasets/constructs_personas/validate.py \\
      datasets/constructs_personas/seed.jsonl \\
      datasets/constructs_personas/sample/train.jsonl.gz \\
      datasets/constructs_personas/sample/val.jsonl.gz

  python3 datasets/constructs_personas/validate.py --self-test
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cp.filters import check_example  # noqa: E402
from cp.taxonomy import items, resolve  # noqa: E402


def _load(path: Path) -> list[dict]:
    opener = gzip.open if path.name.endswith(".gz") else open
    rows = []
    with opener(path, "rt", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{lineno}: {exc}") from exc
    return rows


def _self_test() -> int:
    cat, ident, alias = resolve("spoon")
    assert (cat, ident, alias) == ("construct", "research", "spoon"), (cat, ident, alias)
    cat, ident, alias = resolve("einstein")
    assert ident == "brainstorm" and alias == "einstein"
    cat, ident, alias = resolve("x007")
    assert ident == "007" and alias == "x007"
    cat, ident, alias = resolve("coder")
    assert ident == "coder" and alias is None
    cat, ident, alias = resolve("neutral")
    assert (cat, ident) == ("persona", "neutral")
    ids = {(it["category"], it["id"]) for it in items()}
    assert ("construct", "hyper") in ids
    assert ("construct", "business") in ids
    assert ("construct", "007") in ids
    assert ("persona", "pkd") in ids and ("persona", "house") in ids
    assert len([it for it in items() if it["category"] == "construct"]) == 33
    assert len([it for it in items() if it["category"] == "persona"]) == 31
    print("self-test ok")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--min-per-id", type=int, default=0, help="fail if any canonical id has fewer rows")
    args = parser.parse_args()
    if args.self_test:
        return _self_test()
    if not args.paths:
        parser.error("pass JSONL paths or --self-test")

    rows = []
    for raw in args.paths:
        rows.extend(_load(Path(raw)))
    problems = []
    for index, row in enumerate(rows):
        found = check_example(row)
        if found:
            ident = (row.get("meta") or {}).get("id")
            problems.append(f"row {index} ({ident}): {found[:6]}")
    counts = Counter(
        f"{(row.get('meta') or {}).get('category')}/{(row.get('meta') or {}).get('id')}"
        for row in rows
    )
    expected = [f"{it['category']}/{it['id']}" for it in items()]
    print(f"rows {len(rows)}  ids {len(counts)}  problems {len(problems)}")
    for key in expected:
        print(f"  {key}: {counts.get(key, 0)}")
    missing = [key for key in expected if counts.get(key, 0) < args.min_per_id]
    if missing:
        problems.append(f"below min {args.min_per_id}: {missing}")
    # Aliases must not be stored as ids.
    alias_ids = set()
    for it in items():
        for alias in it.get("aliases") or []:
            alias_ids.add(alias.lower())
    for row in rows:
        ident = str((row.get("meta") or {}).get("id") or "")
        if ident.lower() in alias_ids and ident not in {it["id"] for it in items()}:
            problems.append(f"alias stored as id: {ident}")
    if problems:
        print("\n".join(problems[:40]))
        if len(problems) > 40:
            print(f"... {len(problems) - 40} more")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
