---
type: entity
entity_type: person
title: "Jason Weston"
role: "Lead author of original Memory Networks (Weston et al. 2014); co-author End-to-End Memory Networks; Meta FAIR research lead on dialogue, memory, and reasoning"
first_mentioned: "[[End-to-End Memory Networks]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/external-memory
  - domain/dialogue
  - affiliation/meta-fair
status: developing
projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Originator of the 'memory networks' research program (2014). Memory Networks are the conceptual ancestor of modern attention-over-side-channel architectures, including Latent Scratchpad."
  - slug: "branch-d"
    relevance: secondary
    why: "Memory Networks formalism (input I, generalize G, output O, response R) is the canonical decomposition for any architecture with a learned write/read decision over memory - applicable framing for W3.5."
  - slug: "branch-a"
    relevance: reference
    why: "Pre-LLM era; not in scaling debate."
  - slug: "branch-b"
    relevance: reference
    why: "Memory mechanisms adjacent to detach policy."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Probe methodology unrelated."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[End-to-End Memory Networks]]"
  - "[[Sainbayar Sukhbaatar]]"
sources:
  - "[[End-to-End Memory Networks]]"
---

# Jason Weston

## Position
Research scientist at Meta FAIR; long-tenured (joined 2014). PhD from Royal Holloway, prior to NEC Labs and Google.

## Core contributions

- **Memory Networks, 2014** (arXiv:1410.3916, with Chopra, Bordes). Founding paper of the memory-network research program. Decomposed memory access into four components: input feature map I, generalization G, output feature map O, response R. **Required strong supervision per hop** — score-function (REINFORCE) gradients on discrete memory access were too noisy to train end-to-end. This limitation is what [[End-to-End Memory Networks]] later overcame with soft attention.

- **End-to-End Memory Networks, 2015** ([[End-to-End Memory Networks]]) — co-author with Sukhbaatar et al.

- **bAbI tasks, 2015** (with Bordes et al.). Synthetic question-answering benchmark suite explicitly designed to test the kinds of reasoning memory-augmented models should solve. Still the canonical benchmark for memory-augmented architectures.

- **Hundreds of dialogue / chatbot / RAG papers** at FAIR (BlenderBot, Wizard of Wikipedia, Saliency-Augmented LM, etc.). Continuous workstream on long-context dialogue with external memory.

## Why relevant to this project

The original Memory Networks paper (2014) is **why soft attention over memory had to be invented in the first place** — strong-supervision-per-hop didn't scale, and discrete-decision REINFORCE was too noisy. This is the historical lesson that motivates W3.5's choice of Gumbel-STE over REINFORCE for the emission gate.

The four-component decomposition (I, G, O, R) is also the right mental model for the W3.5 scratchpad: emitted notes (O) are the persistent memory state; subsequent latent positions are queries (I/G); decoded answer is response (R).

## See also

- [[End-to-End Memory Networks]] — co-authored primary source.
- [[Sainbayar Sukhbaatar]] — first author MemN2N.
- [[Discrete Gate Training]] — concept page covering why REINFORCE failed for original Memory Networks.
