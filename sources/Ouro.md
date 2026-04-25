---
type: source
title: "Ouro: Scaling Latent Reasoning via Looped Language Models"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - domain/architecture
  - type/source
  - method/looped-lm
status: read
related:
  - "[[LoopLM]]"
  - "[[Fixed-Width Depth Recurrence]]"
  - "[[Adaptive Exit Gate]]"
  - "[[Manipulation vs Capacity]]"
  - "[[Quora Faithfulness Probe]]"
  - "[[ByteDance Seed]]"
  - "[[Fan Yin]]"
  - "[[Parcae]]"
  - "[[Mechanistic Analysis of Looped Reasoning LMs]]"
  - "[[From Growing to Looping]]"
  - "[[RLTT]]"
  - "[[Think-at-Hard]]"
  - "[[Formal CoT vs Latent]]"
  - "[[Are LRMs Easily Interpretable]]"
  - "[[Adaptive Loops and Memory]]"
  - "[[Step-Decomposed Influence]]"
  - "[[LaDiR]]"
sources:
  - "[[.raw/papers/ouro_notes]]"
  - "[[.raw/papers/2510.25741-ouro]]"

source_type: paper
arxiv_id: "2510.25741"
venue: "arXiv"
date_published: 2025-10-29
authors:
  - "Rui-Jie Zhu"
  - "Zixuan Wang"
  - "Kai Hua"
  - "Tianyu Zhang"
  - "Ziniu Li"
  - "Haoran Que"
  - "Boyi Wei"
  - "Zixin Wen"
  - "Fan Yin"
  - "He Xing"
  - "Lu Li"
  - "Jiajun Shi"
  - "Kaijing Ma"
  - "Shanda Li"
  - "Taylor Kergan"
  - "Andrew Smith"
  - "Xingwei Qu"
  - "Mude Hui"
  - "Bohong Wu"
  - "Qiyang Min"
  - "Hongzhi Huang"
  - "Xun Zhou"
  - "Wei Ye"
  - "Jiaheng Liu"
  - "Jian Yang"
  - "Yunfeng Shi"
  - "Chenghua Lin"
  - "Enduo Zhao"
  - "Tianle Cai"
  - "Ge Zhang"
  - "Wenhao Huang"
  - "Yoshua Bengio"
  - "Jason Eshraghian"
url: "https://arxiv.org/abs/2510.25741"
code_repo: "http://ouro-llm.github.io"
has_weights: true
status: read
confidence: high
key_claims:
  - "Weight-tied depth recurrence applied to the same token positions (LoopLM) matches 2-3× larger standard transformers on reasoning benchmarks at 1.4B/2.6B scales."
  - "Looping does not increase knowledge capacity (≈2 bits/param for Loop-1 and Loop-4 on Capo); gains are in knowledge manipulation, not memorization."
  - "Performance peaks at or near the trained recurrent depth (T=4) and degrades beyond T=5-8; T=1 is catastrophic on reasoning benchmarks."
  - "Reducing recurrent steps from 8 to 4 in pretraining Stage 1b eliminated loss spikes and gradient oscillations; stability scales inversely with backward-chain length."
  - "Linear probes at end of previous recurrent step do NOT reliably predict the next step's answer on Quora (36.1% agreement between step 2 and step 4), while Qwen3-4B-Thinking probes hit 0.99 ROC AUC early — LoopLM provides causally faithful intermediate reasoning."
  - "RLVR (DAPO/GRPO) post-SFT failed to beat the SFT checkpoint because vLLM/SGLang rollouts assume fixed execution path, breaking under variable-depth computation."
  - "Last-step KV cache sharing during decoding reduces memory 4× with <0.3 pt loss on GSM8K/MATH-500; first-step sharing is catastrophic (GSM8K 78.92 → 18.73)."

projects:
  - slug: "branch-a"
    relevance: reference
    why: "From-scratch looped pretraining recipe; not architecture-dependent latent-reasoning at Qwen3 scale."
  - slug: "branch-b"
    relevance: reference
    why: "Ouro's 8→4 recurrent-step reduction is the stability analog of our detach ablation (shorten backward chain) but they still do full BPTT — tangential to min-sufficient detach story."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No bearing on Qwen3 probe methodology or convergence debugging."
  - slug: "branch-d"
    relevance: reference
    why: "Fixed-width depth recurrence is fundamentally different from CODI/LT-Tuning sequence-growing latents; 7.7T-token pretraining is out of our compute budget; useful framing contrast only."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Publicly released 1.4B/2.6B base + Thinking checkpoints with self-reported interpretability gap (no tuned lens, no circuits) — directly actionable target for our tuned-lens / activation-oracle / latent-anchor pipeline; Quora faithfulness and Capo/Mano manipulation-vs-capacity protocols reusable for CODI evaluations."

