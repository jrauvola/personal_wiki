---
type: entity
title: "NeosKnight233/Latent-Thoughts-Tuning"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/repository
  - github
status: seed
entity_type: repository
role: "Official implementation of LT-Tuning"
first_mentioned: "[[Latent Thoughts Tuning]]"
related:
  - "[[Latent Thoughts Tuning]]"
sources:
  - "[[Latent Thoughts Tuning]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Source of truth for the LT-Tuning implementation we need to port onto CODI."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# NeosKnight233/Latent-Thoughts-Tuning

Official GitHub implementation of [[Latent Thoughts Tuning]].

- **URL:** https://github.com/NeosKnight233/Latent-Thoughts-Tuning
- **Stars:** 9 (as of 2026-04-22)
- **Language:** Python 99.2%
- **Checkpoints:** none released

The repo README confirms the three-stage curriculum and Context-Prediction-Fusion formula match the paper. Includes automated stage managers and deepspeed integration scripts. No pre-trained serialization weights on Hugging Face as of late March 2026.

Branch D implementation depends on this repo — either fork directly or port the relevant modules into `latent_eval_training_harness`.
