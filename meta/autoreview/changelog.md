---
type: meta
title: "Autoreview Changelog"
updated: 2026-04-23
---

# Autoreview Changelog

Append-only log of `wiki-autoreview` sweeps. New entries at top.

---

## [2026-04-23] autoreview sweep #2

**Context:** Second live autoreview. Vault has grown 49 → 86 sources after 4 round-2 deep crawls (Scaling Up TTC / HRPO / SIM-CoT / Stochastic Soft Thinking) added 37 new source pages graded by 4 different subagents. Tier-drift risk is real again, especially on primary-heavy assignments from the round-2 subagents.

**Sources reviewed:** 86
**Tier changes:** 12 source-project cells (all primary → secondary)
**Contradictions flagged:** 2 new + 1 merged/extended + 2 framing/refinement notes (3 prior contradictions preserved; ALiCoT theorem extended the curriculum-necessity cluster from 3-way to 4-way)
**Archived:** 0 orphans, 0 stale (none eligible — all 86 sources have ≥1 inbound link and all have `projects:` entries; ≤1 day old pages are never stale)
**Dashboards regenerated:** branch-a, branch-b, branch-c, branch-d, spar-latent-reasoning (all 5)

### Notable tier shifts (all primary → secondary)

All changes were conservative downgrades to keep primary lists signal-dense; no upgrades this sweep.

- [[OneVL]] — spar-latent-reasoning: primary → secondary. Claim of "first latent CoT to surpass explicit CoT" is domain-specific (autonomous driving); [[MARCOS]] has priority on GSM8K. Dual-decoder recipe is a notable SIM-CoT extension but not a north-star synthesis input.
- [[ALiCoT]] — branch-d: primary → secondary. Theorem-only paper, no code, abstract-only; Order-r decay result is framing support rather than a Branch D recipe input.
- [[Stability and Generalization in Looped Transformers]] — branch-b: primary → secondary; spar-latent-reasoning: primary → secondary. Abstract-only paper; theoretical framework is useful for reframing detach ablations but Parcae + Formal-CoT-vs-Latent + Reasoning-by-Superposition already cover the theory axis.
- [[Encode Think Decode]] — branch-d: primary → secondary. E/T/D partition is retrofit methodology; not a CPF-family recipe on the Branch D implementation path.
- [[Loop Think Generalize]] — branch-d: primary → secondary. Compositional-generalization test bed, not a recipe; also studies recurrent-depth models (Huginn/Ouro), not CODI sequence-growing family.
- [[Latent Thinking Optimization]] — branch-a: primary → secondary; branch-d: primary → secondary. Inference-time LTO specific to Huginn-3.5B; not a Qwen3 scaling recipe and not on the Branch D CPF-on-CODI path.
- [[SeLaR]] — branch-d: primary → secondary. Training-free inference mechanism; not trainable on the Branch D path, useful as convergent evidence rather than direct comparator.
- [[LoopFormer]] — branch-a: primary → secondary; spar-latent-reasoning: primary → secondary. No released code or weights; architectural variant rather than implementation input.
- [[Mixture of Recursions]] — branch-b: primary → secondary. No released code; recursion-wise KV caching is a related design axis but not a direct detach/fp32 ablation input.
- [[One Step Forward K Steps Back]] — branch-d: primary → secondary; spar-latent-reasoning: primary → secondary. Diffusion-style paradigm from CODI sequence-growing; no code; conceptual bridge rather than synthesis input.

Total: 12 source-project tier cells, across 10 distinct sources.

### New contradictions (requires attention)

1. **[[OneVL]] "first latent-CoT to surpass explicit CoT" vs [[MARCOS]] priority.** Both claim the milestone. Not strictly contradictory (different domains: driving vs GSM8K), but both pages now carry `[!contradiction]` callouts to note that MARCOS has priority on GSM8K (Sep 2025) and OneVL's "first" claim should be scoped to its driving domain (Apr 2026).

2. **[[ThinkRouter]] confidence-correlates-with-wrongness vs [[Weak vs Strong Supervision Study]] + [[Stochastic Soft Thinking]] shortcut framing.** Not strictly contradictory, but different causal stories for the same empirical domain (latent-reasoning failure). ThinkRouter: noise aggregation in low-confidence soft embeddings leads to false high downstream confidence. Weak/Strong Supervision + SST: latents are often bypassed entirely (shortcut). Both mechanisms exist; compatible but worth distinguishing. Callout added on ThinkRouter; note added on Weak vs Strong Supervision.

