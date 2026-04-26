---
type: meta
title: "Wiki Index"
updated: 2026-04-24T05:00:00
---

# Wiki Index

Master catalog for the Latent Reasoning research wiki.

## Quick links

- [[hot|Hot Cache]] — recent session context (read first)
- [[overview|Overview]] — executive summary / taxonomy
- [[log|Log]] — append-only change record
- [[ideas/INDEX|Ideas Index]] — research ideas parked for later + promoted-to-plan
- [[meta/projects/REGISTRY|Project Registry]] — active projects + primary interests
- [[meta/seeds|Seed Registry]] — papers pending crawl
- [[meta/FRONTMATTER-SCHEMA|Frontmatter Schema]] — authoritative schema reference

## Projects

- [[meta/projects/branch-a|Branch A — Stable Qwen3 Scaling]]
- [[meta/projects/branch-b|Branch B — Minimum-Sufficient Detach]]
- [[meta/projects/branch-c|Branch C — Qwen3 Convergence Contradiction]]
- [[meta/projects/branch-d|Branch D — LT-Tuning CPF on CODI]]
- [[meta/projects/spar-latent-reasoning|SPAR Latent Reasoning — Umbrella]]

## Research syntheses (questions/)

Top-level research questions answered by consolidated autoresearch sweeps (each is an equation-level synthesis of N sources + concepts):

- [[questions/Research - Stability Theory for Latent Recurrence|Research: Stability Theory for Latent Recurrence]] — Jacobian / Parseval / noise / DEQ / Lyapunov menu for F1-F6 routing-lock failures (2026-04-24, 7 sources + 5 concepts + 3 entities).
- [[questions/Research - Info and Distribution Constraints for Latents|Research: Info and Distribution Constraints for Latents]] — VIB / CEB / HSIC-IB / VICReg / Barlow / InfoNCE regularizers mapped to F3/F5/F6 (2026-04-24, 10 sources + 4 concepts + 1 entity).
- [[questions/Research - Disentanglement and Sparse Coding for Latents|Research: Disentanglement and Sparse Coding for Latents]] — Superposition + SAE + causal-disentanglement toolkit for F3 template-lock (2026-04-24, 5 sources + 5 concepts + 3 entities).

## Sources — papers

### Latent-reasoning methodologies (core)

- [[Latent Thoughts Tuning]] — CPF + 3-stage curriculum, anti-collapse at 8B
- [[SIM-CoT]] — Auxiliary-decoder supervision; production Llama 3.1 8B weights
- [[KaVa]] — Compressed KV-cache distillation (ICLR 2026)
- [[COCONUT]] — Foundational curriculum latent reasoning
- [[CODI]] — Single-step L1-aligned distillation
- [[CoLaR]] — Dynamic compression-factor blending
- [[Adaptive Latent RL]] — GRPO-trained halting head
- [[ReGuLaR]] — Rendered-CoT visual VAE prior
- [[LaSER]] — Latent-space dense retrieval (Alibaba Tongyi)
- [[PonderLM-3]] — Differentiable token-adaptive depth
- [[Ouro]] — Looped / iterative LM pretraining

### Stability theory foundations (new — 2026-04-24)

- [[Deep Equilibrium Models]] — Bai, Kolter, Koltun 2019; DEQ framework (fixed-point + IFT)
- [[Stabilizing Equilibrium Models by Jacobian Regularization]] — Bai, Koltun, Kolter 2021 (ICML); Hutchinson estimator
- [[Resurrecting the Sigmoid Dynamical Isometry]] — Pennington, Schoenholz, Ganguli 2017; dynamical-isometry theory
- [[Parseval Networks]] — Cisse et al. 2017 (ICML); tight-frame retraction
- [[Orthogonal Recurrent Networks]] — Vorontsov et al. 2017 (ICML); soft spectral-margin parameterization
- [[Noisy Recurrent Neural Networks]] — Lim et al. 2021 (NeurIPS); noise ≡ Jacobian-Frobenius reg
- [[Robust Learning with Jacobian Regularization]] — Hoffman, Roberts, Yaida 2019; margin = 1/Lipschitz theorem

### Information-theoretic / distribution regularizers (new — 2026-04-24)

