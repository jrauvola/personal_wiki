---
type: experiment
title: "F6 — Gaussian-noise perturbation of latent KV"
slug: f6-kv-noise-sweep
status: success
started: 2026-04-22
finished: 2026-04-23
hypothesis: "If latent KV occupies a narrow geometric basin, small noise should be absorbed but moderate noise should break the routing mechanism."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/inert_latent_hypothesis_tests.md
  - "branch: feature/f6-kv-perturb"
updated: 2026-04-25
---

# F6 — Gaussian-noise perturbation of latent KV

## Parent context

Third GPU test in the F1-F6 battery, branched off [[phase-1-v2-bf16-training]]. Complements F4 (full ablation) and F5 (in-distribution swap) by adding *out-of-distribution geometric perturbation* to latent KV — a scale we can tune.

## Hypothesis

If latent KV is a narrow geometric basin required for template routing, small `σ` should be absorbed (basin tolerance) and larger `σ` should break the routing entirely. The σ at which accuracy collapses defines the basin width.

## Method

- Variant: V2 bf16, num_latent=8.
- New helper `latent_tap.py::_perturb_latent_kv` adds Gaussian noise to latent-position K and V tensors at inference: `KV ← KV + σ × std(KV_layer) × N(0, I)`. Per-layer per-tensor std. Deterministic via `perturb_seed=1234`. Gated by flag `perturb_latent_kv_sigma_mult`.
- σ ∈ {0.1, 0.5, 1.0}.
- Re-evaluate on first 200 GSM8k examples + first 200 SVAMP examples.

## Result

| σ multiplier | Benchmark | N | Accuracy | Δ vs baseline |
|---|---|---|---|---|
| baseline | GSM8k | 1319 | 0.163 | — |
| 0.1 | GSM8k | 200 | **0.215** | +0.052 |
| 0.5 | GSM8k | 200 | **0.005** | -0.158 |
| 1.0 | GSM8k | 200 | **0.010** | -0.153 |
| baseline | SVAMP | 300 | 0.423 | — |
| 0.1 | SVAMP | 200 | **0.375** | -0.048 |
| 0.5 | SVAMP | 200 | **0.025** | -0.398 |
| 1.0 | SVAMP | 200 | **0.030** | -0.393 |

- σ=0.1 absorbed (within sampling noise; GSM8k's slight "improvement" is subset variance).
- σ=0.5 collapses accuracy to <3% on both benchmarks.
- σ=1.0 stays collapsed — no further degradation because template lock is already broken.

## Verdict

**Success — narrow geometric basin confirmed.** Small perturbations are absorbed; σ=0.5 noise destroys the template-routing mechanism entirely. The latent KV must have *enough* geometric structure to route to the format-prior attractor (F6 cliff at σ=0.5), but the per-example content of that structure does not matter (F5 swap-null) and its per-step token content is a fixed template (F3). σ=0.5 noise breaks not the ability to compute per-example answers — that was never there — but the ability to lock into the "The answer is: …" emission mode.

## Revert info

- Code: `feature/f6-kv-perturb` (later cherry-picked into LT-Tuning eval branch alongside F4/F5 helpers). Adds `perturb_latent_kv_sigma_mult` + `perturb_seed` flags to `LatentRuntimeConfig` and `_perturb_latent_kv` helper in `latent_tap.py`.
- No persistent training artifacts. Raw outputs deletable.
- Shared with LT-Tuning F-battery eval; do not remove the helpers if that branch is still active.

## Follow-ups / branch-offs

- F6 closes the F1-F6 battery. Synthesis: latents are a "geometric key for template routing" — narrow basin, content-insensitive but existence-required.
- LT-Tuning re-run [[lt-tuning-f-battery-eval]] queued F6 but the battery crashed before reaching it.
