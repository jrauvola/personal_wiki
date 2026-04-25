---
type: source
title: "RWKV: Reinventing RNNs for the Transformer Era (Peng et al. 2023)"
source_type: paper
arxiv_id: "2305.13048"
venue: "EMNLP 2023"
date_published: 2023-05-22
authors:
  - "Bo Peng"
  - "Eric Alcaide"
  - "Quentin Anthony"
  - "Alon Albalak"
  - "Samuel Arcadinho"
  - "Stella Biderman"
  - "Huanqi Cao"
  - "Xin Cheng"
  - "Michael Chung"
  - "Matteo Grella"
  - "Kranthi Kiran GV"
  - "Xuzheng He"
  - "Haowen Hou"
  - "Przemyslaw Kazienko"
  - "Jan Kocoń"
  - "Jiaming Kong"
  - "Bartlomiej Koptyra"
  - "Hayden Lau"
  - "Krishna Sri Ipsit Mantri"
  - "Ferdinand Mom"
  - "Atsushi Saito"
  - "Guangyu Song"
  - "Xiangru Tang"
  - "Bolun Wang"
  - "Johan S. Wind"
  - "Stanisław Woźniak"
  - "Ruichong Zhang"
  - "Zhenyuan Zhang"
  - "Qihang Zhao"
  - "Peng Zhou"
  - "Qinghua Zhou"
  - "Jian Zhu"
  - "Rui-Jie Zhu"
url: "https://arxiv.org/abs/2305.13048"
code_repo: "https://github.com/BlinkDL/RWKV-LM"
has_weights: true
status: read
confidence: high
key_claims:
  - "RWKV combines parallel-trainable transformer-like training with recurrent constant-memory inference. Time-mixing block: r_t = W_r·(μ_r⊙x_t + (1-μ_r)⊙x_{t-1}), k_t = W_k·(μ_k⊙x_t + (1-μ_k)⊙x_{t-1}), v_t = W_v·(μ_v⊙x_t + (1-μ_v)⊙x_{t-1})."
  - "WKV operator with exponential time decay: wkv_t = (Σ_{i<t} e^{-(t-1-i)w + k_i} ⊙ v_i + e^{u+k_t} ⊙ v_t) / (Σ_{i<t} e^{-(t-1-i)w + k_i} + e^{u+k_t}). Decay vector w is per-channel, learned, parametrized as -exp(w_init)."
  - "Output gating: o_t = W_o·(σ(r_t) ⊙ wkv_t). The sigmoid gate σ(r_t) is the LSTM-style gate that lets the model selectively pass or block the time-mixed signal."
  - "Recurrent inference reformulation: a_t = e^{-w}⊙a_{t-1} + e^{k_t}⊙v_t (numerator state); b_t = e^{-w}⊙b_{t-1} + e^{k_t} (denominator state). Gives O(d) memory and O(Td) time inference."
  - "Time-decay initialization: w_i = -5 + 8·(i/(d-1))^{0.7 + 1.3·l/(L-1)}. Lower channels decay slower; depth-dependent skew encourages hierarchy. Trained 169M / 430M / 1.5B / 3B / 7B / 14B params on Pile (330B tokens, single epoch). 14B is the largest dense RNN ever trained."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Second flagship validation (with Mamba) that gated linear-attention models scale to multi-billion parameters and remain competitive with transformers. The σ(r_t) output gate is the LSTM-style gate at LLM scale - direct analog to what Latent Scratchpad's emission gate has to do."
  - slug: "branch-d"
    relevance: secondary
    why: "RWKV's gate σ(r_t) is in the SAME stream as the wkv signal - shows the 'gate decides whether the time-mixed value passes' pattern works at scale, but doesn't directly emit to a parallel channel like W3.5 does."
  - slug: "branch-a"
    relevance: secondary
    why: "Alternative-architecture data point for whether LLM scaling laws hold for non-attention recurrent backbones."
  - slug: "branch-b"
    relevance: reference
    why: "Different recurrence pattern; not directly related to detach policy."
  - slug: "branch-c"
    relevance: reference
    why: "Architecture difference complicates direct probe transfer."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/linear-attention
  - family/gated-recurrent
  - family/rnn-revival
  - type/source
  - status/foundational
related:
  - "[[Mamba]]"
  - "[[Bo Peng]]"
  - "[[Selective State-Space Model]]"
  - "[[Latent Scratchpad Architecture]]"
sources: []
---

# RWKV: Reinventing RNNs for the Transformer Era

## TL;DR

