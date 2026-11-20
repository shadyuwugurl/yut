"""Build one HF chat example for a canonical id."""
from __future__ import annotations

import hashlib
import random

from answers import render_answer
from frame import (
    MODE_CONSTRUCT,
    S1_MODES,
    S3_MODES,
    Spec,
    blank_frame,
    pack,
)
from pieces import family_for, make_piece
from thinkfit import expand_lines, fit_think
from tools_flow import kinds_for, trajectory

AGI = {
    "agi-teacher-coder": ("s2", "code", "coder", "neutral", ["teacher", "coder"], []),
    "agi-teacher-business": ("s2", "plan", "teacher", "neutral", ["teacher", "business"], []),
    "agi-teacher-007": ("s2", "build", "007", "neutral", ["teacher", "007"], []),
    "agi-brainstorm-007": ("s2", "build", "007", "neutral", ["brainstorm", "007"], []),
    "agi-brainstorm-business": ("s2", "plan", "brainstorm", "neutral", ["brainstorm", "business"], []),
    "agi-brainstorm-coder": ("s2", "code", "coder", "neutral", ["brainstorm", "coder"], []),
    "agi-brainstorm-comedy": ("s2", "brainstorm", "brainstorm", "neutral", ["brainstorm", "comedy"], []),
    "agi-brainstorm-house": ("s2", "deep", "brainstorm", "house", ["brainstorm"], ["house"]),
    "agi-brainstorm-matlock": ("s2", "plan", "brainstorm", "matlock", ["brainstorm"], ["matlock"]),
    "agi-brainstorm-prompt": ("s2", "teach", "prompt", "neutral", ["brainstorm", "prompt"], []),
    "agi-brainstorm-stark": ("s2", "build", "brainstorm", "stark", ["brainstorm"], ["stark"]),
    "agi-brainstorm-story": ("s1", "react", "story", "neutral", ["brainstorm", "story"], []),
    "agi-musk-brainstorm": ("s2", "brainstorm", "brainstorm", "musk", ["brainstorm"], ["musk"]),
    "agi-musk-business": ("s2", "plan", "business", "musk", ["business"], ["musk"]),
    "agi-musk-curie": ("s2", "build", "ai_engineer", "musk", [], ["musk", "curie"]),
    "agi-pkd-house": ("s2", "deep", "logic", "pkd", ["logic"], ["pkd", "house"]),
    "agi-pkd-neo": ("s2", "logic", "logic", "pkd", ["logic"], ["pkd", "neo"]),
    "agi-pkd-comedy": ("s1", "banter", "comedy", "pkd", ["comedy"], ["pkd"]),
    "agi-house-comedy": ("s1", "banter", "comedy", "house", ["comedy"], ["house"]),
    "agi-pkd-vader-comedy": ("s1", "banter", "comedy", "vader", ["comedy"], ["pkd", "vader"]),
    "agi-stark-comedy": ("s1", "banter", "comedy", "stark", ["comedy"], ["stark"]),
    "agi-stark-musk-coder": ("s2", "code", "coder", "stark", ["coder"], ["stark", "musk"]),
    "agi-stark-musk-curie": ("s2", "build", "ai_engineer", "stark", [], ["stark", "musk", "curie"]),
    "agi-vader-comedy": ("s1", "banter", "comedy", "vader", ["comedy"], ["vader"]),
}

COMEDY_AGI = {
    "agi-pkd-comedy",
    "agi-house-comedy",
    "agi-pkd-vader-comedy",
    "agi-stark-comedy",
    "agi-vader-comedy",
    "agi-brainstorm-story",
}


def rng_for(spec: Spec, index: int, seed: int, salt: int) -> random.Random:
    digest = hashlib.sha256(f"{seed}|{salt}|{spec.key}|{index}".encode()).hexdigest()
    return random.Random(int(digest[:16], 16))


