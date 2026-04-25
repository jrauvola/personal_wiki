---
type: concept
title: "Discrete Gate Training (Gumbel-STE vs REINFORCE vs Soft Relaxation)"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/concept
  - domain/discrete-latent
  - method/gumbel-softmax
  - method/reinforce
  - method/straight-through
status: developing
complexity: advanced
domain: discrete-latent
aliases:
  - "ST-Gumbel"
  - "Straight-Through Gumbel-Softmax"
  - "Discrete latent training"
  - "Discrete gradient estimation"
related:
  - "[[Gumbel-Softmax Latent]]"
  - "[[Latent Scratchpad Architecture]]"
  - "[[End-to-End Memory Networks]]"
  - "[[Neural Turing Machines]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "The training-time engineering question for any architecture with discrete decisions inside differentiable computation - including Latent Scratchpad's emission gate. Choosing the right estimator is load-bearing for whether the architecture trains at all."
  - slug: "branch-d"
    relevance: primary
    why: "W3.5 Latent Scratchpad's Bernoulli emission gate must be trained somehow. This concept page enumerates the choices (ST-Gumbel, REINFORCE, soft-then-hard, REBAR/RELAX) and which fit the W3.5 setup."
  - slug: "branch-a"
    relevance: reference
    why: "Standard transformer architecture - no discrete latents."
  - slug: "branch-b"
    relevance: secondary
    why: "Detach policy is conceptually adjacent to STE — both are 'gradient-pass-through with structural modification' tricks."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Probe-protocol unrelated."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Discrete Gate Training (Gumbel-STE vs REINFORCE vs Soft Relaxation)

When a neural network must make a **discrete** decision (sample from a categorical distribution, fire a binary gate, emit one of K tokens) **inside** a differentiable computation graph, gradient estimation becomes the load-bearing engineering question. This page enumerates the choices, their tradeoffs, and which fit the W3.5 Latent Scratchpad setup.

## The four families

### 1. Score-function (REINFORCE) — high-variance, unbiased

```
∇θ E[f(z)] ≈ f(z) · ∇θ log p(z; θ)        z ~ p(z; θ)
```

- **Pros:** unbiased; works with any discrete distribution; no continuous relaxation.
- **Cons:** **enormous variance** — typically 100-1000× higher than reparameterization. Needs control variates (REBAR, RELAX, NVIL, MuProp) to be usable. Doesn't compose well with deep architectures.
- **When used:** when no continuous relaxation exists (e.g. large discrete action spaces in RL).
- **Historical note:** the original Memory Networks (Weston 2014, **NOT** [[End-to-End Memory Networks]]) needed strong supervision rather than REINFORCE because score-function gradients on discrete memory access were too noisy.

### 2. Gumbel-Softmax (Jang et al. 2017) — biased-but-low-variance

The reparameterization for categorical distributions:
```
y_i = exp((log π_i + g_i) / τ) / Σ_j exp((log π_j + g_j) / τ),    g_i ~ Gumbel(0,1)
```
- As `τ → 0`, samples become one-hot (approaches the discrete distribution).
- As `τ → ∞`, samples become uniform (high entropy).

**Pros:** end-to-end differentiable; low variance; simple to implement.
**Cons:** **biased** at τ > 0; the optimization landscape is not the same as the true discrete one. Choosing τ is a hyperparameter; too low → variance explodes; too high → severely biased.

### 3. Straight-Through Gumbel-Softmax (ST-Gumbel) — the workhorse

The recipe used by most modern architectures with discrete latents:
- **Forward pass:** argmax — one-hot, truly discrete.
- **Backward pass:** use softmax gradients (the Gumbel-softmax surrogate).

This is **biased but practical**. The forward/backward mismatch is acceptable in practice for most tasks; the bias decreases as τ → 0.

**Recommended schedule (Jang 2017):**
```
τ = max(0.5, exp(-r · t)),    r ∈ {1e-5, 1e-4}
```
Updated every N steps; minimum τ = 0.5 to avoid variance blowup.

### 4. Soft relaxation only (no hard sampling) — easiest to train, weakest guarantees

Just use the softmax outputs `y` directly as soft assignments — never sample. Gradient flows cleanly. But you lose the sparsity property entirely; the "decision" is always a continuous mixture.