- [[Deep Variational Information Bottleneck]] — Alemi et al. ICLR 2017; canonical VIB
- [[Conditional Entropy Bottleneck]] — Fischer 2020; tighter-bound IB with MNI target
- [[HSIC Bottleneck]] — Ma, Lewis, Kleijn AAAI 2020; kernel-based IB
- [[VICReg]] — Bardes, Ponce, LeCun ICLR 2022; variance-invariance-covariance whitening
- [[Barlow Twins]] — Zbontar et al. ICML 2021; cross-correlation decorrelation
- [[Contrastive Predictive Coding]] — van den Oord 2018; InfoNCE source
- [[InfoVAE]] — Zhao, Song, Ermon AAAI 2019; aggregated-posterior MMD
- [[Continuous Autoregressive Language Models]] — CALM Oct 2025; per-dim KL-clip for collapse
- [[KL-Regularized RL is Designed to Mode Collapse]] — Oct 2025; negative result on KL-RL
- [[Emergence of Invariance and Disentanglement]] — Achille & Soatto JMLR 2018; theory

### Disentanglement / sparse coding (new — 2026-04-24)

- [[Toy Models of Superposition]] — Elhage et al. 2022 (Anthropic); foundational superposition paper
- [[Towards Monosemanticity]] — Bricken, Templeton et al. 2023 (Anthropic); first SAE extraction
- [[Sparse Feature Circuits]] — Marks, Rager et al. 2024 (ICLR 2025); attribution patching
- [[How does Chain of Thought Think]] — 2025 (arxiv 2507.22928); first feature-level causal CoT study
- [[Step-Level Sparse Autoencoder]] — 2026 (arxiv 2603.03031); context-conditioned SAE

### Remaining ingested sources (grouped loosely by lineage)

- **Depth-recurrent / looping:** [[Huginn]] references via [[Parcae]], [[Retrofitted Recurrence]], [[Mixture of Recursions]], [[LoopFormer]], [[Encode Think Decode]], [[Depth-Recurrent Attention Mixtures]], [[AdaPonderLM]], [[Inner Loop Inference]], [[Skip a Layer or Loop it]], [[Loop Think Generalize]], [[Decoding Depth-Recurrent Transformer]], [[Two-Scale Latent Dynamics]]
- **Hybrid / routing:** [[ThinkRouter]], [[SwiReasoning]], [[HRPO]], [[SeLaR]], [[Latent Exploration Decoding]], [[Multiplex Thinking]], [[LEAD]], [[Latent Thinking Optimization]]
- **RL / curriculum / distillation:** [[RLTT]], [[LaDi-RL]], [[BFS-PO]], [[LEPO]], [[LaDiR]], [[Latent-SFT]], [[ALiCoT]], [[Capabilities and Limits of Latent CoT]], [[Soft Tokens Hard Truths]], [[Token Assorted]], [[Stochastic Soft Thinking]], [[Efficient Post-Training Refinement]], [[DART]], [[SemCoT]], [[PCCoT]]
- **Probing / interpretability / mechanism:** [[Are LRMs Easily Interpretable]], [[Weak vs Strong Supervision Study]], [[Dynamics of Latent CoT]], [[Mechanistic Analysis of Looped Reasoning LMs]], [[Reasoning by Superposition]], [[Formal CoT vs Latent]], [[Stability and Generalization in Looped Transformers]]
- **Multimodal / domain:** [[OneVL]], [[OneLatent]], [[DualCoT-VLA]], [[LaRA-VLA]], [[LatentChem]], [[JEPA-Reasoner]], [[Visual Enhanced Depth Scaling]]
- **Surveys / taxonomy:** [[Survey on Latent Reasoning]], [[Latent CoT Survey]], [[Implicit Reasoning Survey]]
- **Compression / efficiency:** [[Beyond Semantics Reasonless Tokens]], [[Soft Thinking]], [[SoftCoT Plus Plus]], [[Continuous CoT Parallel Exploration]], [[Continuous CoT Multilingual]], [[Parallel TTS Latent]], [[GTS]], [[Step-Decomposed Influence]], [[LSTR]], [[Mull-Tokens]], [[Adaptive Latent CoT Pretraining]], [[MARCOS]], [[Scaling Up TTC]], [[CoLT]], [[Latent Tokens]], [[From Growing to Looping]], [[Opaque Serial Depth]], [[Think-at-Hard]], [[System-1.5 Reasoning]], [[SynAdapt]], [[Hierarchical Reasoning Model]], [[Adaptive Loops and Memory]], [[Adaptive Latent RL]], [[One Step Forward K Steps Back]]

## Concepts

### Cross-linking hubs (pre-existing)

