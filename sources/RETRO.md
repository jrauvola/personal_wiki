---
type: source
title: "Improving Language Models by Retrieving from Trillions of Tokens (RETRO, Borgeaud et al. 2022)"
source_type: paper
arxiv_id: "2112.04426"
venue: "ICML 2022"
date_published: 2021-12-08
authors:
  - "Sebastian Borgeaud"
  - "Arthur Mensch"
  - "Jordan Hoffmann"
  - "Trevor Cai"
  - "Eliza Rutherford"
  - "Katie Millican"
  - "George van den Driessche"
  - "Jean-Baptiste Lespiau"
  - "Bogdan Damoc"
  - "Aidan Clark"
  - "Diego de Las Casas"
  - "Aurelia Guy"
  - "Jacob Menick"
  - "Roman Ring"
  - "Tom Hennigan"
  - "Saffron Huang"
  - "Loren Maggiore"
  - "Chris Jones"
  - "Albin Cassirer"
  - "Andy Brock"
  - "Michela Paganini"
  - "Geoffrey Irving"
  - "Oriol Vinyals"
  - "Simon Osindero"
  - "Karen Simonyan"
  - "Jack W. Rae"
  - "Erich Elsen"
  - "Laurent Sifre"
url: "https://arxiv.org/abs/2112.04426"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "RETRO splits input into 64-token chunks; for each chunk, retrieves k=2 nearest neighbors from a database of up to 2 trillion tokens via frozen BERT[CLS] embedding + SCaNN ANN search."
  - "Chunked Cross-Attention (CCA) integrates retrieved chunks via a separate bidirectional encoder + interleaved cross-attention layers in the decoder."
  - "7.5B-param RETRO matches 175B GPT-3 / Jurassic-1 on the Pile - 25x parameter reduction by externalizing knowledge to retrieval database."
  - "Retriever weights are FROZEN - never updated during training. Only the cross-attention and chunk encoder are trained."
  - "RETRO-fitting: existing pretrained transformers can be retrofitted with retrieval by training only the retrieval-specific weights, with ~3% of original pretraining data, maintaining backward compatibility (works with retrieval disabled)."
projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Demonstrates that DISCRETE external memory (retrieval over a frozen text database) scales cleanly to multi-billion parameters and gives 25x parameter equivalent. Validates the 'discrete external store' arm of Latent Scratchpad's design space."
  - slug: "branch-d"
    relevance: secondary
    why: "RETRO-fitting recipe (bolt retrieval onto a pretrained model with 3% extra training) is the procedural template for how W3.5 should be added to a pretrained CODI checkpoint - frozen base + new gate/head, lightweight retraining."
  - slug: "branch-a"
    relevance: reference
    why: "Different scaling axis (database, not parameters)."
  - slug: "branch-b"
    relevance: reference
    why: "Different memory pattern."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/retrieval-augmented
  - family/external-memory
  - family/discrete-memory
  - type/source
  - status/foundational
related:
  - "[[Memorizing Transformers]]"
  - "[[Compressive Transformer]]"
  - "[[Latent Scratchpad Architecture]]"
sources: []
---

# RETRO: Improving Language Models by Retrieving from Trillions of Tokens

## TL;DR

LM augmented with a frozen retrieval index over up to 2 trillion tokens. Each 64-token chunk retrieves 2 nearest neighbors via BERT[CLS] + SCaNN; retrieved content enters via a separate encoder + chunked cross-attention. **A 7.5B RETRO matches 175B GPT-3 / Jurassic-1**, demonstrating 25× parameter equivalence by externalizing knowledge to a discrete database.

## Why this matters for the Latent Scratchpad

RETRO is the **strongest demonstration that discrete external memory works at LLM scale** when designed carefully. The relevance to Latent Scratchpad is structural, not literal:

1. **Discrete external store** — RETRO's database is text; W3.5's scratchpad is vocab tokens. Both demonstrate that the model can integrate signal from a discrete-symbolic side channel without losing the LM's generative coherence.
2. **Frozen retriever / pretrained base** — only the cross-attention / chunk encoder is trained. This is exactly the recipe W3.5 uses: V2 bf16 CODI checkpoint as the frozen base, only the gate + Note Head are trained from scratch.
3. **RETRO-fitting (3% retraining)** — RETRO showed you can retrofit retrieval onto a pretrained transformer with minimal extra compute. W3.5's "init from CODI checkpoint, train gate + head only" is the same playbook.

## Method

**Chunking and retrieval:**
- Input split into chunks of m=64 tokens.
- Per chunk: compute BERT[CLS] embedding; SCaNN approximate-NN search; return k=2 neighbors.
- Each neighbor returns its 64-token continuation (for richer context).

**Chunked Cross-Attention (CCA):**
- Retrieved chunks encoded by a smaller bidirectional encoder.
- Decoder layers interleave standard self-attention with CCA layers (every nth layer).
- CCA queries are decoder hidden states; keys/values are the encoder's output for the retrieved chunks **for the current chunk only** (not the whole sequence).

**Frozen retriever:** BERT embedding model is **never updated** during RETRO training.

## Scale and results

- **Database**: up to 2 trillion tokens (1.7T training, 2T eval). Multi-trillion DB storage: 93TB chunk-level (vs 15TB token-level — chunk-level is the practical sweet spot).
- **Models**: 150M, 400M, 1.5B, 7.5B parameters.
- **Pile perplexity**: 7.5B RETRO **matches GPT-3 (175B) and Jurassic-1 (178B)** despite 25× fewer parameters.
- **RETRO-fitting**: existing pretrained transformers retrofitted with ~3% additional pretraining tokens; backward-compatible (works with retrieval disabled).
- **Retrieval latency**: ~10ms per query (SCaNN).

## Failure modes / limitations

- **Wikipedia-adjacent skew**: gains are largest on Wikipedia-adjacent tasks (Wikitext-103, factoid QA); modest on synthetic-summary tasks.
- **Test-set leakage**: paper carefully analyzes via longest-common-substring; RETRO does some quasi-memorization that overstates "real" generalization. Filtering required for honest eval.
- **Frozen retriever** = ceiling: BERT[CLS] is not a great retrieval embedder; results plateau because the retriever doesn't learn from LM signal.
- **No long-range coherence**: each chunk's retrieval is independent; no mechanism to keep retrieved context consistent across chunks.

## Direct mapping to W3.5 Latent Scratchpad

**BORROW: the RETRO-fitting recipe (frozen base + lightweight new heads).** W3.5 already follows this — start from V2 bf16 CODI checkpoint, train only LoRA + gate + Note Head, freeze base embeddings. RETRO's empirical "3% extra data is enough" is encouraging for W3.5's training budget. **BORROW: frozen retriever framing** — the LM's lm_head should be tied to the Note Head and frozen during scratchpad-only training stages. **IGNORE: external database, retrieval index, chunked cross-attention** — W3.5's scratchpad is in-context, not retrieval-based; RETRO's database scale is irrelevant to the design.

## Citation links to chase

- [[Memorizing Transformers]] — kNN-memory cousin (smaller scale, in-context memory).
- [[Compressive Transformer]] — same author (Rae) different memory design.
- [[Latent Scratchpad Architecture]] — concept page.
