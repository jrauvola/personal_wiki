---
type: experiment
title: "F5 — Cross-example latent KV swap"
slug: f5-cross-example-kv-swap
status: success
started: 2026-04-22
finished: 2026-04-23
hypothesis: "If latents carry per-example reasoning content, overwriting B's latent KV with A's should change B's prediction substantially and likely degrade B's accuracy."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/inert_latent_hypothesis_tests.md
  - "branch: feature/f5-kv-swap"
updated: 2026-04-25
---

# F5 — Cross-example latent KV swap

## Parent context

Companion GPU test to [[f4-latent-kv-ablate]] in the F1-F6 battery. Branched off [[phase-1-v2-bf16-training]]. While F4 asks "does the latent KV matter at all?", F5 asks "does the *per-example content* of the latent KV matter, or is it interchangeable across examples?"

## Hypothesis

If latents carry per-example reasoning content, swapping B's latent-position KV with another arbitrary example A's should:
1. Change B's predicted text substantially (>>50% of cases).
2. Degrade B's accuracy (B is now "reasoning about" a different problem's intermediate state).

If swap is roughly null on both metrics, the latent KV is acting as a generic prefix — its specific per-example content is downstream-invisible.

## Method

- Variant: V2 bf16, num_latent=8, GSM8k.
- Sample 30 GSM8k example pairs (A, B). For each pair:
  1. Forward A through latent rollout, capture A's latent-position K,V slices from every layer via `capture_latent_kv_slice`.
  2. Forward B baseline.
  3. Forward B with A's latent-position KV overwritten via `inject_latent_kv_slice`.
- Greedy decoding, same hyperparameters. Reduced from planned 100 pairs to 30 because GH200 was shared.
- New helpers in `latent_tap.py`: `capture_latent_kv_slice`, `inject_latent_kv_slice`.

## Result

| Metric | Value |
|---|---|
| Pairs | 30 |
| B accuracy, baseline (own KV) | **0.100** (3/30) |
| B accuracy, with A's latent KV injected | **0.100** (3/30) |
| Fraction of B predictions that changed (text) | **13.3%** (4/30) |

Companion proxy at N=200 (see [[f5-proxy-cosine]]): median pairwise cosine 0.78, 63 PCs for 95% variance — latent KVs do carry per-example variation, but that variation does not affect the output for ~87% of cases.

## Verdict

**Failure of the "per-example KV content matters" hypothesis (success of the test).** Overwriting B's latent KV with an arbitrary different example A's latent KV changes B's prediction in only 13% of cases and leaves B's accuracy unchanged (0.100 → 0.100). The decoder treats the latent KV region as a generic "latent prefix" not as a vehicle for reasoning content. Combined with [[f4-latent-kv-ablate]]: latent KV contributes a weak prior, but that prior is example-agnostic. *Caveat:* 30 pairs is small; the F5 mechanism is reconciled with Christopher's ±10-12% Llama-1B KV-steering effect via the basin-vs-direction argument in [[kv-pca-analysis]].

## Revert info

- Code: `feature/f5-kv-swap` (later cherry-picked into LT-Tuning eval branch alongside F4/F6 helpers). New helpers `capture_latent_kv_slice` and `inject_latent_kv_slice` in `latent_tap.py`.
- No persistent training artifacts to revert. Raw outputs deletable.
- The helpers are shared with the LT-Tuning F-battery eval (which also runs F5); do not remove if that branch is still active.

## Follow-ups / branch-offs

- [[f5-proxy-cosine]] — N=200 proxy cosine analysis. Establishes that KV content does vary per-example, but downstream is invisible to it.
- [[branch-2-quora-faithfulness-probe]] — token-level Quora probe attempted to disambiguate "post-hoc commitment" vs "iterative" vs "inert" interpretations of the swap-null. Data-starved; needs raw HS dump.
- [[branch-1-layer-asymmetric-probe]] — confirmed F5's swap-null is mechanistically explained by the final-layer routing template: swapping two copies of the template is no-op.