**Pros:** trivial to train; no estimator needed.
**Cons:** the architecture isn't actually discrete at inference either, unless you add a hard-decode step (which then has a forward/backward mismatch — back to ST anyway).

## REBAR and RELAX (the variance-reduced REINFORCE family)

[REBAR (Tucker et al. 2017, NeurIPS)](https://arxiv.org/abs/1703.07370) combines the two main approaches:
- Use score-function (unbiased) gradient.
- Subtract a **control variate built from the Gumbel-softmax relaxation** to cancel variance.
- Adapt the control-variate's relaxation tightness online — no τ hyperparameter.

**Result:** unbiased + low-variance discrete latent training. Conceptually clean but engineering-heavy. Used in research VAEs but rarely in production systems.

[RELAX (Grathwohl et al. 2017)](https://arxiv.org/abs/1711.00123) generalizes REBAR with a learned neural-network control variate. Strictly more flexible; same training cost.

## Which to use for W3.5 Latent Scratchpad

The W3.5 plan uses **ST-Gumbel-Softmax** for the Bernoulli emission gate (per `scratchpad_head.py` pseudocode in the plan). This is the right default:

- The decision is binary (emit / pass-through), so `K=2` Gumbel-softmax is fine.
- The downstream loss (answer CE + decodability + sparsity) is dense — variance from REINFORCE would dominate.
- The 2-stage curriculum in the plan (soft Stage A → sharp Stage B) is the natural temperature-annealing schedule for ST-Gumbel.

**Recommended W3.5 temperature schedule:**
- Stage A: τ = 2.0 (soft, high entropy — gate explores).
- Stage B: τ = 0.5 (Jang's recommended floor — gate sharpens to near-discrete).

## Failure modes specific to discrete-gate training

These are the patterns that show up in any architecture training discrete gates end-to-end:

1. **Gate collapse to always-fire (gate ≈ 1 everywhere).** Every position emits; sparsity penalty wasn't strong enough. Fix: increase λ_sparsity.
2. **Gate collapse to never-fire (gate ≈ 0 everywhere).** No emissions ever; downstream signal can't reach the gate. Fix: gate_init_bias toward fire (W3.5 plan's `gate_init_bias = -2.0` is the OPPOSITE — designed to suppress early emission so latents pass context first; this is the user's "warmup" constraint).
3. **Mode collapse on what's emitted.** Gate fires variably but always emits the same token. Fix: increase entropy regularization on Note Head outputs; or contrastive L_decode against most-frequent vocab.
4. **Forward/backward mismatch instability.** Argmax-forward / softmax-backward causes loss spikes. Fix: warm up with low temperature; use larger batch size for variance averaging.

## Initialization tricks (load-bearing)

The LSTM analogy in [[Latent Scratchpad]] mentions LSTM's **forget-gate-bias = 1** trick (Jozefowicz 2015). The discrete-gate analog is the **gate_init_bias hyperparameter**:

| Architecture | Init bias | Effect |
|---|---|---|
| LSTM (Jozefowicz 2015) | forget_bias = 1 | Default to "remember" — easier to learn long-range deps |
| W3.5 Latent Scratchpad (planned) | gate_init_bias = -2.0 | Default to "no emission" — let latents pass context first |
| Mixture-of-Experts (Shazeer 2017) | gate noise = N(0, 1/N²) | Force exploration over experts |

The pattern: **bias toward the "safe" default behavior** at init, then let training move the gate where it's useful.

## Sources

- Jang, Gu, Poole 2017 (ICLR) — original Gumbel-Softmax paper. arXiv:1611.01144.
- Maddison, Mnih, Teh 2017 (ICLR) — concurrent Concrete distribution paper. arXiv:1611.00712.
- Tucker, Mnih, Maddison, Sohl-Dickstein 2017 (NeurIPS) — REBAR. arXiv:1703.07370.
- Grathwohl, Choi, Wu, Roeder, Duvenaud 2017 — RELAX. arXiv:1711.00123.
- [[Gumbel-Softmax Latent]] — sibling concept page (focuses on continuous-stream Gumbel).
- [[Latent Scratchpad Architecture]] — where the W3.5 emission gate is specified.
