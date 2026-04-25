---
type: source
title: "Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context (Dai et al. 2019)"
source_type: paper
arxiv_id: "1901.02860"
venue: "ACL 2019"
date_published: 2019-01-09
authors:
  - "Zihang Dai"
  - "Zhilin Yang"
  - "Yiming Yang"
  - "Jaime Carbonell"
  - "Quoc V. Le"
  - "Ruslan Salakhutdinov"
url: "https://arxiv.org/abs/1901.02860"
code_repo: "https://github.com/kimiyoung/transformer-xl"
has_weights: true
status: read
confidence: high
key_claims:
  - "Segment-level recurrence: hidden states from the previous segment are concatenated to the current segment as memory: h̃ = [SG(h_τ) ∘ h_{τ+1}]. The previous-segment states are STOP-GRADIENT — recurrence is forward-only, no BPTT through segment boundaries."
  - "Relative positional encoding decomposes attention into 4 terms: (a) content-based addressing (q-k similarity, position-independent), (b) content-dependent positional bias (q × R relative encoding), (c) global content bias (learned u × keys), (d) global positional bias (learned v × R)."
  - "WikiText-103: 18.3 ppl (151M params); enwik8: 0.99 bpc (277M params). 1,800x faster evaluation than vanilla transformer due to segment caching."
  - "Effective context: 80% longer than RNNs and 450% longer than standard transformers - measured by attention-decay distance."
  - "Segment-level recurrence is what makes the memory pattern: previous-segment hidden states act as a frozen memory bank that the current segment attends over via standard self-attention."
projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Foundational example of 'previous-context-as-frozen-memory' attended via standard attention - the structural template for how Latent Scratchpad's emitted notes attend back into subsequent latent positions via past_kv (notes are SG'd memory that latents query)."
  - slug: "branch-d"
    relevance: secondary
    why: "The SG(h_τ) stop-gradient on previous-segment states is precisely the pattern W3.5 needs: scratchpad notes are detached from the gradient flow at emission, but downstream latents still attend over them."
  - slug: "branch-a"
    relevance: reference
    why: "Standard transformer architecture; not in scaling debate."
  - slug: "branch-b"
    relevance: secondary
    why: "Stop-gradient pattern is conceptually adjacent to detach policies in latent rollout."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/transformer
  - family/segment-recurrence
  - family/external-memory
  - type/source
  - status/foundational
related:
  - "[[Compressive Transformer]]"
  - "[[Memorizing Transformers]]"
  - "[[Latent Scratchpad Architecture]]"
sources: []
---

# Transformer-XL

## TL;DR

Transformer with segment-level recurrence (concatenate stop-gradient previous-segment hidden states as memory) and relative positional encoding (4-term decomposition). Predecessor to Compressive Transformer; first transformer to handle context fragmentation cleanly. SoTA on WikiText-103 and enwik8 at the time.

## Why this matters for the Latent Scratchpad

Transformer-XL establishes the **stop-gradient memory pattern**: previous-segment hidden states are frozen (no backprop through them) but still queried via standard attention. This is structurally identical to how W3.5's scratchpad notes interact with subsequent latent positions:

- Note is emitted at step t (gradient flows to gate + Note Head at step t).
- Note enters past_kv (frozen — no further gradient updates to its embedding).
- Steps t+1, t+2, …, t+M attend over the note via standard self-attention.

This is the published precedent that **detached memory + attention-back is a stable, working pattern** — it's not novel to W3.5; the contribution is the gated-emission decision, not the memory mechanism.

## Method

**Segment-level recurrence:**
```
h̃_{τ+1}^{n-1} = [SG(h_τ^{n-1}) ∘ h_{τ+1}^{n-1}]
q_{τ+1}^n, k_{τ+1}^n, v_{τ+1}^n = h_{τ+1}^{n-1} W_q^T, h̃_{τ+1}^{n-1} W_k^T, h̃_{τ+1}^{n-1} W_v^T
```
where `SG(·)` is stop-gradient. Queries come from the current segment only; keys/values come from the concatenated [previous, current] sequence.

**Relative positional encoding (the 4-term decomposition):**
```
A_{i,j}^rel = q_i^T W_{k,E} k_j      [content-based addressing]
            + q_i^T W_{k,R} R_{i-j}    [content-dependent positional bias]
            + u^T W_{k,E} k_j          [global content bias]
            + v^T W_{k,R} R_{i-j}      [global positional bias]
```
where `R_{i-j}` is a sinusoidal relative-distance encoding, and `u, v` are learned global biases.

## Scale and results

| Dataset | Params | Result |
|---|---|---|
| WikiText-103 | 151M | 18.3 ppl |
| enwik8 | 277M | 0.99 bpc |
| LM1B | — | competitive with prior SoTA |

Effective context length: **80% longer than RNNs, 450% longer than standard transformers** (measured via attention-decay).

Inference: **1,800× faster** than vanilla transformer evaluation due to segment caching.

## Failure modes / limitations

- **Memory size is fixed at training time** — segment cache length is a hyperparameter, not learned.
- **Stop-gradient is conservative** — gradient cannot flow back into the previous segment, which limits how much the model can adapt early-segment representations to later-segment usage.
- **Quadratic attention cost** within a segment+memory window; doesn't help with truly long single-document context.

## Direct mapping to W3.5 Latent Scratchpad

**BORROW: the SG(h_τ) stop-gradient pattern.** W3.5's emitted notes should be detached from the gradient at emission time — gradient flows to the gate + Note Head at step t, but downstream attention over the note is gradient-free. This is the cleanest training pattern and matches Transformer-XL's empirical success. **IGNORE: relative positional encoding** — modern LLM bases (Qwen3, Llama) already have RoPE, which subsumes this. **IGNORE: explicit segment caching** — past_kv in standard transformers handles this for free.

## Citation links to chase

- [[Compressive Transformer]] — direct successor (Rae 2020) with compressed second-tier memory.
- [[Memorizing Transformers]] — kNN-memory descendant.
- [[Latent Scratchpad Architecture]] — concept page.
