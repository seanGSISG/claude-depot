#!/usr/bin/env python3
"""
Self-contained documentation search for Claude Code docs.

Provides fuzzy path search and full-text content search across the locally
mirrored Anthropic documentation. Uses only Python stdlib (no dependencies).

Usage:
    python3 search-docs.py --search "hooks"             # Fuzzy path search
    python3 search-docs.py --search-content "mcp"        # Full-text content search
    python3 search-docs.py --list                        # List all topics
    python3 search-docs.py --status                      # Show install status

Environment:
    DOCS_PATH  Path to docs repo (default: ~/.claude-code-docs)
"""

import argparse
import json
import os
import sys
from difflib import get_close_matches
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DOCS_PATH = Path(os.environ.get("DOCS_PATH", Path.home() / ".claude-code-docs"))
MANIFEST_FILE = DOCS_PATH / "paths_manifest.json"
SEARCH_INDEX_FILE = DOCS_PATH / "docs" / ".search_index.json"

BASE_URL_CODE = "https://code.claude.com"
BASE_URL_PLATFORM = "https://platform.claude.com"

CLAUDE_CODE_CLI_PAGES = {
    "amazon-bedrock", "analytics", "checkpointing", "claude-code-on-the-web",
    "cli-reference", "common-workflows", "costs", "data-usage", "desktop",
    "devcontainer", "github-actions", "gitlab-ci-cd", "google-vertex-ai",
    "headless", "hooks", "hooks-guide", "iam", "interactive-mode", "jetbrains",
    "legal-and-compliance", "llm-gateway", "mcp", "memory", "microsoft-foundry",
    "model-config", "monitoring-usage", "network-config", "output-styles",
    "overview", "plugin-marketplaces", "plugins", "plugins-reference",
    "quickstart", "sandboxing", "security", "settings", "setup", "skills",
    "slash-commands", "statusline", "sub-agents", "terminal-config",
    "third-party-integrations", "troubleshooting", "vs-code",
}

CLAUDE_CODE_CLI_NESTED = {"sdk/migration-guide"}

CATEGORY_LABELS = {
    "claude_code": "Claude Code CLI",
    "api_reference": "Claude API",
    "core_documentation": "Claude Documentation",
    "prompt_library": "Prompt Library",
    "release_notes": "Release Notes",
    "resources": "Resources",
    "uncategorized": "Uncategorized",
}


def get_base_url_for_path(path: str) -> str:
    """Return the correct base URL for a documentation path."""
    if path.startswith("/docs/en/"):
        page_part = path[9:]
        if page_part in CLAUDE_CODE_CLI_PAGES or page_part in CLAUDE_CODE_CLI_NESTED:
            return BASE_URL_CODE
    return BASE_URL_PLATFORM


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_manifest() -> Dict:
    """Load paths manifest (cached)."""
    if not MANIFEST_FILE.exists():
        return {"categories": {}, "metadata": {}}
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_all_paths(manifest: Dict) -> List[str]:
    """Return flat list of all documented paths."""
    paths: List[str] = []
    for cat_paths in manifest.get("categories", {}).values():
        paths.extend(cat_paths)
    return paths


def get_category_for_path(path: str, manifest: Dict) -> Optional[str]:
    """Find the category a path belongs to."""
    for category, paths in manifest.get("categories", {}).items():
        if path in paths:
            return category
    # Try normalized form (/en/docs/claude-code/X -> /docs/en/X)
    if path.startswith("/en/docs/claude-code/"):
        normalized = path.replace("/en/docs/claude-code/", "/docs/en/")
        for category, paths in manifest.get("categories", {}).items():
            if normalized in paths:
                return category
    return None


def get_product_label(category: str, path: str) -> str:
    """Map internal category + path to a user-friendly product label."""
    if category == "api_reference" and "/docs/agent-sdk/" in path:
        return "Claude Agent SDK"
    return CATEGORY_LABELS.get(category, category.replace("_", " ").title())


# ---------------------------------------------------------------------------
# Path search (fuzzy)
# ---------------------------------------------------------------------------

