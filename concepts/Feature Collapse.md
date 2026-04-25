---
type: concept
title: "Feature Collapse"
created: 2026-04-22
updated: 2026-04-24
tags:
  - domain/latent-reasoning
  - type/concept
  - failure-mode
status: developing
complexity: intermediate
domain: latent-reasoning
aliases:
  - "Feature Homogenization"
  - "Latent Collapse"
  - "Representational Collapse"
related:
  - "[[SIM-CoT]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[ReGuLaR]]"
  - "[[Curriculum Distillation]]"
  - "[[ThinkRouter]]"
sources:
  - "[[.raw/papers/research.md]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Branch-d primary interest is fusion/anti-collapse methods; feature collapse is the failure mode CPF is designed to prevent."
  - slug: "branch-a"
    relevance: primary
    why: "Scaling Qwen3 past 4B surfaces collapse dynamics; this concept frames the architecture-dependence finding."
  - slug: "branch-b"
    relevance: secondary
    why: "Detach ablations partly target collapse mitigation."
  - slug: "branch-c"
    relevance: secondary
    why: "Probe methodology needs to distinguish collapse from benign convergence."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Central failure mode across the literature; required framing for the writeup."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Feature Collapse

The central failure mode of weakly supervised continuous-reasoning architectures: sequential latent representations homogenize and lose operator diversity. Without the rigid boundaries of discrete language, continuous vectors degenerate into identical, semantically void representations — destroying the model's capacity for algorithmic planning.

## Manifestations

