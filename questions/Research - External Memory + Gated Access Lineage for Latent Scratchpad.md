---
type: question
title: "Research — External Memory + Gated Access Lineage for Latent Scratchpad"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - domain/external-memory
  - domain/architecture
  - type/question
status: developing
question: "What mechanistic ancestors of Latent Scratchpad - external memory + gated access + discrete addressing - exist in the literature? Which techniques should W3.5 borrow, and which scale-validated training tricks must it adopt?"
answer_quality: solid
projects:
  - slug: spar-latent-reasoning
    relevance: primary
    why: "Taxonomic / writeup background for the W3.5 architecture; grounds the LSTM analogy in specific scale-validated published techniques."
  - slug: branch-d
    relevance: primary
    why: "Direct technique-borrowing for W3.5 implementation. Identifies 5 borrowable techniques and 3 missing training tricks the literature says are load-bearing."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Latent Scratchpad]]"
  - "[[Latent Scratchpad Architecture]]"
  - "[[Research - Latent Scratchpad Precedence]]"
  - "[[Neural Turing Machines]]"
  - "[[Differentiable Neural Computer]]"
  - "[[End-to-End Memory Networks]]"
  - "[[Mamba]]"
  - "[[RWKV]]"
  - "[[Compressive Transformer]]"
  - "[[Transformer-XL]]"
  - "[[RETRO]]"
  - "[[Neural Turing Machine Memory Access]]"
  - "[[Selective State-Space Model]]"
  - "[[Discrete Gate Training]]"
  - "[[Alex Graves]]"
  - "[[Sainbayar Sukhbaatar]]"
  - "[[Jason Weston]]"
  - "[[Albert Gu]]"
  - "[[Bo Peng]]"
sources:
  - "[[Neural Turing Machines]]"
  - "[[Differentiable Neural Computer]]"
  - "[[End-to-End Memory Networks]]"
  - "[[Mamba]]"
  - "[[RWKV]]"
  - "[[Compressive Transformer]]"
  - "[[Transformer-XL]]"
  - "[[RETRO]]"
---

# Research — External Memory + Gated Access Lineage for Latent Scratchpad

> **Question:** Mechanistic ancestors of Latent Scratchpad — external memory + gated access + discrete addressing. Where in the literature does each W3.5 design choice come from, and what training tricks does the literature say are load-bearing that W3.5 currently lacks?

## Overview

This synthesis maps the literature ancestry of [[Latent Scratchpad]] across three threads:

1. **External memory + gated write/read** — the NTM → DNC → MemN2N → modern lineage.
2. **Modern at-scale gated-state architectures** — Mamba and RWKV as proof that LSTM-style gates survive scaling to multi-billion params.
3. **Memory-as-side-channel transformers** — Transformer-XL, Compressive Transformer, RETRO, Memorizing Transformers.

Across these, **the LSTM analogy in [[Latent Scratchpad]] is well-grounded**: gating mechanisms are not historical artifacts; they are the dominant mechanism in modern non-attention LLM architectures (Mamba 2.8B, RWKV 14B). The user's intuition that W3.5's emission gate is "like LSTMs-vs-RNNs" maps onto Mamba's Theorem 1 directly: input-dependent discretization **IS** LSTM-style gating, mathematically identified.

## Key findings

### Finding 1: NTM/DNC are the conceptual root, but predate modern gradient stability tricks

[[Neural Turing Machines]] (Graves 2014) and [[Differentiable Neural Computer]] (Graves 2016 Nature) established the founding pattern: **end-to-end-differentiable read/write heads with content-based + location-based addressing, all trained by gradient descent without REINFORCE.** Key equations and training facts:

- Content-based: `w_t^c(i) = exp(β_t · K[k_t, M_t(i)]) / Σ_j exp(...)` (Source: [[Neural Turing Machines]])
- Interpolation gate: `w_t^g = g_t · w_t^c + (1 − g_t) · w_{t-1}` — the canonical "stay vs move" gate (Source: [[Neural Turing Machines]])
- DNC adds gated allocation-vs-content write: `w_t^w = g_t^w [g_t^a a_t + (1 − g_t^a) c_t^w]` (Source: [[Differentiable Neural Computer]])
- Optimizer: RMSprop with momentum 0.9, gradient clipping (-10, 10), no REINFORCE (Source: [[Neural Turing Machines]])

NTM/DNC training tricks have been mostly subsumed by modern transformer training infrastructure. The conceptual contribution survives; the implementation does not. (Confidence: high.)

### Finding 2: MemN2N's Linear-Start trick is the canonical "soft-then-hard" curriculum

[[End-to-End Memory Networks]] (Sukhbaatar 2015) replaced strong-supervision Memory Networks with end-to-end backprop through soft attention. Critical training trick:

