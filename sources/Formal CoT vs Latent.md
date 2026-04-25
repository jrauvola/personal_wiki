---
type: source
title: "A Formal Comparison Between Chain of Thought and Latent Thought"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/theory
  - domain/complexity
  - type/source
status: read
related:
  - "[[Ouro]]"
  - "[[COCONUT]]"
  - "[[LoopLM]]"
sources:
  - "[[.raw/papers/2509.25239-formal-cot-vs-latent]]"

source_type: paper
arxiv_id: "2509.25239"
venue: "arXiv"
date_published: 2025-09-25
authors:
  - "Kevin Xu"
  - "Issei Sato"
url: "https://arxiv.org/abs/2509.25239"
code_repo: "https://github.com/kevin671/cot-vs-loop"
has_weights: false
status: read
confidence: high
key_claims:
  - "Under standard complexity assumption TC^{k-1} ⊊ TC^k (Theorem 3.12, 3.15): Looped Transformers and Coconut with log^k n latent iterations capture TC^k exactly; CoT with log^k n steps ⊆ TC^{k-1} → latent thought STRICTLY BEATS CoT on polylog-iteration parallel reasoning."
  - "Under FPTAS ⊊ FPRAS for self-reducible relations (Theorem 4.5): CoT enables approximate counting and sampling (via stochastic intermediate tokens) that latent thought provably cannot — CoT wins on randomized-algorithm emulation."
  - "Empirically validates separations: looped TF needs fewer iterations than CoT on word problems / graph connectivity / arithmetic / edit distance (parallelizable); fails on DNF counting and graph-coloring sampling where CoT's Monte Carlo wins."
  - "Assumptions used: log-precision arithmetic (3.2), polynomial-size graphs (3.3), poly-efficient function approximation (3.4)."

projects:
  - slug: "branch-a"
    relevance: not-applicable
    why: "Theoretical complexity result, not architecture-specific."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach/stability tool."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a probe methodology tool."
  - slug: "branch-d"
    relevance: reference
    why: "Theoretical grounding for 'latent parallelism beats CoT on parallel problems' — useful citation for LT-Tuning writeup but not directly implementable."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Clean complexity-theoretic framing of 'when latent beats CoT' is a valuable writeup citation, but theoretical and not an active synthesis input for the workable model; reclassified secondary — primary is reserved for methods we're implementing or directly anchoring the writeup on."

last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# A Formal Comparison Between Chain of Thought and Latent Thought

## TL;DR

Formal complexity-theoretic comparison of CoT vs latent thought. **Two separations:**

1. Looped / latent thought > CoT on parallel reasoning (TC^k vs TC^{k-1} at log^k n iterations, assuming TC^{k-1} ⊊ TC^k).
2. CoT > latent thought on approximate counting and sampling (FPRAS vs FPTAS, assuming FPTAS ⊊ FPRAS for self-reducible relations).

Empirical validation on word problems, graph connectivity, DNF counting, graph-coloring sampling confirms both directions.

## Theoretical results

### Separation 1 — Latent → Parallel

- **Theorem 3.12:** Looped Transformers with log^k n iterations capture TC^k exactly.
- **Lemma 3.13:** CoT with log^k n steps ⊆ TC^{k-1}.
- **Theorem 3.15:** Assuming TC^{k-1} ⊊ TC^k: latent thought strictly > CoT at polylog iterations.
- **Setting:** log-precision arithmetic (Def 3.2), polynomial-size graphs (3.3), poly-efficient function approximation (3.4).

### Separation 2 — CoT → Stochastic

- **Theorem 4.5:** Assuming FPTAS ⊊ FPRAS for self-reducible relations, CoT can approximate count/sample where latent cannot.
- **Lemma 4.3:** CoT admits FPRAS for self-reducible counting problems; latent thought does not.
- **Mechanism:** CoT's stochastic intermediate-token sampling emulates randomized algorithms; latent thought is deterministic in its internal computation.

## Empirical validation

### Parallelizable (Table 2, Figure 6)

- Tasks: word problems, graph connectivity, arithmetic evaluation, edit distance.
- Looped TF needs **fewer iterations** than CoT at matched accuracy.
- Logarithmic scaling of required iterations confirmed.

### Counting/sampling (Figure 7)

- Tasks: DNF formula counting, graph-coloring sampling.
- CoT effective via Monte Carlo / MCMC-style sampling.
- Looped TF fails on probabilistic tasks.

## Relevance

- **First principled answer to "when to prefer latent vs CoT":** depth-driven recursion (latent/looped) wins on parallelizable problems; stochastic token-chain (CoT) wins on counting/sampling.
- **Directly applicable to benchmark choice in Ouro interpretability work:** if we're asking whether Ouro's latent compute does more than CoT, parallel reasoning tasks are the right proxies; trying on counting tasks would understate latent's value.
- **Caveat for CODI-like methods with discrete latent sampling:** VQ-VAE-ified latents (e.g., Discrete Latent, Token Assorted) could in principle inherit some of CoT's counting advantage — depends on stochasticity of the discrete code.
- **Open code:** https://github.com/kevin671/cot-vs-loop.

## Cross-links

- [[Ouro]] — primary looped-LM subject of Separation 1.
- [[COCONUT]] — also covered by the latent-thought regime.
- [[LoopLM]] — the model family the theorems apply to.
