---
type: question
title: "Research: Genealogy of Latent Reasoning (Pre-COCONUT History)"
question: "How did latent / continuous / implicit reasoning in neural networks come to be? What pre-2024 literature set up the COCONUT/CODI paradigm, and which 2024-2026 methods are genuine novelty vs re-invented wheels?"
answer_quality: solid
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - type/question
  - status/synthesis
  - genealogy
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Writeup cornerstone — a 'how latent reasoning came to be' section requires this genealogy. Also required for deciding which Wave-4 alternative training blocks are genuine novelty vs incremental."
  - slug: "branch-a"
    relevance: secondary
    why: "Scaling narrative benefits from grounding CODI/COCONUT in the 2016 → 2024 chain and identifying which precursor ideas have yet to be scaled."
  - slug: "branch-b"
    relevance: secondary
    why: "Detach ablation sits in the 'M-step BPTT with gradient-path surgery' family; Neural ODEs + DEQ show the principled alternatives in the same family."
  - slug: "branch-d"
    relevance: primary
    why: "CPF is the latest reinvention of a long-running thread (hidden-state anchoring in distillation); understanding what it *adds* requires understanding what Deng 2023, SIM-CoT, KaVa already do."
  - slug: "branch-c"
    relevance: reference
    why: "Context-only for probe debugging."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Implicit CoT Precursors]]"
  - "[[Adaptive Computation Time]]"
  - "[[Universal Transformers]]"
  - "[[PonderNet]]"
  - "[[Neural ODEs]]"
  - "[[Deep Equilibrium Models]]"
  - "[[Pause Tokens]]"
  - "[[Filler Tokens]]"
  - "[[Implicit CoT via Knowledge Distillation]]"
  - "[[Stepwise Internalization]]"
  - "[[Quiet-STaR]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
sources:
  - "[[Adaptive Computation Time]]"
  - "[[Universal Transformers]]"
  - "[[PonderNet]]"
  - "[[Neural ODEs]]"
  - "[[Deep Equilibrium Models]]"
  - "[[Pause Tokens]]"
  - "[[Filler Tokens]]"
  - "[[Implicit CoT via Knowledge Distillation]]"
  - "[[Stepwise Internalization]]"
  - "[[Quiet-STaR]]"
---

# Research: Genealogy of Latent Reasoning

**Autoresearch session:** 2026-04-22, 3 rounds, ~12 pages, 10 precursors surveyed.

## Executive answer

