---
type: source
title: "Implicit Chain of Thought Reasoning via Knowledge Distillation (Deng et al. 2023)"
source_type: paper
arxiv_id: "2311.01460"
venue: "arXiv (Microsoft Research)"
date_published: 2023-11-02
authors:
  - "Yuntian Deng"
  - "Kiran Prasad"
  - "Roland Fernandez"
  - "Paul Smolensky"
  - "Vishrav Chaudhary"
  - "Stuart Shieber"
url: "https://arxiv.org/abs/2311.01460"
code_repo: "https://github.com/da03/implicit_chain_of_thought"
has_weights: false
status: read
confidence: high
key_claims:
  - "Introduces 'vertical reasoning': instead of emitting CoT tokens sequentially (horizontal), the teacher's hidden states at each layer corresponding to CoT tokens are used as supervision for the student's hidden states at matching layers."
  - "Three-stage architecture: (1) Teacher — trained on explicit CoT; (2) Emulator — shallow model that predicts teacher's hidden states from prompt alone; (3) Student — uses emulator's predictions as internal scratch-pad to compute the answer."
  - "Distillation objective matches student hidden states to teacher hidden states at corresponding (CoT-token, layer) positions. The student never emits CoT tokens."
  - "GPT-2 Small on 4-digit × 4-digit multiplication: implicit-CoT matches explicit-CoT accuracy at inference speed comparable to no-CoT (≈5× faster than emitting the full CoT)."
  - "First paper to explicitly frame latent reasoning as 'reasoning across layers instead of across tokens' — the load-bearing conceptual shift that COCONUT then adopts and extends to continuous-thought feedback."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "The *direct* conceptual predecessor to both COCONUT and CODI. First paper to distill hidden-state CoT into a compact latent computation. Essential genealogy node."
  - slug: "branch-a"
    relevance: reference
    why: "GPT-2 results are pre-Qwen baseline; architecture-agnostic claim extrapolates."
  - slug: "branch-b"
    relevance: reference
    why: "Hidden-state matching loss prefigures CODI's self-distillation loss; no BPTT axis intervention."
  - slug: "branch-c"
    relevance: secondary
    why: "Hidden-state supervision methodology is directly relevant to probing what's stored in latent states."
  - slug: "branch-d"
    relevance: primary
    why: "Teacher-student hidden-state distillation is the *ur-form* of LT-Tuning / KaVa / SIM-CoT — all descend from this paper's vertical-reasoning insight."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - family/implicit-cot
  - method/knowledge-distillation
  - method/teacher-student
  - type/source
  - status/historical
related:
  - "[[Stepwise Internalization]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[KaVa]]"
  - "[[SIM-CoT]]"
  - "[[Latent Thoughts Tuning]]"
  - "[[Yuntian Deng]]"
sources: []
---

# Implicit CoT via Knowledge Distillation (Deng et al. 2023)

## TL;DR

First paper to compress CoT reasoning into hidden states. Teacher (explicit CoT) + Emulator (predicts teacher hidden states from prompt) + Student (uses emulator's hidden states as scratch-pad). GPT-2 Small on 4×4 multiplication: matches explicit-CoT accuracy at no-CoT speed. Introduces "vertical reasoning" as the conceptual frame.

## Why this matters to our project

This is the **direct conceptual predecessor** to COCONUT, CODI, LT-Tuning, KaVa, and SIM-CoT. Before Deng 2023, the mainstream framing was "compress CoT into fewer tokens" (Wei 2022 CoT, Nye 2022 Scratchpad, Zhang 2022 CoT sampling). Deng 2023 introduced the **axis shift**: compress CoT into *hidden states* across *layers* instead of into tokens across a *sequence*.

Every subsequent hidden-state distillation paper can be decomposed as a variation on Deng's teacher-student pattern:

- **COCONUT (Dec 2024):** Drops the separate emulator; lets the student's own previous hidden states serve as the scratch-pad (continuous-thought feedback). Adds staged curriculum.
- **CODI (2025):** Single-stage self-distillation. Same model is both teacher (with CoT) and student (latent mode), matches own hidden states.
- **LT-Tuning:** Adds Context-Prediction-Fusion to anchor latent trajectory to vocab space.
- **KaVa:** Compresses KV-cache from teacher and injects into student.
- **SIM-CoT:** Explicit auxiliary decoder for latent supervision.

## Method

**Three-stage architecture:**

1. **Teacher** (trained on explicit CoT data): standard next-token-prediction on prompt + CoT + answer.

2. **Emulator** (shallow, auxiliary): takes only the prompt, predicts teacher's hidden states at layer $\ell$ for each CoT token position. Loss = MSE or similar between emulator output and teacher hidden states.

3. **Student**: takes prompt + emulator's predicted hidden states (inserted as "phantom tokens" at the CoT positions), outputs the final answer *without emitting CoT tokens*. Loss = cross-entropy on answer.

**Key training signal:** Student's hidden states at CoT positions are supervised to match teacher's hidden states at the same positions.

## Results

**GPT-2 Small, 4-digit × 4-digit multiplication:**

| Method | Accuracy | Inference speed |
|--------|----------|-----------------|
| No-CoT | ≈0% | 1.0× |
| Explicit CoT | ≈100% | 0.2× (5x slower) |
| Implicit-CoT (iCoT-KD) | ≈90%+ | ≈1.0× |

## Limitations

- Requires training a separate Emulator, adding engineering overhead.
- Hidden-state matching doesn't scale trivially beyond narrow synthetic tasks (authors didn't push past 4x4 multiplication).
- Two models to deploy (Emulator + Student).

Deng's 2024 follow-up ([[Stepwise Internalization]]) drops the Emulator entirely and uses a single-model curriculum — this is what COCONUT and CODI inherit.

## Relevance to our project

This is the canonical entry point for "latent reasoning by hidden-state distillation" and should be cited in the Branch D (LT-Tuning / CPF) writeup as the *primordial* method of the family. All LT-Tuning / KaVa / SIM-CoT recipes are refinements on Deng's 2023 three-stage pattern.

## Citation links to chase

- [[Stepwise Internalization]] (Deng 2024) — simpler single-model follow-up.
- [[COCONUT]] (Hao 2024) — continuous-thought feedback variant.
- [[CODI]] — single-stage self-distillation variant.