def _effort_for(spec: Spec, piece: dict) -> str:
    if spec.category == "thinking_effort" and spec.id != "off":
        return spec.id
    if spec.category == "channel" and spec.id == "instruct":
        return "high" if piece["family"] in ("code", "solve", "plan", "deep", "build", "logic") else "low"
    if spec.category == "thinking_effort" and spec.id == "off":
        return "high" if piece["family"] in ("code", "solve", "plan", "deep", "build", "logic") else "low"
    if spec.category == "reasoning_effort":
        if spec.id in ("effort_low", "effort_medium_low"):
            return "low"
        return "high"
    if spec.category == "protium" and spec.id in ("hermes", "apollo"):
        return "low"
    if spec.category == "orbit" or spec.category == "stance":
        return "low"
    if spec.category == "mode" and spec.id in S1_MODES | S3_MODES:
        return "low"
    if spec.category == "mode" and spec.id == "auto":
        return "low" if piece["family"] in ("chat", "banter", "hotpot", "vibe", "stream") else "high"
    if spec.category == "pathway" and spec.id == "s1":
        return "low"
    if spec.category == "pathway" and spec.id == "s3":
        return "low"
    if spec.category == "pathway" and spec.id == "auto":
        return "low" if piece["family"] in ("chat", "banter", "hotpot", "vibe", "inhibit", "settle", "heal") else "high"
    if spec.category == "agi" and spec.id in COMEDY_AGI:
        return "low"
    if spec.category == "channel" and spec.id == "reasoning":
        return "low" if piece["family"] in ("chat", "hotpot", "banter", "vibe") else "high"
    return "high"


def _concrete_mode(spec: Spec, piece: dict) -> str:
    family = piece["family"]
    by_family = {
        "chat": "chat",
        "hotpot": "hotpot",
        "skim": "skim",
        "vibe": "vibe",
        "banter": "banter",
        "react": "react",
        "pattern": "pattern",
        "complete": "complete",
        "stream": "stream",
        "recall": "recall",
        "solve": "solve",
        "code": "code",
        "build": "build",
        "logic": "logic",
        "plan": "plan",
        "research": "research",
        "brainstorm": "brainstorm",
        "teach": "teach",
        "deep": "deep",
        "extreme": "extreme",
        "inhibit": "inhibit",
        "escalate": "escalate",
        "reroute": "reroute",
        "heal": "heal",
        "settle": "settle",
        "prose": "chat",
        "contract": "plan",
        "loop": "plan",
        "decision": "deep",
        "ui": "code",
    }
    if spec.category == "mode" and spec.id != "auto":
        return spec.id
    if spec.category == "agi":
        return AGI[spec.id][1]
    return by_family.get(family, "chat")


def _pathway_for(spec: Spec, mode: str, effort: str) -> str:
    if spec.category == "pathway" and spec.id != "auto":
        return spec.id
    if spec.category == "agi":
        return AGI[spec.id][0]
    if mode in S3_MODES:
        return "s3"
    if mode in S1_MODES or effort == "low" or effort == "off":
        if mode in S1_MODES or effort == "off" and mode in S1_MODES:
            return "s1"
        if effort == "off":
            return "s1"
        if mode in S1_MODES:
            return "s1"
    if effort == "low" and mode in S1_MODES | S3_MODES:
        return "s1" if mode in S1_MODES else "s3"
    if mode in S3_MODES:
        return "s3"
    if effort == "low" and spec.category == "thinking_effort":
        return "s1"
    return "s2"


