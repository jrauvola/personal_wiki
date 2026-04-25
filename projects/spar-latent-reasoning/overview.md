---
type: overview
title: "Overview"
updated: 2026-04-22
status: developing
---

# Latent Reasoning — Overview

## The landscape

Chain-of-thought prompting lifted LLM capability on arithmetic, symbolic, and deductive tasks by enforcing step-by-step articulation of intermediate logical processes. But discrete-token generation is an operational bottleneck: it floods the KV cache, introduces extreme inference latency, and forces the model to spend representational bandwidth on syntactic coherence rather than computation. The semantic constraints of human language are a suboptimal medium for pure mathematical and algorithmic planning.

In response, late-2025 / early-2026 research has aggressively pivoted to **latent reasoning** — bypassing the autoregressive vocabulary-decoding step and cultivating continuous, high-dimensional thought vectors. In this continuous manifold, models can hold multiple potential reasoning pathways simultaneously, enabling breadth-first search natively within hidden states.

Stabilization is the open problem. Without discrete token boundaries, sequential latent representations are prone to **[[Feature Collapse]]** (homogenization, loss of operator diversity) and to shortcut mappings that look like reasoning but aren't.

### Foundational taxonomy

The field has bifurcated along two primary axes: **supervision strength** (how tightly latent states are anchored to verifiable logic) and **trajectory compression** (how aggressively one latent vector is asked to carry multiple semantic steps).

| Method | Primary paradigm | Core innovation | Target optimization |
|---|---|---|---|
| [[SIM-CoT]] | Strong supervision | Training-only auxiliary decoder for step-wise alignment | Stabilization; prevention of feature collapse |
| [[CODI]] | Weak supervision (distillation) | Single-step $L_1$ alignment of pre-answer token | Single-stage training efficiency |
| [[COCONUT]] | Weak supervision (curriculum) | Multi-stage progressive replacement of text with continuous vectors | Emergent breadth-first search |
| [[CoLaR]] | Compression-first | Dynamic compression factor blending multiple semantic tokens | Extreme inference acceleration; token reduction |
| [[Adaptive Latent RL]] | Post-training RL | Binary halting head trained via GRPO | Dynamic compute allocation per query |
| LT-Tuning (separate migration) | Anti-collapse fusion | Context-Prediction-Fusion: hidden states + vocabulary priors | Scaling robustness at 8B+ |
| KaVa (separate migration) | KV-cache distillation | Compression and self-distillation of teacher KV matrices | Generalization to open-ended reasoning |
| [[ReGuLaR]] | Multimodal VAE | Rendered-CoT image priors regularize latent posteriors | High-fidelity compression via visual semantics |
| [[LaSER]] | Dense retrieval adaptation | Dual-view process-level trajectory alignment | Instantaneous inference for IR pipelines |
| [[PonderLM-3]] | Adaptive pretraining | Differentiable token-dependent attention mask | Token-adaptive compute at pretraining time |

### Tension the field is resolving

The central tension is between **weak supervision** (unconstrained continuous exploration — good for emergent BFS, bad for collapse and shortcuts) and **strong supervision** (anchored latent states — stable at scale, costs some vector freedom). Secondary axes: compression-first (CoLaR) vs adaptive-compute (Adaptive RL, PonderLM-3) vs cross-modal regularization (ReGuLaR) vs KV-space distillation (KaVa).

Shared cross-cutting concepts: [[Feature Collapse]], [[Curriculum Distillation]], [[Token Efficiency]], [[KV Compression]], [[GRPO]].

## Current project scope

SPAR fellowship project. North-star: a workable larger latent reasoning model built by synthesizing V2 / SIM-CoT / LT-Tuning lessons.

Active investigation branches (see [[meta/projects/REGISTRY|Project Registry]]):
- [[meta/projects/branch-a|Branch A]] — Stable Qwen3 scaling
- [[meta/projects/branch-b|Branch B]] — Minimum-sufficient detach ablation
- [[meta/projects/branch-c|Branch C]] — Qwen3 convergence contradiction investigation
- [[meta/projects/branch-d|Branch D]] — LT-Tuning CPF on CODI

## How this vault is used

1. **Ingest:** drop a paper / source into `.raw/`, run `wiki-ingest`. Creates source + entity + concept pages, tiers it per project.
2. **Crawl:** `paper-crawl` takes a seed arXiv ID from `meta/seeds.yaml`, fetches downstream citations, ingests each.
3. **Autoreview:** `wiki-autoreview` runs on a schedule, re-grades every source against the current registry, flags contradictions, archives stale pages.
4. **Query:** `wiki-query` pulls from index + hot cache + relevant pages, synthesizes with citations.

## Non-wiki research_findings (execution state, not knowledge)

These live outside the wiki but may be cross-linked from source pages via `[[.raw/experiments/<name>]]` stubs:
- `../research_findings/experiment_scratchpad.md`
- `../research_findings/monitor_logs/`
- `../research_findings/dgrad_probe/`
- `../research_findings/SESSION_STATE_*.md`
- `../research_findings/checkpoint_*.md`
