#!/usr/bin/env python3
"""
Read skill properties from SKILL.md frontmatter and output as JSON.

Usage:
    read_properties.py <skill-directory>
"""

import argparse
import json
import sys
from pathlib import Path

from quick_validate import find_skill_md, parse_frontmatter


def read_properties(skill_dir):
    """Read skill properties from SKILL.md frontmatter.

    Args:
        skill_dir: Path to the skill directory

    Returns:
        Dictionary of skill properties, omitting None/empty values
    """
    skill_dir = Path(skill_dir)
    skill_md = find_skill_md(skill_dir)

    if skill_md is None:
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")

    content = skill_md.read_text()
    metadata, _ = parse_frontmatter(content)

    # Build output dict, omitting None/empty values (matching models.py to_dict pattern)
    result = {}

    name = metadata.get("name")
    if name:
        result["name"] = str(name).strip()

    description = metadata.get("description")
    if description:
        result["description"] = str(description).strip()

    license_val = metadata.get("license")
    if license_val is not None:
        result["license"] = str(license_val)

    compatibility = metadata.get("compatibility")
    if compatibility is not None:
        result["compatibility"] = str(compatibility)

    allowed_tools = metadata.get("allowed-tools")
    if allowed_tools is not None:
        result["allowed-tools"] = str(allowed_tools)

    meta = metadata.get("metadata")
    if meta and isinstance(meta, dict):
        result["metadata"] = meta

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Read skill properties from SKILL.md and output as JSON."
    )
    parser.add_argument(
        "skill_dir",
        type=Path,
        metavar="SKILL_DIR",
        help="Path to the skill directory",
    )

    args = parser.parse_args()
    skill_dir = Path(args.skill_dir).resolve()

    if not skill_dir.is_dir():
        print(f"Error: Not a directory: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    try:
        props = read_properties(skill_dir)
        print(json.dumps(props, indent=2))
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
