---
type: meta
title: "Experiment Tracker — SPAR Latent Reasoning"
created: 2026-04-25
updated: 2026-04-25
status: evergreen
---

# Experiments

Live tracker. Every experiment in this project has a node under `wiki/experiments/{slug}.md`. Each node has hypothesis / method / result / verdict / revert info. Branch-offs link to parents.

For workflow conventions: see memory `feedback_wiki_experiment_tracking.md`. Authoritative chronological log: `research_findings/experiment_scratchpad.md`.

## How to read this index
- 🟢 success · 🟡 partial · 🔴 failure · ⏸️ planned · 🚫 abandoned · 🟦 in flight
- Indentation = branch-off depth. Top-level entries are root-of-track or independent experiments.
- Status reflects the experiment's outcome, not whether the deliverable exists.

## Phase 1 — V2 / V2' training and characterization

🟢 [[experiments/phase-1-v2-bf16-training]] — V2 bf16 step-boundary detach (foundational)
   🔴 [[experiments/f1-unique-correct]] — CODI adds no unique capability
   🟢 [[experiments/f2-loop-content]] — loops are context-free
   🔴 [[experiments/f3-trace-variance]] — 7/8 latent positions are template
       ⏸️ [[experiments/f3-layer-wise-step3]] — deferred (needs GPU re-dump)
       🟢 [[experiments/branch-1-layer-asymmetric-probe]] — CONFIRM mid-stack content (L28-30)
       🟡 [[experiments/branch-2-quora-faithfulness-probe]] — data-starved (needs raw HS dump)
   🟡 [[experiments/f4-latent-kv-ablate]] — 25-29% drop, loops persist
       🟢 [[experiments/f4-per-example-diagnosis]] — real floor 8.5%
   🔴 [[experiments/f5-cross-example-kv-swap]] — swap is null
       🟢 [[experiments/f5-proxy-cosine]] — pair-cos 0.78, 63 PCs
   🟢 [[experiments/f6-kv-noise-sweep]] — σ=0.5 cliff
   🟢 [[experiments/track-a-first-sentence-trim]] — flat curve, rise is artifact
   🟢 [[experiments/kv-pca-analysis]]
   🟢 [[experiments/kv-distance-bf16-vs-fp32]]
   🟢 [[experiments/prediction-degeneracy-analysis]]
   🟢 [[experiments/lightweight-experiments-e1-e4]]

🟡 [[experiments/phase-1-v2-fp32-comparator]] — cross-precision divergence unexplained

## Phase 2 — Interventions

🔴 [[experiments/phase-2b-lt-tuning-cpf-training]] — training success, eval fails Case C
   🔴 [[experiments/lt-tuning-f-battery-eval]] — Phase 1 + F3 + F1 ran; F4/F5/F6 crashed; Case C

🟢 [[experiments/phase-2a-sim-cot-shared-head-smoke]] — 22.5 GB footprint validated
   ⏸️ [[experiments/phase-2a-sim-cot-full-training]] — gated on Case C escalation

## Infrastructure / tooling

🟢 [[experiments/peft-modules-to-save-resize-fix]]
🟢 [[experiments/safe-decode-qwen3-reserved-vocab-patch]]
🟢 [[experiments/eval-harness-pre-wire-lt-tuning]]

## Synthesis

Most informative experiments to date — see [[meta/state-of-project-2026-04-23]] for the curated narrative arc combining these results. The F1-F6 battery + Track A first-sentence-trim + F4 per-example diagnosis + Branch 1 layer-asymmetric probe together establish the routing-mode characterization of V2 bf16 latents.
