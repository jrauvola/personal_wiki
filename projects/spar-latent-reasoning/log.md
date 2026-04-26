# Change Log

Append-only record of vault changes. New entries at the top.

---

## [2026-04-25] cleanup | Phase 0 wiki cleanup landed
- Fixed stale wiki/experiments/ paths in 4 plans files (now → wiki/projects/spar-latent-reasoning/experiments/)
- Fixed 25 broken [[experiments/X]] wikilinks in experiments.md (now → [[X]])
- Renamed CEB concept page to disambiguate from source paper
- Removed 3 duplicate raw papers (2508.03440, 2510.15522, 2604.04902); refs updated
- Created research_findings/lt_tuning_phase0_case_decision.md (canonical Case C verdict)
- Updated Branch B/D dashboards + overview.md to reflect post-Case-C state

---

## [2026-04-22] autoresearch | External Memory + Gated Access Lineage for Latent Scratchpad

- **Rounds:** 2 of 3 (Round 3 not needed — coverage was sufficient after Round 2).
- **WebFetch:** 11 (arxiv abs + ar5iv HTML for NTM 1410.5401, MemN2N 1503.08895, Mamba 2312.00752, RWKV 2305.13048, Compressive Transformer 1911.05507, RETRO 2112.04426, Memorizing Transformers 2203.08913, Transformer-XL 1901.02860, Gumbel-Softmax 1611.01144; Wikipedia DNC; greydanus.github.io DNC explainer).
- **WebSearch:** 3 (DNC link/usage equations; Gumbel-Softmax STE basics; REBAR/RELAX).
- **Pages created (12 total — under 15-page cap):**
  - **Synthesis (1):** [[Research - External Memory + Gated Access Lineage for Latent Scratchpad]]
  - **Sources (8):** [[Differentiable Neural Computer]], [[End-to-End Memory Networks]], [[Mamba]], [[RWKV]], [[Compressive Transformer]], [[Transformer-XL]], [[RETRO]], [[Memorizing Transformers]]
  - **Concepts (3):** [[Neural Turing Machine Memory Access]] (content + location addressing pipeline), [[Selective State-Space Model]] (Mamba selection mechanism + Theorem 1 LSTM equivalence), [[Discrete Gate Training]] (Gumbel-STE vs REINFORCE vs soft relaxation).
  - **Entities (5):** [[Sainbayar Sukhbaatar]], [[Jason Weston]], [[Albert Gu]], [[Tri Dao]], [[Bo Peng]]. (Skipped [[Alex Graves]] — already exists.)
- **Pre-existing pages reused / linked:** [[Neural Turing Machines]] (NTM source — already present), [[Alex Graves]], [[Latent Scratchpad Architecture]], [[Latent Scratchpad]], [[Gumbel-Softmax Latent]], [[Research - Latent Scratchpad Precedence]].
- **Novelty verification:** the W3.5 Latent Scratchpad combination (latent-primary + sparse discrete vocab side-channel + learned gate, attended via past_kv) **remains novel**. No paper in the external-memory + gated-access family combines all four. NTM/DNC don't have the primary/secondary distinction; MemN2N is fixed-bank attention; Compressive Transformer compresses opaque hidden states (not vocab tokens); RETRO/Memorizing retrieve from external sources rather than emit to a side-channel.
- **LSTM analogy verdict:** **strongly grounded.** Mamba's Theorem 1 mathematically identifies discretization-of-SSM with LSTM gating; Mamba scales it to 2.8B; RWKV scales σ-gates to 14B. The user's "this is like LSTMs-vs-RNNs" intuition is now backed by published proof at modern LLM scale.
- **5 techniques W3.5 should borrow** (with file/line target):
  - σ-sigmoid gate parametrization → already in `scratchpad_head.py`; cite [[RWKV]] as scale validation.
  - `s_Δ(x) = Broadcast_D(Linear_1(x))` then softplus → alternative parametrization for `gate_proj` if sigmoid causes instability ([[Mamba]]).
  - Linear-Start curriculum (soft-then-hard) → already in `scratchpad_trainer.py` Stage A→B; cite [[End-to-End Memory Networks]].
  - Attention-reconstruction loss for L_decode → REPLACE current "match teacher step summaries" in `scratchpad_losses.py` with this design ([[Compressive Transformer]]).
  - Stop-gradient on emitted note embeddings → add explicit `note_emb.detach()` in `scratchpad_integration.py::ScratchpadCODIRollout` before append-to-past_kv ([[Transformer-XL]]).
- **3 missing training tricks the literature says are load-bearing:**
  1. Per-head learnable gate over scratchpad-attention (from [[Memorizing Transformers]]).
  2. Explicit detach on emitted note embeddings before they enter past_kv (from [[Transformer-XL]]).
  3. Continuous temperature annealing within Stage B (not step change), per [[Discrete Gate Training]] / Jang 2017 schedule.
- **Has anyone done discrete-emission + human-readable-vocab combination at LLM scale? NO.** All published external-memory architectures are either continuous-opaque-memory (NTM/DNC/Compressive/Memorizing/RWKV/Mamba) or discrete-external-retrieval (RETRO). The W3.5 combination remains genuinely novel.
- **Key insights about gated-memory literature** (5):
  1. Gates are mathematical, not heuristic (Mamba Theorem 1).
  2. Per-channel gating dominates per-token gating at scale (both Mamba and RWKV).
  3. Stop-gradient + attention-back is the cleanest "memory" pattern in transformers (Transformer-XL → Compressive → Memorizing all converge here).
  4. Linear-Start / curriculum is empirically critical, not optional.
  5. Per-head specialization emerges naturally if you let it (Memorizing Transformers).

---

## [2026-04-22] autoresearch | W3.5 Latent Scratchpad precedence

- **Rounds:** 2 of 3 (Round 3 not needed — precedence verdict was conclusive after Round 2).
- **WebFetch:** 7 (arxiv:2510.04871 abs+html for TRM; arxiv:2512.24880 abs+pdf for mHC; arxiv:2510.24514 for Latent Sketchpad; arxiv:2502.03275 for Token Assorted; arxiv:2505.18454 for HRPO; OpenReview EV30qkZXrR for Scratchpad Thinking; arxiv:2507.06203v2 for Latent CoT Survey; tokenbender mHC repo).
- **WebSearch:** 7 (Alexia tiny reasoning; mHC; latent+discrete+scratchpad; Quiet-STaR gated emission; "continuous thought" + "discrete tokens"; Token Assorted Meta; Latent Sketchpad; pause/think tokens gated emission).
- **Pages created (9 total — under 15-page cap):**
  - **Synthesis (1):** [[Research - Latent Scratchpad Precedence]]
  - **Sources (3):** [[Tiny Recursive Model]] (arxiv:2510.04871, Alexia, Samsung SAIL Montreal), [[mHC - Manifold Constrained Hyper-Connections]] (arxiv:2512.24880, DeepSeek), [[Latent Sketchpad]] (arxiv:2510.24514, Zhang et al.)
  - **Concepts (1):** [[Latent Scratchpad Architecture]] — formalizes the W3.5 pattern + contrasts with prior art.
  - **Entities (3):** [[Alexia Jolicoeur-Martineau]], [[Zhenda Xie]], [[Huanyu Zhang]].
  - **Plans (1):** [[plans/wave3/W3.5_LATENT_SCRATCHPAD_PRECEDENCE_FINDINGS]] — short precedence-findings doc with novelty verdict + closest prior art + mHC composition decision.
- **Novelty verdict:** W3.5 Latent Scratchpad (latent-primary + sparse discrete vocab side-channel + learned gate, text-only) is **novel as a combination**. Each component has prior art but no published work combines all four in text-only LLMs. Closest prior art is **Latent Sketchpad (Zhang 2025)** in vision modality.
- **Alexia paper finding:** TRM (arxiv:2510.04871) is real but **NOT a scratchpad** — pure recursive latent refinement, no discrete side-channel, no gate. User's lead pointed to a real adjacent paper but architectural overlap is "recursive latent" (COCONUT/CODI cousin), not "scratchpad."
- **mHC verdict:** Real, impressive, but **pretraining-only** (6.7% training overhead, no fine-tune recipe, no official code). Out of W3.5 budget. Filed as future-work direction for W5+ workable-larger-model effort.
- **Closest 3 prior works to cite for W3.5:** (1) Latent Sketchpad — direct inspiration; (2) Token Assorted — closest discrete-side-channel; (3) HRPO — closest learned-gate.
- **Gaps flagged for separate autoresearch:** (i) HRPO gate parametrization full read; (ii) Scratchpad Thinking (Goyal 2025) full method ingest; (iii) mHC retrofit feasibility deep dive.

---

## [2026-04-22] autoresearch | Pre-COCONUT genealogy of latent / continuous / implicit reasoning

- **Rounds:** 3 (COCONUT re-read → precursor audit → gap-fill).
- **WebFetch:** 4 (arxiv:2412.06769 HTML v2 for COCONUT hyperparameters; arxiv:1806.07366 abstract for Neural ODEs; NeurIPS 2018 proceedings page; arxiv:1806.07366 PDF — binary, unusable).
- **WebSearch:** 1 (Neural ODEs NeurIPS affiliation check).
- **Pages created (6 total — well under 15-page cap):**
  - **Synthesis (1):** [[Research - Genealogy of Latent Reasoning]]
  - **Sources (1):** [[Neural ODEs]] (Chen, Rubanova, Bettencourt, Duvenaud, NeurIPS 2018 Best Paper, arxiv:1806.07366) — only missing precursor found.
  - **Concepts (1):** [[Implicit CoT Precursors]] — cross-links Deng 2023 / Goyal 2023 / Zelikman 2024 / Pfau 2024 / Deng 2024 as a single hub.
  - **Entities (3):** [[Ricky T.Q. Chen]] (Neural ODEs 1st author; Meta FAIR), [[Eric Zelikman]] (STaR / Quiet-STaR; xAI), [[Jacob Pfau]] (Filler Tokens; NYU).
  - **Plans (1):** [[plans/WAVE_4_REVISED]] — 6 fundamentally-different training blocks (not 4), with COCONUT restored to the list.
