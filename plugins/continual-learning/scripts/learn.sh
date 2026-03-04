#!/bin/bash
# Continual Learning v1.1.0 — single script, all events
# Usage: learn.sh <event>  (SessionStart | PostToolUse | PostToolUseFailure | SessionEnd)
#
# Auto-initializes on first run. No manual setup needed.
# Two-tier memory: global (~/.claude/learnings.db) + local (.claude-memory/)
#
# Categories: tool_insight, mistake, pattern, preference

set -euo pipefail

[[ "${SKIP_CONTINUAL_LEARNING:-}" == "true" ]] && exit 0

EVENT="${1:-}"
INPUT=$(cat 2>/dev/null || echo "{}")

# --- Paths ---
GLOBAL_DB="$HOME/.claude/learnings.db"
LOCAL_DIR=".claude-memory"
LOCAL_DB="$LOCAL_DIR/learnings.db"

# --- Auto-init (creates everything on first run) ---
init_db() {
  local db="$1"
  mkdir -p "$(dirname "$db")"
  command -v sqlite3 &>/dev/null || return 0
  sqlite3 "$db" <<'SQL'
CREATE TABLE IF NOT EXISTS learnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope TEXT NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    last_seen TEXT DEFAULT (datetime('now')),
    hit_count INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS tool_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name TEXT,
    result TEXT,
    ts TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_learnings_scope ON learnings(scope);
CREATE INDEX IF NOT EXISTS idx_learnings_category ON learnings(category);
SQL

  # Schema migration v1.1 — add context columns (idempotent)
  sqlite3 "$db" "ALTER TABLE tool_log ADD COLUMN session_id TEXT;" 2>/dev/null || true
  sqlite3 "$db" "ALTER TABLE tool_log ADD COLUMN context TEXT;" 2>/dev/null || true
  sqlite3 "$db" "ALTER TABLE tool_log ADD COLUMN tool_category TEXT;" 2>/dev/null || true

  sqlite3 "$db" <<'SQL'
CREATE TABLE IF NOT EXISTS tool_sequences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    seq_key TEXT NOT NULL,
    occurrences INTEGER DEFAULT 1,
    last_seen TEXT DEFAULT (datetime('now')),
    UNIQUE(session_id, seq_key)
);
CREATE INDEX IF NOT EXISTS idx_seq_key ON tool_sequences(seq_key);
SQL
}

init_db "$GLOBAL_DB"
[[ -d ".git" ]] && init_db "$LOCAL_DB"

