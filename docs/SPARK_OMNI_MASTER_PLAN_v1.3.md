# SPARK OMNI STACK — MASTER PLAN v1.3
2026-11-05 · Status: Phase-0 bootstrap + proposal shipped; 2026-11-05 audit shipped bootstrap v1.1
+ extract_taxonomy.py. Taxonomy v0.3 LOCKED 2026-11-07 (25/30/20/33/8). NEXT GATE: Q2–Q6, Q8.

One document. Three models. One queue. One pathway.
Source-of-truth detail lives in the pastes (runbook, seeds, scripts, contracts);
this file is the spine that references and sequences them.

---

## 0. HONEST VERDICT (read first)

| Component | Now (M5 32GB + Kaggle 30h/wk) | Later ("forever" track) | Not at this scale |
|---|---|---|---|
| Modified Spark text core (loops, YaRN, TurboQuant, Hydra, S3) | YES | | |
| Sharp-Spark v5 chat template (dynamic frame, no keyword routing) | YES — exists, verified | expand when taxonomy locks | |
| 265k SDG creative-writing dataset (queue + contracts + workers) | YES — 3.5–6 months wall-clock | | |
| LFM persona-furnace JSONL generator (10k–500k rows) | YES | | |
| Domain LoRAs + loop adaptation + Hydra + System-3 head | YES | | |
| Decision head (LiquidAI d1-2B, 2B) | YES | | |
| Weight baking: top constructs + personas (CPT/DPO) | YES — weeks, not months, if scoped | full 30/20/15 baking = 2–3 month CPT project | |
| Multimodal head Track A (fine-tune Spark-X2.5 MLX port / Qwen3.5-VL via mlx-vlm; TiRex-2 for time-series) | YES — partial: understanding, classification, retrieval, forecasting, embeddings | | photoreal video generation, high-fidelity mesh gen, music synthesis |
| Multimodal head Track B (distill Cosmos3-Edge + PE-AV) | NO | YES — multi-GPU-months; start only after Phase 3 ships | |
| Decision-head-governed S1/S2/S3 routing | YES | | |

Total active: ~7.5–8B (4B text + 1.5–2.5B multimodal + 2B decision + bridges).

---

## 1. FINAL ARCHITECTURE

```
[INPUTS]  text · image · video (2D/3D/mask/mesh/spatial) · audio/speech/music ·
          time-series · decision queries · streams (real-time)

                |
[MODIFIED SPARK-X2.6-4B — TEXT CORE]
  · 25 reasoning modes (10 S1 / 10 S2 / 5 S3) baked in weights + template
  · 30 constructs · 20 personas · 33 identities · 8 themes
  · looped forward (num_loops=2, layers 9–35)
  · YaRN RoPE factor 4.0 (full-attention layers only)
  · TurboQuant KV cache (6-bit K / 4-bit V, Hadamard)
  · Hydra heads (4 sequential draft heads, speculative decoding)
  · System-3 routing head (metacognitive)
                |
        [projector: 2-layer MLP, zero-init gate]
                |
[MULTIMODAL HEAD — Track A now / Track B later]
  · vision tower (frames, video, segmentation, 3D cues, spatial)
  · audio tower (speech, music, sound events)
  · time-series tower (TiRex-2 ~54M, streaming-native, prefix rows)
  · fusion layers (joint AV + temporal)
  Outputs: embeddings, classifications, segmentations, masks, forecasts,
           retrieval keys, lightweight synthesis/editing/healing/filling
                |
        [fused state: text hidden + media prefix]
                |
[DECISION HEAD — d1-style, ~0.2B]
  · bidirectional trunk (LFM2.5-Encoder-350M, frozen) + 2-layer head
  · typed heads: noul (yes/no) · choice (N-way) · score (ordinal bins)
  · one choice head each for: 25 modes, 30 constructs, 20 personas, 33 identities, 8 themes
  · confidence scalar + calibration (temperature, ECE penalty in loss)
  · action flags: search · heal · fill · generate · activate · route S1/S2/S3
  Output: probabilities per option — ZERO tokens generated
```

