#!/usr/bin/env bash
set -euo pipefail

# bump-version.sh — Update plugin.json version and create a git tag.
#
# Usage:
#   ./scripts/bump-version.sh <plugin-name> <new-version>
#   ./scripts/bump-version.sh trmm-expert 1.1.0
#
# What it does:
#   1. Updates "version" in plugins/<name>/.claude-plugin/plugin.json
#   2. Commits the change
#   3. Creates an annotated tag: <plugin-name>-v<version>
#   4. Prints the push command (does NOT push automatically)

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <plugin-name> <new-version>"
  echo "Example: $0 trmm-expert 1.1.0"
  exit 1
fi

PLUGIN_NAME="$1"
NEW_VERSION="$2"
PLUGIN_JSON="plugins/${PLUGIN_NAME}/.claude-plugin/plugin.json"

# Validate plugin exists
if [[ ! -f "$PLUGIN_JSON" ]]; then
  echo "Error: $PLUGIN_JSON not found"
  exit 1
fi

# Validate version format (semver: X.Y.Z)
if ! [[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: Version must be semver format (e.g., 1.2.3)"
  exit 1
fi

# Read current version
CURRENT_VERSION=$(python3 -c "import json; print(json.load(open('$PLUGIN_JSON'))['version'])")
echo "Plugin:  $PLUGIN_NAME"
echo "Current: $CURRENT_VERSION"
echo "New:     $NEW_VERSION"

if [[ "$CURRENT_VERSION" == "$NEW_VERSION" ]]; then
  echo "Error: Version is already $NEW_VERSION"
  exit 1
fi

# Update plugin.json
python3 -c "
import json
with open('$PLUGIN_JSON', 'r') as f:
    data = json.load(f)
data['version'] = '$NEW_VERSION'
with open('$PLUGIN_JSON', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
"

echo "Updated $PLUGIN_JSON"

# Commit and tag
TAG="${PLUGIN_NAME}-v${NEW_VERSION}"
git add "$PLUGIN_JSON"
git commit -m "chore(${PLUGIN_NAME}): bump version to ${NEW_VERSION}"
git tag -a "$TAG" -m "${PLUGIN_NAME} v${NEW_VERSION}"

echo ""
echo "Done. Created commit and tag: $TAG"
echo ""
echo "To push:"
echo "  git push && git push origin $TAG"
