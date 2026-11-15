# xhtoken spark 2.6 4b — chat template

Root `chat_template.jinja` is the chat template for **xhtoken spark 2.6 4b** (XHToken/Spark-X2.6-4B, architecture `spark2_5`, about 4.11B, native context 1,048,576).

The live wire is Sharp-Spark v5.1.0, which is the newest Sharp-Spark file (v5.0.1) with one added identity, `josie`. Older Sharp-Spark versions stay in `templates/archive/spark/` and are not copied into the template. There is no keyword routing and no engram hook. On every turn the model is told to pick system, mode, construct, persona, identity, and theme from the situation and to switch when the situation changes. Explicit override kwargs still force a frame.

The system turn then carries a sourced catalog:

- The owner's taxonomy: 25 modes, 30 constructs, 20 personas, 33 identities, 8 themes, plus the ORBIT reasoning layer from `docs/ORBIT_LAYER.txt`.
- DavidAU Turbo Brilliance System V2.0 and its AGI modes, from the GGUF `tokenizer.chat_template` of [Qwen3.8-40B-Ultimate-Heretic-Uncensored-Turbo-Brilliance-50x-AGI-NEO-GGUF](https://huggingface.co/DavidAU/Qwen3.8-40B-Ultimate-Heretic-Uncensored-Turbo-Brilliance-50x-AGI-NEO-GGUF). The 27B AGI repo matches it aside from the URL.
- The Turbo Brilliance System V1.0 help menu, from the GGUF template of [Qwen3.8-27B-Turbo-Brilliance-50X-Reasoning-Instruct-NEO-MAX-MTP-GGUF](https://huggingface.co/DavidAU/Qwen3.8-27B-Turbo-Brilliance-50X-Reasoning-Instruct-NEO-MAX-MTP-GGUF). Matching persona bodies are not repeated.
- Power X12 help and effort blocks, from [LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF](https://huggingface.co/DavidAU/LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF).
- The Jumbo 747 patch line. The rest of [the Jumbo GGUF template](https://huggingface.co/DavidAU/Qwen3.8-27B-Jumbo-Fusion-IQ-747-900-Turbo-Brilliance-50X-Reasoning-Instruct-NEO-MAX-MTP-GGUF) matches V1.0.
- The looping-model premise from the [31B looping card](https://huggingface.co/DavidAU/Qwen3.8-31B-Looping-Transformer-Ablit-Heretic-ARA-Uncensored). Its chat template is V2.0 and is not repeated.
- Deckard, as the dataset definitions on the model cards. Those repos' chat templates are the base model templates and do not contain a Deckard persona prompt.
- Distinct Josie system prompts from [Goekdeniz-Guelmez](https://huggingface.co/Goekdeniz-Guelmez): Josie v2, J.O.S.I.E.-R.1, the short base prompt, v6, v4o, and the OpenWebUI prompt as published (it contains ellipses in the source). Charlie's attached Josie file adds only the paragraphs that were not already there.
- Twin-Turbo's brainstormer card and Deep Research protocol, from the ULTRA-HERETIC `chat_template-tturbo-v2.jinja`. The 709-L GGUF and the ULTRA GGUF repeat those blocks.
- Extra help menus that are not the same text as V1 or V2: Flash abliterated (also Charlie's attached Turbo v2 template), the 8B X12 GGUF, the LFM2.5-24B GGUF, and Ultimate Build2.
- Protium 1.0's objective-gated contract and Hermes-through-Proteus spectrum, from Charlie's attached template. `protium_level` forces one level. Inline `[L0]` / `{REASON:}` sniffing is not executed.
- The V5 Mastercraft palettes and craft specification. `aesthetic_preset` forces one palette. The live tool path clips with `max_tool_arg_chars` / `max_tool_response_chars`, reads `.arguments` or `.parameters` or `.input`, keeps reasoning from `reasoning_content` / `thinking` / `reasoning` (including a `{text: ...}` field), and appends the 3-tier tool-error warnings. It does not reject images.

`{REASON:...}` tags in that catalog are names, not triggers. ChatML and Llama role tokens in the sourced text are rewritten onto Spark roles.

A one-message `"hi"` render is about **76,512** `cl100k_base` tokens. The file is about **365 KB**. The Spark tokenizer is not in the repo, so this is not a Spark token-id count. That is comfortably under the 1,048,576 window. `scripts/verify_template.py` prints the exact estimate.

```bash
python3 scripts/build_omni_template.py
python3 scripts/verify_template.py
python3 scripts/extract_taxonomy.py
```

The raw DavidAU templates used to build the catalog are in `sources/hf/`.

## Layout

```text
chat_template.jinja
README.md
sources/hf/                  DavidAU templates the catalog is extracted from
model/spark/                 Spark2_5 config, modeling, tokenizer, weight index
model/qwen3_5/               separate Qwen3.5 / Qwen3.6-VL dump
templates/archive/spark/     Sharp-Spark v4.0.0, v4.1.0, v5.0.0, v5.0.1, official stock
templates/archive/qwen/      other ChatML templates, including the local Turbo Brilliance v2 copy
templates/archive/{gemma,llama,mistral,glm,deepseek,misc}/
docs/  docs/notes/
scripts/
```

`model/spark/tokenizer_config.json` does not embed a chat template. Pass the root file to `apply_chat_template`.

## Not found

- A separate Turbo Brilliance v1 template file on Hugging Face. V1.0 is the system name inside the 27B NEO-MAX GGUF template. The two Flash Turbo Brilliance GGUFs did not yield a `tokenizer.chat_template` in the first 20 MB of metadata.
- A Jumbo Brilliance persona that is not the V1.0 template plus the 747 patch line.
- A Deckard system prompt inside `chat_template.jinja`. Deckard on the cards is a fine-tune dataset.
- A looping chat template distinct from Turbo Brilliance V2.0. The looping behavior is described in the model-card dev notes.
- System 4, 5, and 6 as cognitive styles.
- A Josie prompt on `JOSIExMistral-7B-v0.32`.
