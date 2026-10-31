#!/bin/bash
# Richtet den Skill claude-editor in jeder neuen Claude-Code-Cloud-Sitzung automatisch ein:
# Python-Umgebung (numpy, faster-whisper), Renderer (puppeteer-core) und Verknüpfung nach ~/.claude/skills.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

SK="${CLAUDE_PROJECT_DIR:-.}/.claude/skills/claude-editor"
cd "$SK"

# Python-Umgebung nur neu installieren, wenn sich requirements.txt oder dieses Skript geändert haben
hashes=.venv/.session-start.sha256
if ! sha256sum --check --status "$hashes" 2>/dev/null; then
  rm -f "$hashes"
  [ -x .venv/bin/python ] || python3 -m venv .venv
  .venv/bin/pip install -q --upgrade pip
  .venv/bin/pip install -q -r requirements.txt
  sha256sum "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh" requirements.txt > "$hashes" || rm -f "$hashes"
fi

# Renderer nur neu installieren, wenn sich package.json oder dieses Skript geändert haben
hashes=node_modules/.session-start.sha256
if ! sha256sum --check --status "$hashes" 2>/dev/null; then
  rm -f "$hashes"
  npm install --no-audit --no-fund --silent
  sha256sum "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh" package.json > "$hashes" || rm -f "$hashes"
fi

# SKILL.md erwartet den Skill unter ~/.claude/skills/claude-editor. Eine echte, ältere Installation dort bleibt unangetastet.
mkdir -p "$HOME/.claude/skills"
ziel="$HOME/.claude/skills/claude-editor"
if [ -L "$ziel" ] || [ ! -e "$ziel" ]; then
  ln -sfn "$SK" "$ziel"
fi

# Chrome für den Renderer: Standardpfade prüft render.mjs selbst, sonst den vorinstallierten Chromium nehmen
if [ -n "${CLAUDE_ENV_FILE:-}" ] && ! command -v google-chrome >/dev/null && [ -x /opt/pw-browsers/chromium ]; then
  echo 'export CHROME=/opt/pw-browsers/chromium' >> "$CLAUDE_ENV_FILE"
fi