> "In linear start (LS) training, commencing with the softmax in each memory layer removed, making the model entirely linear except for the final softmax for answer prediction. When the validation loss stopped decreasing, the softmax layers were re-inserted and training recommenced." (Source: [[End-to-End Memory Networks]])

This is **structurally identical** to the W3.5 plan's Stage A → Stage B curriculum: start with a soft / mostly-off gate, then sharpen. **The W3.5 plan already incorporates this implicitly**, but should cite MemN2N as precedent. (Confidence: high.)

### Finding 3: Mamba Theorem 1 makes the LSTM analogy mathematical, not just rhetorical

[[Mamba]] (Gu & Dao 2023) introduces input-dependent SSMs (selection mechanism) and proves:

> "the discretization is the principled foundation of heuristic gating mechanisms"

Theorem 1: for N=1, A=-1, B=1, the selective recurrence becomes
```
g_t = σ(Linear(x_t)); h_t = (1 − g_t) h_{t-1} + g_t · x_t
```
which **is** the canonical LSTM forget gate. Validated at 2.8B params. (Source: [[Mamba]], [[Selective State-Space Model]])

This is the load-bearing reference for the LSTM analogy in [[Latent Scratchpad]]: input-dependent gates work at LLM scale, full stop. (Confidence: high.)

### Finding 4: RWKV scales LSTM-style σ-gate to 14B

[[RWKV]] (Peng et al. 2023) demonstrates per-channel sigmoid gates `o_t = W_o · (σ(r_t) ⊙ wkv_t)` at **14B parameters**, the largest dense RNN ever trained. (Source: [[RWKV]])

Combined with Mamba, this is conclusive evidence that gating mechanisms are not LSTM-era nostalgia but the dominant mechanism in non-attention LLM architectures. (Confidence: high.)

### Finding 5: Compressive Transformer's attention-reconstruction loss is the right L_decode design

[[Compressive Transformer]] (Rae 2020) trains learned compression of past activations using:

> "L^attn = ||attn(h, old_mem) − attn(h, new_cm)||_2"

This is **content-aware lossy compression**: the compressed memory must produce attention patterns that match the uncompressed memory. Direct analog to W3.5's L_decode: scratchpad notes must be **useful enough that subsequent latent positions can attend over them and reproduce the original answer**.

**This is more robust than the "match teacher CoT step summary" supervision currently in the W3.5 plan**, because it doesn't depend on noisy teacher alignment. (Source: [[Compressive Transformer]]) (Confidence: medium — the analogy is structural; Rae's loss was for hidden states, not vocab tokens.)

### Finding 6: RETRO-fitting is the scaling recipe — frozen base + lightweight new heads

[[RETRO]] (Borgeaud 2022) demonstrated that retrieval can be **bolted onto a pretrained transformer with ~3% additional pretraining tokens**, and the retriever weights stay frozen. (Source: [[RETRO]])

This is the procedural template for W3.5's "init from CODI checkpoint, train gate + head only" recipe. It's encouraging that RETRO-fitting works with 3% extra data — implies W3.5's training budget should be sufficient. (Confidence: high.)

### Finding 7: Memorizing Transformers' per-head learnable gate over memory access is a missing W3.5 ablation

Memorizing Transformers (Wu, Rabe, Hutchins, Szegedy 2022, ICLR, arXiv:2203.08913) (Wu 2022) added a kNN-augmented attention to a single layer; some heads converge to ignoring the memory (g≈0) while others heavily use it (g≈1). **Per-head specialization emerges naturally.** (Source: Memorizing Transformers (Wu, Rabe, Hutchins, Szegedy 2022, ICLR, arXiv:2203.08913))

The W3.5 plan currently treats all attention heads identically when attending over scratchpad notes. **Adding a per-head learnable gate (sigmoid bias on attend-to-scratchpad logits) is a low-cost ablation** that matches Memorizing Transformers' empirical finding. (Confidence: medium.)

### Finding 8: Stop-gradient pattern from Transformer-XL is the cleanest scratchpad-attention training pattern

[[Transformer-XL]] (Dai 2019) uses `h̃ = [SG(h_τ) ∘ h_{τ+1}]` — previous-segment hidden states are stop-gradient frozen, current segment attends over them via standard self-attention. This is **the cleanest-trained pattern for "attend over a frozen memory"** in the transformer family. (Source: [[Transformer-XL]])

W3.5's emitted notes should be detached from gradient at emission time — gradient flows to the gate + Note Head at step t, but downstream attention over the note is gradient-free. The W3.5 plan does not currently specify this explicitly. (Confidence: high.)

## What W3.5 should borrow (concrete techniques)

