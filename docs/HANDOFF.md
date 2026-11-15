# Session Handoff — Pure Upstream Ornith-1.5-9B Chat Template Alignment

**Date:** Sat Nov 07 2026  
**Repo:** `/home/ubuntu/azrael/chat_template`  
**Operator Directive:** Replace `chat_template.jinja` with 100% byte-for-byte pure upstream `ornith-ai/Ornith-1.5-9B` template (sha256 `9dd2fbd270feaa1fbef2d4f634d7887c9c506e3bde140f8e7351c8944e8fd235`), passing Azrael identity, 5-pass priming, and hardening dynamically as caller system messages.

---

## 1. What Was Executed

### Task 1: Overwrite `chat_template/chat_template.jinja`
- Copied exact upstream `ornith-ai/Ornith-1.5-9B` `chat_template.jinja` (150 lines).
- Verified `sha256sum /home/ubuntu/azrael/chat_template/chat_template.jinja`:
  `9dd2fbd270feaa1fbef2d4f634d7887c9c506e3bde140f8e7351c8944e8fd235` (exact match).
- All MiMo tool wire and hardcoded prose blocks removed from the Jinja file.

### Task 2: Regenerate `chat_template/chat_template_oneline.txt`
- Minified using `scripts/minify_jinja.py`:
  `7593 B` -> `5988 B` (21.1% reduction).
- Verified 100% render parity between full and minified templates across all test fixtures.

### Task 3: Authoritative Verification Gate (`scripts/verify.py`)
- Pinned SHA256 match against upstream `9dd2fbd2...`.
- Reasoning wire:
  - `enable_thinking=True`: gen prompt ends with `<|im_start|>assistant\n<think>\n`
  - `enable_thinking=False`: gen prompt ends with `<|im_start|>assistant\n<think>\n\n</think>\n\n`
  - Assistant turn with reasoning: `<|im_start|>assistant\n<think>\n{reasoning}\n</think>\n\n{content}<|im_end|>\n`
  - Assistant turn with empty reasoning: `<|im_start|>assistant\n<think>\n\n</think>\n\n{content}<|im_end|>\n`
  - Content fallback: embedded `<think>` parsed into reasoning content.
- Tool wire (Pure Ornith):
  - System head renders `# Tools\n\nYou have access to the following functions:\n\n<tools>...\n</tools>...`
  - Line-delimited XML tool calls:
    `<tool_call>\n<function=foo>\n<parameter=bar>\nbaz\n</parameter>\n</function>\n</tool_call>`
  - In-user tool responses:
    `<|im_start|>user\n<tool_response>\n{tool_result}\n</tool_response><|im_end|>\n`
  - Consecutive tool responses bundled in a single `<|im_start|>user` turn.
- Dynamic caller system message:
  - Caller system message (`messages[0]`) passes through cleanly to `<|im_start|>system` turn (either standalone or appended after `# Tools` definitions).
- Output: `32 passed, 0 failed` (standalone); `38 passed, 0 failed` (with `--ornith`).

### Task 4: Documentation Alignment
- `chat_template/README.md` updated with exact upstream specs, Qwen3 XML tool wire, and dynamic system message contract.
- `chat_template/HANDOFF.md` updated to document the pure Ornith transition.

### Task 5: Pipeline Workorder Alignment (`traces/WORKORDER-SYMBIOSE-DATA-PIPELINE.md`)
- Aligned template contract to exact upstream Ornith template (sha256 `9dd2fbd2...`).
- Wire table updated: tool calls use `<tool_call>\n<function=...>\n<parameter=...>`, tool responses use `<|im_start|>user\n<tool_response>\n...` with token IDs `248066` (`<tool_response>`) and `248067` (`</tool_response>`).
- Loss-masking algorithm (`tokenize_and_mask_multiturn`) updated with assistant prefix scanning and hard verification that tool response tokens have `labels == -100`.

### Task 6: Downstream Tests & Parity
- `python3 scripts/verify.py` → **32 passed, 0 failed** (exit code 0).
- `python3 -m pytest azrael_trace_alignment_v2/tests/test_template_compat.py` → **27 passed, 0 failed** (exit code 0).
- `npm test` in `/home/ubuntu/azrael` → **10 test files passed, 134 tests passed** (exit code 0).

---

## 2. Verification Summary Table

| Test Suite | Command | Result | Exit Code |
|---|---|---|---|
| Chat Template Verification Gate | `python3 scripts/verify.py` | 32 passed, 0 failed | 0 |
| Chat Template vs Reference Ornith | `python3 scripts/verify.py --ornith ...` | 38 passed, 0 failed | 0 |
| Trace Alignment Compat Suite | `python3 -m pytest azrael_trace_alignment_v2/tests/test_template_compat.py` | 27 passed, 0 failed | 0 |
| Azrael Harness Vitest Suite | `npm test` | 10 passed, 134 passed | 0 |
