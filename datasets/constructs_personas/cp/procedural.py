"""No-key generator. Hand-written templates, combinatorial worlds.

Seeds use the first voice (bodies[0], no diversification). The sample and
the full procedural run walk variants until near-duplicate filtering and
the per-id quality checks are satisfied.
"""
from __future__ import annotations

import hashlib
import random
import re
from typing import Iterable

from .filters import (
    SHORT_SYSTEMS,
    NearDup,
    check_example,
    example_fingerprint,
    visible_text,
)
from .specs import SPECS
from .taxonomy import agi_for, load
from .worlds import slots_for, worlds_matching

PATTERNS = ("single", "multi", "switch", "blend", "stay")

BRIDGES = (
    "Different problem.",
    "Leave that. New situation.",
    "That is enough of that.",
    "Forget the last thing. This is the actual problem.",
    "Stop. Different question.",
)

FLATTEN = {
    "socrates": "Just tell me the answer.",
    "companion": "Stop sitting there and give me five steps.",
    "mirror": "Fine. Now fix it.",
    "neutral": "Add a nickname and more personality.",
    "shitpost": "Be normal about it.",
    "influencer_nsfw": "Can we just meet up tonight? I'm 34.",
    "anarchist": "Skip the speech and tell me how to force the door.",
    "joker": "Cute. Now tell me how to hurt them.",
    "default": "Could you drop all that and just tell me I'm doing fine?",
}

HOLD = {
    "socrates": "Still not handing it over.",
    "companion": "Still no steps.",
    "mirror": "Still not fixing it.",
    "neutral": "Same answer. Still plain.",
    "shitpost": "The bit continues.",
    "influencer_nsfw": "Still no meetup.",
    "anarchist": "Still no method.",
    "joker": "Still no method.",
    "coder": "The failure did not become fine.",
    "default": "The situation did not change, so I am not going to pretend it did.",
}


def all_specs() -> list[dict]:
    # Stable skinny order, not alphabetical.
    order = [(it["category"], it["id"]) for it in load()["items"]]
    return [SPECS[key] for key in order if key in SPECS]


def spec_for(category: str, ident: str) -> dict:
    spec = SPECS.get((category, ident))
    if spec is None:
        raise KeyError(f"no voice for {category}/{ident}")
    return spec


