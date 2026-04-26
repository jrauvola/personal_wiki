---
type: meta
title: "Branch D — LT-Tuning CPF on CODI"
project_slug: branch-d
updated: 2026-04-25
status: case-c-pivot
driver: "ORIGINAL: Implement Context-Prediction-Fusion from LT-Tuning on top of our CODI base. POST-CASE-C (2026-04-24): final-layer CPF FAILED at 4B; mid-layer CPF (W1.2 Phase 2) is the live remaining path. Wave-3 COCONUT becomes primary."
spec: "[[2026-04-17 Latent Reasoning Investigation Design]]"
related:
  - "[[Latent Thoughts Tuning]]"
  - "[[Context-Prediction-Fusion]]"
  - "[[Feature Collapse]]"
---

# Branch D — Reading List

## ⚠️ Case C verdict 2026-04-24 (post-LT-Tuning eval)

**Final-layer CPF FAILED at Qwen3-4B.** LT-Tuning training completed (train_loss=0.539, checkpoint pushed to `jrauvola/qwen3-4b-codi-lt-tuning-bf16-v2detach`) but F-battery eval gave Case C: GSM8k 1.67% (vs V2 baseline 12.06%); template SHIFTED from V2's `The/0/.` attractor to `isha:` / `) is:` attractor; loop rate 99% (vs V2 95%). See `research_findings/lt_tuning_phase0_case_decision.md` for full numbers + verdict.

**Critical: do NOT overgeneralize "CPF failed."** This Case C is for FINAL-LAYER CPF specifically. Branch 1 layer-asymmetric probe (`wiki/projects/spar-latent-reasoning/experiments/branch-1-layer-asymmetric-probe.md`) **CONFIRMED** mid-stack (L28-L30) preserves per-example variation while final layers collapse it. **Mid-layer CPF (W1.2 Phase 2) remains live and is the highest-priority remaining CODI extension.**

**Branch D status post-Case-C:**
- ⏸️ Final-layer CPF (LT-Tuning recipe as-published) — RETIRED.
- 🟢 Mid-layer CPF (W1.2 Phase 2 training) — LIVE; gated on per-layer dump infra (Branch 1 already produced).
- 🟢 W2.4b SIM-CoT Phase 2a (different mechanism, not invalidated by Case C) — queued.
- 🚀 W3.1 COCONUT — promoted to primary per spec §4.5.

## Empirical update 2026-04-23

The F1-F6 battery on the Phase-1 CODI-at-4B anchor (see `.raw/experiments/inert_latent_hypothesis_tests`) is the **largest empirical shift for this branch**. LT-Tuning's [[Context-Prediction-Fusion]] — fusing a vocab-anchored `e_pred` into each latent — was already the load-bearing anti-[[Feature Collapse]] mechanism for Branch D. The F-tests now show that the Phase-1 failure mode is precisely the pathology CPF is designed to break:

- **F3**: 7/8 latent positions decode to a fixed template `The → 0 → 0 → ? → . → . → . → .` (entropy <0.4 bits). Latents carry no per-step content — they are exactly the template-only latents that a vocabulary anchor is supposed to force into per-example content.
- **F5**: cross-example KV swap leaves accuracy unchanged (0.10→0.10, 13% text change at N=30). The decoder treats the latent region as a generic routing key, not a content channel.
- **F6**: σ=0.5 noise collapses accuracy to <3%. The narrow geometric basin is the template-routing key, not a reasoning trace.
- **Capability collapse**: CODI V2 bf16 0.16 vs Qwen3-4B-Instruct-2507 zero-shot 0.86 — a 70 pp gap for CPF to close.

**Reframed north-star rationale for Branch D.** This branch is now the clean test of whether vocab-anchored fusion can force latents to carry per-example content instead of operating as a format-prior template router. It is the most direct pathway toward the project's north-star "workable larger latent-reasoning model" synthesis of V2 / [[SIM-CoT]] / LT-Tuning lessons.

**Success criteria (F-test-derived).** A Branch-D LT-Tuning checkpoint is successful iff: F3 entropy rises on multiple positions (not just step 3); F5 swap becomes non-null with measurable accuracy drop under foreign-example latents; F6 σ=0.5 tolerance shifts upward (template basin widens or disappears); parsed-accuracy recovers toward the zero-shot 0.86 floor, closing at minimum the F4 ablation gap (25-29%) with a margin that shows content was actually injected.

