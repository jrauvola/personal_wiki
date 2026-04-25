---
type: meta
title: "Frontmatter Schema"
updated: 2026-04-22
status: evergreen
---

# Frontmatter Schema — Authoritative Reference

This file defines the YAML frontmatter schema for every page type in this vault. Extends the `claude-obsidian` plugin's default schema with project-tiered relevance.

When `wiki-ingest`, `wiki-autoreview`, `wiki-lint`, or any other skill creates/edits a page, it MUST conform to this schema.

---

## Universal fields (every page)

```yaml
---
type: <source|entity|concept|domain|comparison|question|overview|meta>
title: "Human-Readable Title"
created: 2026-04-22
updated: 2026-04-22
tags:
  - <domain-tag>
  - <type-tag>
status: <seed|developing|mature|evergreen|archived>
related:
  - "[[Other Page]]"
sources:
  - "[[.raw/papers/source-file.md]]"

# Project-tiered relevance (CUSTOM — vault-specific)
projects:
  - slug: "<project-slug>"       # MUST match a slug in meta/projects/REGISTRY.md
    relevance: primary            # primary | secondary | reference | not-applicable
    why: "one-line rationale tying this page to the project's Primary/Secondary interests"

# Autoreview tracking (CUSTOM)
last_reviewed: 2026-04-22         # YYYY-MM-DD; managed by wiki-autoreview
reviewed_by: autoreview           # or <human-name> for manual overrides
---
```

---

## Type-specific extensions

### source (paper)

When `type: source` and `source_type: paper`:

```yaml
source_type: paper
arxiv_id: "2602.10229"
venue: "arXiv"                    # or conference / journal name
date_published: 2026-02-10
authors:
  - "Weihao Liu"
  - "Dehai Min"
  - "Lu Cheng"
url: "https://arxiv.org/abs/2602.10229"
code_repo: "https://github.com/NeosKnight233/Latent-Thoughts-Tuning"  # null if none
has_weights: false                # checkpoints released on HF Hub?
status: triaged | read | integrated | archived
confidence: high | medium | low
key_claims:
  - "Untied input/output embeddings cause geometric mismatch → feature collapse"
  - "CPF interpolation anchors latent trajectory to discrete token manifold"
  - "Three-stage curriculum is load-bearing; skipping stages collapses the model"
```

**`key_claims` is load-bearing** — `wiki-autoreview`'s contradiction pass cross-references these across all source pages. Extract 3-6 verbatim claims per paper, phrased as testable propositions.

### source (article / post / video / podcast / transcript)

```yaml
source_type: article | post | video | podcast | transcript | book
author: "..."
date_published: YYYY-MM-DD
url: "..."
confidence: high | medium | low
key_claims: [...]                 # same load-bearing role as for papers
```

### entity

```yaml
entity_type: person | organization | product | repository | place | dataset
role: "First author, Latent Thoughts Tuning"
first_mentioned: "[[source-page-name]]"
```

### concept

```yaml
complexity: basic | intermediate | advanced
domain: latent-reasoning | interpretability | architecture | curriculum | ...
aliases:
  - "CPF"
  - "Context Prediction Fusion"
```

### comparison

```yaml
subjects:
  - "[[Thing A]]"
  - "[[Thing B]]"
dimensions:
  - "what they optimize"
  - "compute overhead"
  - "engineering cost"
verdict: "one-sentence summary of when to use which"
```

### question

```yaml
question: "Does CPF help at scales below 8B?"
answer_quality: draft | solid | definitive
```

### domain

```yaml
subdomain_of: "[[Parent Domain]]"
page_count: N
```

---

## Status values (custom)

| Value | Meaning |
|---|---|
| `seed` | Created but not yet fully read (only used transiently during batch ingest) |
| `triaged` | Read; tier assigned; not yet integrated into any experiment/writeup |
| `read` | Fully read; tier stable |
| `integrated` | Cited in an experiment, spec, or writeup |
| `mature` | Stable — unlikely to need re-review |
| `evergreen` | Reference material — structurally important |
| `archived` | Moved out of active vault (no active project touches it, or superseded) |

Transitions: `seed → triaged → read → integrated → mature → evergreen | archived`

---

## Tier values (custom)

| Value | Meaning | Usage |
|---|---|---|
| `primary` | Recipe/method we'd implement or directly cite | Top of project reading queue; read in depth |
| `secondary` | Partial signal: technique, ablation, or benchmark worth borrowing | Read when time permits |
| `reference` | Context-only: general framing, superseded method, or unrelated benchmark | Know it exists; don't re-read unless scope expands |
| `not-applicable` | No overlap with this project's concerns | Skip entirely for this project |

Be conservative. When in doubt, downgrade. Primary must stay signal-dense.

---

## Wikilink conventions

- Filename = human-readable Title Case with spaces: `Latent Thoughts Tuning.md`
- Wikilinks use exact filename (no extension): `[[Latent Thoughts Tuning]]`
- Aliases via frontmatter `aliases:` field; wikilinks work on aliases too.
- Folders lowercase-dashed: `wiki/meta/projects/`
- Tags lowercase-hierarchical: `#project/branch-d`, `#domain/architecture`