- [[Feature Collapse]] — central failure mode of weakly-supervised latent reasoning
- [[Context-Prediction-Fusion]] — fusion mechanism from LT-Tuning
- [[Dynamic Switching Protocol]] — confidence-gated latent insertion
- [[Curriculum Distillation]] — multi-stage progressive replacement
- [[Token Efficiency]] — inference-cost axis across latent methods
- [[KV Compression]] — cache-space compression axis
- [[KV-Cache Distillation]] — KaVa's novel supervision signal
- [[Self-Distillation]] — teacher-student sharing a backbone
- [[GRPO]] — RL objective used by Adaptive Latent RL / CoLaR
- [[LoopLM]] — Ouro's framework-level anchor
- [[Fixed-Width Depth Recurrence]] — Ouro compute axis
- [[Adaptive Exit Gate]] — Ouro halting mechanism
- [[Manipulation vs Capacity]] — Physics-of-LMs diagnostic framing
- [[Quora Faithfulness Probe]] — reusable probing protocol
- [[Shortcut Behavior]] — latent-reasoning shortcut-bypass catalog
- [[Gumbel-Softmax Latent]] — stochastic discrete-latent recipes
- [[Routing vs Reasoning]] — F-battery-grounded failure framing
- [[Loop-Mode Emission]] — decoder loop-mode architectural axis
- [[Exploration-Execution Trade-off]] — per-step exploration/exploitation
- [[Conditional Entropy Bottleneck (concept)]] (aliases CEB, Fischer Bottleneck)

### Stability theory (new — 2026-04-24)

- [[Fixed-Point Iteration]] — Picard/Banach framing for M-step latent rollout; the diagnostic lens for F3/F5/F6
- [[Deep Equilibrium Model (DEQ)]] — target architecture: IFT gradients + convergent fixed point
- [[Lyapunov Stability]] — strongest attractor-shaping framework (learned $V(z;x)$ decrease condition)
- [[Spectral Regularization]] — weight-level intervention family (Parseval, orthogonal init, spectral margin)
- [[Jacobian Constraint]] — most portable intervention menu (Frobenius, nuclear, stable-rank, spectral)

### Information / distribution regularization (new — 2026-04-24)

- [[Variational Information Bottleneck]] — canonical IB regularizer + posterior-collapse failure mode
- [[Whitening-Based Anti-Collapse]] — Barlow Twins / VICReg family, prior-free + detach-compatible
- [[Distribution Regularizer Catalog]] — equation-level menu mapping each regularizer to an F-failure

### Disentanglement / sparse coding (new — 2026-04-24)

- [[Superposition]] — core framework for F3 template-lock; position-granularity polysemanticity
- [[Sparse Autoencoder]] — primary dictionary-learning tool; JumpReLU / TopK / L1 variants
- [[Feature Absorption and Splitting]] — failure mode to watch for in naive SAE applications
- [[Matryoshka Sparse Autoencoder]] — absorption-resistant nested-width variant
- [[Causal Disentanglement]] — Locatello impossibility + Schölkopf CRL inductive-bias framing

## Entities

### People — pre-existing

[[Weihao Liu]], [[Dehai Min]], [[Lu Cheng]], [[Anna Kuzina]], [[Zhenyi Shen]], [[Yulan He]], [[Wenhui Tan]], [[Alex Ning]], [[Fanmeng Wang]], [[Jiajie Jin]], [[He Li]], [[Rui-Jie Zhu]], [[Fan Yin]], [[Xilin Wei]], [[Shibo Hao]], [[Ali Hamza Bashir]], [[Arijit Ray]], [[Bingyang Kelvin Liu]], [[Connor Dilgren]], [[Dachuan Shi]], [[DiJia Su]], [[Ferdinand Kapl]], [[Fiorenzo Parascandolo]], [[Georgios Kaissis]], [[Guan Wang]], [[Halil Alperen Gozeten]], [[Hanlin Zhu]], [[Haoqiang Kang]], [[Haoyi Wu]], [[Hayden Prairie]], [[Hugh Blayney]], [[Jindong Li]], [[Jianwei Wang]], [[Jiaxuan Zou]], [[Jiayu Liu]], [[Jingcheng Deng]], [[Jonathan Williams]], [[Junhong Wu]], [[Karthik Valmeekam]], [[Kevin Xu]], [[Markus Frey]], [[Minghan Wang]], [[Nan Jiang]], [[Natasha Butt]], [[Renyu Fu]], [[Rohin Shah]], [[Runyang You]], [[Sarah Wiegreffe]], [[Tianyu Fu]], [[Xiaoqiang Wang]], [[Xin Xu]], [[Xinyuan Wang]], [[Yadong Wang]], [[Yao Tang]], [[Yige Xu]], [[Yingqian Cui]], [[Yinhan He]], [[Yuchang Sun]], [[Yuyan Zhou]], [[Zhen Zhang]], [[Zhenrui Yue]], [[Zirui Li]]

