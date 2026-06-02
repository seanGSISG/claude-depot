---
description: "Pull the latest Anthropic documentation now and rebuild the search index"
allowed-tools: ["Bash"]
---
Force an immediate sync of the locally mirrored Anthropic documentation: pull the
latest from the docs repo, refresh the runtime helper, and rebuild the search index.

Run exactly this, then report the result to the user (files synced, and whether the
docs changed):

!DOCS="$HOME/.claude-code-docs"; if [ -d "$DOCS/.git" ]; then pre=$(git -C "$DOCS" rev-parse HEAD 2>/dev/null || echo none); git -C "$DOCS" pull --ff-only --quiet 2>/dev/null || true; post=$(git -C "$DOCS" rev-parse HEAD 2>/dev/null || echo none); else git clone --quiet https://github.com/seanGSISG/claude-code-docs.git "$DOCS" && pre=none && post=new; fi; if [ -f "$DOCS/scripts/claude-docs-helper.sh" ]; then cp "$DOCS/scripts/claude-docs-helper.sh" "$DOCS/claude-docs-helper.sh" 2>/dev/null || true; chmod +x "$DOCS/claude-docs-helper.sh" 2>/dev/null || true; fi; if [ "$pre" != "$post" ] || [ ! -f "$DOCS/docs/.search_index.json" ]; then for py in python3 python; do command -v "$py" >/dev/null 2>&1 && { (cd "$DOCS" && "$py" scripts/build_search_index.py >/dev/null 2>&1); break; }; done; fi; if [ "$pre" = "$post" ]; then echo "Already up to date: $(find "$DOCS/docs" -name '*.md' 2>/dev/null | wc -l | tr -d ' ') files"; else echo "Updated docs: $(find "$DOCS/docs" -name '*.md' 2>/dev/null | wc -l | tr -d ' ') files (was $pre, now $post)"; fi
