# Latent Reasoning Research Wiki — Claude Instructions

**Vault path:** `/Users/jrauvola/Desktop/wiki/`
**`.raw/` path:** `/Users/jrauvola/Desktop/wiki/.raw/` (gitignored; staging area for sources awaiting ingest)
**Git remote:** `jrauvola/personal_wiki` (private GitHub)
**Project:** SPAR fellowship — Latent Reasoning Interpretability
**Purpose:** Persistent, compounding knowledge base of latent-reasoning literature, with tiered relevance against active investigation branches.

This file extends the `claude-obsidian` plugin's default behavior for this vault. The plugin's skills must honor these customizations.

---

## Mandatory customizations

### 1. Extended frontmatter schema

Every page MUST include the `projects:` field (in addition to the plugin's universal fields). See [[meta/FRONTMATTER-SCHEMA]] for the full schema.

```yaml
projects:
  - slug: "<project-slug>"       # must match a slug in meta/projects/REGISTRY.md
    relevance: primary            # primary | secondary | reference | not-applicable
    why: "one-line rationale tied to the project's Primary/Secondary interests"
```

Additional universal fields:
- `last_reviewed: YYYY-MM-DD` — managed by `wiki-autoreview`, never hand-edit.
- `reviewed_by: autoreview | <human-name>`

### 2. New source_type variant: `paper`

When ingesting an academic paper (arXiv / venue), use `source_type: paper` with these extra fields:

```yaml
source_type: paper
arxiv_id: "2602.10229"
venue: "arXiv"
date_published: 2026-02-10
authors: ["Weihao Liu", "Dehai Min", "Lu Cheng"]
url: "https://arxiv.org/abs/2602.10229"
code_repo: "https://github.com/NeosKnight233/Latent-Thoughts-Tuning"  # null if none
has_weights: false
status: triaged | read | integrated | archived
confidence: high | medium | low
key_claims:
  - "Verbatim claim 1 (testable proposition)"
  - "..."
```

`key_claims` is **load-bearing** for `wiki-autoreview`'s contradiction detection. Extract 3-6 claims per paper, phrased as testable propositions.

### 3. Project-tiered ingestion (extends plugin's `wiki-ingest` step 3)

After creating the source page, for every project in [[meta/projects/REGISTRY]]:
- Read the project's Primary + Secondary interest lines.
- Assess source against them:
  - **primary** — method/results match ≥1 Primary interest AND (has usable code OR implementable <2 weeks).
  - **secondary** — matches a Secondary interest, OR matches Primary but engineering cost is too high.
  - **reference** — context-only: general framing, superseded method, unrelated benchmark.
  - **not-applicable** — no overlap.
- Write a one-line rationale.
- Record in the source page's `projects:` frontmatter.

Discipline: **be conservative.** When in doubt, downgrade. Primary-tier papers are read in depth; that list must stay signal-dense.

### 4. Autoreview discipline

This vault uses a fully-autonomous review model. See [[meta/projects/REGISTRY]] discipline notes. Key rules for any ingest / review:

- **Full-ingest every paper.** No abstract-only/seed-only passes. Resource-not-constrained.
- **LLM assigns tiers**, not humans.
- **Autoreview re-grades** on schedule (see `wiki-autoreview` skill).
- Human attention only for flagged contradictions.

### 5. Execution artifacts stay out of the wiki

These live in `research_findings/` (at project root, parallel to `wiki/`) and MUST NOT be copied into the wiki (they are execution state, not knowledge):

- `../research_findings/experiment_scratchpad.md`
- `../research_findings/monitor_logs/`
- `../research_findings/dgrad_probe/`
- `../research_findings/SESSION_STATE_*.md`
- `../research_findings/checkpoint_*.md`
- `../research_findings/phase0_*/`

Wiki source pages MAY cross-link to them via `[[.raw/experiments/<name>]]` stubs, but never copy content across.

---

## Vault structure (non-standard additions)

Extensions beyond the plugin's default vault layout:

```
meta/
├── projects/
│   ├── REGISTRY.md              # project list + primary/secondary interests
│   ├── branch-a.md              # auto-generated dashboard (wiki-autoreview)
│   ├── branch-b.md
│   ├── branch-c.md
│   ├── branch-d.md
│   └── spar-latent-reasoning.md
├── seeds.yaml                   # paper-crawl input (arXiv IDs → projects)
├── autoreview/
│   └── changelog.md             # append-only sweep log
└── FRONTMATTER-SCHEMA.md        # authoritative schema reference
```

---

## Cross-project reference

Other Claude Code projects may read this wiki as context. Recommended reading order:

1. `wiki/hot.md` (500-word recent context)
2. `wiki/index.md`
3. `wiki/meta/projects/REGISTRY.md` (what we're actually working on)
4. Individual source/concept pages as needed

---

## Source of truth

- Spec: `../docs/superpowers/specs/2026-04-22-paper-crawl-pipeline-design.md`
- Skill drafts: `../docs/paper-crawl/skills/`
- Patches (for reference — superseded by this CLAUDE.md + meta/FRONTMATTER-SCHEMA.md): `../docs/paper-crawl/patches/`
