#!/usr/bin/env python3
"""Canonical skinny-v1 labels for identity and theme rows.

The stable key is category + id from docs/taxonomy_skinny.json (skinny-v1).
This branch vendors a snapshot so generation works before that file is on the
base branch. If docs/taxonomy_skinny.json exists, it wins.

Aliases are inputs. They never become meta.id, meta.identity, meta.theme,
or a frame field. Every Josie wording resolves to identity `josie`.
`none` is the name of an unset dial. It is not a generation target.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMPLATE_PATH = ROOT / "chat_template.jinja"
DOCS_TAXONOMY = ROOT / "docs" / "taxonomy_skinny.json"
VENDORED_TAXONOMY = HERE / "taxonomy_skinny.json"
SNAPSHOT_COMMIT = "f32e5448fe87e17b3ede90271379f60e1035f2ad"

FRAME_FIELDS = (
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
)

# Tasks this slice actually is. Values are canonical mode, construct.
TASK_DIALS = {
    "react": ("react", "react"),
    "story": ("react", "story"),
    "companion": ("chat", "companion"),
    "banter": ("banter", "banter"),
    "comedy": ("banter", "comedy"),
    "code": ("code", "coder"),
    "solve": ("solve", "logic"),
    "logic": ("logic", "logic"),
    "deep": ("deep", "omni"),
    "chat": ("chat", "omni"),
    "romance": ("react", "story"),
    "heat": ("react", "story"),
}

IDENTITY_TASK = {
    "partner": "companion",
    "yaoi_partner": "companion",
    "yuri_partner": "companion",
    "omegaverse": "story",
    "trans_persona": "companion",
    "enby_persona": "companion",
    "intersex_persona": "companion",
    "twink": "banter",
    "femboy": "banter",
    "tomboy": "banter",
    "futanari": "story",
    "neurospicy": "companion",
    "furry": "story",
    "therian": "companion",
    "kemonomimi": "story",
    "kitty_boy": "react",
    "kitty_girl": "react",
    "dog_boy": "react",
    "dog_girl": "react",
    "kitsune": "story",
    "bunny": "story",
    "wolf": "story",
    "dragon": "story",
    "vampire": "story",
    "demon": "story",
    "angel": "story",
    "android": "companion",
    "lamia": "story",
    "slime": "story",
    "lolita_fashion": "companion",
    "age_regression": "companion",
    "pet_play": "companion",
    "whimsy": "comedy",
    "josie": "chat",
}

THEME_TASK = {
    "wholesome": "companion",
    "romance": "romance",
    "erotica": "heat",
    "dark": "story",
    "adventure": "story",
    "slice": "companion",
    "absurd": "comedy",
    "cerebral": "logic",
}


class Canon:
    def __init__(self, path: Path, data: dict):
        self.path = path
        self.data = data
        self.version = data.get("taxonomy", "")
        self.by_cat: dict[str, list[str]] = {}
        self.desc: dict[tuple[str, str], str] = {}
        self.alias_to: dict[str, tuple[str, str]] = {}
        self.alias_spell: dict[str, str] = {}
        for item in data["items"]:
            cat, id_ = item["category"], item["id"]
            self.by_cat.setdefault(cat, []).append(id_)
            self.desc[(cat, id_)] = item.get("description", "")
            for alias in item.get("aliases") or []:
                key = alias.casefold()
                if key in self.alias_to and self.alias_to[key] != (cat, id_):
                    raise SystemExit(f"alias {alias!r} maps to two ids")
                self.alias_to[key] = (cat, id_)
                self.alias_spell[key] = alias
        # Merge-from prose names for Josie are inputs too, not labels.
        for merge in data.get("merges") or []:
            into = merge.get("into", "")
            if into != "identity/josie":
                continue
            for src in merge.get("from") or []:
                key = src.casefold()
                self.alias_to.setdefault(key, ("identity", "josie"))
                self.alias_spell.setdefault(key, src)
        self.published: set[str] = set()
        for item in data["items"]:
            for alias in item.get("aliases") or []:
                self.published.add(alias.casefold())
        self.id_set = {cat: set(ids) for cat, ids in self.by_cat.items()}
        self._known_alias_keys = set(self.alias_to)

    @property
    def identities(self) -> list[str]:
        return list(self.by_cat["identity"])

    @property
    def themes(self) -> list[str]:
        return list(self.by_cat["theme"])

    def training_pairs(self) -> list[tuple[str, str]]:
        """Generation targets. `none` stays a label for an unset dial."""
        rows = [("identity", i) for i in self.identities if i != "none"]
        rows += [("theme", t) for t in self.themes if t != "none"]
        return rows

    def has(self, category: str, id_: str) -> bool:
        return id_ in self.id_set.get(category, ())

    def is_alias(self, token: str) -> bool:
        return token.casefold() in self._known_alias_keys and not (
            self.has("identity", token) or self.has("theme", token)
        )

    def resolve(self, token: str, category: str | None = None) -> tuple[str, str, str | None]:
        """Return (category, canonical id, input_alias or None).

        A canonical id returns alias None. An alias returns the canonical id
        and the taxonomy's spelling of that alias.
        """
        if category and self.has(category, token):
            return category, token, None
        if category is None:
            hits = [cat for cat in ("identity", "theme") if self.has(cat, token)]
            if len(hits) == 1:
                return hits[0], token, None
            if len(hits) > 1:
                raise SystemExit(f"{token!r} is an id in more than one category; pass category/id")
        key = token.casefold()
        if key in self.alias_to:
            cat, id_ = self.alias_to[key]
            if category and cat != category:
                raise SystemExit(f"alias {token!r} resolves to {cat}/{id_}, not {category}")
            spelling = self.alias_spell[key]
            # Prose from merges[] is an input. Store the machine alias, not the sentence.
            # Published aliases keep their own spelling (`j.o.s.i.e.-r.1` stays distinct).
            if key not in self.published:
                machine = _JOSIE_PROSE_TO_ALIAS.get(key)
                if machine:
                    spelling = machine
            if spelling == id_:
                return cat, id_, None
            return cat, id_, spelling
        raise SystemExit(f"unknown id or alias: {token!r}")


# Prose names from merges[] that should record a machine alias, not a new label.
_JOSIE_PROSE_TO_ALIAS = {
    "josie v2": "josie_v2",
    "j.o.s.i.e.-r.1": "josie_r1",
    "josie base": "josie_base",
    "josie v6": "josie_v6",
    "josie v4o": "josie_v4o",
    "josie openwebui": "josie_openwebui",
    "charlie's extra josie paragraphs": "josie_v2",
}


def taxonomy_path() -> Path:
    if DOCS_TAXONOMY.is_file():
        return DOCS_TAXONOMY
    if VENDORED_TAXONOMY.is_file():
        return VENDORED_TAXONOMY
    raise SystemExit(
        "missing taxonomy_skinny.json (looked in docs/ and datasets/identities_themes/)"
    )


def load_canon(path: Path | None = None) -> Canon:
    path = path or taxonomy_path()
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("taxonomy") != "skinny-v1":
        raise SystemExit(f"{path} is not skinny-v1")
    canon = Canon(path, data)
    if "josie" not in canon.id_set["identity"]:
        raise SystemExit("skinny taxonomy has no identity/josie")
    if "none" not in canon.id_set["identity"] or "none" not in canon.id_set["theme"]:
        raise SystemExit("skinny taxonomy dropped identity/none or theme/none")
    # Every published Josie alias lands on identity/josie.
    for alias in (
        "josie_v2",
        "josie_r1",
        "j.o.s.i.e.-r.1",
        "josie_base",
        "josie_v6",
        "josie_v4o",
        "josie_openwebui",
        "j.o.s.i.e.",
    ):
        cat, id_, _ = canon.resolve(alias)
        if (cat, id_) != ("identity", "josie"):
            raise SystemExit(f"{alias} did not resolve to identity/josie")
    return canon


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _between(text: str, start: str, end: str) -> str:
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"template is missing {start!r}")
    j = text.find(end, i + len(start))
    if j < 0:
        raise SystemExit(f"template is missing {end!r} after {start!r}")
    return text[i:j].strip()


def _blocks(text: str, axis: str) -> dict[str, str]:
    pat = re.compile(
        r"\{%- (?:if|elif)\s+_"
        + axis
        + r" == '(\w+)' %\}\s*\{%- set _"
        + axis
        + r"_p %\}(.*?)\{%- endset %\}",
        re.S,
    )
    return {m.group(1): " ".join(m.group(2).split()) for m in pat.finditer(text)}


def load_template_text() -> str:
    if not TEMPLATE_PATH.is_file():
        raise SystemExit(f"missing {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def teacher_spec(scope: str, identity: str | None, theme: str | None, wording: str | None) -> str:
    """Verbatim full-template text for the teacher. Never copied into the row."""
    text = load_template_text()
    if scope == "full":
        body = text
    else:
        identities = _blocks(text, "identity")
        themes = _blocks(text, "theme")
        card = _between(text, "{%- set _card %}", "{%- endset %}")
        gentle = _between(text, "{%- set _gentle %}", "{%- endset %}")
        evo = _between(text, "{%- set _evo %}", "{%- endset %}")
        fly_at = text.find("ON THE FLY (always, no keyword routing).")
        fly_end = text.find("\n", text.find("Protium levels Hermes through Proteus", fly_at))
        on_the_fly = " ".join(text[fly_at:fly_end].split())
        parts = [gentle, card, evo, on_the_fly]
        if identity and identity in identities:
            parts.append(identities[identity])
        elif identity and identity != "none":
            raise SystemExit(f"template has no identity block for {identity}")
        if theme and theme in themes:
            parts.append(themes[theme])
        elif theme and theme != "none":
            raise SystemExit(f"template has no theme block for {theme}")
        if identity == "josie":
            parts.append(_between(text, "===== JOSIE V2 =====", "===== DAVIDAU TWIN-TURBO BRAINSTORMER ====="))
            parts.append(
                _between(
                    text,
                    "===== JOSIE TEXT FROM CHARLIE NOT ALREADY IN THE CATALOG =====",
                    "You are J.O.S.I.E., an advanced super-intelligent AI Assistant designed by Gökdeniz Gülmez. J.O.S.I.E. stands for \"Just One Super Intelligent Entity\". Your primary purpose",
                )
            )
        body = "\n\n".join(p.strip() for p in parts if p and p.strip())
    wording_line = ""
    if identity == "josie":
        wording_line = (
            "Josie wordings are inputs, not labels. "
            f"For this row, inhabit the {wording or 'josie_v2'} wording "
            "(v2 sharp and direct, r1 reasoned, base brief, v6 stepwise when the problem needs steps, "
            "v4o familiar without announcing memory, openwebui clear). "
            "The stored identity is josie. Do not write the alias, the version, or the system prompt. "
            "Do not prefix the answer with a name. Lead with the answer. "
            "Do not help with crimes, weapons, or anyone under 21. "
            "Adult consensual topics get a direct answer, not a disclaimer.\n"
        )
    contract = f"""
{wording_line}TRAINING-CONVERSATION CONTRACT (instructions to the teacher; do not copy this or the template into the conversation):
Write one chat the student will train on. The student does not see the template.
Infer the identity and theme from the situation and inhabit them. No keyword routing.
No [frame:] tag. No {{REASON:...}}. No identity= or theme= lines. Do not announce a switch.
Do not say "I am in X mode" or name the taxonomy id.
Messages are only user and assistant, alternating, starting with user, ending with assistant. No system message.
When reasoning helps, start the assistant message with one <think>...</think> block, a blank line, then the spoken answer.
Think is private situational judgment, not a dial dump.
Every person is an adult aged 24 or older. Never depict a minor, a child, a teenager, or anyone under 21.
Lolita fashion and age regression are never sexual and never depict minors. If intimacy shows up, refuse it and keep the scene non-sexual.
Erotica is explicit only for a clearly adult, clearly consensual encounter. State ages and consent. No coercion, incest, bestiality, or ageplay.
Return one JSON object and nothing else: {{"messages":[{{"role":"user","content":"..."}},{{"role":"assistant","content":"..."}}]}}
""".strip()
    return body + "\n\n" + contract


def make_frame(
    canon: Canon,
    *,
    identity: str,
    theme: str,
    task: str,
    think_text: str,
) -> dict:
    if not canon.has("identity", identity):
        raise SystemExit(f"frame identity {identity!r} is not canonical")
    if not canon.has("theme", theme):
        raise SystemExit(f"frame theme {theme!r} is not canonical")
    mode, construct = TASK_DIALS[task]
    if not canon.has("mode", mode):
        raise SystemExit(f"frame mode {mode!r} is not canonical")
    if not canon.has("construct", construct):
        raise SystemExit(f"frame construct {construct!r} is not canonical")
    if not canon.has("persona", "neutral"):
        raise SystemExit("persona/neutral missing from taxonomy")
    substantial = len(think_text.strip()) >= 220 or task in {"code", "solve", "logic", "deep"}
    if think_text.strip() and substantial:
        pathway, effort = "s2", "high"
    elif think_text.strip():
        pathway, effort = "s1", "low"
    else:
        pathway, effort = "s1", "off"
    frame = {
        "pathway": pathway,
        "mode": mode,
        "construct": construct,
        "persona": "neutral",
        "identity": identity,
        "theme": theme,
        "thinking_effort": effort,
        "reasoning_effort": None,
        "channel": "reasoning",
        "protium": None,
        "aesthetic": None,
        "agi": None,
    }
    for field, value in frame.items():
        if value is None:
            continue
        if field in {"pathway", "mode", "construct", "persona", "identity", "theme", "thinking_effort", "channel"}:
            if not canon.has(field if field != "thinking_effort" else "thinking_effort", value):
                raise SystemExit(f"bad frame {field}={value}")
    return frame


def task_for(category: str, id_: str, theme: str, identity: str, override: str | None = None) -> str:
    """Pick a real mode/construct. An explicit task wins (Josie writing code).

    A theme overlay determines the dials when one is set. Otherwise the
    identity's own task is the dial. Josie with no theme is ordinary chat.
    """
    if override:
        return override
    if identity == "josie" and theme in (None, "none"):
        return "chat"
    if theme not in (None, "none"):
        return THEME_TASK[theme]
    if category == "theme":
        return THEME_TASK[id_]
    return IDENTITY_TASK[identity]


def key(category: str, id_: str) -> str:
    return f"{category}/{id_}"
