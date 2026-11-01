# Sharp-Spark v5.0.0

Dynamic-frame chat template for XHToken/Spark-X2.6-4B.

## What changed from v4.1.0

- **No keyword routing.** Construct / persona / identity are no longer chosen by substring matches on the last user turn.
- **FRAME CARD always present.** The model is given the full inventory and told to silently pick the best combination and inhabit it. No “I am in coder mode” announcements.
- **Explicit overrides still work.** Pass `construct=`, `persona=`, or `identity=` in `chat_template_kwargs` (or template params) to force a frame; the detailed block is then emitted with a `(forced)` marker.
- **Optional private frame tag** for SFT: inside `<think>` the model may write  
  `[frame: construct=NAME|persona=NAME|identity=NAME]`  
  Serving layer can strip it; the template does not require it.
- Reasoning tiers, tools, gentle defaults, adaptive evolution, validation, terseness kept.

## Files

| File | Purpose |
|------|---------|
| `chat_template.jinja` | Drop-in template |
| `verify_template.py` | Automated checks (parse, routing absence, overrides, tools, tiers) |
| `make_synth.py` | Seed synthetic SFT data (ShareGPT JSONL) |
| `synth_frames.jsonl` | 10 starter examples |

## Use

```bash
# transformers / HF
tokenizer.apply_chat_template(messages, add_generation_prompt=True,
    reasoning_effort="medium")           # model decides frame
# or force:
tokenizer.apply_chat_template(..., construct="coder", persona="friend")

# llama.cpp
llama-server --chat-template-file chat_template.jinja ...

# verify
python3 verify_template.py
python3 verify_template.py --show-render
```

## Training the dynamic behaviour (single model)

1. Start from the seed: `python3 make_synth.py --out synth_frames.jsonl --n 200` (cycles and lightly varies the seeds).
2. Expand offline with a stronger teacher if you want scale: same system (FRAME CARD), user prompts that clearly imply one construct, teacher answers that (a) put the private frame tag in thinking and (b) answer fully in-frame with no announcement.
3. SFT (or light DPO against “announced the frame” / “wrong frame” negatives) on Spark-X2.6-4B. No second model required.
4. After training, the same `chat_template.jinja` is used at inference; the model has internalised the inventory and the silent-choice rule.

## Design intent

The template is self-describing. A model that can follow instructions (or that has been shown a few hundred in-frame examples) can read the FRAME CARD and select. Keyword lists were the previous bottleneck; they are gone.