last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Ouro: Scaling Latent Reasoning via Looped Language Models

**Framework name:** LoopLM. **Ouro** is the specific model family (1.4B, 2.6B + Thinking variants).
**Affiliations:** ByteDance Seed + UC Santa Cruz + Princeton + Mila (Bengio, Eshraghian advising).

## Core contribution

Ouro builds latent reasoning into pretraining **from scratch** rather than fine-tuning it onto an instruct model (as [[CODI]] / [[COCONUT]] / [[KaVa]] do). Two axes of departure:

- **CODI/COCONUT/KaVa** fine-tune with `<bot>...<eot>` tokens appended; each latent step adds a KV-cache position (sequence grows).
- **Ouro/LoopLM** applies the full transformer stack `t` times to the **same sequence positions** — [[Fixed-Width Depth Recurrence|weight-tied depth recurrence, no sequence-length growth]].

## Architecture

$$F^{(t)}(\cdot) = \text{lmhead} \circ \underbrace{M_L \circ M_L \circ \cdots \circ M_L}_{t \text{ times}} \circ \text{emb}(\cdot)$$

- **1.4B:** 24 layers × t loops, hidden 2048, MHA + RoPE + SwiGLU, vocab 49,152 (SmolLM2 tokenizer).
- **2.6B:** 48 layers × t loops, created by **upcycling** the 1.4B (layer duplication).
- **Max t (train):** 4 (reduced from 8 after instability — see stability section).
- **Max t (inference):** up to 8 (extrapolates; peaks at T=4, degrades past).
- **Sandwich RMSNorm:** RMSNorm before BOTH attention and FFN (critical for deep recurrence stability).

**Prefill:** all 4 recurrent steps need own KV caches (>10 pt drop on GSM8K if shared at prefill).
**Decoding:** last-step KV cache suffices (see KV cache sharing below).

## [[Adaptive Exit Gate|Entropy-regularized exit objective]] (Eq. 4)

$$\mathcal{L} = \sum_t p_\phi(t|x) \cdot \mathcal{L}^{(t)} - \beta \cdot H(p_\phi(\cdot|x))$$

- `p_φ(t|x)`: learned exit distribution via cumulative halt products `λ_t = σ(Linear(h^(t)))`.
- Uniform prior (equivalent to KL(p_φ || uniform)) — beats geometric priors (η=0.1…0.9) on loss and Pareto frontier. Geometric priors starve deep iterations of credit.
- **Stage II** trains the gate with BCE against a greedy label from per-step loss improvement `I^(t) = max(0, L^(t-1) - L^(t))`, sharp threshold `σ(k·(I−γ))`, k=50, γ=0.005.

**Q-Exit at inference:**

$$\text{CDF}(n|x) = 1 - \prod_{j=1..n}(1 - \lambda_j(x)); \quad t_{\text{exit}} = \min\{m : \text{CDF}(m) \ge q\}$$

`q ∈ [0,1]` is a deployment knob — no retrain needed to change compute-accuracy tradeoff.

## Training pipeline — 7.7T tokens total

Framework: **flame** (built on torchtitan). WSD LR schedule, peak 3e-4. AdamW (β1=0.9, β2=0.95), wd=0.1, grad clip 1.0. RoPE base 10K → 40K (CT Anneal) → 1M (LongCT/Mid).

| Stage | Phase | Tokens | Seq | Steps | β | Notes |
|-------|-------|--------|-----|-------|---|-------|
| 1a | Pre-train I (Exploration) | 3T | 4K | **8** | 0.1 | UNSTABLE — loss spikes |
| 1b | Pre-train II (Stability) | 3T | 4K | **4** | 0.1 | Forks 1.4B (kept) / 2.6B (upcycled 24→48) |
| 2 | CT Annealing | 1.4T | 16K | 4 | 0.05 | Math/code; cosine to 3e-5 |
| 3 | LongCT | 20B | 64K | 4 | 0.05 | ProLong-64K |
| 4 | Mid-training | 300B | 32K | 4 | 0.05 | SFT-mix; cosine to 1e-5 |

## Gradient flow — full BPTT (critical observation)

The paper uses **full BPTT through all recurrent iterations**. No gradient checkpointing, no truncated BPTT, no detach in the main loop. Only `stop_gradient` is in the adaptive exit gate loss (Stage II only).

