#!/bin/bash
# se-skills session start hook
# Injects the using-se-skills meta-skill into every new session
# Pattern: same approach as ae-skills session-start hook

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(dirname "$SCRIPT_DIR")/skills"
META_SKILL="$SKILLS_DIR/using-se-skills/SKILL.md"

if ! command -v jq >/dev/null 2>&1; then
  echo '{"priority": "INFO", "message": "se-skills: jq is required for the session-start hook but was not found on PATH. Install jq to enable auto-pipeline injection. SE skills remain available individually via /se-requirements, /se-architecture, etc."}'
  exit 0
fi

if [ -f "$META_SKILL" ]; then
  CONTENT=$(cat "$META_SKILL")
  jq -cn \
    --arg message "se-skills loaded. SE pipeline ready — Define > Design > Document > Verify > Validate. If you have SE work (requirements/architecture/spec/review/traceability), tell me what you need and I will detect your current phase automatically.

$CONTENT" \
    '{priority: "IMPORTANT", message: $message}'
else
  echo '{"priority": "INFO", "message": "se-skills: using-se-skills meta-skill not found. Skills may still be available individually via slash commands."}'
fi
