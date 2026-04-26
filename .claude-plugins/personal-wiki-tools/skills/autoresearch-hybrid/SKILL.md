---
name: autoresearch-hybrid
description: Hybrid autoresearch loop — WebSearch for keyword discovery, Semantic Scholar for citation-graph expansion. Routing rule was validated empirically; see wiki/projects/lpcvc-2026-track1/experiments/s2-vs-websearch-routing-rule.md. Triggers on "/autoresearch-hybrid <topic>".
argument-hint: <topic> [--project=<slug>]
allowed-tools: [Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash]
version: 0.1.0
---

# autoresearch-hybrid

Iterative autonomous research loop. Uses **WebSearch for keyword discovery** and **Semantic Scholar for citation-graph expansion**, per the codified routing rule from the A/B test ([[projects/lpcvc-2026-track1/experiments/s2-vs-websearch-routing-rule]]).

Files findings into the active project's wiki workspace surfaces. The wiki product is the deliverable — chat is just the interface.

---

## Active-project resolution

Before any filing, resolve the active project slug:

1. `--project=<slug>` argument if provided.
2. `.wiki-project` file in the current working directory (single line).
3. `/Users/jrauvola/Desktop/wiki/ACTIVE_PROJECT` file (single line).
4. If none resolve: STOP and ask the user which project this research is for. Do not file under default.

All filing goes under `/Users/jrauvola/Desktop/wiki/projects/<slug>/` for workspace surfaces and `/Users/jrauvola/Desktop/wiki/{sources,concepts,entities,questions,ideas,comparisons}/` for shared knowledge surfaces (with `projects: [{slug: <slug>, relevance: ...}]` in frontmatter).

## S2 client invocation

Citation-graph queries call the local S2 client via Bash:

```bash
python3 /Users/jrauvola/Desktop/wiki/.tools/s2-client/s2_search.py \
    citation_graph ARXIV:<id> both 8
```

Output is JSON `{"anchor", "citations": [...], "references": [...]}`. Each entry wraps a paper with `citingPaper` or `citedPaper`. The client caches responses on disk (`.cache/`), so re-running the same query is free.

For top-K-by-influence sorting (the API returns by date), sort client-side in the skill: `sorted(papers, key=lambda p: (p.get('influentialCitationCount') or 0, p.get('citationCount') or 0), reverse=True)[:k]`.

## Constraints (mirrors plugin's autoresearch program.md)

- Max search rounds per topic: **3**
- Max wiki pages created per session: **15**
- Max sources fetched per round: **5**
- Confidence labels on every claim: `high` (multiple authoritative sources), `medium` (single good source), `low` (single informal source / unverified)
- Mark sources older than 3 years as potentially stale

## Loop

```
Input: <topic> from $ARGUMENTS

Round 1 — Discovery via WebSearch
1. Decompose topic into 3-5 distinct angles
2. Per angle: 1-2 WebSearch queries
3. Extract URL list + snippets

Round 2 — Citation expansion via S2 (THIS IS THE KEY DIFFERENTIATOR)
4. From Round 1 URLs, extract arxiv IDs (regex: arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5}))
5. For top 3 arxiv hits (by web rank): Bash-call s2_search.py citation_graph ARXIV:<id> both 8
6. Sort each result set by influentialCitationCount + citationCount (client-side)
7. Pick top 2 unique neighbors per anchor that weren't in Round 1

Round 3 — Fetch + extract (5 sources max per program.md)
8. Merge Round 1 web URLs + Round 2 S2-discovered URLs
9. WebFetch top 5 by relevance + influence signal
10. Extract per source: key claims, entities, concepts, contradictions, open questions

Filing
11. Synthesize into pages per "Filing rules" below
12. Update active project's hot.md, log.md, index.md
13. Report to user

Stop after 3 rounds OR when 15-page budget hit OR when no new neighbors surface.
```

## Filing rules

Same shape as the plugin's `autoresearch` skill:

**Sources** → `/Users/jrauvola/Desktop/wiki/sources/<Title>.md`. Frontmatter: `type: source`, `source_type: paper|documentation|blog|...`, `arxiv_id`, `venue`, `date_published`, `authors`, `url`, `code_repo`, `has_weights`, `status: triaged|read|integrated|archived`, `confidence`, `key_claims` (3-6 testable propositions), `projects: [{slug: <active>, relevance: primary|secondary|reference|not-applicable, why: "..."}]`, `last_reviewed: YYYY-MM-DD`, `reviewed_by: autoresearch`.

**Concepts** → `/Users/jrauvola/Desktop/wiki/concepts/<Concept>.md`. Only create if substantive enough to stand alone. Update existing rather than duplicating.

**Entities** → `/Users/jrauvola/Desktop/wiki/entities/<Name>.md`. People, orgs, products, model families.

**Synthesis** → `/Users/jrauvola/Desktop/wiki/questions/Research - <Topic>.md`. Master synthesis. Sections: Overview · Top Findings (with source citations) · Key Entities · Key Concepts · Contradictions · Open Questions · Sources. Frontmatter `type: synthesis`, `related: [...]`, `sources: [...]`.

**Workspace updates:**
- Append entry to top of `projects/<slug>/log.md`: `## YYYY-MM-DD autoresearch-hybrid | <topic>` with rounds, sources found, pages created, key finding.
- Update `projects/<slug>/hot.md` (overwrite, keep under 500 words). Most recent context summary.
- Update `projects/<slug>/index.md` to list new pages under appropriate section.

## Source preference

- Prefer: arXiv, official GitHub repos, official product documentation, peer-reviewed venues.
- Skip as high-confidence: Reddit, social media, undated web pages, sources without their own citations.
- Treat LLM benchmark leaderboard claims as low confidence unless independently verified.
- Citation expansion via S2: weight by `influentialCitationCount` (S2's signal for "papers actually using this work" vs perfunctory mentions).

## Output style

- Declarative, present tense.
- Cite every non-obvious claim: `(Source: [[Page]])`.
- Short pages: under 200 lines. Split if longer.
- No hedging language ("it seems", "perhaps", "might be"). Flag uncertainty explicitly: `> [!gap] This claim needs verification.`

## Report to user

After filing:

```
autoresearch-hybrid complete: <topic>

Rounds: N | WebSearches: N | S2 citation queries: N | WebFetches: N | Pages created: N

Project: <slug>

Created:
  questions/Research - <topic>.md  (synthesis)
  sources/<...>.md
  concepts/<...>.md
  entities/<...>.md

Top findings:
  1. <one-liner with source citation>
  2. <one-liner with source citation>
  3. <one-liner with source citation>

S2-unique finds (papers WebSearch missed but citation graph surfaced):
  - <paper title> (cited by <anchor>)

Open questions filed: N

Hot cache + log + index updated for project <slug>.
```

## Examples

```
/autoresearch-hybrid "MobileCLIP2 INT8 deployment Hexagon NPU latency"
/autoresearch-hybrid "compositionality fine-tuning CLIP retrieval" --project=lpcvc-2026-track1
/autoresearch-hybrid "stability theorems for noisy recurrent networks" --project=spar-latent-reasoning
```

## Failure modes to handle

- **S2 returns 0 results:** continue with WebSearch-only. Note in synthesis "S2 returned no results for citation expansion."
- **arxiv ID extraction fails on all Round 1 hits:** skip Round 2, file synthesis from Round 1 only.
- **Active project unresolved:** STOP and ask. Do not silently file under default.
- **15-page cap hit mid-round:** file what you have, list what was skipped in synthesis Open Questions.
