---
type: source
title: "A Survey on Latent Reasoning"
source_type: paper
arxiv_id: "2507.06203"
venue: "arXiv"
date_published: 2025-07-08
authors:
  - "Rui-Jie Zhu"
  - "Tianhao Peng"
  - "Tianhao Cheng"
  - "Xingwei Qu"
  - "Jinfa Huang"
  - "Dawei Zhu"
  - "Hao Wang"
  - "Kaiwen Xue"
  - "Xuanliang Zhang"
  - "Yong Shan"
  - "Tianle Cai"
  - "Taylor Kergan"
  - "Assel Kembay"
  - "Andrew Smith"
  - "Chenghua Lin"
  - "Binh Nguyen"
  - "Yuqi Pan"
  - "Yuhong Chou"
  - "Zefan Cai"
  - "Zhenhe Wu"
  - "Yongchi Zhao"
  - "Tianyu Liu"
  - "Jian Yang"
  - "Wangchunshu Zhou"
  - "Chujie Zheng"
  - "Chongxuan Li"
  - "Yuyin Zhou"
  - "Zhoujun Li"
  - "Zhaoxiang Zhang"
  - "Jiaheng Liu"
  - "Ge Zhang"
  - "Wenhao Huang"
  - "Jason Eshraghian"
url: "https://arxiv.org/abs/2507.06203"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "TAXONOMY: Latent reasoning methods divide into (1) vertical recurrence — feedback loops on activations, expanding computational depth; (2) horizontal recurrence — hidden states propagated across long sequences, expanding sequential capacity."
  - "TAXONOMY (fine): within vertical recurrence, distinguishes activation-based recurrence, hidden-state propagation, and fine-tuning strategies that compress/internalize explicit traces."
  - "ADVANCED PARADIGM: infinite-depth latent reasoning via masked diffusion models — globally consistent and reversible reasoning; identified as a forward direction."
  - "FRAMING: Neural network layers are the computational substrate for reasoning; hierarchical representations support complex transformations — sets up layer-reuse/depth-recurrence as the natural reasoning primitive."
  - "SCOPE: 34 authors including Rui-Jie Zhu (lead, Ouro), Jason Eshraghian (Mila) — same lineage as Ouro/LoopLM. Comprehensive reference for the umbrella taxonomy."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Canonical framing paper for the umbrella — vertical/horizontal recurrence split is a load-bearing taxonomy we should cite whenever we taxonomize the vault. Matches the authors who produced Ouro."
  - slug: "branch-a"
    relevance: reference
    why: "General framing; useful for the scaling-story literature review section."
  - slug: "branch-b"
    relevance: reference
    why: "Background for detach/BPTT motivation."
  - slug: "branch-d"
    relevance: reference
    why: "Fine-tuning-to-compress-traces section is the taxonomy slot for CPF / LT-Tuning / CODI family."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/survey
related:
  - "[[Ouro]]"
  - "[[Scaling Up TTC]]"
  - "[[Implicit Reasoning Survey]]"
sources:
  - "[[.raw/papers/2507.06203-survey-latent-reasoning]]"
---

# A Survey on Latent Reasoning

## TL;DR
34-author community survey (lead: Rui-Jie Zhu, same lineage as Ouro). Proposes a taxonomy: **vertical recurrence** (feedback loops on activations, expanding computational depth — activation-based reasoning) vs **horizontal recurrence** (hidden-state propagation across long sequences, expanding sequential capacity). Fine-tuning methods that compress/internalize explicit traces are a third axis. Advanced direction: masked-diffusion latent reasoning for infinite-depth, globally-consistent trajectories.

## Relevance
The canonical framing paper for our umbrella. Vertical/horizontal recurrence is the taxonomy we should adopt in the REGISTRY and the Phase-0 writeup — our current coverage is heavy on vertical (COCONUT, CODI, Huginn, Ouro, LT-Tuning) and lighter on horizontal. Worth pulling 5–10 horizontal-recurrence pages next pass.
