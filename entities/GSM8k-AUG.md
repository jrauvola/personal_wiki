---
type: entity
title: "GSM8k-AUG"
created: 2026-04-22
updated: 2026-04-22
tags:
  - entity/dataset
  - domain/benchmarks
  - domain/latent-reasoning
status: seed
entity_type: dataset
role: "Equation-only augmented GSM8k variant used as the canonical latent-CoT benchmark (CODI, PCCoT, KaVa)."
first_mentioned: "[[KaVa]]"
related:
  - "[[KaVa]]"
  - "[[CODI]]"
  - "[[GSM8k-AUG-NL]]"
sources:
  - "[[KaVa]]"
projects:
  - slug: "branch-b"
    relevance: secondary
    why: "Standard benchmark for latent-CoT ablations; useful as evaluation axis for detach/fp32 variants."
  - slug: "branch-d"
    relevance: primary
    why: "Primary benchmark for CODI/PCCoT/KaVa comparisons when evaluating CPF-on-CODI."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Recurring evaluation target across the latent-reasoning literature."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# GSM8k-AUG

Equation-only augmented variant of GSM8k used as the canonical latent-CoT benchmark across CODI, PCCoT, and [[KaVa]]. Traces contain structured arithmetic expressions (e.g. `<<650*2=1300>>`), making token-level correspondence between teacher CoT and student latents tractable.

## Reference scores (Llama-3.2-1B-Instruct, from [[KaVa]])

| Method | Accuracy |
|--------|---------:|
| Full CoT upper bound | 61.6 |
| No-CoT lower bound | 30.9 |
| CODI | 55.6 |
| PCCoT | 53.4 |
| KaVa | 56.5 |

Scales to Llama-3.2-3B: KaVa reaches 65.7 (≈5pt over CODI).

## Related

- [[GSM8k-AUG-NL]] — the natural-language counterpart
- [[KaVa]] — primary source
