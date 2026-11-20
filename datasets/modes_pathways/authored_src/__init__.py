"""Hand-authored rows. Each entry is a finished task, not a template."""
from __future__ import annotations


def load_banks() -> dict[str, list[dict]]:
    from authored_src import bank_s1, bank_s2, bank_meta, bank_effort, bank_protium, bank_rest, bank_agi

    out: dict[str, list[dict]] = {}
    for mod in (bank_s1, bank_s2, bank_meta, bank_effort, bank_protium, bank_rest, bank_agi):
        for key, rows in mod.rows().items():
            out.setdefault(key, []).extend(rows)
    return out