has_sqlite() { command -v sqlite3 &>/dev/null; }
has_jq() { command -v jq &>/dev/null; }
repo_name() { basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"; }

# SQL-safe string: escape single quotes, truncate
sql_safe() {
  local max="${2:-200}"
  echo "${1:0:$max}" | sed "s/'/''/g"
}

# --- Upsert learning: insert if new, bump hit_count if exists ---
# Args: $1=scope $2=category $3=content $4=db_path
upsert_learning() {
  local scope="$1" cat="$2" content="$3" db="$4"
  local s_scope s_cat s_content
  s_scope=$(sql_safe "$scope" 20)
  s_cat=$(sql_safe "$cat" 30)
  s_content=$(sql_safe "$content" 300)

  sqlite3 "$db" \
    "INSERT INTO learnings (scope, category, content, source)
     SELECT '$s_scope','$s_cat','$s_content','auto:$(date -u +%Y%m%d)'
     WHERE NOT EXISTS (
       SELECT 1 FROM learnings WHERE category='$s_cat' AND content='$s_content'
     );
     UPDATE learnings SET hit_count = hit_count + 1, last_seen = datetime('now')
     WHERE category='$s_cat' AND content='$s_content';" 2>/dev/null || true
}

# --- SESSION START -----------------------------------------------
on_session_start() {
  has_sqlite || exit 0

  local context=""

  # --- Global learnings (grouped by category) ---
  local global_count
  global_count=$(sqlite3 "$GLOBAL_DB" "SELECT COUNT(*) FROM learnings;" 2>/dev/null || echo "0")
  if [[ "$global_count" -gt 0 ]]; then
    local mistakes patterns preferences insights

    mistakes=$(sqlite3 "$GLOBAL_DB" \
      "SELECT content FROM learnings WHERE category='mistake'
       ORDER BY hit_count DESC, last_seen DESC LIMIT 3;" 2>/dev/null || echo "")
    patterns=$(sqlite3 "$GLOBAL_DB" \
      "SELECT content FROM learnings WHERE category='pattern'
       ORDER BY hit_count DESC, last_seen DESC LIMIT 3;" 2>/dev/null || echo "")
    preferences=$(sqlite3 "$GLOBAL_DB" \
      "SELECT content FROM learnings WHERE category='preference'
       ORDER BY hit_count DESC, last_seen DESC LIMIT 2;" 2>/dev/null || echo "")
    insights=$(sqlite3 "$GLOBAL_DB" \
      "SELECT content FROM learnings WHERE category='tool_insight'
       ORDER BY hit_count DESC, last_seen DESC LIMIT 2;" 2>/dev/null || echo "")

    if [[ -n "$mistakes" ]]; then
      context="Avoid these mistakes:"
      while IFS= read -r line; do
        [[ -n "$line" ]] && context="$context\n  - $line"
      done <<< "$mistakes"
    fi

    if [[ -n "$patterns" ]]; then
      [[ -n "$context" ]] && context="$context\n"
      local section="Recognized patterns:"
      while IFS= read -r line; do
        [[ -n "$line" ]] && section="$section\n  - $line"
      done <<< "$patterns"
      context="$context$section"
    fi

    if [[ -n "$preferences" ]]; then
      [[ -n "$context" ]] && context="$context\n"
      local section="Preferences:"
      while IFS= read -r line; do
        [[ -n "$line" ]] && section="$section\n  - $line"
      done <<< "$preferences"
      context="$context$section"
    fi

    if [[ -n "$insights" ]]; then
      [[ -n "$context" ]] && context="$context\n"
      local section="Tool notes:"
      while IFS= read -r line; do
        [[ -n "$line" ]] && section="$section\n  - $line"
      done <<< "$insights"
      context="$context$section"
    fi

    if [[ -n "$context" ]]; then
      context="Global learnings ($global_count total):\n$context"
    fi
  fi

  # --- Local (repo) learnings ---
  if [[ -f "$LOCAL_DB" ]]; then
    local local_count
    local_count=$(sqlite3 "$LOCAL_DB" "SELECT COUNT(*) FROM learnings;" 2>/dev/null || echo "0")
    if [[ "$local_count" -gt 0 ]]; then
      local top_local
      top_local=$(sqlite3 "$LOCAL_DB" \
        "SELECT '  - [' || category || '] ' || content FROM learnings
         ORDER BY hit_count DESC, last_seen DESC LIMIT 5;" 2>/dev/null || echo "")
      if [[ -n "$top_local" ]]; then
        [[ -n "$context" ]] && context="$context\n"
        context="${context}\nRepo learnings for $(repo_name) ($local_count total):\n$top_local"
      fi
    fi
  fi

  if [[ -n "$context" ]]; then
    echo -e "$context"
  fi
}

# --- Extract context from tool input ---
# Sets: tool_name, context, tool_cat, session_id
extract_tool_context() {
  tool_name=""
  context=""
  tool_cat="other"
  session_id=""

  if has_jq; then
    tool_name=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || echo "")
    session_id=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null || echo "")

    case "$tool_name" in
      Bash)
        context=$(echo "$INPUT" | jq -r '(.tool_input.command // "")[:120]' 2>/dev/null || echo "")
        tool_cat="bash_cmd"
        ;;
      Write|Edit|Read)
        context=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""' 2>/dev/null || echo "")
        tool_cat="file_op"
        ;;
      Glob|Grep)
        context=$(echo "$INPUT" | jq -r '.tool_input.pattern // ""' 2>/dev/null || echo "")
        tool_cat="search"
        ;;
      WebFetch|WebSearch)
        context=$(echo "$INPUT" | jq -r '.tool_input.url // .tool_input.query // ""' 2>/dev/null || echo "")
        tool_cat="web"
        ;;
      mcp__*)
        context="$tool_name"
        tool_cat="mcp"
        ;;
      Agent)
        context=$(echo "$INPUT" | jq -r '.tool_input.description // ""' 2>/dev/null || echo "")
        tool_cat="other"
        ;;
      *)
        tool_cat="other"
        ;;
    esac
  else
    tool_name=$(echo "$INPUT" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"//')
  fi
}

