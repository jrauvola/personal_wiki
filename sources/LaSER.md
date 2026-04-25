---
type: source
title: "LaSER — Latent Space for Dense Retrieval"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - type/source
  - method/dense-retrieval
  - domain/information-retrieval
status: read
related:
  - "[[Alibaba Tongyi Lab]]"
  - "[[CODI]]"
  - "[[SIM-CoT]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2603.01425-laser]]"
source_type: paper
arxiv_id: "2603.01425"
venue: "arXiv"
date_published: 2026-03-02
authors:
  - "Jiajie Jin"
  - "Yanzhao Zhang"
  - "Mingxin Li"
  - "Dingkun Long"
  - "Pengjun Xie"
  - "Yutao Zhu"
  - "Zhicheng Dou"
url: "https://arxiv.org/abs/2603.01425"
code_repo: "https://github.com/ignorejjj/LaSER"
has_weights: false
status: read
confidence: high
key_claims:
  - "LaSER internalizes explicit query-planning reasoning directly into the latent space of the dense retriever via a self-distillation framework with a dual-view training mechanism: Explicit view maps ground-truth CoT rationale; Latent view generates K continuous thinking tokens in embedding space."
  - "Latent tokens are computed as expected embeddings t_j = p_j^T E where p_j = softmax(W_lm h_{j−1}) — a soft probability-weighted mix over the vocabulary rather than hard token selection."
  - "Process-Level Trajectory Alignment maps M explicit-rationale segments to K latent steps via uniform sampling j_i = ⌊i·M/K⌋ and aligns via KL over document-batch relevance distributions."
  - "On BRIGHT, LaSER on Qwen3-8B reaches 29.3 nDCG@10 versus 25.7 for the fair baseline (+14%) and beats rewrite-then-retrieve (28.1) by 1.2 points while being 333× faster."
  - "LaSER-0.6B (23.1) outperforms the Qwen3-8B fair baseline (25.7) — demonstrating a small latent-thinking retriever can approach an 8B non-reasoning baseline."
  - "Removing output-level distillation drops BRIGHT nDCG@10 from 23.10 to 19.97 — the largest single-component drop in the ablation."
  - "Training with K=3 or K=6 yields similar results; increasing K at inference time shows consistent performance improvements, indicating the model learns robust iterative refinement."
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Dual-view trajectory alignment is loosely analogous to fusion; orthogonal to CPF-on-CODI experiment."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling on retrieval task is outside the Qwen3 architecture-dependence finding."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Retrieval latency is orthogonal to detach/grad-stability ablations."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No relevance to Qwen3 probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: reference
    why: "Domain-specialized variant worth citing in the writeup as evidence latent reasoning generalizes beyond math-domain harnesses."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# LaSER — Latent Space for Dense Retrieval

**Paper:** "LaSER: Internalizing Explicit Reasoning into Latent Space for Dense Retrieval" — Jiajie Jin, Yanzhao Zhang, Mingxin Li, Dingkun Long, Pengjun Xie, Yutao Zhu, Zhicheng Dou — [arXiv:2603.01425](https://arxiv.org/abs/2603.01425) (Mar 2, 2026). Code: [ignorejjj/LaSER](https://github.com/ignorejjj/LaSER).

Developed by [[Alibaba Tongyi Lab]]. Specifically adapts latent reasoning to eliminate extreme latency in Information Retrieval and complex dense retriever networks.

## Core thesis

Contemporary agentic search pipelines use a rewrite-then-retrieve protocol: the LLM autoregressively generates long explicit textual rationales to formulate an optimal query before pinging the database. This introduces prohibitive multi-second latency.

LaSER neutralizes the bottleneck by internalizing explicit query-planning logic directly into the latent space of the dense retriever. A shared LLM backbone runs a **dual-view** training mechanism:

- **Explicit view** — maps the ground-truth textual reasoning path.
- **Latent view** — executes continuous implicit thought.

The critical innovation is a **Process-Level Trajectory Alignment** algorithm that synchronizes intermediate continuous states of the Latent view with the semantic progression of the explicit text, keeping continuous vectors highly informative.

## Empirical results

On the reasoning-intensive BRIGHT benchmark, LaSER matches the deep deductive capabilities of explicit CoT pipelines while using only a fraction of the latent tokens — restoring instantaneous inference efficiency required for commercial search operations.

## Integration notes

Specialized for IR / dense retrieval. Not a general-purpose latent reasoning recipe. Useful primarily as taxonomic reference that latent reasoning generalizes beyond math-domain harnesses into production retrieval workloads.