Why the decision head matters: it reads the same fused state the generator
sees, so it routes BEFORE generation. It cannot be talked out of a frame by
the prompt — it is not reading the prompt, it is reading the representation.

---

## 2. MODEL INVENTORY

| # | Model | Params | Source | Role |
|---|---|---|---|---|
| 1 | Spark-X2.6-4B (modified) | ~4B | XHToken/Spark-X2.6-4B + patched modeling_spark.py | text + personality core |
| 2 | Multimodal head Track A | 1.5–2.5B | Spark-X2.5 MLX multimodal port (mlx-vlm) or Qwen3.5-VL; TiRex-2 ~54M for TS | see/hear/forecast |
| 3 | Decision head | ~2B | LiquidAI d1-2B (LFM3 family, Oct 27 2026) fine-tuned on taxonomy typed Q&A | routing, calibration, activation |
| 4 | Multimodal encoder | ~1.6B | Meta PE-AV Large (Apache 2.0), frozen + LoRA heads; Cosmos3-Edge as future-prediction teacher | see/hear/embed/retrieve |
| 5 | Time-series tower | ~54M | TiRex-2 (xLSTM, streaming-native), fine-tuned on domain mixtures | forecast, stream |
| 6 | Projector bridge | ~50M | new, 2-layer MLP zero-init | align media prefix to text space |
| 7 | (Track B, later) full Cosmos3-Edge + PE-AV distill | 2–4B | teacher: Cosmos3-Edge | research track, gated behind Phase 3 |

---

## 3. TAXONOMY (STATUS: LOCKED v0.3, 2026-11-07 — 25/30/20/33/8, single source of truth = taxonomy.json from extract_taxonomy.py)

Latest numbers from you (canonical until you say otherwise):
  · 25 reasoning modes = 10 System-1 + 10 System-2 + 5 System-3
  · 30 constructs · 20 personas · 33 identities · 8 themes

LOCKED STRUCTURE (v1.1):
  · 25 reasoning modes = 10 System-1 + 10 System-2 + 5 System-3
    (S1 fast/reactive, S2 deliberate, S3 meta/inhibitory — Houdé/Taniguchi frame)
  · 30 constructs, split 15 S1 / 10 S2 / 5 S3 (each construct has a home system)
  · 20 personas — SHARED across all three systems
  · 33 identities — SHARED across all three systems
  · 8 themes — SHARED across all three systems
Existing Sharp-Spark modes (off/low/medium/high/soft/sensual/deep/extreme/
hotpot/mix) map into the 25-mode grid; the grid replaces them. Native
Spark none|low|high still governs actual thinking depth under the hood.

BUILD ORDER (user-specified): make the lists → design the switching →
stick in template → make datasets → train.

---

## 4. CHAT TEMPLATE

Base: Sharp-Spark v5.0.0 (dynamic frame — silent selection, no keyword
routing, explicit kwargs force frames, HELP safety-token, gentle graft,
stateless). File verified: parses, routes, renders official Spark skeleton.

Work waiting on taxonomy lock:
  · Expand FRAME CARD inventories to 30/20/15/10 + 25 modes
  · Regenerate override blocks + valid lists
  · Re-run verification suite (tools, tiers, grouping, generation prompt)

---

## 5. DECISION HEAD — SPEC (v1.1: d1-2B, not a custom 0.2B tower)

WHY THE CHANGE: Liquid shipped LFM3 on 2026-10-27. The family includes d1-2B —
a decision model answering typed questions (yes/no, choice, score, point, read,
estimate, pick) in ONE forward pass with calibrated probabilities, fine-tunable
on a single GPU. That is exactly the machine Section 5 originally specced by
hand, already built and battle-tested. We fine-tune it instead of reinventing it.

- Base: LiquidAI/d1-2B (v1). v2 swaps to d1-Omni-2B once multimodal lands.
- Fine-tune targets: choice heads over the locked taxonomy — 25 modes, 30
  constructs, 20 personas, 33 identities, 8 themes — plus noul/score probes
  for calibration ("is this response sycophantic? yes/no", "confidence 1–5").
- Loss: log loss per typed question + CE on taxonomy labels + ECE regularizer.
- Training data: synthetic typed Q&A generated FROM OUR OWN domain rows
  (the head cannot learn routing from generic sets). Few thousand per axis.