# --- POST TOOL USE (success) -------------------------------------
on_post_tool_use() {
  has_sqlite || exit 0

  local tool_name context tool_cat session_id
  extract_tool_context

  [[ -z "$tool_name" ]] && exit 0

  local s_tool s_ctx s_cat s_sid
  s_tool=$(sql_safe "$tool_name" 100)
  s_ctx=$(sql_safe "$context" 200)
  s_cat=$(sql_safe "$tool_cat" 20)
  s_sid=$(sql_safe "$session_id" 100)

  sqlite3 "$GLOBAL_DB" \
    "INSERT INTO tool_log (tool_name, result, context, tool_category, session_id)
     VALUES ('$s_tool','success','$s_ctx','$s_cat','$s_sid');" 2>/dev/null || true
}

# --- POST TOOL USE FAILURE ----------------------------------------
on_post_tool_use_failure() {
  has_sqlite || exit 0

  local tool_name context tool_cat session_id
  extract_tool_context

  [[ -z "$tool_name" ]] && exit 0

  # Append error snippet if available
  if has_jq; then
    local error_msg
    error_msg=$(echo "$INPUT" | jq -r '.error // ""' 2>/dev/null || echo "")
    if [[ -n "$error_msg" ]]; then
      context="${context}|err:${error_msg:0:80}"
    fi
  fi

  local s_tool s_ctx s_cat s_sid
  s_tool=$(sql_safe "$tool_name" 100)
  s_ctx=$(sql_safe "$context" 250)
  s_cat=$(sql_safe "$tool_cat" 20)
  s_sid=$(sql_safe "$session_id" 100)

  sqlite3 "$GLOBAL_DB" \
    "INSERT INTO tool_log (tool_name, result, context, tool_category, session_id)
     VALUES ('$s_tool','failure','$s_ctx','$s_cat','$s_sid');" 2>/dev/null || true
}

# --- SESSION END --------------------------------------------------

