# Personal Research Wiki — Claude Instructions

**Vault path:** `/Users/jrauvola/Desktop/wiki/`
**`.raw/` path:** `/Users/jrauvola/Desktop/wiki/.raw/` (gitignored; staging area for sources awaiting ingest)
**Git remote:** `jrauvola/personal_wiki` (private GitHub)
**Purpose:** Persistent, compounding knowledge base across multiple research projects, with tiered relevance per project.

This file extends the `claude-obsidian` plugin's default behavior for this vault. The plugin's skills must honor these customizations.

---

## Vault layout

```
/Users/jrauvola/Desktop/wiki/
├── CLAUDE.md                          # this file (vault-wide rules)
├── WORKSPACE.md                       # always-loaded project index
├── ACTIVE_PROJECT                     # one-line file: default project slug
│
├── projects/                          # PER-PROJECT workspace surfaces
│   └── <slug>/
│       ├── hot.md                     # recent context cache
│       ├── index.md                   # page index
│       ├── log.md                     # ingest + change log
│       ├── overview.md                # project overview
│       ├── experiments.md             # experiment tracker root
│       └── experiments/               # per-experiment notes
│
├── concepts/                          # SHARED knowledge surfaces (cross-project)
├── entities/                          # — pages declare per-project relevance
├── sources/                           #   via `projects:` frontmatter
├── ideas/
├── questions/
├── comparisons/
├── canvas/
│
├── meta/
│   ├── projects/
│   │   ├── REGISTRY.md                # project list + primary/secondary interests
│   │   └── <slug>.md                  # auto-generated dashboard per project
│   ├── seeds.yaml                     # paper-crawl input
│   ├── autoreview/changelog.md        # append-only sweep log
│   └── FRONTMATTER-SCHEMA.md
│
└── .raw/                              # gitignored ingest staging
```

**The split rule:**
- **Workspace surfaces** (hot, index, log, overview, experiments) live under `projects/<slug>/`. They swap when the active project swaps.
- **Knowledge surfaces** (concepts, entities, sources, ideas, questions, comparisons, canvas) live at vault root. A page can serve any number of projects via its `projects:` frontmatter.

## Active-project resolution

Skills determine which project's surfaces to load with this resolution order:

1. **`.wiki-project` file in the current working directory** — single line containing a project slug. Codebase-scoped override.
2. **`ACTIVE_PROJECT` file at vault root** — single line. Vault-wide default.
3. **Fallback** — warn and load no project-scoped surfaces.

Skills should also accept a `--project=<slug>` CLI override that wins over both files.

The redirect stubs at vault root (`hot.md`, `index.md`, `log.md`, `overview.md`, `experiments.md`) are temporary safety nets pointing at `projects/spar-latent-reasoning/`. Once the plugin reliably resolves via the rules above, the stubs can be deleted.

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

Project-specific execution state (training logs, monitor output, scratchpads) lives in the project's codebase, not the vault. For `spar-latent-reasoning` the canonical location is `/Users/jrauvola/Desktop/Latent_Reasoning_Project/research_findings/`. Wiki pages MAY cross-link to such artifacts via stubs, but never copy content across.

When a new project is added, document its execution-artifacts location in its `projects/<slug>/overview.md`, not here.

---

## Cross-project reference

Other Claude Code sessions may read this wiki for context. Recommended reading order:

1. [[WORKSPACE]] (project index)
2. `projects/<active-slug>/hot.md` (recent context cache)
3. `projects/<active-slug>/index.md`
4. [[meta/projects/REGISTRY]] (what every project actually cares about)
5. Individual source/concept pages as needed

The active slug comes from `.wiki-project` (cwd) → `ACTIVE_PROJECT` (vault root).

---

## Source of truth (spar-latent-reasoning project)

These references are project-specific and live in the latent reasoning codebase, not here:

- Spec: `/Users/jrauvola/Desktop/Latent_Reasoning_Project/docs/superpowers/specs/2026-04-22-paper-crawl-pipeline-design.md`
- Skill drafts: `/Users/jrauvola/Desktop/Latent_Reasoning_Project/docs/paper-crawl/skills/`
- Patches: `/Users/jrauvola/Desktop/Latent_Reasoning_Project/docs/paper-crawl/patches/`