def search_paths(query: str, manifest: Dict, max_results: int = 20) -> List[Tuple[str, float]]:
    """Fuzzy-search for paths matching *query*. Returns (path, score) pairs."""
    query_lower = query.lower()
    all_paths = get_all_paths(manifest)
    scored: List[Tuple[str, float]] = []

    for path in all_paths:
        path_lower = path.lower()
        score = 0.0

        if query_lower == path_lower:
            score = 100.0
        elif query_lower in path_lower:
            if path_lower.startswith(query_lower):
                score = 80.0
            elif query_lower in path_lower.split("/")[-1]:
                score = 70.0
            else:
                score = 60.0
        else:
            query_words = query_lower.replace("-", " ").split()
            path_words = path_lower.replace("/", " ").replace("-", " ").split()
            matches = sum(1 for w in query_words if w in path_words)
            if matches > 0:
                score = 40.0 * (matches / len(query_words))

        if score == 0:
            similarity = sum(1 for q, p in zip(query_lower, path_lower) if q == p) / max(
                len(query_lower), len(path_lower)
            )
            if similarity > 0.3:
                score = similarity * 30.0

        if score > 0:
            scored.append((path, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:max_results]


# ---------------------------------------------------------------------------
# Content search (full-text)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_search_index() -> Optional[Dict]:
    """Load the full-text search index (cached)."""
    if not SEARCH_INDEX_FILE.exists():
        return None
    try:
        with open(SEARCH_INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def search_content(query: str, index: Dict, max_results: int = 20) -> List[Dict]:
    """Search document content for *query*. Returns list of result dicts."""
    if not index or "index" not in index:
        return []

    query_lower = query.lower()
    query_words = set(query_lower.split())
    results: List[Dict] = []

    for path, doc in index["index"].items():
        score = 0
        title = doc.get("title", "").lower()
        keywords = doc.get("keywords", [])
        preview = doc.get("content_preview", "")

        if query_lower in title:
            score += 100
        keyword_matches = len(query_words & set(keywords))
        score += keyword_matches * 10
        if query_lower in preview.lower():
            score += 20
        for word in query_words:
            if word in keywords:
                score += 5

        if score > 0:
            results.append({
                "path": path,
                "title": doc.get("title", "Untitled"),
                "score": score,
                "preview": preview,
                "file": doc.get("file_path", ""),
                "keywords": keywords[:5],
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def print_path_results(results: List[Tuple[str, float]], query: str, manifest: Dict):
    """Print fuzzy path search results with product context."""
    if not results:
        print(f"No results found for: '{query}'")
        # Suggest alternatives
        suggestions = get_close_matches(query, get_all_paths(manifest), n=5, cutoff=0.4)
        if suggestions:
            print("\nDid you mean:")
            for s in suggestions:
                print(f"  {s}")
        return

    # Collect product counts
    product_counts: Dict[str, int] = {}
    enriched = []
    for path, score in results:
        category = get_category_for_path(path, manifest)
        product = get_product_label(category, path) if category else "Unknown"
        product_counts[product] = product_counts.get(product, 0) + 1
        enriched.append((path, score, product))

    print(f"Found {len(results)} results for: '{query}'\n")

    # Product summary
    if len(product_counts) > 1:
        print("Products:", ", ".join(f"{p} ({c})" for p, c in product_counts.items()))
        print()

    for i, (path, score, product) in enumerate(enriched, 1):
        stars = "***" if score >= 80 else ("**" if score >= 60 else "*")
        base_url = get_base_url_for_path(path)
        print(f"{i:2d}. [{stars}] {path}")
        print(f"    Product: {product}  |  Score: {score:.1f}")
        print(f"    URL: {base_url}{path}")
        print()


def print_content_results(results: List[Dict], query: str, manifest: Dict):
    """Print content search results as JSON with product context."""
    enriched = []
    product_counts: Dict[str, int] = {}

    for r in results:
        path = r.get("path", "")
        category = get_category_for_path(path, manifest)
        product = get_product_label(category, path) if category else "Unknown"
        product_counts[product] = product_counts.get(product, 0) + 1
        enriched.append({
            "path": path,
            "title": r.get("title", "Untitled"),
            "category": category,
            "product": product,
            "score": r.get("score", 0),
            "preview": r.get("preview", "")[:150],
            "keywords": r.get("keywords", [])[:5],
            "file": r.get("file", ""),
        })

    output = {
        "query": query,
        "total_results": len(enriched),
        "results": enriched,
        "product_summary": product_counts,
        "unique_products": len(product_counts),
    }
    print(json.dumps(output, indent=2))


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_search(query: str):
    """Run fuzzy path search."""
    manifest = load_manifest()
    results = search_paths(query, manifest)
    print_path_results(results, query, manifest)


def cmd_search_content(query: str):
    """Run full-text content search."""
    index = load_search_index()
    if index is None:
        print("Search index not available.", file=sys.stderr)
        print("Rebuild with: cd ~/.claude-code-docs && python3 scripts/build_search_index.py", file=sys.stderr)
        sys.exit(1)
    manifest = load_manifest()
    results = search_content(query, index)
    print_content_results(results, query, manifest)


def cmd_list():
    """List all available documentation topics."""
    docs_dir = DOCS_PATH / "docs"
    if not docs_dir.exists():
        print("Documentation directory not found.", file=sys.stderr)
        sys.exit(1)
    files = sorted(p.stem for p in docs_dir.glob("*.md") if p.name != ".search_index.json")
    print(f"Available documentation files ({len(files)}):\n")
    for f in files:
        print(f"  {f}")


def cmd_status():
    """Show installation status."""
    print("Claude Code Docs - Installation Status")
    print("=" * 40)
    print(f"Location: {DOCS_PATH}")
    print(f"Installed: {'Yes' if DOCS_PATH.exists() else 'No'}")

    if not DOCS_PATH.exists():
        sys.exit(1)

    docs_dir = DOCS_PATH / "docs"
    doc_count = len(list(docs_dir.glob("*.md"))) if docs_dir.exists() else 0
    print(f"Documentation files: {doc_count}")

    manifest = load_manifest()
    total = manifest.get("metadata", {}).get("total_paths", 0)
    print(f"Manifest paths: {total}")

    cats = manifest.get("categories", {})
    if cats:
        print(f"Categories: {len(cats)}")
        for cat, paths in cats.items():
            label = CATEGORY_LABELS.get(cat, cat)
            print(f"  {label}: {len(paths)} paths")

    index = load_search_index()
    if index:
        print(f"Search index: {index.get('indexed_files', '?')} files indexed")
    else:
        print("Search index: not built")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Search Claude Code documentation"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--search", metavar="QUERY", help="Fuzzy path search")
    group.add_argument("--search-content", metavar="QUERY", help="Full-text content search")
    group.add_argument("--list", action="store_true", help="List all documentation topics")
    group.add_argument("--status", action="store_true", help="Show installation status")

    args = parser.parse_args()

    if args.search:
        cmd_search(args.search)
    elif args.search_content:
        cmd_search_content(args.search_content)
    elif args.list:
        cmd_list()
    elif args.status:
        cmd_status()


if __name__ == "__main__":
    main()
