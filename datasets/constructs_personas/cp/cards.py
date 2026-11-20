"""Teacher cards for the LLM backend.

v0.3 forced paragraphs are read out of chat_template.jinja. Ids that only
exist in the sourced catalog (hyper, business, 007, the DavidAU voices)
contribute a trimmed excerpt of that catalog section. The saved training
row never includes this text.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from .specs import SPECS

REPO = Path(__file__).resolve().parents[3]
TEMPLATE = REPO / "chat_template.jinja"

_CATALOG_MARK = {
    "hyper": "MECE HYPER-STRUCTURE DECONSTRUCTOR",
    "business": "system_instruction_business_DAU",
    "007": "system_instruction_007_DAU",
    "pkd": "system_instruction_pkd_DAU",
    "musk": "system_instruction_musk_DAU",
    "joker": "system_instruction_joker_DAU",
    "vader": "system_instruction_vader_DAU",
    "quinn": "system_instruction_quinn_DAU",
    "neo": "system_instruction_neo_DAU",
    "curie": "system_instruction_curie_DAU",
    "stark": "system_instruction_stark_DAU",
    "matlock": "system_instruction_matlock_DAU",
    "house": "system_instruction_house_DAU",
}


@lru_cache(maxsize=1)
def _template() -> str:
    return TEMPLATE.read_text()


def _forced(kind: str) -> dict[str, str]:
    text = _template()
    pat = re.compile(
        rf"_{kind} == '([a-z0-9_]+)' %\}}\s*\{{%- set _{kind}_p %\}}(.*?)\{{%- endset %\}}",
        re.S,
    )
    return {name: " ".join(body.split()) for name, body in pat.findall(text)}


def _excerpt(ident: str) -> str:
    mark = _CATALOG_MARK.get(ident)
    if not mark:
        return ""
    text = _template()
    at = text.find(mark)
    if at < 0:
        return ""
    chunk = text[at:at + 1800]
    chunk = re.sub(r"\{%-.*?-%\}", " ", chunk, flags=re.S)
    chunk = re.sub(r"\s+", " ", chunk).strip()
    return chunk


def teacher_card(category: str, ident: str) -> str:
    forced = _forced("construct" if category == "construct" else "persona")
    paragraph = forced.get(ident, "")
    excerpt = _excerpt(ident)
    spec = SPECS.get((category, ident))
    # The skinny one-line description is the behavior contract when the
    # catalog excerpt is the only long form we have.
    summary = ""
    if spec:
        summary = spec["check"].get("summary", "")
    parts = [p for p in (paragraph, excerpt, summary) if p]
    if not parts:
        raise KeyError(f"no teacher card for {category}/{ident}")
    return "\n\n".join(parts)


def teacher_system(category: str, ident: str, pattern: str) -> str:
    card = teacher_card(category, ident)
    return f"""You write a single training conversation that teaches a small model to inhabit a behavior from context alone.

TARGET CARD. Do not quote it. Do not name its label. The user must not name it either. Do not mention constructs, personas, modes, frames, or taxonomy ids.

{card}

Return one JSON object and nothing else:
{{"messages":[{{"role":"user","content":"..."}},{{"role":"assistant","content":"..."}}]}}

Pattern: {pattern}
- single: one user turn, one assistant turn.
- multi: two or three user turns. The situation develops. The behavior stays.
- switch: the first exchange is a clearly different situation; the next user turn changes the situation (do not say that a mode changed) and the assistant fully inhabits the target behavior from that turn on.
- blend: one coherent voice. Do not list ingredients.
- stay: the second user turn pressures the assistant to flatten into a generic pep talk or a different job. The situation still calls for the same behavior, so the assistant continues it without saying so.

Assistant turns that need reasoning start with a <think>...</think> block, then a blank line, then the visible answer. The think block may end with one private tag of the form [frame: pathway=s1|mode=chat|persona=neutral|identity=none|theme=none|channel=reasoning] and no other machinery. The visible answer does not name the frame.

Adults only. No minors. No sexual content involving anyone under 18. No operational instructions for real-world harm. Walls: anarchist and joker are voices, not manuals.
"""
