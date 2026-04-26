"""Semantic Scholar API client for autoresearch-hybrid.

Patterns borrowed from ml-intern/agent/tools/papers_tool.py:
- Rate limiting (1 req/s for search, 10 req/s for others, only when authed)
- Retry on 429/5xx with backoff
- Cache with hashable key (path + sorted params)

Sync stdlib only (no httpx/asyncio). Disk-persistent cache.

Usage:
    python s2_search.py search "<query>" [limit]
    python s2_search.py paper <paper_id>
    python s2_search.py cited_by <paper_id> [limit]
    python s2_search.py cites <paper_id> [limit]
    python s2_search.py citation_graph <paper_id> [direction] [limit]
    python s2_search.py expand <id1,id2,...> [depth] [limit_per_node]
"""
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


# --- env loading ---
def _load_env() -> None:
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


_load_env()
API_KEY = os.environ.get("S2_API_KEY")
BASE = "https://api.semanticscholar.org/graph/v1"
TIMEOUT = 30


# --- rate-limit + cache state ---
_last_request: float = 0.0
_CACHE_DIR = Path(__file__).parent / ".cache"
_CACHE_DIR.mkdir(exist_ok=True)
_memory_cache: dict[str, dict] = {}


def _cache_key(path: str, params: dict | None) -> str:
    p = tuple(sorted((params or {}).items()))
    raw = f"{path}:{p}"
    return hashlib.sha1(raw.encode()).hexdigest()


def _cache_get(key: str) -> dict | None:
    if key in _memory_cache:
        return _memory_cache[key]
    path = _CACHE_DIR / f"{key}.json"
    if path.exists():
        try:
            data = json.loads(path.read_text())
            _memory_cache[key] = data
            return data
        except Exception:
            return None
    return None


def _cache_put(key: str, value: dict) -> None:
    _memory_cache[key] = value
    (_CACHE_DIR / f"{key}.json").write_text(json.dumps(value, ensure_ascii=False))


# --- HTTP with rate-limit + retry ---
def _request(path: str, params: dict | None = None) -> dict | None:
    """GET path with retries on 429/5xx and rate limiting (when authed)."""
    global _last_request
    key = _cache_key(path, params)
    cached = _cache_get(key)
    if cached is not None:
        return cached

    qs = urllib.parse.urlencode(params or {})
    url = f"{BASE}{path}?{qs}" if qs else f"{BASE}{path}"
    headers = {"User-Agent": "wiki-autoresearch/0.2"}
    if API_KEY:
        headers["x-api-key"] = API_KEY

    for attempt in range(3):
        if API_KEY:
            min_interval = 1.0 if "search" in path else 0.1
            elapsed = time.monotonic() - _last_request
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
        _last_request = time.monotonic()

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = json.loads(resp.read())
                _cache_put(key, data)
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(60)
                continue
            if e.code >= 500 and attempt < 2:
                time.sleep(3)
                continue
            return None
        except (urllib.error.URLError, TimeoutError):
            if attempt < 2:
                time.sleep(3)
                continue
            return None
    return None


# --- public API ---
DEFAULT_FIELDS = ",".join([
    "title", "authors.name", "year", "venue", "abstract", "tldr",
    "citationCount", "influentialCitationCount", "url", "externalIds",
    "openAccessPdf",
])

CITATION_FIELDS = (
    "title,externalIds,year,citationCount,influentialCitationCount,"
    "contexts,intents,isInfluential"
)


def search(query: str, limit: int = 10) -> dict | None:
    return _request("/paper/search", {"query": query, "limit": limit, "fields": DEFAULT_FIELDS})


def paper(paper_id: str) -> dict | None:
    fields = (
        DEFAULT_FIELDS
        + ",references.title,references.year,references.influentialCitationCount"
        + ",citations.title,citations.year,citations.influentialCitationCount"
    )
    return _request(f"/paper/{paper_id}", {"fields": fields})


def cited_by(paper_id: str, limit: int = 10) -> dict | None:
    """Top-k papers citing this one (S2's /citations endpoint)."""
    return _request(f"/paper/{paper_id}/citations", {"fields": CITATION_FIELDS, "limit": limit})


def cites(paper_id: str, limit: int = 10) -> dict | None:
    """Top-k papers this one cites (S2's /references endpoint)."""
    return _request(f"/paper/{paper_id}/references", {"fields": CITATION_FIELDS, "limit": limit})


def citation_graph(paper_id: str, direction: str = "both", limit: int = 10) -> dict:
    """Citation graph for paper_id.

    direction: "citations" (cited by) | "references" (cites) | "both"
    Returns {"anchor": paper_id, "citations": [...], "references": [...]}.
    Inner dicts have a "citingPaper" or "citedPaper" wrapper from S2.
    """
    out: dict = {"anchor": paper_id, "citations": [], "references": []}
    if direction in ("citations", "both"):
        c = cited_by(paper_id, limit)
        out["citations"] = (c or {}).get("data", [])
    if direction in ("references", "both"):
        r = cites(paper_id, limit)
        out["references"] = (r or {}).get("data", [])
    return out


def expand(paper_ids: list[str], depth: int = 2, limit_per_node: int = 5) -> dict:
    """Multi-hop traversal. Returns {hop_N: [paper, ...]}.

    hop_0 = paper_ids themselves (just the ID strings).
    hop_d (d >= 1) = newly discovered papers from citing+cited at hop d-1.
    Deduped by paperId/ArXiv across all hops.
    """
    seen: set[str] = set(paper_ids)
    hops: dict[int, list] = {0: list(paper_ids)}
    for d in range(1, depth + 1):
        next_hop: list = []
        for pid in hops[d - 1]:
            pid_str = pid if isinstance(pid, str) else (
                pid.get("paperId")
                or pid.get("externalIds", {}).get("ArXiv", "")
            )
            if not pid_str:
                continue
            g = citation_graph(pid_str, direction="both", limit=limit_per_node)
            for wrapper in (g["citations"] + g["references"]):
                p = wrapper.get("citingPaper") or wrapper.get("citedPaper") or wrapper
                neighbor_id = (
                    p.get("paperId")
                    or p.get("externalIds", {}).get("ArXiv", "")
                )
                if neighbor_id and neighbor_id not in seen:
                    seen.add(neighbor_id)
                    next_hop.append(p)
        hops[d] = next_hop
    return hops


# --- CLI ---
def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    cmd, arg = sys.argv[1], sys.argv[2]

    if cmd == "search":
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        out = search(arg, limit)
    elif cmd == "paper":
        out = paper(arg)
    elif cmd == "cited_by":
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        out = cited_by(arg, limit)
    elif cmd == "cites":
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        out = cites(arg, limit)
    elif cmd == "citation_graph":
        direction = sys.argv[3] if len(sys.argv) > 3 else "both"
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        out = citation_graph(arg, direction, limit)
    elif cmd == "expand":
        ids = arg.split(",")
        depth = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        limit_per_node = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        out = expand(ids, depth, limit_per_node)
    else:
        print(__doc__)
        sys.exit(2)

    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
