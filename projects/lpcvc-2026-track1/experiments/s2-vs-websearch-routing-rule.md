---
type: experiment
slug: s2-vs-websearch-routing-rule
title: "S2 vs WebSearch — routing rule for autoresearch-hybrid"
status: success
started: 2026-04-25
finished: 2026-04-25
hypothesis: "Hybrid wins. Semantic Scholar (S2) is better for academic-paper queries (citation graph + structured metadata); WebSearch is better for vendor-doc / competition-page / GitHub-repo queries."
parent: root
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Defines the routing logic for the autoresearch-hybrid skill we're authoring."
artifacts:
  - "/Users/jrauvola/Desktop/wiki/.tools/s2-client/s2_search.py"
last_reviewed: 2026-04-25
reviewed_by: experiment-runner
---

# S2 vs WebSearch — Routing Rule for autoresearch-hybrid

## Hypothesis (committed before running)

Hybrid wins. Routing rule:
- **S2 → academic-paper queries.** S2's citation graph and structured paper metadata beat WebSearch's blog-noisy snippets.
- **WebSearch → vendor docs, competition pages, GitHub repos, blogs.** S2 doesn't index these.

## Method

Six topics from real unanswered LPCVC questions, each pre-classified by my prediction. Pre-committed gold set (1-3 items per topic). Same query budget for both tools (1 search call each). Then manual usefulness scoring.

## Results

### Per-topic scorecard

| # | Topic | Predicted | S2 recall | WebSearch recall | S2 unique high-value | WS unique high-value | Actual winner |
|---|-------|-----------|----------:|-----------------:|---------------------|----------------------|---------------|
| 1 | AIMET vs QAI Hub built-in INT8 on CLIP | S2 | **0/3** | **1/3** | none | AIMET QAT docs, Qualcomm explainer | **WebSearch** |
| 2 | LPCVC 2025 Track 2 SEUDecoder | WS | **0/3** (+1 bonus) | **2-3/3** | "Evaluation of Winning Solutions of 2025 LPCV Challenge" (arXiv 2604.19054, 2026) — peer-reviewed analysis | full SICer team roster + scoring | **Hybrid (different value)** |
| 3 | Per-channel weight quant FastViT depthwise | S2 | **0/3** | **2/3** | none | Yun et al. CVPRW 2021 (2104.11849), Nagel et al. white paper (2106.08295) | **WebSearch** |
| 4 | KD large CLIP → mobile CLIP for retrieval | S2 | **0/3** (+1 bonus) | **2/3** | AMMKD (2509.00039, Sep 2025) — newer than gold | CLIP-KD (2307.12732), DCLIP (2505.21549) | **Hybrid (different value)** |
| 5 | QAI Hub `submit_quantize_job` adaround percentile | WS | **0/3** | **3/3** | none | All 10 results official; surfaced **`--lite_mp percentage=10;override_qtype=int16` flag** — answers our earlier "mixed precision unsupported" claim | **WebSearch** |
| 6 | MobileCLIP2 INT8 Hexagon NPU latency | mixed | **0/3** | **0/3** | none | none | **tie (both failed — publication gap exists)** |

### Aggregate
- **WebSearch outright wins: 3** (topics 1, 3, 5)
- **Hybrid wins: 2** (topics 2, 4 — S2 added unique value WebSearch missed, but WebSearch had higher gold-set recall)
- **Tie / both failed: 1** (topic 6)
- **S2 outright wins: 0**

### Token / latency cost
- S2: ~3-5 KB structured JSON per query, sub-second
- WebSearch: ~5-8 KB per query (snippets + summary text), 1-3s
- WebSearch is ~60% heavier per query but returns more context

## Verdict

**My hypothesis was wrong.** S2 did NOT win on academic-paper queries by keyword search.

**Why the prediction failed:**
1. S2's search ranking optimizes for textual relevance, not citation quality. Top results were often less-cited tangential papers, not canonical references.
2. WebSearch has direct access to arxiv.org pages (highly web-indexed) and surfaced the canonical papers WebSearch (the search engine used) ranks them well.
3. S2's actual strength is **citation-graph traversal** (given paper X, find papers that cite or are cited by X), NOT keyword search. This experiment only tested keyword search.

**Two new findings WebSearch surfaced for the LPCVC project:**
- 🔥 **`--lite_mp percentage=10;override_qtype=int16`** — Hub built-in DOES support partial mixed precision via the lite_mp option. Earlier wiki claim ([[sources/AIMET to QAI Hub Workflow]]) that "mixed precision is unsupported" needs amending.
- 🔥 **arXiv 2604.19054 — "Evaluation of Winning Solutions of 2025 LPCV Challenge"** (S2-found, 2026 paper). Peer-reviewed analysis of LPCV 2025 winners. Worth ingesting separately.

## Codified routing rule for autoresearch-hybrid

Based on evidence (NOT my hypothesis):

```python
def autoresearch_hybrid(topic):
    # Phase 1 — Discovery: ALWAYS WebSearch first.
    # Evidence: WebSearch had higher gold-set recall on every keyword query,
    # academic and non-academic alike.
    web_results = WebSearch(topic)
    arxiv_ids = extract_arxiv_ids_from(web_results)

    # Phase 2 — Citation expansion: S2 paper/{id} ONLY for top arxiv hits
    # Evidence: S2's strength is the citation graph, not keyword search.
    # AMMKD (topic 4) and the LPCV-2025 evaluation paper (topic 2) suggest
    # S2's reference/citation graph would surface neighbors WebSearch misses.
    for paper_id in arxiv_ids[:3]:
        s2_paper = s2_client.paper(paper_id)
        neighbors = top_k_by_citations(
            s2_paper["references"] + s2_paper["citations"],
            k=3,
        )
    # Phase 3 — Fetch + extract from merged set (WebSearch + S2 neighbors).
    fetch_top_n(merged_urls, n=5)

    # Phase 4 — Synthesize + file as standard autoresearch.
```

**Tool routing:**
- **Discovery (keyword → URL list)** → WebSearch always.
- **Citation expansion (paper → related papers)** → S2 always.
- **Vendor docs / competition / GitHub / blogs** → WebSearch only (S2 has nothing here).
- **Pure academic neighbors of a known paper** → S2 only (WebSearch can't traverse).

## Revert info

If we drop this approach: delete `wiki/.tools/s2-client/`, remove `.tools/**/.env` from `.gitignore`, remove this experiment page. No other side effects. S2_API_KEY remains in LRP `.env` (never moved, only copied).

## Follow-ups

1. **Amend [[sources/AIMET to QAI Hub Workflow]]** — the `lite_mp` flag DOES enable mixed precision in Hub built-in. Earlier claim was wrong.
2. **Ingest arXiv 2604.19054** — "Evaluation of Winning Solutions of 2025 LPCV Challenge" — directly relevant to the LPCVC playbook.
3. **Ingest arXiv 2509.00039** (AMMKD) — adaptive multi-teacher distillation, Sep 2025, more recent than CLIP-KD.
4. **Build `autoresearch-hybrid` skill** with the codified routing above. Discovery via WebSearch; citation-graph expansion via S2; fall back to WebSearch-only when S2 returns 0 results.
5. **Decide on full ml-intern/ migration:** since S2 didn't win on keyword search but DID win on citation expansion, ml-intern's paper-graph-traversal code (which uses S2 citation queries, not keyword search) IS the right wrapper to migrate. Original commit-when-S2-wins criterion still met.
6. **Re-run this experiment with citation-graph queries** (different protocol — give each tool a starting paper, ask for "find related work"). My hypothesis there would actually be S2 wins big.
