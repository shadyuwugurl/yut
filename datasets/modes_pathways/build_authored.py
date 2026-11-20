#!/usr/bin/env python3
"""Write datasets/modes_pathways/authored/<category>__<id>.jsonl from the hand-written banks."""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from author_pack import specs_by_key, write_id  # noqa: E402
from authored_src import load_banks  # noqa: E402


def main() -> int:
    banks = load_banks()
    specs = specs_by_key()
    missing = [k for k in specs if k not in banks]
    extra = [k for k in banks if k not in specs]
    if extra:
        print("unknown keys", extra)
        return 1
    total = 0
    bad = 0
    for key in specs:
        rows = banks.get(key) or []
        if not rows:
            print(f"MISSING {key}")
            missing.append(key)
            continue
        n, errors = write_id(specs[key], rows)
        total += n
        if errors:
            bad += len(errors)
            print(f"{key} kept {n} errors {len(errors)}")
            for err in errors[:6]:
                print(" ", err)
        else:
            print(f"{key} {n}")
    print(f"authored rows {total} rejected {bad} missing_ids {len(set(missing))}")
    return 1 if bad or missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
