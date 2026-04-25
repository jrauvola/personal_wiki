---
type: question
title: "Open Question: Which MobileCLIP checkpoint is actually deployed?"
status: open
priority: P0
created: 2026-04-25
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Latency-numbers vs claimed-architecture mismatch. If wrong checkpoint deployed, all downstream optimization assumptions shift."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# Open Question: Which MobileCLIP checkpoint is actually deployed?

## The discrepancy

Per the team's `context/PROBLEM_OVERVIEW.md`:
- Current best model: **MobileCLIP2-S4**
- INT8 image encoder latency on XR2 Gen 2: **13.7 ms**

Per autoresearch (verified against `apple/ml-mobileclip` source code and the MobileCLIP2 paper, arXiv 2508.20691):

- **MobileCLIP2-S4 uses the MCi4 backbone** (5-stage, 321.6M image params, ~19.6 ms FP latency on iPhone Apple Neural Engine).
- **MobileCLIP-S2 (v1) and MobileCLIP2-B** use the **MCi2 backbone** (4-stage, ~36M image params).
- The 13.7 ms INT8 figure on XR2 Gen 2 is consistent with MCi2 (~36M params), **not** MCi4 (~321M params).

A 9× param-count difference at the same INT8 latency on the same NPU is implausible.

## Why this matters

If the deployed checkpoint is actually MobileCLIP-S2 (or MobileCLIP2-B), not MobileCLIP2-S4:

1. **Accuracy ceiling is lower than assumed.** MobileCLIP-S2 reports COCO T→I/I→T R@1 = 45.4/63.4 vs MobileCLIP2-S4's 50.6/68.8. The team's headroom for further accuracy gain is larger than they think.
2. **All "MobileCLIP2-S4 INT8 = 0.7527 R@10" measurements need re-attribution.** The benchmark needs to know which checkpoint produced the number.
3. **Competition strategy shifts.** If on a smaller backbone, switching UP to MobileCLIP2-S3 or even MobileCLIP2-S4 is a viable accuracy lever (with a real latency cost). If already on MobileCLIP2-S4, accuracy gains must come from fine-tuning or quantization, not bigger backbone.

## How to verify (5 minutes)

```bash
# In the codebase
grep -r "mobileclip2_s4\|MobileCLIP2-S4\|mci4\|MCi4" \
  /Users/jrauvola/Desktop/lpcvc-submission-team-manifold/

# Count params in the actually-loaded model
python -c "
import open_clip
m, _, _ = open_clip.create_model_and_transforms('MobileCLIP2-S4', pretrained='dfndr2b')
n_image = sum(p.numel() for p in m.visual.parameters())
n_text  = sum(p.numel() for p in m.transformer.parameters())
print(f'image: {n_image/1e6:.1f}M params, text: {n_text/1e6:.1f}M params')
# Expect: image ~321M for true S4, ~36M for S2
"
```

If image params ≈ 321M → S4 confirmed. If ≈ 36M → it's MCi2 (S2 or B), `PROBLEM_OVERVIEW.md` and `AGENTS.md` need correcting.

## Reference data — MCi family at a glance

| MobileCLIP variant | Backbone | Stages | Image params | Text type | Native input |
|--------------------|----------|--------|--------------|-----------|--------------|
| MobileCLIP-S0 / MobileCLIP2-S0 | MCi0 | 4 | small | base 12L | 256 |
| MobileCLIP-S1 / MobileCLIP2-S1 | MCi1 | 4 | small | base 12L | 256 |
| **MobileCLIP-S2 / MobileCLIP2-B** | **MCi2** | **4** | **~36M** | **base 12L** | **256** |
| MobileCLIP2-S3 | MCi3 | **5** | larger | base 12L | 256 |
| **MobileCLIP2-S4** | **MCi4** | **5** | **~321M** | **base 12L** | **256** |

Source: [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]]

## Status

- **2026-04-25:** Flagged via autoresearch round 3. Not yet verified by the team.
