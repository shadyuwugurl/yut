#!/usr/bin/env python3
"""Wrap hand-written turns in skinny-v1 meta. Does not invent the words."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cp.filters import check_example  # noqa: E402
from cp.procedural import _assistant, _frame, spec_for  # noqa: E402

SHORT = (
    "You are a helpful assistant.",
    "Answer the person in front of you.",
    "Be direct.",
)


def _uid(category: str, ident: str, pattern: str, messages: list[dict]) -> str:
    blob = "\n".join(m["role"] + "\n" + m["content"] for m in messages)
    digest = hashlib.sha1(blob.encode()).hexdigest()[:12]
    return f"cp-{category}-{ident}-{pattern}-{digest}"


def pack(category: str, ident: str, pattern: str, turns: list[tuple[str, str]], *,
         switch_from: tuple[str, str] | None = None,
         blend_with: str | None = None,
         nsfw: bool = False,
         system: str | None = None) -> dict:
    """turns are ('user', text) or ('think', text) or ('assistant', visible).

    A 'think' turn must be followed by 'assistant'. Think text must not
    include the frame tag; this adds the tag for the active frame.
    """
    spec = spec_for(category, ident)
    extra = [blend_with] if blend_with else []
    frame = _frame(spec, extra)
    src_frame = None
    if switch_from:
        src_frame = _frame(spec_for(*switch_from), [])
    messages = []
    if system:
        if system not in SHORT:
            raise ValueError("system line is not allowlisted")
        messages.append({"role": "system", "content": system})
    user_i = 0
    pending_think = None
    pending_frame = frame
    i = 0
    while i < len(turns):
        kind, text = turns[i]
        if kind == "user":
            messages.append({"role": "user", "content": text.strip()})
            user_i += 1
            if switch_from and user_i - 1 >= 1:
                pending_frame = frame
            elif switch_from:
                pending_frame = src_frame
            i += 1
            continue
        if kind == "think":
            pending_think = text.strip()
            i += 1
            continue
        if kind != "assistant":
            raise ValueError(kind)
        think = pending_think
        pending_think = None
        use_frame = src_frame if (switch_from and user_i <= 1) else frame
        # user_i has already counted the user turn this assistant answers.
        if switch_from and user_i <= 1:
            use_frame = src_frame
        else:
            use_frame = frame
        messages.append({"role": "assistant", "content": _assistant(think or "", text, use_frame)})
        i += 1
    if pending_think:
        raise ValueError("think without assistant")
    switch = None
    blend = None
    if pattern == "switch":
        if not switch_from:
            raise ValueError("switch needs switch_from")
        switch = {
            "from": switch_from[1],
            "to": ident,
            "from_category": switch_from[0],
            "to_category": category,
            "at_user_turn": 1,
        }
    if pattern == "blend":
        if not blend_with:
            raise ValueError("blend needs blend_with")
        blend = [ident, blend_with]
    think_flag = any(m["content"].startswith("<think>\n") for m in messages if m["role"] == "assistant")
    row = {
        "messages": messages,
        "meta": {
            "category": category,
            "id": ident,
            "alias_input": None,
            "pattern": pattern,
            "switch": switch,
            "blend": blend,
            "frame": frame,
            "think": think_flag,
            "source": "authored",
            "nsfw": nsfw or spec["nsfw"],
            "taxonomy": "skinny-v1",
            "uid": _uid(category, ident, pattern, messages),
        },
    }
    problems = check_example(row)
    if problems:
        raise ValueError(f"{category}/{ident} {pattern}: {problems}")
    return row


def write_id(ident_category: str, ident: str, rows: list[dict]) -> Path:
    out = ROOT / "authored" / f"{ident}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if out.exists():
        for line in out.read_text().splitlines():
            if line.strip():
                existing.append(json.loads(line))
    seen = {r["meta"]["uid"] for r in existing}
    added = 0
    for row in rows:
        if row["meta"]["uid"] in seen:
            continue
        existing.append(row)
        seen.add(row["meta"]["uid"])
        added += 1
    with out.open("w", encoding="utf-8") as handle:
        for row in existing:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"{ident_category}/{ident}: +{added} now {len(existing)}")
    return out
