---
type: idea
title: "Latent Scratchpad"
created: 2026-04-24
updated: 2026-04-24
tags:
  - idea
  - architecture/hybrid
  - interpretability
  - faithfulness
  - domain/latent-reasoning
status: promoted-to-plan
maturity: planned
plan_link: /Users/jrauvola/Desktop/Latent_Reasoning_Project/plans/wave3/W3.5_latent_scratchpad.md
grounding_sources:
  - "[[Latent Sketchpad]]"
  - "[[Token Assorted]]"
  - "[[HRPO]]"
  - "[[Scratchpad Thinking]]"
  - "[[Quiet-STaR]]"
  - "[[Nye et al. Scratchpad 2021]]"
related_concepts:
  - "[[Latent Scratchpad Architecture]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
  - "[[Loop-Mode Emission]]"
related:
  - "[[Research - Latent Scratchpad Precedence]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Novel interpretability-preserving latent architecture; first branch that explicitly trades interpretability budget against accuracy."
  - slug: "branch-d"
    relevance: secondary
    why: "Composes with CPF — scratchpad externalizes the reasoning that CPF tries to anchor to vocab manifold."
last_reviewed: 2026-04-24
reviewed_by: josh
---

# Latent Scratchpad

## The idea in two paragraphs

Latent reasoning models (CODI, COCONUT, LT-Tuning) do all their reasoning in opaque continuous hidden states. Chain-of-thought forces verbalization of every step — interpretable but expensive and constrained by language. **Latent Scratchpad proposes the middle: latent tokens do the heavy computation (primary stream, CODI-compatible) AND a sparse discrete vocab-readable side-channel captures structured "notes" at chosen transitions.** Like a human doing mental math with occasional scribbles — most of the thinking is intuitive, but key intermediate results get written down for verification and memory.

Architecturally: M latent steps per rollout (unchanged from CODI). A learned sparsity-gated emission head fires at 0-K positions (K=3 by default) to write 1-3 vocab tokens into a scratchpad buffer. The buffer attends back into subsequent latent positions via past_kv. Training adds three loss terms: answer CE (primary), scratchpad decodability (weak supervision from teacher CoT step summaries), and sparsity penalty on gate activations. **Critical constraint (per user intuition):** the gate cannot fire until after `warmup_latent_steps = 2` so latents pass context FIRST before any externalization happens.

## Why it matters for our project

Reframes the F1-F6 routing-not-reasoning pathology. Current framing: "latents are either routing keys OR reasoning channels; F5 swap-null proves routing." Scratchpad framing: **latents are the computation; scratchpad is where legible structure lives.** F5 swap-null is expected (latents are compute, not content); the new test becomes "does swapping scratchpads change predictions?" Expected yes, substantially.

Also breaks the F3 template-lock by construction: the decoder's format-prior attractor captures all interpretable-token budget *because* the model has no legible commit point during rollout. Scratchpad gives it one.

## The COMPRESSION + KV-bandwidth framing (added 2026-04-25)

After the 2026-04-24 team meeting (Christopher + Uzay), a sharper mechanistic frame emerged that strengthens W3.5's case:

**Christopher's finding:** at Qwen3-4B, latent KV "disappears" before the answer token attends. CODI throws away hidden state by design; only KV bleeds through, and not enough of it at 1B+. Explains the scaling pattern — GPT-2 fits its reasoning into a tiny KV (86% on GSM8K) but 1B+ models can't (<20%).

**Implied by user (2026-04-25):** if smaller models work because their CoT/reasoning is *small enough to fit in the KV cache* available at the answer-attention point, then a scratchpad that **compresses** the reasoning to fit available KV bandwidth should let larger models work too. The scratchpad isn't just a legibility channel — it's a *KV-cache-fitting compression mechanism*.

**This reframes W3.5 from interpretability-first to bandwidth-first:**

- **Original framing:** scratchpad emissions are short discrete vocab tokens for human readability; aux loss enforces decodability against teacher CoT.
- **New framing:** scratchpad emissions are *information-dense compressed reasoning summaries* whose primary purpose is to maintain non-zero KV-bandwidth at the answer-attention point. Legibility becomes a free side effect of using the vocab embedding space (not an objective).

**Loss design implication:**

