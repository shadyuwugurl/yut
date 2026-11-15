#!/usr/bin/env python3
"""Render-check the skinny Spark chat template.

Same cases as scripts/verify_template.py for the wire that must not change
(plain chat, multi-turn, tools, tool errors, overrides, clipping), pointed at
templates/skinny/chat_template.jinja. Prints the cl100k_base token count of a
one-message "hi" render.

Usage:
  python3 scripts/verify_skinny.py
  python3 scripts/verify_skinny.py --show-render
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from jinja2 import Environment

REPO = Path(__file__).resolve().parent.parent
SKINNY = REPO / "templates" / "skinny" / "chat_template.jinja"
ROOT_COPY = REPO / "chat_template_skinny.jinja"
FULL = REPO / "chat_template.jinja"
TAXONOMY = REPO / "docs" / "taxonomy_skinny.json"

BOS = "<\uFF5Cstart\u2581of\u2581sentence\uFF5C>"
EOS = "<\uFF5Cend\u2581of\u2581sentence\uFF5C>"
GUIDE_LINE = re.compile(r"^([a-z0-9][a-z0-9_-]*) — ")


def raise_exception(msg):
    raise Exception(msg)


def load():
    env = Environment()
    env.globals["raise_exception"] = raise_exception
    return env.from_string(SKINNY.read_text())


def render(tmpl, messages, add_generation_prompt=True, **kwargs):
    return tmpl.render(
        messages=messages,
        add_generation_prompt=add_generation_prompt,
        **kwargs,
    )


def tokens(text: str) -> int:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text, disallowed_special=()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show-render", action="store_true")
    args = ap.parse_args()
    fails = []

    def check(ok: bool, label: str):
        print(f"{'PASS' if ok else 'FAIL'}  {label}")
        if not ok:
            fails.append(label)

    check(SKINNY.is_file() and ROOT_COPY.is_file(), "skinny template and root copy exist")
    check(SKINNY.read_text() == ROOT_COPY.read_text(), "templates/skinny and chat_template_skinny.jinja match")
    full = FULL.read_text()
    check("===== CATALOG =====" in full, "full root template was not replaced")
    check(SKINNY.stat().st_size < FULL.stat().st_size // 5, "skinny file is much smaller than the full template")

    tax = json.loads(TAXONOMY.read_text())
    items = tax["items"]
    expected_ids = Counter(item["id"] for item in items)
    tmpl = load()

    try:
        render(tmpl, [])
        check(False, "empty messages must raise")
    except Exception as e:
        check("No messages" in str(e), "empty messages raises")

    try:
        render(tmpl, [{"role": "user", "content": "x"}], reasoning_effort="banana")
        check(False, "invalid effort must raise")
    except Exception as e:
        check("mode must be one of" in str(e), "invalid effort raises")

    plain = render(tmpl, [{"role": "user", "content": "hi"}])
    check(plain.startswith(BOS + "<|System|>"), "plain chat opens a System turn")
    check("USE X FOR Y" in plain, "decision guide present")
    check("GENTLE DEFAULTS" in plain, "gentle defaults present")
    check("ORBIT" in plain and "contextual_sanity" in plain, "orbit fundamentals present")
    check("ON THE FLY" in plain and "Do not wait for a keyword" in plain, "on-the-fly rule present")
    check("chosen silently" not in plain and "FRAME CARD" not in plain, "long frame card is not copied")
    check("===== CATALOG =====" not in plain, "sourced catalog is absent")
    check("engram" not in plain.lower(), "engram text is absent")
    check("<|im_start|>" not in plain and "<|vision_start|>" not in plain, "no ChatML or Qwen vision tokens")
    for foreign in ("<start_of_turn>", "<|start_header_id|>", "[INST]", "[gMASK]", "<|turn>", "<|im_end|>"):
        check(foreign not in plain, f"foreign token absent: {foreign}")
    check(BOS + "<|User|>hi" + EOS in plain, "user turn uses Spark tokens")
    check(plain.rstrip().endswith("<|Bot|><think>"), "default generation prompt opens think")
    check("thinking_effort=high" in plain, "auto system maps to native high")
    check("CONSTRUCT LOCKED" not in plain, "plain chat has no construct lock")
    check("SYSTEM WARNING" not in plain, "plain chat does not invent a tool warning")

    found = Counter()
    for line in plain.splitlines():
        match = GUIDE_LINE.match(line)
        if match:
            found[match.group(1)] += 1
    check(found == expected_ids, "guide lines match taxonomy ids one-for-one")

    closed = render(tmpl, [{"role": "user", "content": "hi"}], add_generation_prompt=False)
    check("<|Bot|>" not in closed, "no generation prompt when add_generation_prompt is false")
    check(BOS + "<|User|>hi" + EOS in closed, "user turn still rendered without generation prompt")

    codey = render(tmpl, [{"role": "user", "content": "please code a binary search"}], reasoning_effort="off")
    check(codey.count("CONSTRUCT LOCKED (forced):") == plain.count("CONSTRUCT LOCKED (forced):"),
          "keyword 'code' does not add a construct lock")

    locked = render(tmpl, [{"role": "user", "content": "hi"}], mode="code", reasoning_effort="off")
    check("MODE LOCKED (forced): system=s2, mode=code." in locked, "mode=code locks s2/code")

    coder = render(tmpl, [{"role": "user", "content": "hi"}], construct="coder", reasoning_effort="off")
    check(coder.count("CONSTRUCT LOCKED (forced): coder.") == 1, "construct=coder adds one lock")
    friend = render(tmpl, [{"role": "user", "content": "hi"}], persona="friend", reasoning_effort="off")
    check("PERSONA LOCKED (forced): friend." in friend, "persona=friend locks")
    femboy = render(tmpl, [{"role": "user", "content": "hi"}], identity="femboy", reasoning_effort="off")
    check("IDENTITY LOCKED (forced): femboy." in femboy, "identity=femboy locks")
    theme = render(tmpl, [{"role": "user", "content": "hi"}], theme="cerebral", reasoning_effort="off")
    check("THEME LOCKED (forced): cerebral." in theme, "theme=cerebral locks")
    josie = render(tmpl, [{"role": "user", "content": "hi"}], identity="josie", reasoning_effort="off")
    check("IDENTITY LOCKED (forced): josie." in josie, "identity=josie locks")
    styled = render(tmpl, [{"role": "user", "content": "hi"}], aesthetic_preset="luxury", reasoning_effort="off")
    check("AESTHETIC PRESET (forced): luxury." in styled, "aesthetic_preset=luxury locks")
    leveled = render(tmpl, [{"role": "user", "content": "hi"}], protium_level="artemis", reasoning_effort="off")
    check("PROTIUM LEVEL (forced): artemis." in leveled, "protium_level=artemis locks")
    hyper = render(tmpl, [{"role": "user", "content": "hi"}], construct="hyper", reasoning_effort="off")
    check("CONSTRUCT LOCKED (forced): hyper." in hyper, "construct=hyper locks a catalog construct")
    house = render(tmpl, [{"role": "user", "content": "hi"}], persona="house", reasoning_effort="off")
    check("PERSONA LOCKED (forced): house." in house, "persona=house locks a catalog persona")
    ignored = render(tmpl, [{"role": "user", "content": "hi"}], construct="not-a-construct", persona="not-a-persona", reasoning_effort="off")
    check("CONSTRUCT LOCKED" not in ignored and "PERSONA LOCKED" not in ignored, "unknown construct and persona are ignored")
    neutral = render(tmpl, [{"role": "user", "content": "hi"}], persona="neutral", identity="none", theme="none", reasoning_effort="off")
    check("PERSONA LOCKED" not in neutral and "IDENTITY LOCKED" not in neutral and "THEME LOCKED" not in neutral,
          "neutral/none overrides add no lock line")

    sys_lock = render(tmpl, [{"role": "user", "content": "hi"}], system="s1")
    check("SYSTEM LOCKED (forced): s1." in sys_lock, "system=s1 locks the pathway")
    check("thinking_effort=low" in sys_lock, "s1 maps to native low")

    for tier, expect_open, effort in (
        ("off", False, None),
        ("low", True, "low"),
        ("high", True, "high"),
        ("soft", True, "low"),
    ):
        out = render(tmpl, [{"role": "user", "content": "hi"}], reasoning_effort=tier)
        tail = out[out.rfind("<|Bot|>"):]
        opened = tail.endswith("<think>")
        check(opened == expect_open, f"reasoning_effort={tier} thinking_open={opened}")
        if effort:
            check(f"thinking_effort={effort}" in out, f"reasoning_effort={tier} native effort={effort}")

    extreme = render(tmpl, [{"role": "user", "content": "hi"}], reasoning_effort="xhigh")
    check("MODE LOCKED (forced): system=s2, mode=extreme." in extreme, "xhigh remaps to mode extreme")
    deep = render(tmpl, [{"role": "user", "content": "hi"}], reasoning_effort="medium")
    check("MODE LOCKED (forced): system=s2, mode=deep." in deep, "medium remaps to mode deep")
    mixed = render(tmpl, [{"role": "user", "content": "hi"}], reasoning_effort="mix")
    check("CONSTRUCT LOCKED (forced): kitbash." in mixed, "mix with no construct forces kitbash")
    check("MODE LOCKED" not in mixed, "mix leaves the mode unlocked")

    off = render(tmpl, [{"role": "user", "content": "hi"}], enable_thinking=False, reasoning_effort="high")
    check(off.rstrip().endswith("<|Bot|></think>"), "enable_thinking=False forces a closed think tag")
    check("thinking_effort=" not in off, "thinking off omits the thinking_effort line")

    msgs = [
        {"role": "system", "content": "SYSTEM_SENTINEL"},
        {"role": "user", "content": "first question"},
        {"role": "assistant", "content": "first answer", "reasoning_content": "because"},
        {"role": "user", "content": "second question"},
        {"role": "system", "content": "LATER_SYSTEM"},
    ]
    out = render(tmpl, msgs)
    user_at = out.find("<|User|>")
    check("SYSTEM_SENTINEL" in out[:user_at], "caller system prompt is inside the first System turn")
    check(BOS + "<|User|>first question" + EOS in out, "first user turn present")
    check("<think>because</think>first answer" in out, "assistant reasoning and content use think tags")
    check(BOS + "<|User|>second question" + EOS in out, "second user turn present")
    check(BOS + "<|System|>\nLATER_SYSTEM" + EOS in out, "later system message is its own turn")
    check(out.rstrip().endswith("<|Bot|><think>"), "multi-turn generation prompt opens think")

    mapped = render(
        tmpl,
        [{"role": "user", "content": "q"}, {"role": "assistant", "content": "a", "thinking": {"text": "mapped"}}],
        add_generation_prompt=False,
        reasoning_effort="off",
    )
    check("<think>mapped</think>a" in mapped, "thinking.text is accepted as reasoning")
    dropped = render(
        tmpl,
        [{"role": "user", "content": "q"}, {"role": "assistant", "content": "a", "reasoning_content": "secret"}],
        add_generation_prompt=False,
        reasoning_effort="off",
        preserve_thinking=False,
    )
    check("<think>secret</think>" not in dropped and "</think>a" in dropped, "preserve_thinking=false drops past reasoning")

    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather",
            "parameters": {"type": "object", "properties": {"city": {"type": "string"}}},
        },
    }]
    out = render(tmpl, [{"role": "user", "content": "weather?"}], tools=tools, reasoning_effort="off")
    check("<tools>" in out and "get_weather" in out and "## Tools" in out, "tools block renders")

    tool_msgs = [
        {"role": "user", "content": "weather?"},
        {"role": "assistant", "content": "", "tool_calls": [
            {"function": {"name": "get_weather", "arguments": {"city": "Sydney"}}},
            {"function": {"name": "get_time", "arguments": '{"tz":"UTC"}'}},
        ]},
        {"role": "tool", "content": "22C"},
        {"role": "tool", "content": "03:00"},
    ]
    out = render(tmpl, tool_msgs, tools=tools, reasoning_effort="off", add_generation_prompt=False)
    check("<tool_call>get_weather<arg_key>city</arg_key><arg_value>Sydney</arg_value></tool_call>" in out,
          "dict tool arguments use arg_key/arg_value")
    check('<tool_call>get_time<arg_value>{"tz":"UTC"}</arg_value></tool_call>' in out,
          "string tool arguments pass through verbatim")
    check(out.count("<|Tool|>") == 1, "consecutive tool results share one Tool turn")
    check("<tool_response>22C</tool_response>" in out and "<tool_response>03:00</tool_response>" in out,
          "both tool responses render")

    params_out = render(
        tmpl,
        [
            {"role": "user", "content": "weather?"},
            {"role": "assistant", "content": "", "tool_calls": [
                {"function": {"name": "get_weather", "parameters": {"city": "Sydney"}}},
            ]},
        ],
        add_generation_prompt=False,
        reasoning_effort="off",
    )
    check("<arg_key>city</arg_key><arg_value>Sydney</arg_value>" in params_out, "tool arguments read from function.parameters")
    input_out = render(
        tmpl,
        [
            {"role": "user", "content": "weather?"},
            {"role": "assistant", "content": "", "tool_calls": [
                {"function": {"name": "get_weather", "input": {"city": "Melbourne"}}},
            ]},
        ],
        add_generation_prompt=False,
        reasoning_effort="off",
    )
    check("<arg_value>Melbourne</arg_value>" in input_out, "tool arguments read from function.input")

    clipped = render(
        tmpl,
        [
            {"role": "user", "content": "go"},
            {"role": "assistant", "content": "", "tool_calls": [
                {"function": {"name": "run", "arguments": {"cmd": "abcdefghij"}}},
            ]},
            {"role": "tool", "content": "0123456789OK"},
        ],
        add_generation_prompt=False,
        reasoning_effort="off",
        max_tool_arg_chars=4,
        max_tool_response_chars=4,
    )
    check("<arg_value>abcd [TRUNCATED]</arg_value>" in clipped, "max_tool_arg_chars clips arguments")
    check("<tool_response>0123 [TRUNCATED]" in clipped, "max_tool_response_chars clips tool responses")

    err_out = render(
        tmpl,
        [
            {"role": "user", "content": "go"},
            {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "run", "arguments": {"cmd": "x"}}}]},
            {"role": "tool", "content": "failed to open socket"},
        ],
        add_generation_prompt=False,
        reasoning_effort="off",
    )
    check("The previous tool call returned an error" in err_out, "first tool error appends the tier-1 warning")
    pair = [
        {"role": "user", "content": "go"},
        {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "run", "arguments": {"cmd": "x"}}}]},
        {"role": "tool", "content": "failed to open"},
        {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "run", "arguments": {"cmd": "y"}}}]},
        {"role": "tool", "content": "connection refused"},
    ]
    pair_out = render(tmpl, pair, add_generation_prompt=False, reasoning_effort="off")
    check("2 consecutive tool errors" in pair_out, "second consecutive tool error appends the tier-2 warning")
    triple = [{"role": "user", "content": "go"}]
    for _ in range(3):
        triple.append({"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "run", "arguments": {"cmd": "x"}}}]})
        triple.append({"role": "tool", "content": "failed to open"})
    triple_out = render(tmpl, triple, add_generation_prompt=False, reasoning_effort="off")
    check("CRITICAL AGENTIC LOOP" in triple_out, "third consecutive tool error appends the loop warning")
    code_ok = render(
        tmpl,
        [
            {"role": "user", "content": "go"},
            {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "run", "arguments": {"cmd": "x"}}}]},
            {"role": "tool", "content": "def add(a, b):\n    return a + b\n"},
        ],
        add_generation_prompt=False,
        reasoning_effort="off",
    )
    check("SYSTEM WARNING" not in code_ok, "a code-shaped tool response is not treated as an error")

    blocks = render(
        tmpl,
        [{"role": "user", "content": [{"type": "text", "text": "block hello"}]}],
        reasoning_effort="off",
    )
    check("block hello" in blocks, "content list-of-blocks works")
    try:
        render(tmpl, [{"role": "user", "content": [{"type": "image", "image": "x"}]}], reasoning_effort="off")
        check(False, "image blocks must raise")
    except Exception as e:
        check("Unsupported" in str(e), "image blocks raise")

    try:
        render(tmpl, [{"role": "observer", "content": "x"}])
        check(False, "unknown role must raise")
    except Exception as e:
        check("Unsupported message role" in str(e), "unknown role raises")

    n = tokens(plain)
    check(1500 <= n <= 4000, f"hi render is inside 1.5k-4k cl100k tokens ({n})")

    if args.show_render:
        print("\n----- skinny hi render (head) -----")
        print(plain[:1500])
        print("...")

    print()
    print(f"RENDER SIZE  chars={len(plain)} file_bytes={SKINNY.stat().st_size}")
    print(f"TOKEN ESTIMATE  cl100k_base {n} tokens (not the Spark tokenizer; none is in the repo)")
    print("WINDOW  native context 1048576; skinny target band 1500-4000 for a one-message hi")
    print()
    if fails:
        print(f"{len(fails)} FAIL(s)")
        for label in fails:
            print(" ", label)
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