- Routing: confidence < τ and S2 logits dominate → escalate to slow path;
  S3 logits fire → inhibit / search / heal.
- Where it runs: alongside Spark on the M5 (d1-2B quantised ~1 GB) or Kaggle.
  Single-pass decisioning keeps latency near zero.
- Fallback if d1-2B underperforms on taxonomy routing: custom 0.2B tower on
  LFM2.5-Encoder-350M (original Section 5 spec) — keep as plan B.

---

## 6. MULTIMODAL HEAD

THE MIDDLE PATH (v1.1, replaces plain Track A): do not distill — RENT the
pretrained encoders and train heads on top.
- AV/spatial: Meta PE-AV Large (~1.6B, Apache 2.0) as the frozen joint
  audio-video encoder. Train on top: classification, segmentation, retrieval,
  cross-modal search heads (LoRA or small MLP heads). Feeds embeddings +
  prefix rows through the projector into Spark.
- Temporal/world signals: NVIDIA Cosmos3-Edge is the TEACHER, not the student.
  Use its predictions / features as supervision for the PE-AV-side temporal
  heads and for self-consistency rewards. Full distillation stays Track B,
  gated behind Phase 3 + real GPU budget (months, not weeks).
- Time-series: TiRex-2 (see Q7 answer in Section 13) — fine-tuned, streaming
  native, feeds prefix rows through the projector.
- RL: GRPO-style with verifiable rewards (forecast MASE/CRPS, retrieval
  Recall@K, segmentation IoU) on Kaggle 30h/wk.
- Delivers: understanding, classification, segmentation, masks, retrieval,
  forecasts, embeddings, streaming, lightweight editing/filling/healing.

---

## 7. DATA

### 7.1 SDG master runbook (265k creative-writing rows)
Architecture (from your runbook, unchanged): HF dataset repo as primary queue
(MC7ever/sdg-queue), GitHub mirror, Kaggle tertiary. Seven machines max.
Segments: theme 20k · persona voice 30k · specialist 25k · construct 50k ·
memories 120k · extras 20k. Contracts (5), Stage-A prompts (5), 21 persona
briefings, 1,070 human seeds (7 files). Worker: claim 25 → generate → verify
→ checkpoint 10 → push. Reaper: 2h tombstones. Final: dedupe by id, drop
verify-fails, 90/5/5 split.

Sequencing note: build_queue.py REQUIRES all 7 seed files present or the
count silently comes up short — verify wc -l before Phase 0 step 5 of the
orchestrator prompt.

### 7.2 LFM persona furnace (10k–500k rows, fast, single-machine)
Layered on the same queue OR run standalone against a local server:
- Generator system prompt: JSONL-only output, anti-hedge / anti-doomloop /
  anti-neutralize rules, persona-voice contracts, 5 genre buckets
  (horror 25 · ERP 25 · RP 20 · lit 20 · opinion 10)
- Verifier pass (same model or M1 Air second opinion): JSON verdict
  pass/regenerate/drop with reason codes
- Same triple-mirror queue mechanics; 10-row checkpoints
- Content boundary (standing, not negotiable): adult fiction between adults
  is in; sexualized minors, non-consent framed as titillation, and
  operational real-world harm instructions are out — the verifier enforces.

### 7.3 External datasets (~100, grouped)
TEXT: FineWeb-Edu, Dolma, SlimPajama, OpenHermes/UltraChat, ToolBench,
  GSM8K/MATH/MetaMath, LiveCodeBench, DPO mixtures, Banking77, HotpotQA.
VISION/IMAGE: LAION-5B/COCO-gated, COYO-700M, OpenImages, COCO, ADE20K,
  Cityscapes, ImageNet-1k/21k, Visual Genome, CC3M/12M, SBU, WIT, DataComp,
  SA-1B, SA-V, RefCOCO, VQA v2/GQA, TextVQA/DocVQA/ChartQA.