# 1. Tool insights — only flag tools with high failure *rate* (not just count)
analyze_tool_insights() {
  local fail_tools
  fail_tools=$(sqlite3 "$GLOBAL_DB" \
    "SELECT f.tool_name, f.fail_cnt, COALESCE(s.ok_cnt, 0) as ok_cnt
     FROM (
       SELECT tool_name, COUNT(*) as fail_cnt FROM tool_log
       WHERE result='failure' AND ts > datetime('now','-4 hours')
       GROUP BY tool_name HAVING fail_cnt > 2
     ) f
     LEFT JOIN (
       SELECT tool_name, COUNT(*) as ok_cnt FROM tool_log
       WHERE result='success' AND ts > datetime('now','-4 hours')
       GROUP BY tool_name
     ) s ON f.tool_name = s.tool_name
     WHERE f.fail_cnt * 100.0 / (f.fail_cnt + COALESCE(s.ok_cnt, 0)) > 20;" \
    2>/dev/null || echo "")

  if [[ -n "$fail_tools" ]]; then
    while IFS='|' read -r tool fail_cnt ok_cnt; do
      [[ -z "$tool" ]] && continue
      local rate=$(( fail_cnt * 100 / (fail_cnt + ok_cnt) ))
      upsert_learning "global" "tool_insight" \
        "Tool \"$tool\" frequently fails (${rate}% failure rate) — check usage pattern" \
        "$GLOBAL_DB"
    done <<< "$fail_tools"
  fi
}

# 2. Mistake learnings — specific failure patterns
analyze_mistakes() {
  # Permission/access errors
  local perm_errors
  perm_errors=$(sqlite3 "$GLOBAL_DB" \
    "SELECT COUNT(*) FROM tool_log
     WHERE result='failure' AND ts > datetime('now','-4 hours')
       AND (context LIKE '%Permission denied%' OR context LIKE '%EACCES%');" \
    2>/dev/null || echo "0")
  if [[ "$perm_errors" -gt 2 ]]; then
    upsert_learning "global" "mistake" \
      "Repeated permission errors — check file permissions before write operations" \
      "$GLOBAL_DB"
  fi

  # File not found
  local notfound
  notfound=$(sqlite3 "$GLOBAL_DB" \
    "SELECT COUNT(*) FROM tool_log
     WHERE result='failure' AND ts > datetime('now','-4 hours')
       AND (context LIKE '%No such file%' OR context LIKE '%ENOENT%');" \
    2>/dev/null || echo "0")
  if [[ "$notfound" -gt 2 ]]; then
    upsert_learning "global" "mistake" \
      "Repeated file-not-found errors — verify paths exist before operations" \
      "$GLOBAL_DB"
  fi

  # Bash commands failing by first word (e.g., npm, pip, docker)
  local fail_cmds
  fail_cmds=$(sqlite3 "$GLOBAL_DB" \
    "SELECT SUBSTR(context, 1, INSTR(context || ' ', ' ') - 1) as cmd,
            COUNT(*) as cnt
     FROM tool_log
     WHERE result='failure' AND tool_category='bash_cmd'
       AND ts > datetime('now','-4 hours')
       AND context != '' AND context IS NOT NULL
     GROUP BY cmd HAVING cnt > 2
     ORDER BY cnt DESC LIMIT 3;" 2>/dev/null || echo "")

  if [[ -n "$fail_cmds" ]]; then
    while IFS='|' read -r cmd cnt; do
      [[ -z "$cmd" ]] && continue
      upsert_learning "global" "mistake" \
        "\"$cmd\" commands fail frequently ($cnt times) — verify syntax and arguments" \
        "$GLOBAL_DB"
    done <<< "$fail_cmds"
  fi

  # Edit tool failures (old_string not matching)
  local edit_fails
  edit_fails=$(sqlite3 "$GLOBAL_DB" \
    "SELECT COUNT(*) FROM tool_log
     WHERE result='failure' AND tool_name='Edit'
       AND ts > datetime('now','-4 hours');" 2>/dev/null || echo "0")
  if [[ "$edit_fails" -gt 2 ]]; then
    upsert_learning "global" "mistake" \
      "Edit tool fails often — read file first to ensure old_string matches exactly" \
      "$GLOBAL_DB"
  fi

  # Trial-and-error pattern (repeated fail then success on same tool)
  local retry_tools
  retry_tools=$(sqlite3 "$GLOBAL_DB" \
    "SELECT t1.tool_name, COUNT(*) as fail_cnt
     FROM tool_log t1
     WHERE t1.result='failure' AND t1.ts > datetime('now','-4 hours')
       AND EXISTS (
         SELECT 1 FROM tool_log t2
         WHERE t2.tool_name = t1.tool_name
           AND t2.result='success'
           AND t2.ts > t1.ts
           AND t2.ts < datetime(t1.ts, '+2 minutes')
       )
     GROUP BY t1.tool_name HAVING fail_cnt > 2
     LIMIT 3;" 2>/dev/null || echo "")

  if [[ -n "$retry_tools" ]]; then
    while IFS='|' read -r tool cnt; do
      [[ -z "$tool" ]] && continue
      upsert_learning "global" "mistake" \
        "Trial-and-error pattern with $tool ($cnt retries) — plan before executing" \
        "$GLOBAL_DB"
    done <<< "$retry_tools"
  fi
}

# 3. Pattern learnings — recurring workflows and file types
analyze_patterns() {
  # Tool sequence fingerprints (3-tool sliding window)
  local session_id=""
  if has_jq; then
    session_id=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null || echo "")
  fi

  if [[ -n "$session_id" ]]; then
    local seq
    seq=$(sqlite3 "$GLOBAL_DB" \
      "SELECT GROUP_CONCAT(tool_name, '>') FROM (
         SELECT tool_name FROM tool_log
         WHERE session_id='$(sql_safe "$session_id" 100)'
           AND result='success'
         ORDER BY ts
         LIMIT 100
       );" 2>/dev/null || echo "")

    if [[ -n "$seq" ]]; then
      IFS='>' read -ra tools <<< "$seq"
      local len=${#tools[@]}
      declare -A seq_counts 2>/dev/null || true
      for ((i=0; i<len-2; i++)); do
        local triplet="${tools[$i]}>${tools[$((i+1))]}>${tools[$((i+2))]}"
        seq_counts["$triplet"]=$(( ${seq_counts["$triplet"]:-0} + 1 ))
      done

      for triplet in "${!seq_counts[@]}"; do
        local count=${seq_counts["$triplet"]}
        if [[ "$count" -gt 3 ]]; then
          local s_trip s_sid
          s_trip=$(sql_safe "$triplet" 200)
          s_sid=$(sql_safe "$session_id" 100)
          sqlite3 "$GLOBAL_DB" \
            "INSERT INTO tool_sequences (session_id, seq_key, occurrences)
             VALUES ('$s_sid','$s_trip',$count)
             ON CONFLICT(session_id, seq_key) DO UPDATE SET
               occurrences = $count, last_seen = datetime('now');" 2>/dev/null || true
        fi
      done
    fi
  fi

  # Cross-session recurring sequences
  local common_seqs
  common_seqs=$(sqlite3 "$GLOBAL_DB" \
    "SELECT seq_key, SUM(occurrences) as total
     FROM tool_sequences
     GROUP BY seq_key HAVING COUNT(DISTINCT session_id) > 2
     ORDER BY total DESC LIMIT 3;" 2>/dev/null || echo "")

  if [[ -n "$common_seqs" ]]; then
    while IFS='|' read -r seq_key total; do
      [[ -z "$seq_key" ]] && continue
      local readable
      readable=$(echo "$seq_key" | sed 's/>/ then /g')
      upsert_learning "global" "pattern" \
        "Common workflow: $readable" \
        "$GLOBAL_DB"
    done <<< "$common_seqs"
  fi

  # File type patterns (local scope)
  if [[ -f "$LOCAL_DB" ]]; then
    local file_exts
    file_exts=$(sqlite3 "$GLOBAL_DB" \
      "SELECT
         CASE
           WHEN context LIKE '%.ts' OR context LIKE '%.tsx' THEN 'TypeScript'
           WHEN context LIKE '%.js' OR context LIKE '%.jsx' THEN 'JavaScript'
           WHEN context LIKE '%.py' THEN 'Python'
           WHEN context LIKE '%.sh' THEN 'Shell'
           WHEN context LIKE '%.rs' THEN 'Rust'
           WHEN context LIKE '%.go' THEN 'Go'
           WHEN context LIKE '%.ps1' THEN 'PowerShell'
           WHEN context LIKE '%.md' THEN 'Markdown'
           WHEN context LIKE '%.json' THEN 'JSON'
           WHEN context LIKE '%.yaml' OR context LIKE '%.yml' THEN 'YAML'
           ELSE NULL
         END as lang,
         COUNT(*) as cnt
       FROM tool_log
       WHERE tool_category='file_op' AND result='success'
         AND ts > datetime('now','-24 hours')
       GROUP BY lang HAVING lang IS NOT NULL AND cnt > 5
       ORDER BY cnt DESC LIMIT 2;" 2>/dev/null || echo "")

    if [[ -n "$file_exts" ]]; then
      while IFS='|' read -r lang cnt; do
        [[ -z "$lang" ]] && continue
        upsert_learning "local" "pattern" \
          "Primary language in this repo: $lang" \
          "$LOCAL_DB"
      done <<< "$file_exts"
    fi
  fi

  # Heavy tool usage — stable content (no volatile counts) to avoid duplicates
  local top_tools
  top_tools=$(sqlite3 "$GLOBAL_DB" \
    "SELECT tool_name, COUNT(*) as cnt FROM tool_log
     WHERE result='success' AND ts > datetime('now','-24 hours')
     GROUP BY tool_name HAVING cnt > 20
     ORDER BY cnt DESC LIMIT 3;" 2>/dev/null || echo "")

  if [[ -n "$top_tools" ]]; then
    while IFS='|' read -r top_tool top_cnt; do
      [[ -z "$top_tool" ]] && continue
      upsert_learning "global" "pattern" \
        "Heavy $top_tool usage — primary workflow tool" \
        "$GLOBAL_DB"
    done <<< "$top_tools"
  fi
}

# 4. Preference learnings — detected behavioral signals
analyze_preferences() {
  # Write vs Edit ratio
  local write_cnt edit_cnt
  write_cnt=$(sqlite3 "$GLOBAL_DB" \
    "SELECT COUNT(*) FROM tool_log
     WHERE tool_name='Write' AND result='success' AND ts > datetime('now','-24 hours');" \
    2>/dev/null || echo "0")
  edit_cnt=$(sqlite3 "$GLOBAL_DB" \
    "SELECT COUNT(*) FROM tool_log
     WHERE tool_name='Edit' AND result='success' AND ts > datetime('now','-24 hours');" \
    2>/dev/null || echo "0")

  local total_file=$(( write_cnt + edit_cnt ))
  if [[ "$total_file" -gt 10 ]]; then
    local ratio=$(( edit_cnt * 100 / total_file ))
    if [[ "$ratio" -gt 75 ]]; then
      upsert_learning "global" "preference" \
        "Edit tool preferred over Write — surgical edits style" \
        "$GLOBAL_DB"
    elif [[ "$ratio" -lt 25 ]]; then
      upsert_learning "global" "preference" \
        "Write tool preferred over Edit — full-file write style" \
        "$GLOBAL_DB"
    fi
  fi

  # MCP server usage
  local mcp_count
  mcp_count=$(sqlite3 "$GLOBAL_DB" \
    "SELECT COUNT(*) FROM tool_log
     WHERE tool_category='mcp' AND result='success' AND ts > datetime('now','-24 hours');" \
    2>/dev/null || echo "0")

  if [[ "${mcp_count:-0}" -gt 10 ]]; then
    local top_mcp
    top_mcp=$(sqlite3 "$GLOBAL_DB" \
      "SELECT tool_name, COUNT(*) as cnt FROM tool_log
       WHERE tool_category='mcp' AND result='success' AND ts > datetime('now','-24 hours')
       GROUP BY tool_name ORDER BY cnt DESC LIMIT 1;" 2>/dev/null || echo "")
    if [[ -n "$top_mcp" ]]; then
      IFS='|' read -r mcp_name mcp_cnt <<< "$top_mcp"
      local server_name
      server_name=$(echo "$mcp_name" | sed 's/^mcp__//;s/__.*//')
      upsert_learning "global" "preference" \
        "Frequently uses $server_name MCP server — integrate with workflows" \
        "$GLOBAL_DB"
    fi
  fi

  # Search-before-edit pattern
  local search_before_edit
  search_before_edit=$(sqlite3 "$GLOBAL_DB" \
    "SELECT COUNT(*) FROM tool_log t1
     WHERE t1.tool_name IN ('Grep','Glob') AND t1.result='success'
       AND t1.ts > datetime('now','-4 hours')
       AND EXISTS (
         SELECT 1 FROM tool_log t2
         WHERE t2.tool_name IN ('Edit','Write')
           AND t2.ts > t1.ts
           AND t2.ts < datetime(t1.ts, '+3 minutes')
       );" 2>/dev/null || echo "0")

  local direct_edits
  direct_edits=$(sqlite3 "$GLOBAL_DB" \
    "SELECT COUNT(*) FROM tool_log
     WHERE tool_name IN ('Edit','Write') AND result='success'
       AND ts > datetime('now','-4 hours');" 2>/dev/null || echo "0")

  if [[ "${direct_edits:-0}" -gt 5 && "${search_before_edit:-0}" -gt 0 ]]; then
    local search_ratio=$(( search_before_edit * 100 / direct_edits ))
    if [[ "$search_ratio" -gt 60 ]]; then
      upsert_learning "global" "preference" \
        "Search-before-edit workflow — typically searches before editing files" \
        "$GLOBAL_DB"
    fi
  fi
}

on_session_end() {
  has_sqlite || exit 0

  local total failures
  total=$(sqlite3 "$GLOBAL_DB" \
    "SELECT COUNT(*) FROM tool_log WHERE ts > datetime('now','-4 hours');" 2>/dev/null || echo "0")
  failures=$(sqlite3 "$GLOBAL_DB" \
    "SELECT COUNT(*) FROM tool_log WHERE result='failure' AND ts > datetime('now','-4 hours');" 2>/dev/null || echo "0")

  # Run all analyzers
  analyze_tool_insights
  analyze_mistakes
  analyze_patterns
  analyze_preferences

  # --- Compact: prune old tool logs (keep 7 days) ---
  sqlite3 "$GLOBAL_DB" "DELETE FROM tool_log WHERE ts < datetime('now','-7 days');" 2>/dev/null || true
  sqlite3 "$GLOBAL_DB" "DELETE FROM tool_sequences WHERE last_seen < datetime('now','-30 days');" 2>/dev/null || true

  # --- Compact: decay old learnings (>60 days, low hit count) ---
  sqlite3 "$GLOBAL_DB" \
    "DELETE FROM learnings WHERE last_seen < datetime('now','-60 days') AND hit_count < 3;" 2>/dev/null || true
  [[ -f "$LOCAL_DB" ]] && sqlite3 "$LOCAL_DB" \
    "DELETE FROM learnings WHERE last_seen < datetime('now','-60 days') AND hit_count < 3;" 2>/dev/null || true

  # Status to stderr only
  echo "Session reflected — tools: $total, failures: $failures" >&2
}

# --- Dispatch -----------------------------------------------------
case "$EVENT" in
  SessionStart)          on_session_start ;;
  PostToolUse)           on_post_tool_use ;;
  PostToolUseFailure)    on_post_tool_use_failure ;;
  SessionEnd)            on_session_end ;;
  *)                     echo "Usage: learn.sh <SessionStart|PostToolUse|PostToolUseFailure|SessionEnd>" >&2; exit 1 ;;
esac

exit 0
