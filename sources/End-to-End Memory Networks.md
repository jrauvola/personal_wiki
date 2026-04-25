---
type: source
title: "End-to-End Memory Networks (Sukhbaatar, Szlam, Weston, Fergus 2015)"
source_type: paper
arxiv_id: "1503.08895"
venue: "NeurIPS 2015"
date_published: 2015-03-31
authors:
  - "Sainbayar Sukhbaatar"
  - "Arthur Szlam"
  - "Jason Weston"
  - "Rob Fergus"
url: "https://arxiv.org/abs/1503.08895"
code_repo: "https://github.com/facebook/MemNN"
has_weights: false
status: read
confidence: high
key_claims:
  - "End-to-End Memory Networks (MemN2N) replace the strong-supervision per-hop loss of Weston 2014 Memory Networks with end-to-end backprop through a soft attention over discrete memory slots: p_i = Softmax(u^T m_i), o = Σ_i p_i c_i."
  - "Multi-hop memory access stacks K layers (typically K=3) with the query state accumulating: u^{k+1} = u^k + o^k (or H u^k + o^k for layer-wise weight tying). Multi-hop is verified to outperform single-hop on bAbI tasks requiring multi-step reasoning."
  - "Linear-Start (LS) training: remove the softmax on attention layers, train as linear model until validation loss plateaus, then re-insert softmax. This trick is load-bearing - without LS, attention collapses to a single slot."
  - "Position Encoding (PE) and Temporal Encoding (TE) are required for non-bag-of-words representation. l_{kj} = (1 − j/J) − (k/d)(1 − 2j/J) for PE; T_A(i), T_C(i) learned matrices for TE."
  - "On bAbI 1k joint training: 13.9% mean error (PE+LS+RN, 3 hops). Strong-supervision baseline: 3.2%. On bAbI 10k: 4.2% mean error - approaches strong supervision performance with no per-hop labels."
projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Founding paper for end-to-end soft-attention over discrete memory - the conceptual prior for any 'attend to a side-channel of discrete tokens' mechanism, including Latent Scratchpad's attend-back via past_kv."
  - slug: "branch-d"
    relevance: secondary
    why: "Multi-hop attention over a memory bank is the structural ancestor of how Latent Scratchpad expects subsequent latent positions to attend back to emitted notes. The 'Linear-Start' training trick is directly applicable to the gate-init phase of W3.5."
  - slug: "branch-a"
    relevance: reference
    why: "Pre-Transformer; not in modern scaling lineage."
  - slug: "branch-b"
    relevance: reference
    why: "Differentiable memory-attention is the grandparent of CODI's KV-cache-as-memory pattern."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/memory-augmented-networks
  - family/external-memory
  - type/source
  - status/historical
related:
  - "[[Neural Turing Machines]]"
  - "[[Differentiable Neural Computer]]"
  - "[[Latent Scratchpad Architecture]]"
  - "[[Sainbayar Sukhbaatar]]"
  - "[[Jason Weston]]"
sources: []
---

# End-to-End Memory Networks (Sukhbaatar et al. 2015)

## TL;DR

First fully end-to-end soft-attention model over a bank of discrete memory slots. Replaces strong-supervision Memory Networks (Weston et al. 2014) with backprop-only training. Stacks K=3 attention "hops" over the same memory; attention is a softmax over slot-similarity scores. Achieves competitive bAbI performance with no per-hop supervision.

## Why this matters for the Latent Scratchpad

MemN2N is the **founding paper** for "attend over a discrete memory bank with end-to-end backprop." The key property — backprop flows through the softmax distribution over slots, not through discrete picks — is exactly the property W3.5's scratchpad needs. The notes are discrete vocab tokens, but subsequent latent positions attend over them through standard softmax attention, which is differentiable.

The Linear-Start (LS) training trick is directly relevant to W3.5's gate-init problem (gate collapse). Without LS, attention collapses to a single slot; with LS, the model first learns the linear "average over all slots" solution, then sharpens. W3.5's analogous recipe: initialize gate with bias `-2.0` (mostly-off) so the model first learns the no-emission solution, then unfreezes / sharpens.

## Method (verbatim equations)

**Single-layer attention (memory slot i):**
```
p_i = Softmax(u^T m_i)
o = Σ_i p_i c_i
```
where `{m_i}` are input-side memory embeddings, `{c_i}` are output-side memory embeddings, and `u` is the query/state.

**Multi-hop (adjacent weight tying):**
```
u^{k+1} = u^k + o^k
```

**Multi-hop (layer-wise weight tying):**
```
u^{k+1} = H u^k + o^k
```
where H is a learned linear transformation between hops.

**Position Encoding (PE):**
```
m_i = Σ_j l_j ⊙ (A x_{ij})
l_{kj} = (1 − j/J) − (k/d)(1 − 2j/J)
```
encodes word position within a sentence.

**Temporal Encoding (TE):**
```
m_i = Σ_j A x_{ij} + T_A(i)
c_i = Σ_j C x_{ij} + T_C(i)
```
where `T_A(i), T_C(i)` are learned matrices that encode the sentence's position in the story.

**Final answer:** `â = Softmax(W (o^K + u^K))`.

## Training tricks

- **Linear-Start (LS):** "commencing with the softmax in each memory layer removed, making the model entirely linear except for the final softmax for answer prediction. When the validation loss stopped decreasing, the softmax layers were re-inserted and training recommenced."
- **Random Noise (RN):** add random null memories to inputs to regularize.
- **Optimizer:** SGD, learning rate η = 0.01, anneal η/2 every 25 epochs until 100 epochs total. **No momentum or weight decay.**
- **Gradient clipping:** norm clipped at 40.

## Scale and results

- bAbI 1k joint: **13.9% mean error** with PE+LS+RN, 3 hops.
- bAbI 10k joint: **4.2% mean error** (with non-linearity for tasks 17, 19).
- Strong-supervision baseline (per-hop labels): 3.2%.
- Failed tasks (>5% error) on 1k: **11 of 20**. On 10k: **4 of 20**.
- Penn Treebank LM: 121 ppl (matches LSTM baselines).
- Text8 LM: 154 ppl.

## Failure modes / limitations

- **Attention collapse without LS:** softmax sharpens too quickly during early training and gets stuck in a single-slot mode.
- **Tasks 17 (positional reasoning) and 19 (path-finding)** require explicit non-linearity (ReLU between hops); attention alone is not expressive enough.
- **Memory grows linearly** with input length — pre-LLM era assumption that doesn't transfer to scaling.
- **Discrete slots, not learned representations** — the memory bank is a fixed bag-of-input-sentences, not learned.

## Direct mapping to W3.5 Latent Scratchpad

**BORROW: the Linear-Start training schedule.** The gate-init problem in W3.5 (Stage A: gate_init_bias = -2.0, low emission; Stage B: sharpen) is the same structural choice MemN2N's authors made for the same reason. **BORROW: multi-hop attention over the memory bank** — W3.5's scratchpad notes need to be attended over multiple times by subsequent latent positions; standard transformer self-attention provides this for free, but the conceptual frame "scratchpad = memory bank, latents = K-hop queries over it" is the right mental model. **IGNORE: explicit position/temporal encodings** for memory slots — the LLM's positional embeddings already cover this.

## Citation links to chase

- [[Neural Turing Machines]] — adjacent external-memory paper from the same year.
- [[Sainbayar Sukhbaatar]] — entity page.
- [[Jason Weston]] — entity page (lead author of original Memory Networks 2014).
- [[Discrete Gate Training]] — concept page covering Gumbel-STE / REINFORCE / soft-relaxation tradeoffs.
