"""Skinny-v1 labels for constructs and personas.

The stable key is category + id from docs/taxonomy_skinny.json (branch
cursor/spark-skinny-template-3cef). Aliases are accepted inputs. They are
never stored as meta.id.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLICE = ROOT / "taxonomy_slice.json"

# Three-part fusions the skinny spec names explicitly. Two-part ids are parsed.
AGI_TRIPLES = {
    frozenset(("pkd", "vader", "comedy")): "agi-pkd-vader-comedy",
    frozenset(("stark", "musk", "coder")): "agi-stark-musk-coder",
    frozenset(("stark", "musk", "curie")): "agi-stark-musk-curie",
}


@lru_cache(maxsize=1)
def load():
    data = json.loads(SLICE.read_text())
    items = data["items"]
    by_key = {(it["category"], it["id"]): it for it in items}
    alias = {}
    for it in items:
        for raw in it.get("aliases") or []:
            alias.setdefault(raw.lower(), []).append((it["category"], it["id"]))
    agi = {}
    for entry in data.get("agi") or []:
        parts = entry["id"].split("-")[1:]
        agi[frozenset(parts)] = entry["id"]
    agi.update(AGI_TRIPLES)
    return {
        "taxonomy": data["taxonomy"],
        "items": items,
        "by_key": by_key,
        "alias": alias,
        "agi": agi,
    }


def items(category=None):
    rows = load()["items"]
    if category:
        rows = [it for it in rows if it["category"] == category]
    return rows


def resolve(name, category=None):
    """Map a canonical id or an alias to (category, id, alias_input).

    alias_input is None when `name` was already the canonical id.
    """
    data = load()
    raw = name.strip()
    if "/" in raw:
        cat, _, ident = raw.partition("/")
        return resolve(ident, category=cat)
    key = raw.lower()
    if category:
        it = data["by_key"].get((category, key))
        if it:
            return category, it["id"], None
        hits = [pair for pair in data["alias"].get(key, []) if pair[0] == category]
        if len(hits) == 1:
            return hits[0][0], hits[0][1], raw
        raise SystemExit(f"unknown {category} id or alias: {name}")
    id_hits = [it for it in data["items"] if it["id"] == key]
    if len(id_hits) == 1:
        return id_hits[0]["category"], id_hits[0]["id"], None
    if len(id_hits) > 1:
        raise SystemExit(f"{name} is an id in more than one category; pass category/id")
    hits = data["alias"].get(key, [])
    if len(hits) == 1:
        return hits[0][0], hits[0][1], raw
    if len(hits) > 1:
        raise SystemExit(f"alias {name} maps to {hits}; pass category/id")
    raise SystemExit(f"unknown construct/persona id or alias: {name}")


def agi_for(ids):
    """Return the skinny agi id when this blend is one of the named fusions."""
    key = frozenset(ids)
    return load()["agi"].get(key)