- **Homogenization of latent representations** — continuous vectors lose semantic diversity and fail to preserve the distinct operator information necessary for complex multi-step deductions. (See [[SIM-CoT]].)
- **Scaling-induced collapse** — architectures with untied input/output embedding weights suffer severe geometric distribution mismatches when raw processed hidden states are recurrently injected back into the input layer; rapidly induces collapse after only a few sequential iterations.
- **Catastrophic degradation at scale** — canonical baselines like [[COCONUT]] plummet to ~41.5% accuracy at 8B parameter scale due to unchecked feature homogenization.
- **Shortcut mappings** — weak supervision leaves intermediate latent states unconstrained; models adopt superficial shortcut mappings rather than internalizing genuine algorithmic logic. (See [[CODI]]'s degenerative shortcut behavior noted in `PROJECT_STATE.md:82`.)
- **Confidence pathology under Soft Thinking** — per [[ThinkRouter]], reasoning trajectories ending in incorrect answers contain FEWER low-confidence steps than correct ones. Low-probability soft embeddings aggregate multiple incompatible alternatives, propagating noise that leads to false high downstream confidence. A distinct manifestation of collapse in the training-free inference regime (soft embeddings degenerate into noisy high-confidence aggregates rather than semantic slots).
- **Layer-asymmetric entropy collapse** — per [[Latent Exploration Decoding]] (LED, round-2 crawl), post-RL LRMs exhibit collapsed final-layer entropy while intermediate layers retain high entropy. Refines the aggregate-collapse picture: collapse is layer-asymmetric, and intermediate layers are a reservoir of preserved diversity that decoding-time interventions (LED, [[SeLaR]], [[ThinkRouter]]) can draw from. [[Latent Thinking Optimization]] (round-2 crawl) gives a parallel finding for Huginn: process-reward signal is visible to a reward classifier but invisible to logit lens — same layer/readout asymmetry.

## Mitigations surveyed

| Method | Mechanism |
|---|---|
| [[Latent Thoughts Tuning]] | [[Context-Prediction-Fusion]] — `e_fusion = α · h_ctx + (1−α) · e_pred` anchors the latent trajectory to the discrete token manifold by interpolating hidden states with vocabulary-prior embeddings. Sustains 68.8% at 8B where COCONUT collapses to 41.5%. |
| [[SIM-CoT]] | Training-only auxiliary decoder anchors each latent state to a verifiable human-readable logical step via cross-entropy supervision. |
| [[ReGuLaR]] | Variational cross-modal prior from rendered-CoT visual embeddings regularizes the text model's latent posterior into a structured geometry. |
| [[COCONUT]] anti-forgetting sampling | Uniform probability interleaving of earlier-curriculum-stage data prevents catastrophic forgetting of the vocabulary mapping. |
| [[KaVa]] | Per-step KV-cache distillation from a teacher model closes the supervision gap that lets latents collapse. |
| [[ThinkRouter]] | Inference-time routing: when `p_t^max < τ`, emit a discrete token instead of the noisy soft embedding — breaks the noise-accumulation loop without any training. |
| [[OneVL]] | Dual auxiliary decoders (language + visual world-model) supervise latent tokens with both text-CoT reconstruction and future-frame prediction — generalizes SIM-CoT's single-decoder recipe to multi-modal targets. Claimed first latent CoT to surpass explicit CoT. |
| [[OneLatent]] | Compresses CoT to a single latent token with supervision from rendered-CoT images via DeepSeek-OCR hidden states — external vision-tower supervision as collapse prevention. |
| [[ALiCoT]] | Aligns latent token distributions with intermediate reasoning-state distributions; theoretically motivated by the Order-r Interaction decay theorem — formal case that distribution-alignment supervision is necessary, not stylistic. |

## Theoretical framing (2026)

[[ALiCoT]] provides the first theoretical lower-bound: on irreducible problems, the learning signal for Order-r logical dependencies **exponentially decays** when intermediate steps are skipped, creating high-order interaction barriers. This formalizes the intuition that raw latent-CoT training without explicit alignment cannot learn deep reasoning chains — collapse is not a training-hyperparameter issue but a fundamental signal-decay problem that demands anchor-to-explicit interventions.

## Cross-references

Sources that explicitly discuss this failure mode: [[Latent Thoughts Tuning]], [[SIM-CoT]], [[COCONUT]], [[CODI]], [[ReGuLaR]], [[KaVa]], [[ThinkRouter]], [[OneVL]], [[OneLatent]], [[ALiCoT]], [[Visual Enhanced Depth Scaling]], [[Latent Exploration Decoding]], [[SeLaR]], [[Latent Thinking Optimization]].

## Related failure-mode concepts (layer-asymmetric diversity preservation)

- **Mode elicitation** ([[LaDi-RL]]) — policy entropy decays under discrete RL, collapsing diversity. Latent diffusion distributes stochasticity across denoising steps to prevent mode collapse. Parallel framing to the Greedy Pitfall ([[Stochastic Soft Thinking]]).

## Empirical refinement (SPAR F1-F6, 2026-04-23)

The SPAR inert-latent F1-F6 battery on Qwen3-4B-Instruct-2507 + CODI V2 bf16 (`num_latent=8`) forces a refinement of the "feature collapse" framing for this regime. The layer-asymmetric picture the branch docs already reference (LED, LTO) extends to a per-position template asymmetry: F3 shows 7 of 8 latent positions decode (logit-lens) to a fixed string `The → 0 → 0 → ? → . → . → . → .` with <0.4 bits entropy, and only one position (step 3) shows cross-example variation. F6 shows the KV sits in a narrow geometric basin — σ=0.1 Gaussian noise is absorbed, σ=0.5 collapses accuracy from ~16% to <3%.

Critically, this is **not** monotonic collapse of the hidden state to a single point. The F5 proxy over 200 examples shows median pair cosine similarity of 0.78 (not 1.0) with 63 PCs needed for 95% variance — the latent KV carries meaningful per-example geometric content. What has collapsed is the **functional role** of the latent: it serves as a routing key to a format-prior attractor, not as a carrier of reasoning content. See [[Routing vs Reasoning]] for the functional-role framing and `research_findings/inert_latent_hypothesis_tests.md` for the full battery.

## KV PCA refinement (2026-04-24)

The PCA analysis (`research_findings/kv_pca_analysis.md`, 200 examples × 3 benchmarks × 2 variants) shows that V2 bf16 (tighter basin, GSM8k 0.163 — within-variant RMS 70.8-72.8) and V2' fp32 (looser basin, RMS 76.7-79.6, 9-10% wider) occupy **distinct sub-basins of the same manifold** — centroid cosine 0.94-0.96 and centroid distance ~40-48 vs within-radius ~70-80. Collapse here is not to a single universal point; it is to a variant-specific template sub-basin within a shared low-rank structure (top 10 PCs ≈ 67-72% variance in 2048-d). Feature collapse in this regime is better framed as *sub-basin capture* than hidden-state homogenization.

## Branch-1 layer-wise result (2026-04-24)

The layer-asymmetric probe on V2 bf16 at Qwen3-4B (`research_findings/layer_probe/v2_bf16_step3/layer_asymmetric_probe_v2_bf16.md`, 500 GSM8k examples, step 3) confirms collapse here is a **final-6-layer phenomenon**, not stack-wide and not monotone. Geometric dispersion traces a U across 37 layers: rises from embed through L22-L30 (median pair cos 0.966 at L28; top-1 PC variance 0.137 at L30; 95%-PC count 213 at L22), then re-collapses sharply at L31-L36 (final L36: pair cos 0.989, top-1 PC 0.310 — 2.27× the trough; 95%-PC count 82 — 38% of the mid-stack peak). Aligns with [[Latent Exploration Decoding]] and [[Latent Thinking Optimization]]'s broader layer-asymmetric-collapse framing for post-RL LRMs / Huginn — same readout-versus-internal-state asymmetry, now pinned in the CODI V2 bf16 regime.
