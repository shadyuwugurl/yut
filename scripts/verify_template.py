#!/usr/bin/env python3
"""Render-check chat_template.jinja for xhtoken spark 2.6 4b.

Renders the way Hugging Face transformers apply_chat_template does: a Jinja2
environment, a raise_exception global, and the messages / tools / generation
kwargs the caller passes. No tokenizer weights are required.

Usage:
  python3 scripts/verify_template.py
  python3 scripts/verify_template.py --show-render
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jinja2 import Environment

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "chat_template.jinja"

BOS = "<\uFF5Cstart\u2581of\u2581sentence\uFF5C>"
EOS = "<\uFF5Cend\u2581of\u2581sentence\uFF5C>"


def raise_exception(msg):
    raise Exception(msg)


def load():
    env = Environment()
    env.globals["raise_exception"] = raise_exception
    return env.from_string(TEMPLATE.read_text())


def render(tmpl, messages, add_generation_prompt=True, **kwargs):
    return tmpl.render(
        messages=messages,
        add_generation_prompt=add_generation_prompt,
        **kwargs,
    )


def live(text: str) -> str:
    """Conversation wire after the inlined library."""
    marker = "=" * 5 + " LIBRARY END " + "=" * 5
    return text.split(marker, 1)[-1]


def head(text: str) -> str:
    """System instructions before the inlined library."""
    return text.split("===== LIBRARY =====", 1)[0]


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

    # 1. Empty messages
    try:
        render(tmpl, [])
        check(False, "empty messages must raise")
    except Exception as e:
        check("No messages" in str(e), "empty messages raises")

    # 2. Invalid effort / mode
    try:
        render(tmpl, [{"role": "user", "content": "x"}], reasoning_effort="banana")
        check(False, "invalid effort must raise")
    except Exception as e:
        check("mode must be one of" in str(e), "invalid effort raises")

    # 3. Plain chat, generation prompt on (thinking default = open / high)
    plain = render(tmpl, [{"role": "user", "content": "hi"}])
    check(plain.startswith(BOS + "<|System|>"), "plain chat opens a System turn")
    check("FRAME CARD" in plain, "frame card always present")
    check("chosen silently" in plain, "silent-choice rule present")
    check("CONSTRUCTS (dial 2" in plain, "construct inventory present")
    check("PERSONAS (dial 3" in plain, "persona inventory present")
    check("IDENTITIES (dial 4" in plain, "identity inventory present")
    check("THEMES (dial 5" in plain, "theme inventory present")
    check("<|im_start|>" not in plain and "<|vision_start|>" not in plain, "no ChatML or Qwen vision tokens")
    for foreign in ("<start_of_turn>", "<|start_header_id|>", "[INST]", "[gMASK]", "<|turn>", "<|im_end|>"):
        check(foreign not in plain, f"foreign token absent: {foreign}")
    check(BOS + "<|User|>hi" + EOS in plain, "user turn uses Spark tokens")
    check(plain.rstrip().endswith("<|Bot|><think>"), "default generation prompt opens think")
    check("thinking_effort=high" in plain, "auto system maps to native high")

    # 4. add_generation_prompt false
    closed = render(tmpl, [{"role": "user", "content": "hi"}], add_generation_prompt=False)
    check("<|Bot|>" not in live(closed), "no generation prompt when add_generation_prompt is false")
    check(BOS + "<|User|>hi" + EOS in closed, "user turn still rendered without generation prompt")

    # 5. Explicit overrides
    out = render(tmpl, [{"role": "user", "content": "hi"}], construct="coder", reasoning_effort="off")
    check("CODER MODE (forced)" in out, "explicit construct=coder emits forced block")

    out = render(tmpl, [{"role": "user", "content": "hi"}], persona="friend", reasoning_effort="off")
    check("FRIEND PERSONA (forced)" in out, "explicit persona=friend emits forced block")

    out = render(tmpl, [{"role": "user", "content": "hi"}], identity="femboy", reasoning_effort="off")
    check("FEMBOY IDENTITY (forced)" in out, "explicit identity=femboy emits forced block")

    out = render(tmpl, [{"role": "user", "content": "hi"}], theme="cerebral", reasoning_effort="off")
    check("CEREBRAL THEME (forced)" in out, "explicit theme=cerebral emits forced block")

    # 6. Thinking on/off and native effort
    for tier, expect_open, effort in [
        ("off", False, None),
        ("low", True, "low"),
        ("high", True, "high"),
        ("soft", True, "low"),
    ]:
        out = render(tmpl, [{"role": "user", "content": "hi"}], reasoning_effort=tier)
        tail = out[out.rfind("<|Bot|>"):]
        opened = tail.endswith("<think>")
        check(opened == expect_open, f"reasoning_effort={tier} thinking_open={opened}")
        if effort:
            check(f"thinking_effort={effort}" in out, f"reasoning_effort={tier} native effort={effort}")

    out = render(
        tmpl,
        [{"role": "user", "content": "hi"}],
        enable_thinking=False,
        reasoning_effort="high",
    )
    check(out.rstrip().endswith("<|Bot|></think>"), "enable_thinking=False forces none")
    check("thinking_effort=" not in head(out), "thinking off omits thinking_effort line")

    # 7. System prompt + multi-turn + reasoning content + a later system turn
    msgs = [
        {"role": "system", "content": "SYSTEM_SENTINEL"},
        {"role": "user", "content": "first question"},
        {
            "role": "assistant",
            "content": "first answer",
            "reasoning_content": "because",
        },
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

    # 8. Tools: definitions, dict args, string args, grouped results
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather",
                "parameters": {
                    "type": "object",
                    "properties": {"city": {"type": "string"}},
                },
            },
        }
    ]
    out = render(
        tmpl,
        [{"role": "user", "content": "weather?"}],
        tools=tools,
        reasoning_effort="off",
    )
    check("<tools>" in out and "get_weather" in out, "tools block renders")
    check("## Tools" in out, "tools preamble renders")

    tool_msgs = [
        {"role": "user", "content": "weather?"},
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {"function": {"name": "get_weather", "arguments": {"city": "Sydney"}}},
                {"function": {"name": "get_time", "arguments": '{"tz":"UTC"}'}},
            ],
        },
        {"role": "tool", "content": "22C"},
        {"role": "tool", "content": "03:00"},
    ]
    out = render(tmpl, tool_msgs, tools=tools, reasoning_effort="off", add_generation_prompt=False)
    check(
        "<tool_call>get_weather<arg_key>city</arg_key><arg_value>Sydney</arg_value></tool_call>" in out,
        "dict tool arguments use arg_key/arg_value",
    )
    check(
        '<tool_call>get_time<arg_value>{"tz":"UTC"}</arg_value></tool_call>' in out,
        "string tool arguments pass through verbatim",
    )
    check(live(out).count("<|Tool|>") == 1, "consecutive tool results share one Tool turn")
    check("<tool_response>22C</tool_response>" in out, "first tool response rendered")
    check("<tool_response>03:00</tool_response>" in out, "second tool response rendered")
    wire = live(out)
    tool_span = wire[wire.find("<|Tool|>"):wire.find(EOS, wire.find("<|Tool|>")) + len(EOS)]
    check(
        "<tool_response>22C</tool_response><tool_response>03:00</tool_response>" in tool_span,
        "grouped tool responses sit inside one sentence",
    )

    # 9. Content blocks, and rejection of the other model's vision blocks
    out = render(
        tmpl,
        [{"role": "user", "content": [{"type": "text", "text": "block hello"}]}],
        reasoning_effort="off",
    )
    check("block hello" in out, "content list-of-blocks works")
    try:
        render(
            tmpl,
            [{"role": "user", "content": [{"type": "image", "image": "x"}]}],
            reasoning_effort="off",
        )
        check(False, "image blocks must raise")
    except Exception as e:
        check("Unsupported" in str(e), "image blocks raise (text-only Spark wire)")

    # 10. No keyword routing: a coding request must not add a forced block.
    # The library already contains the words, so compare counts, not presence.
    codey = render(
        tmpl,
        [{"role": "user", "content": "please code a binary search"}],
        reasoning_effort="off",
    )
    check(
        codey.count("CODER MODE (forced)") == plain.count("CODER MODE (forced)"),
        "keyword 'code' does NOT add a forced coder block",
    )
    check("FRAME CARD" in codey, "still has frame card so model can choose coder itself")
    check("ON THE FLY" in plain and "Do not wait for a keyword" in plain, "on-the-fly switching instructions present")
    hi_off = render(tmpl, [{"role": "user", "content": "hi"}], reasoning_effort="off")
    coder = render(
        tmpl,
        [{"role": "user", "content": "hi"}],
        construct="coder",
        reasoning_effort="off",
    )
    check(
        coder.count("CODER MODE (forced)") == hi_off.count("CODER MODE (forced)") + 1,
        "explicit construct=coder adds exactly one forced block",
    )

    # 11. Library content from the rest of the repo, converted onto Spark tokens
    for label, needle in (
        ("Josie", "J.O.S.I.E."),
        ("Turbo Brilliance", "Turbo-Brilliance"),
        ("ORBIT", "ORBIT Reasoning Layer"),
        ("Protium gates", "PROTIUM OBJECTIVE-GATED"),
        ("AGI modes", "agi-teacher-coder"),
        ("froggeric", "froggeric"),
        ("arrow", "arrow4.0"),
        ("engram hook", "ENGRAM HOOK"),
        ("looping", "num_loops"),
        ("taxonomy", '"taxonomy": "v0.3"'),
        ("Jumbo model name from the session dump", "Jumbo-Fusion"),
        ("S1", "S1 FAST"),
        ("S2", "S2 DELIBERATE"),
        ("S3", "S3 META"),
    ):
        check(needle in plain, f"library contains {label}")
    import uuid
    sentinel = "ENGRAM-" + uuid.uuid4().hex
    recalled = render(
        tmpl,
        [{"role": "user", "content": "hi"}],
        add_generation_prompt=False,
        engram=sentinel,
    )
    check(sentinel in recalled, "engram kwarg is injected")
    check(sentinel not in plain, "engram text is absent when not passed")
    size = TEMPLATE.stat().st_size
    check(size >= 2_000_000, f"template file is multiple MB ({size} bytes)")

    # 12. Unsupported role
    try:
        render(tmpl, [{"role": "observer", "content": "x"}])
        check(False, "unknown role must raise")
    except Exception as e:
        check("Unsupported message role" in str(e), "unknown role raises")

    if args.show_render:
        print("\n----- sample render (default thinking, no overrides) -----")
        print(plain[:2000])
        print("...")

    chars = len(plain)
    token_note = f"chars/4 estimate {chars // 4}"
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        n = len(enc.encode(plain, disallowed_special=()))
        token_note = (
            f"cl100k_base {n} tokens (not the Spark tokenizer; none is in the repo); "
            f"chars/4 estimate {chars // 4}"
        )
    except Exception as e:
        token_note += f"; tiktoken unavailable ({e})"
    print()
    print(f"RENDER SIZE  chars={chars} file_bytes={size}")
    print(f"TOKEN ESTIMATE  {token_note}")
    print("WINDOW  stock tokenizer model_max_length=131072; patched max_position_embeddings=1048576")
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
