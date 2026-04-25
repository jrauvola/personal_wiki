---
type: meta
title: "SPAR Latent Reasoning — State of Project, 2026-04-23"
updated: 2026-04-24
status: snapshot
---

# State of Project — 2026-04-23

## Headline

Phase 1 (CODI V2 eval + interpretability) has resolved into a crisp negative result: on Qwen3-4B-Instruct-2507, CODI training *collapses* ~70 percentage points of base-model capability (zero-shot GSM8k 0.86 → V2 bf16 0.16) and the F1-F6 test battery shows the remaining latents act as a *geometric key for template routing*, not as a vehicle for iterative reasoning. The rising `num_latent` accuracy curve that motivated the Phase 1 writeup is a loop-lucky-match artifact, visible once first-sentence-trim regrading is applied. Phase 2 is now in flight as the clean test: an [[Latent Thoughts Tuning]] / [[Context-Prediction-Fusion]] run on the same base model is training on the GH200, and a [[SIM-CoT]] auxiliary-decoder arm is OOM-blocked but has a shared-lm_head fallback smoked successfully. The north-star — a workable larger latent reasoning model synthesizing V2 / SIM-CoT / LT-Tuning lessons — depends on Phase 2 breaking the template-routing mode before any scaling run is attempted.

## Phase 1 — established facts

