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


_NAME_FALLBACK_FIELDS = ("name", "plan_name", "product_name", "title", "provider")


def get_item_name(data: dict, fallback: str = "(unnamed)") -> str:
    for field in _NAME_FALLBACK_FIELDS:
        value = lookup(data, field)
        if value and isinstance(value, (str, int, float)):
            text = str(value).strip()
            if text and _UNCERTAIN_MARKER not in text:
                return text
    return fallback


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


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

HTML_STYLE = """
:root { --fg: #1a1f24; --muted: #5a6470; --accent: #1f6feb; --border: #d4d8dd;
        --bg: #fff; --code-bg: #f4f6f8; --uncertain: #b16500; }
* { box-sizing: border-box; }
body { font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
       color: var(--fg); background: var(--bg); max-width: 980px;
       margin: 2rem auto; padding: 0 1.5rem; }
h1 { font-size: 1.9rem; margin: 0 0 .25rem; }
h2 { font-size: 1.4rem; margin: 2rem 0 .5rem; padding-bottom: .25rem;
     border-bottom: 1px solid var(--border); }
h3 { font-size: 1.1rem; margin: 1.25rem 0 .4rem; color: var(--accent); }
.subtitle { color: var(--muted); margin-bottom: 2rem; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
ul { padding-left: 1.4rem; }
li { margin: .25rem 0; }
strong.field { color: var(--fg); }
code, pre { background: var(--code-bg); border-radius: 4px; padding: .1rem .3rem;
            font: 0.93em ui-monospace, "SF Mono", Menlo, Consolas, monospace; }
table.toc { width: 100%; border-collapse: collapse; margin: 1rem 0; }
table.toc th, table.toc td { padding: .5rem .6rem; border-bottom: 1px solid var(--border);
                             text-align: left; vertical-align: top; font-size: .94rem; }
table.toc th { background: var(--code-bg); font-weight: 600; }
table.toc td.num { width: 2rem; color: var(--muted); }
.uncertain-list { color: var(--uncertain); }
.uncertain-list li::marker { content: "⚠ "; }
.long { line-height: 1.5; }
""".strip()


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def format_value_html(value: object, indent: int = 0) -> str:
    """Render a JSON value as HTML-friendly inline content."""
    if isinstance(value, list):
        if not value:
            return "<em>(empty)</em>"
        if all(isinstance(item, dict) for item in value):
            return "<br>".join(
                " | ".join(
                    f"{escape_html(str(k))}: {format_value_html(v, indent + 1)}"
                    for k, v in item.items()
                )
                for item in value
            )
        joined = ", ".join(escape_html(str(item)) for item in value)
        if len(joined) > _LONG_STRING_THRESHOLD:
            return "<ul>" + "".join(f"<li>{escape_html(str(item))}</li>" for item in value) + "</ul>"
        return joined
    if isinstance(value, dict):
        if not value:
            return "<em>(empty)</em>"
        parts = [
            f"<strong>{escape_html(str(k))}</strong>: {format_value_html(v, indent + 1)}"
            for k, v in value.items()
        ]
        joined = "; ".join(parts)
        if len(joined) > _LONG_STRING_THRESHOLD:
            return "<br>".join(parts)
        return joined
    text = str(value).strip()
    escaped = escape_html(text)
    if len(text) > _LONG_STRING_THRESHOLD:
        return escaped.replace("\n", "<br>")
    return escaped


def render_toc_html(items: list[tuple[str, dict, list]], toc_fields: list[str]) -> list[str]:
    lines = ["<h2>Table of Contents</h2>"]
    if toc_fields:
        header_cells = "".join(f"<th>{escape_html(f)}</th>" for f in toc_fields)
        lines.append('<table class="toc">')
        lines.append(f"<thead><tr><th>#</th><th>Item</th>{header_cells}</tr></thead>")
        lines.append("<tbody>")
        for idx, (name, data, uncertain_list) in enumerate(items, start=1):
            anchor = slug(name)
            row_cells = [f'<td class="num">{idx}</td>', f'<td><a href="#{anchor}">{escape_html(name)}</a></td>']
            for field in toc_fields:
                val = lookup(data, field)
                if is_uncertain(val, field, uncertain_list):
                    row_cells.append("<td><em>—</em></td>")
                else:
                    row_cells.append(f"<td>{format_value_html(val)}</td>")
            lines.append(f"<tr>{''.join(row_cells)}</tr>")
        lines.append("</tbody></table>")
    else:
        lines.append("<ol>")
        for name, _, _ in items:
            anchor = slug(name)
            lines.append(f'  <li><a href="#{anchor}">{escape_html(name)}</a></li>')
        lines.append("</ol>")
    return lines