- Drop "decodability against teacher CoT step summaries" as PRIMARY supervision (it's a legibility constraint, not a bandwidth constraint).
- Replace with "KV-bandwidth-at-answer-position" as primary supervision: the answer-token attention head MUST be able to retrieve step-relevant information from the scratchpad emissions even when latent KV has fully decayed.
- Add length penalty (compression incentive) + information-content reward (bandwidth utilization).

**Falsifiable scaling prediction (the strong-form hypothesis):**

If your compression intuition is right:
- W3.5 helps MORE at Qwen3-4B than at GPT-2.
- Reason: at GPT-2 the latent KV doesn't disappear before the answer attends, so scratchpad is redundant. At 4B the latent KV disappears, so scratchpad is the bandwidth that survives.
- This is the OPPOSITE of standard "test small first, hope it scales" expectation. It says: at scale, scratchpad is *necessary*; at small, scratchpad is *helpful but not load-bearing*.

**Pre-step that tests this:** Christopher's per-position KV-norm instrumentation (added to PRE-STEPS.md as #0). Measure KV-norm of latent positions at the answer-attention point on V2 bf16 baseline. Three cases:
1. KV-norm is non-zero at all latent positions → "latent KV disappears" hypothesis is wrong; bandwidth isn't the failure.
2. KV-norm decays monotonically (latest latent has most bandwidth) → CODI is throwing away history; scratchpad emissions at recent positions might fix it.
3. KV-norm is uniformly low → CODI's latent positions can't carry bandwidth at all; scratchpad needs to do ALL the carrying, not augment.

Each case implies a different W3.5 design. **Run the KV-norm probe before training any W3.5 variant.**

## Mechanistic basis — the LSTM analogy

The architectural intuition is genuinely close to what LSTMs did for RNNs, not just surface-similar:

**Failure mode LSTMs solved:** vanilla RNN single-hidden-state has gradient flowing through T non-linearities → vanishing/exploding. LSTM adds a protected cell state `c_t` where the default is `c_t = c_{t-1}` (Constant Error Carousel) with multiplicative gates (`f_t`, `i_t`, `o_t`) controlling deviations. Gradients flow through the cell state linearly → preserved over long horizons.

**Failure mode Latent Scratchpad targets:** CODI's continuous latents route through the same attention that format-attractors capture → F3 template collapse, F5 swap-null. Adding a discrete scratchpad with default-no-emit + gated write gives a **protected secondary store** that's structurally immune to the continuous-geometry attractor collapse.

**Same pattern both architectures instantiate:** add a secondary store structurally protected from the primary stream's failure mode, controlled by learned gates.

**Three honest disanalogies:**
1. LSTM gates are continuous (standard gradients); scratchpad gates are discrete (Gumbel-STE needed).
2. LSTM cell state is internal/opaque; scratchpad is external/human-readable (a bigger legibility commitment).
3. Transformers already have attention for selective access; scratchpad adds a **discrete legible commit point** on top — different property, not just selective memory.

**Strongest evidence it can work at scale:**
- **Mamba** (Gu & Dao 2023): selective gates at LLM scale beat transformers on long context → gated-memory mechanisms are not LSTM-era artifacts.
- **RETRO** (Borgeaud et al. 2022): 25B-param LM + retrieval matches 175B-param LM without → discrete memory offload at scale works.
- **Neural Turing Machines** (Graves 2014): end-to-end training of discrete external memory heads validated years ago.
- **[[Latent Sketchpad]]** at vision: same pattern validated in a different modality.
- **[[HRPO]]**: learned gate between continuous hidden and discrete token embedding at 1-7B.

**LSTM parallels that also warn us:**
- Added representation complexity justified only at scale — LSTMs barely beat RNNs on small tasks; same risk at GPT-2.
- Training difficulty requires care (forget-gate-bias = 1 in LSTM; gate-init-bias = -2.0 in our plan; temperature annealing; 2-stage curriculum).
- Marginal at small scale is plausible; Qwen3-4B may be where the gain shows.

## Grounding papers (in order of closeness to our proposal)

1. **[[Latent Sketchpad]]** (Zhang 2025, arxiv:2510.24514) — direct inspiration. Same architectural pattern (primary latent stream + interpretable side-channel) but in vision modality with continuous visual latents + Sketch Decoder. **Code:** `hwanyu112/Latent-Sketchpad`. W3.5 ports the pattern to text-only LLMs; replaces Sketch Decoder with direct vocab emission tied to lm_head.
2. **[[Token Assorted]]** (Su 2025) — closest discrete-side-channel. Uses VQ-VAE codebook latents with randomized-m training. Differs from W3.5 in two ways: (a) codes are opaque (VQ), not vocab-readable; (b) no learned gate — mixing is random. W3.5's vocab-readable + learned-gate combo is the differentiator.
3. **[[HRPO]]** (Yue 2025) — closest learned gate. Uses `g(ctx)·h_hidden + (1-g)·e_token` with learned context-dependent blending + RL training. Differs: HRPO's gate blends in a *single* stream; W3.5's gate emits to a *parallel side-channel*. **Code:** `Yueeeeeeee/HRPO` — borrow gate parametrization.
4. **[[Scratchpad Thinking]]** (Goyal 2025, NeurIPS MechInterp Workshop) — motivation. Finds that CODI's latents already internally alternate "storage" vs "computation" steps. **W3.5 is a structural decision to surface this pre-existing pattern to a legible channel**, rather than imposing an artificial one.
5. **[[Quiet-STaR]]** (Zelikman 2024) — thoughts-before-tokens framing. Differs: Quiet-STaR thoughts are textual and fire at every position; W3.5 thoughts are latent by default, scratchpad emissions are sparse.
6. **[[Nye et al. Scratchpad 2021]]** — original scratchpad paper (pre-CoT). Purely discrete intermediate work area. W3.5 borrows the framing but replaces all-discrete with sparse-discrete-over-continuous.
7. **[[Neural Turing Machines]]** / **[[Differentiable Neural Computer]]** (Graves 2014-16) — differentiable external memory with read/write heads. W3.5 uses a learned discrete-emission gate in place of NTM's continuous-vector write.

## Concepts involved

- **[[Latent Scratchpad Architecture]]** — the concept page formalizing the pattern.
- **[[Feature Collapse]]** — the failure mode W3.5 directly targets.
- **[[Routing vs Reasoning]]** — the dichotomy W3.5 dissolves.
- **[[Loop-Mode Emission]]** — the pathology W3.5 predicts it cures via legible commit points.

## Mechanism (full details in the plan)

```
input → M latent steps (primary stream, CODI-compatible)
         ↓
         gate(h_t) ∈ Bernoulli per position (Gumbel-Softmax STE during training)
         ↓
         if gate fires and step > warmup: emit 1-3 vocab tokens → scratchpad buffer
         ↓
         buffer attends back into subsequent latent positions via past_kv
         ↓
answer generation

losses: L_answer (primary CE) + λ_d · L_decode (notes match teacher step summaries) 
      + λ_s · L_sparsity (L1 on gate activations) + λ_b · L_budget (hard penalty > K)
```

See `plans/wave3/W3.5_latent_scratchpad.md` for full pseudocode, configs, stepwise implementation.

## New evaluation tests W3.5 introduces

- **F7 scratchpad-mask ablation** — mask all emitted notes, measure accuracy drop. Gate: ≥30% relative drop at 4B → scratchpad is causal.
- **F8 cross-example scratchpad swap** — swap example A's scratchpad into B's forward pass. Gate: ≥50% predictions change → scratchpad drives predictions per-example.
- **Causal faithfulness intervention** (per Goyal 2025 methodology) — replace note token with wrong token (e.g., "5" → "10"), check if prediction shifts consistently.

## Current status

**Promoted to plan: 2026-04-24.** Plan at `plans/wave3/W3.5_latent_scratchpad.md` (17th implementation plan; ready for coding agent hand-off after spec approval).

## Open questions

1. Can the gate be trained end-to-end without instability (gate collapse to always-fire or never-fire)?
2. What's the right supervision signal for scratchpad notes? Teacher CoT step summaries vs. contrastive-against-format-tokens vs. information-bottleneck-only?
3. Does scratchpad compose with CPF (Branch D) or are they redundant?
4. At Qwen3-4B scale, what's the minimum K_budget that still produces interpretable trajectories?
5. Does the scratchpad-attention-back mechanism require architectural changes, or does it work via standard past_kv reuse?

## Next step if we return to this idea

Review `plans/wave3/W3.5_latent_scratchpad.md` before handing to coding agent. Verify HRPO gate parametrization (plan Step 1) — determines whether discrete Bernoulli + Gumbel-STE is needed or whether HRPO's parametrization is directly reusable.

## Pulling in relevant information

When re-opening this idea in a future session, read in this order:
1. This page (quick overview)
2. `plans/wave3/W3.5_latent_scratchpad.md` (full implementation plan)
3. `wiki/concepts/Latent Scratchpad Architecture.md` (formal mechanism)
4. `wiki/questions/Research - Latent Scratchpad Precedence.md` (the 2026-04-24 autoresearch findings that grounded the novelty claim)
5. Source pages above (individual paper depth)
