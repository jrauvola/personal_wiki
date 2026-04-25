---
type: meta
title: "Operations Log — lpcvc-2026-track1"
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: project workspace surface
updated: 2026-04-25
---

# Operations Log

Append-only log of ingest / lint / autoreview operations. Newest entries at the top.

## 2026-04-25

- **autoresearch round 3 (4 parallel subagents).** Subagent A: FastViT-MCi2/MCi4 architecture deep-dive. Subagent B: AIMET vs QAI Hub built-in. Subagent C: LPCV historical winners + Qualcomm playbook. Subagent D: distillation, TripletCLIP, SigLIP2 image-encoder, Matryoshka, sigmoid vs softmax. Pages filed: 5 (1 P0 question + 3 sources + 1 concept). Major surprise: possible MobileCLIP-S2/MCi2 vs MobileCLIP2-S4/MCi4 deployed-checkpoint mismatch (latency consistent with MCi2). Most actionable new finding: LPCVC 2025 Track 2 (SEUDecoder) winning pattern = frozen VL backbone + small fine-tuned head — cross-validates the CLIC text-only fine-tune direction.
- **autoresearch round 1+2 (5 angles).** Searches: 9 (5 R1 + 4 R2). Fetches: 7 (4 R1 + 3 R2). Pages created: 9 (1 synthesis + 4 sources + 4 concepts + 1 entity). Key contradiction surfaced: team's swish→ReLU intuition not supported by EfficientFormer iPhone-NPU data (3.1% accuracy cost for 0.5 ms savings; HardSwish 10× slower). Highest-yield finding: CLIC text-encoder-only fine-tune at 0.01% pretraining cost. Synthesis: [[questions/Research - LPCVC 2026 Track 1 Winning Recipes]].
- **Project bootstrapped.** Added entry to `meta/projects/REGISTRY.md`, scaffolded `projects/lpcvc-2026-track1/{hot,index,log,overview,experiments}.md` and `experiments/`. Codebase pointer `.wiki-project` set in `/Users/jrauvola/Desktop/lpcvc-submission-team-manifold/`. CLAUDE.md added to codebase with path-resolution overrides.