def build_frame(spec: Spec, piece: dict) -> dict:
    frame = blank_frame()
    effort = _effort_for(spec, piece)
    mode = _concrete_mode(spec, piece)
    if spec.category == "agi":
        pathway, mode, construct, persona, _c, _p = AGI[spec.id]
        frame["agi"] = spec.id
        frame["persona"] = persona
    else:
        pathway = _pathway_for(spec, mode, effort)
        construct = MODE_CONSTRUCT.get(mode, "omni")
        if spec.category == "aesthetic":
            construct = "coder"
            mode = "code"
            pathway = "s2"
            effort = "high"
        if spec.category == "stance":
            construct = "story"
            mode = "chat"
            pathway = "s1"
            effort = "low"
        if spec.category == "patch":
            construct = "deeptree"
            mode = "plan"
            pathway = "s2"
            effort = "high"
        if spec.category == "reasoning_mode":
            construct = "deeptree"
            mode = "plan"
            pathway = "s2"
            effort = "high"
        if spec.category == "protium":
            frame["protium"] = spec.id
        if spec.category == "aesthetic":
            frame["aesthetic"] = spec.id
    if spec.category == "channel":
        frame["channel"] = spec.id
    elif effort == "off" and spec.category == "thinking_effort":
        frame["channel"] = "reasoning"
    else:
        frame["channel"] = "reasoning"
    if spec.category == "reasoning_effort":
        frame["reasoning_effort"] = spec.id
    if spec.category == "thinking_effort":
        effort = spec.id
    frame["pathway"] = pathway
    frame["mode"] = mode
    frame["construct"] = construct if spec.category != "agi" else frame.get("construct", construct)
    if spec.category == "agi":
        frame["construct"] = AGI[spec.id][2]
        frame["pathway"] = AGI[spec.id][0]
        frame["mode"] = AGI[spec.id][1]
        frame["persona"] = AGI[spec.id][3]
        frame["agi"] = spec.id
        frame["thinking_effort"] = "low" if spec.id in COMEDY_AGI else "high"
        frame["channel"] = "reasoning"
    else:
        frame["thinking_effort"] = effort
    if frame["channel"] == "instruct":
        frame["thinking_effort"] = "off"
    return frame


def required_lines(spec: Spec, piece: dict) -> list[str]:
    if spec.category == "reasoning_mode":
        return list(piece["loop_lines"])
    if spec.category == "protium" and spec.id == "swarm":
        return [
            "Disassembly: " + (piece["checks"][0] if piece.get("checks") else piece["lead"]),
            "Angles: " + " | ".join(piece.get("alts") or piece.get("checks") or [piece["lead"]]),
            "The tension that matters: " + (piece["edges"][0] if piece.get("edges") else piece["detail"]),
            "The winning vector is the lead, and the rest is commentary.",
        ]
    if spec.category == "protium" and spec.id == "council":
        return [
            "Success looks like one ruling a person could execute.",
            "Panel split is in the alternatives, not in a new project.",
            "Dissent accounted for: " + (piece["edges"][0] if piece.get("edges") else piece["detail"]),
            piece["lead"],
        ]
    if spec.category == "protium" and spec.id == "hermes":
        return [piece["checks"][0], "It holds. Stop."]
    if spec.category == "protium" and spec.id == "artemis":
        return list(piece.get("boundaries") or []) + list(piece.get("edges") or []) + piece["checks"][:2]
    if spec.category == "orbit" and spec.id == "contextual_sanity":
        return [
            "Only the facts in the note are allowed to move the answer.",
            "Another question would not change the pick, so don't ask it.",
            piece["lead"],
        ]
    if spec.category == "orbit" and spec.id == "provisional_judgment":
        return [piece["lead"], "Keep the revision condition next to the call.", piece["edges"][0] if piece.get("edges") else piece["detail"]]
    if spec.category == "orbit" and spec.id == "childlike_capacity":
        return [piece["lead"], "Leave one option that is playful and still actually doable."]
    if spec.category == "orbit" and spec.id == "instrument_bounded":
        return [
            "The conclusion stops where the pasted facts stop.",
            piece["detail"],
            piece["lead"],
        ]
    if spec.category == "mode" and spec.id == "inhibit":
        return list(piece["checks"])
    if spec.category == "mode" and spec.id == "settle":
        return list(piece["checks"]) + ["That is the question they asked. Stop after it."]
    if spec.category == "mode" and spec.id == "escalate":
        return [
            "The clock-time half is a lookup I don't have. Say so and don't invent it.",
            "The break-even is the part that needs the real pass.",
        ] + list(piece["checks"])
    if spec.category == "patch":
        return [f"Section {h} is present and non-empty." for h in piece["contract"]]
    if spec.category == "reasoning_effort" and spec.id == "effort_high":
        return [
            "Path A: " + piece["lead"],
            "Path B: " + (piece["alts"][0] if piece.get("alts") else piece["detail"]),
            "Stress: " + (piece["edges"][0] if piece.get("edges") else piece["checks"][0]),
        ]
    if spec.category == "reasoning_effort" and spec.id in ("effort_ultra", "effort_xultra"):
        return [
            "Draft: " + piece["lead"],
            "Adversarial pass: " + (piece["edges"][0] if piece.get("edges") else "try to break the lead"),
            "The draft survives, with the flip condition named.",
        ] + list(piece["checks"])
    lines = list(piece.get("checks") or [])
    if piece.get("detail"):
        lines.append(piece["detail"])
    if not lines:
        lines = [piece["lead"]]
    return lines


