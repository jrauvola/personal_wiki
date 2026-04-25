---
type: meta
title: "Workspace"
updated: 2026-04-25
---

# Workspace

Top-level index of all projects this vault hosts. Always loaded by the `wiki` skill.

## Active project

The active project determines which `projects/<slug>/` workspace surfaces (hot, index, log, overview, experiments) get loaded by default.

**Resolution order:**
1. `.wiki-project` file in the current working directory (single line: project slug)
2. `ACTIVE_PROJECT` file at vault root (single line: project slug)
3. Fallback: warn and load no project-scoped surfaces

**To change the default:** write a slug to `/Users/jrauvola/Desktop/wiki/ACTIVE_PROJECT`, or drop a `.wiki-project` file in your project's codebase root.

---

## Projects

### spar-latent-reasoning

**Status:** evergreen
**Goal:** SPAR fellowship writeup — interpretability of continuous CoT; north-star: a workable larger latent reasoning model synthesizing V2 / SIM-CoT / LT-Tuning lessons.
**Codebase:** `/Users/jrauvola/Desktop/Latent_Reasoning_Project/`
**Workspace surfaces:**
- [[projects/spar-latent-reasoning/hot]] — recent context cache
- [[projects/spar-latent-reasoning/index]] — page index
- [[projects/spar-latent-reasoning/log]] — ingest + change log
- [[projects/spar-latent-reasoning/overview]] — project overview
- [[projects/spar-latent-reasoning/experiments]] — experiment tracker
**Sub-branches:** branch-a (Stable Qwen3 Scaling), branch-b (Min-Sufficient Detach), branch-c (Qwen3 Convergence), branch-d (LT-Tuning CPF on CODI). See [[meta/projects/REGISTRY]] for branch details.

---

## Shared (cross-project) surfaces

These live at the vault root and are not scoped to any single project. Pages declare relevance per project via the `projects:` frontmatter field — see [[meta/FRONTMATTER-SCHEMA]].

- `concepts/` — concepts, methods, mechanisms
- `entities/` — people, orgs, model families
- `sources/` — papers, URLs, transcripts (with `projects:` tier per project)
- `ideas/` — speculative directions
- `questions/` — open questions
- `comparisons/` — head-to-head analyses
- `canvas/` — visual layer (Obsidian canvas files)
- `meta/` — registry, schema, autoreview reports

---

## Adding a new project

1. Pick a slug (kebab-case, e.g. `alignment-faking-organism`).
2. Append a section to [[meta/projects/REGISTRY]] with status, goal, primary/secondary/reference interests.
3. `mkdir projects/<slug>` and scaffold empty `hot.md`, `index.md`, `log.md`, `overview.md`, `experiments.md`.
4. Add the project's codebase path here under "Projects".
5. Drop a `.wiki-project` file in that codebase containing the slug.
6. Commit + push.
