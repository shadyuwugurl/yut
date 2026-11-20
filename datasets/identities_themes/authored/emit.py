#!/usr/bin/env python3
"""Schema wrapper for hand-authored rows. It does not invent dialogue."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from canonical import load_canon, make_frame, task_for  # noqa: E402
from safety import check_record  # noqa: E402

CANON = load_canon()
AUTHORED = HERE


def _think_text(messages: list[dict]) -> str:
    parts = []
    for msg in messages:
        if msg["role"] == "assistant" and "<think>" in msg["content"]:
            end = msg["content"].find("</think>")
            parts.append(msg["content"][len("<think>"):end])
    return "\n".join(parts)


def row(
    *,
    category: str,
    id_: str,
    messages: list[tuple[str, str]],
    shape: str,
    theme: str = "none",
    identity: str | None = None,
    switch_from: str | None = None,
    switch_to: str | None = None,
    input_alias: str | None = None,
    task: str | None = None,
) -> dict:
    if category == "identity":
        identity = id_
    elif identity is None:
        identity = "none"
    if category == "theme":
        theme = id_
    packed = [{"role": role, "content": text.strip()} for role, text in messages]
    think = _think_text(packed)
    task_name = task or task_for(category, id_, theme, identity)
    frame = make_frame(CANON, identity=identity, theme=theme, task=task_name, think_text=think)
    has_think = any("<think>" in m["content"] for m in packed if m["role"] == "assistant")
    if has_think and frame["thinking_effort"] == "off":
        frame["thinking_effort"] = "low"
        frame["pathway"] = "s1"
    if not has_think:
        frame["thinking_effort"] = "off"
        frame["pathway"] = "s1"
    record = {
        "messages": packed,
        "meta": {
            "taxonomy": "skinny-v1",
            "category": category,
            "id": id_,
            "key": f"{category}/{id_}",
            "identity": identity,
            "theme": theme,
            "labels": [f"identity/{identity}", f"theme/{theme}"],
            "switch": shape == "shift",
            "switch_from": None if shape != "shift" else {"category": "theme", "id": switch_from, "key": f"theme/{switch_from}"},
            "switch_to": None if shape != "shift" else {"category": "theme", "id": switch_to, "key": f"theme/{switch_to}"},
            "shape": shape,
            "source": "authored",
            "think": has_think,
            "input_alias": input_alias,
            "frame": frame,
        },
    }
    reason = check_record(record, CANON)
    if reason:
        preview = packed[0]["content"][:80].replace("\n", " ")
        raise SystemExit(f"{category}/{id_} {shape} rejected ({reason}): {preview}")
    return record


def write_rows(id_: str, rows: list[dict], append: bool = False) -> Path:
    path = AUTHORED / f"{id_}.jsonl"
    mode = "a" if append else "w"
    with path.open(mode, encoding="utf-8") as fh:
        for record in rows:
            if record["meta"]["id"] != id_:
                raise SystemExit(f"row id {record['meta']['id']} != file {id_}")
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path
