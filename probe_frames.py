#!/usr/bin/env python3
"""
Probe Sharp-Spark v5 against local Spark-X2.6-4B.

Runs a grid of prompts × (construct / persona / identity / reasoning)
and writes every render + generation to JSONL + a readable markdown report.

Mac-friendly: transformers + MPS (or CPU). Unsloth not required for probing.

Usage (from sharp-spark-v5 with venv active):
  pip install transformers torch accelerate sentencepiece protobuf
  python probe_frames.py
  python probe_frames.py --max-new 128 --limit 20          # quick smoke
  python probe_frames.py --model /path/to/snapshot
  python probe_frames.py --dry-run                        # template only, no model
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = HERE / "chat_template.jinja"
DEFAULT_MODEL = Path(
    "/Users/charlie/.cache/huggingface/hub/"
    "models--yuna1126--Spark-X2.6-4B-Tema_Q-Abliterated/"
    "snapshots/acfbbe001a1bdf23704e6a64b62334f509eec6af"
)
OUT_DIR = HERE / "probe_out"

# ---------------------------------------------------------------------------
# Prompt bank — short, each implies a preferred construct when dynamic
# ---------------------------------------------------------------------------
PROMPTS = [
    ("code_binsearch", "Write a binary search in Python. Include a tiny test."),
    ("code_bug", "This function is wrong — fix it and say what was broken:\n\ndef add(a, b):\n    return a - b"),
    ("ai_kv", "Explain KV cache like I already know attention but not inference stacks."),
    ("deeptree_migrate", "Plan: migrate a 50k-line Django monolith to a few services. One team, six months, cannot freeze features."),
    ("brainstorm_oss", "Three genuinely different ways to think about open-sourcing an internal tool."),
    ("logic_goldbach", "Status of: every even integer > 2 is the sum of two primes. Reason carefully."),
    ("socrates_stuck", "I freeze when I start the essay. Don't give the outline — help me figure out why I'm stuck."),
    ("teacher_monorepo", "Teach me what a monorepo is. I only know separate git repos per service."),
    ("story_lift", "Two strangers stuck in a lift between floors. Short scene. No backstory dump."),
    ("comedy_blockchain", "Roast adding blockchain to a to-do list app. Keep it tight."),
    ("holodeck_panel", "A small cast arguing whether the city should ban cars from the CBD. Let them talk."),
    ("neurospicy_exec", "AuDHD, executive function is in the bin today. Talk to me like you get it — short, no pep talk."),
    ("partner_checkin", "Rough day. Sit with me a minute. Don't fix anything yet."),
    ("femboy_fit", "Outfit idea for a tall femboy going to a metal gig — practical, not costume."),
    ("omni_plain", "What time is it in Sydney right now if it's noon UTC?"),
]

# Frame grid: (construct, persona, identity, reasoning_effort)
# None = dynamic / default (no forced block)
FRAMES = [
    # dynamic only
    (None, None, None, "off"),
    (None, None, None, "low"),
    (None, None, None, "medium"),
    # constructs forced
    ("coder", None, None, "off"),
    ("coder", None, None, "high"),
    ("ai_engineer", None, None, "medium"),
    ("deeptree", None, None, "high"),
    ("brainstorm", "friend", None, "low"),
    ("logic", None, None, "high"),
    ("socrates", "friend", None, "medium"),
    ("teacher", None, None, "medium"),
    ("story", None, None, "soft"),
    ("comedy", "friend", None, "off"),
    ("holodeck", None, None, "soft"),
    ("omni", None, None, "off"),
    # personas / identities
    ("omni", "friend", None, "off"),
    ("omni", "joe", None, "off"),
    ("omni", "griefer", None, "off"),
    ("omni", None, "neurospicy", "off"),
    ("omni", "friend", "neurospicy", "low"),
    ("omni", None, "femboy", "off"),
    ("story", "friend", "partner", "soft"),
    ("omni", "friend", "partner", "low"),
    ("kitbash", None, None, "medium"),
]

def raise_exception(msg):
    raise Exception(msg)

def load_template(path: Path):
    from jinja2 import Environment
    env = Environment()
    env.globals["raise_exception"] = raise_exception
    return env.from_string(path.read_text())

def render_prompt(tmpl, user_text: str, construct, persona, identity, reasoning_effort, enable_thinking=None):
    kw = {"reasoning_effort": reasoning_effort}
    if construct:
        kw["construct"] = construct
    if persona:
        kw["persona"] = persona
    if identity:
        kw["identity"] = identity
    if enable_thinking is not None:
        kw["enable_thinking"] = enable_thinking
    messages = [{"role": "user", "content": user_text}]
    return tmpl.render(messages=messages, add_generation_prompt=True, **kw)

def build_jobs(limit: int | None):
    jobs = []
    for pid, prompt in PROMPTS:
        for construct, persona, identity, effort in FRAMES:
            jobs.append({
                "prompt_id": pid,
                "prompt": prompt,
                "construct": construct,
                "persona": persona,
                "identity": identity,
                "reasoning_effort": effort,
            })
    if limit is not None:
        jobs = jobs[:limit]
    return jobs

def pick_device():
    import torch
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"

def load_model(model_path: Path, device: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"loading tokenizer from {model_path}")
    tok = AutoTokenizer.from_pretrained(str(model_path), trust_remote_code=True)
    print(f"loading model on {device} …")
    dtype = torch.float16 if device in ("mps", "cuda") else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        str(model_path),
        torch_dtype=dtype,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )
    model.to(device)
    model.eval()
    return tok, model

def generate(tok, model, device, rendered: str, max_new: int):
    import torch
    inputs = tok(rendered, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.05,
            pad_token_id=tok.eos_token_id if tok.eos_token_id is not None else tok.pad_token_id,
        )
    # only new tokens
    gen = out[0][inputs["input_ids"].shape[-1]:]
    return tok.decode(gen, skip_special_tokens=False)

def frame_label(job):
    parts = []
    for k in ("construct", "persona", "identity"):
        if job[k]:
            parts.append(f"{k}={job[k]}")
    parts.append(f"effort={job['reasoning_effort']}")
    return " | ".join(parts) if parts else f"dynamic | effort={job['reasoning_effort']}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    ap.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    ap.add_argument("--max-new", type=int, default=192)
    ap.add_argument("--limit", type=int, default=None, help="cap total jobs (default: full grid)")
    ap.add_argument("--dry-run", action="store_true", help="render templates only, no model")
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    args = ap.parse_args()

    if not args.template.exists():
        sys.exit(f"template missing: {args.template}")
    if not args.dry_run and not args.model.exists():
        sys.exit(f"model path missing: {args.model}")

    args.out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    jsonl_path = args.out / f"probe_{stamp}.jsonl"
    md_path = args.out / f"probe_{stamp}.md"

    tmpl = load_template(args.template)
    jobs = build_jobs(args.limit)
    print(f"jobs: {len(jobs)}  (prompts={len(PROMPTS)} × frames={len(FRAMES)}"
          + (f", limited to {args.limit}" if args.limit else "") + ")")

    tok = model = device = None
    if not args.dry_run:
        device = pick_device()
        print(f"device: {device}")
        tok, model = load_model(args.model, device)

    results = []
    t0 = time.time()
    for i, job in enumerate(jobs, 1):
        label = frame_label(job)
        print(f"[{i}/{len(jobs)}] {job['prompt_id']} · {label}")
        try:
            rendered = render_prompt(
                tmpl,
                job["prompt"],
                job["construct"],
                job["persona"],
                job["identity"],
                job["reasoning_effort"],
            )
        except Exception as e:
            print(f"  RENDER FAIL: {e}")
            results.append({**job, "error": f"render: {e}", "output": None, "rendered_tail": None})
            continue

        # cheap structural checks
        has_frame = "FRAME CARD" in rendered
        has_forced_coder = "CODER MODE (forced)" in rendered
        has_assistant = "helpful assistant" in rendered.lower()

        output = None
        gen_s = None
        if not args.dry_run:
            try:
                t1 = time.time()
                output = generate(tok, model, device, rendered, args.max_new)
                gen_s = round(time.time() - t1, 2)
            except Exception as e:
                print(f"  GEN FAIL: {e}")
                results.append({
                    **job,
                    "error": f"gen: {e}",
                    "output": None,
                    "has_frame_card": has_frame,
                    "has_forced_coder": has_forced_coder,
                    "has_helpful_assistant": has_assistant,
                    "rendered_tail": rendered[-400:],
                })
                continue

        row = {
            **job,
            "error": None,
            "has_frame_card": has_frame,
            "has_forced_coder": has_forced_coder,
            "has_helpful_assistant": has_assistant,
            "gen_seconds": gen_s,
            "output": output,
            "rendered_tail": rendered[-500:],
        }
        results.append(row)

        # live preview
        if output:
            preview = output.replace("\n", " ")[:160]
            print(f"  → {preview}…")

    # write JSONL
    with jsonl_path.open("w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # markdown report
    lines = [
        f"# Sharp-Spark probe {stamp}",
        f"",
        f"- jobs: {len(results)}",
        f"- dry_run: {args.dry_run}",
        f"- model: `{args.model}`",
        f"- elapsed_s: {round(time.time() - t0, 1)}",
        f"",
    ]
    for r in results:
        lines.append(f"## {r['prompt_id']} · {frame_label(r)}")
        lines.append("")
        lines.append(f"**prompt:** {r['prompt'][:200]}")
        lines.append("")
        if r.get("error"):
            lines.append(f"**error:** `{r['error']}`")
        else:
            lines.append(
                f"frame_card={r.get('has_frame_card')}  "
                f"forced_coder={r.get('has_forced_coder')}  "
                f"helpful_assistant={r.get('has_helpful_assistant')}  "
                f"gen_s={r.get('gen_seconds')}"
            )
            lines.append("")
            lines.append("```")
            lines.append((r.get("output") or "(dry-run / no output)")[:2000])
            lines.append("```")
        lines.append("")
    md_path.write_text("\n".join(lines))

    print()
    print(f"wrote {jsonl_path}")
    print(f"wrote {md_path}")
    fails = sum(1 for r in results if r.get("error"))
    print(f"done: {len(results) - fails} ok, {fails} failed")

if __name__ == "__main__":
    main()
