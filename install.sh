#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"

usage() {
  echo "Usage: $0 [codex|claude|all] [<skill-name>]"
  echo ""
  echo "  codex   Install for Codex      (~/.agents/skills/, ~/.codex/skills/)"
  echo "  claude  Install for Claude Code (~/.claude/skills/)"
  echo "  all     Install for all supported tools"
  echo ""
  echo "  Optional second argument: install only the named skill"
  echo ""
  echo "Available skills:"
  list_skills
  exit 1
}

list_skills() {
  for skill_dir in "$SKILLS_DIR"/*/; do
    [ -f "$skill_dir/SKILL.md" ] && echo "  - $(basename "$skill_dir")"
  done
}

install_one() {
  local target_base="$1"
  local skill_name="$2"
  local source="$SKILLS_DIR/$skill_name/SKILL.md"

  if [ ! -f "$source" ]; then
    echo "  [skip] $skill_name: source not found ($source)" >&2
    return 0
  fi

  mkdir -p "$target_base/$skill_name"
  cp "$source" "$target_base/$skill_name/SKILL.md"
  echo "  ✓ $target_base/$skill_name/SKILL.md"
}

install_all_to() {
  local target_base="$1"
  local filter="${2:-}"

  for skill_dir in "$SKILLS_DIR"/*/; do
    local skill_name
    skill_name="$(basename "$skill_dir")"
    [ -n "$filter" ] && [ "$filter" != "$skill_name" ] && continue
    install_one "$target_base" "$skill_name"
  done
}

install_codex() {
  local filter="${1:-}"
  echo "==> Codex"
  install_all_to "$HOME/.agents/skills" "$filter"
  install_all_to "$HOME/.codex/skills"  "$filter"
}

install_claude() {
  local filter="${1:-}"
  echo "==> Claude Code"
  install_all_to "$HOME/.claude/skills" "$filter"
}

# ── entry point ──────────────────────────────────────────────────────────────

if [ ! -d "$SKILLS_DIR" ]; then
  echo "Error: skills directory not found: $SKILLS_DIR" >&2
  exit 1
fi

TARGET="${1:-}"
SKILL_FILTER="${2:-}"

case "$TARGET" in
  codex)  install_codex  "$SKILL_FILTER" ;;
  claude) install_claude "$SKILL_FILTER" ;;
  all)
    install_codex  "$SKILL_FILTER"
    install_claude "$SKILL_FILTER"
    ;;
  *) usage ;;
esac

echo ""
echo "Done."
