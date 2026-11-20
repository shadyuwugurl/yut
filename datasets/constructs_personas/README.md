# Constructs and personas

Skinny-v1 labels. Every construct and persona in `taxonomy_slice.json` (copied from `docs/taxonomy_skinny.json` on `cursor/spark-skinny-template-3cef`). `hyper`, `business`, and `007` are included. So are `neutral` and the ten DavidAU voices.

## Row

```json
{
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "<think>\n...\n[frame: pathway=s2|mode=code|construct=coder|persona=neutral|identity=none|theme=none|channel=reasoning]\n</think>\n\n..."}
  ],
  "meta": {
    "category": "construct",
    "id": "coder",
    "alias_input": null,
    "pattern": "single",
    "switch": null,
    "blend": null,
    "frame": {
      "pathway": "s2",
      "mode": "code",
      "construct": "coder",
      "persona": "neutral",
      "identity": "none",
      "theme": "none",
      "thinking_effort": "high",
      "reasoning_effort": null,
      "channel": "reasoning",
      "protium": null,
      "aesthetic": null,
      "agi": null
    },
    "think": true,
    "source": "seed",
    "nsfw": false,
    "taxonomy": "skinny-v1",
    "uid": "cp-construct-coder-single-..."
  }
}
```

`pattern` is `single`, `multi`, `switch`, `blend`, or `stay`. `switch` is null unless the pattern is `switch` (`from`, `to`, categories, `at_user_turn`). `blend` is null unless the pattern is `blend` (lead id first). When the blend is one of the skinny `agi-*` fusions, `frame.agi` is that id and the parts stay the underlying construct and persona ids.

A short system line (`You are a helpful assistant.` and two others) is present on some rows. The full catalog is not.

## Files

| Path | What |
| --- | --- |
| `seed.jsonl` | Authored exemplars, 20 per id except `ai_engineer` at 19 (templates in `cp/specs.py`, `cp/specs_personas.py`, situations in `cp/worlds.py`). Not model output. |
| `sample/train.jsonl.gz`, `sample/val.jsonl.gz` | Procedural sample, target 100 per id, 5% val. Near-duplicate filtered against the seeds. `drabble` landed at 86 and `holodeck` at 98; every other id hit 100. |
| `sample/counts.json` | Row counts. |
| `taxonomy_slice.json` | Canonical ids, aliases, descriptions. |
| `generate.py` | Procedural backend and OpenAI-compatible teacher backend. |
| `validate.py` | Schema, role order, canonical ids, trigger leaks, adult-only NSFW. |

## Generate

```bash
python3 datasets/constructs_personas/generate.py --emit-seeds \
    --out datasets/constructs_personas/seed.jsonl --seed 11

python3 datasets/constructs_personas/generate.py --backend procedural --n 100 \
    --out datasets/constructs_personas/sample --seed 11 \
    --avoid datasets/constructs_personas/seed.jsonl

OPENAI_BASE_URL=https://host/v1 OPENAI_API_KEY=... MODEL=... \
python3 datasets/constructs_personas/generate.py --backend llm --n 3000 \
    --out datasets/constructs_personas/full --seed 11 --workers 8

python3 datasets/constructs_personas/generate.py --backend procedural --n 3000 \
    --out datasets/constructs_personas/full --seed 11

python3 datasets/constructs_personas/generate.py --id spoon --n 20 \
    --out /tmp/spoon.jsonl --backend procedural
```

`--id spoon` stores `meta.id = research` and `meta.alias_input = spoon`.

Default `--n` is 3000. The procedural backend stops at the near-duplicate ceiling instead of emitting copies. The teacher backend is the one that can actually fill 3000 distinct rows per id.

## Checks

User text must not contain the row's ids, snake_case aliases, or routing words (`construct`, `persona`, `frame card`). Visible assistant text must not announce the frame. A private `[frame: ...]` tag is allowed only as the last line of `<think>`. NSFW rows are adult-only. `anarchist` and `joker` refuse operational harm instead of teaching it. `007` isolates a failed tool call and does not repeat it. `house` names a discriminating test and does not write a dose.
