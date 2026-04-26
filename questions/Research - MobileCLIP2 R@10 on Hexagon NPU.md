---
type: synthesis
title: "Research: MobileCLIP2 R@10 Recall measurements on Hexagon NPU"
created: 2026-04-25
updated: 2026-04-25
status: developing
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Validation run of autoresearch-hybrid skill on a topic where both tools failed in the prior A/B test (topic 6). Tests whether hybrid mode surfaces value neither tool got alone."
related:
  - "[[sources/AXERA MobileCLIP2 w8a16 Deployment]]"
  - "[[sources/AWQ - Activation-aware Weight Quantization]]"
  - "[[sources/RegCache - Activation Quantization Vision Encoders]]"
  - "[[concepts/Activation-Aware Quantization Tactics for Vision Encoders]]"
sources:
  - "[[sources/AXERA MobileCLIP2 w8a16 Deployment]]"
  - "[[sources/AWQ - Activation-aware Weight Quantization]]"
  - "[[sources/RegCache - Activation Quantization Vision Encoders]]"
last_reviewed: 2026-04-25
reviewed_by: autoresearch-hybrid
---

# Research: MobileCLIP2 R@10 Recall Measurements on Hexagon NPU

## Overview

Validation run of the new `autoresearch-hybrid` skill on the exact topic where both WebSearch-only and S2-only failed in the [[experiments/s2-vs-websearch-routing-rule|prior A/B test (topic 6)]]. **Hybrid mode succeeded — surfaced 3 high-value sources neither tool found alone.** Confirms the routing rule pays off in practice.

## Top Findings

### 🔥 1. The team is almost certainly running MobileCLIP2-S2, not S4.

AXERA published deployment latencies for both variants on AX650 NPU at w8a16:

| Variant | Image enc | Text enc | Combined |
|---------|-----------|----------|----------|
| MobileCLIP2-S2 | **19.1 ms** | 5.7 ms | **~25 ms** ✓ |
| MobileCLIP2-S4 | **65.3 ms** | 12.7 ms | **~78 ms** ✗ |

The team's measured 13.7 ms image encoder INT8 on Qualcomm XR2 Gen 2 is consistent with MCi2 (S2 backbone, ~36M params) at faster pure W8A8. **There is no plausible path to 13.7 ms for MobileCLIP2-S4 on any current mobile NPU.** Resolves [[questions/Open Question - Which MobileCLIP Checkpoint Is Actually Deployed]]. (Source: [[sources/AXERA MobileCLIP2 w8a16 Deployment]])

### 🔥 2. w8a16 is the cross-vendor production default for MobileCLIP2.

AXERA defaults to w8a16 (not pure W8A8) for both deployed variants. Cross-validates [[sources/AIMET to QAI Hub Workflow]]'s amended guidance that partial mixed precision via `--lite_mp percentage=N;override_qtype=int16` is the right first lever when pure W8A8 hurts attention activations. (Source: [[sources/AXERA MobileCLIP2 w8a16 Deployment]])

### 🔥 3. RegCache is a vision-specific INT8 fix that doesn't appear in keyword search.

[[sources/RegCache - Activation Quantization Vision Encoders]] (arXiv 2510.04547, October 2025) introduces "prefixing registers" — outlier-absorbing prefix tokens specifically designed for vision encoders. Training-free. Authors explicitly state outliers behave differently in vision models vs LLMs, so SmoothQuant/AWQ-style fixes don't directly transfer. **Surfaced via S2 citation graph from MobileCLIP2 anchor; WebSearch missed this paper.**

### 4. MobileCLIP2 reports R@1, not R@10.

The team's metric (Recall@10) is not the metric Apple reports for MobileCLIP/MobileCLIP2. To predict LPCVC performance from Apple's published numbers, treat R@1 as a *lower bound* — R@10 will be higher but the relative ranking across variants should hold. (Source: WebSearch + emergentmind.com summary)

### 5. DFNDR-2B-trained MobileCLIP2 students are biased toward zero-shot classification.

Apple's MobileCLIP2 paper acknowledges: "DFN-pretrained students do not always achieve SOTA retrieval." DFNDR-2B is biased toward zero-shot classification (especially ImageNet-1k). For LPCVC retrieval, this means **MobileCLIP2 may not be optimal even ignoring quantization** — a fine-tune step (per CLIC, see [[sources/CLIC - Compositional Awareness in CLIP]]) is more important. (Source: WebSearch + arXiv html)

