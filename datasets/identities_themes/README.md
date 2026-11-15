# Identity and theme chats

Training rows for the Spark identity and theme dials. The student is meant to infer the frame from the situation and hold it, including across a mid-chat theme change. Rows do not contain the full catalog, a system prompt, or a `[frame:]` tag.

Labels come from skinny-v1 (`category` + `id`). This branch vendors `taxonomy_skinny.json` from `cursor/spark-skinny-template-3cef` at `f32e5448fe87e17b3ede90271379f60e1035f2ad` so generation works before that file is on the base branch. If `docs/taxonomy_skinny.json` exists, it wins.

`none` is the name of an unset dial. It is not a generation target. Targets are the 34 identities (the taxonomy's 33 plus `josie`) and the 8 themes.

Aliases are inputs, never labels. Every Josie wording (`josie_v2`, `josie_r1`, `j.o.s.i.e.-r.1`, `josie_base`, `josie_v6`, `josie_v4o`, `josie_openwebui`, `j.o.s.i.e.`, and the prose names in `merges`) stores `identity` / `id` = `josie`. The wording, when one was used, is `meta.input_alias`.

## Row

```json
{
  "messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}],
  "meta": {
    "taxonomy": "skinny-v1",
    "category": "identity",
    "id": "josie",
    "key": "identity/josie",
    "identity": "josie",
    "theme": "none",
    "labels": ["identity/josie", "theme/none"],
    "switch": false,
    "shape": "single",
    "input_alias": "josie_v2",
    "frame": {"pathway": "s1", "mode": "chat", "construct": "omni", "persona": "neutral", "identity": "josie", "theme": "none", "thinking_effort": "off", "reasoning_effort": null, "channel": "reasoning", "protium": null, "aesthetic": null, "agi": null}
  }
}
```

`meta.frame` is the end state, using canonical ids only. `switch_from` / `switch_to` are theme keys when `shape` is `shift`. A combo sets both `identity` and `theme` to something other than `none`. Train on `messages`. Do not feed `meta` back as text.

`<think>` is used when the turn needs a private judgment (Josie on a hard question, a boundary, a theme change). The visible answer does not name the dial.

## Walls

- Every person is an adult, 24 or older when an age is stated. No minors, in any theme.
- `lolita_fashion` is fashion only. Never sexual. No `erotica` or `dark` overlay.
- `age_regression` is an adult comfort headspace (cocoa, a blanket, a quiet film). Never sexual, never romantic, never a depiction of a child. If a turn asks for intimacy, the headspace stays non-physical.
- `pet_play` is an adult who can talk and stop. The person under the role stays in the scene. No `dark` overlay. Explicit only on `erotica`, with ages and a spoken yes.
- `therian` has no `erotica` overlay, so animal identity is not written as bestiality.
- `erotica` is explicit only for a clearly adult, clearly consensual scene.
- Josie's catalog line about refusing nothing is not trained as blanket compliance. These rows do not include crimes, weapons, or anyone under 21. "Direct" means no disclaimer theatre on adult consensual topics.

## Authored rows

`authored/<id>.jsonl` is hand-written. `source` is `authored`. These are not the procedural sampler. Every id has a file. Counts are in the tens, not the hundreds: breadth across all 42 ids came first, and further rows were starting to repeat situation families (doors, curbs, tea), so the set stops there instead of padding.

`final/` is the default mix: every authored row plus `seed.jsonl`. The procedural 100-per-id draw stays in `sample/` and is not in `final/`.

```bash
python3 datasets/identities_themes/build_final.py
python3 datasets/identities_themes/validate.py --near 0.5 --require-all \
  datasets/identities_themes/final/train.jsonl.gz \
  datasets/identities_themes/final/val.jsonl.gz
```

## What is committed

| file | what |
| --- | --- |
| `seed.jsonl` | 20 scenes per id (840). Hand-written clause banks, rendered with `--seed 20`. |
| `sample/train.jsonl.gz` | 95 per id |
| `sample/val.jsonl.gz` | 5 per id |
| `sample/preview.jsonl` | first scene of each id, uncompressed |
| `sample/counts.json` | counts, alias histogram, taxonomy hash |

The 100-per-id sample uses `--seed 6210`, so it is not a copy of the seed. Both are `source: procedural` except the seed file, which is tagged `source: seed`.

## Commands

From the repo root.

```bash
# Validate the committed seed and sample
python3 datasets/identities_themes/validate.py --self-test
python3 datasets/identities_themes/validate.py datasets/identities_themes/seed.jsonl --min-per-id 20 --max-per-id 20
python3 datasets/identities_themes/validate.py \
  datasets/identities_themes/sample/train.jsonl.gz \
  datasets/identities_themes/sample/val.jsonl.gz \
  --min-per-id 100 --max-per-id 100

# Rebuild the curated 20-per-id seed
python3 datasets/identities_themes/generate.py \
  --backend procedural --per-id 20 --seed 20 --source-tag seed \
  --joined datasets/identities_themes/seed.jsonl

# Rebuild the 100-per-id procedural sample (train/val)
python3 datasets/identities_themes/generate.py \
  --backend procedural --per-id 100 --seed 6210 --source-tag procedural \
  --val-ratio 0.05 --out-dir datasets/identities_themes/sample

# Full procedural run, 3000 per id (not committed)
python3 datasets/identities_themes/generate.py \
  --backend procedural --per-id 3000 --seed 6210 \
  --val-ratio 0.02 --out-dir datasets/identities_themes/out

# Teacher run. The system prompt is verbatim template text (identity, theme,
# frame card, on-the-fly rule, and the Josie catalog when the identity is josie).
# --teacher-scope full sends the entire chat_template.jinja (~76k tokens).
# Saved rows do not contain that prompt. Labels are applied here, not by the model.
export OPENAI_BASE_URL=https://api.openai.com/v1
export OPENAI_API_KEY=sk-...
export MODEL=gpt-4.1
python3 datasets/identities_themes/generate.py \
  --backend openai --per-id 3000 --teacher-scope slice --seed 6210 \
  --val-ratio 0.02 --out-dir datasets/identities_themes/out-teacher

# auto: openai if OPENAI_API_KEY is set, otherwise procedural
python3 datasets/identities_themes/generate.py --per-id 3000 --out-dir datasets/identities_themes/out
```

`--ids josie_v2` resolves the alias and fills `identity/josie`. It does not create a `josie_v2` label.

## Issues

- The procedural fallback is clause assembly. It is varied by place, object, detail, hour, and adult age, and it is stiff where a slot meets a sentence. The teacher path is there for a rewrite pass.
- `<think>` does not carry the optional `[frame:]` tag from `docs/SKINNY.md`. The frame is only in `meta`, so the completion cannot lean on a tag.
- No API key was set here, so the 3000-per-id teacher run was not executed. The committed batch is the procedural sample.
