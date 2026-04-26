---
type: source
source_type: deployment_artifact
title: "AXERA-TECH MobileCLIP — w8a16 deployment on AX650 NPU"
arxiv_id: null
venue: "HuggingFace model card"
date_published: 2025
authors: ["AXERA-TECH"]
url: "https://huggingface.co/AXERA-TECH/MobileCLIP"
code_repo: "https://github.com/AXERA-TECH/axera.ml-mobileclip"
has_weights: true
status: integrated
confidence: high
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Only public production deployment of MobileCLIP2-S2 + S4 on a mobile NPU with measured per-encoder latency. Calibration reference for our Hexagon target — and decisive evidence on the team's checkpoint-identity question."
key_claims:
  - "MobileCLIP2-S2 on Axera AX650 NPU at w8a16: image encoder 19.146 ms, text encoder 5.675 ms (combined ~24.8 ms — within LPCVC 35 ms gate)."
  - "MobileCLIP2-S4 on Axera AX650 NPU at w8a16: image encoder 65.328 ms, text encoder 12.663 ms (combined ~78 ms — would FAIL LPCVC 35 ms gate)."
  - "Default deployment quantization is w8a16, not pure W8A8. Confirms cross-vendor pattern that transformer attention activations need INT16 for accuracy retention."
  - "Both encoders compiled separately (image + text). Same pattern as LPCVC sample solution and OpenAI CLIP on Qualcomm AI Hub."
  - "Compiled via Pulsar2 v4.2 framework (Axera's equivalent of QAI Hub). Calibration methodology not disclosed on the model card — must consult github.com/AXERA-TECH/axera.ml-mobileclip."
last_reviewed: 2026-04-25
reviewed_by: autoresearch-hybrid
---

# AXERA MobileCLIP2 — w8a16 Deployment on AX650 NPU

## Why this matters

This is the **only public production deployment of MobileCLIP2 on a mobile NPU** found by autoresearch (the gap [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]] and [[sources/Qualcomm AI Hub Quantization Documentation]] both flagged). Surfaced via WebSearch on the keyword "MobileCLIP MobileCLIP2 Qualcomm Hexagon NPU deployment".

The numbers it provides are the closest external benchmark for the team's deployment target — Axera AX650 is a different vendor's NPU, but the per-encoder latency profile is the right shape to calibrate expectations against.

## The measured table

| Variant | Image encoder | Text encoder | Combined |
|---------|---------------|--------------|----------|
| MobileCLIP2-S2 | **19.146 ms** | 5.675 ms | **~24.8 ms** ✓ under LPCVC gate |
| MobileCLIP2-S4 | **65.328 ms** | 12.663 ms | **~78.0 ms** ✗ FAILS LPCVC gate |

Quantization: **w8a16** (INT8 weights, INT16 activations). Framework: Pulsar2 v4.2.

## Decisive read for the team

The team's [[questions/Open Question - Which MobileCLIP Checkpoint Is Actually Deployed]] question now has strong signal:

- **Team-measured 13.7 ms INT8 image encoder on Qualcomm XR2 Gen 2** is consistent with **MobileCLIP2-S2 (MCi2)** at ~36M image params. Axera shows 19.1 ms at w8a16; pure W8A8 on Hexagon HMX could plausibly be faster.
- **MobileCLIP2-S4 (MCi4)** at ~321M image params would be ~3-4× slower at minimum. Axera's 65.3 ms confirms this. **There is no plausible path to 13.7 ms image encoder for MobileCLIP2-S4 on any current mobile NPU.**

**Therefore:** the team should treat their deployed model as MobileCLIP2-S2, not MobileCLIP2-S4. Update `lpcvc_models.py` defaults if needed.

## Read for submission strategy

- **Stay on MobileCLIP2-S2** (combined ~25 ms on Axera w8a16) — well under the 35 ms LPCVC gate, leaves headroom for accuracy improvements.
- **Do NOT switch to MobileCLIP2-S4** — Axera's 78 ms combined latency is decisive. Even Hexagon's typically faster int8 path won't bring it under 35 ms for the larger backbone.
- **Consider MobileCLIP2-S3 (MCi3, 5-stage)** as the accuracy-vs-latency middle ground — likely 35-45 ms combined, may still fit if Hexagon's int8 is meaningfully faster than Axera's w8a16.
- **Follow w8a16 as the production default** — Axera's choice cross-validates the [[sources/AIMET to QAI Hub Workflow]] guidance that pure W8A8 is risky on transformer attention; partial mixed precision (`--lite_mp`) on Hub is the equivalent path.

## Open gaps

- **Recall@K numbers for the deployed Axera quantized models** — not on the model card. Without these, can't directly compare quantization R@10 retention to FP baseline.
- **Calibration methodology** — referenced GitHub repo (`AXERA-TECH/axera.ml-mobileclip`) needs inspection to extract their calibration recipe.
- **Per-channel weight quantization status** — w8a16 is the precision spec; whether it's per-tensor or per-channel weights is not stated. (Per-channel is mandatory for MCi-family per [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]].)

## Cross-references

- [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]] — backbone details
- [[questions/Open Question - Which MobileCLIP Checkpoint Is Actually Deployed]] — this page resolves it
- [[sources/AIMET to QAI Hub Workflow]] — Hub equivalent of Pulsar2
- [[concepts/INT8 Calibration for Vision-Language Models]]