| Technique | Source | Where in W3.5 plan to apply |
|---|---|---|
| **σ(r) sigmoid gate parametrization** | [[RWKV]] | `scratchpad_head.py::ScratchpadGate` — already in plan; cite RWKV as scale validation. |
| **`s_Δ(x) = Broadcast_D(Linear_1(x))` then softplus for scalar-broadcast gate** | [[Mamba]] | Alternative parametrization for `gate_proj` if sigmoid causes instability. |
| **Linear-Start curriculum (soft-then-hard)** | [[End-to-End Memory Networks]] | Stage A → Stage B in `scratchpad_trainer.py` — already in plan; cite MemN2N as precedent. |
| **Attention-reconstruction loss for L_decode** | [[Compressive Transformer]] | `scratchpad_losses.py::L_decode` — REPLACE current "match teacher step summaries" with attention-reconstruction; more robust to teacher noise. |
| **Stop-gradient on emitted note embeddings** | [[Transformer-XL]] | `scratchpad_integration.py::ScratchpadCODIRollout` — explicitly detach note embeddings before they enter past_kv. |

## What W3.5 is currently missing — load-bearing training tricks the literature says you need

These are tricks the literature says are load-bearing for the architectural family but the current W3.5 plan does not specify:

### Missing trick 1: Per-head learnable gate over scratchpad attention

Memorizing Transformers (Wu, Rabe, Hutchins, Szegedy 2022, ICLR, arXiv:2203.08913) showed that **only some heads should attend over external memory** — specialization emerges. W3.5 currently treats all heads identically. **Add a per-head sigmoid gate** with init bias = 0 (50/50 per-head); let training decide which heads use the scratchpad. Cost: ~num_heads × 1 scalar per layer. Matters at 4B scale where attention head count is high.

### Missing trick 2: Explicit detach / stop-gradient on emitted note embeddings

[[Transformer-XL]]'s `SG(h_τ)` pattern is the cleanest training-stable pattern for "attend over a frozen memory." W3.5's current `scratchpad_integration.py` pseudocode doesn't explicitly detach note embeddings before they enter past_kv. **Without explicit detach, gradient will try to backprop through the note token embedding via the attention chain**, creating a coupled-loss problem that's harder to train. Add `note_emb.detach()` before append-to-past_kv. Cost: zero. Critical for stable training.

### Missing trick 3: Temperature annealing schedule for ST-Gumbel gate

[[Discrete Gate Training]] documents the recommended Jang 2017 schedule: `τ = max(0.5, exp(-r·t))` with `r ∈ {1e-5, 1e-4}`. W3.5's plan currently specifies fixed `gate_temperature: 2.0` (Stage A) → `0.5` (Stage B). **Better: continuous annealing within each stage**, not a step change. Stage A: τ from 2.0 → 1.0 over the epoch. Stage B: τ from 1.0 → 0.5 over the epoch. Avoids temperature-step-induced loss spikes.

## Novelty verification

After the deeper crawl, **the novelty claim from [[Research - Latent Scratchpad Precedence]] still holds**. No paper in the external-memory + gated-access lineage combines:
- Latent-primary backbone (CODI/COCONUT-compatible).
- Discrete vocab-readable side-channel (NOT VQ codes).
- Learned sparsity-penalized emission gate.
- Side-channel attended via standard past_kv (no separate attention layer).

Specifically:
- **NTM/DNC** are end-to-end differentiable but don't have a primary-stream/side-channel distinction (memory is the only state).
- **MemN2N** is soft-attention over a fixed memory bank, not a learned-write side-channel.
- **Compressive Transformer** has the two-tier memory pattern but compresses hidden states (opaque), not vocab tokens.
- **RETRO / Memorizing Transformers** retrieve from external sources, not emit to a side-channel.
- **Mamba / RWKV** have at-scale gating but no separate-channel architecture.

**The W3.5 contribution is the combination + the human-readable-vocab choice**, not any individual mechanism. (Confidence: high — same conclusion as the prior [[Research - Latent Scratchpad Precedence]] sweep, now confirmed against a deeper external-memory literature crawl.)

## 5 key insights about the gated-memory literature that strengthen the LSTM analogy

1. **Gates are mathematical, not heuristic.** Mamba Theorem 1 proves discretization-of-continuous-SSM is **literally** the LSTM forget-gate equation. Gates are a fundamental mechanism, not an architectural curiosity.

2. **Per-channel gating dominates per-token gating at scale.** Both Mamba (per-channel Δ) and RWKV (per-channel μ + w + σ(r)) use per-channel gates, not single per-token scalars. **W3.5's per-position scalar gate may be a simplification that hurts at 4B scale** — consider per-channel-broadcast gate as ablation.