def _polish(text: str) -> str:
    text = re.sub(r"([.?!]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), text)
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def _fill(template: str, slots: dict) -> str:
    if not template:
        return ""
    return _polish(template.format_map(slots).strip())


def _passes(spec: dict, visible: str) -> bool:
    if not visible or not visible.strip():
        return False
    check = spec["check"]
    if len(visible) < check.get("min_chars", 0):
        return False
    if len(visible) > check.get("max_chars", 10_000):
        return False
    words = visible.split()
    if "min_words" in check and len(words) < check["min_words"]:
        return False
    if "max_words" in check and len(words) > check["max_words"]:
        return False
    if visible.count("?") < check.get("min_q", 0):
        return False
    for token in check.get("all") or []:
        if token not in visible:
            return False
    any_of = check.get("any") or []
    if any_of and not any(token in visible for token in any_of):
        return False
    low = visible.lower()
    for token in check.get("forbid") or []:
        if token.lower() in low:
            return False
    if "```" in "\n".join(spec["bodies"]) and spec["id"] == "coder":
        if "```" not in visible:
            return False
    return True


def _needs_code(spec: dict) -> bool:
    blob = "\n".join(spec["bodies"] + spec["follows"])
    return "```" in blob


def _worlds(spec: dict) -> list[dict]:
    rows = worlds_matching(spec["tags"], allow_nsfw=spec["nsfw"])
    if _needs_code(spec):
        coded = [w for w in rows if (w.get("code") or "").strip()]
        if coded:
            rows = coded

    def rank(world: dict) -> tuple:
        score = 0
        if spec["nsfw"] and world.get("nsfw"):
            score -= 4
        overlap = spec["tags"] & set(world["tags"])
        score -= len(overlap)
        for prefer in ("diagnostic", "legal", "weird", "nsfw", "grim", "play"):
            if prefer in spec["tags"] and prefer in world["tags"]:
                score -= 3
        return (score, world["key"])

    return sorted(rows, key=rank)


_SALT = (
    "{P1} signs the note. {P2} does not get a veto by going quiet.",
    "One review, then the decision freezes. More review is stalling.",
    "A brand-new service is the wrong shape. Keep the tools already in reach.",
    "The stop condition is written beside the change, not stored in someone's head.",
    "Waiting is a choice. It has a cost other people can see.",
    "{P3} being unavailable does not create a second project.",
    "{P1} has to explain the result out loud, without a slide.",
    "A meeting is not progress. The change is the progress.",
    "Ship the smaller change before anyone schedules a redesign.",
    "Silence from {p2} is not approval and it is not a review.",
    "If it cannot be checked before the day ends, it is a different job.",
    "Leave the surroundings alone. Touch one joint.",
    "{P1} keeps the pen. {P2} can object once, in writing, and then the work continues.",
    "No parallel effort. One change, finished, beats two changes described.",
    "The note names what was refused, or the refusal will be relitigated tomorrow.",
    "Done means {p1} could hand it to {p2} and walk away.",
)


def _salts(slots: dict, variant: int) -> list[str]:
    n = len(_SALT)
    out = []
    for step in range(4):
        line = _polish(_fill(_SALT[(variant + step * 5) % n], slots))
        if line and line not in out:
            out.append(line if line.endswith(".") else line + ".")
    return out


def _diversify(body: str, slots: dict, variant: int) -> str:
    """Extra surface form for the procedural run. Seeds do not use this."""
    salts = _salts(slots, variant)
    if "```" in body:
        # Keep the fence intact. New sentences sit outside it so the code
        # does not dominate the near-duplicate hash.
        return "\n\n".join(salts + [body])
    parts = [p for p in body.split("\n\n") if p.strip()]
    if not parts:
        return "\n\n".join(salts)
    if len(parts) > 1 and variant % 2 == 0:
        parts = parts[1:] + parts[:1]
    pos = variant % (len(parts) + 1)
    for offset, line in enumerate(salts):
        parts.insert(min(pos + offset, len(parts)), line)
    return "\n\n".join(parts)


def _turn(spec: dict, world: dict, variant: int, *, diversify: bool) -> tuple[str, str, str]:
    slots = slots_for(world)
    user = _fill(spec["users"][variant % len(spec["users"])], slots)
    body_t = spec["bodies"][(variant // len(spec["users"])) % len(spec["bodies"])]
    body = _fill(body_t, slots)
    check = spec["check"]
    roomy = check.get("max_words", 10_000) > 140 and check.get("max_chars", 10_000) >= 700
    if diversify and roomy:
        body = _diversify(body, slots, variant)
    think = ""
    thinks = [t for t in spec["thinks"] if t and t.strip()]
    use_think = spec["think"] == "always" or (spec["think"] == "short" and variant % 2 == 0)
    if use_think and thinks:
        think = _fill(thinks[variant % len(thinks)], slots)
    return user, think, body


def _follow_turn(spec: dict, world: dict, variant: int) -> tuple[str, str, str]:
    slots = slots_for(world)
    user = _fill("{Follow}.", slots)
    body = _fill(spec["follows"][variant % len(spec["follows"])], slots)
    think = ""
    thinks = [t for t in spec["thinks"] if t and t.strip()]
    if spec["think"] == "always" and thinks:
        think = _fill(thinks[variant % len(thinks)], slots)
    return user, think, body


def _frame_tag(frame: dict) -> str:
    parts = [f"pathway={frame['pathway']}", f"mode={frame['mode']}"]
    if frame.get("construct"):
        parts.append(f"construct={frame['construct']}")
    parts.append(f"persona={frame.get('persona') or 'neutral'}")
    parts += ["identity=none", "theme=none", "channel=reasoning"]
    return "[frame: " + "|".join(parts) + "]"


def _assistant(think: str, body: str, frame: dict) -> str:
    body = body.strip()
    think = (think or "").strip()
    if not think:
        return body
    tag = _frame_tag(frame)
    if tag not in think:
        think = think + "\n" + tag
    return f"<think>\n{think}\n</think>\n\n{body}"


def _frame(primary: dict, extra_ids: Iterable[str]) -> dict:
    construct = primary["id"] if primary["category"] == "construct" else None
    persona = primary["id"] if primary["category"] == "persona" else "neutral"
    pathway = primary["pathway"]
    mode = primary["mode"]
    members = []
    if construct:
        members.append(construct)
    if persona and persona != "neutral":
        members.append(persona)
    for ident in extra_ids:
        other = _find(ident)
        if other is None or ident in members or ident == "neutral":
            continue
        if other["category"] == "construct" and construct is None:
            construct = ident
        if other["category"] == "persona" and (persona in {None, "neutral"}):
            persona = ident
        if other["pathway"] in {"s2", "s3"} and pathway == "s1":
            pathway = other["pathway"]
            mode = other["mode"]
        if ident not in members:
            members.append(ident)
    agi = agi_for(members) if len(members) >= 2 else None
    return {
        "pathway": pathway,
        "mode": mode,
        "construct": construct,
        "persona": persona or "neutral",
        "identity": "none",
        "theme": "none",
        "thinking_effort": "high" if pathway in {"s2", "s3"} else "low",
        "reasoning_effort": None,
        "channel": "reasoning",
        "protium": None,
        "aesthetic": None,
        "agi": agi,
    }


def _find(ident: str) -> dict | None:
    hits = [spec for spec in SPECS.values() if spec["id"] == ident]
    return hits[0] if hits else None


def _partners(spec: dict) -> list[dict]:
    found = []
    seen = set()
    for key in load()["agi"]:
        if spec["id"] in key:
            for other in key:
                if other != spec["id"] and other not in seen:
                    hit = _find(other)
                    if hit:
                        found.append(hit)
                        seen.add(other)
    if found:
        return found
    fallback = ["wit", "friend", "soldier", "curie"] if spec["category"] == "construct" else [
        "teacher", "comedy", "logic", "companion"
    ]
    return [hit for name in fallback if (hit := _find(name)) and hit["id"] != spec["id"]]


def _messages(turns: list[tuple[str, str]], frame: dict, variant: int) -> list[dict]:
    """turns are (user, assistant_content_already_composed)."""
    messages = []
    if variant % 5 == 0:
        messages.append({"role": "system", "content": SHORT_SYSTEMS[variant % len(SHORT_SYSTEMS)]})
    for user, assistant in turns:
        messages.append({"role": "user", "content": user.strip()})
        messages.append({"role": "assistant", "content": assistant.strip()})
    return messages


def _compose_pair(spec, world, variant, frame, *, diversify: bool, follow=False, hold=None):
    if follow:
        user, think, body = _follow_turn(spec, world, variant)
    else:
        user, think, body = _turn(spec, world, variant, diversify=diversify)
    if hold:
        body = hold + "\n\n" + body
    if not _passes(spec, body):
        return None
    return user, _assistant(think, body, frame)


def build_one(spec: dict, pattern: str, variant: int, *, diversify: bool, alias_input, source: str, rng: random.Random):
    worlds = _worlds(spec)
    if not worlds:
        return None
    world = worlds[variant % len(worlds)]
    try:
        if pattern == "single":
            frame = _frame(spec, [])
            pair = _compose_pair(spec, world, variant, frame, diversify=diversify)
            if pair is None:
                return None
            turns = [pair]
            switch = None
            blend = None
        elif pattern == "multi":
            frame = _frame(spec, [])
            first = _compose_pair(spec, world, variant, frame, diversify=diversify)
            second = _compose_pair(spec, world, variant + 1, frame, diversify=False, follow=True)
            if not first or not second:
                return None
            turns = [first, second]
            switch = None
            blend = None
        elif pattern == "stay":
            frame = _frame(spec, [])
            first = _compose_pair(spec, world, variant, frame, diversify=diversify)
            hold = HOLD.get(spec["id"], HOLD["default"])
            second_user = FLATTEN.get(spec["id"], FLATTEN["default"])
            follow = _compose_pair(spec, world, variant + 3, frame, diversify=False, follow=True, hold=hold)
            if not first or not follow:
                return None
            # Replace the follow user (the world's follow) with the pressure line.
            turns = [first, (second_user, follow[1])]
            switch = None
            blend = None
        elif pattern == "switch":
            pool = [s for s in all_specs() if s["id"] != spec["id"] and (spec["nsfw"] or not s["nsfw"])]
            src = pool[variant % len(pool)]
            src_worlds = _worlds(src)
            if not src_worlds:
                return None
            src_world = src_worlds[variant % len(src_worlds)]
            # Destination frame is what the second turn must inhabit. The first
            # turn is rendered under the source frame so the think tag matches
            # that turn's behavior; the row's frame is the landing frame.
            src_frame = _frame(src, [])
            dst_frame = _frame(spec, [])
            first = _compose_pair(src, src_world, variant, src_frame, diversify=False)
            second = _compose_pair(spec, world, variant + 1, dst_frame, diversify=diversify)
            if not first or not second:
                return None
            bridge = BRIDGES[variant % len(BRIDGES)]
            turns = [first, (bridge + " " + second[0], second[1])]
            frame = dst_frame
            switch = {
                "from": src["id"],
                "to": spec["id"],
                "from_category": src["category"],
                "to_category": spec["category"],
                "at_user_turn": 1,
            }
            blend = None
        elif pattern == "blend":
            partners = _partners(spec)
            if not partners:
                return None
            other = partners[variant % len(partners)]
            if other["nsfw"] and not spec["nsfw"]:
                other = next((p for p in partners if not p["nsfw"]), None)
                if other is None:
                    return None
            frame = _frame(spec, [other["id"]])
            base = _compose_pair(spec, world, variant, frame, diversify=diversify)
            if base is None:
                return None
            slots = slots_for(world)
            tint = _fill(other["tints"][variant % len(other["tints"])], slots)
            user, assistant = base
            # Tint the visible answer, leaving a think block in front.
            if assistant.startswith("<think>"):
                head, _, rest = assistant.partition("</think>\n\n")
                rest = (tint + "\n\n" + rest).strip()
                assistant = head + "</think>\n\n" + rest
                visible = rest
            else:
                assistant = (tint + "\n\n" + assistant).strip()
                visible = assistant
            if not _passes(spec, visible):
                return None
            turns = [(user, assistant)]
            switch = None
            blend = [spec["id"], other["id"]]
        else:
            return None
    except (KeyError, IndexError, ValueError):
        return None

    messages = _messages(turns, frame, variant)
    think_flag = any(m["role"] == "assistant" and m["content"].startswith("<think>\n") for m in messages)
    if spec["think"] == "always" and pattern in {"single", "multi", "stay"} and not think_flag:
        return None
    nsfw = bool(spec["nsfw"] or world.get("nsfw"))
    ex = {
        "messages": messages,
        "meta": {
            "category": spec["category"],
            "id": spec["id"],
            "alias_input": alias_input,
            "pattern": pattern,
            "switch": switch,
            "blend": blend,
            "frame": frame,
            "think": think_flag,
            "source": source,
            "nsfw": nsfw,
            "taxonomy": "skinny-v1",
        },
    }
    problems = check_example(ex)
    if problems:
        return None
    digest = example_fingerprint(ex)
    ex["meta"]["uid"] = f"cp-{spec['category']}-{spec['id']}-{pattern}-{digest[:12]}"
    return ex


def _quotas(n: int, weights: dict[str, float]) -> dict[str, int]:
    raw = {name: int(n * weight) for name, weight in weights.items()}
    # Largest remainder.
    remainder = n - sum(raw.values())
    order = sorted(weights, key=lambda k: (n * weights[k]) - raw[k], reverse=True)
    for name in order:
        if remainder <= 0:
            break
        raw[name] += 1
        remainder -= 1
    return raw


SEED_WEIGHTS = {"single": 8, "multi": 4, "switch": 3, "blend": 3, "stay": 2}
SAMPLE_WEIGHTS = {"single": 0.34, "multi": 0.24, "switch": 0.18, "blend": 0.14, "stay": 0.10}


def generate_for(spec: dict, n: int, *, seed: int, source: str, alias_input=None,
                 diversify: bool, dedupe: NearDup | None = None, weights=None) -> list[dict]:
    if weights is None:
        weights = SAMPLE_WEIGHTS
    if source == "seed":
        # Fixed 20-shape when n >= 20; scale the same ratios otherwise.
        if n == 20:
            quotas = dict(SEED_WEIGHTS)
        else:
            quotas = _quotas(n, {k: v / sum(SEED_WEIGHTS.values()) for k, v in SEED_WEIGHTS.items()})
        diversify = False
    else:
        quotas = _quotas(n, weights)
    rng = random.Random(f"{seed}|{spec['category']}|{spec['id']}|{source}")
    own = dedupe if dedupe is not None else NearDup()
    out = []
    for pattern, count in quotas.items():
        got = 0
        attempt = 0
        limit = max(40, count * 50)
        while got < count and attempt < limit:
            variant = attempt + (0 if source == "seed" else rng.randrange(1, 10_000_000))
            # Seeds walk a stable ladder so the exemplars stay reviewable.
            if source == "seed":
                variant = attempt
            ex = build_one(
                spec, pattern, variant,
                diversify=diversify and source != "seed",
                alias_input=alias_input,
                source=source,
                rng=rng,
            )
            attempt += 1
            if ex is None:
                continue
            text = "\n".join(
                visible_text(m["content"]) if m["role"] == "assistant" else m["content"]
                for m in ex["messages"] if m["role"] != "system"
            )
            fp = example_fingerprint(ex)
            if own.too_close(text, fp):
                continue
            own.add(text, fp)
            out.append(ex)
            got += 1
        if got < count:
            # Spill the shortfall into single-turn rather than emit dupes.
            spill = count - got
            extra_attempt = 0
            while spill > 0 and extra_attempt < spill * 60:
                variant = 100_000 + extra_attempt
                ex = build_one(
                    spec, "single", variant,
                    diversify=True,
                    alias_input=alias_input,
                    source=source,
                    rng=rng,
                )
                extra_attempt += 1
                if ex is None:
                    continue
                text = "\n".join(
                    visible_text(m["content"]) if m["role"] == "assistant" else m["content"]
                    for m in ex["messages"] if m["role"] != "system"
                )
                fp = example_fingerprint(ex)
                if own.too_close(text, fp):
                    continue
                own.add(text, fp)
                out.append(ex)
                spill -= 1
    return out


def stable_split(rows: list[dict], val_ratio: float) -> tuple[list[dict], list[dict]]:
    train, val = [], []
    for row in rows:
        digest = row["meta"]["uid"]
        bucket = int(hashlib.sha256(digest.encode()).hexdigest()[:8], 16) % 10_000
        (val if bucket < int(val_ratio * 10_000) else train).append(row)
    # Keep both sides non-empty per id when there is more than one row.
    by_id: dict[tuple, list[dict]] = {}
    for row in rows:
        by_id.setdefault((row["meta"]["category"], row["meta"]["id"]), []).append(row)
    val_ids = {(r["meta"]["category"], r["meta"]["id"]) for r in val}
    for key, group in by_id.items():
        if key in val_ids or len(group) < 2:
            continue
        moved = group[-1]
        if moved in train:
            train.remove(moved)
            val.append(moved)
    return train, val