def render_item_html(
    name: str,
    data: dict,
    uncertain_list: list,
    categories: list[dict],
    defined_fields: set[str],
) -> list[str]:
    anchor = slug(name)
    lines = [f'<h2 id="{anchor}">{escape_html(name)}</h2>']
    for cat in categories:
        cat_lines = []
        for field in cat.get("fields", []):
            field_name = field["name"]
            val = lookup(data, field_name)
            if is_uncertain(val, field_name, uncertain_list):
                continue
            cat_lines.append(
                f'<li><strong class="field">{escape_html(field_name)}</strong>: '
                f"{format_value_html(val)}</li>"
            )
        if cat_lines:
            lines.append(f"<h3>{escape_html(cat['category'])}</h3>")
            lines.append("<ul>")
            lines.extend(cat_lines)
            lines.append("</ul>")
    extras = collect_extra_fields(data, defined_fields)
    if extras:
        extra_lines = []
        for k, v in extras.items():
            if is_uncertain(v, k, uncertain_list):
                continue
            extra_lines.append(
                f'<li><strong class="field">{escape_html(str(k))}</strong>: '
                f"{format_value_html(v)}</li>"
            )
        if extra_lines:
            lines.append("<h3>Other Info</h3><ul>")
            lines.extend(extra_lines)
            lines.append("</ul>")
    if uncertain_list:
        lines.append("<h3>Uncertain Fields</h3>")
        lines.append('<ul class="uncertain-list">')
        for f in uncertain_list:
            lines.append(f"  <li>{escape_html(str(f))}</li>")
        lines.append("</ul>")
    return lines


def render_html_document(
    title: str,
    items: list[tuple[str, dict, list]],
    categories: list[dict],
    defined_fields: set[str],
    toc_fields: list[str],
    results_dir_name: str,
) -> str:
    parts = [
        "<!doctype html>",
        '<html lang="en"><head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{escape_html(title)}</title>",
        f"<style>{HTML_STYLE}</style>",
        "</head><body>",
        f"<h1>{escape_html(title)}</h1>",
        f'<p class="subtitle">Generated from {len(items)} item(s) in <code>{escape_html(results_dir_name)}/</code>.</p>',
    ]
    parts.extend(render_toc_html(items, toc_fields))
    for name, data, uncertain_list in items:
        parts.extend(render_item_html(name, data, uncertain_list, categories, defined_fields))
    parts.append("</body></html>")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic-dir", required=True, help="Topic directory containing fields.yaml and results/")
    parser.add_argument("--results-dir", default="results", help="Subdirectory with per-item JSON (default: results)")
    parser.add_argument("--fields", default="fields.yaml", help="Field definitions file (default: fields.yaml)")
    parser.add_argument("--toc-fields", default="", help="Comma-separated field names to summarize in TOC")
    parser.add_argument("--output", default="report.md", help="Markdown output filename relative to topic-dir (used when format is md or both)")
    parser.add_argument("--html-output", default="report.html", help="HTML output filename relative to topic-dir (used when format is html or both)")
    parser.add_argument("--format", choices=("md", "html", "both"), default="both", help="Output format(s) to emit. Default: both")
    parser.add_argument("--title", default=None, help="Report title (default: derived from topic-dir name)")
    args = parser.parse_args()

    topic_dir = Path(args.topic_dir).resolve()
    fields_path = topic_dir / args.fields
    results_dir = topic_dir / args.results_dir

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
    written: list[Path] = []

    if args.format in ("md", "both"):
        md_path = topic_dir / args.output
        lines = [f"# {title}", "", f"_Generated from {len(items)} item(s) in `{results_dir.name}/`._", ""]
        lines.extend(render_toc(items, toc_fields))
        for name, data, uncertain_list in items:
            lines.extend(render_item(name, data, uncertain_list, categories, defined_fields))
        md_path.write_text("\n".join(lines), encoding="utf-8")
        written.append(md_path)

    if args.format in ("html", "both"):
        html_path = topic_dir / args.html_output
        html = render_html_document(title, items, categories, defined_fields, toc_fields, results_dir.name)
        html_path.write_text(html, encoding="utf-8")
        written.append(html_path)

    for p in written:
        print(f"[OK] Wrote {p} ({len(items)} items)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
