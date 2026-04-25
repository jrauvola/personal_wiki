---
type: meta
title: "Ideas Index"
created: 2026-04-24
updated: 2026-04-24
tags:
  - meta
  - ideas
status: evergreen
---

# Ideas Index

Catalog of research ideas that surfaced during this project but aren't yet full plans — or that are "parked" as future work. Each idea page includes: (a) the idea in 1-2 paragraphs, (b) papers it's grounded in via wikilinks, (c) concepts involved, (d) mechanism if known, (e) current status, (f) next step when we return to it.

**Why this exists:** ideas get lost between sessions if not caught somewhere structural. The INDEX is the quick-scan; individual pages have the depth. When we decide to promote an idea to a plan, the grounding papers are already pre-wired for retrieval.

## Status legend

- **active** — currently under consideration, near-term candidate for plan
- **parked** — interesting, deferred to specific later milestone
- **future-work** — beyond current SPAR scope, noted for post-fellowship work
- **promoted-to-plan** — has a plan at `plans/*` (kept here for cross-link)
- **retired** — explored and rejected

## Maturity legend

- **raw** — one-sentence intuition, no mechanism specified
- **sketched** — mechanism written down, open implementation questions
- **planned** — full implementation plan exists at `plans/*`
- **in-progress** — coding agent has started
- **shipped** — empirical result filed

---

## Active

(none currently active — see Demoted / contingent below)

## Demoted / contingent (2026-04-25)

| Idea | Status | Activation conditions | Links |
|---|---|---|---|
| [[Latent Scratchpad]] | demoted-contingent | 4 pre-commit warnings unresolved + 3 simpler interventions must fail (Pre-Step #0 KV-norm, LT-Tuning Phase 0, W2.4b SIM-CoT) | `plans/wave3/W3.5_latent_scratchpad.md` |

## Parked (future milestone)

| Idea | Status | Maturity | Trigger |
|---|---|---|---|
| [[Manifold-Constrained Residual Stream (mHC)]] | parked | sketched | post-W4 / workable-larger-model phase |

## Future work (beyond current scope)

| Idea | Status | Maturity | Why deferred |
|---|---|---|---|
| [[Wasserstein OT on Latent CoT]] | future-work | raw | No prior art in corpus; ungrounded for a plan today |
| [[Per-Token Continuous Thought]] | future-work | raw | Quiet-STaR × COCONUT empty cell per genealogy |
| [[Continuous-Thought Pretraining]] | future-work | sketched | All COCONUT-family are fine-tuning only; W3.2 Pause-PT is partial swing |
| [[Dense Per-Step Latent Supervision]] | future-work | raw | Pfau 2024 flagged as required but uncovered |
| [[Cross-Precision Determinism Investigation]] | future-work | raw | V2 bf16 vs V2' fp32 unexplained — most reproducible unexplained finding |
| [[Autoresearch 2.0 — Math-Feasibility Gated Autoexperimenting]] | future-work | raw | Meta-branch proposed by user 2026-04-23; tooling-level |
| [[Attention Composite-Block Jacobian]] | future-work | raw | W2.3 targets per-projection; composite-block unexplored |
| [[MoCo-Style Cross-Batch InfoNCE]] | future-work | sketched | Batch <32 fallback for W2.2; swap in if W2.2 hits batch limits |
| [[Continuous-Solver Variable Compute]] | future-work | raw | Continuous-depth analogue of ACT; unused per genealogy |

## Retired

(empty — ideas explicitly retired are noted in the originating plan's "Kill criterion" section, not here)

---

## Promotion workflow

1. An idea starts as a paragraph in this INDEX + one-liner in the status table.
2. When it has mechanism specified and grounding clear, promote to individual page at `wiki/ideas/{slug}.md`.
3. When it passes a feasibility bar, promote to a full plan at `plans/*` (and update this INDEX row).
4. When the plan becomes a coding-agent task, promote status to "in-progress."
5. When empirical results land, promote to "shipped" and link the experiment scratchpad entry.

## Cross-referencing

Every idea page links to:
- **Sources** (papers in `wiki/sources/`) that ground the idea
- **Concepts** (in `wiki/concepts/`) that formalize the mechanism
- **Projects** (in `wiki/meta/projects/`) that would absorb the idea if promoted

This makes retrieval cheap when an idea matures — one grep surfaces all relevant papers without re-running the crawl.
