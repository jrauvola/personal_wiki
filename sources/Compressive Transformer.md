---
type: source
title: "Compressive Transformers for Long-Range Sequence Modelling (Rae et al. 2020)"
source_type: paper
arxiv_id: "1911.05507"
venue: "ICLR 2020"
date_published: 2019-11-13
authors:
  - "Jack W. Rae"
  - "Anna Potapenko"
  - "Siddhant M. Jayakumar"
  - "Timothy P. Lillicrap"
url: "https://arxiv.org/abs/1911.05507"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "Compressive Transformer extends Transformer-XL with a SECOND-tier compressed memory: short-term FIFO memory of n_m past activations + long-term compressed memory of n_cm slots, each storing c past activations compressed via f_c."
  - "Compression function f_c options tested: max/mean pooling, 1D conv (learnable), dilated conv, most-used-attention. Most-used + content-based attention-reconstruction loss is the best training signal."
  - "Auxiliary attention-reconstruction loss: L^attn = ||attn(h, old_mem) - attn(h, new_cm)||_2. Reconstructs content-based attention over compressed memories rather than original ones - lossy compression that preserves task-relevant information."
  - "Compression rates c ∈ {2,3,4} tested. Enwik8: c=3 optimal (0.97 BPC); WikiText-103: c=4 optimal (17.1 ppl); RL: c=4 best."
  - "PG-19 benchmark numbers: 36-layer Compressive Transformer = 33.6 test ppl vs 36-layer Transformer-XL baseline = 36.3. Adam optimizer, linear warmup 1e-6 to 3e-4, cosine decay back to 1e-6."
projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Establishes that learned compression of past activations into a compressed memory store is trainable end-to-end at LM scale - the conceptual prior for Latent Scratchpad's 'gate decides what gets compressed/written to side-channel.'"
  - slug: "branch-d"
    relevance: secondary
    why: "Two-tier memory (recent FIFO + compressed long-term) is parallel to W3.5's 'latent past_kv + emitted scratchpad notes' two-channel pattern. Borrow the attention-reconstruction loss design."
  - slug: "branch-a"
    relevance: reference
    why: "Pre-large-model era; predates LLaMA-class scale."
  - slug: "branch-b"
    relevance: reference
    why: "Different memory pattern; not directly applicable."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/external-memory
  - family/compressed-memory
  - type/source
  - status/historical
related:
  - "[[Transformer-XL]]"
  - "[[Latent Scratchpad Architecture]]"
sources: []
---

# Compressive Transformers for Long-Range Sequence Modelling

## TL;DR

Two-tier memory transformer: a short-term FIFO memory (size n_m) holds recent activations, and a long-term compressed memory (size n_cm) holds older activations compressed by a function f_c at rate c. Auxiliary attention-reconstruction loss trains f_c to preserve content the attention layer would have used. Sets PG-19 SoTA at ~33.6 test ppl.

## Why this matters for the Latent Scratchpad

Compressive Transformer is the **closest published analog** for "two parallel memory channels with learned content-aware compression." The structural pattern is exactly what W3.5 instantiates: primary stream (latent past_kv) + secondary stream (compressed/emitted scratchpad notes). The key insight — **attention-reconstruction loss is the right training signal for compression** — is directly transferable to W3.5's L_decode loss design.

In W3.5 terms: the "compression function f_c" maps to "the Note Head + emission gate," and "attention-reconstruction loss" maps to "the scratchpad note must be useful enough that subsequent latent positions can attend over it and still get the right answer."

## Method

**Two-tier memory:**
- Short-term FIFO memory `mem` of size n_m past activations (per layer).
- Long-term compressed memory `cm` of size n_cm slots, each from compressing c past activations: `cm_t = f_c(mem_{t-c:t})`.

**Compression functions tested:**
- Max / mean pooling (kernel = stride = c).
- 1D convolution (learnable).
- Dilated convolution (learnable).
- Most-used-attention (sort by avg attention, keep top-k).

**Best combination:** content-based 1D conv + attention-reconstruction loss.

**Attention-reconstruction loss** (Algorithm 2):
```
L^attn = L^attn + ||attn(h^(i), old_mem^(i)) − attn(h^(i), new_cm^(i))||_2
```
Reconstructs the layer-i attention pattern over **compressed** memories vs. the original. This is content-aware lossy compression: only keep what attention would have used.

**Compression rate** c ∈ {2, 3, 4}. Enwik8: c=3 (0.97 BPC). WikiText-103: c=4 (17.1 ppl). RL: c=4.

## Scale and results

- **PG-19** (open-vocab books LM, the paper's headline benchmark): 36-layer Compressive Transformer = **33.6 test ppl** vs 36-layer Transformer-XL = 36.3.
- **WikiText-103**: 17.1 ppl (vs Transformer-XL 18.3).
- **Enwik8**: 0.97 BPC.
- **Speech (WaveNet-class task)**: ~40M params, beats WaveNet and Transformer-XL.

**Optimizer:** Adam, linear warmup 1e-6 → 3e-4, cosine decay back to 1e-6.

## Failure modes / limitations

- "the main limitation of this work is additional complexity, if the task one wishes to solve does not contain long-range reasoning then the Compressive Transformer is unlikely to provide additional benefit."
- Temporal range is bounded by `l × (n_m + c × n_cm)` (number of layers × per-layer total memory).
- Compression is **per-layer**, not global — memory cost scales linearly with depth.

## Direct mapping to W3.5 Latent Scratchpad

**BORROW: the attention-reconstruction loss design.** L_decode in W3.5 should ideally test "if the scratchpad notes are present, can subsequent latent positions reproduce the attention pattern they would have had with the full latent stream?" — direct analog of Compressive Transformer's L^attn. This is an alternative to the "match teacher CoT step summary" supervision currently in the W3.5 plan, and may be more robust to teacher-noise. **BORROW: two-tier memory framing** — the W3.5 spec implicitly treats latents as Tier 1 and scratchpad as Tier 2; Compressive Transformer is a published precedent. **IGNORE: per-layer compression** — W3.5's scratchpad is per-rollout, not per-layer.

## Citation links to chase

- [[Transformer-XL]] — direct architectural predecessor (segment recurrence baseline).
- Memorizing Transformers (Wu, Rabe, Hutchins, Szegedy 2022, ICLR, arXiv:2203.08913) — kNN-memory cousin at larger scale (no separate source page; cited inline).
- [[Latent Scratchpad Architecture]] — concept page.