**Status.** LT-Tuning CPF training is in-flight at Qwen3-4B on the GH200 (epoch 0.78 at time of writing, 2026-04-24 scratchpad entry). Co-running with the [[SIM-CoT]] shared-head smoke has held within memory budget.

## Empirical update 2026-04-24

LT-Tuning post-training eval battery is pre-wired, awaiting checkpoint release. Runbook: `latent_eval_training_harness/scripts/lt_tuning_runbook.md`; two eval configs + launcher staged. F-test helpers (F4 latent-KV ablate, F5 cross-example KV swap, F6 Gaussian noise, F1-F3 inert-latent diagnostics) live on branches `f4-latent-ablate`, `f5-kv-swap`, `f6-kv-perturb`, `f-tests-inert-latent` (SHAs in runbook); merge required before launch. Stacked Track A × F4 floor of 8.5% (`research_findings/f4_per_example_diagnosis.md`) pins the Phase-2 "beats-substrate" threshold at ~15% GSM8k. See `research_findings/experiment_scratchpad.md` for live status.

## Empirical update 2026-04-24 (Branch 1 CONFIRM)

Branch 1's layer-asymmetric probe (`research_findings/layer_probe/v2_bf16_step3/layer_asymmetric_probe_v2_bf16.md`, 500 GSM8k × 37 layers, V2 bf16 Qwen3-4B step 3) **CONFIRMS** middle-layer CPF as a V3 design candidate. Per-layer geometric dispersion is U-shaped: median pair cos 0.966 at L28 (mid-stack trough) vs 0.989 at L36 (final, F3 baseline); top-1 PC variance 0.137 at L30 vs 0.310 at L36 (final uses 2.27× as much variance on a single direction); 95%-PC count 213 at L22 vs 82 at L36 (final lives in ~40% as many intrinsic dims). The last 5 layers re-collapse sharply (L31→L36). Open-question 2 ("layer index I") now has a concrete candidate: **`I ≈ 28-30`**, anchored *before* the re-collapse. This is the first directly actionable V3 design element from the Branch 1 probe and reframes the LT-Tuning paper's default-final-layer choice as scale/architecture-dependent. See [[Context-Prediction-Fusion]] § Middle-layer anchoring candidate. Logit-lens-per-layer entropy is the designated follow-up (Qwen3-4B shard 1/3 not locally cached).

Auto-generated by `wiki-autoreview` sweep #2, 2026-04-23. Vault has 86 sources after round-2 deep crawls.

## Primary sources (15)

| Source | Why | Status |
|---|---|---|
| [[Latent Thoughts Tuning]] | CPF equation + 3-stage curriculum is the exact recipe Branch D implements | read |
| [[CODI]] | Base implementation — CPF is being implemented on top of CODI | read |
| [[SIM-CoT]] | Auxiliary-decoder anti-collapse directly complements CPF | read |
| [[KaVa]] | Direct alternative fusion/anti-collapse via per-step KV targets | read |
| [[HRPO]] | Learnable-gated fusion g·h + (1−g)·e — structurally identical CPF form, independent discovery | read |
| [[Soft Thinking]] | Identifies decoupled-embedding mismatch at >7B — corroborates Branch D core hypothesis | read |
| [[Latent-SFT]] | Latent-Vocab constraint is functionally equivalent to CPF vocabulary anchor | read |
| [[Stochastic Soft Thinking]] | Greedy Pitfall is the mechanistic justification for CPF | read |
| [[Weak vs Strong Supervision Study]] | Frames the LT-Tuning (strong, CPF) vs COCONUT (weak) axis; validates Stage 3 CPF as shortcut-suppression | read |
| [[Capabilities and Limits of Latent CoT]] | Proves curriculum learning is theoretically necessary — validates LT-Tuning's 3-stage | read |
| [[Dynamics of Latent CoT]] | First causal study of CODI; early-output-bias / late-representational-commitment gap is the diagnostic CPF should close | read |
| [[Are LRMs Easily Interpretable]] | CODI latents 65-71% decodable with operand context — feature collapse real but surmountable | read |
| [[PCCoT]] | Jacobi parallel updates directly compatible with CODI + CPF | read |
| [[SemCoT]] | Contrastive sentence transformer as semantic-preservation loss | read |
| [[Multiplex Thinking]] | K-sample sparse CPF (top-K sampled vocab, weighted sum into embedding) — direct comparator to LT-Tuning CPF form; code + checkpoints released | read |

## Secondary sources (36)

