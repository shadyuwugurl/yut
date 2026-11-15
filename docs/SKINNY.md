# Skinny Spark template

The full root `chat_template.jinja` is a sourced catalog. A one-message `hi` render is about 76.5k `cl100k_base` tokens. This branch adds a second template that keeps the Spark wire and replaces the catalog with a short decision guide. The behavior of each id is trained from synthetic rows, not pasted into the prompt.

`chat_template.jinja` is unchanged. The skinny file is `templates/skinny/chat_template.jinja`, copied to `chat_template_skinny.jinja` at the repo root. Pass that file to `apply_chat_template`. Do not overwrite the full template with it.

## What the render still does

Official Spark tokens: `<｜start▁of▁sentence｜>`, `<｜end▁of▁sentence｜>`, `<|System|>`, `<|User|>`, `<|Bot|>`, `<|Tool|>`, plus `<think>` and `<arg_key>` / `<arg_value>`.

The conversation loop is the full template's loop: content blocks, reasoning from `reasoning_content` / `thinking` / `reasoning` (including a `{text: ...}` field), tool calls from `.arguments` or `.parameters` or `.input`, grouped tool results, `max_tool_arg_chars` / `max_tool_response_chars`, and the three tool-error warnings. `preserve_thinking=false` or `preserve_reasoning=false` drops past think text. Image blocks and unknown roles still raise.

Thinking still follows the live map. `reasoning_effort=off` or `enable_thinking=false` closes the think tag. Otherwise the prompt is invoked with `thinking_effort=low` on pathway s1 and `thinking_effort=high` on s2 or auto. Legacy kwargs, only when `mode` is unset: `low` / `soft` / `sensual` become mode `chat`; `medium` / `deep` become mode `deep`; `high` / `xhigh` become mode `extreme`; `mix` becomes mode `auto` and, if `construct` is unset, construct `kitbash`.

There is no keyword routing and no engram hook. A user message that says "code" does not lock `coder`. Locks come only from override kwargs.

## What the system block is

Gentle defaults, the orbit fundamentals, a `USE X FOR Y` guide, the hard walls, adaptive evolution, the short validation and terseness lines, and an on-the-fly rule. A forced override adds one lock line (`MODE LOCKED`, `CONSTRUCT LOCKED`, `PERSONA LOCKED`, `IDENTITY LOCKED`, `THEME LOCKED`, `AESTHETIC PRESET`, `PROTIUM LEVEL`). It does not paste a character card.

The guide lists every id in `docs/taxonomy_skinny.json`. A repeated spelling in two sections is two dials (`logic` the mode is not `logic` the construct). A leading `i` means channel `instruct`. A leading `x` means that construct at `effort_xultra`. `{REASON:einstein}` is construct `brainstorm`. `protium_level=einstein` is protium L8.

`python3 scripts/verify_skinny.py` renders plain chat, multi-turn, tools, tool errors, clipping, and each override, and prints the `cl100k_base` count. The `hi` render is required to stay inside 1,500–4,000 tokens. Measured with `cl100k_base` (the Spark tokenizer is not in the repo), a current `hi` render is 3,903 tokens, against about 76,512 for the full template.

## The spec

`docs/taxonomy_skinny.json` is the shared label list (`skinny-v1`). The stable key is `category` + `id`. Do not rename an id. Add an alias when a source name has to point at an id that already exists. `counts` and `merges` record how the full catalog was collapsed. `kwarg_map` is the template's override behavior, which is not the same thing as the DavidAU depth ladder (`reasoning_effort/effort_*`).

Near-duplicates that are one id:

- Instruct mode is channel `instruct`. The `i` prefix is not a second copy of every construct.
- `xomni`, `xdeeptree`, and the other `x*` names are that construct at `effort_xultra`.
- `spoon`, twin-turbo deep research, and the Qwen deep-research protocol are construct `research`.
- The Sternberg panel, `{REASON:einstein}`, and the twin-turbo brainstormer are construct `brainstorm`.
- Josie v2, R1, base, v6, v4o, and the OpenWebUI wording are identity `josie`.
- Protium L0 / Mortal is `thinking_effort/off`, not its own level.
- Turbo Brilliance V1, V2, Flash, Build2, the LFM2.5-24B menu, and both Power X12 menus are the same ids. The help-menu chrome is not a mode.
- Deckard is stance `deckard` (a dataset voice, no persona card). Jumbo is patch `jumbo`. The looping model is reasoning_mode `loop`.
- The exquisite craft spec is aesthetic `exquisite`, not an eighth palette.
- System 4, 5, and 6 are not in the template and are not in this spec.

`auto`, `neutral`, and `none` are included so an unset dial has a name. They are not extra v0.3 modes. v0.3's 25/30/20/33/8 are all still here. Added on top: pathway `auto`; mode `auto`; constructs `hyper`, `business`, `007`; persona `neutral` plus the ten DavidAU voices (`pkd`, `musk`, `joker`, `vader`, `quinn`, `neo`, `curie`, `stark`, `matlock`, `house`); identity `none` and `josie`; theme `none`; the effort, channel, protium, aesthetic, orbit, and agi ids.

## How a dataset row maps

Other agents writing under `datasets/` should label frames with these ids and no others. Aliases are accepted inputs (`spoon` → construct `research`); the stored label is the canonical id.

A row needs the situation, the frame, and a completion that inhabits the frame without announcing it. The system side can be this skinny template. Do not paste the full catalog back into the row.

```json
{
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
  }
}
```

Use a category only when the row is actually that thing. `reasoning_effort` is the DavidAU depth id (`effort_low` … `effort_xultra`) or null. It is not the legacy kwarg. `agi` is one of the `agi-*` ids when the row is a fusion, and the parts stay the underlying construct and persona ids. `orbit` is always on, so it is not a pick on the frame. `stance`, `patch`, and `reasoning_mode` are optional tags (`deckard`, `jumbo`, `loop`) for rows that are specifically those.

Inside `<think>`, a row may carry a private tag and nothing else about the machinery:

`[frame: pathway=s2|mode=code|construct=coder|persona=neutral|identity=none|theme=none|channel=reasoning]`

The visible answer does not name the frame.

Walls, same as the full template: `lolita_fashion` is never sexual; `age_regression` is an adult SFW headspace and ends before intimacy; `pet_play` is an adult with a person underneath; `erotica` and `influencer_nsfw` only in a clearly adult consensual frame; `anarchist` and `joker` are voices, not manuals for real harm.

`scripts/make_synth.py` still lists identities (`spy`, `imposter`, `hacker`) that are not in this spec. New rows should not use them.