### Extended contradictions (prior clusters grew)

3. **Curriculum/alignment necessity cluster grew from 3-way to 4-way.** [[ALiCoT]]'s Order-r decay theorem (round-2 crawl) joins [[Capabilities and Limits of Latent CoT]] as a second independent theoretical-necessity result for explicit-alignment training. Both still contested by [[Soft Tokens Hard Truths]] (RL-only, 8B, no curriculum, matches discrete CoT) and [[Token Assorted]] (randomized-m single-stage beats multi-stage curriculum for discrete latents). Callouts updated on all 4 papers to reference the 4-way cluster. Plausible resolution: theorems apply to continuous-latent distillation regimes; RL and discrete-codebook latents escape — but not established.

### New framing / refinement notes (not strict contradictions but worth tracking)

4. **[[Latent Exploration Decoding]] layer-asymmetric entropy collapse refines [[Feature Collapse]].** Our prior Feature Collapse framing treated collapse as aggregate across the latent trajectory. LED shows it's layer-asymmetric — final layer collapses, intermediate layers preserve entropy. This is why decoding-time interventions (LED, [[SeLaR]], [[ThinkRouter]]) can recover diversity without retraining. [[Latent Thinking Optimization]] gives a parallel finding on Huginn: process-reward information is invisible to logit-lens but visible to a reward classifier. Same layer/readout asymmetry. Feature Collapse concept page updated to reflect this.

5. **Iteration-sampling design space (Huginn Poisson-Lognormal vs Ouro uniform+exit vs LoopFormer shortcut modulation).** Not contradictory but distinct design points in "make a shared recurrent block produce meaningful outputs across iteration counts." Paired with BPTT truncation choices (full vs k=8), this defines a 3×2 matrix of retrofit options Branch A should explicitly consider. Note added on [[Scaling Up TTC]].

### Preserved contradictions (unchanged this sweep)

- [[Are LRMs Easily Interpretable]] vs [[Weak vs Strong Supervision Study]] on CODI latent utilization.
- [[Capabilities and Limits of Latent CoT]] vs [[Soft Tokens Hard Truths]] — now part of the 4-way cluster above.
- [[Capabilities and Limits of Latent CoT]] vs [[Token Assorted]] — now part of the 4-way cluster above.

### Dropped contradictions (auto-resolved)

None this sweep.

### Audit of round-2 crawl-wave tier consistency

The 4 parallel crawler subagents (Scaling Up TTC, HRPO, SIM-CoT, Stochastic Soft Thinking) produced 37 new source pages. Observations:

- **Same over-grading pattern as sweep #1, different subagents.** Enthusiasm-driven primary tagging persists. Of the 37 new sources, 10 needed downgrades from primary (12 source-project cells). The pattern: when a paper has a striking result (LoopFormer elastic-depth, OneVL "first-to-surpass", ALiCoT theorem, Latent Thinking Optimization's positive interpretability), the crawler tags primary. Autoreview discipline reserves primary for methods we're actively running OR (for theory/interpretability) load-bearing framing.
- **Scaling-Up-TTC crawler was the most disciplined.** 16 sources added, relatively few over-grading issues. This may reflect better-scoped crawl context or the fact that recurrent-depth family has sharper recipes to evaluate (code + weights are clearer signals).
- **SIM-CoT crawler was the most enthusiastic.** OneVL, ALiCoT, CoLT, LaRA-VLA, DualCoT-VLA, OneLatent, LatentChem, Adaptive-Latent-CoT-Pretraining, Visual-Enhanced-Depth-Scaling — 9 sources, many multimodal/domain-specific, 2 got primary downgrades. Pattern: "SIM-CoT's auxiliary-decoder idea is being extended to X" crawler read as primary-worthy. Autoreview discipline: SIM-CoT extensions are secondary unless they advance a recipe on our stack.
- **Stochastic-Soft-Thinking crawler was accurate on core papers (SeLaR, Multiplex Thinking, ThinkRouter as primary for appropriate projects) but over-graded SeLaR as branch-d primary.** Pattern: entropy/contrastive diversity papers are adjacent to CPF but not always recipe inputs.
- **HRPO crawler was brief but accurate.** 3 sources (ThinkRouter, Implicit Reasoning Survey, Mull-Tokens) — minimal adjustment needed.
- **Under-grading remained minimal.** No upgrades this sweep. This may be an autoreview blind spot: we're calibrated to downgrade, not upgrade.