They hit the same class of problem as our V2/V3 fp32 / detach ablations. §4.3:

> "reducing recurrent steps from 8 to 4 in Stage 1b ... stabilized training instabilities, including loss spikes"

Their solution: **shorten the backward chain** by reducing recurrent steps (8 → 4). Architectural analog of Josh's detach: cut the chain instead of detaching at each step.

Other stability tricks: sandwich RMSNorm, batch size 4M→8M, β annealed 0.1→0.05, LR deliberately lower than param-matched transformers would use.

## Reasoning SFT → Ouro-Thinking

- **8.3M SFT examples** (Math 3.5M, Code 3.2M, Science 808K, Chat 767K).
- 2 epochs, max seq 32K, LR 2e-5, cosine decay.
- Data: OpenThoughts3, AceReason-1.1-SFT, OpenCodeReasoning, Llama-Nemotron-Post-Training, OO1-Chat-747K, DeepWriting-20K.
- Codebase: LlamaFactory.

## RL failure mode — open infra problem

Post-SFT RLVR with DAPO and GRPO on DAPO-17K. **Neither beat SFT.**

Root cause: vLLM/SGLang fast-rollouts assume **fixed execution path** — breaks under LoopLM variable depth.

- Off-policy rollouts (generate full 4-step, pick first-token-over-threshold, use cumulative loss up to that step): off-policy mismatch (tokens from depth=4, losses from earlier) killed it.
- Fixed 4-round RL: no off-policy issue but no improvement. Hypothesis: low headroom post-SFT at small scale.

Surprise: even trained fixed at T=4, the model still chose fewer rounds when beneficial at inference. Generalization mechanism unclear.

**Implication:** any RL-based latent-reasoning work (GRPO/DAPO on CODI included) needs custom rollout infra supporting dynamic depth.

## Results

### Base model

**Ouro-1.4B (R=4) vs 1-4B baselines:**
- MMLU 67.35 (vs Qwen3-4B 73.19)
- **BBH 71.02** (vs Qwen3-4B 70.95) — beats 4B
- **GSM8K 78.92** (vs Qwen3-4B 72.86) — beats 4B
- **MATH500 82.40** (vs Qwen3-4B 59.60, Gemma3-4B 68.60) — dominant
- HumanEval+ 67.40 (vs Qwen3-4B 70.70)

**Ouro-2.6B (R=4) vs 3-12B:**
- **MMLU-Pro 55.73** (vs Qwen3-8B 53.72) — beats 8B
- **BBH 80.46** (vs Qwen3-8B 77.65, Gemma3-12B 78.41) — beats 12B
- **MATH500 90.85** (vs Gemma3-12B 83.20) — beats 12B
- MBPP 80.40

### Thinking variants

Ouro-1.4B-Thinking competitive with Qwen3-4B (AIME24 pass@1: 65.0 vs 61.3). Ouro-2.6B-Thinking matches/exceeds Qwen3-8B on several (AIME25 pass@10: 76.7 vs 81.3; OlympiadBench 76.44 vs 75.25).

### Depth scaling

Performance peaks at or near T=4 (trained depth); degrades at T=5-8. Exception: Ouro-1.4B-Thinking peaks at T=5 on OlympiadBench (72.30). T=1 is catastrophic (AIME24 pass@1 → 0.0 for 1.4B-Thinking).

Ouro-1.4B base:

| T | MMLU | ARC-C | HellaSwag |
|---|------|-------|-----------|
| 1 | 41.21 | 37.63 | 55.24 |
| 4 | **67.45** | **60.92** | **74.29** |
| 8 | 64.49 | 58.19 | 71.60 |

### Early-exit Pareto (Fig. 5, MMLU)

1. Trained Ponder Gate — best (~66% @ 2.5 avg rounds).
2. Untrained Ponder Gate (entropy reg only) — ~64% @ 2.5, closely tracks trained.
3. Hidden-state-difference threshold `‖h_t − h_{t−1}‖ < ε` — within 1-2% of trained gate.
4. Static exit — dominated.

Takeaway: representation stability is a decent "done computing" proxy; entropy reg alone already learns useful halting.

### KV cache sharing (Table 14)

Decoding only (prefill always needs full caches):

| Strategy | GSM8K | MATH-500 | Memory |
|----------|-------|----------|--------|
| Full (4× cache) | 78.92 | 82.40 | 1.00× |
| First-step only | **18.73** | 8.43 | 0.25× — catastrophic |
| **Last-step only** | **78.85** | **80.40** | **0.25×** |
| Averaged | 78.73 | 78.52 | 0.25× |

