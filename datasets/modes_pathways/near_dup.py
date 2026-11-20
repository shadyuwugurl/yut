#!/usr/bin/env python3
"""Flag near-duplicate authored rows by 5-word shingles on user text plus the visible answer."""
from __future__ import annotations

import gzip
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from frame import split_think  # noqa: E402


def _load(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def _norm(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9']+", text.lower())
    return words


def _shingles(words: list[str], n: int = 5) -> set[tuple[str, ...]]:
    if len(words) < n:
        return {tuple(words)} if words else set()
    return {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}


def visible_blob(ex: dict) -> str:
    parts = []
    for msg in ex["messages"]:
        if msg["role"] == "user":
            parts.append(msg["content"])
        elif msg["role"] == "assistant":
            _think, visible = split_think(msg.get("content") or "")
            parts.append(visible)
    return "\n".join(parts)


def scan(paths: list[Path], threshold: float = 0.72) -> list[tuple[float, str, str]]:
    rows = []
    for path in paths:
        for i, ex in enumerate(_load(path)):
            words = _norm(visible_blob(ex))
            rows.append((f"{path.name}#{i}", _shingles(words), ex["meta"]["category"] + "/" + ex["meta"]["id"]))
    hits = []
    for i in range(len(rows)):
        a_id, a_set, a_key = rows[i]
        if not a_set:
            continue
        for j in range(i + 1, len(rows)):
            b_id, b_set, b_key = rows[j]
            if not b_set:
                continue
            inter = len(a_set & b_set)
            if not inter:
                continue
            score = inter / len(a_set | b_set)
            if score >= threshold:
                hits.append((score, f"{a_key} {a_id}", f"{b_key} {b_id}"))
    hits.sort(reverse=True)
    return hits


def main() -> int:
    root = HERE / "authored"
    paths = sorted(root.glob("*.jsonl"))
    if not paths:
        print("no authored jsonl")
        return 1
    hits = scan(paths)
    print(f"files {len(paths)} near_dups {len(hits)} threshold 0.72")
    for score, a, b in hits[:30]:
        print(f"{score:.2f}  {a}  ~  {b}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
