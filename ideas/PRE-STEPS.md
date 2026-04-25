---
type: meta
title: "Pre-Step Catalog — Cheap Intuition Tests Before Full Implementation"
created: 2026-04-24
updated: 2026-04-24
tags:
  - meta
  - ideas
  - pre-step
status: evergreen
---

# Pre-Step Catalog

For every active / parked / future-work idea, a **cheap intuition test we can run in hours, not weeks** that either confirms the idea's core premise or kills it before we commit engineering time.

**The discipline:** a pre-step must be (a) cheap (≤1 GPU-day wall-clock), (b) specific (a concrete measurement, not exploration), (c) falsifiable (pre-specified kill criterion), (d) grounded in existing infrastructure (reuse checkpoints, data, code), (e) pre-specified success (what would justify committing to the full plan).

Think of pre-steps as **smoke tests for hypotheses**. Many of Wave 1's plans (JumpReLU SAE, Layer-Asymmetric probe, ThinkRouter τ) are already pre-steps for larger ideas. This doc surfaces pre-steps across the full idea catalog.

## Priority order (cost-adjusted expected information)

Pre-steps sorted by "bits-of-decision-info per GPU-hour":

| # | Idea | Pre-step | Cost | Kill / confirm signal |
|---|---|---|---|---|
| 0 | **KV-norm-at-answer-position probe** (Christopher's diagnostic, 2026-04-24 meeting) | Instrument per-position latent-KV norm at answer-attention point on V2 bf16 + GPT-2 CODI | ~0.5 GPU-hr | **Tests latent-KV-disappears hypothesis; gates W3.5 design choice + frames the SPAR writeup mechanistic story** |
| 1 | W1.1 JumpReLU SAE (already queued) | SAE on existing V2 bf16 KV dumps | ~1 GPU-hr | pre-step for **Latent Scratchpad** |
| 2 | Autoresearch 2.0 | Manual mechanism-to-harness translation on 1 recent paper | ~2 CPU-hr | Tests meta-feasibility |
| 3 | Cross-Precision Determinism | 4-seed reproducibility study on V2 bf16 vs V2' fp32 | ~2 GPU-hr | Isolate basin drift from seed variance |
| 4 | MoCo-style Cross-Batch InfoNCE | Compute effective batch size for W2.2 as configured | ~0 GPU-hr | 1-line arithmetic check |
| 5 | Attention Composite-Block Jacobian | Measure ρ(J) per block on 1 V2 bf16 forward | ~0.5 GPU-hr | Eigenvalue distribution |
| 6 | Latent Scratchpad (W3.5) | GPT-2 green-smoke stage A only (1 epoch, no Stage B) | ~8 GPU-hr | Gate trainability |
| 7 | mHC Retrofit | Low-rank mHC-as-adapter on Qwen3-4B single layer | ~4 GPU-hr | Feasibility of retrofit |
| 8 | Dense Per-Step Latent Supervision | Analyze W2.4b SIM-CoT run, per-position info gain | ~2 CPU-hr | Info-gain calc on done run |
| 9 | Per-Token Continuous Thought | Replicate Quiet-STaR at GPT-2 for 1 epoch, measure thought-position distribution | ~12 GPU-hr | Where do thoughts help? |
| 10 | Continuous-Thought Pretraining | Continued-pretraining (not from-scratch) on GPT-2 with latent tokens for 1k steps | ~6 GPU-hr | Can latent tokens emerge without full restart? |
| 11 | Wasserstein OT on Latent CoT | Toy 2D synthetic mixture; Sinkhorn on latent trajectories | ~0.5 CPU-hr | Proof of concept |
| 12 | Continuous-Solver Variable Compute | Neural ODE on GPT-2-micro; adjoint method gradient check | ~4 GPU-hr | Adjoint stability at tiny scale |

---

## Detailed pre-steps by idea

### 0. KV-norm-at-answer-position — Christopher's diagnostic (HIGHEST PRIORITY)

**Pre-step: KV-NORM-PROBE**

Instrument the V2 bf16 Qwen3-4B and GPT-2 CODI checkpoints to log the **L2 norm of latent-position keys/values at the answer-token attention point** for 100 GSM8k examples each. Christopher's hypothesis (2026-04-24 meeting): the "latent KV disappears" before the answer token attends — explains the scaling cliff.

**Concrete measurements:**
- For each of M=8 latent positions per example: at answer-token forward pass, compute `||K[latent_pos]||_2` and `||V[latent_pos]||_2` per attention head per layer.
- Aggregate: per-position mean KV-norm at answer-attention.
- Compare GPT-2 (works) vs Qwen3-4B (fails).

**Three diagnostic cases:**
1. **KV-norm uniform high at both scales:** "latent KV disappears" hypothesis is **wrong**. Bandwidth isn't the failure; some other mechanism is. Sharply changes the SPAR mechanistic narrative.
2. **KV-norm decays monotonically (latest has most), worse at 4B:** CODI is throwing away history. Recent latents carry; older ones don't. **W3.5 design:** scratchpad emissions at recent positions augment what's already there.
3. **KV-norm uniformly low at 4B but high at GPT-2:** CODI's latent positions cannot carry bandwidth at scale at all. **W3.5 design:** scratchpad must do ALL the carrying, not augment. Length penalty + information-density reward becomes the primary objective.

**Cost:** 0.5 GPU-hr (pure inference, 100 examples).

**Go/no-go:** this pre-step doesn't kill anything — it CHOOSES between three different W3.5 designs. Run before any W3.5 training.

**Tracked in:** `wiki/ideas/Latent Scratchpad.md` § "COMPRESSION + KV-bandwidth framing." Christopher's diagnostic is the most direct test of the bandwidth hypothesis.

---

### 1. Latent Scratchpad (W3.5) — promoted-to-plan

**Pre-step: W3.5-GREEN-SMOKE-STAGE-A-ONLY**

Before committing to the full 72-hour Qwen3-4B Stage A + Stage B training, run ONLY Stage A of the W3.5 plan on GPT-2 for 1 epoch and measure gate behavior.

**Concrete measurements:**
- Gate activation mean after 1 epoch of Stage A (`bias=-2.0` init, lambda_sparsity=0.1, soft gate).
  - Expected: 0.05 < mean < 0.25 (gate is firing sometimes but not collapsing to always-fire).
  - Kill: mean < 0.01 (gate dead) or mean > 0.9 (gate degenerate).
- Gate activation variance per position.
  - Expected: variance > 0.1 (gate fires differentially based on context).
  - Kill: variance < 0.01 (gate uniform across positions).
- Whether the note_head emits anything sensible when forced to fire.
  - Force `gate = 1` for a test batch at step 4; inspect emitted tokens.
  - Expected: vocabulary includes at least 20% non-punctuation non-stopword tokens.
  - Kill: emits only `.`, `The`, `is`, `0` at >90% rate.

**Cost:** ~8 GPU-hours on GH200 (1 epoch at GPT-2 scale with aux-decoder). Reuses SIM-CoT GPT-2 warm-start checkpoint.

**Go/no-go:** if ALL three pass → proceed to Stage B. If any fails → retire or rethink before committing Qwen3-4B compute.

**Tracked in:** `plans/wave3/W3.5_latent_scratchpad.md` Step 7 (green-smoke gate).

---

### 2. Manifold-Constrained Residual Stream (mHC) — parked

**Pre-step: MHC-AS-LOW-RANK-ADAPTER**

Before committing to from-scratch pretraining, test whether mHC's Birkhoff-polytope-constrained Hyper-Connection can be retrofit as a LoRA-style adapter on a single Qwen3-4B attention block.

**Concrete measurements:**
- Add narrow (N=2 widening) + low-rank Hyper-Connections at ONE transformer block in Qwen3-4B V2 bf16.
- Train adapter alone on CODI objective for 1k steps.
- Measure: does the doubly-stochastic constraint (Sinkhorn projection) survive LoRA decomposition, or does SVD of `BA` break the Birkhoff property?
- Measure: does the adapted block show richer latent content per F4 KV-ablate Δ?

**Cost:** ~4 GPU-hours. Reuses existing V2 bf16 base.

**Go/no-go:** if SVD preserves Birkhoff AND F4 Δ grows by ≥5pp → file as active mHC-retrofit idea, promote to sketched-plan. If SVD breaks Birkhoff or F4 unchanged → mHC truly requires from-scratch pretraining, keep parked.

---

### 3. Cross-Precision Determinism Investigation — future-work

**Pre-step: SEED-VARIANCE-ISOLATION**

The most reproducible unexplained finding in our project: V2 bf16 and V2' fp32 produce **different digit attractors** despite identical recipes. Before any investigation, separate the cross-precision effect from seed-to-seed variance.

**Concrete measurements:**
- Retrain V2 bf16 with 4 seeds (42, 11, 73, 137) on our existing config; same for V2' fp32 with 4 seeds.
- Compute KV-PCA basin-distance matrix (8×8).
- Expected patterns:
  - Block-diagonal structure (bf16-bf16 close, fp32-fp32 close, bf16-fp32 far) → cross-precision effect is systematic, worth investigating.
  - Random structure → seed variance dominates; the bf16-vs-fp32 story is overstated.
  - Bimodal (half of bf16 seeds look like fp32) → there are 2 basins, precision is a weak prior, not the cause.

**Cost:** ~2 GPU-hours per retraining × 8 = 16 GPU-hours. Long but cheap per-experiment.

**Go/no-go:** block-diagonal structure → promote to active investigation. Else retire the "cross-precision determinism is weird" narrative.

---

### 4. MoCo-Style Cross-Batch InfoNCE — future-work

**Pre-step: BATCH-SIZE-ARITHMETIC**

Trivial but necessary. Before implementing MoCo queue, verify whether W2.2 V3 composite actually has a batch-size problem.

**Concrete measurements:**
- Read the W2.2 config: `per_device_train_batch_size=4 * gradient_accumulation_steps=8 = 32` at optimizer step.
- BUT InfoNCE runs on the per-forward-pass batch of 4.
- Compute bound: `log(4) ≈ 2 bits` lower bound on mutual information — likely too small to be useful.
- Check: is there a cheap way to aggregate latents across accumulation steps without breaking gradient flow?

**Cost:** 0 GPU-hours. 10-minute analysis.

**Go/no-go:** if batch size ≥ 32 at InfoNCE computation time → no need for MoCo. Else → implement MoCo queue as W2.2 fallback.

---

### 5. Attention Composite-Block Jacobian — future-work

**Pre-step: SINGLE-FORWARD-SPECTRUM**

W2.3 Parseval retracts per-projection matrices (Q/K/V/O individually). Composite-block spectrum is unexplored. Before committing to a Parseval-composite branch, just measure the composite spectrum once.

**Concrete measurements:**
- Single forward pass on V2 bf16 Qwen3-4B with 1 GSM8k example.
- At block 6 (middle), compute the Jacobian of the composite attention+MLP block via power iteration (10 steps).
- Measure top-3 singular values.
- Compare to the product of top-3 per-projection singular values.

**Cost:** 0.5 GPU-hours.

**Go/no-go:** if composite top-3 ≠ product-of-projection top-3 by >20% → Parseval at composite level is a distinct intervention, worth its own branch. Else → W2.3 per-projection Parseval is sufficient.

---

### 6. Autoresearch 2.0 — future-work

**Pre-step: MANUAL-TRANSLATION-ON-1-PAPER**

Before building meta-autoresearch infrastructure, verify the core premise: **can we reliably translate a paper's mathematical formulation into harness-compatible config?**

**Concrete measurements:**
- Pick one recent paper (`SeLaR` is a good candidate — we already ingested it, relatively simple).
- By hand: extract the paper's mathematical formulation (entropy gate + contrastive repulsion), translate into pseudocode against our harness's `latent_tap.py`, produce a working config yaml.
- Measure: how long does it take? What parts required human judgment? What parts would an LLM agent get wrong?

**Cost:** 2 CPU-hours. Already partially done during W1.3b SeLaR planning.

**Go/no-go:** if manual translation is <30% human judgment → an LLM agent can probably do this with specific prompting → Autoresearch 2.0 is feasible, build it. If >60% human judgment → the meta-approach is too speculative, keep as one-off per-paper translation.

---

### 7. Wasserstein OT on Latent CoT — future-work

**Pre-step: TOY-SYNTHETIC-SINKHORN**

Before implementing Wasserstein regularization at Qwen3-4B, test whether Sinkhorn converges on synthetic 2D mixture data that mimics the latent-trajectory geometry.

**Concrete measurements:**
- Generate 200 synthetic 2D mixture distributions (3 Gaussians each) as stand-in for per-example latent trajectories.
- Compute pairwise Sinkhorn distances with ε ∈ {0.01, 0.1, 1.0}.
- Measure: convergence iterations, numerical stability at low ε (closest to Wasserstein).

**Cost:** 0.5 CPU-hours, pure numpy.

**Go/no-go:** if Sinkhorn converges cleanly at ε=0.1 → Wasserstein regularization is computationally feasible → promote to sketched plan. Else → Wasserstein on latent CoT requires more sophisticated transport (Gromov-Wasserstein? entropic regularization with multi-scale?), stay future-work.

---

### 8. Per-Token Continuous Thought — future-work

**Pre-step: QUIET-STAR-REPRO-POSITION-DISTRIBUTION**

Before designing a Quiet-STaR × COCONUT hybrid, verify that Quiet-STaR itself actually produces useful thoughts at every position (or does it degenerate to "useful only at rare positions"?).

**Concrete measurements:**
- Replicate Quiet-STaR at GPT-2 scale for 1 epoch on GSM8k.
- Measure: thought-token attribution per position (which positions' thoughts actually improve answer likelihood?).
- Measure: thought-vocabulary distribution (are thoughts semantic or formatting?).

**Cost:** 12 GPU-hours. Heaviest pre-step but high info.

**Go/no-go:** if ≥30% of positions have thoughts that causally improve answer → per-token thinking IS the win → promote W3.3 to active. If ≤5% of positions have useful thoughts → per-token is wasteful → re-scope to sparse-thought architecture (converges back to Latent Scratchpad territory).

---

### 9. Continuous-Thought Pretraining — future-work

**Pre-step: WARM-START-CONTINUED-PT**

Instead of from-scratch continuous-thought pretraining, test whether continued-pretraining on an already-trained GPT-2 with injected latent tokens produces anything interesting.

**Concrete measurements:**
- Load `zen-E/CODI-gpt2` or similar.
- Continue pretraining for 1k steps on OpenWebText with M=4 latent tokens injected every 50 natural tokens.
- Measure: perplexity on held-out text (does continuous-thought injection hurt language modeling?).
- Measure: F3 entropy on injected latent positions after continued PT.

**Cost:** 6 GPU-hours.

**Go/no-go:** if perplexity holds within 5% AND F3 per-position entropy >1 bit after continued PT → warm-start continuous-PT is a cheap path to continuous-thought pretraining → promote W3.2 Pause-PT to active (as continued-PT variant, not from-scratch). If PT hurts perplexity or latents collapse → from-scratch is genuinely required, keep W3.2 as full plan.

---

### 10. Dense Per-Step Latent Supervision — future-work

**Pre-step: ANALYZE-W2.4B-AFTER-ITS-DONE**

Don't design a new branch; INSTEAD analyze the W2.4b SIM-CoT Phase 2a run once it completes. SIM-CoT's aux decoder IS dense per-step supervision; W2.4b will tell us how useful it is.

**Concrete measurements:**
- Post-W2.4b: per-position, compute mutual information I(aux-decoder-output; gold-step-tokens).
- Measure: at which positions is MI highest? Is there a pattern (first position? boundary positions? random)?
- Estimate: what would a more efficient dense-supervision scheme (emit only at high-MI positions) look like?

**Cost:** 2 CPU-hours of analysis, 0 new GPU.

**Go/no-go:** this pre-step is FREE (just analyzing an experiment we're already running). Output informs whether to spin a dedicated dense-supervision branch or leave W2.4b's result as the answer.

---

### 11. Continuous-Solver Variable Compute — future-work

**Pre-step: NEURAL-ODE-AT-TINY-SCALE**

Before committing to a continuous-depth variable-compute architecture at Qwen3-4B, verify that the adjoint method gradient is stable at tiny scale.

**Concrete measurements:**
- Build a toy neural ODE on GPT-2-micro (2-layer, ~1M params).
- Train for 1k steps with `torchdiffeq` adjoint backward.
- Measure: gradient norm stability, whether the solver integration steps converge (ideally <10 steps per forward).
- Measure: does the solver learn variable-compute allocation (more steps on harder tokens) or uniform?

**Cost:** 4 GPU-hours.

**Go/no-go:** if adjoint is stable AND variable-compute emerges → continuous-solver approach is feasible → promote to sketched plan. Else → adjoint instability kills the approach at scale; stay future-work.

---

## Summary discipline

**Before we commit to any plan in `plans/`**, run its pre-step. If the pre-step kills the idea, we saved weeks. If the pre-step confirms, we commit with confidence. Per-step cost is small; cumulative cost saved by filtering out dead ends is large.

**For ideas still in INDEX-only status:** promote to full idea page only after pre-step passes. Before pre-step, the idea is speculation; after pre-step-pass, it's grounded speculation.

**Track pre-step results** in each idea's "Pre-step feasibility check" section (see [[Latent Scratchpad]], [[Manifold-Constrained Residual Stream (mHC)]] for examples). Update status/maturity after pre-step lands.
