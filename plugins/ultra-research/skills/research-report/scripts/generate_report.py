#!/usr/bin/env python3
"""
Convert per-item JSON research results into a single markdown report.

Reads:
  - <topic-dir>/fields.yaml  (field categories + definitions)
  - <topic-dir>/<output-dir>/*.json  (one per researched item)

Writes:
  - <topic-dir>/<output>  (the markdown report)

The script is invoked by the research-report skill. It is intentionally standalone
so that the same logic runs every time (no drift from per-run regeneration).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

# Bidirectional mapping: canonical category name -> list of variant keys that
# may appear as nested-dict keys in JSON or as `category:` strings in fields.yaml.
# Kept in sync with skills/research-en/research/scripts/validate_json.py.
CATEGORY_MAPPING = {
    "Basic Info": ["basic_info", "Basic Info"],
    "Technical Features": ["technical_features", "technical_characteristics", "Technical Features"],
    "Performance Metrics": ["performance_metrics", "performance", "Performance Metrics"],
    "Milestone Significance": ["milestone_significance", "milestones", "Milestone Significance"],
    "Business Info": ["business_info", "commercial_info", "Business Info"],
    "Competition & Ecosystem": ["competition_ecosystem", "competition", "Competition & Ecosystem"],
    "History": ["history", "History"],
    "Market Positioning": ["market_positioning", "market", "Market Positioning"],
}

_SKIP_KEYS = {"_source_file", "uncertain"}
_NESTED_KEYS = {k for variants in CATEGORY_MAPPING.values() for k in variants}
_UNCERTAIN_MARKER = "[uncertain]"
_LONG_STRING_THRESHOLD = 100


def slug(text: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")


def load_fields(fields_path: Path) -> tuple[list[dict], dict[str, str]]:
    """Return (category_list, field-to-category map).

    category_list preserves fields.yaml ordering: each entry is
    {"category": str, "fields": [{"name": str, "description": str, ...}, ...]}
    """
    with fields_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    categories = data.get("field_categories", [])
    field_to_cat = {
        field["name"]: cat["category"]
        for cat in categories
        for field in cat.get("fields", [])
    }
    return categories, field_to_cat


def lookup(data: dict, field_name: str) -> object:
    """Find a field value across flat or nested-by-category JSON structures."""
    if field_name in data:
        return data[field_name]
    for variants in CATEGORY_MAPPING.values():
        for k in variants:
            if k in data and isinstance(data[k], dict) and field_name in data[k]:
                return data[k][field_name]
    for v in data.values():
        if isinstance(v, dict) and field_name in v:
            return v[field_name]
    return None


def is_uncertain(value: object, field_name: str, uncertain_list: list) -> bool:
    if field_name in uncertain_list:
        return True
    if value is None:
        return True
    if isinstance(value, str):
        s = value.strip()
        return s == "" or _UNCERTAIN_MARKER in s
    return False


def format_value(value: object, indent: int = 0) -> str:
    """Render a JSON value as a markdown-friendly string."""
    pad = "  " * indent
    if isinstance(value, list):
        if not value:
            return "_(empty)_"
        if all(isinstance(item, dict) for item in value):
            lines = []
            for item in value:
                parts = [f"{k}: {format_value(v, indent + 1)}" for k, v in item.items()]
                lines.append(" | ".join(parts))
            return "<br>".join(lines)
        joined = ", ".join(str(item) for item in value)
        if len(joined) > _LONG_STRING_THRESHOLD:
            return "<br>".join(f"- {item}" for item in value)
        return joined
    if isinstance(value, dict):
        if not value:
            return "_(empty)_"
        parts = [f"**{k}**: {format_value(v, indent + 1)}" for k, v in value.items()]
        joined = "; ".join(parts)
        if len(joined) > _LONG_STRING_THRESHOLD:
            return "<br>".join(parts)
        return joined
    text = str(value).strip()
    if len(text) > _LONG_STRING_THRESHOLD:
        return text.replace("\n", "<br>")
    return text


def collect_extra_fields(data: dict, defined_fields: set[str]) -> dict[str, object]:
    """Find JSON fields not in fields.yaml, excluding internal/category keys."""
    extras: dict[str, object] = {}

    def walk(obj: object) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in _SKIP_KEYS or k in _NESTED_KEYS or k in defined_fields:
                    if k in _NESTED_KEYS and isinstance(v, dict):
                        walk(v)
                    continue
                extras[k] = v

    walk(data)
    return extras


def get_item_name(data: dict) -> str:
    name = lookup(data, "name")
    return str(name).strip() if name else "(unnamed)"


def render_toc(items: list[tuple[str, dict, list]], toc_fields: list[str]) -> list[str]:
    lines = ["## Table of Contents", ""]
    for idx, (name, data, uncertain_list) in enumerate(items, start=1):
        anchor = slug(name)
        summary_bits = []
        for field in toc_fields:
            val = lookup(data, field)
            if not is_uncertain(val, field, uncertain_list):
                summary_bits.append(f"{field}: {format_value(val)}")
        suffix = f" - {' | '.join(summary_bits)}" if summary_bits else ""
        lines.append(f"{idx}. [{name}](#{anchor}){suffix}")
    lines.append("")
    return lines


def render_item(
    name: str,
    data: dict,
    uncertain_list: list,
    categories: list[dict],
    defined_fields: set[str],
) -> list[str]:
    lines = [f"## {name}", ""]
    for cat in categories:
        cat_name = cat["category"]
        cat_lines = []
        for field in cat.get("fields", []):
            field_name = field["name"]
            val = lookup(data, field_name)
            if is_uncertain(val, field_name, uncertain_list):
                continue
            cat_lines.append(f"- **{field_name}**: {format_value(val)}")
        if cat_lines:
            lines.append(f"### {cat_name}")
            lines.extend(cat_lines)
            lines.append("")
    extras = collect_extra_fields(data, defined_fields)
    if extras:
        lines.append("### Other Info")
        for k, v in extras.items():
            if is_uncertain(v, k, uncertain_list):
                continue
            lines.append(f"- **{k}**: {format_value(v)}")
        lines.append("")
    if uncertain_list:
        lines.append("### Uncertain Fields")
        for f in uncertain_list:
            lines.append(f"- {f}")
        lines.append("")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic-dir", required=True, help="Topic directory containing fields.yaml and results/")
    parser.add_argument("--results-dir", default="results", help="Subdirectory with per-item JSON (default: results)")
    parser.add_argument("--fields", default="fields.yaml", help="Field definitions file (default: fields.yaml)")
    parser.add_argument("--toc-fields", default="", help="Comma-separated field names to summarize in TOC")
    parser.add_argument("--output", default="report.md", help="Output markdown filename relative to topic-dir")
    parser.add_argument("--title", default=None, help="Report title (default: derived from topic-dir name)")
    args = parser.parse_args()

    topic_dir = Path(args.topic_dir).resolve()
    fields_path = topic_dir / args.fields
    results_dir = topic_dir / args.results_dir
    output_path = topic_dir / args.output

    if not fields_path.exists():
        print(f"[ERROR] fields.yaml not found: {fields_path}", file=sys.stderr)
        return 1
    if not results_dir.exists():
        print(f"[ERROR] results dir not found: {results_dir}", file=sys.stderr)
        return 1

    categories, field_to_cat = load_fields(fields_path)
    defined_fields = set(field_to_cat.keys())
    toc_fields = [f.strip() for f in args.toc_fields.split(",") if f.strip()]

    items: list[tuple[str, dict, list]] = []
    for json_path in sorted(results_dir.glob("*.json")):
        with json_path.open(encoding="utf-8") as f:
            data = json.load(f)
        uncertain_list = data.get("uncertain", []) if isinstance(data.get("uncertain"), list) else []
        name = get_item_name(data)
        items.append((name, data, uncertain_list))

    if not items:
        print(f"[WARN] No JSON files in {results_dir}", file=sys.stderr)
        return 1

    title = args.title or topic_dir.name.replace("-", " ").replace("_", " ").title()
    lines = [f"# {title}", "", f"_Generated from {len(items)} item(s) in `{results_dir.name}/`._", ""]
    lines.extend(render_toc(items, toc_fields))
    for name, data, uncertain_list in items:
        lines.extend(render_item(name, data, uncertain_list, categories, defined_fields))

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote {output_path} ({len(items)} items)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