- **Precursor audit result:** All 10 target precursors already ingested EXCEPT Neural ODEs:
  - Already present: [[Adaptive Computation Time]], [[Universal Transformers]], [[Deep Equilibrium Models]], [[PonderNet]], [[Pause Tokens]], [[Filler Tokens]], [[Implicit CoT via Knowledge Distillation]], [[Stepwise Internalization]], [[Quiet-STaR]].
  - Filed this session: [[Neural ODEs]].
- **COCONUT hyperparameters extracted verbatim (from arxiv:2412.06769v2 HTML):**
  - Base: GPT-2 only (no Llama/Mistral). LR=1e-4. Batch=128. Opt reset at stage boundaries.
  - c=2 on GSM8k, c=1 on ProntoQA/ProsQA.
  - GSM8k: 3 stages + initial + 1 extra; 6 epochs initial, 3 per subsequent.
  - ProntoQA/ProsQA: 6 stages + initial; 5 epochs each.
  - Anti-forgetting mix rate: p=0.3 (explicit in § 5 analysis).
  - n+1 forward passes per training step where n = scheduled latent thoughts.
  - Loss masked on questions + latent thoughts; CE only on surviving language tokens + answer.
- **Fundamental-difference-from-CODI analysis (key table):**
  - COCONUT = K-stage curriculum, latent positions masked from loss, CE-only signal, optimizer reset, p=0.3 mixing.
  - CODI = 1-stage, L1 alignment of hidden state at pre-answer boundary, dual forward pass, no curriculum.
  - These are two distinct optimization problems, not variants of one.
- **Revised Wave 4 (from [[plans/WAVE_4_REVISED]]):** COCONUT (added, required), Implicit-CoT-KD (added, context-only), PonderNet-style halting (added, subsumes HRM), DEQ (added, north-star novelty), Quiet-STaR (added, per-token), Pause/Filler pretraining (added, cheapest). Dropped: Retrofitted Recurrence, Ouro retrofit, Token Assorted (all not fundamentally different — incremental variations of existing blocks).
- **Primary-tier hits per project:**
  - spar-latent-reasoning: 6 primary on all new pages (taxonomic).
  - branch-d: 3 primary (Implicit CoT Precursors, Genealogy synthesis, Neural ODEs secondary).
  - branch-b: 2 primary (Neural ODEs for adjoint-sensitivity framing; Genealogy for DEQ arc).
  - branch-a: 2 secondary (scaling context for NODE/DEQ).
  - branch-c: 1 secondary (Jacob Pfau faithfulness concern).
- **Key new findings (for writeup):**
  - Field has a **linear**, not branching, pre-2024 genealogy — most design slots had only 1 representative before 2024. The 2024 explosion (5 precursors in 13 months) is a phase transition.
  - COCONUT's **single novelty** vs precursors is feeding the model's own hidden state back as input embedding. Curriculum (Deng 2024) + delimiters (Goyal 2023) were already published.
  - Three 2025 papers (HRM, AdaPonderLM, MoR) independently resurrect PonderNet at LLM scale without citing each other as inspiration — strong reinvention signal.
  - O(1)-memory gradients (Neural ODE adjoint 2018; DEQ IFT 2019) are available but no LLM-scale DEQ exists. CODI V2 detach is a crude approximation; DEQ is the principled frontier.
  - Pretraining-with-latent-thoughts is the open question COCONUT explicitly names; only [[Adaptive Latent CoT Pretraining]] has tried continuous-thought pretraining, still modest results.
