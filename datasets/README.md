# Datasets

Training rows for baking Sharp-Spark behavior into weights, so `chat_template_skinny.jinja` can replace the full catalog. Labels are skinny-v1 ids from `docs/taxonomy_skinny.json` (branch `cursor/spark-skinny-template-3cef`). An alias is an input name only. The stored label is `meta.category` + `meta.id`.

<!-- slice: constructs_personas -->

## Constructs and personas

`datasets/constructs_personas/` covers every skinny-v1 **construct** (33, including `hyper`, `business`, `007`) and **persona** (31, including `neutral` and the DavidAU voices `pkd`, `musk`, `joker`, `vader`, `quinn`, `neo`, `curie`, `stark`, `matlock`, `house`).

The user text never names the frame. The assistant inhabits it. A `<think>` block is used when the behavior is deliberative, and may end with the private `[frame: ...]` tag from `docs/SKINNY.md`. The saved row does not contain the full catalog or the teacher card.

Aliases resolved by the generator (not stored as ids): `spoon` and `deep_research` → `construct/research`; `einstein` → `construct/brainstorm`; `x007` / `agent_007` → `construct/007`; other `x*` names → that construct. `meta.alias_input` records the alias only when the generator was invoked with one.

```bash
python3 datasets/constructs_personas/validate.py --self-test
python3 datasets/constructs_personas/validate.py \
    datasets/constructs_personas/seed.jsonl \
    datasets/constructs_personas/sample/train.jsonl.gz \
    datasets/constructs_personas/sample/val.jsonl.gz
```

Full 3k-per-id run (teacher model, card text is not stored):

```bash
OPENAI_BASE_URL=https://host/v1 OPENAI_API_KEY=... MODEL=... \
python3 datasets/constructs_personas/generate.py --backend llm --n 3000 \
    --out datasets/constructs_personas/full --seed 11 --workers 8
```

Same scale with no key (procedural fallback):

```bash
python3 datasets/constructs_personas/generate.py --backend procedural --n 3000 \
    --out datasets/constructs_personas/full --seed 11
```

Adult NSFW rows exist only for personas and situations the taxonomy marks that way (`influencer_nsfw`, and adult flirt or negotiation elsewhere). No minors.

<!-- /slice: constructs_personas -->