def _history_message(spec: Spec, turn: dict, final_frame: dict) -> tuple[dict, dict]:
    frame = dict(final_frame)
    frame["pathway"] = turn.get("pathway", "s1")
    frame["mode"] = turn.get("mode", "chat")
    frame["construct"] = turn.get("construct", "omni")
    frame["thinking_effort"] = turn.get("effort", "low")
    frame["channel"] = "reasoning"
    frame["protium"] = None
    frame["aesthetic"] = None
    frame["agi"] = None
    frame["reasoning_effort"] = None
    lines = [
        "This turn is small. Store the fact or answer the joke, and don't start the later problem.",
        turn["answer"],
    ]
    think = fit_think(frame, lines, [], 80, 320)
    message = {"role": "assistant", "content": pack(think, turn["answer"])}
    return message, frame


def _finish(spec: Spec, frame: dict, messages: list, tools, turns, tool_kind, switches, parts) -> dict:
    meta = {
        "category": spec.category,
        "id": spec.id,
        "frame": frame,
        "turns": turns,
        "tool_trajectory": tool_kind,
        "switches": switches,
        "source": "procedural",
    }
    if spec.category == "orbit":
        meta["orbit"] = spec.id
    if spec.category == "stance":
        meta["stance"] = spec.id
    if spec.category == "patch":
        meta["patch"] = spec.id
        meta["contract"] = messages  # replaced below
    if spec.category == "reasoning_mode":
        meta["reasoning_mode"] = spec.id
    if parts:
        meta["parts"] = parts
    ex = {"messages": messages, "meta": meta}
    if tools:
        ex["tools"] = tools
    return ex


def compose_piece(spec: Spec, piece: dict, index: int) -> dict:
    frame = build_frame(spec, piece)
    messages = []
    turns = []
    switches = False
    for turn in piece.get("history") or []:
        messages.append({"role": "user", "content": turn["user"]})
        msg, turn_frame = _history_message(spec, turn, frame)
        messages.append(msg)
        turns.append(turn_frame)
        switches = True
    messages.append({"role": "user", "content": piece["user"]})
    answer = render_answer(spec, piece)
    lo, hi = _band(spec, frame, True)
    if lo == 0:
        content = pack("", answer)
        think = ""
    else:
        required = required_lines(spec, piece)
        optional = expand_lines(piece, 80)
        think = fit_think(frame, required, optional, lo, hi)
        content = pack(think, answer)
    messages.append({"role": "assistant", "content": content})
    turns.append(frame)
    parts = None
    if spec.category == "agi":
        _p, _m, _c, _persona, constructs, personas = AGI[spec.id]
        parts = {"constructs": constructs, "personas": personas}
    ex = _finish(spec, frame, messages, None, turns, None, switches, parts)
    if spec.category == "patch":
        ex["meta"]["contract"] = piece["contract"]
    return ex