| Source | Why | Status |
|---|---|---|
| [[AdaPonderLM]] | Halting gate has structural similarity to HRPO's learnable gate | read |
| [[Adaptive Latent RL]] | Post-training add-on layering on CPF+CODI | read |
| [[ALiCoT]] | Order-r decay theorem gives theoretical scaffolding for CPF (downgraded primary→secondary this sweep: no code, abstract-only) | read |
| [[COCONUT]] | Anti-collapse contrast: drops from 50.3% → 41.5% at 8B | read |
| [[CoLaR]] | Compression-first, orthogonal axis | read |
| [[CoLT]] | Tool-call latent paradigm — inverts SIM-CoT's training-only decoder into inference-time unpacker | read |
| [[Continuous CoT Parallel Exploration]] | CSFT's convex-combo-of-vocab target is structurally identical to CPF | read |
| [[DART]] | Self-distillation with REM — fusion-style alternative | read |
| [[Depth-Recurrent Attention Mixtures]] | Depth attention as alternative cross-iteration information flow | read |
| [[Efficient Post-Training Refinement]] | Residual-refinement anti-collapse without curriculum | read |
| [[Encode Think Decode]] | E/T/D partition ≡ Prelude/Core/Coda — informs CPF placement (downgraded primary→secondary this sweep: not CPF-family recipe) | read |
| [[GTS]] | Post-hoc ITS module; composes with CPF at inference | read |
| [[Latent Thinking Optimization]] | Reward-anchor framing parallel to CPF vocab-anchor (downgraded primary→secondary this sweep: Huginn-specific) | read |
| [[Latent Tokens]] | Periodic latent-token insertion as alternative anchoring | read |
| [[LEPO]] | RL-on-latent complements post-SFT | read |
| [[Loop Think Generalize]] | Compositional-generalization test bed (downgraded primary→secondary this sweep: probe-bed rather than recipe) | read |
| [[LoopFormer]] | Shortcut modulation has iteration-conditional anchor similar to CPF | read |
| [[LSTR]] | Sparse-structure add-on compatible with CPF | read |
| [[MARCOS]] | Variational latent-chain alternative to CPF fusion | read |
| [[Mixture of Recursions]] | Token-level routing is alternative to CPF per-step anchor | read |
| [[Mull-Tokens]] | Three-stage curriculum + dual supervision (text LM-head + image encoder) — multimodal curriculum analog to LT-Tuning | read |
| [[One Step Forward K Steps Back]] | Trajectory anchor as third anti-collapse axis (downgraded primary→secondary this sweep: diffusion paradigm + no code) | read |
| [[OneVL]] | Dual auxiliary decoders (language + world-model) | read |
| [[Parallel TTS Latent]] | Inference-time parallel scaling | read |
| [[Retrofitted Recurrence]] | Alternative retrofit path: pure depth recurrence + curriculum, no CPF | read |
| [[Scaling Up TTC]] | No CPF-style anchoring; stochastic s_0 + path-independence as anti-collapse alternative | read |
| [[SeLaR]] | Entropy-aware contrastive pushes away from dominant token; training-free (downgraded primary→secondary this sweep: inference-time only) | read |
| [[Skip a Layer or Loop it]] | CoLa argues for lightweight trained refinement (CPF) rather than full conversion | read |
| [[Soft Tokens Hard Truths]] | Alternative training signal (RL, no distillation) at 8B | read |
| [[SoftCoT Plus Plus]] | Contrastive objective for latent diversity | read |
| [[SwiReasoning]] | Hybrid latent/explicit switching — could wrap a CPF-trained model | read |
| [[SynAdapt]] | Synthetic CCoT target as alternative alignment | read |
| [[System-1.5 Reasoning]] | Two-stage self-distillation comparable to LT-Tuning's 3-stage | read |
| [[Think-at-Hard]] | Token-level adaptive-depth + LoRA as minimum-intervention alternative | read |
| [[ThinkRouter]] | Soft-embedding noise diagnosis motivates CPF's vocab anchor | read |
| [[Token Assorted]] | Randomized-m single-stage training challenges curriculum necessity for discrete latents | read |

## Reference sources (33)