Linear-attention RNN (no softmax over keys) with explicit per-channel exponential time decay and sigmoid output gates. Trains in parallel like a transformer; runs inference as an O(d)-memory RNN. Largest dense RNN ever trained: 14B params on the Pile.

## Why this matters for the Latent Scratchpad

RWKV is the **second** of the two paired modern validations (with [[Mamba]]) that **LSTM-style gates work at LLM scale**. The σ(r_t) output gate in the time-mixing block is the canonical LSTM output gate, applied per-channel, at 14B parameters. This directly underwrites the LSTM analogy in [[Latent Scratchpad]].

Unlike Mamba (whose gate is on the state-transition Δ), RWKV's gate is on the **output signal that flows from the time-mixed buffer back into the residual stream**. That's structurally closer to what W3.5's emission gate does: decide whether the gated signal exits the latent stream into the legible scratchpad channel.

## Method (verbatim equations)

**Time-mixing token shift:**
```
r_t = W_r · (μ_r ⊙ x_t + (1 − μ_r) ⊙ x_{t−1})
k_t = W_k · (μ_k ⊙ x_t + (1 − μ_k) ⊙ x_{t−1})
v_t = W_v · (μ_v ⊙ x_t + (1 − μ_v) ⊙ x_{t−1})
```
The μ vectors are per-channel learned mixing rates between the current token and the previous timestep.

**WKV operator with exponential decay:**
```
wkv_t = ( Σ_{i=1}^{t-1} e^{-(t-1-i)w + k_i} ⊙ v_i + e^{u + k_t} ⊙ v_t )
        ─────────────────────────────────────────────────────────────
        ( Σ_{i=1}^{t-1} e^{-(t-1-i)w + k_i} + e^{u + k_t} )
```
where `w` is a learnable per-channel decay vector and `u` separately weights the current token.

**Output gating** (the LSTM-style gate at scale):
```
o_t = W_o · (σ(r_t) ⊙ wkv_t)
```

**RNN inference reformulation:**
```
a_t = e^{-w} ⊙ a_{t-1} + e^{k_t} ⊙ v_t      (numerator state)
b_t = e^{-w} ⊙ b_{t-1} + e^{k_t}              (denominator state)
wkv_t = (a_{t-1} + e^{u+k_t} ⊙ v_t) / (b_{t-1} + e^{u+k_t})
```
Gives **O(d) memory and O(Td) time** inference.

**Time-decay initialization** (depth-dependent skew):
```
w_i = -5 + 8 · (i/(d-1))^{0.7 + 1.3·l/(L-1)}
```
Lower channels decay slower; deeper layers receive faster-decaying channels. This is a load-bearing init recipe — random init causes training instability.

## Scale and results

| Model | Params | Tokens | Pile val ppl |
|---|---|---|---|
| RWKV-169M | 169M | 330B | — |
| RWKV-430M | 430M | 330B | — |
| RWKV-1.5B | 1.5B | 330B | 7.70 |
| RWKV-3B | 3B | 330B | 7.00 |
| RWKV-7B | 7B | 330B | — |
| RWKV-14B | 14B | 330B | — |

**Largest dense RNN ever trained.** Scaling law fit (`r² = 0.994`) tracks transformer scaling.

## Failure modes / limitations

The authors explicitly acknowledge:

> "linear attention of RWKV leads to significant efficiency gains but … may also limit the model's performance on tasks that require recalling minutiae information over very long contexts."

Also:

> "increased importance of prompt engineering in comparison to standard Transformer models"

— because information bottlenecks through a single state vector per timestep.

## Direct mapping to W3.5 Latent Scratchpad

**BORROW: the σ(r_t)-style sigmoid output gate** — already the parametrization in W3.5's plan; RWKV is a successful at-scale validation. **BORROW: the depth-dependent time-decay init recipe** for the gate-emission position — early latent positions should be biased toward "no emission yet" (analog of slow decay), late positions toward "emit now" (analog of fast decay). This generalizes the user's "warmup_latent_steps = 2" constraint into a smooth init bias. **IGNORE: the WKV operator itself** — W3.5 lives inside a transformer backbone and doesn't replace attention; the RWKV-style decay is only relevant if a future variant pushes scratchpad attention into a linear/decay form.

## Citation links to chase

- [[Mamba]] — paired modern validation of gated linear models at scale.
- [[Bo Peng]] — entity page.
- [[Selective State-Space Model]] — concept page; RWKV and Mamba are kin.
- [[Latent Scratchpad]] — LSTM analogy underwritten by RWKV at 14B.