Latent reasoning in neural networks did not begin with COCONUT (Dec 2024). Two independent research programs, both initiated by Alex Graves in 2014-2016, converged in 2023-2024 to produce COCONUT and CODI. The **halting/adaptive-compute** line (ACT → UT → PonderNet → HRM / Ouro / MoR) produced the architectural pattern "apply a shared block T times with a halting head." The **implicit-CoT** line (Deng 2023 iCoT-KD → Pause Tokens → Quiet-STaR → Filler Tokens → Deng 2024 Stepwise Internalization) produced the pipeline "distill explicit CoT into hidden-state / extra-token computation." COCONUT = the marriage: Stepwise Internalization (curriculum from Deng 2024) + Pause Token delimiters (special tokens from Goyal 2023) + **continuous-thought feedback** (the genuine novelty, feeding the student's own hidden state back as the next input embedding). CODI is the same marriage but swaps the curriculum for single-stage self-distillation — an orthogonal design dimension.

Three threads that fed into the modern field are under-exploited by 2024-2026 methods:

1. **Continuous-depth compute (Neural ODEs 2018 / DEQ 2019).** The O(1)-memory gradient via adjoint / IFT is available since 2018 but not used at LLM scale. CODI's M-step BPTT is the *baseline*, not the *frontier*.
2. **Per-token latent thinking (Quiet-STaR 2024).** All COCONUT descendants use one latent block per prompt. Per-token granularity with continuous thoughts is an open direction.
3. **Pretraining with latent thoughts (Goyal 2023 + Zelikman 2024).** The field has converged on fine-tuning; continuous-thought *pretraining* is a genuinely open question that only [[Adaptive Latent CoT Pretraining]] has attempted.

---

## COCONUT re-read — exact training recipe

(From the full paper, arXiv:2412.06769v2 HTML, Dec 2024 / Nov 2025 v3.)

| Hyperparameter | Value | Source |
|---|---|---|
| Base model | Pre-trained GPT-2 (only) | "We use a pre-trained GPT-2 as the base model for all experiments." |
| Learning rate | $1 \times 10^{-4}$ | "The learning rate is set to 1×10⁻⁴" |
| Effective batch size | 128 | "while the effective batch size is 128" |
| Optimizer | Not explicitly stated in excerpts extracted (typical is AdamW; code repo should confirm) | — |
| Continuous thoughts per step ($c$) | 2 on GSM8k; 1 on ProntoQA/ProsQA | "2 latent thoughts (i.e., c=2) for each reasoning step"; "one continuous thought for every reasoning step (i.e., c=1)" |
| Stages (GSM8k) | 3 stages besides initial + 1 extra | "3 stages besides the initial stage" + final extension |
| Stages (ProntoQA/ProsQA) | 6 stages besides initial | "6 training stages in addition to the initial stage" |
| Epochs per stage (GSM8k) | 6 initial, 3 per subsequent | "6 epochs in the initial stage, and 3 epochs in each remaining stage" |
| Epochs per stage (ProntoQA/ProsQA) | 5 | "5 epochs per stage" |
| Total training | 50 epochs | "training until the 50th epoch" |
| Anti-forgetting mix rate | $p = 0.3$ | "always mixing data from other stages with a certain probability (p=0.3)" — used explicitly in Section 5 (analysis); not stated for main training |
| Forward passes per training step | $n + 1$ for $n$ scheduled latent thoughts | "We perform n+1 forward passes when n latent thoughts are scheduled" |
| Optimizer state | Reset at stage boundaries | "reset the optimizer when training stages switch" |
| Loss mask | On questions + latent thoughts; loss only on surviving language tokens + answer | "mask the loss on questions and latent thoughts" |
| Inference output constraint | $\mathcal{M}(x_{t+1} \mid x_{\leq t})$ undefined while in latent mode | "is not defined when i<t<j, since the latent thought is not intended to be mapped back to language space" |

### What makes COCONUT fundamentally different from CODI's single-stage self-distillation

| Dimension | COCONUT | CODI |
|---|---|---|
| **Training stages** | Multi-stage curriculum (K = 4-7); each stage removes one more language reasoning step, replacing it with $c$ continuous thoughts | Single-stage joint training; no curriculum |
| **Supervision source** | Progressive removal of teacher CoT tokens; continuous thoughts are unsupervised (no per-step alignment loss) | L1 distance between teacher's (explicit-CoT) and student's (latent) hidden states at the pre-answer boundary |
| **Teacher-student coupling** | Same model at different stages; earlier-stage data interleaved at $p=0.3$ for anti-forgetting | Same model in the same gradient step, two parallel forward passes (teacher w/ CoT, student latent) |
| **Continuous-thought loss signal** | Via downstream language-token CE only — latent positions are *masked* | Direct hidden-state alignment via L1 loss at boundary |
| **Forward passes per step** | $n+1$ where $n$ = latent thoughts in current stage | 2 (teacher + student) |
| **Optimizer reset** | Yes, at stage transitions | N/A — no stage boundaries |
| **Anti-forgetting mechanism** | Uniform-probability ($p=0.3$) mixing of earlier-stage data | None needed — single stage |

These are not two hyperparameter variants of the same method. They instantiate **two distinct answers** to the question "how do you induce hidden-state-only reasoning from a model pre-trained on text?":

- **COCONUT's answer:** curriculum. Gradually withdraw text scaffolding; the model is forced to learn what it's about to lose. No explicit latent-state supervision — the signal propagates through downstream language CE.
- **CODI's answer:** self-distillation. Run the model twice, force the student's hidden state to match the teacher's hidden state at a single alignment point. No curriculum; one gradient step.

Either is fundamentally different from any pre-COCONUT recipe (which uses either pure explicit CoT or pure no-CoT, never the latent-feedback middle ground). Both descend from different slices of the precursor literature.

---

## Historical lineage — text tree

```
             1986 ┤ Rumelhart, Hinton, Williams — backprop; neural net as differentiable function
             2014 ┤ Graves — Neural Turing Machines: differentiable memory, controller iterations
             2016 ┤ Graves — Adaptive Computation Time (ACT) 1603.08983
                  │   first halting head; ponder cost regularizer; biased gradient
                  │
                  │ --- HALTING / DEPTH-ADAPTIVE LINE ---
             2018 ┤ Dehghani et al. — Universal Transformers 1807.03819
                  │   Transformer with ACT halting; depth-recurrent; shared block; Turing complete
                  ├ Chen, Rubanova, Bettencourt, Duvenaud — Neural ODEs 1806.07366 (NeurIPS Best)
                  │   continuous-depth, adjoint-sensitivity method, O(1) memory gradient
             2019 ┤ Bai, Kolter, Koltun — Deep Equilibrium Models 1909.01377
                  │   fixed-point z* = f(z*, x); implicit-function-theorem gradients; O(1) memory
             2021 ┤ Banino, Balaguer, Blundell — PonderNet 2107.05407
                  │   probabilistic (unbiased) reformulation of ACT; KL-to-geometric-prior
                  │
                  │ --- IMPLICIT COT / CONTENT-COMPRESSION LINE ---
        2022-2023 ┤ STaR (Zelikman) — rationale bootstrapping; filtered CoT fine-tune
             2023 ┤ Deng et al. — Implicit CoT via Knowledge Distillation 2311.01460
                  │   "vertical reasoning"; teacher + emulator + student; hidden-state distillation
                  │ Goyal et al. — Think Before You Speak / Pause Tokens 2310.02226
                  │   insert M learnable blanks; pause-PT + pause-FT; 1B scale
             2024 ┤ Zelikman et al. — Quiet-STaR 2403.09629
                  │   per-token rationales; <start-thought>/<end-thought> delimiters; REINFORCE
                  │ Pfau, Merrill, Bowman — Filler Tokens 2404.15758
                  │   meaningless fillers can replicate CoT on TC^0 tasks; theoretical grounding
                  │ Deng, Choi, Shieber — Stepwise Internalization 2405.14838
                  │   single-model curriculum; linear token-removal schedule; no continuous feedback
                  │
                  │ === CONVERGENCE: "feed the hidden state back" ===
             2024 ┤ Hao et al. — COCONUT 2412.06769 (Dec 2024)
                  │   Stepwise + Pause-delimiters + CONTINUOUS-THOUGHT FEEDBACK = new paradigm
             2025 ┤ Shen et al. — CODI 2502.21074
                  │   continuous-thought feedback + single-stage SELF-DISTILLATION (drops curriculum)
                  │ Liu et al. — LT-Tuning (Branch D primary)
                  │   adds Context-Prediction-Fusion (CPF) anchoring on top
                  │ Alibaba — KaVa
                  │   KV-cache distillation variant
                  │ Chen et al. — SIM-CoT
                  │   explicit auxiliary decoder for per-step latent supervision
             2025 ┤ --- DEPTH-RECURRENT LINE RESURFACES AT LLM SCALE ---
                  │ Wang et al. — HRM (Hierarchical Reasoning Model); PonderNet halting at LLM scale
                  │ Geiping — Huginn; Retrofitted Recurrence (k=8 truncated BPTT)
                  │ Zhu et al. — Ouro; fixed-width depth recurrence
                  │ Bae et al. — Mixture of Recursions; per-token dynamic iteration
                  │ Kim et al. — AdaPonderLM; PonderLM-3 (token-adaptive)
```

### Which modern method descends from which precursor

| Modern method | Direct precursor(s) | Contribution on top |
|---|---|---|
| COCONUT | Stepwise Internalization + Pause Tokens + (novel) hidden-state feedback | Continuous-thought feedback + anti-forgetting $p=0.3$ |
| CODI | Implicit CoT via KD + Quiet-STaR | Single-stage self-distillation; drops emulator; drops curriculum |
| LT-Tuning (CPF) | CODI + Quiet-STaR mixing head | Context-prediction-fusion gate; anchor latent to vocab |
| KaVa | Implicit CoT via KD | KV-cache compression as distillation target |
| SIM-CoT | Implicit CoT via KD + Quiet-STaR | Explicit auxiliary decoder at every latent step |
| HRM | PonderNet + Universal Transformers | Q-learning halt head at LLM scale |
| Ouro | Universal Transformers | Pretrain as shared-block loop from scratch |
| Huginn / Retrofitted Recurrence | Universal Transformers + truncated BPTT | 800B-token pretraining; retrofitting via curriculum |
| Mixture of Recursions | Universal Transformers + PonderNet | Per-token gated iteration |
| AdaPonderLM / PonderLM-3 | PonderNet | Direct LM adaptation of PonderNet |
| Adaptive Latent CoT Pretraining | Quiet-STaR + COCONUT | Continuous-thought during pretraining (still the only attempt) |
| ReGuLaR | COCONUT + Neural ODEs latent VAE | Rendered-CoT visual prior |

---

## Five key insights about the field's trajectory

### 1. The field has a **linear**, not branching, genealogy up to 2024

A striking observation: almost every 2016-2024 latent-reasoning precursor is the *sole known representative* of its design slot at its time. Graves-2016 was the only ACT; Dehghani-2018 was the only Transformer-era depth-recurrent paper for 3 years; DEQ-2019 was the only widely-cited fixed-point paper through 2023; Deng-2023 was the only hidden-state CoT distillation paper for a year. The 2024 explosion (Quiet-STaR, Filler Tokens, Stepwise Internalization, COCONUT, all within 13 months) is a phase transition — the field was tiny until suddenly it wasn't. For writeup framing: the 108-source vault (2024-2026) papers over a pre-2024 literature that's only ~10 papers deep per design slot. Most 2024-2026 methods are re-combining a *small* set of older moves.

### 2. COCONUT's single novelty is **hidden-state feedback** — everything else was in the field

COCONUT's staged curriculum came from Deng 2024 (Stepwise Internalization); its `<bot>`/`<eot>` delimiters came from Pause Tokens (Goyal 2023); its ACT-agnostic fixed-$c$ compute budget came from Filler Tokens (Pfau 2024) and Pause Tokens. The **only** genuinely new ingredient is that the removed CoT positions are replaced by the model's own previous hidden states (fed back as input embeddings) rather than by null fillers or teacher hidden states. This insight is elegant but fragile: once hidden-state feedback is the innovation, the design space below it (what hidden state? all layers? last layer? per position?) is vast and mostly unexplored.

### 3. The **halting/depth-adaptive** line has been re-discovered three times at LLM scale in 2025

Graves-2016 → Dehghani-2018 → Banino-2021 established the halting-head pattern. It sat dormant at LLM scale for ~4 years. Then three 2025 papers independently resurrect it: HRM (Q-learning halt), AdaPonderLM (Gumbel-softmax halt), Mixture of Recursions (routing-based halt). Plus Ouro (fixed-T without halting), Huginn / Retrofitted Recurrence. None of these groups cite each other as contemporaneous inspirations — the "apply shared block variable times" idea re-crystallizes. This is strong evidence the design is fundamental, but it also means the field is redoing PonderNet's homework at scale rather than learning from it. Our writeup can explicitly call this out.

### 4. **Continuous-depth gradients** (Neural ODEs 2018 / DEQ 2019) are available but nobody at LLM scale uses them

CODI's V2 detach is a *crude* approximation of DEQ's implicit-function-theorem gradient (detach cuts the chain; IFT *replaces* the chain with a closed-form gradient). Neural ODEs' adjoint sensitivity method gives O(1)-memory gradients through arbitrary-depth trajectories. TorchDEQ exists (2023) but no >1B LLM DEQ has been trained. If Branch B's detach ablation converges on "detach at step M works better than full BPTT," the next step is DEQ, not more detach variants. This is a plausible north-star arc that *no current paper has published*. Genuinely novel territory.

### 5. **Pretraining with latent thoughts** is the open problem COCONUT itself flags

COCONUT's conclusion explicitly names continuous-thought pretraining as future work. Quiet-STaR (March 2024) actually did it with discrete thoughts on Mistral-7B; [[Adaptive Latent CoT Pretraining]] (2025) is the only group to try continuous-thought pretraining. Goyal's Pause Tokens paper found that pause-PT is *load-bearing* — PauseFT alone doesn't work. This predicts CODI / LT-Tuning / KaVa (all fine-tuning-only) are leaving systematic gains on the table. If the north-star latent reasoner needs pretraining, the field is roughly nowhere.

---

## Under-explored precursor → under-explored modern direction

For each precursor, which contemporary design direction does it suggest that nobody is pursuing?

| Precursor | Ignored design direction |
|---|---|
| Neural ODEs | Adaptive-solver-based per-input latent compute; continuous-depth latent reasoning |
| Deep Equilibrium Models | IFT gradients replacing M-step BPTT at LLM scale |
| PonderNet | Unbiased-gradient halting head at LLM scale (HRM uses Q-learning, still biased) |
| Pause Tokens | **Continuous-thought pretraining** (not just FT) with width-expanding blanks |
| Quiet-STaR | **Per-token continuous** latent thoughts (all COCONUT-family are per-question) |
| Filler Tokens | Dense per-step supervision of latent states (all COCONUT-family are weakly supervised) |
| Deng 2023 (iCoT-KD) | Retraining the *emulator* to do the latent computation; nobody has done this after 2023 |
| Stepwise Internalization | Curriculum with **no hidden-state feedback** as a pure baseline (no 2024-2026 paper runs this isolated) |

---

## Which current methods look LESS novel given historical context (re-invented wheel candidates)

Ranking by how much of the method was published before 2024:

1. **[[Mixture of Recursions]]** — 80% Universal Transformers + 20% PonderNet + routing. The "apply the block T times, route which tokens get more iterations" is literally UT's per-position dynamic halting.
2. **[[Hierarchical Reasoning Model]]** — 70% PonderNet. Q-learning halting head replaces ACT's regularizer; two-level recurrent modules is ML-genre folklore back to LSTM-stacks. Fresh at LLM scale, not fresh as a design.
3. **[[AdaPonderLM]] / [[PonderLM-3]]** — ~90% PonderNet. Direct LM adaptation. Not reinvention — credited adaptation, but minimal novel design.
4. **[[Ouro]]** — 75% Universal Transformers. Pretrain-from-scratch as shared-block loop; novel scale, not novel design.
5. **[[Soft Thinking]]** / probabilistic superposition of tokens at inference — implicit in Graves 2016's ACT halt-weighted output averaging. The 2025 papers don't cite ACT-style averaging; this is reinvention.
6. **[[From Growing to Looping]]** — growing-via-depth-duplication then looping is the 2018-2019 UT result plus ResNet-style growing.
7. **[[Continuous CoT Parallel Exploration]]** — parallel beam in continuous space is a straightforward extension of COCONUT's BFS claim; theoretically implicit in Quiet-STaR's per-token parallel sampling.

Less reinvention (genuinely new territory):

- **[[CODI]]** — self-distillation specifically with L1 alignment at pre-answer token is a new move (Deng 2023 did emulator-to-student MSE at per-layer, per-token; CODI's single-point alignment + no emulator is fresh).
- **[[Latent Thoughts Tuning]]** (CPF) — anchoring via vocab-space context fusion is genuinely novel (Quiet-STaR's mixing head is token-probability mixing, not embedding fusion).
- **[[KaVa]]** — KV-cache distillation is a new supervision target; no precursor does this.
- **[[SIM-CoT]]** — explicit auxiliary decoder at every latent step is a new supervision structure.
- **[[Reasoning by Superposition]]** — formal framing of continuous thoughts as superposition over hypothesis space is new analysis.

---

## Open questions for Branch-D / writeup

1. Does CODI's single-stage self-distillation vs COCONUT's curriculum benchmark on the same metrics? (COCONUT paper compares to an iCoT (Deng 2023) variant but not CODI, which postdates.)
2. What does **Stepwise Internalization without continuous-thought feedback** score on GSM8k? This is the null model that nobody has isolated. If it's close to COCONUT, the COCONUT complexity is unjustified; if far, continuous-thought feedback is load-bearing — a clean story.
3. Does DEQ-style IFT gradient beat V2 detach on CODI? (Branch B pre-registered question.)
4. Per-token continuous thoughts + COCONUT-style feedback — unpublished.
5. Continuous-thought pretraining at 4B-8B scale — only [[Adaptive Latent CoT Pretraining]] has tried; results modest.

---

## Bibliography (source pages ingested for this synthesis)

Pre-2024 precursors (now in vault):

- [[Adaptive Computation Time]] (Graves 2016)
- [[Universal Transformers]] (Dehghani 2018)
- [[Neural ODEs]] (Chen 2018) ← new this session
- [[Deep Equilibrium Models]] (Bai 2019)
- [[PonderNet]] (Banino 2021)
- [[Implicit CoT via Knowledge Distillation]] (Deng 2023)
- [[Pause Tokens]] (Goyal 2023)
- [[Quiet-STaR]] (Zelikman 2024)
- [[Filler Tokens]] (Pfau 2024)
- [[Stepwise Internalization]] (Deng 2024)

Concept page that cross-links these: [[Implicit CoT Precursors]].

Modern reference points (already ingested):

- [[COCONUT]] (Hao 2024, Dec)
- [[CODI]] (Shen 2025)
- [[Latent Thoughts Tuning]] (Branch D primary)
- [[SIM-CoT]], [[KaVa]], [[HRM]], [[Ouro]], [[Retrofitted Recurrence]], [[Mixture of Recursions]], [[Adaptive Latent CoT Pretraining]]

**Total new pages filed this session:** 1 source ([[Neural ODEs]]), 3 entities ([[Ricky T.Q. Chen]], [[Eric Zelikman]], [[Jacob Pfau]]), 1 concept ([[Implicit CoT Precursors]]), 1 synthesis (this file), 1 plan ([[plans/WAVE_4_REVISED]]).