### People — new (2026-04-24 autoresearch batch)

- [[Alex Alemi]] — VIB lead author (Google Brain)
- [[Shaojie Bai]] — primary architect of DEQ + Jacobian-regularization recipes
- [[J. Zico Kolter]] — PI of the DEQ program; co-author on stability-theory-for-neural-nets work
- [[Jeffrey Pennington]] — foundational dynamical-isometry theory (Pennington-Schoenholz-Ganguli)
- [[Nelson Elhage]] — lead of Toy Models of Superposition; Anthropic
- [[Samuel Marks]] — sparse feature circuits recipe (attribution patching + SAE)
- [[Bernhard Schölkopf]] — senior author of causal representation learning literature

### Orgs

[[InternLM]], [[Alibaba Tongyi Lab]], [[ByteDance Seed]], [[Lapisbird]], [[Adobe Research]]

### Repos

[[NeosKnight233 Latent-Thoughts-Tuning]]

### Datasets

[[GSM8k-AUG]], [[GSM8k-AUG-NL]]

## Ideas (parked + promoted)

Research ideas that aren't yet plans — or that are too big for current scope and parked as future work. Each idea page tracks its grounding papers and concepts, so retrieval is cheap when we return.

See [[ideas/INDEX|Ideas Index]] for the full catalog.

- [[ideas/Latent Scratchpad]] — latent-primary + sparse discrete vocab-readable side-channel (status: **promoted-to-plan** at `plans/wave3/W3.5_latent_scratchpad.md`)
- [[ideas/Manifold-Constrained Residual Stream (mHC)]] — DeepSeek mHC pretraining architecture as future-work parallel residual-lane home for scratchpad (status: **parked**, requires from-scratch pretraining)

## Status-at-a-glance (post 2026-04-24 autoresearch batch)

- **Sources:** 108 papers ingested (up from 86 at sweep #2). 22 added this batch (7 stability + 10 info/dist + 5 disentanglement).
- **Concepts:** 33 cross-linking hubs (up from 17). 14 added this batch (5 stability + 4 info/dist + 5 disentanglement + 1 concept-flavor CEB duplicate of the source page).
- **Entities:** 77 (up from 70). 7 people added this batch.
- **Syntheses (questions/):** 3 top-level research syntheses filed (new section).
- **Raw papers:** ~91 (some duplicates to clean in next wiki-lint pass).
- **Autoreview sweeps:** #1 on 2026-04-23 (49 sources), #2 on 2026-04-23 (86 sources). Next sweep due after autoresearch batch settles.
- **Autoresearch batches:** 1st batch 2026-04-24 — three parallel agents (stability / info / disentanglement); consolidation recorded at [[meta/autoreview/2026-04-24-autoresearch-consolidation]].

## Phase 0 verdict (2026-04-24, post-Case-C)

- **LT-Tuning Phase 0 F-battery: failed.** CPF training collapses on small-model regime; the Case C verdict consolidates the diagnosis. Canonical decision doc: `Latent_Reasoning_Project/research_findings/lt_tuning_phase0_case_decision.md`.
- **Mid-layer CPF (W1.2): still live.** Layer-asymmetric probe + middle-layer CPF kept on the active branch as the most concrete extant intervention.
- **Branch 1 CONFIRM: mid-stack content is preserved** — middle layers carry decodable content even when final-layer logit lens collapses. This is now the load-bearing prior for the pivoted research stack.
- **Primary lineage going forward: COCONUT** as the curriculum/architecture base, with mid-layer CPF as the feasible LT-Tuning carryover and Branch B/D dashboards re-scoped accordingly. See [[meta/projects/branch-b]] and [[meta/projects/branch-d]] for the post-Case-C dashboards and [[overview]] for the rolled-up framing.

## Vault hygiene (2026-04-25)

- Phase 0 wiki cleanup landed: stale `wiki/experiments/` paths corrected in 4 plans files; 25 broken `[[experiments/X]]` wikilinks fixed in `experiments.md`; CEB concept page renamed to `Conditional Entropy Bottleneck (concept).md` to disambiguate from source paper; 3 duplicate raw papers removed (2508.03440-soft-thinking-single-threaded, 2510.15522-latent-sft-superposition, 2604.04902-are-lrms-interpretable); CEB concept-vs-paper references audited across 8 files.
- See [[log#[2026-04-25] cleanup | Phase 0 wiki cleanup landed]].
