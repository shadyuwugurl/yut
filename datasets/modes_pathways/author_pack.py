"""Pack hand-written rows into Spark HF chats. Does not invent the words."""
from __future__ import annotations

import json
from pathlib import Path

from compose import AGI, COMEDY_AGI
from frame import (
    MODE_CONSTRUCT,
    S1_MODES,
    S3_MODES,
    Spec,
    all_specs,
    blank_frame,
    frame_tag,
    pack,
)
from quality import problems

HERE = Path(__file__).resolve().parent
AUTHORED = HERE / "authored"

def _fn(name, desc, props, required):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": desc,
            "parameters": {"type": "object", "properties": props, "required": required},
        },
    }

TOOL_WEATHER = _fn("get_weather", "Current weather for a city.", {"city": {"type": "string"}}, ["city"])
TOOL_TIME = _fn("get_time", "Local time for an IANA timezone.", {"tz": {"type": "string"}}, ["tz"])
TOOL_READ = _fn("read_file", "Read a text file the user already has.", {"path": {"type": "string"}}, ["path"])
TOOL_SEARCH = _fn("search_docs", "Search the project's docs.", {"query": {"type": "string"}}, ["query"])
TOOL_QUERY = _fn("run_query", "Run one read-only SELECT.", {"sql": {"type": "string"}}, ["sql"])
TOOL_HTTP = _fn("http_get", "GET a URL on a host the user operates.", {"url": {"type": "string"}}, ["url"])

def call(name, **arguments):
    return {"type": "function", "function": {"name": name, "arguments": arguments}}


def specs_by_key() -> dict[str, Spec]:
    return {s.key: s for s in all_specs()}


def default_frame(spec: Spec, hint: dict | None = None) -> dict:
    hint = hint or {}
    frame = blank_frame()
    if spec.category == "agi":
        pathway, mode, construct, persona, _c, _p = AGI[spec.id]
        frame.update(
            {
                "pathway": pathway,
                "mode": mode,
                "construct": construct,
                "persona": persona,
                "agi": spec.id,
                "thinking_effort": "low" if spec.id in COMEDY_AGI else "high",
                "channel": "reasoning",
            }
        )
    elif spec.category == "mode":
        mode = spec.id if spec.id != "auto" else hint.get("mode", "chat")
        if mode == "auto":
            raise ValueError("mode/auto needs hint.mode")
        frame["mode"] = mode
        frame["pathway"] = "s1" if mode in S1_MODES else "s3" if mode in S3_MODES else "s2"
        frame["construct"] = MODE_CONSTRUCT.get(mode, "omni")
        frame["thinking_effort"] = "low" if frame["pathway"] != "s2" else "high"
    elif spec.category == "pathway":
        pathway = spec.id if spec.id != "auto" else hint.get("pathway", "s1")
        mode = hint.get("mode") or ("chat" if pathway == "s1" else "settle" if pathway == "s3" else "deep")
        frame["pathway"] = pathway
        frame["mode"] = mode
        frame["construct"] = MODE_CONSTRUCT.get(mode, "omni")
        frame["thinking_effort"] = "low" if pathway != "s2" else "high"
    elif spec.category == "thinking_effort":
        mode = hint.get("mode", "chat" if spec.id != "high" else "solve")
        frame["mode"] = mode
        frame["construct"] = MODE_CONSTRUCT.get(mode, "omni")
        frame["thinking_effort"] = spec.id
        frame["pathway"] = "s1" if spec.id != "high" else "s2"
        if spec.id == "high":
            frame["pathway"] = "s2"
        elif mode in S3_MODES:
            frame["pathway"] = "s3"
        else:
            frame["pathway"] = "s1" if spec.id != "high" else "s2"
    elif spec.category == "reasoning_effort":
        mode = hint.get("mode", "solve")
        frame["mode"] = mode
        frame["construct"] = MODE_CONSTRUCT.get(mode, "logic")
        frame["pathway"] = "s2" if spec.id not in ("effort_low", "effort_medium_low") else "s1"
        frame["thinking_effort"] = "low" if spec.id in ("effort_low", "effort_medium_low") else "high"
        frame["reasoning_effort"] = spec.id
    elif spec.category == "channel":
        mode = hint.get("mode", "chat" if spec.id == "reasoning" else "solve")
        frame["mode"] = mode
        frame["construct"] = MODE_CONSTRUCT.get(mode, "omni")
        frame["channel"] = spec.id
        if spec.id == "instruct":
            frame["thinking_effort"] = "off"
            frame["pathway"] = "s2" if mode not in S1_MODES | S3_MODES else ("s3" if mode in S3_MODES else "s1")
        else:
            frame["thinking_effort"] = hint.get("thinking_effort", "high" if mode not in S1_MODES else "low")
            frame["pathway"] = "s1" if frame["thinking_effort"] == "low" else "s2"
    elif spec.category == "protium":
        mode = hint.get("mode", "solve" if spec.id in ("hermes", "apollo", "artemis", "oracle") else "plan")
        if spec.id in ("swarm", "council"):
            mode = hint.get("mode", "brainstorm")
        frame["mode"] = mode
        frame["construct"] = MODE_CONSTRUCT.get(mode, "logic")
        frame["protium"] = spec.id
        short = spec.id in ("hermes", "apollo")
        frame["thinking_effort"] = "low" if short else "high"
        frame["pathway"] = "s1" if short else "s2"
    elif spec.category == "aesthetic":
        frame.update(
            {
                "pathway": "s2",
                "mode": "code",
                "construct": "coder",
                "thinking_effort": "high",
                "aesthetic": spec.id,
            }
        )
    elif spec.category == "orbit":
        frame.update(
            {
                "pathway": "s2",
                "mode": hint.get("mode", "deep"),
                "construct": "deeptree",
                "thinking_effort": "low",
            }
        )
    elif spec.category == "stance":
        frame.update(
            {
                "pathway": "s1",
                "mode": "chat",
                "construct": "story",
                "thinking_effort": "low",
            }
        )
    elif spec.category == "patch":
        frame.update(
            {
                "pathway": "s2",
                "mode": "plan",
                "construct": "deeptree",
                "thinking_effort": "high",
            }
        )
    elif spec.category == "reasoning_mode":
        frame.update(
            {
                "pathway": "s2",
                "mode": "plan",
                "construct": "deeptree",
                "thinking_effort": "high",
            }
        )
    else:
        raise ValueError(spec.key)
    for key in ("pathway", "mode", "construct", "persona", "thinking_effort", "channel"):
        if key in hint:
            frame[key] = hint[key]
    if frame["channel"] == "instruct":
        frame["thinking_effort"] = "off"
    return frame


