#!/usr/bin/env python3
"""OpenAI-compatible teacher. The system prompt is template text.

The completion is parsed as a conversation and returned without that prompt.
Labels are applied by the caller from the skinny taxonomy, not by the model.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

from canonical import teacher_spec


class TeacherError(RuntimeError):
    pass


class OpenAITeacher:
    def __init__(self, base: str, key: str, model: str, timeout: int = 120):
        if not base or not key or not model:
            raise TeacherError("OPENAI_BASE_URL, OPENAI_API_KEY, and MODEL are required")
        self.base = base.rstrip("/")
        self.key = key
        self.model = model
        self.timeout = timeout

    @classmethod
    def from_env(cls) -> "OpenAITeacher":
        return cls(
            os.environ.get("OPENAI_BASE_URL", ""),
            os.environ.get("OPENAI_API_KEY", ""),
            os.environ.get("MODEL", ""),
        )

    def complete(self, system: str, user: str) -> str:
        url = self.base + "/chat/completions"
        payload = {
            "model": self.model,
            "temperature": 0.9,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        last = "no attempt"
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                return body["choices"][0]["message"]["content"]
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", "replace")[:500]
                last = f"HTTP {exc.code}: {detail}"
                if exc.code not in {408, 409, 429, 500, 502, 503, 504}:
                    raise TeacherError(last) from exc
            except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError) as exc:
                last = str(exc)
            time.sleep(2 ** attempt)
        raise TeacherError(last)


def parse_messages(text: str) -> list[dict]:
    raw = text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        if raw.endswith("```"):
            raw = raw[: raw.rfind("```")]
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end < start:
        raise TeacherError("teacher did not return JSON")
    data = json.loads(raw[start : end + 1])
    messages = data.get("messages")
    if not isinstance(messages, list):
        raise TeacherError("teacher JSON has no messages")
    clean = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")
        if role not in {"user", "assistant"} or not isinstance(content, str):
            raise TeacherError("teacher message roles must be user or assistant")
        clean.append({"role": role, "content": content.strip()})
    return clean


def brief_for(record_plan: dict) -> str:
    """Tell the teacher the situation. The canonical id is not a line to copy."""
    lines = [
        "Write the conversation described here.",
        f"Shape: {record_plan['shape']}.",
        f"Canonical identity (do not print this id): {record_plan['identity']}.",
        f"Canonical theme (do not print this id): {record_plan['theme']}.",
        record_plan["direction"],
    ]
    if record_plan.get("input_alias"):
        lines.append(
            f"Josie wording input (do not print this alias): {record_plan['input_alias']}."
        )
    if record_plan["shape"] == "shift":
        lines.append(
            "Start in theme "
            f"{record_plan['switch_from']} and change, without announcing it, to theme "
            f"{record_plan['switch_to']} when the user changes the situation."
        )
    lines.append("JSON only.")
    return "\n".join(lines)


def system_for(record_plan: dict, scope: str) -> str:
    identity = record_plan["identity"]
    theme = record_plan["theme"]
    return teacher_spec(
        scope,
        None if identity == "none" else identity,
        None if theme == "none" else theme,
        record_plan.get("input_alias"),
    )
