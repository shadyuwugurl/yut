"""Quality gate shared by the generator and the validator."""
from __future__ import annotations

import ast
import hashlib
import json
import re

from frame import (
    FORBIDDEN,
    PALETTE_FINGERPRINT,
    SLOP,
    Spec,
    all_specs,
    split_think,
    band_for,
)

_MODE_CMD = re.compile(r"\b(switch to|enter|activate|use)\b.{0,32}\bmode\b", re.I)
_CANON = {(s.category, s.id) for s in all_specs()}
_ALIAS_AS_ID = set()
for _s in all_specs():
    for _a in _s.aliases:
        if (_s.category, _a) not in _CANON:
            _ALIAS_AS_ID.add((_s.category, _a))


def signature(ex: dict) -> str:
    payload = {"messages": ex["messages"], "tools": ex.get("tools")}
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def _is_error(content: str) -> bool:
    head = content.lower()[:150]
    if head.startswith("failed to "):
        return True
    needles = (
        "command not found",
        "connection refused",
        "timed out",
        "no such file or directory",
        '"success": false',
        '"success":false',
    )
    return any(n in head for n in needles)


def _repeated_sentence(think: str) -> str | None:
    """Flag a sentence reused verbatim. Real derivations don't do that."""
    seen = []
    for raw in re.split(r"(?<=[.!?])\s+|\n+", think):
        line = " ".join(raw.split()).strip(" -")
        if len(line) < 45 or line.startswith("[frame:"):
            continue
        key = line.lower()
        if key in seen:
            return line
        seen.append(key)
    return None


def _calls(message: dict) -> list[dict]:
    return list(message.get("tool_calls") or [])


def _problems_tools(ex: dict) -> list[str]:
    kind = ex["meta"].get("tool_trajectory")
    if not kind:
        return []
    out = []
    if not ex.get("tools"):
        out.append("tool trajectory without tools")
    msgs = ex["messages"]
    assistants = [m for m in msgs if m["role"] == "assistant"]
    tool_msgs = [m for m in msgs if m["role"] == "tool"]
    call_msgs = [m for m in assistants if _calls(m)]
    if kind == "direct":
        if call_msgs:
            out.append("direct trajectory called a tool")
        return out
    if not call_msgs:
        out.append(f"{kind} trajectory made no call")
        return out
    if _calls(assistants[-1]):
        out.append("final turn still has a tool call")
    if kind == "call":
        if not tool_msgs or _is_error(tool_msgs[-1]["content"]):
            out.append("call trajectory did not end on a successful tool result")
    elif kind in ("retry", "code_retry"):
        if len(call_msgs) != 2:
            out.append(f"retry expected 2 calls, got {len(call_msgs)}")
        else:
            a = _calls(call_msgs[0])[0]["function"]
            b = _calls(call_msgs[1])[0]["function"]
            if a["name"] != b["name"] or a["arguments"] == b["arguments"]:
                out.append("retry did not correct the arguments")
        if len(tool_msgs) < 2 or not _is_error(tool_msgs[0]["content"]) or _is_error(tool_msgs[1]["content"]):
            out.append("retry errors were not one failure then one success")
        if kind == "code_retry":
            final_visible = split_think(assistants[-1]["content"])[1]
            if "```python" not in final_visible or ">=" not in final_visible:
                out.append("code retry did not ship the corrected function")
    elif kind == "diagnose":
        names = [_calls(m)[0]["function"]["name"] for m in call_msgs]
        if len(names) < 3 or names[0] != names[1] or names[2] == names[0]:
            out.append("diagnose did not switch tools after two failures")
        if len(tool_msgs) < 3 or not _is_error(tool_msgs[0]["content"]) or not _is_error(tool_msgs[1]["content"]):
            out.append("diagnose missing two opening errors")
        if len(tool_msgs) >= 3 and _is_error(tool_msgs[2]["content"]):
            out.append("diagnose third result should be the alternative tool succeeding")
    elif kind == "pivot":
        if len(call_msgs) != 3:
            out.append(f"pivot expected 3 calls, got {len(call_msgs)}")
        if len(tool_msgs) != 3 or not all(_is_error(m["content"]) for m in tool_msgs):
            out.append("pivot expected three error results and then a stop")
        final = split_think(assistants[-1]["content"])[1].lower()
        if "fourth" not in final and "not sending" not in final and "not going to" not in final:
            out.append("pivot answer does not refuse another try")
    else:
        out.append(f"unknown trajectory {kind}")
    for m in call_msgs:
        for call in _calls(m):
            fn = call.get("function") or {}
            if not fn.get("name") or not isinstance(fn.get("arguments"), dict):
                out.append("tool call arguments must be an object so arg_key/arg_value render")
    return out


