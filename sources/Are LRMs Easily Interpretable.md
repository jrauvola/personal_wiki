---
type: source
title: "Are Latent Reasoning Models Easily Interpretable?"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/interpretability
  - type/source
status: read
related:
  - "[[Ouro]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[Sarah Wiegreffe]]"
sources:
  - "[[.raw/papers/2604.04902-lrm-interpretable]]"

source_type: paper
arxiv_id: "2604.04902"
venue: "arXiv"
date_published: 2026-04-06
authors:
  - "Connor Dilgren"
  - "Sarah Wiegreffe"
url: "https://arxiv.org/abs/2604.04902"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "On logical reasoning datasets (PrOntoQA, ProsQA), Coconut and CODI predictions are almost entirely unchanged with zero latent tokens — latent reasoning tokens are often unnecessary for the model's final answer; this partially explains why LRMs fail to consistently beat explicit-CoT methods."
  - "When latent tokens ARE necessary, gold natural-language reasoning traces can be decoded from latent vectors via top-10 vocab projections 54-65% of the time (Coconut+GPT-2 backtracking), up to 93% counting question numbers."
  - "On correct-prediction instances, Forward-Chaining unsupervised decoding (using counterfactual prompts for verification) recovers verified natural-language traces 67% (3/3 verifications) to 93% (1/3 verifications) for Coconut+GPT-2 on GSM8k-Aug."
  - "Forward-chaining recovery rate drops up to 62 percentage points on incorrect predictions — interpretability correlates with prediction correctness."
  - "Evaluated on Coconut and CODI with GPT-2 Small and Llama-3.2-1B-Instruct backbones on GSM8k-Aug, PrOntoQA, ProsQA."
  - "Implication: current LRMs largely encode interpretable processes rather than uninterpretable ones; the 'opaque latent' narrative is overstated."

projects:
  - slug: "branch-a"
    relevance: not-applicable
    why: "Studies Coconut/CODI, not Qwen3 architecture-specific."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a stability ablation."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a probe methodology tool for Qwen3."
  - slug: "branch-d"
    relevance: primary
    why: "DIRECTLY examines CODI's latent structure (one of our two Branch D hosts alongside LT-Tuning) and finds 65-71% of gold traces recoverable with operand context. This is evidence that CODI latents encode the expected solution — so feature collapse is real but SURMOUNTABLE even without fusion. Must-read before Branch D Day 3-7."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Key anti-narrative finding: LRM latents ARE interpretable, and interpretability correlates with correctness. This is a strong anchor for our SPAR writeup's interpretability chapter; also methodologically — backtracking + forward-chaining with counterfactual verification are reusable decoding methods for Ouro latents."

last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Are Latent Reasoning Models Easily Interpretable?

> [!contradiction] CODI latent utilization vs [[Weak vs Strong Supervision Study]]
> This paper finds CODI latents encode gold traces 65-71% of the time — latents ARE used. [[Weak vs Strong Supervision Study]] finds weakly-supervised methods (including CODI) often exhibit shortcut behavior, with accuracy achieved without using latent reasoning. Tension: same latent, one audit says "used", the other says "often not used." Likely reconciled by task/dataset: logical tasks (PrOntoQA/ProsQA) show zero-latent answers unchanged (shortcut), while GSM8K-Aug arithmetic shows high decode rates. Resolution requires per-task re-audit.

## TL;DR

Empirical interpretability study of **Coconut** and **CODI** on GSM8k-Aug / PrOntoQA / ProsQA with GPT-2 and Llama-3.2-1B backbones. Two big findings:

1. **Latent reasoning tokens are often unnecessary.** On logical reasoning tasks, LRMs produce the same answer with ~zero latent tokens. This partially explains why LRMs fail to consistently beat explicit CoT.
2. **When latent tokens matter, they're decodable.** Backtracking over top-10 vocab projections recovers gold traces 54-65% of the time (93% counting question numbers); unsupervised forward-chaining with counterfactual verification verifies traces for 67-93% of correct predictions. Interpretability correlates with correctness (recovery drops 62 pp on incorrect predictions).

## Method

### Necessity tests

1. **Early-stopping:** insert `<eot>` at 0, 1, 2, …, 6 latent tokens. See which position the answer stabilizes.
2. **Multi-reasoning training:** train models in three modes (no reasoning / explicit CoT / latent) on identical data to isolate training regimen from architecture.

