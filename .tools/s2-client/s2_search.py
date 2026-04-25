"""Minimum-viable Semantic Scholar API client for autoresearch A/B test.

Usage:
    python s2_search.py search "<query>" [limit]
    python s2_search.py paper <paperId>

Reads S2_API_KEY from sibling .env file (gitignored).
"""
import json
import os
import sys
from pathlib import Path

import urllib.request
import urllib.parse


def _load_env():
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
DEFAULT_FIELDS = ",".join([
    "title", "authors.name", "year", "venue", "abstract", "tldr",
    "citationCount", "influentialCitationCount", "url", "externalIds",
    "openAccessPdf",
])


def _get(path: str, params: dict) -> dict:
    qs = urllib.parse.urlencode(params)
    url = f"{BASE}{path}?{qs}"
    headers = {"User-Agent": "wiki-autoresearch/0.1"}
    if API_KEY:
        headers["x-api-key"] = API_KEY
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def search(query: str, limit: int = 10) -> dict:
    return _get("/paper/search", {"query": query, "limit": limit, "fields": DEFAULT_FIELDS})


def paper(paper_id: str) -> dict:
    fields = DEFAULT_FIELDS + ",references.title,references.year,references.influentialCitationCount,citations.title,citations.year,citations.influentialCitationCount"
    return _get(f"/paper/{paper_id}", {"fields": fields})


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    cmd = sys.argv[1]
    arg = sys.argv[2]
    if cmd == "search":
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        out = search(arg, limit)
    elif cmd == "paper":
        out = paper(arg)
    else:
        print(__doc__)
        sys.exit(2)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