### Schema + structural observations

- **Concept coverage still under-built.** Round-2 papers cite concepts without dedicated pages: `Mode Elicitation` (LaDi-RL, LED-adjacent), `Layer-Asymmetric Collapse` (LED + LTO), `Opaque Serial Depth` (conceptualized in the source page but no concept page). Follow-up for `wiki-lint`.
- **Entity coverage expanded.** 70 entities now (up from 61). Notably new: Jonas Geiping, Sean McLeish, Markus Frey, Hugh Blayney, Sangmin Bae, Yee Whye Teh.
- **`last_reviewed` normalization succeeded** — all 86 sources carry `last_reviewed: 2026-04-23, reviewed_by: autoreview` after this sweep.
- **Duplicate raw-file warning:** `.raw/papers/` has both `2508.03440-soft-thinking-mechanism.md` and `2508.03440-soft-thinking-single-threaded.md` for the same arXiv ID — both referenced. Also `2604.04902-are-lrms-interpretable.md` and `2604.04902-lrm-interpretable.md` (duplicate for Are-LRMs). Flag for `wiki-lint` canonicalization.

### Systemic issues noticed

- **Primary-discipline drift recurs every crawl wave.** Both sweeps downgraded ~10 primary tags. This suggests crawlers should either be given explicit "reserve primary for active-run or load-bearing framing" instructions OR autoreview should accept downgrade-heavy sweeps as the expected steady-state cost of broad crawls.
- **Contradiction clusters grow rather than resolve.** Sweep #1 flagged 3 contradictions; sweep #2 added 2 more and extended 1 existing cluster (curriculum necessity) from 3-way to 4-way. None resolved. For interpretability-driven writeups this is actually valuable — the tension is the scientific signal. But eventually someone needs to take a stance.
- **Domain-specific papers contaminate core taxonomy.** SIM-CoT crawler's VLA trilogy (OneVL / LaRA-VLA / DualCoT-VLA) and Mull-Tokens (multimodal) + LatentChem + Visual-Enhanced-Depth-Scaling pull the taxonomy toward applied-domain breadth. All now secondary/reference on the core branches. Worth a periodic "prune applied-domain to reference" pass.

### Most valuable newly-realized findings (things that emerge from cross-source review)

1. **CPF convergence is now five independent groups.** Sweep #1 noted LT-Tuning / HRPO / Latent-SFT / Soft Thinking converging on the `weighted-vocab-embeddings + context` form. Sweep #2 adds [[Multiplex Thinking]] (K-sample sparse variant, with released code + checkpoints). Five independent discoveries of the same mechanism across distinct research groups is strong evidence for a fundamental inductive bias rather than convergent local-minimum seeking. Branch D's CPF-on-CODI is on very solid ground.

2. **Feature Collapse is layer-asymmetric.** Not a single new paper's claim — emerges from reading [[Latent Exploration Decoding]] (final-layer-only entropy collapse) + [[Latent Thinking Optimization]] (Huginn reward signal invisible to logit lens but visible to classifier) + [[ThinkRouter]] (confidence anomaly on soft embeddings) together. The intermediate layers are a preserved-diversity reservoir. Branch D CPF reads as one of several interventions (alongside training-free decoding-time methods SeLaR / LED / ThinkRouter) that exploit this asymmetry — our writeup can now frame them as a coherent family.

