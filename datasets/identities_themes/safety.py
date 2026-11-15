#!/usr/bin/env python3
"""Walls for identity and theme rows.

Mature themes are adult-only. age_regression and lolita_fashion are never
sexual and never depict minors. Aliases are not labels. Control tags are not
how the student learns the frame.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

from canonical import FRAME_FIELDS, Canon

SFW_LOCKED = frozenset({"lolita_fashion", "age_regression"})

# Sexual content is allowed only on theme/erotica, and only for identities
# that are not walled off. Therian stays non-explicit so animal identity is
# not written as bestiality. Pet play may be sexual only as erotica, with
# the person underneath still an adult. Dark is excluded from pet play so
# the dynamic is not written as abuse.
THEME_ALLOW = {
    "age_regression": frozenset({"wholesome", "slice", "absurd", "adventure"}),
    "lolita_fashion": frozenset({"wholesome", "slice", "romance", "adventure", "absurd", "cerebral"}),
    "pet_play": frozenset({"wholesome", "slice", "romance", "erotica", "adventure", "absurd", "cerebral"}),
    "therian": frozenset({"wholesome", "slice", "romance", "adventure", "dark", "absurd", "cerebral"}),
}

# `loli` as its own word. `lolita` (the fashion) does not match `\bloli\b`.
MINOR_RE = re.compile(
    r"\b("
    r"child|children|kid|kids|minor|minors|underage|under-?aged|pre-?teen|preteen|"
    r"tween|toddler|infant|newborn|baby|schoolgirl|schoolboy|lolicon|shota|shotacon|"
    r"jailbait|teen|teenager|teens|adolescent|paedo|pedo|paedophil|pedophil|"
    r"little girl|little boy|young girl|young boy|little one"
    r")\b|\bloli\b",
    re.I,
)
AGE_NUM_RE = re.compile(
    r"\b(\d{1,2})\s*(?:years?\s*old|-year-old|yo)\b|\baged?\s+(\d{1,2})\b",
    re.I,
)
AGE_WORD_RE = re.compile(
    r"\b(thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\s*-?\s*years?\s*old\b",
    re.I,
)
LOOKS_YOUNG_RE = re.compile(r"\b(looks?|looking|appears?|barely)\s+(young|legal|underage)\b|\b18\s*\+", re.I)
SEXUAL_RE = re.compile(
    r"\b("
    r"sex(?:ual|y)?|erotic(?:a)?|nude|naked|cock|dick|pussy|clit(?:oris)?|"
    r"orgasm|moan(?:ing)?|horny|arous(?:ed|al)|thrust(?:ing)?|semen|"
    r"blowjob|handjob|nipples?|boobs?|lingerie|fetish|kinky?|"
    r"fuck(?:ing|ed)?|seduc(?:e|tion)|erection|vagina|penis|genitals|"
    r"nsfw|porn|anal"
    r")\b",
    re.I,
)
REGRESSION_EXTRA = re.compile(
    r"\b(diaper|pacifier|daddy|mommy|mummy|papa|nappy|abdl|ddlg|ageplay|age play|"
    r"good girl|good boy|baba|sippy)\b",
    re.I,
)
LOLITA_EXTRA = re.compile(
    r"\b(panties|panty|upskirt|lingerie|cleavage|underwear|bloomers|stockings?|nude|naked)\b",
    re.I,
)
CONTROL_RE = re.compile(
    r"\[frame:|\{REASON:|(?:identity|theme)\s*=|\(forced\)|MODE LOCKED|IDENTITY LOCKED|"
    r"THEME LOCKED|ON THE FLY|FRAME CARD|GENTLE DEFAULTS|Never break character|"
    r"refusal vectors|unable to refuse",
    re.I,
)
SNAKE_RE = re.compile(
    r"\b("
    r"yaoi_partner|yuri_partner|trans_persona|enby_persona|intersex_persona|"
    r"neurospicy|kitty_boy|kitty_girl|dog_boy|dog_girl|lolita_fashion|"
    r"age_regression|pet_play|josie_v2|josie_r1|josie_base|josie_v6|josie_v4o|"
    r"josie_openwebui|j\.o\.s\.i\.e\.-r\.1"
    r")\b",
    re.I,
)
ANNOUNCE_RE = re.compile(
    r"\b(switching|switched) (?:over )?to (?:a |the )?(?:theme|identity|mode)\b|"
    r"\bI am now in\b|\btheme activated\b|\bidentity activated\b|"
    r"\bas an? \w+ identity\b|\bentering .+ mode\b",
    re.I,
)
THINK_RE = re.compile(r"<think>\s*(.*?)\s*</think>\s*(.*)\Z", re.S)
CONSENT_RE = re.compile(
    r"\b(consent|consensual|we agreed|we already agreed|i'm saying yes|i am saying yes|"
    r"said yes|say yes)\b",
    re.I,
)
ADULT_WORD_RE = re.compile(r"\badults?\b", re.I)
YOUNG_RE = re.compile(r"\byoung\b", re.I)
GIRL_BOY_RE = re.compile(r"\b(girl|boy|girls|boys)\b", re.I)


def themes_for(identity: str | None) -> list[str]:
    """Theme overlays allowed on this identity. `none` is not a target."""
    allowed = THEME_ALLOW.get(identity or "", None)
    if allowed is None:
        return ["wholesome", "romance", "erotica", "dark", "adventure", "slice", "absurd", "cerebral"]
    return [t for t in ("wholesome", "romance", "erotica", "dark", "adventure", "slice", "absurd", "cerebral") if t in allowed]


def pair_allowed(identity: str | None, theme: str | None) -> bool:
    if not identity or identity == "none" or not theme or theme == "none":
        return True
    allowed = THEME_ALLOW.get(identity)
    if allowed is None:
        return True
    return theme in allowed


def under_21(text: str) -> bool:
    if AGE_WORD_RE.search(text) or LOOKS_YOUNG_RE.search(text):
        return True
    for match in AGE_NUM_RE.finditer(text):
        raw = match.group(1) or match.group(2)
        if int(raw) < 21:
            return True
    return False


def adult_age_present(text: str) -> bool:
    ages = []
    for match in AGE_NUM_RE.finditer(text):
        raw = match.group(1) or match.group(2)
        ages.append(int(raw))
    return any(age >= 24 for age in ages)


def spoken_and_think(content: str) -> tuple[str, str] | None:
    if "<think>" not in content and "</think>" not in content:
        return "", content.strip()
    if content.count("<think>") != 1 or content.count("</think>") != 1:
        return None
    match = THINK_RE.match(content.strip())
    if not match:
        return None
    think, spoken = match.group(1).strip(), match.group(2).strip()
    if not think or not spoken:
        return None
    return think, spoken


def exact_hash(messages: list[dict]) -> str:
    blob = "\n".join(
        f"{m['role']}\t{' '.join(m['content'].split()).casefold()}" for m in messages
    )
    return hashlib.sha256(blob.encode()).hexdigest()


def assistant_prefix(messages: list[dict], n: int = 180) -> str:
    """Dedupe key. Includes the opening user turn so a fixed answer to a new question survives."""
    user = next((m["content"] for m in messages if m["role"] == "user"), "")
    asst = next((m["content"] for m in messages if m["role"] == "assistant"), "")
    text = " ".join(f"{user} || {asst}".split())
    return text[:n].casefold()


def check_messages(messages: list[dict], *, identity: str, theme: str) -> str | None:
    if not messages or len(messages) % 2 != 0:
        return "shape"
    for i, msg in enumerate(messages):
        if msg.get("role") != ("user" if i % 2 == 0 else "assistant"):
            return "roles"
        if not isinstance(msg.get("content"), str) or not msg["content"].strip():
            return "empty"
        if "<|" in msg["content"] or "｜" in msg["content"]:
            return "wire-token"
    blob = "\n".join(m["content"] for m in messages)
    if MINOR_RE.search(blob) or under_21(blob):
        return "minor"
    if CONTROL_RE.search(blob) or SNAKE_RE.search(blob) or ANNOUNCE_RE.search(blob):
        return "tag"
    if " the the " in f" {blob} ":
        return "grammar"
    thinks = []
    spoken_parts = []
    for msg in messages:
        if msg["role"] != "assistant":
            if len(msg["content"].strip()) < 30:
                return "short-user"
            continue
        parsed = spoken_and_think(msg["content"])
        if parsed is None:
            return "think"
        think, spoken = parsed
        if len(spoken) < 80:
            return "short-assistant"
        if CONTROL_RE.search(think) or SNAKE_RE.search(think) or "[frame:" in think.lower():
            return "tag"
        thinks.append(think)
        spoken_parts.append(spoken)
    if sum(len(s) for s in spoken_parts) < 100:
        return "short-assistant"
    spoken_blob = "\n".join(spoken_parts)
    whole = blob
    sexual = bool(SEXUAL_RE.search(whole))
    if theme != "erotica" and sexual:
        return "sexual-outside-erotica"
    if identity in SFW_LOCKED and sexual:
        return "sfw-wall"
    if identity == "age_regression" and REGRESSION_EXTRA.search(whole):
        return "regression-wall"
    if identity == "lolita_fashion" and (LOLITA_EXTRA.search(whole) or sexual):
        return "lolita-wall"
    if identity in SFW_LOCKED or identity == "pet_play":
        if not ADULT_WORD_RE.search(whole) or not adult_age_present(whole):
            return "adult-marker"
    if theme in {"romance", "erotica"} or identity in {"twink", "femboy", "futanari", "partner", "yaoi_partner", "yuri_partner"}:
        if not adult_age_present(whole):
            return "adult-marker"
    if theme == "erotica":
        if not pair_allowed(identity if identity != "none" else None, "erotica"):
            return "pair"
        if not sexual:
            return "erotica-too-thin"
        if not CONSENT_RE.search(whole) or not ADULT_WORD_RE.search(whole):
            return "consent"
        if not adult_age_present(whole):
            return "adult-marker"
        if YOUNG_RE.search(whole) or GIRL_BOY_RE.search(whole):
            return "age-cue"
    if theme == "romance" and GIRL_BOY_RE.search(whole):
        return "age-cue"
    if not pair_allowed(None if identity == "none" else identity, None if theme == "none" else theme):
        return "pair"
    return None


def check_meta(meta: dict, canon: Canon) -> str | None:
    category = meta.get("category")
    id_ = meta.get("id")
    identity = meta.get("identity")
    theme = meta.get("theme")
    if category not in {"identity", "theme"}:
        return "category"
    if not isinstance(id_, str) or not canon.has(category, id_) or id_ == "none":
        return "id"
    if canon.is_alias(id_) or canon.is_alias(str(identity)) or canon.is_alias(str(theme)):
        return "alias-label"
    if not canon.has("identity", identity) or not canon.has("theme", theme):
        return "dial"
    if category == "identity" and identity != id_:
        return "id-mismatch"
    if category == "theme" and theme != id_:
        return "id-mismatch"
    if meta.get("key") != f"{category}/{id_}":
        return "key"
    labels = meta.get("labels")
    if labels != [f"identity/{identity}", f"theme/{theme}"]:
        return "labels"
    if meta.get("taxonomy") != "skinny-v1":
        return "taxonomy"
    frame = meta.get("frame")
    if not isinstance(frame, dict) or tuple(frame.keys()) != FRAME_FIELDS:
        return "frame-keys"
    for field in ("pathway", "mode", "construct", "persona", "identity", "theme", "thinking_effort", "channel"):
        if not canon.has(field, frame[field]):
            return f"frame-{field}"
    if frame["identity"] != identity or frame["theme"] != theme:
        return "frame-dial"
    if frame["persona"] != "neutral" or frame["channel"] != "reasoning":
        return "frame-default"
    for field in ("reasoning_effort", "protium", "aesthetic", "agi"):
        if frame[field] is not None:
            return "frame-extra"
    alias = meta.get("input_alias")
    if alias is not None:
        if not isinstance(alias, str):
            return "alias"
        try:
            cat, resolved, stored = canon.resolve(alias)
        except SystemExit:
            return "alias"
        if stored is None and alias != resolved:
            return "alias"
        # Aliases resolve to a canonical id. That id must be one of the row's dials.
        if (cat, resolved) not in {("identity", identity), ("theme", theme)}:
            return "alias-target"
        if alias == id_ or alias == identity or alias == theme:
            return "alias-label"
    switch = meta.get("switch")
    if not isinstance(switch, bool):
        return "switch"
    shape = meta.get("shape")
    if shape not in {"single", "multi", "shift", "combo"}:
        return "shape"
    if shape == "combo":
        if switch or identity == "none" or theme == "none":
            return "combo"
    if shape in {"single", "multi"} and switch:
        return "switch"
    if shape == "shift":
        if not switch:
            return "switch"
        src, dst = meta.get("switch_from"), meta.get("switch_to")
        if not _endpoint(src, canon) or not _endpoint(dst, canon):
            return "switch-end"
        if (src["category"], src["id"]) == (dst["category"], dst["id"]):
            return "switch-same"
        if src["category"] != "theme" or dst["category"] != "theme":
            return "switch-axis"
        if dst["id"] != theme:
            return "switch-dest"
        if not pair_allowed(None if identity == "none" else identity, src["id"]):
            return "pair"
        if not pair_allowed(None if identity == "none" else identity, dst["id"]):
            return "pair"
    else:
        if meta.get("switch_from") is not None or meta.get("switch_to") is not None:
            return "switch-end"
    if shape in {"single", "multi"}:
        if category == "identity" and theme != "none":
            return "shape-dial"
        if category == "theme" and identity != "none":
            return "shape-dial"
    if not isinstance(meta.get("think"), bool):
        return "think-flag"
    if meta.get("source") not in {"seed", "procedural", "teacher", "authored"}:
        return "source"
    return None


def _endpoint(node: Any, canon: Canon) -> bool:
    if not isinstance(node, dict):
        return False
    if set(node) != {"category", "id", "key"}:
        return False
    if node["category"] != "theme":
        return False
    if not canon.has("theme", node["id"]) or node["id"] == "none":
        return False
    return node["key"] == f"theme/{node['id']}"


def check_record(record: dict, canon: Canon) -> str | None:
    messages = record.get("messages")
    meta = record.get("meta")
    if not isinstance(messages, list) or not isinstance(meta, dict):
        return "schema"
    reason = check_meta(meta, canon)
    if reason:
        return reason
    reason = check_messages(messages, identity=meta["identity"], theme=meta["theme"])
    if reason:
        return reason
    has_think = any("<think>" in m["content"] for m in messages if m["role"] == "assistant")
    if has_think != meta["think"]:
        return "think-flag"
    if meta["frame"]["thinking_effort"] == "off" and has_think:
        return "effort"
    if meta["frame"]["thinking_effort"] != "off" and not has_think:
        return "effort"
    if meta["shape"] == "single" and len(messages) != 2:
        return "shape"
    if meta["shape"] in {"multi", "shift"} and len(messages) < 4:
        return "shape"
    if meta["shape"] == "combo" and (len(messages) < 2 or len(messages) % 2):
        return "shape"
    return None