def problems(ex: dict, spec: Spec) -> list[str]:
    out: list[str] = []
    meta = ex.get("meta") or {}
    if meta.get("category") != spec.category or meta.get("id") != spec.id:
        out.append("meta label does not match spec")
    if (spec.category, spec.id) not in _CANON:
        out.append("id is not canonical")
    if (meta.get("category"), meta.get("id")) in _ALIAS_AS_ID:
        out.append("alias stored as label")
    frame = meta.get("frame") or {}
    for key in (
        "pathway",
        "mode",
        "construct",
        "persona",
        "identity",
        "theme",
        "thinking_effort",
        "reasoning_effort",
        "channel",
        "protium",
        "aesthetic",
        "agi",
    ):
        if key not in frame:
            out.append(f"frame missing {key}")
    if "orbit" in frame or "stance" in frame or "patch" in frame:
        out.append("orbit/stance/patch do not live on the frame")
    if spec.category == "mode" and spec.id != "auto" and frame.get("mode") != spec.id:
        out.append("mode frame does not wear the mode")
    if spec.category == "mode" and spec.id == "auto" and frame.get("mode") in (None, "auto"):
        out.append("auto must resolve to a real mode")
    if spec.category == "pathway" and spec.id != "auto" and frame.get("pathway") != spec.id:
        out.append("pathway frame mismatch")
    if spec.category == "pathway" and spec.id == "auto" and frame.get("pathway") not in ("s1", "s2", "s3"):
        out.append("pathway auto did not choose")
    if spec.category == "thinking_effort" and frame.get("thinking_effort") != spec.id:
        out.append("thinking_effort mismatch")
    if spec.category == "reasoning_effort" and frame.get("reasoning_effort") != spec.id:
        out.append("reasoning_effort mismatch")
    if spec.category == "channel" and frame.get("channel") != spec.id:
        out.append("channel mismatch")
    if spec.category == "protium" and frame.get("protium") != spec.id:
        out.append("protium mismatch")
    if spec.category == "aesthetic" and frame.get("aesthetic") != spec.id:
        out.append("aesthetic mismatch")
    if spec.category == "agi" and frame.get("agi") != spec.id:
        out.append("agi mismatch")
    if spec.category == "orbit" and meta.get("orbit") != spec.id:
        out.append("orbit tag missing")
    if spec.category == "stance" and meta.get("stance") != spec.id:
        out.append("stance tag missing")
    if spec.category == "patch" and meta.get("patch") != spec.id:
        out.append("patch tag missing")
    if spec.category == "reasoning_mode" and meta.get("reasoning_mode") != spec.id:
        out.append("reasoning_mode tag missing")

    turns = meta.get("turns") or []
    assistants = [m for m in ex["messages"] if m["role"] == "assistant"]
    if len(turns) != len(assistants):
        out.append("turns do not line up with assistant messages")
    for i, (msg, turn) in enumerate(zip(assistants, turns)):
        is_final = i == len(assistants) - 1
        think, visible = split_think(msg.get("content") or "")
        lo, hi = band_for(spec, turn, is_final, meta.get("source"))
        if meta.get("source") == "authored" and think:
            repeated = _repeated_sentence(think)
            if repeated:
                out.append(f"turn {i} restates a sentence: {repeated[:80]}")
        if lo == 0:
            if think or "<think>" in (msg.get("content") or ""):
                out.append(f"turn {i} should not think")
        else:
            if not (lo <= len(think) <= hi):
                out.append(f"turn {i} think length {len(think)} outside {lo}-{hi}")
            tag = (
                "[frame: pathway={pathway}|mode={mode}|construct={construct}"
                "|persona={persona}|identity={identity}|theme={theme}|channel={channel}]"
            ).format(**turn)
            if not think.startswith(tag):
                out.append(f"turn {i} private tag does not match the frame")
        if is_final and not visible and not _calls(msg):
            out.append("empty final answer")
        low = visible.lower()
        for phrase in SLOP:
            if phrase in low:
                out.append(f"slop phrase: {phrase}")
                break
        for phrase in FORBIDDEN:
            if phrase.lower() in low:
                out.append(f"machinery leaked into the answer: {phrase}")
                break
        if "i am in " in low or "i'm in " in low and "mode" in low:
            out.append("announced the frame")
        if "```python" in visible:
            block = visible.split("```python", 1)[1].split("```", 1)[0]
            try:
                ast.parse(block)
            except SyntaxError as exc:
                out.append(f"python block does not parse: {exc}")
    for msg in ex["messages"]:
        if msg["role"] != "user":
            continue
        text = msg["content"]
        low = text.lower()
        for phrase in FORBIDDEN:
            if phrase.lower() in low:
                out.append(f"user text contains {phrase}")
                break
        if _MODE_CMD.search(text):
            out.append("user text commands a mode")
        if spec.category in ("protium", "aesthetic", "agi", "orbit", "stance", "patch", "reasoning_mode", "reasoning_effort"):
            if spec.id.lower() in low:
                out.append("user text names the label")
    if spec.category == "protium" and spec.id == "swarm":
        visible = split_think(assistants[-1]["content"])[1]
        if not visible.startswith("[SWARM VERDICT]"):
            out.append("swarm answer must open with the verdict token")
    if spec.category == "protium" and spec.id == "council":
        visible = split_think(assistants[-1]["content"])[1]
        if not visible.startswith("[COUNCIL VERDICT]"):
            out.append("council answer must open with the verdict token")
    if spec.category == "aesthetic":
        visible = split_think(assistants[-1]["content"])[1]
        for needle in PALETTE_FINGERPRINT[spec.id]:
            if needle not in visible:
                out.append(f"aesthetic missing {needle}")
    if spec.category == "patch":
        visible = split_think(assistants[-1]["content"])[1]
        cursor = 0
        for heading in meta.get("contract") or []:
            token = f"## {heading}"
            at = visible.find(token, cursor)
            if at < 0:
                out.append(f"missing contract section {heading}")
                break
            cursor = at + len(token)
    if spec.category == "reasoning_mode":
        think = split_think(assistants[-1]["content"])[0].lower()
        if "re-ponder" not in think:
            out.append("loop think never re-ponders")
    if spec.category == "orbit" and spec.id == "provisional_judgment":
        if "i'd revise" not in split_think(assistants[-1]["content"])[1].lower():
            out.append("provisional judgment has no revision condition")
    if spec.category == "orbit" and spec.id == "instrument_bounded":
        visible = split_think(assistants[-1]["content"])[1].lower()
        if "only the" not in visible and "nothing about" not in visible and "says nothing" not in visible:
            out.append("instrument bound is not stated")
    if spec.category == "stance":
        visible = split_think(assistants[-1]["content"])[1]
        if not re.search(r"\d", visible):
            out.append("deckard prose has no concrete detail")
    out.extend(_problems_tools(ex))
    return out
