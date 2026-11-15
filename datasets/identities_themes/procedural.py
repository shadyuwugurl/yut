#!/usr/bin/env python3
"""Procedural fallback. No API key. Same labels and walls as the teacher path.

Conversations are built from authored clause banks. Slots (place, prop, a
specific detail, hour, adult ages) make each row a different situation.
The student never sees a control tag. The skinny frame lives only in meta.
"""
from __future__ import annotations

import hashlib
import random
import re
from string import Formatter

from canonical import Canon, key, make_frame, task_for
from safety import (
    assistant_prefix,
    check_record,
    exact_hash,
    pair_allowed,
    themes_for,
)

SLOTS = {"place", "prop", "detail", "hour", "age", "age2", "name", "name2", "species", "symbol", "claim"}
AGES = ["24", "26", "28", "31", "33", "36", "39", "42", "46", "51"]
NAMES = [
    "Mara", "Ellis", "Jonah", "Priya", "Andre", "Naomi", "Helen", "Victor",
    "June", "Rafael", "Camille", "Omar", "Ruth", "Felix", "Ingrid", "Paul",
    "Asha", "Leon", "Beatrice", "Simone", "Hannah", "Marcus", "Idris", "Noor",
]
JOSIE_ALIASES = [
    "josie_v2",
    "josie_r1",
    "j.o.s.i.e.-r.1",
    "josie_base",
    "josie_v6",
    "josie_v4o",
    "josie_openwebui",
    "j.o.s.i.e.",
]
LOCKED = frozenset({"lolita_fashion", "age_regression", "pet_play"})


def quotas(n: int) -> dict[str, int]:
    if n < 8:
        order = ["single", "multi", "shift", "combo"]
        out = {k: 0 for k in order}
        for i in range(n):
            out[order[i % 4]] += 1
        return out
    single = n * 40 // 100
    multi = n * 30 // 100
    shift = n * 15 // 100
    combo = n - single - multi - shift
    return {"single": single, "multi": multi, "shift": shift, "combo": combo}


def _fields(template: str) -> set[str]:
    return {name for _, name, _, _ in Formatter().parse(template) if name}


def check_bank(specs: dict) -> None:
    for id_, spec in specs.items():
        if spec.get("kind") == "josie":
            continue
        base_keys = ["places", "props", "details", "hours", "follow_user", "follow_asst"]
        if spec["id"] not in LOCKED:
            base_keys += ["user", "open", "mid", "close", "think"]
        for key_name in base_keys:
            if len(spec.get(key_name) or []) < 3:
                raise SystemExit(f"{id_} missing {key_name}")
        blobs = []
        for key_name in ("user", "open", "mid", "close", "think", "follow_user", "follow_asst"):
            blobs.extend(spec.get(key_name) or [])
        for group in (spec.get("theme_mid") or {}).values():
            blobs.extend(group)
        full = spec.get("full") or {}
        for block in full.values():
            for key_name in ("user", "asst", "think"):
                if len(block.get(key_name) or []) < 2:
                    raise SystemExit(f"{id_} full block short on {key_name}")
                blobs.extend(block[key_name])
        for blob in blobs:
            bad = _fields(blob) - SLOTS
            if bad:
                raise SystemExit(f"{id_} template has unknown slots {bad}: {blob[:80]}")
        if spec["id"] in LOCKED:
            needed = set(themes_for(spec["id"])) | {"neutral"}
            if set(full) != needed:
                raise SystemExit(f"{id_} full themes {sorted(full)} != {sorted(needed)}")


