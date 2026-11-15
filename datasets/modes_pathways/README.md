# Modes, pathways, effort, and tool use

Training rows for the skinny Spark template. The model is supposed to pick the
frame from the situation. User turns do not name the mode, the effort, the
pathway, a protium level, a palette, or an agi id, and they do not carry a
`{REASON:...}` tag.

Labels are the canonical ids in `ids.json`, copied from `docs/taxonomy_skinny.json`
on `cursor/spark-skinny-template-3cef` (skinny-v1). The stable key is
`meta.category` + `meta.id`. Aliases (`ultra`, `xultra`, `dau_high`, legacy
`low` / `xhigh`, the `i` prefix, the `x` prefix) are inputs in that file, not
labels stored on a row.

This slice is pathway, mode, thinking_effort, reasoning_effort, channel,
protium, aesthetic, orbit, agi, stance, patch, and reasoning_mode. 91 ids.
Orbit, stance, patch, and reasoning_mode are tags beside the frame. They are
not frame fields. Tool use is a trajectory on rows whose frame already calls
for it (`mode/code`, `mode/build`, `pathway/s2`, `channel/reasoning`, and the
`007` agi fusions): a clean call, a corrected retry, a second failure that
switches tools, a third failure that stops, or a direct answer when the tool
does not apply.

`meta.frame` is the frame the completion inhabits. `mode/auto` and
`pathway/auto` record the concrete pick in the frame and keep `auto` as the
label. A private `[frame: ...]` tag is allowed inside `<think>` and nowhere
else. `channel/instruct` and `thinking_effort/off` have no think tag.

## Layout

```text
ids.json          canonical slice (do not rename an id)
generate.py       procedural bank, or an OpenAI-compatible teacher
validate.py       filters plus a Jinja render through chat_template.jinja
seed.jsonl        20 authored rows per id
sample/           100 procedural rows per id, gzip, train/val
```

Think length is checked against the effort. `thinking_effort/low` is a short
think. `thinking_effort/high` is a deep one. `thinking_effort/off` and
`channel/instruct` are empty. `reasoning_effort/effort_low` through
`effort_xultra` use that ladder, and `effort_ultra` / `effort_xultra` run
longer than native high on purpose. Protium hermes and apollo stay short and
exit. Oracle, extreme, and loop run long. Swarm and council open the visible
answer with `[SWARM VERDICT]` and `[COUNCIL VERDICT]`.

## Commands

Seed (deterministic, no key):

```bash
python3 datasets/modes_pathways/generate.py \
  --backend procedural \
  --per-id 20 \
  --seed 7 \
  --source seed \
  --val-ratio 0.02 \
  --flat datasets/modes_pathways/seed.jsonl
```

Sample batch committed in this branch:

```bash
python3 datasets/modes_pathways/generate.py \
  --backend procedural \
  --per-id 100 \
  --seed 20261115 \
  --source procedural \
  --val-ratio 0.02 \
  --gzip \
  --out datasets/modes_pathways/sample
```

Full run. Default `--per-id` is 3000. With `OPENAI_API_KEY` unset, `--backend auto`
stays on the procedural bank. With a key, the teacher prompt is the full
`chat_template.jinja` and the rows are still emitted without that template.
A failed or empty teacher response falls back to the procedural row.

```bash
python3 datasets/modes_pathways/generate.py \
  --backend auto \
  --per-id 3000 \
  --seed 20261115 \
  --val-ratio 0.02 \
  --gzip \
  --out datasets/modes_pathways/full

OPENAI_BASE_URL=https://api.openai.com/v1 \
OPENAI_API_KEY=... \
MODEL=gpt-4.1 \
python3 datasets/modes_pathways/generate.py \
  --backend openai \
  --per-id 3000 \
  --seed 20261115 \
  --val-ratio 0.02 \
  --gzip \
  --out datasets/modes_pathways/full
```

Check a file, including a few renders through `scripts/verify_template.py`'s
Jinja environment (Spark tokens, `<think>`, `<arg_key>` / `<arg_value>`, and
the three tool-error warnings):

```bash
python3 datasets/modes_pathways/validate.py datasets/modes_pathways/seed.jsonl
python3 datasets/modes_pathways/validate.py \
  datasets/modes_pathways/sample/train.jsonl.gz \
  datasets/modes_pathways/sample/val.jsonl.gz
```

Val is about 2% by hash, with at least one val row per id.
