# DRIFT & SYNC NOTES — Spark Omni stack (audit 2026-11-05)

## Maths — VERIFIED PASS
- Human seeds: 40+30+20+20+360+150+450 = 1,070 across 7 files (matches proposal §4)
- Stage-A expansion targets: 500+300+200+300+100 = 1,400 (matches bootstrap Phase 2)
- Queue: 20k+30k+25k+50k+120k+20k = 265,000 (matches bootstrap Phase 3 gate exactly)
- Taxonomy in template: 25 modes (10 S1/10 S2/5 S3) + 30 constructs (15/10/5)
  + 20 personas + 33 identities + 8 themes — counted programmatically, all match v0.3
- sys_of_mode covers all 25 modes; template renders clean (default + forced-frame test)

## FAILS — fix these
1. MASTER_PLAN §3 + §1 diagram say "15 identities · 10 themes" — stale.
   Template + proposal are v0.3: **33 identities · 8 themes**. Sync the plan.
2. MASTER_PLAN §5 fine-tune targets say "15 identities, 10 themes" → 33, 8.
3. HONEST VERDICT table says "Decision head (d1-style, 0.2B)" — stale. §5 already
   upgraded to LiquidAI d1-2B (2B). Total params: "~6–7B" → "~7.5–8B"
   (4B text + 1.5–2.5B multimodal + 2B decision + ~0.1B bridges).
4. Verdict table Track A says "Chronos-2 for time-series" — everything else
   (proposal §2, plan §6, inventory #5) says **TiRex-2**. Pick one (recommend TiRex-2, close Q7).
5. Plan §10 hardware: "M5 Air 16GB (school), BATCH_SIZE 15" — bootstrap + proposal §6
   say **M4 Air, batch 12**. Sync plan.
6. bootstrap.sh v1.0 arg parsing crashes with two flags — FIXED in v1.1.
7. bootstrap.sh v1.0 never checked scripts/ exist — FIXED in v1.1.
8. bootstrap.sh v1.0 `git push` to HF fails on a fresh box (no git creds) — FIXED
   in v1.1 (token remote fallback; token sits in sdg/.git/config — personal machine only).
9. verifier profile MODEL_PORT pointed at :8000 — FIXED in v1.1 (→ :8002, its 3B slot).

## OPEN GATE — needs YOU (plan §13)
- Q1 taxonomy lock: confirm **v0.3 = 25/30/20/33/8** (template + proposal already agree)
- Q2 which 10 constructs + 5 personas get weight-baked first
- Q3 Spark-X2.6-4B BF16 + GGUF local? exact path?
- Q4 Track A confirmed? (fine-tune Spark-X2.5 MLX port / Qwen3.5-VL; Track B gated)
- Q5 decision trunk: d1-2B fine-tune (recommended) vs custom 0.2B tower
- Q6 gated dataset requests (LAION/COCO/ScanNet++) — sent?
- Q7 TiRex-2 vs Chronos-2 — recommend TiRex-2
- Q8 v1 = text core + template + decision head local end-to-end — agree?

## New questions from this audit
- personas.json is 1 line — does that single JSON contain all 21 briefings? (can't verify here)
- Does worker.py already handle KAGGLE=1 / vLLM-AWQ mode? (bootstrap assumes it)
- Pin mlx-lm version in Phase 0 — the template needs raise_exception + full Jinja support
- Verifier machine: v1.1 lets it run Phase 2–3 off its 3B, but consider a --pull-only
  mode later (clone the queue instead of building it)
- RunPod 4090 is in the fleet but has no bootstrap profile — fine, it's manual one-off,
  but say so in §10