Final-step representations dominate autoregressive generation.

## Physics-of-LMs experiments (§6)

### Capo — knowledge capacity

GPT-2 style 1M-40M params, bioS(N) synthetic biographies, 1000 exposures.
**Loop-1 and Loop-4 both ≈2 bits/parameter.** Looping does NOT raise capacity. Parameter count is the memorization bottleneck.

### Mano — knowledge manipulation

Modular arithmetic on binary trees, depth L ∈ {10, 16, 24}.

| Setup | L=10 | L=16 | L=24 |
|-------|------|------|------|
| Base (12⊗1) iso-FLOP | 93.6 | 94.4 | 34.8 |
| Base (2⊗1) | 21.5 | 8.4 | 7.5 |
| **Loop (2⊗6)** | **98.1** | **96.3** | **78.0** |
| Base (6⊗1) | 84.7 | 59.5 | 20.0 |
| **Loop (6⊗2)** | 93.4 | 88.5 | 35.1 |

Looped models beat iso-parameter AND iso-FLOP baselines on deep composition.

### Multi-hop QA (Fig. 7)

Loop-2/Loop-4 learn 3-hop QA with significantly fewer samples and faster convergence than iso-param Loop-1. Gain is in **sample efficiency**, not asymptotic accuracy.

### Graph reachability (Theorem 1)

Single-layer transformer, hidden `O(n)`, `O(log² D)` loops solves combined context+parametric reachability (D=graph diameter).

| Method | Sequential steps |
|--------|------------------|
| Discrete CoT | O(n²) |
| Continuous CoT (COCONUT) | O(D) |
| **LoopLM / Universal Transformer** | **O(log D)** |

Mechanism: repeated squaring via attention (all-pairs reachability doubling each loop) — parallel expansion across the whole graph per loop, not step-by-step.

### MMLU category analysis (App. B.4)

T=1 → T=4 gains:
- **Reasoning-heavy:** Elementary math +155.6%, Formal logic +143.3%, Logical fallacies +127.8%, High-school stats +126.9%.
- **Retrieval-heavy:** Moral scenarios +7.8%, Global facts +8.3%, Virology +13.7%, Anatomy +21.4%.

Strongly supports the [[Manipulation vs Capacity|manipulation-not-capacity]] thesis.

## Safety (§7.1)

HEx-PHI: harmfulness score improves monotonically with recurrent steps, **including extrapolation T=5-8**. Ouro-1.4B-Thinking @ T=4: harmful rate **0.009** (matches Qwen3-4B-Thinking). 2.6B: **0.003**.

PCA on last-input-token hidden state (Fig. 8b): at T=1 benign/harmful entangled; at T=4 separable; unsafe responses cluster at boundary. **Safety = representation separability; more loops keeps improving it past trained depth** even when task performance degrades.

## Faithfulness (§7.2) — [[Quora Faithfulness Probe]]

Quora Question Pairs, linear probes on hidden states at layer 24i to predict step-i answer.

- **Qwen3-4B-Thinking baseline:** probe at early layers → **0.99 ROC AUC** predicting final answer. Token CoT is **post-hoc rationalization**.
- **Ouro 1.4B (R=4):** probes at layer 24(i−1) (end of previous step) do NOT reliably predict step-i answer for i ∈ {2, 3, 4}.
- Agreement matrix: step 2 ↔ step 4 only **36.1%**; step 2 ↔ step 3 = 55.1%. Each loop genuinely updates the decision.
- Past T=4 (extrapolation): agreement → ~90% (fixed point; model stops reasoning beyond trained depth).

Claim: LoopLM provides **causally faithful** intermediate reasoning in a way token-level CoT does not.

## Deployment advantages (§7.3)

Because `Text(R_s)` and `Text(R_T)` share a latent trajectory:

1. **Native speculative decoding** — `Text(R_s)` proposes, `Text(R_T)` verifies; no external draft model.
2. **Joint acceleration + preemptive safety** — screen intermediate predictions before streaming.
3. **Anytime generation with monotone refinement** — training enforces `E[L^(t+1)] ≤ E[L^(t)]`; any step is a valid output.

## Scaling laws (App. D, E)

$$\mathcal{L}_{\text{total}} = E + \frac{A}{(N+t_1)^\alpha} + \frac{B}{(D+t_2)^\beta} + \frac{C}{(T_{\max}+t_3)^\gamma} \quad (R^2 \approx 0.9596)$$

