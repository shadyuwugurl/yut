"""OpenAI-compatible teacher backend.

Environment:
  OPENAI_BASE_URL   e.g. https://host/v1  or https://host
  OPENAI_API_KEY
  MODEL

The teacher sees the full-template card. The saved row does not.
"""
from __future__ import annotations

import json
import os
import random
import urllib.error
import urllib.request

from .cards import teacher_card, teacher_system
from .filters import check_example, example_fingerprint
from .procedural import _frame

PATTERNS = ("single", "multi", "switch", "blend", "stay")


def _endpoint() -> tuple[str, str, str]:
    base = os.environ.get("OPENAI_BASE_URL", "").rstrip("/")
    key = os.environ.get("OPENAI_API_KEY", "")
    model = os.environ.get("MODEL", "")
    if not base or not key or not model:
        raise SystemExit("LLM backend needs OPENAI_BASE_URL, OPENAI_API_KEY, and MODEL")
    if base.endswith("/chat/completions"):
        url = base
    elif base.endswith("/v1"):
        url = base + "/chat/completions"
    else:
        url = base + "/v1/chat/completions"
    return url, key, model


def _chat(system: str, user: str, temperature: float) -> str:
    url, key, model = _endpoint()
    payload = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"teacher HTTP {exc.code}: {detail}") from exc
    return data["choices"][0]["message"]["content"]


def _parse_messages(raw: str) -> list[dict] | None:
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        text = text.rsplit("```", 1)[0]
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            return None
        try:
            obj = json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            return None
    messages = obj.get("messages") if isinstance(obj, dict) else None
    if not isinstance(messages, list):
        return None
    cleaned = []
    for msg in messages:
        if not isinstance(msg, dict):
            return None
        role = msg.get("role")
        content = msg.get("content")
        if role == "system":
            # The teacher must not smuggle the card back in.
            continue
        if role not in {"user", "assistant"} or not isinstance(content, str):
            return None
        cleaned.append({"role": role, "content": content.strip()})
    return cleaned


def generate_llm_one(spec: dict, pattern: str, *, variant: int, alias_input,
                     partner: dict | None = None, temperature: float = 0.9):
    system = teacher_system(spec["category"], spec["id"], pattern)
    note = ""
    extra_ids: list[str] = []
    switch = None
    blend = None
    if pattern == "switch":
        if partner is None:
            return None
        note = (
            "\n\nStart the conversation in this OTHER behavior. "
            "Do not name it. On the second user turn the situation changes "
            "into the target card, and the assistant inhabits the target from "
            "that turn on, again without naming it.\n\n"
            + teacher_card(partner["category"], partner["id"])
        )
        switch = {
            "from": partner["id"],
            "to": spec["id"],
            "from_category": partner["category"],
            "to_category": spec["category"],
            "at_user_turn": 1,
        }
    elif pattern == "blend":
        if partner is None:
            return None
        note = (
            "\n\nBlend the target card with this second behavior into ONE voice. "
            "Do not list the ingredients or name either label.\n\n"
            + teacher_card(partner["category"], partner["id"])
        )
        extra_ids = [partner["id"]]
        blend = [spec["id"], partner["id"]]
    raw = _chat(system + note, (
        f"Write pattern={pattern}. Vary the concrete details. "
        "The user text implies the behavior by the situation alone. Adults only."
    ), temperature)
    messages = _parse_messages(raw)
    if not messages:
        return None
    frame = _frame(spec, extra_ids)
    think_flag = any(
        m["role"] == "assistant" and m["content"].startswith("<think>")
        for m in messages
    )
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
            "source": "llm",
            "nsfw": bool(spec["nsfw"] or (partner or {}).get("nsfw")),
            "taxonomy": "skinny-v1",
        },
    }
    problems = check_example(ex)
    if problems:
        return None
    digest = example_fingerprint(ex)
    ex["meta"]["uid"] = f"cp-{spec['category']}-{spec['id']}-{pattern}-{digest[:12]}"
    return ex


def pattern_for(rng: random.Random) -> str:
    return rng.choices(PATTERNS, weights=[0.34, 0.24, 0.18, 0.14, 0.10], k=1)[0]
