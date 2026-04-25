---
type: meta
title: "Project Registry"
updated: 2026-04-22
---

# Project Registry

Active research projects. The `wiki-ingest` and `wiki-autoreview` skills consult this file to assign per-source relevance tiers.

Tier semantics:
- **primary** — recipe / method we'd actually implement or directly cite. Top of project reading queue.
- **secondary** — partial signal: a technique, ablation, or benchmark worth borrowing.
- **reference** — context-only: know it exists, don't re-read unless scope expands.
- **not-applicable** — paper does not touch this project's concerns.

---

## branch-a — Stable Qwen3 Scaling

**Status:** active
**Goal:** Scale Qwen3-4B → Qwen3.5-9B after the Gemma-3 Q/K RMSNorm finding. Write "latent reasoning is architecture-dependent" finding.
**Primary interest:** architecture-dependent latent reasoning, scaling recipes, Qwen-family configs.
**Secondary:** baselines worth copying wholesale, grad stability at scale.
**Reference:** broader latent reasoning taxonomy.
**Source spec:** [[2026-04-17 Latent Reasoning Investigation Design]] § 6.1

---

## branch-b — Minimum-Sufficient Detach Ablation

**Status:** active
**Goal:** Ablate minimum-sufficient variant across V2/V3/V4 + fp32 axes. Scale simplest winner to 9B.
**Primary interest:** detach / fp32 sufficiency, grad-stability diagnostics, KV-cache detach strategies.
**Secondary:** truncated BPTT variants, KaVa-style truncation.
**Source spec:** [[2026-04-17 Latent Reasoning Investigation Design]] § 6.2

---

## branch-c — Qwen3 Convergence Contradiction

**Status:** conditional (active only if Qwen3 diverges with Gemma-specific pathology)
**Goal:** Investigate probe methodology + Qwen3 config for bugs.
**Primary interest:** probe methodology validity, Qwen3 configuration debugging, architecture diagnostics.
**Source spec:** [[2026-04-17 Latent Reasoning Investigation Design]] § 6.3

---

## branch-d — LT-Tuning CPF on CODI

**Status:** active (highest-value scientific branch if universal/diverged)
**Goal:** Implement LT-Tuning Context-Prediction-Fusion on CODI as Days 3-7 primary experiment.
**Primary interest:** fusion mechanisms, anchor-to-vocab-space tricks, 8B scaling recipes, anti-collapse methods.
**Secondary:** related failure-mode analysis (SIM-CoT auxiliary decoder, KaVa distillation, feature-collapse literature).
**Reference:** general latent reasoning methods.
**Source spec:** [[2026-04-17 Latent Reasoning Investigation Design]] § 6.4

---

## spar-latent-reasoning — Umbrella

**Status:** evergreen
**Goal:** SPAR fellowship writeup — interpretability of continuous CoT; north-star: a workable larger latent reasoning model synthesizing V2 / SIM-CoT / LT-Tuning lessons.
**Primary interest:** methods we're actively running or citing; taxonomic framing papers.
**Secondary:** methodology critiques, interpretability techniques for latent spaces.
**Reference:** broader latent reasoning literature.

---

## How to update this file

- Add a new project section when a new branch opens.
- Move `status:` to `closed` when a branch is finished; autoreview will downgrade `primary` sources to `reference` for closed projects on the next sweep.
- Primary/secondary interest lines are the actual inputs to tier assignment — make them concrete (techniques, benchmarks, scaling claims), not vague ("latent reasoning").
