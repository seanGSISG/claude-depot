---
description: "Pull the latest Anthropic documentation now"
allowed-tools: ["Bash"]
---
Force an immediate sync of the locally mirrored Anthropic documentation: pull the
latest from the docs repo and refresh the runtime helper. Search runs over the live
files (no index), so there is nothing to rebuild.

Run exactly this, then report the result to the user (files synced, and whether the
docs changed):

!DOCS="$HOME/.claude-code-docs"; if [ -d "$DOCS/.git" ]; then pre=$(git -C "$DOCS" rev-parse HEAD 2>/dev/null || echo none); git -C "$DOCS" pull --ff-only --quiet 2>/dev/null || true; post=$(git -C "$DOCS" rev-parse HEAD 2>/dev/null || echo none); else git clone --quiet https://github.com/seanGSISG/claude-code-docs.git "$DOCS" && pre=none && post=new; fi; [ -f "$DOCS/scripts/claude-docs-helper.sh" ] && { cp "$DOCS/scripts/claude-docs-helper.sh" "$DOCS/claude-docs-helper.sh" 2>/dev/null; chmod +x "$DOCS/claude-docs-helper.sh" 2>/dev/null; }; if ! command -v rg >/dev/null 2>&1; then if command -v winget >/dev/null 2>&1; then winget install --silent --accept-source-agreements --accept-package-agreements BurntSushi.ripgrep.MSVC >/dev/null 2>&1 || true; elif command -v brew >/dev/null 2>&1; then brew install ripgrep >/dev/null 2>&1 || true; elif command -v apt-get >/dev/null 2>&1; then sudo -n apt-get install -y ripgrep >/dev/null 2>&1 || true; fi; fi; if [ "$pre" = "$post" ]; then echo "Already up to date: $(find "$DOCS/docs" -name '*.md' 2>/dev/null | wc -l | tr -d ' ') files"; else echo "Updated docs: $(find "$DOCS/docs" -name '*.md' 2>/dev/null | wc -l | tr -d ' ') files (was $pre, now $post)"; fi