- **Capability collapse:** zero-shot Qwen3-4B-Instruct-2507 = 0.86 on GSM8k, V2 bf16 at `num_latent=8` = 0.163; V2' fp32 ≈ same neighborhood. CODI training destroys ~70 pp of GSM8k capability (`research_findings/lightweight_experiments_E1_E4.md`, `research_findings/prediction_degeneracy_analysis.md`).
- **Rising num_latent curve is loop-lucky-match:** Track A first-sentence-trim regrade flattens the num_latent=0/2/4/8 sweep — the "CODI scales with latent count" Phase 1 signal vanishes once predictions are trimmed at the first period (`research_findings/track_a_posthoc_first_sentence_regrade.md`). An instance of [[Shortcut Behavior]].
- **Per-bench accuracy (V2 bf16 / V2' fp32, `num_latent=8`):** GSM8k 0.163 / ~0.163; SVAMP 0.423 / 0.423; gsm-hard ≈ 0.05-0.07. P0 (no detach) is worst; V3'/V4 variants similar order of magnitude to V2.
- **E1-E4 framing:** CODI learns answer-format priors (1-leading at 45-71% vs 18-29% chance) and destroys 60.8% of GSM8k problems that the base model solves zero-shot.

## F1-F6 battery — inert-latent hypothesis status

Primary source: `research_findings/inert_latent_hypothesis_tests.md`. Companion: `research_findings/f1_f2_f3_inert_latent_tests.md`.

- **F1 unique-correct.** Across GSM8k / gsm-hard / SVAMP, only 10 / 28 / 6 problems are V2-correct AND zero-shot-wrong (2.8% of V2-correct). The V2-unique set is dominated by lucky format-prior matches on easy or large-target problems — CODI adds essentially no unique reasoning capability.
- **F2 loop content.** ~12% of looped substrings contain any digit from the question. Loops are context-free format-prior emission.
- **F3 trace variance.** 7 of 8 latent positions decode to a fixed template under logit lens (`The → 0 → 0 → ? → . → . → . → .`, <0.4 bits entropy); only step 3 shows 1.5 bits of cross-example variation, and that is a three-way digit branch.
- **F4 latent-KV ablate.** Cropping latent KV before answer generation drops GSM8k 0.163 → 0.122 (-25%) and SVAMP 0.423 → 0.300 (-29%). Loop rate stays ~100%. Latents contribute a weak non-zero prior; most accuracy survives ablation.
- **F5 cross-example KV swap.** N=30 pairs: B's accuracy 0.100 → 0.100 under A-latent injection; 13% of predictions change text. Proxy at N=200: median pairwise cosine 0.78, 63 PCs for 95% variance — latent KVs carry per-example content, but that content is downstream-invisible.
- **F6 Gaussian noise.** σ=0.1 absorbed; σ=0.5 collapses accuracy to 0.005-0.025 on both GSM8k and SVAMP; σ=1.0 stays collapsed. Narrow geometric basin required for template routing.

**Synthesis.** The strict "latents are fully inert" hypothesis is refuted (F4 -25-29%, F5 proxy non-zero per-example variation). The weaker "inert for reasoning, structurally necessary for routing" form holds: latents act as a geometric key that lets the decoder's attention lock into its `"The answer is: ..."` format-prior attractor. The specific per-example content is downstream-invisible (F5), the token-level decoded form is a fixed template (F3), but the key's existence in a narrow geometric basin is required (F6). Rising `num_latent` → stronger routing lock, not iterative computation. This is a concrete instantiation of [[Feature Collapse]] expressed as template-key routing.

## What the evidence implies for the north-star

- **Template-routing is the failure mode to avoid in any V3.** Any training recipe that leaves latents as a generic "prefix with the right geometry" will reproduce this mode at 4B — and likely worse at larger scale, where the base model's own format-prior is even stronger.
- **[[Context-Prediction-Fusion]] (LT-Tuning and the 5-way CPF convergence)** forces latents to participate in the vocab-embedding blend rather than act as a free-form prefix, hypothesized to defeat the template-key mode. ([[Latent Thoughts Tuning]])
- **[[SIM-CoT]] auxiliary decoder** supervises each latent step to decode a specific reasoning token, forcing step-identifiable content and breaking F3's template-only decoding.
- **Hybrid latent/discrete** ([[HRPO]], [[ThinkRouter]], [[SwiReasoning]]) side-steps the template lock by letting the model emit explicit tokens when the latent channel isn't informative.
- **A scaling run is premature** until Phase 2 shows one of these interventions breaks the template lock on the 4B base. Scaling a model whose latents are a geometric routing key just amplifies the routing, not the reasoning.

## Phase 2 status

- **LT-Tuning CPF on Qwen3-4B-Instruct-2507:** training started ~2026-04-23 17:30 UTC on the GH200 in a persistent tmux session. Expected finish ~2026-04-24 11:30 UTC. Auto-upload watcher configured to push the final checkpoint to `jrauvola/qwen3-4b-codi-lt-tuning-bf16-v2detach` on HF. In flight at time of writing; verify run status before trusting this as current.
- **SIM-CoT full-LM aux decoder:** OOM-blocked on the GH200 when the full aux decoder is trained alongside the base model. Shared-lm_head fallback smoke (bs=1/ga=1, 10 steps) completed successfully at 22.5 GB (`configs/training/qwen3_4b_codi_gh200_sim_cot_shared_head_smoke.yaml`). Plan: wait for LT-Tuning to release GPU, then try full-LM variant on an idle GPU; fall back to shared-head if that also OOMs.
- **Expected next decisions after LT-Tuning returns.** (1) Run F3/F4/F5/F6 on the LT-Tuning checkpoint to test whether CPF breaks the template-key pattern. (2) Launch full-LM SIM-CoT on the idle GPU. (3) If LT-Tuning GSM8k > 30%, that is the first checkpoint where the F-battery becomes a meaningful generalization test rather than a V2-specific characterization.

## Open scientific questions

- Does Phase 2 LT-Tuning CPF break F3's 7/8-templated pattern — i.e. do the non-step-3 latent positions show >0.4 bits of entropy?
- Does Phase 2 cross-example KV swap (F5) produce a meaningful accuracy delta, or does the CPF-trained model also treat latent KV as example-agnostic?
- Is the narrow geometric basin (F6) universal at 4B, or specific to Qwen3-4B-Instruct-2507's format-prior shape?
- Does [[SIM-CoT]]'s aux-decoder loss force step-identifiable content strongly enough to defeat the template-key attractor, or does the base model's format prior dominate regardless?
- On the north-star model, is the rising `num_latent` curve a real computational signal (passes first-sentence-trim regrade) or a dressed-up routing lock?
- Does the template-routing mode manifest at 8B/9B or does stronger base-model capability overwhelm it?
- Can a coherent V3 compose V2 detach + SIM-CoT aux + LT-Tuning CPF, or do the three mechanisms overlap / interfere?
- Is F1 "no unique reasoning capability beyond base" a universal property of post-hoc latent scaffolding, or a CODI-specific collapse artifact?

## Open infrastructure questions

- Aux-decoder memory budget on GH200: full-LM SIM-CoT OOMs when co-running with LT-Tuning; what's the clean single-GPU budget for full-LM at bs=2/ga=4?
- Dataset variant for Phase 2: GSM8k-aug vs GSM8k-base-only vs mixed — which best isolates the template-break signal without introducing base-capability confounds?
- HF upload automation: the auto-upload watcher for LT-Tuning is new; needs a post-Phase-2 audit that the watcher handles both clean-finish and crash-resume cases for SIM-CoT and future runs.

## Links

- Research findings index: `research_findings/inert_latent_hypothesis_tests.md`, `research_findings/f1_f2_f3_inert_latent_tests.md`, `research_findings/lightweight_experiments_E1_E4.md`, `research_findings/track_a_posthoc_first_sentence_regrade.md`, `research_findings/kv_pca_analysis.md`, `research_findings/prediction_degeneracy_analysis.md`, `research_findings/experiment_scratchpad.md`.
- Branch docs: [[branch-a]] (Qwen3 scaling), [[branch-b]] (detach ablation), [[branch-c]] (convergence contradiction), [[branch-d]] (LT-Tuning CPF on CODI).
- Umbrella: [[spar-latent-reasoning]].
- Concepts: [[Feature Collapse]], [[Context-Prediction-Fusion]], [[Shortcut Behavior]], [[Exploration-Execution Trade-off]], [[KV-Cache Distillation]], [[Curriculum Distillation]], [[Self-Distillation]], [[Manipulation vs Capacity]].
- Sources (north-star inputs): [[CODI]], [[SIM-CoT]], [[Latent Thoughts Tuning]], [[HRPO]], [[Latent-SFT]], [[Soft Thinking]], [[Multiplex Thinking]].

## Addendum 2026-04-24

Seven findings accumulated since the 2026-04-23 snapshot; propagated to the wiki this sync.

- **F4 per-example diagnosis** (`research_findings/f4_per_example_diagnosis.md`). Joined baseline (n=215 correct) + F4-ablate (n=161 correct) on all 1319 GSM8k ids. Sets: preserved=127, lost=88, gained=34. The lost-88 population has the highest target-in-loop fraction (94.3%) and longest mean loop substring — but 76/88 (86%) are still Track-A-trim-correct. F4 and Track A therefore expose *different* failure layers, not the same one. Stacking gives "both-survive" floor = 112/1319 = **8.5%**, below F4's 12.2% and Track A's 10.8%. Refutes the "F4 = real floor" hypothesis; sharpens the real capability-floor estimate. Implication: Phase 2 must clear ~15% on GSM8k to beat the template-routing substrate.

- **SIM-CoT shared-head smoke** (2026-04-24 scratchpad). Full-LM SIM-CoT (`aux_decoder_full_lm: true`) OOM at step 1 on GH200. Shared-`lm_head` fallback smoke (bs=1/ga=1/10 steps, co-running with LT-Tuning's ~38 GB) completes 10/10 in 48 s at **22.5 GB** peak. Not safe to co-run with LT-Tuning at bs=2/ga=4. Go-path: wait for LT-Tuning checkpoint, try full-LM first on idle GPU, fall back to shared-head.

- **KV PCA analysis** (`research_findings/kv_pca_analysis.md`). 200 examples × 3 benchmarks × 3 num_latent × 2 variants. V2 bf16 within-variant RMS radius 70.8-72.8 vs V2' fp32 76.7-79.6 — bf16 basin **9-10% tighter** across all benchmarks. Centroid cosine 0.94-0.96 and centroid distance ~40-48 vs within-radius ~70-80 → the two variants occupy *distinct sub-basins of the same manifold*, not the same point. Positions 0-1 carry more cross-example variation than 2-7 (consistent with F3). Top 10 PCs ≈ 67-72% variance in 2048-d — heavy low-rank structure. Reconciles Christopher's ±10-12% 1B KV-steering effect with our F5 null at 4B: Christopher perturbs out-of-basin, F5 stays in-basin.

- **F3 layer-wise deferred** (`research_findings/f3_layerwise_step3.md`). Deferred; local data insufficient (final-layer-only traces, 200-example KV dumps, no `embed_tokens`/tied `lm_head` shards locally). Final-layer anchor re-verified across 1319 examples: step 3 entropy **1.493 bits**, top-1 `0` at 54.3%, top-5 `0/1/./2/=`. GPU re-dump spec: one-line patch to `latent_tap.py` saving `hidden_states[l][:, -1:, :]` for all 36 layers, ~361 MB fp16, <10% eval wall-clock overhead.

- **LT-Tuning eval battery pre-wire** (`latent_eval_training_harness/scripts/lt_tuning_runbook.md`). Two eval configs + launcher staged. F-test helpers live on branches `f4-latent-ablate`, `f5-kv-swap`, `f6-kv-perturb`, `f-tests-inert-latent` (SHAs in runbook). Merge required before post-LT-Tuning F-battery launch.

- **Track A × F4 stacking synthesis.** Real capability floor = 8.5% on GSM8k (stacked F4 ∩ Track A), not 12.2% (F4 alone) or 10.8% (Track A alone). Phase 2 "beats the substrate" threshold now pinned at ~15%.

- **Scale-sensitivity decision.** Agreed NOT to scale the model down for iteration speed; data subsample + 200-example preliminary eval subsets are the faster path. Template-routing is scale-sensitive (Christopher ±10-12% at 1B vs our null at 4B), so shrinking the base model would invalidate the pathology we're trying to break.

Still-pending (not yet wiki-landed): Branch 1 / Branch 2 probes running; LT-Tuning CPF training in flight.

- **Branch 1 layer-asymmetric probe — CONFIRM** (`research_findings/layer_probe/v2_bf16_step3/layer_asymmetric_probe_v2_bf16.md`, 500 GSM8k × 37 layers, V2 bf16 step 3, late-day add). F3's template-lock is a **final-layer readout artifact**, not stack-wide. Per-layer geometric dispersion traces a U: rises from embed through mid-stack peak L22-L30 (median pair cos 0.966 at L28, top-1 PC variance 0.137 at L30, 95%-PC count 213 at L22), then re-collapses across L31-L36 (final L36: pair cos 0.989, top-1 PC 0.310 — 2.27× the trough; 95%-PC count 82 — 38% of mid-stack peak). Mid-stack preserves per-example content; the last 6 layers compress it into the decoder-facing routing template. Mechanistic explanation for F5's swap-null. **V3 implication:** middle-layer [[Context-Prediction-Fusion]] is on the table — anchor target `h_{t-1, L≈28-30}` instead of final-layer hidden, placed *before* the L31→L36 re-collapse. Logit-lens-per-layer deferred (Qwen3-4B shard 1/3 not locally cached). Resolves the F3 layer-wise deferred item.