### Decoding methods

**Backtracking (supervised, requires gold trace):**
- Top-10 vocab projections per latent token.
- Check whether gold-trace operands and results appear.

**Forward chaining (unsupervised):**
- Assume top integer tokens are step results.
- Verify via counterfactual prompts: change operands, check whether projections shift correspondingly.
- Assemble traces backward from final answer.

## Models studied

- **Coconut** (Hao et al., 2025) on GPT-2 Small and Llama-3.2-1B-Instruct.
- **CODI** (Shen et al., 2025b) on GPT-2 Small and Llama-3.2-1B-Instruct.

## Datasets

- GSM8k-Aug (arithmetic, 1-10 steps).
- PrOntoQA (logical, 6 steps).
- ProsQA (logical, 3-6 steps).

## Key numbers

**Necessity:**

- Logical reasoning tasks → "almost zero" latent tokens needed for stable prediction.
- GSM8k-Aug → latent reasoning provides minimal advantage when controlling for training data.

**Backtracking decode rates, correct predictions only:**

| Setup | Rate |
|---|---|
| Coconut + GPT-2, original traces | 54% |
| Coconut + GPT-2, multiple-valid traces | 65% |
| Coconut + GPT-2, incl. question numbers | 93% |
| Coconut + Llama, no Q context | 8-17% |
| Coconut + Llama, with Q context | 65-71% |
| CODI, with full operand context | 65-71% |

**Forward chaining, correct predictions:**

- Coconut + GPT-2, 1/3 verifications: 93%.
- Coconut + GPT-2, 3/3 verifications: 67%.
- Drop ≤62 percentage points on incorrect predictions — **interpretability ⇔ correctness**.

## Relevance

- **Directly affects Branch D.** We plan to implement LT-Tuning CPF on CODI; this paper shows CODI latents already encode the gold trace 65-71% of the time. That means:
  - Feature collapse is not total — CODI latents have signal.
  - CPF's role is to *strengthen* or *stabilize* this signal, not to add it from scratch.
  - If CPF pushes the recovery rate from 65% → 85%+ on our probes, that's a clean success metric we hadn't defined before.
- **Reusable methodology for our Ouro probes:** forward-chaining with counterfactual verification is directly applicable to Ouro's per-step latents (the [[Quora Faithfulness Probe]] tests a similar question with linear probes; this paper's method is complementary).
- **Anti-narrative find:** the common claim that latent reasoning is "opaque" is overstated. Our writeup should cite this as a counter-framing.
- **Caveat:** tested on GPT-2 Small and Llama-3.2-1B — small scale. Unclear whether decoding rates hold at Qwen3-4B / 8B.

## SPAR empirical follow-up (2026-04-23)

Dilgren & Wiegreffe report CODI latents 65-71% decodable with operand context on GPT-2 / Llama-3.2-1B and note interpretability correlates with correctness (recovery drops up to 62pp on incorrect predictions). Our F3 on CODI V2 bf16 at Qwen3-4B-Instruct-2507 (`research_findings/inert_latent_hypothesis_tests.md`) finds 7/8 positions template-only (entropy <0.4 bits; dominant template `The → 0 → 0 → ? → . → . → . → .`), i.e. *not* per-example interpretable.

Reconciliation: (i) our decoding is a strict lower bound — logit-lens on the final layer only, no backtracking or forward-chaining with counterfactual verification; earlier-layer or multi-token decoding might recover more. (ii) Our V2 capability floor is ~16% GSM8k vs the higher-performing checkpoints they evaluate. Their interpretability-correctness correlation implies that once accuracy crosses some threshold, latents become interpretable — which maps cleanly to our taxonomy ([[Routing vs Reasoning]]): *routing-mode* is the low-accuracy regime where latents are a geometric key (F3/F5/F6), and *reasoning-mode* emerges only with capability. Our 2.8% F1 unique-correct set and 0% F5 accuracy change are consistent with a model that never escaped routing-mode.

## Cross-links

- [[Ouro]] — same interpretability question, different architecture.
- [[COCONUT]] / [[CODI]] — subjects of the paper.
- [[Quora Faithfulness Probe]] — related per-step faithfulness methodology.
