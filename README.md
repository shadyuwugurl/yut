# xhtoken spark 2.6 4b — chat template

Root `chat_template.jinja` is the chat template for **xhtoken spark 2.6 4b** (XHToken/Spark-X2.6-4B, architecture `spark2_5`, about 4.11B). The live wire is Sharp-Spark: Spark sentence tokens, taxonomy v0.3, and explicit override kwargs. There is no keyword routing. On every turn, including mid-conversation, the model is told to pick system, mode, construct, persona, identity, and theme from the situation and to switch when the situation changes.

The same system turn then inlines every other file in the repo (templates, docs, notes, JSON, model sources, scripts). ChatML, Gemma, Llama, Mistral, GLM, DeepSeek, Ring, and Qwen vision tokens in that library are rewritten onto the Spark roles. The file is about 4.1 MB. Rebuild it with `python3 scripts/build_omni_template.py`.

A one-message `"hi"` render is about **1.10 million** `cl100k_base` tokens (about 1.00 million by a chars/4 estimate). `scripts/verify_template.py` prints the exact estimate for the current file. The Spark tokenizer is not in the repo, so this is not a Spark token-id count. The stock tokenizer `model_max_length` is 131072. The patched `max_position_embeddings` is 1,048,576. The rendered prompt is larger than both, so a basic chat does not fit either window. That is the cost of leaving the whole library always on.

Native thinking levels are `none`, `low`, and `high`. Pass `engram` to inject recalled text. The template does not store memory itself. ORBIT is always on, ahead of the library.

These names were not separate sources in the repo, and they were not invented:

- Turbo Brilliance v1 has no file of its own. The v2 template contains the "Turbo-Brilliance System V1.0" writeup, and that file is in the library.
- Jumbo Brilliance has no template or prompt. The session dump names a Hugging Face Jumbo-Fusion model, and that dump is in the library.
- System 4, System 5, and System 6 do not exist as cognitive styles. The frame card has S1, S2, and S3. S4/S5 lines inside the Vader persona are skill bullets, and they ride along inside the DavidAU text.

Control tokens:

```text
<｜start▁of▁sentence｜> <|System|> ... <｜end▁of▁sentence｜>
<｜start▁of▁sentence｜> <|User|> ... <｜end▁of▁sentence｜>
<｜start▁of▁sentence｜> <|Bot|> <think> ... </think> ... <｜end▁of▁sentence｜>
<｜start▁of▁sentence｜> <|Tool|> <tool_response> ... </tool_response> <｜end▁of▁sentence｜>
```

The Spark text path still rejects image and video blocks. Tool calls use `<tool_call>`, `<arg_key>`, and `<arg_value>`.

```bash
python3 scripts/verify_template.py
python3 scripts/extract_taxonomy.py
```

## Layout

```text
chat_template.jinja          always-on Spark template plus the full library
README.md
model/spark/                 Spark2_5 config, modeling code, weight index, tokenizer
model/qwen3_5/               Qwen3.5 / Qwen3.6-VL config and tokenizer dump
templates/archive/spark/     Sharp-Spark v4–v5 and the official stock template
templates/archive/qwen/      ChatML, froggeric, Protium-Qwen, Ornith, arrow, DavidAU, Turbo Brilliance v2
templates/archive/gemma/
templates/archive/llama/
templates/archive/mistral/
templates/archive/glm/
templates/archive/deepseek/
templates/archive/misc/      Ring, LFM2.5, ZAYA example, ORBIT injection snippet
docs/                        master plan, handoff, drift notes, specs snapshot, taxonomy
docs/notes/                  session dump, Josie / next-step notes, clipboard pastes
scripts/                     build_omni_template.py, verify_template.py, extract_taxonomy.py, make_synth.py, probe_frames.py
```

`model/spark/tokenizer_config.json` does not embed a `chat_template`. The root file is the one to pass to `apply_chat_template`. The Qwen tokenizer files were left as the other model's tokenizer. Their ChatML strings inside the library copy are rewritten; the files under `model/qwen3_5/` are unchanged.

The previous root DavidAU template is still at `templates/archive/qwen/previous-root-davidau-qwen3.8.jinja`, and its text is also inside the root library.