VIDEO/TEMPORAL/3D: Ego4D, Ego-Exo4D, Kinetics-400/600/700, ActivityNet,
  Something-Something V2, EPIC-KITCHENS, HowTo100M, WebVid-10M, Panda-70M,
  DAVIS, YouTube-VOS, HOT3D/HOI4D, BridgeData V2, DROID/Open-X, PointMotionBench,
  ScanNet/++ (gated), Matterport3D, Objaverse/XL, ShapeNet, ModelNet.
AUDIO/SPEECH/MUSIC: AudioSet, VGGSound, Clotho, AudioCaps, VoxCeleb 1/2,
  Common Voice, LibriSpeech/Light, GigaSpeech, MLS, FLEURS, VCTK, ESC-50,
  UrbanSound, NSynth, FMA, MUSDB, Speech Commands.
TIME-SERIES: Chronos mixtures, GIFT-Eval, ETT/Electricity/Traffic/Weather,
  PhysioNet, MIMIC-III/IV TS, M4/M5, UEA/UCR, PeMS, ERA5 subsets.
AV/OMNI/DOC: Daily-Omni, WorldSense, MMTA, CMU-MOSEI, EgoSchema, Video-MME,
  InfographicVQA, SlideVQA, remote-sensing TS (OlmoEarth-style).
RETRIEVAL: MTEB/BEIR, MS MARCO, Natural Questions, MSR-VTT/ActivityNet-Captions.
Synthetic support: Cosmos rollouts, InstructPix2Pix/MagicBrush editing pairs,
  Places inpainting, MUSDB separation, TS imputation sets.

Gated sets (LAION, COCO, ScanNet++, medical): request access NOW via HF UI —
approvals lag; substitute DataComp/CC12M if stalled.

### 7.4 Decision-head training data
Synthetic typed Q&A generated from your own domain rows: "Is this response
sycophantic? yes/no", "Which construct fits? choice of 30", "Confidence 1–5".
Source rows come from 7.1/7.2 outputs + domain LoRA data. Few thousand per
domain; regenerate per taxonomy lock.

---

## 8. TRAINING PATHWAY (staged, hardware-mapped)

| Stage | What | Where | Time |
|---|---|---|---|
| 0 | Repo init + queue build + seed-file verification (wc -l on all 7) | M5 | 1 evening |
| 1 | SDG + furnace workers spinning (runs in background for months) | fleet | 3.5–6 mo wall |
| 2 | Text core: loop LoRA, Hydra heads, System-3 head | M5 | 15–25 h |
| 3 | Domain LoRAs (16-ish, grouped A/B/C) | M5 | 8–12 h |
| 4 | Decision head on frozen fused state | M5 | 2–3 h |
| 5 | Weight baking: top 10 constructs + 5 personas (CPT/DPO) | Kaggle 30h/wk | 2–3 wks |
| 6 | Multimodal Track A fine-tune + projector | Kaggle (+M5 cache/evals) | 2–3 wks |
| 7 | Quant + package + calibration re-fit | M5 | 2 h |
| 8 | Eval suite | M5 + Kaggle | 1–2 wks |
| 9 | Track B distillation scoping (only after Stage 5) | — | gated |

Stages 1 and 2–4 run in parallel: workers generate data while M5 trains.

---

## 9. EVALS / BENCHMARKS / TESTS

BENCHMARKS (20+): MMLU-Pro, GPQA, BBH, MuSR, MATH-L5, GSM8K, AIME,
HumanEval, MBPP, LiveCodeBench, SWE-bench Lite, RULER, LongBench, TruthfulQA,
HaluEval, SimpleQA, τ-bench, AgentBench, ToolBench, Daily-Omni, WorldSense,
Video-MME, GIFT-Eval, Chronos zero-shot.

EVALS (30+): SycophancyBench, EQ-Bench, AGC-Bench, MIDA, BBQ, hedging
accuracy, human-likeness, persuasion shift, anti-corporate-speak, persona
consistency over long context, mode-switch accuracy under conflicting signals,
S1/S2 correctness under time pressure, S3 routing accuracy, retrieval Recall@K,
noisy-modality retrieval, AV-conditioned forecast, streaming latency,
decision ECE/Brier, routing confusion matrix, inhibition success, construct
activation, identity consistency, theme adherence + 12 domain probes.