Validated by leave-out fits on model size (R² preserved), training data (25/50/75% fit → 0.94-0.96), max recurrent step (fit 2 of {2,4,8} → R² ≈ 0.96).

**Findings:**
- Standard model > LoopLM at same parameters on benchmarks; gap widens with more recurrent steps, shrinks with model size.
- **γ > 0:** step-wise loss consistently decreases with depth.
- At small sizes the model "exploits" shallow step-wise loss (grows with training) via the learned gate to reduce total loss — suggests clean step-wise dynamics need larger models.

## Interpretability gap — our opportunity

The paper reports **limited** interpretability analysis across loop iterations. Have:
- PCA of final hidden state at different recurrent steps (safety).
- Linear probes at 24i → step-i answer (faithfulness).
- Step-by-step agreement on Quora.

Missing:
- Tuned lens across loop iterations.
- Layer-within-loop activation analysis.
- Hidden-state trajectory PCA/UMAP beyond safety framing.
- lm_head-decoded intermediate outputs at each loop.
- Mechanistic interp (circuits, head analysis).
- Comparison of learned representations to explicit CoT traces.

Released public checkpoints + open gap ⇒ prime target for our tuned-lens / activation-oracle / latent-anchor pipeline.

## Compute cost

Not benchmarked rigorously. 4-step 1.4B ≈ 5.6B FLOPs-equiv per forward. "2-3× parameter efficiency" claim is vs 4B/8B baselines — no comparison to a dense 5.6B trained identically on 7.7T.

Inference: with last-step KV sharing, decoding memory comparable to standard transformer of same param count; prefill is 4× heavier.

## Relevance to our work

### Ouro teaches us

1. Latent reasoning scales when **baked into pretraining** — CODI-style LoRA post-hoc may hit a ceiling fundamentally.
2. Reducing recurrent steps for stability is legitimate; Josh's detach and Ouro's step-reduction solve the same problem from different angles.
3. [[Fixed-Width Depth Recurrence]] is a real alternative to sequence-growing latent tokens — could be tried with COCONUT (reuse positions instead of append).
4. The **manipulation-vs-capacity** framework (Capo + Mano + Multi-hop QA) is directly reusable to ask: "does CODI increase knowledge capacity or manipulation?"
5. The **Quora faithfulness protocol** is a strong eval for CODI too — probe each latent position on ambiguous tasks (Quora, WiC) to test whether CODI latents update decisions or post-hoc rationalize.
6. Interpretability gap is narrower than we thought but still open.
7. RLVR + dynamic depth is upstream-broken; any RL + latent reasoning experiment needs custom rollout infra.

### Ouro does NOT help with

1. Cannot use Ouro checkpoints as a CODI base — architecture is fundamentally different (no `<bot>`/`<eot>`, fixed-width vs sequence-growth).
2. From-scratch 7.7T pretraining is out of budget.
3. No code/guidance for fine-tuning an existing model into a looped architecture.
4. Scale (7.7T tokens) is infeasible to replicate.

## Model availability

Public release at http://ouro-llm.github.io. Base + Thinking variants for 1.4B and 2.6B. Need to verify:
- Exact HF repo names (likely ByteDance or LoopLM org).
- License.
- Inference code (vLLM/SGLang custom PRs by Fan Yin).
- Whether adaptive-exit gate weights are in the release.

## Eval reproduction targets

Standardized via lm-eval-harness + evalplus (Table 16).

- **General:** MMLU (5-shot logprob), MMLU-Pro (5-shot CoT), BBH (3-shot CoT), ARC-C (25-shot logprob), HellaSwag (10-shot), Winogrande (5-shot).
- **Math/code:** GSM8K (3-shot CoT), MATH500 (5-shot CoT, in-house), HumanEval/+ (pass@1), MBPP/+ (pass@1).
- **Reasoning:** AIME 2024/2025 (pass@1, pass@10), OlympiadBench, GPQA, SuperGPQA, BeyondAIME, HLE — in-house LLM-as-judge @ temp=1.0, top_p=0.7.
- **Safety:** HEx-PHI (330 ex, 11 cats, GPT-4o judge, 1-5).
- **Faithfulness:** Quora Question Pairs (linear probes).

Most already present in `configs/evaluation/broader_suite_plus_p3_gemma3_gh200.yaml`. Net-new: AIME24/25, OlympiadBench, GPQA, SuperGPQA, BeyondAIME, HLE, HEx-PHI, Quora.
