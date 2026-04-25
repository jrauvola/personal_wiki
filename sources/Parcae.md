---
type: source
title: "Parcae: Scaling Laws For Stable Looped Language Models"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/architecture
  - domain/scaling-laws
  - type/source
  - method/looped-lm
status: read
related:
  - "[[Ouro]]"
  - "[[LoopLM]]"
  - "[[Fixed-Width Depth Recurrence]]"
sources:
  - "[[.raw/papers/2604.12946-parcae]]"

source_type: paper
arxiv_id: "2604.12946"
venue: "arXiv"
date_published: 2026-04-14
authors:
  - "Hayden Prairie"
  - "Zachary Novack"
  - "Taylor Berg-Kirkpatrick"
  - "Daniel Y. Fu"
url: "https://arxiv.org/abs/2604.12946"
code_repo: null
has_weights: false
status: read
confidence: medium
key_claims:
  - "Looped LM instability (residual explosion, loss spikes) is an unconstrained-spectral-norm problem; constraining ρ(Ā)<1 via a negative-diagonal parameterization A = Diag(−exp(log_A)) with zero-order-hold discretization Ā = exp(Δ⊙A) stabilizes training."
  - "At 1.3B parameters on 100B tokens, Parcae gets 6.3% lower validation perplexity vs prior RDM looped baselines and +2.99 CORE / +1.18 Core-Extended points vs param-matched Transformers, reaching 87.5% quality of a 2× Transformer."
  - "770M Parcae matches 1.3B Transformer quality on CORE."
  - "Training-FLOP optimal allocation follows power laws: optimal recurrent-depth μ_rec ∝ FLOP^0.40, optimal data D ∝ FLOP^0.78."
  - "Test-time-compute scaling follows a saturating exponential decay L(T) = L_∞ + Z·exp(−zT); unified train+inference law with irreducible floor."
  - "Truncated backprop μ_bwd = ⌈μ_rec/2⌉ (half the forward recurrence) is the recipe used; per-sequence depth sampling + 'prelude' normalization stabilize training."

projects:
  - slug: "branch-a"
    relevance: reference
    why: "Architecture-dependent scaling is adjacent but Parcae studies looped LMs from scratch, not Qwen-family fine-tunes."
  - slug: "branch-b"
    relevance: secondary
    why: "μ_bwd = ⌈μ_rec/2⌉ truncated backprop is the exact analog of our detach-at-step-k ablation axis — Parcae provides a scaling-law framework for 'how much BPTT is enough?' that our V2/V3/V4 detach ablations can borrow; strong outside-reference even though we're not training from scratch."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not about probe validity."
  - slug: "branch-d"
    relevance: reference
    why: "Different paradigm (fixed-width depth recurrence, not sequence-growing latents) — useful as scaling-law reference but not a CPF-integration path."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Clean scaling-law framework for looped LMs with stability recipe — useful reference for the writeup's depth-recurrence discussion, but from-scratch pretraining and the looped-LM paradigm are not on the V2 / SIM-CoT / LT-Tuning synthesis line."

last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Parcae: Scaling Laws For Stable Looped Language Models

## TL;DR

Recast looping as a discrete nonlinear time-variant dynamical system; constrain its spectral radius below 1 via a **negative-diagonal parameterization** with zero-order-hold discretization. This prevents the residual-state explosion that plagued prior looped / RDM (recurrent-depth models) work. At 1.3B / 100B-tokens Parcae beats a param-matched Transformer on CORE by ~3 points and recovers scaling laws: **μ_rec ∝ FLOP^0.40**, **D ∝ FLOP^0.78**, test-time L(T) = L_∞ + Z exp(−zT).

## Method

### Dynamical-system form

Layer recurrence:

$h_{t+1} = \bar{A} \cdot h_t + \bar{B} \cdot e + \bar{R}(h_t, e)$

- `e` = layer input (skip / embedding path).
- `R̄` = the original residual block (nonlinear).

### Negative-diagonal parameterization

$A = \text{Diag}(-\exp(\log A)), \quad \log A \in \mathbb{R}^{d_h}$

- Diagonal → decouples dims.
- `−exp(·)` → always negative (stable continuous-time).
- Zero-order-hold discretization: $\bar{A} = \exp(\Delta \odot A)$ with learned Δ.
- Result: **ρ(Ā) < 1** guaranteed.

Contrast: prior RDMs could hit ρ(Ā) ≥ 1 during training, producing residual explosion / loss spikes (the same class of instability Ouro mitigated by reducing 8 → 4 loops).

### Additional recipe

- **Prelude normalization.**
- **Per-sequence depth sampling** (train with varied μ_rec per batch).
- **Truncated BPTT: μ_bwd = ⌈μ_rec/2⌉** — half the forward recurrence backpropagates.

## Results

### End-to-end quality — 1.3B, 100B tokens

- vs prior RDM: **6.3% lower validation PPL.**
- vs param-matched Transformer: **+2.99 CORE, +1.18 Core-Extended.**
- Reaches 87.5% of 2× Transformer quality.
- 770M Parcae ≈ 1.3B Transformer on CORE.

### PPL examples

| Size | Fixed-depth | Parcae looped |
|---|---|---|
| 140M | 21.48 | 19.06 (T=8) |
| 370M | 15.79 | 14.49 |

### Scaling laws

- **Training-FLOP optimal:** μ_rec ∝ FLOP^0.40, D ∝ FLOP^0.78.
- **IsoFLOP Pareto:** +1.2 to +2.0 CORE pts vs Transformers.
- **Test-time scaling:** L(T) = L_∞ + Z exp(−zT). Saturating exponential with irreducible floor.
- Unified train+inference law: ties recurrent-depth compute to final quality.

## Relevance

- **Directly addresses Ouro's instability.** Ouro reduced loops 8 → 4 to stabilize; Parcae instead constrains spectral norm → can train stably at higher μ_rec.
- **μ_bwd = ⌈μ_rec/2⌉** is the scaling-friendly truncated-BPTT recipe — same class as Josh's detach-at-k ablation. Bridging these: Parcae does step-k truncation; our V2/V3 does detach-at-step-k. Parcae's scaling-law framework would tell us how μ_bwd should scale with training compute even if we keep the fine-tuning setup.
- **Open engineering question:** can a Qwen3-4B or 8B loaded as a looped model (retrofit, not from-scratch) use Parcae's negative-diagonal parameterization to stabilize the V2 detach variant? Speculative.
- **Complements Ouro's scaling laws.** Parcae nails down looped-LM scaling laws more cleanly at smaller scales with stability guaranteed, where Ouro had R²≈0.96 on aggregate fits.

## Cross-links

- [[Ouro]] — compared directly.
- [[LoopLM]] — same architectural family.
- [[Fixed-Width Depth Recurrence]] — Parcae is another instance.
