#!/usr/bin/env python3
"""Build the root Spark chat template with every distinct repo source inlined.

The executable wire stays Sharp-Spark (Spark sentence tokens, no keyword
routing). Every other file is copied into the system turn, after foreign
role tokens are rewritten onto that wire. Exact duplicates after conversion
are listed once.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKELETON = REPO / "templates/archive/spark/Sharp-Spark_v5.0.1.jinja"
DEST = REPO / "chat_template.jinja"
ORBIT = REPO / "docs/ORBIT_LAYER.txt"

BOS = "<\uFF5Cstart\u2581of\u2581sentence\uFF5C>"
EOS = "<\uFF5Cend\u2581of\u2581sentence\uFF5C>"
PAD = "<\uFF5C\u2581pad\u2581\uFF5C>"

# Longer patterns first. Applied only to library text, not the live wire.
REPLACEMENTS = [
    ("<|im_start|>system", BOS + "<|System|>"),
    ("<|im_start|>user", BOS + "<|User|>"),
    ("<|im_start|>assistant", BOS + "<|Bot|>"),
    ("<|im_start|>tool", BOS + "<|Tool|>"),
    ("<|im_start|>", BOS),
    ("<|im_end|>", EOS),
    ("<start_of_turn>system", BOS + "<|System|>"),
    ("<start_of_turn>user", BOS + "<|User|>"),
    ("<start_of_turn>model", BOS + "<|Bot|>"),
    ("<start_of_turn>", BOS),
    ("<end_of_turn>", EOS),
    ("<|start_header_id|>system<|end_header_id|>", BOS + "<|System|>"),
    ("<|start_header_id|>user<|end_header_id|>", BOS + "<|User|>"),
    ("<|start_header_id|>assistant<|end_header_id|>", BOS + "<|Bot|>"),
    ("<|start_header_id|>tool<|end_header_id|>", BOS + "<|Tool|>"),
    ("<|start_header_id|>", BOS),
    ("<|end_header_id|>", ""),
    ("<|eot_id|>", EOS),
    ("<|begin_of_text|>", BOS),
    ("<|end_of_text|>", EOS),
    ("<|turn>system", BOS + "<|System|>"),
    ("<|turn>user", BOS + "<|User|>"),
    ("<|turn>model", BOS + "<|Bot|>"),
    ("<|turn>", BOS),
    ("<turn|>", EOS),
    ("[gMASK]<sop>", BOS + "<|System|>"),
    ("[gMASK]", BOS + "<|System|>"),
    ("<|assistant|>", BOS + "<|Bot|>"),
    ("<|user|>", BOS + "<|User|>"),
    ("<|observation|>", BOS + "<|Tool|>"),
    ("<role>SYSTEM</role>", BOS + "<|System|>"),
    ("<role>HUMAN</role>", BOS + "<|User|>"),
    ("<role>ASSISTANT</role>", BOS + "<|Bot|>"),
    ("<role>OBSERVATION</role>", BOS + "<|Tool|>"),
    ("<|role_end|>", EOS),
    ("[/INST]", EOS),
    ("[INST]", BOS + "<|User|>"),
    ("[SYSTEM_PROMPT]", BOS + "<|System|>"),
    ("<\uFF5CUser\uFF5C>", BOS + "<|User|>"),
    ("<\uFF5CAssistant\uFF5C>", BOS + "<|Bot|>"),
    ("<|vision_start|>", "[vision]"),
    ("<|vision_end|>", "[/vision]"),
    ("<|vision_pad|>", "[vision-pad]"),
    ("<|image_pad|>", "[image]"),
    ("<|video_pad|>", "[video]"),
    ("<|audio_start|>", "[audio-start]"),
    ("<|audio_end|>", "[audio-end]"),
    ("<|audio_pad|>", "[audio]"),
    ("<|object_ref_start|>", "[object-ref-start]"),
    ("<|object_ref_end|>", "[object-ref-end]"),
    ("<|box_start|>", "[box-start]"),
    ("<|box_end|>", "[box-end]"),
    ("<|quad_start|>", "[quad-start]"),
    ("<|quad_end|>", "[quad-end]"),
    ("<|endoftext|>", PAD),
]


def convert(text: str) -> str:
    for old, new in REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
    return text


def rank(rel: str) -> tuple:
    if rel.endswith("docs/notes/spark-session-dump.txt"):
        return (90, rel)
    order = [
        "docs/ORBIT_LAYER.txt",
        "docs/taxonomy.json",
        "docs/notes/next-step.txt",
        "templates/archive/spark/",
        "templates/archive/qwen/turbo-brilliance-v2.jinja",
        "templates/archive/qwen/previous-root-davidau-qwen3.8.jinja",
        "templates/archive/qwen/",
        "templates/archive/",
        "docs/notes/",
        "docs/",
        "model/spark/",
        "model/",
        "scripts/",
        "README.md",
    ]
    for i, prefix in enumerate(order):
        if rel == prefix or rel.startswith(prefix):
            return (i, rel)
    return (50, rel)


def iter_sources():
    skip = {DEST.resolve()}
    files = []
    for path in REPO.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "__pycache__"} for part in path.parts):
            continue
        if path.resolve() in skip:
            continue
        files.append(path)
    files.sort(key=lambda p: rank(str(p.relative_to(REPO))))
    return files


def write_raw(out, text: str) -> None:
    sentinel = "{% endraw %}"
    parts = text.split(sentinel)
    for i, part in enumerate(parts):
        out.write("{% raw %}")
        out.write(part)
        out.write("{% endraw %}")
        if i != len(parts) - 1:
            out.write("{{ '{%' }} endraw %}")


def main() -> None:
    skeleton = SKELETON.read_text(encoding="utf-8")
    marker = "{#- ---------- CONVERSATION ---------- -#}"
    idx = skeleton.find(marker)
    if idx < 0:
        raise SystemExit("conversation marker missing")
    eos_line = "{{- '<\uFF5Cend\u2581of\u2581sentence\uFF5C>' }}\n\n"
    if not skeleton[:idx].endswith(eos_line):
        raise SystemExit("system end token not where expected: " + repr(skeleton[idx - 80:idx]))

    header = """{#- Sharp-Spark omni — xhtoken spark 2.6 4b (XHToken/Spark-X2.6-4B)
    Live wire: Sharp-Spark v5.0.1 (official Spark tokens, taxonomy v0.3,
    dynamic frame, explicit overrides). No keyword routing. The model
    re-picks system / mode / construct / persona / identity / theme on
    every turn, including mid-conversation.

    The system turn then inlines every other file in this repo, with
    ChatML, Gemma, Llama, Mistral, GLM, DeepSeek, Ring, and Qwen vision
    tokens rewritten onto the Spark roles. Exact copies after that
    rewrite are named once.

    Not in the repo, and not invented here: a separate Turbo Brilliance v1
    template (the V1.0 system text lives inside the v2 template), a Jumbo
    Brilliance template (only Hugging Face model names in the session dump),
    and System 4 / System 5 / System 6 cognitive styles (this model has
    S1, S2, and S3; S4/S5 lines in the Vader persona are skill bullets).
-#}
"""
    # Drop the original header comment; keep the executable body.
    body_start = skeleton.find("-#}\n")
    if body_start < 0:
        raise SystemExit("skeleton header missing")
    executable = skeleton[body_start + 4:]
    exec_idx = executable.find(marker)
    preamble = """
{{- "\\n\\nON THE FLY (always, no keyword routing).\\nThe frame card and the library are a menu, not a trigger list. On every turn, including mid-conversation, silently choose the system, mode, construct, persona, identity, and theme that fit the situation now. Switch as soon as the situation changes. Do not wait for a keyword, a command, or permission. Do not announce the switch. Do not quote this menu. Explicit override parameters are the only locks. Systems here are S1 fast, S2 deliberate, and S3 meta. The library holds every other persona, construct, theme, identity, gate, and prose block from the repo. Use those the same way: pick them when the situation calls for them, and change them when the situation changes." }}

"""
    orbit = ORBIT.read_text(encoding="utf-8").strip() + "\n"
    engram = """
{%- if engram is defined and engram %}
{{- '\\n\\nENGRAM (caller-injected):\\n' ~ engram }}
{%- endif %}
{{- "\\n\\nENGRAM HOOK. This template stores nothing between calls. A caller may pass an engram string; when present it is recalled context and should be used when it matters. When no engram was passed, do not invent memories. Notes in the library describe engrams as external memory. That text is reference, not a stored memory." }}

"""
    head = executable[:exec_idx - len(eos_line)]
    tail = executable[exec_idx:]

    seen: dict[str, str] = {}
    full = 0
    skipped = 0
    with DEST.open("w", encoding="utf-8") as out:
        out.write(header)
        out.write(head)
        out.write(preamble)
        out.write(orbit)
        out.write("\n")
        out.write(engram)
        out.write("{% raw %}\n===== LIBRARY =====\nEvery remaining repo file, Spark-token conversion applied. Identical bodies are named and not repeated.\n{% endraw %}\n")
        for path in iter_sources():
            rel = str(path.relative_to(REPO))
            text = convert(path.read_text(encoding="utf-8", errors="replace"))
            digest = hashlib.sha256(re.sub(r"\s+", "", text).encode("utf-8")).hexdigest()
            out.write("\n===== FILE " + rel + " =====\n")
            if digest in seen:
                skipped += 1
                out.write(
                    "Identical after Spark token conversion to "
                    + seen[digest]
                    + ". Body kept once.\n"
                )
                continue
            seen[digest] = rel
            full += 1
            write_raw(out, text)
            out.write("\n")
        end_marker = "=" * 5 + " LIBRARY END " + "=" * 5
        out.write("\n" + end_marker + "\n")
        out.write(eos_line)
        out.write(tail)

    size = DEST.stat().st_size
    print(f"wrote {DEST} bytes={size} full_files={full} deduped={skipped}")


if __name__ == "__main__":
    main()