| Source | Why |
|---|---|
| [[Adaptive Latent CoT Pretraining]] | Pretraining-time axis |
| [[Adaptive Loops and Memory]] | Memory orthogonal to fusion |
| [[Beyond Semantics Reasonless Tokens]] | Faithfulness-adjacent |
| [[Continuous CoT Multilingual]] | CODI generalization |
| [[Decoding Depth-Recurrent Transformer]] | Probe critique |
| [[DualCoT-VLA]] | VLA domain extension |
| [[Formal CoT vs Latent]] | Theoretical separation |
| [[From Growing to Looping]] | Grow ≡ loop equivalence |
| [[Hierarchical Reasoning Model]] | No fusion/anchor recipe |
| [[Implicit Reasoning Survey]] | Taxonomy |
| [[Inner Loop Inference]] | Train-free recurrence; no anchoring |
| [[JEPA-Reasoner]] | Decoupled-architecture paradigm |
| [[LaDi-RL]] | Latent-diffusion RL |
| [[LaDiR]] | Diffusion paradigm |
| [[LaRA-VLA]] | VLA domain |
| [[LaSER]] | IR-specific |
| [[Latent CoT Survey]] | Taxonomy |
| [[Latent Exploration Decoding]] | Decoding-time intervention |
| [[LatentChem]] | Chemistry domain; no-curriculum counterpoint |
| [[LEAD]] | Multimodal entropy-gated decoding |
| [[Mechanistic Analysis of Looped Reasoning LMs]] | Recurrence mech-interp |
| [[OneLatent]] | Extreme single-token compression |
| [[Opaque Serial Depth]] | Complexity bounds |
| [[Ouro]] | Fixed-width depth recurrence |
| [[Parcae]] | Looped-LM scaling laws |
| [[PonderLM-3]] | Differentiable halting |
| [[Reasoning by Superposition]] | Theoretical anti-collapse |
| [[ReGuLaR]] | Multimodal VAE |
| [[RLTT]] | Trajectory credit; future-work pointer |
| [[Stability and Generalization in Looped Transformers]] | Theory |
| [[Step-Decomposed Influence]] | Attribution |
| [[Survey on Latent Reasoning]] | 34-author taxonomy |
| [[Visual Enhanced Depth Scaling]] | Multimodal gradient dynamics |

## Key concepts

- [[Context-Prediction-Fusion]] — the mechanism itself
- [[Dynamic Switching Protocol]] — LT-Tuning's adaptive-compute layer (Stage 2)
- [[Feature Collapse]] — the failure mode CPF addresses (now with layer-asymmetric refinement)
- [[Curriculum Distillation]] — multi-stage training pattern
- [[Shortcut Behavior]] — target of strong-supervision anti-collapse
- [[Gumbel-Softmax Latent]] — alternative anti-collapse mechanism to CPF

## Notable round-2 additions (sweep #2)

- **CPF-family convergence reaches 5 independent groups.** With round-2 Multiplex Thinking (PKU / Microsoft lineage) now in vault as a K-sample sparse CPF variant, the CPF-equivalent fusion form has been independently derived by LT-Tuning, HRPO, Latent-SFT, Soft Thinking, and Multiplex Thinking. Five groups converge on the same `weighted-sum-of-embeddings + context` mechanism — strong evidence for a fundamental inductive bias.
- **Contradiction cluster on curriculum/alignment necessity grows to 4-way.** Theorem 1 (Capabilities and Limits) + ALiCoT Order-r decay theorem (new) vs Soft Tokens Hard Truths + Token Assorted. Two independent theoretical necessity results vs two independent empirical no-curriculum-needed results. Resolution plausibly: theoretical claims apply to continuous distillation-based regimes; RL and discrete-codebook latents escape.

## Open questions for implementation

1. **α schedule:** fixed, learned, or annealed? HRPO says learnable; LT-Tuning uses scheduled; Multiplex Thinking has self-adaptive K (collapses when confident, expands when uncertain) — a third option.
2. **Layer index I:** which layer to extract `h_{t-1, I}` from?
3. **Stage ordering on a pre-trained CODI:** skip Stage 1 or restart?
4. **Embedding tying interaction:** Qwen3 `tie_word_embeddings = false`; Gemma-3 ties. Does CPF behavior differ on tied-embedding architectures?
5. **Composition with existing V2 KV/latent detach:** does CPF obsolete or compose?
6. **Learnable vs fixed α:** HRPO uses learnable context-dependent gate — better than LT-Tuning's fixed/scheduled?
7. **CPF + Gumbel stochasticity:** does adding Gumbel noise (Latent-SFT, LEPO) on top improve or destabilize?
8. **New:** Does K-sample (Multiplex) outperform full-vocab softmax (LT-Tuning CPF) for `e_pred`? Cheap ablation.

## Integration targets

- Harness: `latent_eval_training_harness/` (CODI reimplementation)
- External repo to reference: [[NeosKnight233 Latent-Thoughts-Tuning]]
- Blocks: requires Branch A (stable CODI base) to be green first.