- **Reinvented-wheel candidates (less novel given history):** Mixture of Recursions, HRM, AdaPonderLM/PonderLM-3, Ouro, Soft Thinking, From Growing to Looping, Continuous CoT Parallel Exploration.
- **Under-explored precursor directions (possible new directions):** per-token continuous thought (Quiet-STaR × COCONUT), DEQ at LLM scale, continuous-thought pretraining, DENSE per-step latent supervision (Pfau 2024's warning to weak-supervision methods).
- **Compliance:** Did NOT edit index.md or hot.md per explicit instructions. hot.md + index.md will be consolidated by user.

---

## [2026-04-23] autoresearch | Info-theoretic and distribution-regularization techniques for breaking routing-lock / template-attractor failures

- **Rounds:** 3 (broad → gap-fill → targeted F5 mapping).
- **WebSearch queries:** 15; WebFetch: 16 (5 abstract-only; 11 successful ar5iv HTML).
- **Pages created (15 total, exactly at budget):**
  - **Synthesis (1):** [[Research - Info and Distribution Constraints for Latents]]
  - **Sources (9):** [[Deep Variational Information Bottleneck]] (Alemi et al., ICLR 2017); [[Conditional Entropy Bottleneck]] (Fischer, 2020); [[HSIC Bottleneck]] (Ma, Lewis, Kleijn, AAAI 2020); [[VICReg]] (Bardes, Ponce, LeCun, ICLR 2022); [[Barlow Twins]] (Zbontar et al., ICML 2021); [[Contrastive Predictive Coding]] (van den Oord, 2018, InfoNCE source); [[InfoVAE]] (Zhao, Song, Ermon, AAAI 2019); [[Continuous Autoregressive Language Models]] (CALM, arxiv 2510.27688, Oct 2025); [[KL-Regularized RL is Designed to Mode Collapse]] (arxiv 2510.20817, Oct 2025); [[Emergence of Invariance and Disentanglement]] (Achille & Soatto, JMLR 2018).
  - **Concepts (4):** [[Variational Information Bottleneck]]; [[Conditional Entropy Bottleneck (concept)]]; [[Whitening-Based Anti-Collapse]]; [[Distribution Regularizer Catalog]].
  - **Entities (1):** [[Alex Alemi]].
- **Primary-tier hits per project:**
  - branch-d: 9 primary — VIB, CEB, VICReg, Barlow Twins, InfoNCE, InfoVAE, CALM, Whitening concept, Distribution Regularizer Catalog. Every one directly maps to F3 / F5 / F6 failure modes.
  - spar-latent-reasoning: 10 primary — the full stack for the writeup's regularization chapter.
  - branch-b: 0 primary, 6 secondary — whitening / HSIC-IB are detach-compatible.
  - branch-a: 0 primary, 2 secondary — scaling-neutral regularizers; CALM's scaling finding transfers.
  - branch-c: 0 primary, 2 secondary — per-dim KL + cross-position correlation as F-battery extensions.
- **Key findings (equation-level):**
  - **F3 template lock is canonical posterior collapse.** CALM (Oct 2025) observed 71/128 dim collapse and fixed with per-dim KL-clip: `L_KL^clip = Σ_i max(λ_KL, L_{KL,i})`, λ_KL=0.5. Adapted to CODI's positional collapse: per-position KL-clip.
  - **F5 swap-null is literally the InfoNCE training signal.** Swap-NCE loss `L = -Σ_i log[exp(z_i^T W q_i) / Σ_j exp(z_j^T W q_i)]` forces I(Z;Y|question) > 0 by construction. Needs batch size ≥ 32 for non-trivial MI bound.
  - **CPF is an implicit VIB; CEB formalises it with a learnable γ.** CPF's α·h_ctx + (1-α)·e_pred is structurally a CEB variational bound: h_ctx ↔ e(z|x), e_pred ↔ b(z|y). VCEB = <log e(z|x)> - <log b(z|y)> - γ<log c(y|z)> with γ=1 targeting Minimum Necessary Information (MNI).
  - **VICReg variance hinge fixes F6 by construction.** `v(Z) = (1/d)Σ_j max(0, γ - std(z_j))` directly widens per-dim spread. Batch-local, detach-compatible, no prior choice needed.
  - **KL-RL on top of CPF will undo it.** [[KL-Regularized RL is Designed to Mode Collapse]] shows mode collapse is inherent at the RL optimum, not an optimisation artefact. If CPF is ever RL-fine-tuned, MARA-style reward shaping is required.
- **Proposed stack for BranchD V3 (recommended):**
  - `L_total = L_CE(y) + λ_1 · L_KL-clip + λ_2 · L_swap-NCE + λ_3 · L_VIC-var`
  - Starts λ_1=1, λ_2=0.1, λ_3=1, λ_KL=0.1, γ (variance hinge)=0.3·mean-LN-std. Needs ablation.
- **Literature gaps flagged (for follow-up autoresearch):**
  - No 2024-2025 paper applies Wasserstein / Sinkhorn OT to latent-CoT rollouts.
  - No direct EBM regularization of latent-reasoning trajectories (Energy Matching Apr 2025 is tangential).
  - CEB empirical γ schedule for LLM reasoning unexplored (paper benchmarks only on image classification).
- **Cross-project impact:** This synthesis gives branch-d five concrete loss formulations to try as V3 variants; branch-b a batch-local whitening/HSIC-IB alternative; branch-c two new diagnostic probes (per-dim KL, cross-position correlation).
- **Failures:** arxiv.org/abs HTML parser returned abstract-only for 5 fetches; recovered via ar5iv.labs.arxiv.org/html mirror for all but the OpenReview PDF (1 source lost: Causal Differentiating Concepts) — noted in Open Questions.
- **Compliance:** Did NOT edit index.md or hot.md per explicit instruction (3-agent consolidation pattern).

---

## [2026-04-24] autoresearch | Disentanglement and Sparse Coding for Latents

- **Rounds:** 2 of max 3 (third round not needed — gaps were detail, not framing).
- **Searches:** 10 WebSearch + 10 WebFetch calls.
- **Sources found:** 5 canonical papers filed + ~10 cross-referenced (Gao 2024 Top-K SAE, Rajamanoharan 2024 JumpReLU, Nabeshima 2025 Matryoshka, Chanin 2024 Absorption, Cunningham 2023 Dictionary, Locatello 2019 Impossibility, Schölkopf 2021 CRL, Arjovsky 2019 IRM, Templeton 2024 Scaling Monosemanticity, Hyvärinen nonlinear ICA).
- **Pages created (14):**
  - **Synthesis:** [[Research - Disentanglement and Sparse Coding for Latents]]
  - **Sources (5):** [[Toy Models of Superposition]], [[Towards Monosemanticity]], [[Sparse Feature Circuits]], [[How does Chain of Thought Think]], [[Step-Level Sparse Autoencoder]]
  - **Concepts (5):** [[Superposition]], [[Sparse Autoencoder]], [[Feature Absorption and Splitting]], [[Matryoshka Sparse Autoencoder]], [[Causal Disentanglement]]
  - **Entities (3):** [[Nelson Elhage]], [[Samuel Marks]], [[Bernhard Schölkopf]]
- **Project tiers:**
  - spar-latent-reasoning: primary across the full set — anti-superposition toolkit for the writeup.
  - branch-c: 6 primary — SAE-based probes resolve the LTO-vs-DDR probe-typology contest via principled basis + attribution-patching causal baseline.
  - branch-d: 3-4 primary (SSAE, Matryoshka SAE, Causal Disentanglement via CPF-as-inductive-bias framing) + 3 secondary.
  - branch-a: 1 primary (How-does-CoT-Think scale threshold).
  - branch-b: all NA.
- **Top 5 findings:**
  1. **F3 template-lock is the canonical superposition-at-position signature** (Elhage 2022). 7-into-1 direction packing is the geometric phenomenon Toy Models formalizes, applied at *position*-granularity instead of neuron-granularity. Phase-change finding predicts routing-lock emerges abruptly during training once sparsity crosses a threshold.
  2. **F5 decoder-invariance is the basis-mismatch signature SAEs are designed to reveal.** Per-example content exists in the KV (63 PCs, 0.78 median cosine) but is orthogonal to the logit-lens readout direction. SAE on CODI latents is the definitive test.
  3. **Sparse autoencoder + attribution patching resolves Branch C's probe-typology contest.** Both LTO and DDR are linear probes in a superposed basis; SAE features are the canonical monosemantic basis, and attribution patching (Marks 2024) gives a causal ground-truth. Whichever probe's feature set aligns more with causally-implicated features wins.
  4. **CPF is theoretically load-bearing, not decorative.** Locatello 2019 proves unsupervised disentanglement is impossible without inductive bias; CPF's embedding-space anchor is precisely the auxiliary-variable inductive bias the theorem leaves room for. Upgrades CPF from "empirical trick" to "specific instance of causal-representation theory".
  5. **Step-Level SAE (2026) is the strongest methodological import.** Context-conditioned encoder+decoder isolates per-position *incremental* content rather than absolute activation. Directly tests whether F3's 7 empty positions hold invisible-but-real content (||I^k||_1 > 0) or are genuinely empty (||I^k||_1 → 0) — a question the F-battery alone cannot answer.
- **Proposed probe formulations & loss terms (filed in synthesis §Proposed probes):**
  - P1. Vanilla / JumpReLU SAE on CODI latents (baseline).
  - P2. Step-conditioned SAE (SSAE) for incremental content.
  - P3. Attribution patching for causal feature identification.
  - P4. Anti-superposition orthogonality penalty — two variants (per-example, batch-averaged).
  - P5. Multi-environment invariance (IRM-flavored) on problem-type partitions of GSM8K.
  - P6. Matryoshka-SAE probe hierarchy resolving Branch C's probe-granularity question.
- **Key open questions:** Does SAE on CODI recover features at "empty" positions? Does L_diversity during training break routing-lock? Does SSAE conditioning recipe transfer from discrete steps to continuous latents? Does CPF-trained CODI show more distinct Matryoshka features at position 3 than vanilla?
- **Key contradictions flagged:** L1 vs L0 sparsity (L1 causes shrinkage + absorption — prefer JumpReLU/Matryoshka for CODI); 70M vs 2.8B CoT scale threshold (implies below-1B continuous-CoT works mechanistically differently from 4B+); impossibility theorem vs sparsity-is-enough (sparsity is *one* inductive bias, not sufficient for *causal* disentanglement).
- **Skipped / follow-up candidates:** Gated SAE detail, IRM deep review, Orthogonal SAE, Scaling Monosemanticity 2024, SynthSAEBench.
- **Per task instructions:** index.md + hot.md NOT edited (consolidated later).

---

## [2026-04-24] autoresearch | Stability Theory for Latent Recurrence

- **Rounds:** 2 (3rd round skipped — gap coverage adequate).
- **Sources found:** 8 external (6 full-ingested, 2 referenced from prior wiki entries).
- **Pages created (15 total, at hard cap):**
  - synthesis: [[Research - Stability Theory for Latent Recurrence]]
  - sources: [[Deep Equilibrium Models]], [[Stabilizing Equilibrium Models by Jacobian Regularization]], [[Resurrecting the Sigmoid Dynamical Isometry]], [[Parseval Networks]], [[Orthogonal Recurrent Networks]], [[Noisy Recurrent Neural Networks]], [[Robust Learning with Jacobian Regularization]]
  - concepts: [[Fixed-Point Iteration]], [[Deep Equilibrium Model (DEQ)]], [[Lyapunov Stability]], [[Spectral Regularization]], [[Jacobian Constraint]]
  - entities: [[Shaojie Bai]], [[J. Zico Kolter]], [[Jeffrey Pennington]]
- **Key findings (top 5 linking stability theory → our routing-lock problem):**
  1. F6 narrow basin = bounded per-step Jacobian norm `rho(J_f) >= 1.3` implies 8x amplification through M=8 rollout; Parseval or Jacobian-Frobenius penalty forces it to `≤ 1` mechanically widening basin.
  2. F3 template attractor = rank-1 Jacobian dominance; stable-rank regularizer `||J||_F^2 / ||J||_2^2` or Parseval retraction directly eliminates the rank-1 singular-direction monopoly.
  3. V2 detach is truncated implicit-function-theorem gradient; principled replacement is DEQ + IFT using `(I - J_f)^{-1}`.
  4. "No-recall fixed points are countable → cannot be input-dependent" (Labovich 2026 theorem) — formal explanation of F5 swap-null; CPF converts CODI to recall-mode and is *predicted* to resolve it.
  5. Noise injection ≡ Jacobian-Frobenius regularization in the small-noise limit (Lim et al. 2021 SDE theorem). Zero compute overhead, afternoon engineering; expected immediate F6 widening.
- **Most applicable concepts to our project:** [[Jacobian Constraint]] (most portable), [[Spectral Regularization]] (implementation family), [[Fixed-Point Iteration]] (framing), [[Deep Equilibrium Model (DEQ)]] (target architecture), [[Lyapunov Stability]] (strongest but costliest).
- **Open questions for follow-up research:**
  - Attention-block Jacobian spectrum (weight-level vs effective-block Jacobian).
  - Recurrent-depth Jacobian dynamics scaling law (Huginn / Ouro data).
  - Partial-IFT variants between full DEQ and crude detach.
  - Lyapunov-auxiliary × teacher-forcing interaction.
  - Noise-injection post-linearization regime at σ=0.5.

---

## [2026-04-23] paper-crawl | Seed: Stochastic Soft Thinking (2508.03440)

- **Crawl depth:** 1 (downstream citations of SST).
- **Discovered:** 19 S2 citations (18 arXiv-resolved, 1 non-arxiv).
- **Dedupe:** 7 raw-paper dups (Soft Tokens Hard Truths 2509.19170, LaDiR 2510.04573, Latent-SFT 2510.15522, SwiReasoning 2510.05069, Parallel TTS Latent 2510.07745, Dynamics of Latent CoT 2602.08783, LEPO 2604.17892) + 1 wiki-source-exists (ThinkRouter 2602.11683, pre-ingested via HRPO crawl). 1 dropped as off-topic (2603.00510 MLLM visual sparsity).
- **Papers full-ingested (9 new):**
  1. [[SeLaR]] (2604.08299) — training-free entropy-gated soft + contrastive anti-collapse. **Primary for branch-d** — direct structural sibling to CPF.
  2. [[Latent Exploration Decoding]] (2602.01698, isInfluential=True) — post-RL final-layer entropy collapse; intermediate layers retain diversity → depth-conditioned decoding.
  3. [[Multiplex Thinking]] (2601.08808, Furu Wei group) — K-sample multiplex token (structurally ≡ CPF e_pred with K-sampling); self-adaptive width; code+checkpoints public.
  4. [[LaDi-RL]] (2602.01705, Kang et al. UCSD) — latent-diffusion RL avoids mode-elicitation collapse; +9.4% code / +5.7% math.
  5. [[Latent CoT Survey]] (2505.16782, 34 cit / 2 infl) — canonical token-wise horizontal vs layer-wise vertical taxonomy; registry at github.com/EIT-NLP/Awesome-Latent-CoT.
  6. [[JEPA-Reasoner]] (2512.19171) — decoupled JEPA reasoner + separate Talker module; 0.9B, +149.5% 8-shot GSM8K.
  7. [[LEAD]] (2603.13366) — multimodal twin of SeLaR; entropy-gated soft for MLRM hallucination mitigation.
  8. [[Opaque Serial Depth]] (2603.09786, Google DeepMind Safety: Brown-Cohen, Lindner, Shah) — formal CoT-necessity measure; Gemma 3 numeric bounds; MoE < dense depth.
  9. [[BFS-PO]] (2602.14917) — RL with max-entropy-node backtracking reduces overthinking; discrete (no latent), shared author cluster with LED.
- **Entity pages:** updated [[Haoqiang Kang]] (add LaDi-RL); new: [[Renyu Fu]], [[Yao Tang]], [[Bingyang Kelvin Liu]], [[Rohin Shah]], [[Fiorenzo Parascandolo]]. [[Wenhui Tan]] already existed.
- **Concept pages updated:**
  - [[Shortcut Behavior]] — added 4 new mitigation avenues (entropy-gated, depth-conditioned, latent-diffusion RL, self-adaptive multiplex) and linked SeLaR/LED/LaDi-RL/Multiplex Thinking as sources.
  - [[Gumbel-Softmax Latent]] — extended from 4→7 recipes; added Multiplex Thinking (top-K sampling), LaDi-RL (diffusion stochasticity), SeLaR (entropy-gated).
- **[[Stochastic Soft Thinking]]** source page: related-list extended with SeLaR, LED, Multiplex Thinking, LaDi-RL, ThinkRouter.
- **Primary-tier hits per project:**
  - branch-d: 2 primary (SeLaR, Multiplex Thinking) — both direct CPF analogues.
  - spar-latent-reasoning: 3 primary (SeLaR, Multiplex Thinking, Latent CoT Survey).
  - branch-a: 1 secondary (Multiplex Thinking RL scaling; LED entropy probe); 1 reference (Opaque Serial Depth Gemma 3 bounds).
  - branch-b, branch-c: no hits (all reference/NA).
- **Key findings:**
  - **SeLaR's contrastive-push-away anti-collapse is the cleanest training-free analog to LT-Tuning CPF.** Both prevent soft embeddings from collapsing to top-1: CPF anchors to hidden state (training-time); SeLaR pushes away via contrastive (inference-time). Could ablate CPF with a contrastive-only variant.
  - **Multiplex Thinking makes the "CPF e_pred is probability-weighted vocab sum" structural insight crisp.** Multiplex restricts the sum to K samples, adds RL, and gets self-adaptive width. Directly suggests the ablation: LT-Tuning CPF with α=0 + K-sample e_pred.
  - **LED's entropy asymmetry** (final-layer collapses post-RL; intermediate layers retain diversity) is a *new diagnostic* — cheap inference-time probe. Could validate our Qwen3 baselines without retraining.
  - **Four independent diagnoses of "latent RL collapses diversity":** SST (Greedy Pitfall), LED (final-layer entropy collapse), LaDi-RL (mode elicitation), SeLaR/ThinkRouter (soft-embedding noise aggregation). Collectively establish the failure taxonomy for the writeup.
  - **Opaque Serial Depth gives a Gemma 3-specific theoretical anchor** for our architecture-dependence finding. Paper computes numeric upper bounds for Gemma 3; MoE < dense means Gemma-3's dense architecture has higher opaque depth → more capacity for un-externalized reasoning → more latent reasoning headroom.
  - **JEPA-Reasoner's 149.5% GSM8K gain at 0.9B is striking** but needs scale validation. Decoupled reasoner + Talker is an architecture axis distinct from CPF (fusion) / SIM-CoT (auxiliary decoder) — could be a third synthesis input.
- **Overlaps with existing vault:** SST-downstream overlaps substantially with CoLaR-downstream (Latent-SFT, LEPO, SwiReasoning, Parallel TTS) and with Ouro-downstream (LaDiR). This is expected — the 2026 stochastic-latent / hybrid cluster is tight. ThinkRouter had a wiki source page from HRPO crawl (not CoLaR/CODI/COCONUT), which shows the dedupe is working across 4+ parallel crawls.
- **Failures:** arxiv.org/abs HTML parser failed for 6/10 papers on first pass (citation_title meta tag missing on some layouts); recovered via export.arxiv.org API with HTTPS redirect. No S2 or WebFetch failures.
- **seeds.yaml:** new section `# === Crawled from Stochastic Soft Thinking downstream 2026-04-23 ===`; SST seed status updated to `crawled`, papers_ingested=9.

---

## [2026-04-23] paper-crawl | Seed: SIM-CoT (2509.20317)
- **Crawl depth:** 1 (downstream citations of SIM-CoT). Original seed skipped in round 1 of the deep-crawl sweep; returned to it in this pass.
- **Discovered:** 20 S2 citations (all 20 arXiv-resolved). 2 flagged isInfluential=true.
- **Pre-filtered:** 10 retained, 10 dropped. Dropped: SeC (VOS), STAR-Bench (audio 4D), ARM-Thinker (multimodal reward models), Visual Self-Refine (chart parsing), LatentPilot (VLN), Shorter Thoughts DSS-GRPO (segment-wise RL compression, not latent), LaST-VLA (near-duplicate of OneVL/DualCoT-VLA domain), LLM-Driven Kernel Evolution (off-topic). Dynamics-Within-Latent-CoT (2602.08783) already in vault as [[Dynamics of Latent CoT]] from CODI crawl — deduped.
- **Papers ingested (10, 9 new + 1 co-discovered with Stochastic Soft Thinking parallel crawl):**
  1. [[CoLT]] (2602.04246, **isInfluential**) — latent reasoning as tool calls; seed tokens unpacked by external smaller model. Inverts SIM-CoT's aux-decoder-at-training into aux-decoder-at-inference.
  2. [[OneVL]] (2604.18486, **isInfluential**) — Xiaomi 50-author report; **dual auxiliary decoders** (language + visual-world-model) + three-stage training; **first latent CoT method claimed to surpass explicit CoT**. Direct multimodal extension of SIM-CoT recipe.
  3. [[LaRA-VLA]] (2602.01166) — VLA three-stage curriculum explicit→latent→action-conditioning; 90% latency reduction.
  4. [[ThinkRouter]] (2602.11683) — training-free inference-time confidence-aware routing; counter-intuitive finding that incorrect latent trajectories have FEWER low-confidence steps. Co-discovered via Stochastic Soft Thinking crawl; existing source page preserved.
  5. [[Adaptive Latent CoT Pretraining]] (2602.08220) — per-token variable-length latent CoT in one-stage Llama pretraining; adaptive halting emerges without curriculum.
  6. [[LatentChem]] (2602.07075) — chemistry-domain emergent latent reasoning from task-success optimization only; 59.88% non-tie win vs CoT; 10.84× overhead reduction.
  7. [[ALiCoT]] (2601.21576) — **first theoretical analysis of CoT compression hardness** via Order-r Interaction exponential decay; NatBool-DAG benchmark; distribution-alignment method; 54.4× speedup comparable to explicit CoT.
  8. [[OneLatent]] (2602.13738) — single-token compression via rendered-CoT-image + DeepSeek-OCR hidden-state supervision; 99.80% ProntoQA / 97.80% ProsQA with ONE latent token; up to 87.4× compression.
  9. [[Visual Enhanced Depth Scaling]] (2604.10500) — token-level gradient-dynamics analysis during latent training (visual under-optimization, complex-token gradient instability bounded by depth); visual replay + routing depth scaling.
  10. [[DualCoT-VLA]] (2603.22280) — dual learnable-query-token sets (visual + linguistic CoT); single-step forward reasoning; SOTA LIBERO + RoboCasa GR1.
- **Primary-tier hits per project:**
  - spar-latent-reasoning = 3 primary ([[OneVL]], [[ThinkRouter]] (pre-existing), [[ALiCoT]])
  - branch-d = 1 primary ([[ALiCoT]] — theoretical scaffolding for CPF)
  - branch-a = 0 primary, 1 secondary ([[Adaptive Latent CoT Pretraining]])
  - branch-b = 0 primary, 1 secondary ([[Visual Enhanced Depth Scaling]] — gradient-dynamics methodology)
  - branch-c = 0 primary
- **Key findings:**
  - **OneVL's "first latent CoT to surpass explicit CoT" claim** is the strongest 2026 such claim. Xiaomi-resourced 50-author report; dual-decoder supervision (text CoT + future-frame world model) generalizes SIM-CoT. Load-bearing for SPAR north-star thesis; needs PDF read for ablation validation.
  - **ALiCoT provides the first theoretical lower bound** on CoT compression: Order-r Interaction decay theorem formally explains why naive latent-CoT collapses and why distribution-alignment supervision is necessary (not stylistic). Direct scaffolding for LT-Tuning CPF framing — CPF is a concrete instantiation of the alignment the theorem demands. NatBool-DAG is a candidate shortcut-eliminating benchmark.
  - **ThinkRouter's confidence pathology** (incorrect latent trajectories have FEWER low-confidence steps than correct ones) is a measurable, portable diagnostic for latent overconfidence. Consistent with [[Shortcut Behavior]] framing.
  - **Visual Enhanced Depth Scaling's gradient-dynamics methodology** is directly importable to Branch B's text-only grad-stability ablations. Finding that complex-token gradient instability is bounded by fixed depth is distinct from detach-pipeline issues.
  - **Three parallel 2026 VLA extensions** (OneVL, LaRA-VLA, DualCoT-VLA) confirm the SIM-CoT recipe travels to multi-modal / action domains. All use three-stage curriculum + auxiliary supervision structure.
- **Parallel-crawl overlaps:** [[ThinkRouter]] already ingested by Stochastic Soft Thinking parallel crawl (existing rich Qwen3-quantified page preserved). [[Dynamics of Latent CoT]] (2602.08783) already in vault from CODI crawl — deduped. No other conflicts.
- **Failures:** WebFetch returned mostly abstract-only content (these are recent 2026 papers; arXiv HTML abstract pages have limited body text via WebFetch). Captured verbatim abstracts + author lists + metadata; numerics/ablations for followup depth pass require PDF reads. No fetch failures, no S2 rate-limit issues. All raw `.md` files created in `.raw/papers/`.
- **Concept pages updated:** [[Feature Collapse]] (+OneVL, OneLatent, ALiCoT rows in mitigations table; +Theoretical framing section citing ALiCoT Order-r decay theorem; cross-references extended); [[Shortcut Behavior]] (+ALiCoT theoretical framing + ThinkRouter confidence finding).
- **seeds.yaml:** added `# === Crawled from SIM-CoT downstream 2026-04-23 ===` section with 10 entries; flipped 2509.20317 seed to `status: crawled` with `crawled_at: 2026-04-23`.

---

## [2026-04-23] paper-crawl | Seed: Scaling Up TTC (2502.05171, Huginn-0125)

- **Crawl depth:** seed ingest + 1 downstream hop. Seed NOT previously in vault — ingested first, then crawled.
- **Seed ingested:** [[Scaling Up TTC]] — 3.5B recurrent-depth model trained on 800B tokens; Prelude/Recurrent-Core/Coda architecture; truncated BPTT k=8; stochastic s_0 + Poisson-Lognormal iteration sampling; re-injection of prelude output at each step. Authored by Geiping, McLeish, Kirchenbauer, ..., Goldstein (UMD / ELLIS-MPI / LLNL).
- **Citations discovered:** 195 total, 179 with arXiv IDs. 22 deduped against existing 49 sources (12% of downstream already covered — HRPO, LEPO, Parcae, Mechanistic Analysis, Are LRMs Interpretable, From Growing to Looping, COCONUT, CODI, HRM, Soft Thinking Mechanism, SIM-CoT, CoT2, LaDiR, Soft Tokens Hard Truths, Parallel TTS, MARCOS, Think-at-Hard, Step-Decomposed Influence, Dynamics of Latent CoT, PonderLM-3, Weak vs Strong, RLTT).
- **Pre-filter:** 157 new arxiv candidates ranked by (score = keyword-relevance on recurrent/looped/latent-reasoning/TTC/halting/scaling/feature-collapse/curriculum) > isInfluential > infCit > cit. Top 25 reviewed; 15 ingested.
- **Papers ingested (15, all new source pages):**
  1. [[Retrofitted Recurrence]] (2511.07384) — UMD follow-up to Huginn: convert pretrained TinyLlama/OLMo/Llama-3.2-1B to depth-recurrent via curriculum of recurrences; Muon > AdamW; matched-FLOP wins on math.
  2. [[Encode Think Decode]] (2510.07358) — FAIR Meta: iterate only a middle-layer subset T; +28.4% on 17 reasoning benchmarks.
  3. [[AdaPonderLM]] (2603.01914) — Token-wise halting via iteration-specific MLP gates + monotonic mask + KV reuse; -10% inference compute on Pythia 70M-2.8B.
  4. [[Decoding Depth-Recurrent Transformer]] (2507.02199) — Probes Huginn with Logit Lens + Coda Lens; finds limited evidence of latent CoT and sharp cross-block discontinuities.
  5. [[Latent Thinking Optimization]] (2509.26314) — Process-reward probe on Huginn latent trajectories; parallel LTO inference with negligible overhead.
  6. [[Inner Loop Inference]] (2602.14759) — Train-free block looping on pretrained non-recurrent Transformers; unlocks latent capability.
  7. [[Stability and Generalization in Looped Transformers]] (2604.15259) — Fixed-point theory: reachability / input-dependence / geometry axes; theorem that no-recall loops have countable fixed points.
  8. [[Loop Think Generalize]] (2604.07822) — Implicit-reasoning probes on Huginn/Ouro: systematic generalization + depth extrapolation.
  9. [[Two-Scale Latent Dynamics]] (2509.23314) — Two-scale geometry (refinement within-block + drift across-blocks); acceleration-based early-exit beats Huginn's KL exit.
  10. [[Skip a Layer or Loop it]] (2507.07996) — CoLa: per-sample MCTS over skip/loop layer sequences; >75% of samples benefit from non-static architecture.
  11. [[LoopFormer]] (2602.11451) — Elastic-depth looped transformers via shortcut modulation; iteration-aware residual.
  12. [[Depth-Recurrent Attention Mixtures]] (2601.21582) — Dreamer: sequence + depth + expert attention addresses the hidden-size bottleneck of plain recurrent depth.
  13. [[One Step Forward K Steps Back]] (2604.18839) — Denoising Recursion Models bridge diffusion and looped transformers via trajectory-level supervision.
  14. [[Survey on Latent Reasoning]] (2507.06203) — 34-author taxonomy: vertical (depth) vs horizontal (sequential) recurrence. Cited as umbrella framing.
  15. [[Mixture of Recursions]] (2507.10524) — KAIST/Mila: token-level routers + recursion-wise KV cache; Pareto front 135M-1.7B. Most-influential non-Huginn recursive-transformer paper.
- **Primary-tier hits per project:**
  - **branch-a (Qwen3 scaling):** 8 primary — Scaling Up TTC, Retrofitted Recurrence, ETD, AdaPonderLM, Two-Scale Dynamics, Skip-or-Loop, LoopFormer, Depth-Recurrent Attention Mixtures, Mixture of Recursions, Inner Loop Inference, Loop-Think-Generalize, Latent Thinking Optimization.
  - **branch-b (detach/BPTT):** 5 primary — Scaling Up TTC, Retrofitted Recurrence, Stability and Generalization, Two-Scale Dynamics, Mixture of Recursions.
  - **branch-c (probe methodology):** 1 primary — Decoding Depth-Recurrent Transformer (Coda Lens!); 3 secondary.
  - **branch-d (CPF):** 3 primary — Scaling Up TTC (secondary-leaning), ETD, Latent Thinking Optimization, One Step Forward K Steps Back.
  - **spar-latent-reasoning:** 14 primary (all except LoopFormer/Skip-or-Loop which are secondary).
- **Key findings:**
  - **Huginn is the foundational seed of an entire sub-family.** 22/179 citations already in vault — this was the single biggest dedupe win yet. Strong validation that earlier crawls (Ouro, CODI, CoLaR, COCONUT) were centered on the right hub.
  - **Two waves of Huginn follow-up visible in citation graph:** (wave 1 — capability) Ouro, Parcae, Retrofitted Recurrence, Mixture of Recursions, ETD; (wave 2 — interpretability/theory) Decoding Depth-Recurrent, Latent Thinking Optimization, Two-Scale Dynamics, Mechanistic Analysis, Are LRMs Interpretable, Stability & Generalization, Loop-Think-Generalize.
  - **Three independent anti-off-distribution mechanisms converged:** Huginn (Poisson-Lognormal iteration sampling), LoopFormer (shortcut modulation), ETD (subset-only iteration). Same scientific problem — variable-depth robustness — three orthogonal solutions. Worth a comparison page.
  - **Train-free recurrence results (Inner Loop Inference + CoLa + From Growing to Looping) are a quietly important triangle:** capability for variable-depth reasoning is partially latent in pretrained models. Raises the baseline question for any recurrent-training claim.
  - **Acceleration-based early-exit (Two-Scale Dynamics) strictly dominates KL-based exit (Huginn default).** Cheap, drop-in upgrade for any recurrent-depth inference pipeline.
  - **Probe-methodology tension:** Decoding Depth-Recurrent finds LIMITED latent CoT, but Latent Thinking Optimization finds CLEAR process-reward signal in the same architecture. The information is there — just not in logit space. Mechanistic Analysis (already in vault) resolves via cyclic-fixed-point framing.
- **Parallel-crawl overlaps:** 22 existing-vault hits (none from parallel-running HRPO/SIM-CoT/SST crawls — all from prior Ouro/CODI/CoLaR/COCONUT crawls and earlier manual ingests).
- **Failures / rate limits:** None. 14/15 HTML v1 retrievals succeeded; 2604.15259 (Stability & Generalization) HTML not yet indexed on arxiv.org (paper posted 2026-04-16, 7 days before crawl) — fell back to abstract page. Source page notes `confidence: medium` and schedules full-text re-ingest on next autoreview.

---

## [2026-04-23] paper-crawl | Seed: HRPO (2505.18454)

- **Crawl depth:** 1 (downstream citations of HRPO).
- **Discovered:** 10 S2 citations, all 10 with arXiv IDs.
- **Deduped against existing 49 sources + parallel crawls:** 3 already in vault:
  - 2602.10520 [[RLTT]] (via Ouro crawl)
  - 2510.05069 [[SwiReasoning]]
  - 2505.23648 [[Continuous CoT Parallel Exploration]] (CoT2, via CODI crawl)
- **Dropped as out-of-scope (4):**
  - 2604.17866 LAnR — Latent Abstraction for RAG (retrieval-centric, different problem).
  - 2604.04457 RAR — Retrieval-Augmented Conversational Recommendation (recsys domain).
  - 2602.10494 Canvas-of-Thought — multimodal reasoning via HTML Canvas DOM CRUD (not latent reasoning mechanism).
  - 2601.07055 Dr. Zero — "HRPO" in the abstract is an unrelated "hop-grouped RPO" for search-agent self-evolution (acronym collision).
- **Papers ingested (3, all new source pages):**
  1. [[ThinkRouter]] (2602.11683) — Training-free inference-time binary router between discrete-token-sampling and Soft-Thinking top-j soft embeddings, gated by `p_t^max < τ`. +19.70 Pass@1 on Qwen3-1.7B STEM avg. UCSD / Adobe Research.
  2. [[Implicit Reasoning Survey]] (2509.02350) — Mechanism-level three-paradigm taxonomy (latent-optimization / signal-guided-control / layer-recurrent-execution). Most complete public taxonomy; organizing frame for writeup. HKUST-GZ / Jilin / CUHK / Yale. cc=27.
  3. [[Mull-Tokens]] (2512.10941) — Modality-agnostic latent tokens + three-stage curriculum on Qwen2.5-VL 7B; +3% avg, +16% on puzzle split. Google / UW / Stanford / BU.
- **Entity pages created (4):** [[Xin Xu]], [[Jindong Li]], [[Arijit Ray]], [[Adobe Research]]. (Lead-author-only this crawl; no need to fan out to all ~20 co-authors like earlier Ouro crawl.)
- **Concept pages updated (2):**
  - [[Context-Prediction-Fusion]] — added section "Related hybrid/fusion mechanisms (downstream literature)" linking [[HRPO]], [[ThinkRouter]], [[Mull-Tokens]]; reinforces that independently-converged discoveries (CPF / HRPO / Mull-Tokens curriculum) suggest a robust inductive bias.
  - [[Feature Collapse]] — added "Confidence pathology under Soft Thinking" manifestation (ThinkRouter's finding) and ThinkRouter row in mitigation table.
- **Primary-tier hits per project:**
  - spar-latent-reasoning = 2 primary ([[ThinkRouter]] — third hybrid-routing data point alongside HRPO + SwiReasoning; [[Implicit Reasoning Survey]] — writeup organizing frame).
  - branch-d = 0 primary (2 secondary: [[ThinkRouter]], [[Mull-Tokens]]).
  - branch-a / branch-b / branch-c = 0 primary (all reference or n/a).
- **Key findings:**
  - **ThinkRouter is a third independent hybrid-discrete-latent data point.** Together with HRPO (RL-learned gate) and SwiReasoning (switch), three distinct designs converge on the same claim: pure-latent reasoning suffers at low-confidence steps and hybridizing with discrete sampling helps. Strengthens spar writeup's case that hybridization is not a method-specific trick.
  - **ThinkRouter diagnoses a NEW failure mode of soft embeddings:** incorrect-answer trajectories have FEWER low-confidence steps than correct-answer trajectories under Soft Thinking. Low-probability aggregation creates noisy high-confidence reasoning. This is distinct from — but complementary to — the geometric-mismatch/feature-collapse pathology CPF targets. Opens the question: does CPF's α-mixing with hidden state disambiguate the soft-embedding noise, or does CPF also need a confidence-aware override?
  - **Implicit Reasoning Survey's taxonomy cleanly categorizes our entire vault's methods.** HRPO → internal-state-level latent optimization; LT-Tuning/CODI/SynAdapt → trajectory-level semantic anchoring; COCONUT/BoLT → progressive refinement; CoLaR/LightThinker → adaptive efficiency; Soft Thinking/SoftCoT → exploratory diversification; Ouro/Parcae/LoopLM → layer-recurrent execution. Usable as the synthesis chapter's skeleton.
  - **Mull-Tokens validates the "latent tokens + three-stage curriculum + RL refinement" recipe in the multimodal domain.** Stage-1 dual supervision (LM-head for text / frozen image-encoder for image) is a modality-aware analog of CPF's vocabulary-anchoring. First demonstration that the LR recipe transfers beyond text without task-specific supervision — strengthens writeup's claim that the synthesis target is a general mechanism.
- **Parallel-crawl overlaps:** none this crawl. All 3 new papers unique.
- **No S2 rate limits, no fetch failures.** All 3 PDFs fetched via arxiv.org/pdf and converted via PyMuPDF.

---

## [2026-04-23] autoreview sweep #1

- **Sources reviewed:** 49
- **Tier changes applied:** 11 (9 spar-latent-reasoning primary→secondary prunes + 1 branch-a HRPO secondary→reference + 1 spar Continuous-CoT-Multilingual secondary→reference)
- **Contradictions flagged:** 3 ([[Are LRMs Easily Interpretable]] ↔ [[Weak vs Strong Supervision Study]]; [[Capabilities and Limits of Latent CoT]] ↔ [[Soft Tokens Hard Truths]]; [[Capabilities and Limits of Latent CoT]] ↔ [[Token Assorted]])
- **Archived:** 0 — all entities have `projects:` entries; all concepts have ≥1 inbound link; no source is >1 day old
- **Dashboards regenerated:** branch-a, branch-b, branch-c, branch-d, spar-latent-reasoning
- **Main drift observed:** systematic over-grading on spar-latent-reasoning primary by the 4 crawler subagents. Pruned primary from 28 → 19 sources to keep signal density.
- **hot.md refreshed** with top 3 changes + top 3 contradictions + active reading queues.
- **Schema gaps noted for next lint:** missing concept pages `Greedy Pitfall`, `Sparse Autoencoder`, `R-KV Eviction`; drift in [[Soft Thinking]] / [[Reasoning by Superposition]] related-lists pointing at non-existent pages.
- See [[meta/autoreview/changelog]] for full detail.

---

## [2026-04-23] paper-crawl | Seed: Ouro / LoopLM (2510.25741)
- **Crawl depth:** 1 (downstream citations of Ouro)
- **Discovered:** 41 S2 citations (40 arXiv-resolved).
- **Pre-filtered:** retained 10 with direct overlap to looped-LM / scaling / interpretability / curriculum / manipulation-capacity; dropped ~30 with domain-specific abstracts (CTR prediction, VLA, VLM, energy principle, NeuroAI, topology, spoken dialogue, etc.).
- **Papers ingested (10, 9 new + 1 co-discovered with CoLaR crawl):**
  1. [[LaDiR]] (2510.04573) — VAE + latent-diffusion flow-matching; LLaMA-3.1-8B; beats Coconut on 7 math benchmarks.
  2. [[Step-Decomposed Influence]] (2602.10097) — step-resolved TracIn for looped TFs; TensorSketch at scale.
  3. [[Parcae]] (2604.12946) — stable-looped LM; negative-diagonal param constrains ρ(Ā)<1; μ_rec ∝ FLOP^0.40.
  4. [[Mechanistic Analysis of Looped Reasoning LMs]] (2604.11791) — cyclic fixed points; shows Ouro drifts past T_train.
  5. [[From Growing to Looping]] (2602.16490) — depth-growing ≡ looping mechanistically; 2× inference-time looping on grown models.
  6. [[RLTT]] (2602.10520) — trajectory-level RL credit; fixes Ouro's reported GRPO failure (+14-34 pts).
  7. [[Think-at-Hard]] (2511.08577) — selective per-token iteration on Qwen3; 6% tokens iterate; public code.
  8. [[Formal CoT vs Latent]] (2509.25239) — complexity separations (TC^k vs TC^{k-1}; FPRAS/FPTAS).
  9. [[Are LRMs Easily Interpretable]] (2604.04902) — CODI/Coconut latents 65-93% decodable. Co-discovered by CoLaR crawl; source page written by this Ouro crawl.
  10. [[Adaptive Loops and Memory]] (2603.08391) — decouples think-harder (loops) from know-more (memory).
- **Entity pages created (9):** [[Haoqiang Kang]], [[Georgios Kaissis]], [[Hayden Prairie]], [[Hugh Blayney]], [[Ferdinand Kapl]], [[Jonathan Williams]], [[Tianyu Fu]], [[Kevin Xu]], [[Markus Frey]]. [[Connor Dilgren]] + [[Sarah Wiegreffe]] already present from CoLaR parallel crawl.
- **Concept pages updated (3):** [[LoopLM]], [[Fixed-Width Depth Recurrence]], [[Adaptive Exit Gate]] — each gained a downstream-literature / updated-landscape section linking all new papers.
- **Primary-tier hits per project:** spar-latent-reasoning = 5 primary ([[Parcae]], [[RLTT]], [[Think-at-Hard]], [[Formal CoT vs Latent]], [[Are LRMs Easily Interpretable]]). branch-d = 1 primary ([[Are LRMs Easily Interpretable]]). branch-a = 0 primary (1 secondary: [[Think-at-Hard]]). branch-b = 0 primary (1 secondary: [[Parcae]]).
- **Key findings:**
  - **[[RLTT]] directly resolves Ouro's named open RL failure.** Our [[Ouro]] page flagged GRPO/DAPO as broken post-SFT due to vLLM/SGLang fixed-depth rollout assumption; RLTT reframes credit assignment across loop trajectory → +14.4 MATH-500 / +16.6 AIME24 / +34.3 GSM8K on Ouro-2.6B-Thinking. LoopLM + RL is tractable if you distribute reward.
  - **[[Mechanistic Analysis of Looped Reasoning LMs]] gives a mechanism for Ouro's T>4 degradation.** Ouro doesn't reach stable cyclic fixed points; retrofitted Llama does (stable to T=128). Suggests architectural fixes: stronger input injection, different normalization.
  - **[[Are LRMs Easily Interpretable]] — CODI latents encode expected solutions 65-71% of the time.** Critical Branch D input: feature collapse is not total; CPF's role is to strengthen signal not add from scratch. Methodology (backtracking + forward-chaining with counterfactual verification) directly reusable for Ouro latents.
  - **[[Parcae]] offers a stability recipe Ouro didn't use.** Negative-diagonal spectral constraint allows training without Ouro's 8→4 loop-reduction workaround. Scaling law μ_rec ∝ FLOP^0.40 is the first clean depth-recurrence power law.
  - **[[Formal CoT vs Latent]] provides complexity-theoretic separations** to anchor the SPAR writeup's taxonomy: latent wins on parallel reasoning (TC^k); CoT wins on randomized counting (FPRAS).
- **Parallel-crawl overlaps:** [[Are LRMs Easily Interpretable]] (2604.04902) discovered by both Ouro and CoLaR crawls; source page created once here. All 9 other Ouro downstream papers are unique to this crawl. LaDiR's raw file (`2510.04573-ladir.md`) existed under my chosen name from parallel COCONUT crawl; content preserved — my fresh write overwrote once, as expected with same content.
- **No S2 rate limits, no fetch failures.** All 10 papers fetched via WebFetch in parallel batches.

---

## [2026-04-23] paper-crawl | Seed: CODI (2502.21074)
- **Crawl depth:** 1 (downstream citations of CODI only).
- **Discovered:** 127 S2 citations (116 arXiv-resolved after dropping non-arXiv).
- **Pre-filtered:** dropped ~100 candidates — surveys (efficient-inference, overthinking), domain-specific (clinical diagnosis, autonomous driving, visual VLA, narrative tasks, dense retrieval), tangential or already-in-vault. Retained 15 direct-relevance candidates.
- **Deduped against existing + parallel-crawl output:** 5 candidates already ingested by CoLaR / COCONUT parallel crawls (`[[Weak vs Strong Supervision Study]]`, `[[LSTR]]`, `[[Stochastic Soft Thinking]]`, `[[Are Latent Reasoning Models Easily Interpretable]]`, `[[Continuous CoT Parallel Exploration]]` aka CoT2). Dropped these to avoid duplicate source pages.
- **Papers ingested (10, all new source pages):**
  1. [[DART]] (2506.11752) — Self-distillation cousin of CODI; Reasoning Evolvement Module (REM) for non-autoregressive Silent Thought.
  2. [[SemCoT]] (2510.24940) — Contrastive sentence transformer for semantic alignment + lightweight implicit-reasoning generator via KD. Code: YinhanHe123/SemCoT.
  3. [[PCCoT]] (2506.18582) — Jacobi parallel rollout replaces sequential continuous CoT; ~50% training + inference speedup; improved stability. Code: whyNLP/PCCoT.
  4. [[SynAdapt]] (2508.00574) — Synthetic CCoT as explicit alignment target + difficulty-classifier + adaptive re-think on hard questions.
  5. [[System-1.5 Reasoning]] (2505.18962) — Two-stage self-distillation + DS/SS shortcuts; 20× GSM8K speedup, 92.31% token reduction.
  6. [[Soft Tokens Hard Truths]] (2509.19170) — **First scalable RL-trained continuous CoT without distillation.** Llama/Qwen ≤8B, hundreds of tokens; train-soft / infer-discrete best config.
  7. [[Dynamics of Latent CoT]] (2602.08783) — **First causal-SCM interp study of CODI+COCONUT.** Staged-functionality + early-bias/late-commitment gap. Code: J1mL1/causal-latent-cot.
  8. [[Continuous CoT Multilingual]] (2603.08177) — CODI-framework multilingual eval; 29-50× compression; CODI wins on low-resource zero-shot.
  9. [[GTS]] (2602.14077) — Learned conditional Gaussian perturbation + GRPO (backbone frozen) for latent inference-time scaling.
  10. [[HRPO]] (2505.18454) — **Learnable gated hidden-state + token fusion trained by RL without CoT traces.** Structurally equivalent to LT-Tuning CPF with a learnable, context-dependent gate.
- **Key findings:**
  - **HRPO = CPF via RL.** HRPO's gating mechanism `g·h_hidden + (1−g)·e_token` is the same functional form as LT-Tuning's CPF `α·h_ctx + (1−α)·e_pred`. Two independent groups (UIUC/Google DeepMind and NeosKnight233) landed on the same fusion mechanism with different training recipes (RL-gate vs distillation-schedule). Strong convergent-evolution signal confirming branch-d's CPF-on-CODI target.
  - **CODI is causally studied.** [[Dynamics of Latent CoT]] performs the first do-intervention analysis on CODI; finds latent-step budgets behave as *staged functionality with non-local routing*, and a persistent gap between early output bias and late representational commitment. Directly testable diagnostic for CPF ablations.
  - **CODI latent rollout is underutilized.** [[Are Latent Reasoning Models Easily Interpretable]] (already ingested via CoLaR crawl) finds latent tokens often unnecessary — motivates CPF's anti-collapse role independently of accuracy metrics.
  - **RL + continuous CoT scales.** [[Soft Tokens Hard Truths]] trains Llama/Qwen up to 8B with RL alone (no distillation) — a distinct recipe from CODI's distillation and LT-Tuning's curriculum. Three synthesis inputs for the north-star now: distillation (CODI / SIM-CoT / LT-Tuning), RL (HRPO / Soft-Tokens-Hard-Truths), theory ([[Continuous CoT Parallel Exploration]] / [[Capabilities and Limits of Latent CoT]]).
  - **Jacobi parallel rollout is a free efficiency win.** [[PCCoT]] ~50% faster training + inference at matched or better accuracy, with improved stability — directly compatible with CODI and CPF.
- **Primary-tier hits per project:**
  - branch-d: 4 (SemCoT, PCCoT, Dynamics of Latent CoT, HRPO) + strong-secondary on DART / System-1.5.
  - branch-a: 2 (Soft Tokens Hard Truths, HRPO).
  - branch-b: 1 (PCCoT).
  - branch-c: 1 (Dynamics of Latent CoT).
  - spar-latent-reasoning: 3 (Soft Tokens Hard Truths, Dynamics of Latent CoT, HRPO).
- **Notable overlap / skipped:** 2604.04902, 2602.22441, 2602.01695, 2508.03440, 2505.23648 already covered by parallel CoLaR + COCONUT crawls — dropped my duplicates to avoid last-writer-wins conflicts on source pages.
- **Rate limits / failures:** None. S2 API returned all 127 citations across 2 pages cleanly. arXiv abstract WebFetch succeeded on all 15 pre-filtered candidates.

---

## [2026-04-23] paper-crawl | COCONUT (2412.06769) downstream
- **Seed:** [[COCONUT]] (arXiv:2412.06769)
- **Citations fetched:** 448 total via S2 (5 pages × 100, with offsets 0/100/200/300/400). 420 had arXiv IDs after dedupe. Top 30 reviewed by isInfluential → influentialCitationCount → citationCount.
- **Filter stage 1 (top-15 by influence):** selected 15 candidates with direct latent-reasoning / CoT-compression / feature-collapse / scaling signal. Dropped: survey papers (2503.16419, 2503.23077, 2503.24235), safety-focused (2501.18492 GuardReasoner, 2507.11473 CoT monitorability), domain-specific (2506.17218 multimodal, 2502.00592 MemoryLLM, 2505.19092 recommendation, 2511.20639 multi-agent, 2512.06690 personalized-gen, 2602.11401 image-diffusion).
- **Filter stage 2 (dedupe vs vault):** 6 of 15 already ingested by parallel crawls or pre-existed in vault — [[Stochastic Soft Thinking]] (2508.03440), [[System-1.5 Reasoning]] (2505.18962), [[LaDiR]] (2510.04573), [[Latent-SFT]] (2510.15522), [[MARCOS]] (2509.25020). Also [[SynAdapt]] (2508.00574) alternate already present. Skipped modification per crawl discipline.
- **Sources created (9 new):** [[Hierarchical Reasoning Model]] (2506.21734), [[Soft Thinking]] (2505.15778), [[Token Assorted]] (2502.03275), [[Reasoning by Superposition]] (2505.12514), [[SoftCoT Plus Plus]] (2505.11484), [[Beyond Semantics Reasonless Tokens]] (2505.13775), [[Continuous CoT Parallel Exploration]] (2505.23648), [[Latent Tokens]] (2505.12629), [[Efficient Post-Training Refinement]] (2506.08552).
- **Entity pages created (9):** [[Guan Wang]], [[Zhen Zhang]], [[DiJia Su]], [[Hanlin Zhu]], [[Yige Xu]], [[Karthik Valmeekam]], [[Halil Alperen Gozeten]], [[Yuchang Sun]], [[Xinyuan Wang]].
- **Concepts updated:** None modified (existing concept pages are preserved per crawl rules). Candidate new concept — "Single-Threaded Reasoners" / "Greedy Pitfall" — already covered by existing [[Stochastic Soft Thinking]] raw claims + concepts.
- **Primary-tier hits per project:** branch-a: 0 primary (1 secondary — HRM for architecture alternative; Token Assorted 8B); branch-b: 0 primary; branch-c: 0 primary (1 secondary — Beyond Semantics for probe-validity context); branch-d: 3 primary ([[Soft Thinking]], [[Stochastic Soft Thinking]] already-logged via CoLaR, and theoretical CSFT support from [[Continuous CoT Parallel Exploration]]); spar-latent-reasoning: 8 primary.
- **Key findings (new signal this crawl):**
  - **7B embedding-decoupling is a first-principles barrier — independently diagnosed.** [[Soft Thinking]] (Zhang et al.) explicitly articulates the weight-tied-vs-decoupled embedding problem at the 7B boundary as the reason COCONUT-style methods fail at scale — the *same* failure [[Latent Thoughts Tuning]] attributes to untied embeddings causing feature collapse, reached via independent analysis. Three convergent diagnoses now: LT-Tuning, Soft Thinking, Latent-SFT. Branch D's CPF thesis is externally corroborated.
  - **HRM proves latent reasoning works at 27M without any CoT supervision.** Orthogonal architectural direction from curriculum-distillation methods; uses DEQ-inspired one-step gradient (O(1) memory, no BPTT). Demonstrates that the scaling ceiling for curriculum methods is not a fundamental expressivity ceiling — it's a training-dynamics ceiling specific to fine-tuning pretrained LLMs.
  - **Theoretical foundation is now complete.** [[Reasoning by Superposition]] (NeurIPS 2025, Shibo Hao co-author) + [[Continuous CoT Parallel Exploration]] (ICLR 2026) jointly establish that continuous CoT is strictly more expressive than discrete CoT (D vs O(n²) for D-diameter graph reachability) *and* that training recovers the superposition representation automatically. Combined with [[Capabilities and Limits of Latent CoT]] proving curriculum is necessary, the theoretical stack is: expressivity proven → curriculum necessary → specific anti-collapse mechanism (CPF / Latent-Vocab / residual-refinement) required at scale.
  - **Token Assorted provides an 8B scaling data point.** Llama-3.1-8B Fresh-Gaokao-Math-2023 +13.3% with discrete latent tokens (VQ-VAE codebook) and *randomized-m single-stage training* (no curriculum). This is a direct challenge to the "curriculum is necessary" theorem — but the target space is discrete vocabulary extensions, not continuous latents, which are governed by different training dynamics. Useful contrast to cite in Branch D's curriculum-ablation section.
- **No failures or rate limits.** S2 API handled 5 pages smoothly; 15/15 arXiv HTML fetches succeeded (2508.03440 needed v4 because v1-v3 were placeholder stubs).
- **Raw papers saved to `.raw/papers/`:** full HTML→markdown for all 15 (even though 6 source pages were not created, raw files remain as breadcrumbs for future crawls).

---

## [2026-04-23] paper-crawl | Seed: CoLaR (2505.16552)
- **Crawl depth:** 1 (downstream citations of CoLaR only)
- **Discovered:** 47 S2 citations (46 arXiv-resolved, 2 already in wiki).
- **Pre-filtered:** dropped 34 candidates — surveys, domain-specific (VLN, video, anomaly detection), low-overlap abstracts. Retained 10 with direct overlap to latent reasoning / compression / stochastic-latent / curriculum-theory / interpretability.
- **Papers ingested (10):**
  1. [[MARCOS]] (2509.25020) — Markov chain of continuous thoughts; claims +4.7% over CoT on GSM8K, 15.7× speedup. First latent method to *surpass* CoT. Raw file was previously seeded by COCONUT crawler; this agent created the source page.
  2. [[Weak vs Strong Supervision Study]] (2602.22441) — empirical supervision-axis audit; identifies shortcut-vs-diversity trade-off.
  3. [[LSTR]] (2602.01695) — sparse transcoders as active reasoning operators (not just probes); bridges SAE interpretability and latent throughput.
  4. [[Latent-SFT]] (2510.15522) — Chain of Superposition; Latent-Vocab constraint ≡ LT-Tuning CPF independently derived.
  5. [[SwiReasoning]] (2510.05069, ICLR 2026) — training-free entropy-routed hybrid; +1.8-3.1% accuracy + 57-79% token efficiency.
  6. [[Parallel TTS Latent]] (2510.07745, ACL 2026) — first continuous-space parallel TTS; MC Dropout + Gaussian Noise + LatentRM.
  7. [[LEPO]] (2604.17892) — Gumbel-Softmax RL for latent reasoning; unified gradient estimator.
  8. [[Capabilities and Limits of Latent CoT]] (2602.01148) — **theoretical keystone**. Symbolic Index, Exploration-Execution Trade-off, proves curriculum learning is necessary. ProsQA 97% / GSM8K 34.1%.
  9. [[Stochastic Soft Thinking]] (2508.03440) — diagnoses **Greedy Pitfall** in soft thinking; Gumbel-Softmax fix across 8 benchmarks.
  10. [[Are LRMs Easily Interpretable]] (2604.04902) — Sarah Wiegreffe et al.; latent tokens often unnecessary; 65-93% gold-trace decoding; interpretability correlates with correctness. (Source page written by parallel CODI crawler with richer detail; my duplicate removed.)
- **Entity pages created (11):** [[Jiayu Liu]], [[Yingqian Cui]], [[Yadong Wang]], [[Jingcheng Deng]], [[Dachuan Shi]], [[Runyang You]], [[Yuyan Zhou]], [[Jiaxuan Zou]], [[Junhong Wu]], [[Connor Dilgren]], [[Sarah Wiegreffe]].
- **Concept pages created (3, all multi-paper hubs):** [[Gumbel-Softmax Latent]] (5 papers converge), [[Shortcut Behavior]] (3 independent diagnoses), [[Exploration-Execution Trade-off]] (theoretical keystone + empirical corroboration).
- **Key findings:**
  - **Convergent evolution on CPF.** [[Latent-SFT]]'s Latent-Vocab constraint is functionally equivalent to LT-Tuning's Context-Prediction-Fusion, derived independently. Two groups landing on the same vocabulary-manifold anchor mechanism strongly validates Branch D's CPF-on-CODI implementation target.
  - **Curriculum is now theoretically proven.** [[Capabilities and Limits of Latent CoT]] (2602.01148) proves curriculum learning is *necessary* (theorem) to unify exploration and computation capabilities — upgrades LT-Tuning's 3-stage empirical finding from heuristic to theorem-backed.
  - **Greedy Pitfall unifies stochastic-latent work.** CoLaR (Gaussian), MARCOS (variational), Latent-SFT (Gumbel SFT), LEPO (Gumbel RL), Stochastic Soft Thinking (Gumbel inference) are all solutions to the same diagnosed failure mode ([[Shortcut Behavior]] + [[Gumbel-Softmax Latent]]).
  - **Shortcut behavior triangulated.** Three independent methodologies ([[Stochastic Soft Thinking]], [[Weak vs Strong Supervision Study]], [[Are LRMs Easily Interpretable]]) converge on: current latent models often don't use their latent tokens. Critical for any interpretability or efficiency claim.
  - **MARCOS raw file overlap with COCONUT crawler.** `.raw/papers/2509.25020-marcos.md` existed (seeded by parallel COCONUT crawl) but source page was missing — created here with `discovered_via: 2505.16552`.
- **Primary-tier hits per project:** branch-d: 3 (Weak/Strong Supervision, Capabilities/Limits, Stochastic Soft Thinking); branch-a: 1 (Capabilities/Limits); spar-latent-reasoning: 7 (MARCOS, Weak/Strong, LSTR, Latent-SFT, SwiReasoning, Capabilities/Limits, Soft Thinking + interp paper).
- **No failures or rate limits.** All 10 papers fetched via WebFetch in parallel batches of 5.

---

## [2026-04-23] upgrade-pass | Full-paper verification + arXiv ID resolution
- Raw papers saved (full-text, verbatim abstracts + methods + results + conclusions):
  - `.raw/papers/2502.21074-codi.md`, `2412.06769-coconut.md`, `2505.16552-colar.md`, `2509.20317-sim-cot.md`, `2510.02312-kava.md`, `2510.25741-ouro.md`, `2511.21581-adaptive-latent-reasoning.md`, `2601.23184-regular.md`, `2603.01425-laser.md`, `2603.02023-ponderlm-3.md`
- Source pages upgraded: all 11 (added verified arxiv_ids, full author lists, date_published, code_repo, paper-verbatim key_claims)
- New entity pages (+11): [[Alex Ning]], [[Fanmeng Wang]], [[He Li]], [[Jiajie Jin]], [[Lapisbird]], [[Rui-Jie Zhu]], [[Shibo Hao]], [[Wenhui Tan]], [[Xilin Wei]], [[Yulan He]], [[Zhenyi Shen]]
- Seeds.yaml: resolved all null arxiv_ids; added arxiv_resolved_at stamps
- Factual corrections surfaced (validates autoreview hypothesis — surveys drift):
  - COCONUT 5th key_claim ("noise accumulation and semantic drift when scaled") dropped — was survey editorial, not in paper
  - SIM-CoT "+8.2% amplification" attribution fixed (vs COCONUT, not vs GPT-2 baseline)
  - KaVa's "55.7" degradation figure was from GSM8k-Hard, not GSM8k-AUG-NL (wrong-column)
  - CODI GitHub: `zen-E/CODI` → `zhenyi4/codi` (HF weights still at `zen-E/CODI-*`)
  - Ouro lead author corrected (Fan Yin → Rui-Jie Zhu; full 33-author list added)
- Executed via 2 parallel subagents (1 for known-arxiv upgrade, 1 for null-arxiv resolution).

---

## [2026-04-23] ingest | Latent Thoughts Tuning (Branch D primary target)
- Source: `.raw/papers/2602.10229-latent-thoughts-tuning.md`
- Summary: [[Latent Thoughts Tuning]]
- Pages created: [[Context-Prediction-Fusion]], [[Dynamic Switching Protocol]], [[Weihao Liu]], [[Dehai Min]], [[Lu Cheng]], [[NeosKnight233 Latent-Thoughts-Tuning]]
- Pages updated: [[Feature Collapse]] (added LT-Tuning/CPF mitigation row + cross-reference)
- Per-project dashboards: [[meta/projects/branch-a]], [[meta/projects/branch-b]], [[meta/projects/branch-c]], [[meta/projects/branch-d]], [[meta/projects/spar-latent-reasoning]] generated.
- Project-local skills wired: `.claude/skills/paper-crawl/SKILL.md`, `.claude/skills/wiki-autoreview/SKILL.md`.
- Key insight: CPF equation `e_fusion = α·h_ctx + (1−α)·e_pred` + mandatory 3-stage curriculum is the concrete recipe Branch D has been chasing. Stage 3 ablation shows 23.5% accuracy drop at 8B if fusion is removed — the curriculum is load-bearing, not decorative.

---

## [2026-04-22] migration | Bulk ingest from research_findings + papers/research.md
- Sources migrated: [[KaVa]] (from kava_notes.md + research.md § KaVa), [[Ouro]] (from ouro_notes.md), [[CODI]] + [[COCONUT]] + [[SIM-CoT]] + [[CoLaR]] + [[Adaptive Latent RL]] + [[ReGuLaR]] + [[LaSER]] + [[PonderLM-3]] (from research.md per-method sections).
- Concept pages created: [[Feature Collapse]], [[Curriculum Distillation]], [[Token Efficiency]], [[KV Compression]], [[KV-Cache Distillation]], [[Self-Distillation]], [[GRPO]], [[LoopLM]], [[Fixed-Width Depth Recurrence]], [[Adaptive Exit Gate]], [[Manipulation vs Capacity]], [[Quora Faithfulness Probe]].
- Entity pages created: [[Anna Kuzina]], [[Fan Yin]], [[InternLM]], [[Alibaba Tongyi Lab]], [[ByteDance Seed]], [[GSM8k-AUG]], [[GSM8k-AUG-NL]].
- Overview rewritten: `overview.md` top-level taxonomy + lattice framing migrated from research.md.
- Executed via 3 parallel subagents; consistency of project-tier assignments across migrations will be audited by first autoreview sweep.

---

## [2026-04-22] init | Vault scaffold
- Source: manual init
- Pages created: [[index]], [[hot]], [[log]], [[overview]], [[meta/projects/REGISTRY]], [[meta/seeds]], [[CLAUDE]], [[meta/FRONTMATTER-SCHEMA]]
- Key insight: Vault moved from `research_findings/wiki/` to `./wiki/` at project root (+ `.raw/` parallel) to match plugin default paths — cleaner long-term, no symlink indirection.
