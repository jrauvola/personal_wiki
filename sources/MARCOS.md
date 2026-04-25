---
type: source
title: "MARCOS — Markov Chain of Continuous Thoughts"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/stochastic-latent
  - type/source
  - method/variational
status: read
source_type: paper
arxiv_id: "2509.25020"
venue: "arXiv"
date_published: 2025-09-29
authors:
  - "Jiayu Liu"
  - "Zhenya Huang"
  - "Anya Sims"
  - "Enhong Chen"
  - "Yee Whye Teh"
  - "Ning Miao"
url: "https://arxiv.org/abs/2509.25020"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "MARCOS models reasoning as a hidden Markov chain of continuous high-dimensional thoughts, with explicit reasoning steps serving as observable emissions that reveal the implicit latent process."
  - "A two-phase variational training scheme resolves the incompatibility between latent Markov reasoning and standard supervised learning."
  - "On GSM8K, MARCOS achieves +4.7% accuracy over token-based CoT with up to 15.7× inference speedup."
  - "MARCOS outperforms existing continuous reasoning methods (COCONUT, CoLaR, CODI) across three reasoning benchmarks."
  - "Step-level (rather than token-level) control over randomness makes MARCOS a natural substrate for RL in continuous-reasoning LLMs."
related:
  - "[[CoLaR]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[Feature Collapse]]"
sources:
  - "[[.raw/papers/2509.25020-marcos]]"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Variational latent-chain approach is an alternative to CPF fusion; informative for north-star synthesis but not the implementation target."
  - slug: "branch-a"
    relevance: secondary
    why: "Claimed 15.7× speedup at comparable accuracy is a scaling-relevant datapoint, but no Qwen-specific validation."
  - slug: "branch-b"
    relevance: reference
    why: "Tangential to detach/grad-stability axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No bearing on probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "+4.7% over token-CoT on GSM8K with 15.7× speedup is a striking writeup datapoint, but no released code/weights and variational framing off the V2/SIM-CoT/LT-Tuning synthesis line — cite but not a primary synthesis input."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# MARCOS — Markov Chain of Continuous Thoughts

> [!contradiction] MARCOS primacy vs [[OneVL]] 'first-to-surpass' claim
> MARCOS (Sep 2025) claims to be the first continuous-reasoning method to surpass token CoT on GSM8K (+4.7%). [[OneVL]] (Apr 2026) claims to be the "first latent CoT to surpass explicit CoT" across 4 driving benchmarks. Not a direct contradiction — different benchmarks, different domains — but both claims collide on the "first" language. MARCOS wins on priority for math reasoning; OneVL's claim should be scoped to its driving domain.

Liu, Huang, Sims, Chen, Teh, Miao — [arXiv:2509.25020](https://arxiv.org/abs/2509.25020) (2025-09-29). Yee Whye Teh's group. No code repo released at time of crawl.

## Core thesis

Autoregressive token CoT has three defects: (1) thousand-token generation is slow, (2) discrete tokens create an information bottleneck, (3) "thinking while speaking" forces short-sighted reasoning. MARCOS replaces the token-level chain with a **hidden Markov chain of continuous high-dimensional thoughts**, where explicit tokens are observable emissions that reveal — but do not constrain — the latent process.

## Method

### Generative model

`z_1 → z_2 → ... → z_T` — latent Markov chain of continuous thoughts. Each `z_t` is a high-dimensional vector. Emission: `y_t ~ p(y | z_t)` — observed CoT tokens are windows onto the latent state.

### Two-phase variational training

| Phase | Objective | What it learns |
|---|---|---|
| 1 | Variational ELBO aligning observed CoT with latent Markov chain | Encoder posterior `q(z | y)`, decoder emission `p(y | z)` |
| 2 | Latent-only refinement (no token emissions in inner loop) | Stable inference-time thought transitions |

### Step-level stochasticity

Because MARCOS is generative, randomness lives at the *step* level (`z_t` sampled per step), not the *token* level. This is CoLaR-compatible but more fundamental — CoLaR's latent head emits a Gaussian-sampled next compressed embedding; MARCOS's variational transition does the same thing under a generative-model banner.

## Recipe

- **Benchmarks:** GSM8K + two others (ProsQA, MATH likely — paper excerpt didn't specify all three).
- **Comparisons:** token CoT baseline; continuous-reasoning baselines (COCONUT-class).
- **Objective:** Phase 1 ELBO; Phase 2 latent-only refinement.

## Results

| Metric | MARCOS | Baseline |
|---|---|---|
| GSM8K accuracy | +4.7% vs token CoT | — |
| Inference speedup | up to 15.7× | 1× |
| Wins over continuous-reasoning baselines | 3/3 benchmarks | — |

First reported case (per the paper) of a continuous-reasoning method *surpassing* token CoT on GSM8K rather than just approaching it.

## Relevance to our project

- **Primary for spar-latent-reasoning.** The "+4.7% over token CoT + 15.7× speedup" result is a north-star-adjacent datapoint. Much of the writeup's argument hinges on whether latent methods can truly beat explicit CoT; MARCOS claims yes on GSM8K.
- **Secondary for branch-d.** Variational framing is an alternative, not a replacement, for LT-Tuning's CPF. Informative for synthesis.
- **Risk flagged.** No released code/weights; independent reproduction not available. Two-phase variational training is non-trivial to implement from scratch.

## Citation links to chase

- Upstream: [[COCONUT]], [[CoLaR]]
- Sibling stochastic-latent work: LEPO (2604.17892), Stochastic Soft Thinking (2508.03440), Latent-SFT (2510.15522)

## Artifacts

- **Paper:** [arXiv:2509.25020](https://arxiv.org/abs/2509.25020)
- **Code:** none released at crawl time.
- **Raw source:** [[.raw/papers/2509.25020-marcos]]
