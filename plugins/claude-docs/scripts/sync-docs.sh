#!/bin/bash
set -euo pipefail

# Sync Claude Code documentation repo on session start.
# Clones ~/.claude-code-docs if missing, pulls if behind remote.
# Rebuilds search index after successful pull when Python 3.9+ is available.
# Silent on success (no stdout), only stderr on errors.
# Always exits 0 to avoid blocking session start.

DOCS_PATH="$HOME/.claude-code-docs"
REPO_URL="https://github.com/seanGSISG/claude-code-docs.git"
LOCK_FILE="$DOCS_PATH/.sync.lock"

# Ensure we never block session start
trap 'rm -f "$LOCK_FILE" 2>/dev/null; exit 0' EXIT

# Acquire lock (prevent concurrent syncs)
acquire_lock() {
    if [[ -f "$LOCK_FILE" ]]; then
        local lock_age
        lock_age=$(($(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || stat -f %m "$LOCK_FILE" 2>/dev/null || echo 0)))
        if [[ $lock_age -gt 60 ]]; then
            rm -f "$LOCK_FILE" 2>/dev/null || true
        else
            return 1
        fi
    fi
    echo $$ > "$LOCK_FILE" 2>/dev/null || true
    return 0
}

# Check if Python 3.9+ is available
has_python39() {
    command -v python3 &>/dev/null || return 1
    local ver
    ver=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
    local major minor
    major=$(echo "$ver" | cut -d. -f1)
    minor=$(echo "$ver" | cut -d. -f2)
    [[ "$major" -ge 3 && "$minor" -ge 9 ]]
}

# Rebuild search index if possible
rebuild_index() {
    if has_python39 && [[ -f "$DOCS_PATH/scripts/build_search_index.py" ]]; then
        (cd "$DOCS_PATH" && python3 scripts/build_search_index.py) >/dev/null 2>&1 || true
    fi
}

# Main sync logic
if ! acquire_lock; then
    exit 0
fi

if [[ ! -d "$DOCS_PATH" ]]; then
    # Clone fresh
    if git clone --quiet "$REPO_URL" "$DOCS_PATH" 2>/dev/null; then
        rebuild_index
    else
        echo "claude-docs: failed to clone docs repo" >&2
    fi
    exit 0
fi

# Pull if behind remote
cd "$DOCS_PATH" 2>/dev/null || exit 0

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

if ! git fetch --quiet origin "$BRANCH" 2>/dev/null; then
    if ! git fetch --quiet origin main 2>/dev/null; then
        exit 0
    fi
    BRANCH="main"
fi

LOCAL=$(git rev-parse HEAD 2>/dev/null || echo "")
REMOTE=$(git rev-parse "origin/$BRANCH" 2>/dev/null || echo "")
BEHIND=$(git rev-list "HEAD..origin/$BRANCH" --count 2>/dev/null || echo "0")

if [[ "$LOCAL" != "$REMOTE" ]] && [[ "$BEHIND" -gt 0 ]]; then
    if git pull --quiet origin "$BRANCH" 2>/dev/null; then
        rebuild_index
    fi
fi

exit 0
