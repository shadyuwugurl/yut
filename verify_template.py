#!/usr/bin/env python3
"""Verify Sharp-Spark v5.0.0 chat template.

Usage:
  python3 verify_template.py
  python3 verify_template.py --show-render
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from jinja2 import Environment

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "chat_template.jinja"

def raise_exception(msg):
    raise Exception(msg)

def load():
    env = Environment()
    env.globals["raise_exception"] = raise_exception
    return env.from_string(TEMPLATE.read_text())

def render(tmpl, messages, **kwargs):
    return tmpl.render(messages=messages, add_generation_prompt=True, **kwargs)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show-render", action="store_true")
    args = ap.parse_args()
    tmpl = load()
    fails = []

    def check(ok: bool, label: str):
        print(f"{'PASS' if ok else 'FAIL'}  {label}")
        if not ok:
            fails.append(label)

    # 1. Parse + empty
    try:
        render(tmpl, [])
        check(False, "empty messages must raise")
    except Exception as e:
        check("No messages" in str(e), "empty messages raises")

    # 2. Invalid effort
    try:
        render(tmpl, [{"role":"user","content":"x"}], reasoning_effort="banana")
        check(False, "invalid effort must raise")
    except Exception as e:
        check("reasoning_effort must be one of" in str(e), "invalid effort raises")

    # 3. Frame card always present (no keyword needed)
    out = render(tmpl, [{"role":"user","content":"hi"}], reasoning_effort="off")
    check("FRAME CARD" in out, "frame card always present")
    check("silently choose" in out.lower() or "silently choose" in out, "silent-choice rule present")
    check("CONSTRUCT (pick one)" in out, "construct inventory present")
    check("PERSONA (pick one" in out, "persona inventory present")
    check("IDENTITY (pick one" in out, "identity inventory present")
    # No keyword-triggered detailed blocks on plain "hi"
    check("CODER MODE" not in out, "no coder block without override")
    check("FEMBOY IDENTITY" not in out, "no femboy block without override")

    # 4. Explicit overrides still work
    out = render(tmpl, [{"role":"user","content":"hi"}], construct="coder", reasoning_effort="off")
    check("CODER MODE (forced)" in out, "explicit construct=coder emits forced block")

    out = render(tmpl, [{"role":"user","content":"hi"}], persona="friend", reasoning_effort="off")
    check("FRIEND PERSONA (forced)" in out, "explicit persona=friend emits forced block")

    out = render(tmpl, [{"role":"user","content":"hi"}], identity="femboy", reasoning_effort="off")
    check("FEMBOY IDENTITY (forced)" in out, "explicit identity=femboy emits forced block")

    # 5. Reasoning tiers
    for tier, expect_think in [("off", False), ("low", True), ("high", True), ("soft", True)]:
        out = render(tmpl, [{"role":"user","content":"hi"}], reasoning_effort=tier)
        has = "<think>" in out.split("<|Bot|>")[-1]
        check(has == expect_think, f"reasoning_effort={tier} thinking_open={has}")

    out = render(tmpl, [{"role":"user","content":"hi"}], enable_thinking=False, reasoning_effort="high")
    check("<think>" not in out.split("<|Bot|>")[-1], "enable_thinking=False forces off")

    # 6. Tools
    tools = [{"type":"function","function":{"name":"get_weather","description":"Get weather","parameters":{"type":"object","properties":{"city":{"type":"string"}}}}}]
    out = render(tmpl, [{"role":"user","content":"weather?"}], tools=tools, reasoning_effort="off")
    check("<tools>" in out and "get_weather" in out, "tools block renders")

    msgs = [
        {"role":"user","content":"weather?"},
        {"role":"assistant","content":"","tool_calls":[{"function":{"name":"get_weather","arguments":{"city":"Sydney"}}}]},
        {"role":"tool","content":"22C"},
    ]
    out = render(tmpl, msgs, tools=tools, reasoning_effort="off")
    check("<tool_call>get_weather" in out and "<tool_response>22C</tool_response>" in out, "tool call + response path")

    # 7. Content blocks
    out = render(tmpl, [{"role":"user","content":[{"type":"text","text":"block hello"}]}], reasoning_effort="off")
    check("block hello" in out, "content list-of-blocks works")

    # 8. No keyword routing residual
    # Old v4 would have turned "code this" into coder mode automatically.
    out = render(tmpl, [{"role":"user","content":"please code a binary search"}], reasoning_effort="off")
    check("CODER MODE" not in out, "keyword 'code' does NOT auto-trigger coder block")
    check("FRAME CARD" in out, "still has frame card so model can choose coder itself")

    # 9. Generation prompt shape
    out = render(tmpl, [{"role":"user","content":"x"}], reasoning_effort="medium")
    check(out.rstrip().endswith("<|Bot|><think>") or out.rstrip().endswith("<|Bot|></think>"), "generation prompt ends correctly")

    if args.show_render:
        print("\n----- sample render (off, no overrides) -----")
        print(render(tmpl, [{"role":"user","content":"hi"}], reasoning_effort="off")[:2000])
        print("...")

    print()
    if fails:
        print(f"{len(fails)} FAIL(s)")
        for f in fails:
            print(" ", f)
        return 1
    print("ALL PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