3. **Retrofit path to recurrent-depth is viable.** Combining [[Retrofitted Recurrence]] (curriculum conversion of pretrained LMs with k=8 BPTT, 3-model validation) + [[Encode Think Decode]] (FAIR's middle-layer-only retrofit, +28.4% on 17 benchmarks) + [[From Growing to Looping]] (grow ≡ loop mechanistic equivalence) + [[Inner Loop Inference]] (zero-train upper bound) + [[Skip a Layer or Loop it]] (MCTS over layer config) → a clear recipe space for adding depth recurrence to Qwen3-4B without a Frontier-scale from-scratch pretraining. This materially expands Branch A's scope from "scale post-hoc latent scaffolding" to "scale post-hoc latent scaffolding OR retrofit to depth-recurrent."

4. **Hybrid latent/discrete reasoning is a recurring design pattern.** [[ThinkRouter]] (training-free, threshold-switch) + [[SwiReasoning]] (switch-based) + [[HRPO]] (learned-gate RL) — three independent groups at distinct points in the design space. Collectively indicate that pure-latent is suboptimal, and that the switching axis (latent vs discrete per step) is load-bearing. For the SPAR writeup, this belongs in the taxonomy as a distinct cell, not scattered.

5. **Theoretical necessity claims don't generalize across latent regimes.** Sweep #1 flagged the Capabilities-and-Limits vs Soft-Tokens / Token-Assorted tension. Sweep #2 adds [[ALiCoT]]'s Order-r decay theorem as a second independent necessity result — and it's contested by the same two empirical papers. The signal here: theoretical arguments for "curriculum / alignment necessary" appear tied to continuous distillation regimes. RL (Soft Tokens) and discrete-codebook latents (Token Assorted) escape. The writeup's theory section needs this caveat.

6. **Probe methodology itself is contested.** [[Decoding Depth-Recurrent Transformer]] (logit-lens says Huginn has little interpretable latent CoT; introduces Coda Lens) + [[Latent Thinking Optimization]] (reward-classifier says Huginn latents DO encode process-level signal) + [[Are LRMs Easily Interpretable]] (CODI latents 65-71% decodable with context) + [[Weak vs Strong Supervision Study]] (CODI latents often bypassed for shortcut behavior). The picture: same models, different readouts give different answers. Branch C's probe-methodology investigations now have a clear methodological target — any claim about latent interpretability should specify the readout.

---

## [2026-04-23] autoreview sweep #1

**Context:** First live autoreview. Vault has 49 sources, 17 concepts, 61 entities after the initial crawl wave (4 parallel seed crawls on COCONUT/CODI/CoLaR/Ouro). 38 of 49 sources were freshly graded by 4 different crawler subagents; this sweep re-reads every source against the current REGISTRY.

**Sources reviewed:** 49
**Tier changes:** 11 (all reviewed pages, 11 had ≥1 tier shift)
**Contradictions flagged:** 3 (0 resolved)
**Archived:** 0 orphans, 0 stale (none eligible — all entity pages have `projects:` entries; all concepts have ≥1 inbound link; all sources are ≤1 day old)
**Dashboards regenerated:** branch-a, branch-b, branch-c, branch-d, spar-latent-reasoning

### Notable tier shifts

All changes were spar-latent-reasoning primary-list prunes + a couple of smaller adjustments. Intent: keep spar-primary reserved for methods we're actively running/citing or for load-bearing framing.

- [[Parcae]] — spar-latent-reasoning: primary → secondary (looped-LM scaling laws; useful reference, but from-scratch pretraining is off the V2/SIM-CoT/LT-Tuning synthesis line)
- [[Think-at-Hard]] — spar-latent-reasoning: primary → secondary (Qwen3 base + public code is attractive, but looping adaptive-depth is taxonomic-only for the north-star)
- [[Mechanistic Analysis of Looped Reasoning LMs]] — spar-latent-reasoning: primary → secondary (Ouro T>4 explanation is valuable but we're not running Ouro mech-interp as primary)
- [[Formal CoT vs Latent]] — spar-latent-reasoning: primary → secondary (clean theoretical separation; citation-only for writeup)
- [[Hierarchical Reasoning Model]] — spar-latent-reasoning: primary → secondary ('no-CoT, from-scratch' is a counterpoint citation, not a synthesis input)
- [[Continuous CoT Parallel Exploration]] — spar-latent-reasoning: primary → secondary (theoretical framing is already anchored by [[Reasoning by Superposition]] + [[Capabilities and Limits of Latent CoT]])
- [[MARCOS]] — spar-latent-reasoning: primary → secondary (+4.7% over token CoT is a great datapoint but no code; cite, not anchor)
- [[Latent-SFT]] — spar-latent-reasoning: primary → secondary (CPF-equivalent and Gumbel-SFT are citation-worthy; superposition framing already primary-anchored elsewhere)
- [[LSTR]] — spar-latent-reasoning: primary → secondary (interpretability overlay; architecture pulls off the main synthesis line)
- [[HRPO]] — branch-a: secondary → reference (no direct Qwen3 scaling test; RL-without-CoT framing is not the architecture-dependence story)
- [[Continuous CoT Multilingual]] — spar-latent-reasoning: secondary → reference (CODI generalization datapoint only; no method/framing contribution)

### New contradictions (requires attention)

1. **[[Are LRMs Easily Interpretable]] vs [[Weak vs Strong Supervision Study]] on CODI latent utilization:** Interpretability paper finds CODI latents encode gold traces 65-71% of the time on GSM8k-Aug. Supervision study finds weakly-supervised CODI often exhibits shortcut behavior (latents not used). Likely reconciled by task type (arithmetic: decodes well and uses; logical: zero-latent answers unchanged). Flagged on both pages with `[!contradiction]` callouts.

2. **[[Capabilities and Limits of Latent CoT]] vs [[Soft Tokens Hard Truths]] on curriculum necessity:** Theoretical paper proves curriculum is necessary to traverse Exploration-Execution trade-off. Soft Tokens paper trains continuous CoT via RL alone at 8B without curriculum, matching discrete CoT. May be regime-specific (distillation vs RL) — but tension is unresolved. Flagged on both pages.

3. **[[Capabilities and Limits of Latent CoT]] vs [[Token Assorted]] on curriculum necessity (discrete-latent variant):** Token Assorted explicitly ablates and finds randomized-m single-stage training OUTPERFORMS multi-stage curriculum. May be the discrete-latent vs continuous-latent distinction — distributional-mismatch-driven curriculum necessity may not apply when latents live in a discrete codebook. Flagged on both pages.

No fourth contradiction this sweep; CPF / fusion convergence is clean. [[Latent Thoughts Tuning]] / [[HRPO]] / [[Latent-SFT]] / [[Soft Thinking]] all agree on vocab-manifold anchoring as the anti-collapse mechanism.

### Dropped contradictions (auto-resolved)

None — no prior contradictions to re-check; this is sweep #1.

### Audit of crawl-wave tier consistency

The 4 parallel crawler subagents produced 38 of the 49 source pages. Observations on consistency:

- **Overall consistency is high.** The CPF-family convergence (LT-Tuning / HRPO / Latent-SFT / Soft Thinking all tagging branch-d primary, all with similar rationales) reads as four independent crawler subagents landing on the same interpretation — a healthy signal of shared context understanding.
- **Systematic over-grading on spar-latent-reasoning primary.** Multiple subagents marked taxonomic / theoretical papers as spar-primary when the REGISTRY discipline is "methods we're *actively* running or citing." This sweep reclassified 9 such cases. Pattern: when a paper has a striking empirical finding (MARCOS +4.7%, Parcae scaling-laws) or a novel framing (LSTR sparse-transcoder, HRM no-CoT), the initial crawler tagged it primary out of enthusiasm. Autoreview discipline: primary is reserved for synthesis inputs + interpretability anchors, not "interesting findings." Watch for this on future crawls.
- **Under-grading was minimal.** No paper needed a tier upgrade in this sweep. This is possibly because the initial crawl is very recent and crawlers were tuned to surface relevance; may drift on next sweep.
- **Project coverage is solid.** All 49 sources have `projects:` entries for all 5 projects. No missing project tags.

### Schema + structural observations

- **Concept pages are under-created.** Many sources cite concepts that don't have a dedicated page: `Shortcut Behavior` (exists, good), `Exploration-Execution Trade-off` (exists, 1 inbound — could gain more), `Gumbel-Softmax Latent` (exists, 2 inbound), `Greedy Pitfall` (doesn't exist — could be created from [[Stochastic Soft Thinking]]), `Sparse Autoencoder` (linked from [[LSTR]] but missing).
- **Entity orphans (0 inbound wikilinks) are not true orphans** — they all have `projects:` entries per schema. Per SKILL § 4, orphan = 0 inbound AND no `projects:`. No entity is eligible for archive.
- **`last_reviewed` normalization succeeded** — all 49 sources now carry `last_reviewed: 2026-04-23, reviewed_by: autoreview`. [[Latent Thoughts Tuning]] was a straggler at 2026-04-22; fixed.
- **[[KaVa]]'s related list** includes `[[R-KV Eviction]]` which doesn't exist as a concept page. Minor, but a concept-creation target if we want fuller coverage of KV-compression mechanisms.
- **[[Soft Thinking]]'s related list** references `[[Soft Thinking Mechanism]]` and `[[Latent Reasoning as Chain of Superposition]]` — neither exists as a page. Likely renames/duplicates of [[Stochastic Soft Thinking]] and [[Latent-SFT]] respectively. Cross-linking drift; flag for next lint pass.
- **[[Reasoning by Superposition]]'s related list** references `[[Latent Reasoning as Chain of Superposition]]` — should likely be `[[Latent-SFT]]`.

Net: concept-page creation and wikilink-canonicalization are the obvious next-sweep follow-ups; they're deferred to a `wiki-lint` pass rather than blocking this autoreview.

---