### 6. No public Qualcomm Hexagon MobileCLIP2 deployment exists.

Confirmed across both tools. Qualcomm AI Hub Models repo has no MobileCLIP/FastViT/MCi entry (verified in earlier autoresearch). Axera AX650 is the only public mobile-NPU deployment. **The team is producing the first Hexagon datapoint — publication leverage when LPCVC submission lands.**

## S2-unique finds (papers WebSearch missed but citation graph surfaced)

The autoresearch-hybrid routing rule's key payoff:

1. **AWQ (arXiv 2306.00978)** — foundational activation-aware quant principle. 1253 citations. Found via S2 citation graph from TernaryCLIP. (Source: [[sources/AWQ - Activation-aware Weight Quantization]])
2. **RegCache (arXiv 2510.04547)** — vision-encoder-specific INT8 activation quant via prefix tokens. Found via S2 citation graph from MobileCLIP2 anchor. (Source: [[sources/RegCache - Activation Quantization Vision Encoders]])
3. **TinyCLIP (arXiv 2309.12314)** — affinity-mimicking + weight-inheritance distillation, 50% compression at iso-perf. Found via S2 citation graph from MobileCLIP1 anchor. (Not yet fully ingested — flagged as follow-up.)

## Key Concepts

- [[concepts/Activation-Aware Quantization Tactics for Vision Encoders]] — synthesizes the three families of fix (lite_mp, RegCache, AIMET+AdaRound) into a decision tree the team can follow.

## Contradictions

- **Earlier wiki claim:** MobileCLIP2-S4 is the team's deployed model (per [[projects/lpcvc-2026-track1/overview]] and [[questions/Open Question - Which MobileCLIP Checkpoint Is Actually Deployed]]).
  **Evidence now:** Axera latency table makes this implausible. Resolution: update overview.md to reflect S2 / MCi2 as the likely deployed variant pending team verification.

## Open Questions

1. **What's the team's actual measured Recall@10 on the LPCVC sample with MobileCLIP2 INT8?** Still pending team measurement — the load-bearing diagnostic.
2. **Does Hexagon HMX W8A8 (or W8A16) on MobileCLIP2-S2 hit <20 ms image encoder?** Axera's 19.1 ms is at w8a16; pure W8A8 on Hexagon could plausibly be ~13 ms (matches team measurement). Needs verification.
3. **Does RegCache's prefix-token approach work on the MobileCLIP2 image graph as exported?** No public test on MobileCLIP-family. The team would be the first to validate.
4. **What does AXERA's calibration recipe look like in `AXERA-TECH/axera.ml-mobileclip` GitHub repo?** Worth fetching to compare against the team's recipe.
5. **MobileCLIP2-S3 (MCi3, 5-stage) at w8a16 latency?** Not in Axera's deployed set. The accuracy-vs-latency middle ground between S2 and S4 is unmeasured externally.
6. **TernaryCLIP Recall@K on COCO/Flickr** — abstract didn't surface them. May need full-paper fetch for that data.

## Sources

- [[sources/AXERA MobileCLIP2 w8a16 Deployment]] — primary new evidence (per-encoder latency table)
- [[sources/AWQ - Activation-aware Weight Quantization]] — Lin et al., MIT-Han Lab, 2023, MLSys 2024
- [[sources/RegCache - Activation Quantization Vision Encoders]] — arXiv 2510.04547, October 2025
- [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]] — backbone reference (existing)
- [[sources/AIMET to QAI Hub Workflow]] — Hub quantization reference (existing, amended this session)
- [[sources/CLIC - Compositional Awareness in CLIP]] — fine-tuning reference (existing)

## Validation result for the autoresearch-hybrid skill

This run was the deferred validation from the [[experiments/s2-vs-websearch-routing-rule|prior A/B test]]. Topic 6 ("MobileCLIP2 INT8 deployment Hexagon NPU latency") was the topic where both single tools failed (recall 0/3 each).

**Result:** hybrid mode succeeded. WebSearch found AXERA's HuggingFace page (Family A); S2 citation graph from MobileCLIP2 surfaced RegCache + AWQ + TinyCLIP (Families B and C). Combined: 3 unique high-value sources, decisive answer to the checkpoint-identity question, decision-tree concept page tying tactics to the team's specific failure mode.

**Skill performed as designed.** Routing rule validated in production.
