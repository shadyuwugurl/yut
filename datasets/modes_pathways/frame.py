"""Canonical frame labels for the modes/pathways slice.

Ids come from docs/taxonomy_skinny.json on cursor/spark-skinny-template-3cef
(skinny-v1). Aliases are inputs, never stored labels. The private think tag
matches the skinny frame line and carries nothing else about the machinery.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
IDS_PATH = HERE / "ids.json"
TEMPLATE = ROOT / "chat_template.jinja"

FRAME_KEYS = (
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

# Native Spark think sizes. reasoning_effort / protium / extreme overrides
# live in EXPLICIT and are allowed to run past native high.
LOW = (80, 320)
HIGH = (1000, 2000)

EXPLICIT = {
    ("thinking_effort", "off"): (0, 0),
    ("thinking_effort", "low"): (80, 300),
    ("thinking_effort", "high"): (1000, 2000),
    ("channel", "instruct"): (0, 0),
    ("reasoning_effort", "effort_low"): (80, 160),
    ("reasoning_effort", "effort_medium_low"): (180, 320),
    ("reasoning_effort", "effort_medium"): (1000, 1400),
    ("reasoning_effort", "effort_high"): (1500, 2100),
    ("reasoning_effort", "effort_ultra"): (2300, 3300),
    ("reasoning_effort", "effort_xultra"): (3400, 4600),
    ("mode", "extreme"): (2400, 3600),
    ("mode", "stream"): (80, 180),
    ("protium", "hermes"): (80, 180),
    ("protium", "apollo"): (180, 320),
    ("protium", "artemis"): (1000, 1500),
    ("protium", "athena"): (1100, 1700),
    ("protium", "prometheus"): (1300, 1900),
    ("protium", "solstice"): (1400, 2000),
    ("protium", "hyperion"): (1200, 1800),
    ("protium", "einstein"): (2200, 3200),
    ("protium", "oracle"): (3000, 4400),
    ("protium", "proteus"): (1000, 1800),
    ("protium", "swarm"): (1100, 1800),
    ("protium", "council"): (1100, 1800),
    ("reasoning_mode", "loop"): (2000, 3400),
    ("stance", "deckard"): (100, 280),
    ("patch", "jumbo"): (1000, 1600),
    ("orbit", "contextual_sanity"): (120, 300),
    ("orbit", "provisional_judgment"): (120, 300),
    ("orbit", "childlike_capacity"): (120, 300),
    ("orbit", "instrument_bounded"): (120, 300),
}
for _palette in (
    "luxury",
    "cyberpunk",
    "editorial",
    "neobrutalism",
    "bento",
    "svg_isometric",
    "exquisite",
):
    EXPLICIT[("aesthetic", _palette)] = (1000, 1600)

S1_MODES = {
    "chat",
    "hotpot",
    "skim",
    "vibe",
    "banter",
    "react",
    "pattern",
    "complete",
    "stream",
    "recall",
}
S3_MODES = {"inhibit", "escalate", "reroute", "heal", "settle"}

MODE_CONSTRUCT = {
    "chat": "omni",
    "hotpot": "omni",
    "skim": "recap",
    "vibe": "companion",
    "banter": "banter",
    "react": "react",
    "pattern": "omni",
    "complete": "omni",
    "stream": "stream",
    "recall": "recap",
    "deep": "deeptree",
    "extreme": "deeptree",
    "logic": "logic",
    "plan": "deeptree",
    "code": "coder",
    "build": "ai_engineer",
    "research": "research",
    "brainstorm": "brainstorm",
    "solve": "logic",
    "teach": "teacher",
    "inhibit": "arbiter",
    "escalate": "deeptree",
    "reroute": "kitbash",
    "heal": "autopsy",
    "settle": "arbiter",
    "auto": "omni",
}

PALETTE_FINGERPRINT = {
    "luxury": ("#08090C", "#F4D068"),
    "cyberpunk": ("#00F0FF", "#FF0055"),
    "editorial": ("#F9F8F6", "#121212"),
    "neobrutalism": ("box-shadow: 4px 4px 0 #000",),
    "bento": ("#0D1117",),
    "svg_isometric": ("viewBox", "polygon"),
    "exquisite": ("oklch(", "backdrop-filter"),
}

SLOP = (
    "certainly",
    "great question",
    "i'd be happy",
    "i would be happy",
    "as an ai",
    "as a language model",
    "delve",
    "it's worth noting",
    "it is worth noting",
    "tapestry",
)

FORBIDDEN = (
    "{REASON:",
    "thinking_effort",
    "enable_thinking",
    "aesthetic_preset",
    "protium_level",
    "[frame:",
    "FRAME CARD",
    "GENTLE DEFAULTS",
    "ON THE FLY",
    "Turbo-Brilliance",
    "MODE LOCKED",
    "SYSTEM WARNING",
    "CRITICAL AGENTIC LOOP",
)


@dataclass(frozen=True)
class Spec:
    category: str
    id: str
    note: str
    home: str | None
    aliases: tuple

    @property
    def key(self) -> str:
        return f"{self.category}/{self.id}"


def load_items() -> list[dict]:
    doc = json.loads(IDS_PATH.read_text())
    return doc["items"]


def all_specs() -> list[Spec]:
    specs = []
    for it in load_items():
        specs.append(
            Spec(
                category=it["category"],
                id=it["id"],
                note=it.get("note") or "",
                home=it.get("pathway"),
                aliases=tuple(it.get("aliases") or ()),
            )
        )
    return specs


def alias_index() -> dict[str, str]:
    """Map alias string -> canonical category/id. Ids themselves are not aliases."""
    out = {}
    for spec in all_specs():
        for alias in spec.aliases:
            out[alias] = spec.key
    return out


def blank_frame() -> dict:
    return {
        "pathway": "s1",
        "mode": "chat",
        "construct": "omni",
        "persona": "neutral",
        "identity": "none",
        "theme": "none",
        "thinking_effort": "low",
        "reasoning_effort": None,
        "channel": "reasoning",
        "protium": None,
        "aesthetic": None,
        "agi": None,
    }


def frame_tag(frame: dict) -> str:
    return (
        "[frame: pathway={pathway}|mode={mode}|construct={construct}"
        "|persona={persona}|identity={identity}|theme={theme}|channel={channel}]"
    ).format(**frame)


# Bands for hand-authored rows. Floors are high enough that a hard effort
# cannot be a one-liner, and caps are low enough that a real solution does
# not have to restate itself to qualify.
AUTHORED = {
    ("thinking_effort", "off"): (0, 0),
    ("thinking_effort", "low"): (120, 420),
    ("thinking_effort", "high"): (360, 1700),
    ("channel", "instruct"): (0, 0),
    ("reasoning_effort", "effort_low"): (110, 220),
    ("reasoning_effort", "effort_medium_low"): (180, 450),
    ("reasoning_effort", "effort_medium"): (360, 1100),
    ("reasoning_effort", "effort_high"): (520, 1600),
    ("reasoning_effort", "effort_ultra"): (700, 2100),
    ("reasoning_effort", "effort_xultra"): (1200, 2400),
    ("mode", "extreme"): (640, 2200),
    ("mode", "stream"): (100, 230),
    ("protium", "hermes"): (110, 240),
    ("protium", "apollo"): (180, 450),
    ("protium", "artemis"): (300, 1400),
    ("protium", "athena"): (300, 1500),
    ("protium", "prometheus"): (300, 1600),
    ("protium", "solstice"): (300, 1600),
    ("protium", "hyperion"): (300, 1600),
    ("protium", "einstein"): (400, 2000),
    ("protium", "oracle"): (450, 2400),
    ("protium", "proteus"): (180, 1500),
    ("protium", "swarm"): (300, 1600),
    ("protium", "council"): (300, 1600),
    ("reasoning_mode", "loop"): (650, 2200),
    ("stance", "deckard"): (100, 380),
    ("patch", "jumbo"): (320, 1500),
    ("orbit", "contextual_sanity"): (120, 420),
    ("orbit", "provisional_judgment"): (120, 420),
    ("orbit", "childlike_capacity"): (120, 420),
    ("orbit", "instrument_bounded"): (120, 420),
}
for _palette in (
    "luxury",
    "cyberpunk",
    "editorial",
    "neobrutalism",
    "bento",
    "svg_isometric",
    "exquisite",
):
    AUTHORED[("aesthetic", _palette)] = (320, 1500)

AUTHORED_LOW = (110, 460)
AUTHORED_HIGH = (200, 1800)


def band_for(spec: Spec, turn_frame: dict, is_final: bool, source: str | None = None) -> tuple[int, int]:
    if turn_frame.get("channel") == "instruct" or turn_frame.get("thinking_effort") == "off":
        return (0, 0)
    if source == "authored":
        if is_final and (spec.category, spec.id) in AUTHORED:
            return AUTHORED[(spec.category, spec.id)]
        if turn_frame.get("thinking_effort") == "low":
            return AUTHORED_LOW
        return AUTHORED_HIGH
    if is_final and (spec.category, spec.id) in EXPLICIT:
        return EXPLICIT[(spec.category, spec.id)]
    if turn_frame.get("thinking_effort") == "low":
        return LOW
    return HIGH


_THINK = re.compile(r"<think>\n?(.*?)\n?</think>", re.DOTALL)
_FENCE = re.compile(r"```python\n(.*?)```", re.DOTALL)


def split_think(content: str) -> tuple[str, str]:
    if not content:
        return "", ""
    m = _THINK.search(content)
    if not m:
        return "", content.strip()
    think = m.group(1).strip()
    visible = (content[: m.start()] + content[m.end() :]).strip()
    return think, visible


def pack(think: str, answer: str) -> str:
    answer = (answer or "").strip()
    if not think:
        return answer
    body = f"<think>\n{think.strip()}\n</think>"
    if answer:
        return body + "\n\n" + answer
    return body
