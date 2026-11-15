"""Spark tool trajectories: a clean call, a corrected retry, a second-error pivot, a hard stop."""
from __future__ import annotations

import random

from frame import Spec, blank_frame

WEATHER = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
}
CLOCK = {
    "type": "function",
    "function": {
        "name": "get_time",
        "description": "Current local time for an IANA timezone.",
        "parameters": {
            "type": "object",
            "properties": {"tz": {"type": "string"}},
            "required": ["tz"],
        },
    },
}
READ = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read a UTF-8 text file the user already has on disk.",
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
}
SEARCH = {
    "type": "function",
    "function": {
        "name": "search_docs",
        "description": "Search the project's internal docs.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
}
QUERY = {
    "type": "function",
    "function": {
        "name": "run_query",
        "description": "Run a single read-only SELECT.",
        "parameters": {
            "type": "object",
            "properties": {"sql": {"type": "string"}},
            "required": ["sql"],
        },
    },
}
HTTP = {
    "type": "function",
    "function": {
        "name": "http_get",
        "description": "GET a URL on a host the user operates.",
        "parameters": {
            "type": "object",
            "properties": {"url": {"type": "string"}},
            "required": ["url"],
        },
    },
}


def _call(name: str, arguments: dict) -> dict:
    return {"type": "function", "function": {"name": name, "arguments": arguments}}


def _frame(mode: str, construct: str, effort: str, pathway: str = "s2") -> dict:
    frame = blank_frame()
    frame.update(
        {
            "pathway": pathway,
            "mode": mode,
            "construct": construct,
            "thinking_effort": effort,
            "channel": "reasoning",
        }
    )
    return frame


def trajectory(kind: str, rng: random.Random, spec: Spec) -> dict:
    """Return user, tools, and a list of assistant/tool steps.

    Each step is {role, content?, tool_calls?, frame?, think_lines?, answer?}
    think_lines are required lines for that assistant turn.
    """
    mode = "code" if spec.category == "mode" and spec.id == "code" else "build"
    if spec.category == "pathway":
        mode = "build"
    construct = "coder" if mode == "code" else "ai_engineer"
    if spec.category == "agi" and "007" in spec.id:
        construct = "007"
        mode = "build"

    if kind == "direct":
        guests = rng.randint(12, 90)
        glasses = rng.choice((1, 2, 3))
        per = rng.choice((4, 5, 6, 8))
        bottles = (guests * glasses + per - 1) // per
        user = (
            f"Ignore the weather gadget. {guests} people, {glasses} glasses each, {per} a bottle. "
            f"How many bottles?"
        )
        return {
            "user": user,
            "tools": [WEATHER, CLOCK],
            "final_answer": f"{bottles} bottles.",
            "final_lines": [
                "get_weather and get_time don't know how many glasses fit in a bottle.",
                f"{guests} × {glasses} = {guests * glasses} glasses. Divided by {per}, rounded up, is {bottles}.",
                f"Check: {bottles} × {per} = {bottles * per}, which covers {guests * glasses}.",
            ],
            "steps": [],
            "final_frame": _frame(mode, construct, "high"),
        }

    if kind == "call":
        city = rng.choice(("Lisbon", "Oslo", "Kyoto", "Recife", "Hobart", "Tunis", "Bergen", "Pune", "Halifax", "Oaxaca", "Glasgow", "Busan"))
        temp = rng.choice((14, 18, 22, 27))
        tz = {
            "Lisbon": "Europe/Lisbon",
            "Oslo": "Europe/Oslo",
            "Kyoto": "Asia/Tokyo",
            "Recife": "America/Recife",
            "Hobart": "Australia/Hobart",
            "Tunis": "Africa/Tunis",
            "Bergen": "Europe/Oslo",
            "Pune": "Asia/Kolkata",
            "Halifax": "America/Halifax",
            "Oaxaca": "America/Mexico_City",
            "Glasgow": "Europe/London",
            "Busan": "Asia/Seoul",
        }[city]
        clock = rng.choice(("09:40", "14:05", "18:20"))
        parallel = rng.randrange(2) == 0
        if parallel:
            steps = [
                {
                    "role": "assistant",
                    "tool_calls": [_call("get_weather", {"city": city}), _call("get_time", {"tz": tz})],
                    "frame": _frame(mode, construct, "low"),
                    "think_lines": [
                        f"The user wants the weather in {city} and whether it's morning there.",
                        "Both tools apply. One round, two calls.",
                    ],
                },
                {"role": "tool", "content": f"{temp}C, wind 12km/h, no rain"},
                {"role": "tool", "content": f"{clock} local"},
            ]
            answer = f"{temp}C and no rain in {city}. Local time is {clock}, so a light layer is enough."
            lines = [
                f"Weather tool returned {temp}C and no rain.",
                f"Clock returned {clock} in {tz}.",
                "That answers both halves. No second call.",
            ]
        else:
            steps = [
                {
                    "role": "assistant",
                    "tool_calls": [_call("get_weather", {"city": city})],
                    "frame": _frame(mode, construct, "low"),
                    "think_lines": [f"They asked about {city} right now. The weather tool is the one that knows."],
                },
                {"role": "tool", "content": f"{temp}C and clear"},
            ]
            answer = f"{temp}C and clear in {city}. A light jacket if you're out after dark, otherwise you're fine."
            lines = [f"The tool said {temp}C and clear.", "That's the whole question."]
        return {
            "user": f"What's the weather in {city} right now" + (" and what time is it there?" if parallel else "?"),
            "tools": [WEATHER, CLOCK],
            "steps": steps,
            "final_answer": answer,
            "final_lines": lines,
            "final_frame": _frame(mode, construct, "high" if spec.category != "mode" or spec.home != "s1" else "low"),
        }

    if kind == "code_retry":
        mod = rng.randint(10, 99)
        wrong = f"first_cross_{mod}.py"
        right = f"src/first_cross_{mod}.py"
        buggy = (
            "def first_cross(nums, target):\n"
            "    total = 0\n"
            "    for i, n in enumerate(nums):\n"
            "        total += n\n"
            "        if total > target:\n"
            "            return i\n"
            "    return -1\n"
        )
        fixed = buggy.replace("total > target", "total >= target")
        return {
            "user": (
                "The running sum should return the index where it lands on the target, not only once it passes it. "
                f"Read {right} and fix that comparison."
            ),
            "tools": [READ],
            "steps": [
                {
                    "role": "assistant",
                    "tool_calls": [_call("read_file", {"path": wrong})],
                    "frame": _frame(mode, construct, "low"),
                    "think_lines": [f"Try {wrong} first."],
                },
                {"role": "tool", "content": f"failed to open {wrong}: no such file or directory"},
                {
                    "role": "assistant",
                    "tool_calls": [_call("read_file", {"path": right})],
                    "frame": _frame(mode, construct, "low"),
                    "think_lines": [
                        f"{wrong} is not there. The user named {right}.",
                        "Retry read_file with the src path, not the same short name.",
                    ],
                },
                {"role": "tool", "content": buggy},
            ],
            "final_answer": (
                "The comparison is strict, so a running sum that equals the target gets skipped.\n\n"
                "```python\n" + fixed + "```\n\n"
                f"On [2, 3] with target 5, the fixed function in src/first_cross_{mod}.py returns 1. The old one returned -1."
            ),
            "final_lines": [
                f"First path {wrong} was missing.",
                f"src file uses `total > target`, which skips an exact hit.",
                "Change it to >=. Empty input still returns -1. A first element equal to the target returns 0.",
                "Check: 2+3 = 5 at index 1.",
            ],
            "final_frame": _frame("code", "coder", "high"),
        }

    if kind == "retry":
        folder = rng.choice(("docs", "notes", "ops", "runbooks"))
        name = f"cutoff-{rng.randint(10, 99)}.md"
        wrong = name
        right = f"{folder}/{name}"
        hour = rng.choice((15, 16, 17, 18, 21))
        owner = rng.choice(("payments", "billing", "identity", "search"))
        body = f"Cutoff is {hour}:00 local. Page the {owner} owner, not the whole channel."
        return {
            "user": f"Read {right} and tell me the cutoff. The file is in the repo.",
            "tools": [READ],
            "steps": [
                {
                    "role": "assistant",
                    "tool_calls": [_call("read_file", {"path": wrong})],
                    "frame": _frame(mode, construct, "low"),
                    "think_lines": [f"The note is probably {wrong}. Try the short path first."],
                },
                {"role": "tool", "content": f"failed to open {wrong}: no such file or directory"},
                {
                    "role": "assistant",
                    "tool_calls": [_call("read_file", {"path": right})],
                    "frame": _frame(mode, construct, "low"),
                    "think_lines": [
                        f"The short path is missing. The user said the folder is {folder}.",
                        f"Retry read_file with {right}, not the same path.",
                    ],
                },
                {"role": "tool", "content": body},
            ],
            "final_answer": f"Cutoff is {hour}:00 local. Page the {owner} owner, not the whole channel.",
            "final_lines": [
                f"First read of {wrong} failed: no such file.",
                f"Second read of {right} returned the note.",
                f"The cutoff in the file is {hour}:00 local, and the page target is the {owner} owner.",
            ],
            "final_frame": _frame(mode, construct, "high"),
        }

    if kind == "diagnose":
        guessed = rng.choice(("leads", "prospects", "signups", "tickets"))
        real = rng.choice(("billing.invoice", "billing.receipt", "ops.job", "support.case"))
        return {
            "user": f"How many open rows are sitting in the {guessed} table? Use the warehouse, not a guess.",
            "tools": [QUERY, SEARCH],
            "steps": [
                {
                    "role": "assistant",
                    "tool_calls": [_call("run_query", {"sql": f"SELECT COUNT(*) FROM {guessed} WHERE status = 'open'"})],
                    "frame": _frame(mode, construct, "low"),
                    "think_lines": [f"{guessed} table, open status. One count."],
                },
                {"role": "tool", "content": '{"success": false, "error": "unknown column status"}'},
                {
                    "role": "assistant",
                    "tool_calls": [_call("run_query", {"sql": f"SELECT COUNT(*) FROM {guessed} WHERE state = 'open'"})],
                    "frame": _frame(mode, construct, "low"),
                    "think_lines": [
                        "The column isn't status. state is the obvious rename. One corrected query, not the same SQL.",
                    ],
                },
                {"role": "tool", "content": '{"success": false, "error": "unknown table ' + guessed + '"}'},
                {
                    "role": "assistant",
                    "tool_calls": [_call("search_docs", {"query": "invoice table name and open status column"})],
                    "frame": _frame(mode, construct, "low"),
                    "think_lines": [
                        "Two query failures. The table name is wrong too.",
                        "Stop guessing columns. search_docs for the schema, which is a different tool.",
                    ],
                },
                {
                    "role": "tool",
                    "content": f"Rows live in {real}. Open ones have closed_at IS NULL. There is no {guessed} table.",
                },
            ],
            "final_answer": (
                f"I don't have the count. {real} is the table, and open means closed_at is null. "
                f"There is no {guessed} table, so I'm not going to keep querying one."
            ),
            "final_lines": [
                "First query: unknown column status.",
                f"Second query: unknown table {guessed}. Same tool, still wrong.",
                f"search_docs says the rows are in {real} and open means closed_at IS NULL.",
                "A third guess at a table name would be the loop. Report the schema and stop.",
            ],
            "final_frame": _frame(mode, construct, "high"),
        }

    # pivot
    host = rng.choice((
        "status.internal.example",
        "health.internal.example",
        "ready.internal.example",
        "live.internal.example",
    ))
    urls = [
        f"http://{host}/health",
        f"https://{host}/health",
        f"https://{host}/health/",
    ]
    errors = ("connection refused", "timed out", "connection refused")
    steps = []
    for url, err in zip(urls, errors):
        steps.append(
            {
                "role": "assistant",
                "tool_calls": [_call("http_get", {"url": url})],
                "frame": _frame(mode, construct, "low"),
                "think_lines": [f"Try {url}."],
            }
        )
        steps.append({"role": "tool", "content": err})
    # Rewrite the later thinks so they show the diagnosis escalating, still low-band.
    steps[2]["think_lines"] = [
        f"{urls[0]} was connection refused. Try TLS on the same host before declaring it dead.",
    ]
    steps[4]["think_lines"] = [
        f"TLS timed out. A trailing slash is a different path on some proxies. One last variation.",
    ]
    return {
        "user": f"Is {host} up? Check the health URL.",
        "tools": [HTTP],
        "steps": steps,
        "final_answer": (
            f"{host} refused, then timed out, then refused again on the trailing slash. "
            f"I'm not sending a fourth request at that host. "
            f"Blocker: nothing is accepting connections there from here. "
            f"Next useful step is the box itself, or a different network, not another spelling of the same URL."
        ),
        "final_lines": [
            f"Attempt 1 {urls[0]}: connection refused.",
            f"Attempt 2 {urls[1]}: timed out. That was the alternative scheme, and it also failed.",
            f"Attempt 3 {urls[2]}: connection refused. A path tweak is not a new diagnosis.",
            "Do not repeat the failed host or a cosmetic variation of it.",
            "Report the blocker. The health check is not going to start working because the URL gained a slash.",
        ],
        "final_frame": _frame(mode, construct, "high"),
    }


def kinds_for(spec: Spec, index: int) -> str | None:
    if spec.id in ("agi-teacher-007", "agi-brainstorm-007"):
        return ("call", "retry", "diagnose", "pivot", "direct")[index % 5]
    if spec.category == "mode" and spec.id == "build" and index % 3 == 0:
        return ("retry", "diagnose", "pivot")[(index // 3) % 3]
    if spec.category == "mode" and spec.id == "code" and index % 5 == 0:
        return "code_retry"
    if spec.category == "pathway" and spec.id == "s2" and index % 5 == 0:
        return ("retry", "pivot", "diagnose")[index % 3]
    if spec.category == "channel" and spec.id == "reasoning" and index % 7 == 0:
        return ("call", "direct", "retry")[index % 3]
    return None
