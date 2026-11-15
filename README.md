# xhtoken spark 2.6 4b — chat template

Root `chat_template.jinja` is the chat template for **xhtoken spark 2.6 4b** (XHToken/Spark-X2.6-4B). The architecture class in this repo is still `spark2_5`: hidden size 2560, 36 layers, vocab 131072, about 4.11B parameters. Spark 2.6 keeps that text core. It is not the Qwen3.5 / Qwen3.6-VL dump that used to sit next to it.

The template is Sharp-Spark v5.1.0. The rendered wire is Sharp-Spark v5.0.1, which is the latest complete file in that line:

- official Spark control tokens, from the stock template recorded in `docs/sharp-spark-specs.txt`
- Sharp-Spark v5.0.0 dynamic frame (silent selection, no keyword routing, explicit kwargs force a frame)
- taxonomy v0.3 locked in v5.0.1: 25 modes, 30 constructs, 20 personas, 33 identities, 8 themes

Native thinking levels are `none`, `low`, and `high`. `enable_thinking=False` or `reasoning_effort=off` closes the channel (`</think>`). System 1 and System 3 use `low`. System 2 and `auto` use `high`.

Control tokens:

```text
<｜start▁of▁sentence｜> <|System|> ... <｜end▁of▁sentence｜>
<｜start▁of▁sentence｜> <|User|> ... <｜end▁of▁sentence｜>
<｜start▁of▁sentence｜> <|Bot|> <think> ... </think> ... <｜end▁of▁sentence｜>
<｜start▁of▁sentence｜> <|Tool|> <tool_response> ... </tool_response> <｜end▁of▁sentence｜>
```

Tool calls use `<tool_call>`, `<arg_key>`, and `<arg_value>`. String arguments are copied through as-is. `| tojson` is called with no arguments so llama.cpp minja can render it.

ChatML (`<|im_start|>`), Qwen vision pads, and the Gemma, Llama, Mistral, and GLM wires are other models. They stay in `templates/archive/` and are not part of this template. The Spark text model rejects non-text content blocks.

Check a render with:

```bash
python3 scripts/verify_template.py
python3 scripts/extract_taxonomy.py
```

## Layout

```text
chat_template.jinja          final Sharp-Spark template
README.md
model/spark/                 Spark2_5 config, modeling code, weight index, tokenizer
model/qwen3_5/               separate Qwen3.5 / Qwen3.6-VL config and tokenizer dump
templates/archive/spark/     older Sharp-Spark versions and the official stock template
templates/archive/qwen/      ChatML, froggeric, Protium-Qwen, Ornith, arrow, DavidAU
templates/archive/gemma/
templates/archive/llama/
templates/archive/mistral/
templates/archive/glm/
templates/archive/deepseek/
templates/archive/misc/      Ring, LFM2.5, ZAYA example, ORBIT injection snippet
docs/                        master plan, handoff, drift notes, specs snapshot, taxonomy
docs/notes/                  session dump and clipboard notes
scripts/                     verify_template.py, extract_taxonomy.py, make_synth.py, probe_frames.py
```

`model/spark/config.json` is the patched Spark config that matches `configuration_spark.py` (sliding window 4096, YaRN factor 4, untied embeddings). `model/spark/model.safetensors.index.json` is a tied ~4.11B map and has no separate `lm_head`. The stock tied config, including its quantization map, is the `config.json` section of `docs/sharp-spark-specs.txt`.

`model/spark/tokenizer_config.json` and `special_tokens_map.json` are the Spark tokenizer from that same specs snapshot (`bos` / `eos` are the start- and end-of-sentence tokens, `tool_parser_type` is `glm47`). They do not embed a `chat_template` string. The root `chat_template.jinja` is the template to pass to `apply_chat_template`. The Qwen tokenizer files were not updated: they belong to the other model and use ChatML ids, and they did not contain a template either.

The previous root `chat_template.jinja` was a large DavidAU Qwen 3.8 template. It is kept at `templates/archive/qwen/previous-root-davidau-qwen3.8.jinja`.