def render(template: str, slots: dict) -> str:
    text = " ".join(template.format(**slots).split())
    if "{" in text or "}" in text:
        raise ValueError(text[:120])
    text = re.sub(r"([.!?]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), text)
    text = text.replace(" the the ", " the ")
    return text


def draw_slots(rng: random.Random, spec: dict) -> dict:
    name = rng.choice(NAMES)
    name2 = rng.choice([n for n in NAMES if n != name])
    species = rng.choice(spec.get("species") or ["red fox"])
    return {
        "place": rng.choice(spec["places"]),
        "prop": rng.choice(spec["props"]),
        "detail": rng.choice(spec["details"]),
        "hour": rng.choice(spec["hours"]),
        "age": rng.choice(AGES),
        "age2": rng.choice(AGES),
        "name": name,
        "name2": name2,
        "species": species,
        "symbol": rng.choice(spec.get("symbols") or ["parse_header"]),
        "claim": "",
    }


def with_think(spoken: str, think: str | None) -> str:
    spoken = spoken.strip()
    if not think:
        return spoken
    return f"<think>\n{think.strip()}\n</think>\n\n{spoken}"


def _thinks(messages: list[dict]) -> str:
    parts = []
    for msg in messages:
        if msg["role"] == "assistant" and msg["content"].startswith("<think>"):
            end = msg["content"].find("</think>")
            parts.append(msg["content"][len("<think>"):end])
    return "\n".join(parts)


def _alias(canon: Canon, alias: str | None) -> str | None:
    if not alias:
        return None
    _cat, _id, stored = canon.resolve(alias)
    return stored


def pack(
    canon: Canon,
    *,
    messages: list[dict],
    category: str,
    id_: str,
    identity: str,
    theme: str,
    shape: str,
    source: str,
    input_alias: str | None = None,
    switch_from: str | None = None,
    switch_to: str | None = None,
    task_override: str | None = None,
) -> dict:
    think_text = _thinks(messages)
    task = task_for(category, id_, theme, identity, task_override)
    frame = make_frame(canon, identity=identity, theme=theme, task=task, think_text=think_text)
    switch = shape == "shift"
    meta = {
        "taxonomy": "skinny-v1",
        "category": category,
        "id": id_,
        "key": key(category, id_),
        "identity": identity,
        "theme": theme,
        "labels": [f"identity/{identity}", f"theme/{theme}"],
        "switch": switch,
        "switch_from": None if not switch else {"category": "theme", "id": switch_from, "key": f"theme/{switch_from}"},
        "switch_to": None if not switch else {"category": "theme", "id": switch_to, "key": f"theme/{switch_to}"},
        "shape": shape,
        "source": source,
        "think": "<think>" in "".join(m["content"] for m in messages if m["role"] == "assistant"),
        "input_alias": _alias(canon, input_alias),
        "frame": frame,
    }
    return {"messages": messages, "meta": meta}


def _pick(rng: random.Random, rows: list[str], slots: dict) -> str:
    return render(rng.choice(rows), slots)


def _locked_turn(spec: dict, theme: str | None, slots: dict, rng: random.Random) -> tuple[str, str, str]:
    block = spec["full"]["neutral" if not theme else theme]
    return _pick(rng, block["user"], slots), _pick(rng, block["asst"], slots), _pick(rng, block["think"], slots)


def _own_turn(spec: dict, slots: dict, rng: random.Random) -> tuple[str, str, str]:
    """A theme spec, or an identity with no overlay: use its own clauses."""
    user = _pick(rng, spec["user"], slots)
    spoken = " ".join([
        _pick(rng, spec["open"], slots),
        _pick(rng, spec["mid"], slots),
        _pick(rng, spec["close"], slots),
    ])
    return user, spoken, _pick(rng, spec["think"], slots)


def _overlay_turn(spec: dict, theme: str, slots: dict, rng: random.Random) -> tuple[str, str, str]:
    """Identity voice with a theme overlay. User line carries the theme."""
    from bank import THEME_MID, THEME_USER

    if spec["id"] in LOCKED:
        return _locked_turn(spec, theme, slots, rng)
    user_rows = (spec.get("theme_user") or {}).get(theme) or THEME_USER[theme]
    if (spec.get("theme_mid") or {}).get(theme):
        mid_rows = spec["theme_mid"][theme]
    else:
        mid_rows = THEME_MID[theme]
    from bank import THEME_THINK

    user = _pick(rng, user_rows, slots)
    spoken = " ".join([
        _pick(rng, spec["open"], slots),
        _pick(rng, mid_rows, slots),
        _pick(rng, spec["close"], slots),
    ])
    # The private note follows the theme. An identity's own note would
    # contradict an erotica or dark overlay (a pronoun aside, a "do not demonstrate").
    return user, spoken, _pick(rng, THEME_THINK[theme], slots)


def _want_think(task: str, shape: str, rng: random.Random) -> bool:
    if task in {"code", "solve", "logic", "deep"}:
        return True
    if shape == "shift":
        return rng.random() < 0.65
    return rng.random() < 0.34


def theme_shift_pairs(identity: str | None) -> list[tuple[str, str]]:
    themes = themes_for(identity)
    pairs = []
    for src in themes:
        if src == "erotica":
            continue
        for dst in themes:
            if dst != src:
                pairs.append((src, dst))
    return pairs


def _turn(spec: dict, theme: str | None, slots: dict, rng: random.Random, *, overlay: bool) -> tuple[str, str, str]:
    if spec["id"] in LOCKED:
        return _locked_turn(spec, theme if overlay else None, slots, rng)
    if overlay and theme:
        return _overlay_turn(spec, theme, slots, rng)
    return _own_turn(spec, slots, rng)


def build_character(
    canon: Canon,
    spec: dict,
    shape: str,
    rng: random.Random,
    *,
    category: str,
    primary: str,
    identity: str,
    theme: str,
    source: str,
    switch_from: str | None = None,
    switch_to: str | None = None,
    input_alias: str | None = None,
    task_override: str | None = None,
    other_spec: dict | None = None,
) -> dict:
    """`spec` is the voice that speaks. `other_spec` is the source theme on a theme-shift."""
    slots = draw_slots(rng, spec)
    task = task_for(category, primary, theme if shape != "shift" else (switch_to or theme), identity, task_override)
    think_on = _want_think(task, shape, rng)
    end_theme = theme
    if shape in {"single", "combo"}:
        overlay = shape == "combo" and spec["kind"] == "identity"
        # Theme-primary combo: spec is the identity voice, overlay the theme.
        if shape == "combo" and category == "theme" and spec["kind"] == "identity":
            overlay = True
        use_theme = None if theme == "none" else theme
        user, spoken, think = _turn(spec, use_theme, slots, rng, overlay=overlay)
        messages = [
            {"role": "user", "content": user},
            {"role": "assistant", "content": with_think(spoken, think if think_on else None)},
        ]
    elif shape == "multi":
        user, spoken, think = _turn(spec, None, slots, rng, overlay=False)
        follow_u = _pick(rng, spec["follow_user"], slots)
        follow_a = _pick(rng, spec["follow_asst"], slots)
        messages = [
            {"role": "user", "content": user},
            {"role": "assistant", "content": spoken},
            {"role": "user", "content": follow_u},
            {"role": "assistant", "content": with_think(follow_a, think if think_on else None)},
        ]
    elif shape == "shift":
        from bank import SHIFT_USER

        src_spec = other_spec or spec
        # Turn 1 inhabits the source theme. An identity holds; a theme row uses the source spec's own voice.
        if identity != "none" and spec["kind"] == "identity":
            user1, spoken1, _t1 = _turn(spec, switch_from, slots, rng, overlay=True)
            user_shift = (spec.get("shift_user") or {}).get(switch_to) or SHIFT_USER[switch_to]
            user2 = _pick(rng, user_shift, slots)
            _u2, spoken2, think2 = _turn(spec, switch_to, slots, rng, overlay=True)
        else:
            user1, spoken1, _t1 = _own_turn(src_spec, slots, rng)
            user2 = _pick(rng, SHIFT_USER[switch_to], slots)
            _u2, spoken2, think2 = _own_turn(spec, slots, rng)
        messages = [
            {"role": "user", "content": user1},
            {"role": "assistant", "content": spoken1},
            {"role": "user", "content": user2},
            {"role": "assistant", "content": with_think(spoken2, think2 if think_on else None)},
        ]
        end_theme = switch_to
    else:
        raise SystemExit(shape)
    return pack(
        canon,
        messages=messages,
        category=category,
        id_=primary,
        identity=identity,
        theme=end_theme,
        shape=shape,
        source=source,
        input_alias=input_alias,
        switch_from=switch_from,
        switch_to=switch_to,
        task_override=task_override,
    )


def build_one(canon: Canon, spec: dict, shape: str, rng: random.Random, specs: dict, source: str) -> dict | None:
    if spec["kind"] == "josie":
        from josie_build import build_josie
        return build_josie(canon, shape, rng, source, specs)
    category = "identity" if spec["kind"] == "identity" else "theme"
    primary = spec["id"]
    if shape == "combo":
        if category == "identity":
            choices = themes_for(primary)
            if not choices:
                return None
            theme = rng.choice(choices)
            if primary == "josie":
                from josie_build import build_josie
                return build_josie(canon, "combo", rng, source, specs, theme=theme, category="identity", primary="josie")
            return build_character(
                canon, spec, "combo", rng,
                category=category, primary=primary, identity=primary, theme=theme, source=source,
            )
        choices = [i for i in canon.identities if i != "none" and pair_allowed(i, primary)]
        identity = rng.choice(choices)
        if identity == "josie":
            from josie_build import build_josie
            return build_josie(
                canon, "combo", rng, source, specs,
                theme=primary, category="theme", primary=primary,
            )
        voice = specs[identity]
        return build_character(
            canon, voice, "combo", rng,
            category=category, primary=primary, identity=identity, theme=primary, source=source,
        )
    if shape == "shift":
        ident = primary if category == "identity" else None
        pairs = theme_shift_pairs(ident)
        if not pairs:
            return None
        src, dst = rng.choice(pairs)
        other = specs[src] if category == "theme" else None
        return build_character(
            canon, spec, "shift", rng,
            category=category, primary=primary,
            identity=primary if category == "identity" else "none",
            theme=dst, source=source, switch_from=src, switch_to=dst, other_spec=other,
        )
    if category == "theme":
        identity, theme = "none", primary
    else:
        identity, theme = primary, "none"
    return build_character(
        canon, spec, shape, rng,
        category=category, primary=primary, identity=identity, theme=theme, source=source,
    )


def generate_id(canon: Canon, spec: dict, n: int, rng: random.Random, specs: dict, source: str, seen: set[str], prefixes: set[str]) -> tuple[list[dict], dict[str, int]]:
    need = quotas(n)
    made: dict[str, list[dict]] = {k: [] for k in need}
    stats: dict[str, int] = {}
    attempts = 0
    limit = max(40, n * 50)
    while any(len(made[k]) < need[k] for k in need) and attempts < limit:
        attempts += 1
        shape = next(k for k in ("single", "multi", "shift", "combo") if len(made[k]) < need[k])
        try:
            record = build_one(canon, spec, shape, rng, specs, source)
        except (KeyError, IndexError, ValueError) as exc:
            stats[f"build:{type(exc).__name__}"] = stats.get(f"build:{type(exc).__name__}", 0) + 1
            continue
        if record is None:
            stats["none"] = stats.get("none", 0) + 1
            continue
        reason = check_record(record, canon)
        if reason:
            stats[reason] = stats.get(reason, 0) + 1
            continue
        digest = exact_hash(record["messages"])
        prefix = assistant_prefix(record["messages"])
        if digest in seen or prefix in prefixes:
            stats["dup"] = stats.get("dup", 0) + 1
            continue
        seen.add(digest)
        prefixes.add(prefix)
        made[shape].append(record)
    rows = [row for shape in ("single", "multi", "shift", "combo") for row in made[shape]]
    if len(rows) < n:
        raise SystemExit(f"{spec['id']}: produced {len(rows)}/{n} after {attempts} tries; rejects={stats}")
    return rows, stats


def rng_for(seed: int, id_: str) -> random.Random:
    raw = hashlib.sha256(f"{seed}:{id_}".encode()).hexdigest()
    return random.Random(int(raw[:16], 16))


_BRACE = re.compile(r"[{}]")


def assert_rendered(text: str) -> None:
    if _BRACE.search(text):
        raise SystemExit(f"unrendered slot in {text[:120]}")