3. **Stop-gradient + attention-back is the cleanest "memory" pattern in transformers.** Transformer-XL → Compressive → Memorizing Transformers all converge on: attend over previous-segment SG'd hidden states. W3.5's note-embedding handling should follow this exact pattern.

4. **Linear-Start / curriculum is empirically critical, not optional.** MemN2N, Compressive Transformer, RETRO all use some form of "warmup then commit" curriculum. The W3.5 plan's 2-stage Stage A → Stage B is correct; **don't try to skip it**.

5. **Per-head specialization emerges naturally if you let it.** Memorizing Transformers' per-head gate converges to a sparse mix of "uses memory / ignores memory" heads. W3.5 should expose this degree of freedom and measure whether the 4B model converges to the same pattern.

## Has W3.5's discrete-emission + human-readable-vocab combination been attempted?

**No.** All published external-memory architectures fall into two categories:

- **Continuous opaque memory** — NTM/DNC memory matrix, Compressive Transformer compressed memory, Memorizing Transformers kNN cache, all RWKV/Mamba states. Not human-readable.
- **Discrete external retrieval** — RETRO retrieves from a frozen text database; results are real text, but it's input retrieval, not gated emission to a side channel.

W3.5's combination — **gated emission of human-readable vocab tokens to a side channel attended via past_kv** — is genuinely novel within the external-memory + gated-access family. The closest precedents remain those identified in [[Research - Latent Scratchpad Precedence]]: [[Latent Sketchpad]] (vision modality), [[HRPO]] (in-stream gate), [[Token Assorted]] (VQ side-channel).

## Contradictions

> [!gap] None significant. The literature is largely consistent: gates work at scale, stop-gradient on memory is stable, soft-then-hard curricula are required.

The only mild contradiction: **Mamba paper claims attention extrapolates only 2× while selective SSMs extrapolate 4000×** — but this is on the selective-copy task specifically, not natural language. Different benchmarks give different verdicts. (Sources: [[Mamba]] Figure 5 vs general transformer LM eval.)

## Open questions for further research

- **Does per-channel gating outperform per-position gating in W3.5?** Direct ablation needed at 4B scale.
- **Does attention-reconstruction L_decode work better than teacher-summary L_decode?** Empirical question; both should be tried.
- **What is the right stop-gradient policy on emitted notes?** Full SG, partial SG (stop at note_head only), or no SG?
- **Per-head learnable gate over scratchpad — does it converge to interpretable head specialization at 4B?** Open empirical question.

## Sources

- [[Neural Turing Machines]] — Graves, Wayne, Danihelka 2014. arXiv:1410.5401. Founding paper for differentiable external memory.
- [[Differentiable Neural Computer]] — Graves et al. 2016. Nature 538, 471-476. NTM successor with allocation + temporal addressing.
- [[End-to-End Memory Networks]] — Sukhbaatar, Szlam, Weston, Fergus 2015. NeurIPS. Founding paper for end-to-end soft-attention over discrete memory.
- [[Mamba]] — Gu & Dao 2023. arXiv:2312.00752. Selection mechanism; Theorem 1 LSTM equivalence; 2.8B validation.
- [[RWKV]] — Peng et al. 2023. arXiv:2305.13048. 14B dense RNN with σ output gate.
- [[Compressive Transformer]] — Rae et al. 2020. ICLR. Two-tier memory + attention-reconstruction loss.
- [[Transformer-XL]] — Dai et al. 2019. ACL. Segment recurrence + SG memory pattern.
- [[RETRO]] — Borgeaud et al. 2022. ICML. Frozen retriever; RETRO-fitting; 25× param reduction.
- Memorizing Transformers (Wu, Rabe, Hutchins, Szegedy 2022, ICLR, arXiv:2203.08913) — referenced but not given a separate source page (cited in synthesis only; per-head learnable kNN memory gate is the key transferable technique). Skipped to respect 15-page cap.

## Notes

- **Hard cap on pages this autoresearch session: 15 created (at cap).**
- Final page split: 7 sources + 3 concepts + 4 entities + 1 synthesis = 15. Memorizing Transformers source page and Tri Dao entity page were dropped to respect the cap; their key insights are summarized inline in this synthesis (per-head gate trick) and in [[Albert Gu]] (Tri Dao kernel-engineering note).
- WebFetch count: 11. WebSearch count: 3. Round 2 sufficient — Round 3 not used.
- Pre-existing pages reused: [[Neural Turing Machines]], [[Alex Graves]], [[Latent Scratchpad Architecture]], [[Latent Scratchpad]], [[Gumbel-Softmax Latent]], [[Research - Latent Scratchpad Precedence]].
