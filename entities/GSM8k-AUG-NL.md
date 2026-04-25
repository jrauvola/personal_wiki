---
type: entity
title: "GSM8k-AUG-NL"
created: 2026-04-22
updated: 2026-04-22
tags:
  - entity/dataset
  - domain/benchmarks
  - domain/latent-reasoning
status: seed
entity_type: dataset
role: "Natural-language variant of GSM8k-AUG; stress-test for latent-CoT methods against verbose, non-template reasoning traces."
first_mentioned: "[[KaVa]]"
related:
  - "[[KaVa]]"
  - "[[GSM8k-AUG]]"
  - "[[CODI]]"
sources:
  - "[[KaVa]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Natural-language stress test is precisely the failure mode CPF-on-CODI must pass; KaVa's ~1pt degradation here is the bar to beat."
  - slug: "branch-b"
    relevance: secondary
    why: "Alternative evaluation axis to stress detach/fp32 variants beyond equation-only traces."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Defines the 'supervision gap' phenomenon quantitatively — load-bearing for the writeup."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# GSM8k-AUG-NL

Natural-language variant of [[GSM8k-AUG]] where CoT traces are verbose English prose rather than structured arithmetic expressions. Functions as a stress-test for latent-CoT methods against non-token-aligned reasoning.

## Why it matters

The gap between GSM8k-AUG and GSM8k-AUG-NL quantifies each method's "supervision gap" robustness:

| Method | GSM8k-AUG | GSM8k-AUG-NL | Δ |
|--------|----------:|-------------:|--:|
| Full CoT | 61.6 | 53.2 | −8.4 |
| COCONUT | 45.3 | 27.2 | −18.1 |
| CODI | 55.6 | 49.7 | −5.9 |
| PCCoT | 53.4 | 50.7 | −2.7 |
| **KaVa** | **56.5** | **55.7** | **−0.8** |

(CODI on Qwen-0.5B reportedly drops 20+ points; the Llama-1B numbers above are less severe but the ordering is consistent.)

KaVa's ~1-point degradation is the headline result — compressed-KV supervision absorbs abstract structure that direct hidden-state matching misses.

## Related

- [[GSM8k-AUG]] — equation-only counterpart
- [[KaVa]] — primary source