TESTS (15+): held-out RP, emotion, empathy, persuasion, deception detection,
bias refusal, hedging appropriateness, human tone, anti-sycophancy under
pressure, science reasoning, Rust/Swift/Jinja coding, math word problems,
niche knowledge, decision calibration, S3 routing, multimodal retrieval,
time-series forecast, 128k long-context retrieval, looped-reasoning depth,
Hydra acceptance length.

Every-20k-row audits during generation: 500-row stratified samples, 1–5
scoring on voice/density/originality/instruction/genre; <3.5 avg → pause
category, revise contract.

---

## 10. HARDWARE PLAN

| Machine | Role | Notes |
|---|---|---|
| M5 MBP 32GB | primary: queue, workers, text LoRAs, heads, quant, evals | charge cap 80%, external fan in clamshell |
| M1 Air 8GB | verifier second-opinion | catches same-model blind spots |
| Kaggle 2×T4 16GB×2 | 30h/wk: multimodal fine-tune, weight baking | session dies = reaper handles rows |
| RunPod 4090 $10 | one-off bursts | hard stop 18h or $10; manual only, no bootstrap profile |
| M4 Air 16GB (school) | secondary worker | BATCH_SIZE 12 |
| 2016 Intel MBP | do not deploy | |

Local-first always; rent only what the stage demands.

---

## 11. KILL CRITERIA (from runbook, kept)

- Inline pass rate <60% for 500 consecutive rows → stop, revise contracts
- Median row length <300 tokens for 500 consecutive → check stops/max_tokens
- Dedup rate >25% → Stage-A diversity insufficient, raise temperature
- Decision ECE >0.1 after calibration fit → re-collect typed data, re-fit
- Mode/construct activation accuracy <70% on held-out → retrain decision head
- HF repo >2GB → shard done.jsonl to S3, queue stays on HF

---

## 12. STANDING CONSTRAINTS (mine, unchanged)

1. age_regression stays SFW-only comfort mode; no sexualized regressed/minor
   framing anywhere in template, datasets, or generated rows.
2. lolita = fashion subculture identity, non-sexualized.
3. Hacker/spy/imposter/deception data stays fiction-voiced: no operational
   real-world harm instructions in any generated row.
4. Furnace + SDG verifiers enforce 1–3 automatically with drop codes.

---

## 13. OPEN QUESTIONS (the gate — answer these and we start)

Q1. CLOSED 2026-11-07 — taxonomy v0.3 LOCKED: 25 modes (10 S1/10 S2/5 S3),
    30 constructs, 20 personas, 33 identities, 8 themes. Template + proposal
    already agree; this plan synced to match.
Q2. Which 10 constructs + 5 personas get weight-baked first? (rest stay
    template + decision-head)
Q3. Base weights: do you have Spark-X2.6-4B BF16 (and the GGUF) local already?
    Which files, which path?
Q4. Track A multimodal confirmed as the build? (fine-tune Spark-X2.5 MLX port
    / Qwen3.5-VL now; Cosmos3-Edge+PE-AV distill gated behind Phase 3 + GPU)
Q5. Decision head trunk: LFM2.5-Encoder-350M (recommended, d1 pattern) or a
    bidirectional adapter on Spark's final hidden (keeps everything one model)?
Q6. HF handle for the dataset repos — pick a name so I can swap it into the
    runbook + worker scripts. Also: request gated access now (LAION/COCO/
    ScanNet++) — yes/no?
Q7. CLOSED 2026-11-07 — TiRex-2. Speed-first call: ~38–54M vs 120M params is
    ~2–3x faster inference AND ~2–3x faster/cheaper fine-tuning on the Kaggle
    30h/wk budget; xLSTM streaming-native matches the real-time streams input
    class; the plan fine-tunes on domain mixtures anyway, so Chronos-2's
    zero-shot edge is bought back with training. Chronos-2 stays in the eval
    list as a zero-shot benchmark only. Revisit ONLY if multivariate 8k-ctx
    forecasting becomes a core workload.
Q8. Definition of done for v1: I recommend (a) text core + template + decision
    head running locally end-to-end. Multimodal lands in v2. Agree?
