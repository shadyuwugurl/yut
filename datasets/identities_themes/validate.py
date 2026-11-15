#!/usr/bin/env python3
"""Validate identity/theme jsonl (plain or gzip) against skinny-v1 labels and the walls."""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from canonical import load_canon, make_frame  # noqa: E402
from safety import check_record, exact_hash  # noqa: E402


def load_rows(paths: list[Path]) -> list[dict]:
    rows = []
    for path in paths:
        opener = gzip.open if str(path).endswith(".gz") else open
        with opener(path, "rt", encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"{path}:{line_no}: {exc}") from exc
    return rows


def self_test() -> None:
    canon = load_canon()
    assert canon.version == "skinny-v1"
    assert len([i for i in canon.identities if i != "none"]) == 34
    assert len([t for t in canon.themes if t != "none"]) == 8
    for alias in (
        "josie_v2", "josie_r1", "j.o.s.i.e.-r.1", "josie_base", "josie_v6",
        "josie_v4o", "josie_openwebui", "j.o.s.i.e.", "Josie v2", "Josie OpenWebUI",
    ):
        cat, id_, stored = canon.resolve(alias)
        assert (cat, id_) == ("identity", "josie"), alias
        assert id_ != alias
        assert stored != "josie"
    cat, id_, stored = canon.resolve("josie")
    assert (cat, id_, stored) == ("identity", "josie", None)
    # A forged alias label must not validate.
    bad = {
        "messages": [
            {"role": "user", "content": "I am a 31-year-old adult. What is 12 times 3 plus 1?"},
            {"role": "assistant", "content": "37. Twelve times three is 36, plus one is 37. Multiply, then add."},
        ],
        "meta": {
            "taxonomy": "skinny-v1",
            "category": "identity",
            "id": "josie_v2",
            "key": "identity/josie_v2",
            "identity": "josie_v2",
            "theme": "none",
            "labels": ["identity/josie_v2", "theme/none"],
            "switch": False,
            "switch_from": None,
            "switch_to": None,
            "shape": "single",
            "source": "seed",
            "think": False,
            "input_alias": None,
            "frame": {},
        },
    }
    assert check_record(bad, canon) in {"id", "alias-label", "dial", "frame-keys"}
    minor = json.loads(json.dumps(bad))
    minor["meta"]["id"] = "josie"
    minor["meta"]["identity"] = "josie"
    minor["meta"]["key"] = "identity/josie"
    minor["meta"]["labels"] = ["identity/josie", "theme/none"]
    minor["meta"]["frame"] = make_frame(canon, identity="josie", theme="none", task="chat", think_text="")
    minor["messages"][0]["content"] = "The child in the room is 12 years old and asked a question about the weather today."
    assert check_record(minor, canon) == "minor", check_record(minor, canon)
    print("self-test ok")


def near_duplicates(rows: list[dict], threshold: float = 0.55) -> list[tuple[int, int, float]]:
    """Flag pairs whose assistant word-shingles overlap too much."""
    def shingles(row: dict) -> set[str]:
        text = " ".join(
            m["content"].split("</think>")[-1].lower()
            for m in row["messages"]
            if m["role"] == "assistant"
        )
        words = [w for w in text.split() if w]
        return {" ".join(words[i:i + 5]) for i in range(max(0, len(words) - 4))}

    bags = [(i, shingles(r), r["meta"]["key"]) for i, r in enumerate(rows)]
    hits = []
    by: dict[str, list[tuple[int, set[str]]]] = {}
    for i, bag, key in bags:
        by.setdefault(key, []).append((i, bag))
    for group in by.values():
        for a in range(len(group)):
            ia, ba = group[a]
            if not ba:
                continue
            for b in range(a + 1, len(group)):
                ib, bb = group[b]
                if not bb:
                    continue
                inter = len(ba & bb)
                if not inter:
                    continue
                score = inter / len(ba | bb)
                if score >= threshold:
                    hits.append((ia, ib, round(score, 3)))
    return hits


def main() -> None:
    p = argparse.ArgumentParser(description="Validate identity/theme jsonl")
    p.add_argument("paths", nargs="*", type=Path)
    p.add_argument("--min-per-id", type=int, default=None)
    p.add_argument("--max-per-id", type=int, default=None)
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--near", type=float, default=None, help="flag assistant shingle Jaccard at or above this")
    p.add_argument("--require-all", action="store_true", help="fail if any training id is absent")
    args = p.parse_args()
    if args.self_test:
        self_test()
        if not args.paths:
            return
    if not args.paths:
        raise SystemExit("give jsonl paths or --self-test")
    canon = load_canon()
    rows = load_rows(args.paths)
    errors = Counter()
    seen = set()
    per = Counter()
    alias_as_id = []
    josie_aliases = Counter()
    for i, row in enumerate(rows):
        reason = check_record(row, canon)
        if reason:
            errors[reason] += 1
            if errors[reason] <= 3:
                print(f"row {i}: {reason} key={row.get('meta', {}).get('key')}")
            continue
        digest = exact_hash(row["messages"])
        if digest in seen:
            errors["dup"] += 1
        seen.add(digest)
        per[row["meta"]["key"]] += 1
        if row["meta"]["id"] == "josie" and row["meta"].get("input_alias"):
            josie_aliases[row["meta"]["input_alias"]] += 1
        if canon.is_alias(row["meta"]["id"]) or canon.is_alias(row["meta"]["identity"]) or canon.is_alias(row["meta"]["theme"]):
            alias_as_id.append(row["meta"]["key"])
    expected = [f"{c}/{i}" for c, i in canon.training_pairs()]
    missing = [k for k in expected if per[k] == 0]
    bad_range = []
    for key, n in per.items():
        if args.min_per_id is not None and n < args.min_per_id:
            bad_range.append(f"{key}={n}<{args.min_per_id}")
        if args.max_per_id is not None and n > args.max_per_id:
            bad_range.append(f"{key}={n}>{args.max_per_id}")
    near_hits = near_duplicates(rows, args.near) if args.near is not None else []
    print(json.dumps({
        "rows": len(rows),
        "ok": len(rows) - sum(errors.values()),
        "errors": dict(errors),
        "ids": len(per),
        "missing": missing if args.require_all else [],
        "absent": [] if args.require_all else missing,
        "range": bad_range,
        "alias_labels": alias_as_id,
        "near_duplicates": len(near_hits),
        "near_sample": [{"a": a, "b": b, "score": s} for a, b, s in near_hits[:8]],
        "josie_input_alias": dict(sorted(josie_aliases.items())),
        "per_id": dict(sorted(per.items())),
    }, indent=2))
    if errors or bad_range or alias_as_id or near_hits or (args.require_all and missing):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