def _asst(frame: dict, think: str, answer: str, tool_calls=None) -> dict:
    if frame.get("thinking_effort") == "off" or frame.get("channel") == "instruct":
        body = pack("", answer)
    else:
        text = frame_tag(frame)
        extra = (think or "").strip()
        if extra:
            text = text + "\n" + extra
        body = pack(text, answer)
    msg = {"role": "assistant", "content": body}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    return msg


def pack_one(spec: Spec, row: dict) -> dict:
    """row keys: user, think, answer, optional history, tools, steps, hint, contract, tool_trajectory.

    history items: {user, think, answer, hint?}
    steps items before the final answer: {think, tool_calls} then the matching tool contents
    are passed as step['result'] (str or list of str for parallel).
    """
    final = default_frame(spec, row.get("hint"))
    messages = []
    turns = []
    switches = bool(row.get("history"))
    for past in row.get("history") or []:
        messages.append({"role": "user", "content": past["user"]})
        if "frame" in past:
            past_frame = blank_frame()
            past_frame.update(past["frame"])
        else:
            past_frame = default_frame(
                spec,
                past.get("hint") or {"mode": "chat", "pathway": "s1", "thinking_effort": "low", "construct": "omni", "channel": "reasoning"},
            )
            if not past.get("keep_dials"):
                past_frame["agi"] = None
                past_frame["protium"] = None
                past_frame["aesthetic"] = None
                past_frame["reasoning_effort"] = None
        messages.append(_asst(past_frame, past.get("think", ""), past.get("answer", "")))
        turns.append(past_frame)
    messages.append({"role": "user", "content": row["user"]})
    for step in row.get("steps") or []:
        step_frame = blank_frame()
        step_frame.update(final)
        step_frame["thinking_effort"] = "low"
        step_frame["channel"] = "reasoning"
        calls = step["tool_calls"]
        messages.append(_asst(step_frame, step.get("think", ""), "", calls))
        turns.append(step_frame)
        results = step["result"]
        if isinstance(results, str):
            results = [results]
        for result in results:
            messages.append({"role": "tool", "content": result})
    messages.append(_asst(final, row.get("think", ""), row.get("answer", "")))
    turns.append(final)
    ex = {
        "messages": messages,
        "meta": {
            "category": spec.category,
            "id": spec.id,
            "frame": final,
            "turns": turns,
            "tool_trajectory": row.get("tool_trajectory"),
            "switches": switches or bool(row.get("steps")),
            "source": "authored",
        },
    }
    if spec.category == "agi":
        _p, _m, _c, _persona, constructs, personas = AGI[spec.id]
        ex["meta"]["parts"] = {"constructs": constructs, "personas": personas}
    if spec.category == "orbit":
        ex["meta"]["orbit"] = spec.id
    if spec.category == "stance":
        ex["meta"]["stance"] = spec.id
    if spec.category == "patch":
        ex["meta"]["patch"] = spec.id
        ex["meta"]["contract"] = row.get("contract") or []
    if spec.category == "reasoning_mode":
        ex["meta"]["reasoning_mode"] = spec.id
    if row.get("tools"):
        ex["tools"] = row["tools"]
    return ex


def write_id(spec: Spec, rows: list[dict], path: Path | None = None) -> tuple[int, list[str]]:
    path = path or AUTHORED / f"{spec.category}__{spec.id}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    packed = []
    errors = []
    seen = set()
    for i, row in enumerate(rows):
        try:
            ex = pack_one(spec, row)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{spec.key}#{i} pack {exc}")
            continue
        probs = problems(ex, spec)
        if probs:
            errors.append(f"{spec.key}#{i} " + "; ".join(probs[:4]))
            continue
        blob = json.dumps(ex["messages"], ensure_ascii=False, sort_keys=True)
        if blob in seen:
            errors.append(f"{spec.key}#{i} exact duplicate")
            continue
        seen.add(blob)
        packed.append(ex)
    with path.open("w", encoding="utf-8") as fh:
        for ex in packed:
            fh.write(json.dumps(ex, ensure_ascii=False) + "\n")
    return len(packed), errors
