---
type: meta
title: "Hot Cache"
updated: 2026-04-24T02:00:00
---

# Recent Context

## Last Updated

2026-04-24 (autoresearch batch #1). Three parallel autoresearch agents completed synthesis sweeps on stability theory, information/distribution regularization, and disentanglement/sparse coding. Consolidation filed at [[meta/autoreview/2026-04-24-autoresearch-consolidation]].

## Top 5 findings from this batch (2026-04-24 autoresearch)

1. **Noise injection ≡ Jacobian-Frobenius regularization at zero compute overhead** ([[Noisy Recurrent Neural Networks]] SDE-limit theorem, Lim et al. 2021). For hidden-state noise $z_t \leftarrow z_t + \sigma\epsilon$ the implicit regularizer is $\frac{\sigma^2}{2}\mathbb{E}[\|J_f\|_F^2]+O(\sigma^4)$. This unifies [[Stochastic Soft Thinking]], [[Multiplex Thinking]], and [[Stabilizing Equilibrium Models by Jacobian Regularization]] — they're the same mechanism. Highest-value-per-effort F6 intervention.

2. **F5 swap-null is literally the InfoNCE training signal** ([[Contrastive Predictive Coding]]). The F5 eval (shuffle latents within batch; measure accuracy delta) is the test-time version of the InfoNCE training loss. A swap-NCE loss $\mathcal{L} = -\sum_i \log\frac{\exp(z_i^T W q_i)}{\sum_j \exp(z_j^T W q_i)}$ forces $I(Z;Y|\text{question}) > 0$ by construction. The F5 protocol is a training signal waiting to be used.

3. **F3 template-lock is canonical superposition-at-position-granularity** ([[Toy Models of Superposition]]). 7-into-1 direction packing is geometrically the same phenomenon Elhage 2022 formalizes, applied at position rather than neuron granularity. SAE on CODI latents is the definitive diagnostic; attribution patching ([[Sparse Feature Circuits]]) gives a causal baseline that resolves Branch C's LTO-vs-DDR probe-typology contest.

4. **No-recall fixed points are countable → cannot be input-dependent** (Labovich 2026 theorem, [[Stability and Generalization in Looped Transformers]]). Cleanest formal explanation of F5 swap-null. CODI's base rollout is no-recall; CPF makes it recall-mode by injecting context each step. Theorem *predicts* F5 AND *predicts* CPF will cure it — an actual testable implication.

5. **CPF is not a hack — it's the specific inductive bias that breaks Locatello's impossibility theorem** ([[Causal Disentanglement]]). Unsupervised disentanglement is provably impossible without inductive biases on model or data. CPF's $e_\text{fusion} = \alpha h_\text{ctx} + (1-\alpha) e_\text{pred}$ is equivalent to (a) auxiliary-variable supervision, (b) sparse mechanism shift, (c) multi-environment invariance — the three canonical inductive biases. Upgrades CPF from empirical trick to theoretically load-bearing.

### Runner-up findings worth surfacing

- **F6 narrow basin = per-step Jacobian norm $\rho(J_f) \geq 1.3$** implies 8× amplification through $M=8$ rollout. Parseval retraction ($W \leftarrow (1+\beta)W - \beta WW^TW$) forces $\|J\|_2 \leq 1$ mechanically, eliminating the rank-1 dominance signature of F3 simultaneously. Half-day engineering cost.
- **CALM (Oct 2025) observed the direct analogue of F3** — 71/128 latent dimensions collapse to prior without remediation — and fixed with per-dim KL clip $\lambda_\text{KL} = 0.5$. Adapted per-position this is a drop-in F3 intervention.
- **KL-regularized RL collapses to single mode at the global optimum, not as an optimisation artifact** ([[KL-Regularized RL is Designed to Mode Collapse]]). Any CPF variant that's later RL-fine-tuned will undo its anti-collapse gains unless MARA-style reward shaping is added. Negative result we must cite.
- **Step-Level SAE (2026)** isolates per-position *incremental* content via context-conditioning. Directly tests whether F3's 7 empty positions hold invisible-but-real content ($\|I^k\|_1 > 0$) or are genuinely empty — a question the F-battery alone cannot answer.

## Top 5 interventions ranked by cost/impact (from stability synthesis)

| # | Intervention | Compute | Eng. time | Addresses |
|---|---|---|---|---|
| 1 | Noise injection at each latent step ($\sigma\sim 0.1$) | 0% | 0.5 day | F6 basin |
| 2 | Orthogonal init of recurrent-block weights | 0% | 0.5 day | F3, F6 |
| 3 | Parseval retraction $\beta=10^{-3}$ on recurrent weights | ~1% | 1 day | F3, F6 |
| 4 | Hutchinson Jacobian-Frobenius penalty $\lambda=10^{-3}$ | ~15% | 2 days | F3, F6 |
| 5 | Full DEQ reformulation with Anderson root-finding | ~50% | 2 weeks | F3, F5, F6 |

(1)+(2) first as zero-cost sanity check; add (3) if insufficient; (4) only if needed; (5) is the north-star arc.

## Recommended Branch D V3 regularization stack (from info/dist synthesis)

$$\mathcal{L}_\text{total} = \mathcal{L}_\text{CE}(y) + \lambda_1 \mathcal{L}_\text{KL-clip} + \lambda_2 \mathcal{L}_\text{swap-NCE} + \lambda_3 \mathcal{L}_\text{VIC-var}$$

- Start $\lambda_1 = 1$, $\lambda_2 = 0.1$, $\lambda_3 = 1$, $\lambda_\text{KL} = 0.1$, variance-hinge $\gamma = 0.3 \cdot \text{mean-LN-std}$. Ablate.

## Active project reading queues (carried forward from sweep #2)

- **Branch A (Stable Qwen3 Scaling):** 15 primary. Core unchanged (SIM-CoT, Soft Tokens Hard Truths, Capabilities-and-Limits, COCONUT, CODI). New additions: Scaling Up TTC, Retrofitted Recurrence, Mixture of Recursions, Encode Think Decode, AdaPonderLM, Two-Scale Latent Dynamics, Depth-Recurrent Attention Mixtures, Inner Loop Inference, Skip-a-Layer-or-Loop-it, Loop-Think-Generalize.
- **Branch B (Min-Sufficient Detach):** 5 primary. CODI, PCCoT + Scaling Up TTC (k=8 BPTT canonical), Retrofitted Recurrence (k=8 cross-architecture validation), Two-Scale Latent Dynamics (geometric stability diagnostics). **New addition from this batch:** stability-theory menu reframes detach itself as truncated IFT — see [[questions/Research - Stability Theory for Latent Recurrence]].
- **Branch C (Qwen3 Convergence — conditional):** 2 primary. Dynamics of Latent CoT + Decoding Depth-Recurrent Transformer. **New addition:** [[Sparse Feature Circuits]] + [[Step-Level Sparse Autoencoder]] give a principled resolution of the LTO-vs-DDR probe-typology contest.
- **Branch D (LT-Tuning CPF on CODI):** 15 primary. Core 14 stable. **New addition from this batch:** five concrete loss formulations (KL-clip, swap-NCE, VIC-var, CEB-CPF, pos-BT) with equation-level specs; see [[questions/Research - Info and Distribution Constraints for Latents]] and [[Distribution Regularizer Catalog]].
- **SPAR Latent Reasoning (umbrella):** 38 primary. This batch adds a stability-theory chapter, regularization chapter, and interpretability chapter to the writeup — each a standalone research synthesis page.

## Biggest findings preserved + extended (cumulative across sweeps)

### From this batch (2026-04-24)

- **Noise injection ≡ Jacobian-Frobenius regularization at zero overhead** — unifies Stochastic Soft Thinking, Multiplex Thinking, and Jacobian-reg DEQ.
- **F5 ≡ InfoNCE** — the eval is the loss; swap-NCE forces $I(Z;Y|q) > 0$ by construction.
- **F3 = superposition at position-granularity** — SAE is the diagnostic, attribution patching the causal baseline.
- **F5 theorem** — no-recall fixed points are countable (Labovich 2026), predicts CPF cures F5.
- **CPF breaks Locatello's impossibility theorem** — it's the inductive bias, not a hack.

### From sweep #2 (preserved)

- **Convergent evolution on CPF — now five independent groups.** LT-Tuning's `e_fusion = α·h_ctx + (1−α)·e_pred` has 4 siblings now: HRPO (learnable gate), Latent-SFT (Gumbel-SFT), Soft Thinking (anchor-to-vocab), and [[Multiplex Thinking]] (K-sample sparse CPF with code + checkpoints). Five independent discoveries of the same mechanism is strong evidence for a fundamental inductive bias. **Extension from this batch:** [[Causal Disentanglement]] upgrades this from "five convergent reinventions" to "correct instantiation of a theoretically-necessary inductive bias."
- **Curriculum/alignment necessity — theorem-backed but contested.** 2 independent theoretical necessity results ([[Capabilities and Limits of Latent CoT]] + [[ALiCoT]]) vs 2 independent empirical no-curriculum-needed results ([[Soft Tokens Hard Truths]] + [[Token Assorted]]). Unresolved four-way cluster.
- **Latent surpasses CoT milestone — now contested priority.** [[MARCOS]] reports +4.7% over token CoT on GSM8K (Sep 2025, 15.7× speedup). [[OneVL]] claims "first" across driving benchmarks (Apr 2026). MARCOS has priority on math; OneVL scoped to driving.
- **Shortcut behavior is real + measurable — now with 2 more diagnoses.** [[Stochastic Soft Thinking]], [[Weak vs Strong Supervision Study]], [[Are LRMs Easily Interpretable]] baseline trio joined by [[ThinkRouter]] (confidence-correlates-wrong) and [[Latent Exploration Decoding]] (layer-asymmetric entropy). Five convergent failure-mode diagnostics, each on a different axis.
- **Feature Collapse is layer-asymmetric, not uniform.** [[Latent Exploration Decoding]] + [[Latent Thinking Optimization]]: intermediate layers preserve entropy even when final layer collapses; reward-classifier can read what logit-lens cannot. This refines the [[Feature Collapse]] concept and opens a clear decoding-time intervention axis.
- **CODI latents are 65-93% decodable** when operand context is provided.
- **Ouro's RL failure is solved** by [[RLTT]].
- **Depth-recurrence scaling law** per [[Parcae]].
- **Complexity-theoretic CoT-vs-latent** per [[Formal CoT vs Latent]].
- **Recurrent-depth retrofit is feasible without from-scratch pretraining.** [[Retrofitted Recurrence]] (UMD, Geiping lab) converts TinyLlama/OLMo/Llama-3.2-1B to depth-recurrent via curriculum + k=8 truncated BPTT. Directly applicable to Qwen3-4B without the 800B-token Frontier run of Huginn.
- **Huginn iteration sampling vs Ouro exit gate vs LoopFormer shortcut modulation.** Three distinct design points in the "make a shared block behave meaningfully across iteration counts" space. 3×2 matrix with BPTT truncation (full vs k=8).
- **Two-Scale Latent Dynamics provides geometric stability metrics** — step-norm + consecutive-angle signatures of fixed-point convergence. Portable measurement for Branch B detach ablations.
- **Implicit Reasoning Survey taxonomy is the writeup's organizing skeleton** — 3 top-level paradigms (latent optimization / signal-guided control / layer-recurrent execution), 6 cross-cutting challenges. Fits our existing vault cleanly.
- **Hybrid latent/discrete reasoning is a recurring design pattern, not a one-off.** [[ThinkRouter]] + [[SwiReasoning]] + [[HRPO]] — three independent groups at training-free, learned-gate-RL, and switch-based respectively. Collectively establish the hybrid design space.

## Top 3 contradictions flagged (carried + new)

1. **OneVL "first latent-CoT to surpass explicit" vs [[MARCOS]] priority.** (sweep #2)
2. **ALiCoT Order-r decay theorem vs no-curriculum empirics.** (sweep #2)
3. **[[ThinkRouter]] confidence-correlates-with-wrongness vs [[Weak vs Strong Supervision Study]] + [[Stochastic Soft Thinking]] shortcut framing.** (sweep #2)

### New contradictions this batch (2026-04-24)

- **Hard orthogonality: Parseval beneficial (Cisse 2017) vs harmful (Vorontsov 2017).** CNN-on-CIFAR information-rich regime favors exact Parseval; RNN long-dependency info-bottlenecked regime favors soft spectral margin. Resolution: try soft margin first ($m \in \{0.01, 0.05, 0.1\}$); fall back to exact Parseval only if margin doesn't suffice.
- **InfoVAE vs VIB on posterior collapse.** InfoVAE claims VIB's per-example KL $q(z|x) \| p(z)$ *causes* collapse and proposes aggregated-posterior MMD; VIB predates this critique. Resolution: InfoVAE more credible for our "decoder too flexible" regime — use MMD or CALM KL-clip variant.
- **L1 vs L0 sparsity in SAEs.** Classical Bricken SAEs use L1; Gao 2024 Top-K + Rajamanoharan 2024 JumpReLU show L1 causes shrinkage + feature absorption. Resolution: prefer JumpReLU or Matryoshka for CODI application.
- **Unsupervised disentanglement impossibility vs sparsity-is-enough.** Locatello 2019 proves inductive bias is necessary; Cunningham/Bricken 2023 show sparsity yields interpretable features. Partial resolution: sparsity is one of the allowed biases; impossibility refers to distributional-independence-only models. We still need auxiliary signals (CPF) for *causal* (not just statistical) disentanglement.

## Active Threads

- **Just completed:** Autoresearch batch #1 (3 parallel agents, stability + info/dist + disentanglement). Consolidation: [[meta/autoreview/2026-04-24-autoresearch-consolidation]].
- **In flight:** Ideation + ranking agents surfacing new branch candidates from the three syntheses (tasks #34 / #35 in task list).
- **Branch D go/no-go readiness:** 15 primary sources reviewed; five concrete V3 loss formulations specified (KL-clip, swap-NCE, VIC-var, CEB-CPF, pos-BT). Ready to implement when spec turns from design → code.
- **Branch B next step:** the stability synthesis reframes detach as truncated IFT gradient — the V2-vs-no-detach question should be run as a proxy for "DEQ or not" rather than as a detach hyperparameter sweep.

## Key Recent Facts

- Vault path: `/Users/jrauvola/Desktop/wiki/`
- `.raw/` path: `/Users/jrauvola/Desktop/wiki/.raw/` (gitignored)
- Git remote: `jrauvola/personal_wiki` (private GitHub)
- Custom schema adds `projects:` tiered relevance and `paper` source_type.
- Project registry seeded with Branches A/B/C/D + spar-latent-reasoning umbrella.
- Autoreview discipline: LLM full-ingests every paper, assigns tiers, re-grades on schedule; human attention only for flagged contradictions.
- 108 sources, 33 concepts, 77 entities, 3 syntheses as of 2026-04-24 autoresearch batch #1.

## Recent corrections (preserved)

- None at the factual level from sweep #2 (tier re-calibrations only).

### Sweep #1 factual errata (preserved)

- COCONUT: survey-claim "vulnerable to noise accumulation" is NOT in the actual paper.
- SIM-CoT: "+8.2% amplification" vs COCONUT, not GPT-2.
- KaVa: 55.7 figure is GSM8k-Hard, not GSM8k-AUG-NL.
- CODI: repo is `zhenyi4/codi` (HF at `zen-E/CODI-*`).
- Ouro: lead author is Rui-Jie Zhu.