def _band(spec: Spec, frame: dict, is_final: bool) -> tuple[int, int]:
    from frame import band_for

    return band_for(spec, frame, is_final)


def compose_tool(spec: Spec, index: int, rng: random.Random, kind: str) -> dict:
    flow = trajectory(kind, rng, spec)
    final = flow["final_frame"]
    # The row's label still owns the frame dials that are the point of the id.
    owned = build_frame(spec, {"family": "code", "lead": "", "checks": [], "edges": [], "alts": []})
    if spec.category == "mode" and spec.id in ("code", "build"):
        final["mode"] = spec.id
        final["construct"] = MODE_CONSTRUCT[spec.id]
        final["pathway"] = "s2"
    elif spec.category == "pathway" and spec.id == "s2":
        final["pathway"] = "s2"
    elif spec.category == "channel" and spec.id == "reasoning":
        final["channel"] = "reasoning"
    elif spec.category == "agi":
        final["agi"] = spec.id
        final["construct"] = AGI[spec.id][2]
        final["persona"] = AGI[spec.id][3]
        final["mode"] = AGI[spec.id][1]
        final["pathway"] = AGI[spec.id][0]
    # Keep the owned thinking effort on the final turn so the band matches the id.
    final["thinking_effort"] = owned["thinking_effort"]
    final["channel"] = owned["channel"]
    if owned.get("reasoning_effort"):
        final["reasoning_effort"] = owned["reasoning_effort"]
    if owned.get("protium"):
        final["protium"] = owned["protium"]

    messages = [{"role": "user", "content": flow["user"]}]
    turns = []
    for step in flow["steps"]:
        if step["role"] == "tool":
            messages.append({"role": "tool", "content": step["content"]})
            continue
        step_frame = step["frame"]
        step_frame["persona"] = final["persona"]
        step_frame["identity"] = "none"
        step_frame["theme"] = "none"
        if spec.category == "agi":
            step_frame["agi"] = spec.id
            step_frame["construct"] = final["construct"]
            step_frame["persona"] = final["persona"]
        lo, hi = _band(spec, step_frame, False)
        think = fit_think(step_frame, step["think_lines"], expand_lines({"lead": step["think_lines"][0], "checks": step["think_lines"]}, 20), lo, hi)
        messages.append(
            {
                "role": "assistant",
                "content": pack(think, ""),
                "tool_calls": step["tool_calls"],
            }
        )
        turns.append(step_frame)
    lo, hi = _band(spec, final, True)
    piece = {
        "lead": flow["final_answer"],
        "checks": flow["final_lines"],
        "edges": flow["final_lines"],
        "alts": [],
        "detail": flow["final_lines"][0],
    }
    if lo == 0:
        think = ""
    else:
        think = fit_think(final, flow["final_lines"], expand_lines(piece, 80), lo, hi)
    messages.append({"role": "assistant", "content": pack(think, flow["final_answer"])})
    turns.append(final)
    parts = None
    if spec.category == "agi":
        _p, _m, _c, _persona, constructs, personas = AGI[spec.id]
        parts = {"constructs": constructs, "personas": personas}
    return _finish(spec, final, messages, flow["tools"], turns, kind, False, parts)


def compose(spec: Spec, index: int, seed: int, salt: int = 0) -> dict:
    rng = rng_for(spec, index, seed, salt)
    kind = kinds_for(spec, index)
    if kind:
        return compose_tool(spec, index, rng, kind)
    family = family_for(spec.category, spec.id, index)
    # make_piece rebuilds aesthetic briefs; pass the family through make_piece's own selector
    piece = make_piece(spec.category, spec.id, index, rng)
    piece["family"] = family if spec.category != "aesthetic" else piece["family"]
    if spec.category != "aesthetic":
        # make_piece already selected the family. Trust it.
        pass
    return compose_piece(spec, piece, index)
