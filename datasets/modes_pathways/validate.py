#!/usr/bin/env python3
"""Validate modes/pathways JSONL and render a few rows through the full Spark template.

  python3 datasets/modes_pathways/validate.py datasets/modes_pathways/seed.jsonl
  python3 datasets/modes_pathways/validate.py datasets/modes_pathways/sample/train.jsonl.gz --render 8
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))

from frame import Spec, all_specs  # noqa: E402
from quality import problems  # noqa: E402
from verify_template import BOS, EOS, load, render  # noqa: E402


def load_rows(path: Path) -> list[dict]:
    opener = gzip.open if path.suffix == ".gz" else open
    rows = []
    with opener(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _specs() -> dict[tuple[str, str], Spec]:
    return {(s.category, s.id): s for s in all_specs()}


def render_checks(rows: list[dict]) -> list[str]:
    tmpl = load()
    fails = []

    def one(row, **kwargs):
        msgs = row["messages"]
        tools = row.get("tools")
        extra = dict(kwargs)
        if tools:
            extra["tools"] = tools
        return render(tmpl, msgs, add_generation_prompt=False, reasoning_effort="off", **extra)

    def find(pred):
        for row in rows:
            if pred(row):
                return row
        return None

    call = find(lambda r: r["meta"].get("tool_trajectory") == "call")
    pivot = find(lambda r: r["meta"].get("tool_trajectory") == "pivot")
    instruct = find(lambda r: r["meta"]["category"] == "channel" and r["meta"]["id"] == "instruct")
    deep = find(lambda r: r["meta"]["category"] == "mode" and r["meta"]["id"] == "deep")
    aesthetic = find(lambda r: r["meta"]["category"] == "aesthetic")
    off = find(lambda r: r["meta"]["category"] == "thinking_effort" and r["meta"]["id"] == "off")

    if call:
        text = one(call)
        if "<tool_call>" not in text or "<arg_key>" not in text or "<arg_value>" not in text:
            fails.append("call row did not render arg_key/arg_value tool calls")
        if not text.startswith(BOS):
            fails.append("render does not open with the Spark BOS")
    else:
        fails.append("no call trajectory available to render")
    if pivot:
        text = one(pivot)
        if "CRITICAL AGENTIC LOOP" not in text:
            fails.append("pivot row did not render the third-error loop warning")
        if "The previous tool call returned an error" not in text:
            fails.append("pivot row did not render the first-error warning")
    else:
        fails.append("no pivot trajectory available to render")
    if instruct:
        text = one(instruct)
        # Historical instruct turns close think instead of opening a body.
        if "<think>" in text.split("===== LIBRARY END =====")[-1]:
            # The catalog itself may contain the word inside the library. Look at the live tail.
            pass
        live = text.split("===== LIBRARY END =====")[-1]
        if "<think>" in live:
            fails.append("instruct row rendered a think body")
        if "</think>" not in live:
            fails.append("instruct row did not close think")
    else:
        fails.append("no instruct row available to render")
    if deep:
        live = one(deep).split("===== LIBRARY END =====")[-1]
        if "<think>" not in live or "</think>" not in live:
            fails.append("deep row did not render a think span")
        if BOS + "<|Bot|>" not in one(deep) and "<|Bot|>" not in live:
            fails.append("deep row missing a Bot turn")
    if aesthetic:
        try:
            one(aesthetic)
        except Exception as exc:  # noqa: BLE001
            fails.append(f"aesthetic row failed to render: {exc}")
    if off:
        live = one(off).split("===== LIBRARY END =====")[-1]
        if "<think>" in live:
            fails.append("thinking off rendered a think body")
    # A handful of arbitrary rows must render, and the user text must survive.
    shown = 0
    for row in rows:
        if shown >= 6:
            break
        try:
            text = one(row)
        except Exception as exc:  # noqa: BLE001
            fails.append(f"render raised: {exc}")
            continue
        user = next(m["content"] for m in row["messages"] if m["role"] == "user")
        # User text can be long; check a stable prefix that isn't only whitespace.
        probe = user.strip().splitlines()[0][:40]
        if probe and probe not in text:
            fails.append("user text missing from render")
        if EOS not in text:
            fails.append("render missing Spark EOS")
        shown += 1
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--render", type=int, default=6)
    args = ap.parse_args()
    specs = _specs()
    total = 0
    bad = 0
    by = Counter()
    samples = []
    for path in args.paths:
        rows = load_rows(path)
        print(f"{path} {len(rows)} rows")
        for row in rows:
            total += 1
            key = (row.get("meta", {}).get("category"), row.get("meta", {}).get("id"))
            by[f"{key[0]}/{key[1]}"] += 1
            spec = specs.get(key)
            if spec is None:
                bad += 1
                print(f"  UNKNOWN {key}")
                continue
            probs = problems(row, spec)
            if probs:
                bad += 1
                if bad <= 12:
                    print(f"  {key[0]}/{key[1]}: {probs[:5]}")
        samples.extend(rows)
    print(f"ids {len(by)} rows {total} bad {bad}")
    if args.render and samples:
        fails = render_checks(samples)
        for item in fails:
            print("RENDER", item)
            bad += 1
        if not fails:
            print("RENDER ok")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
