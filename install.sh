#!/usr/bin/env bash
set -euo pipefail

# Claude-VC installer
# Copies the vc skill into ~/.claude/ for Claude Code to discover.
# Safe to re-run: cleans stale vc files before copying, writes a
# version marker so `update.sh` can detect what's installed.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"
COMMANDS_DIR="${CLAUDE_DIR}/commands"
VERSION_FILE="${SKILLS_DIR}/vc/.version"

# Read version from plugin manifest
VERSION=$(python3 -c "import json; print(json.load(open('${SCRIPT_DIR}/.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo "unknown")
GIT_SHA=$(git -C "${SCRIPT_DIR}" rev-parse --short HEAD 2>/dev/null || echo "unknown")

echo "Installing claude-vc v${VERSION} (${GIT_SHA})..."

# Clean previous installation to remove stale files from earlier versions
# (v1.5.x and earlier installed multiple vc-* skills and top-level command wrappers)
if [ -d "${SKILLS_DIR}/vc" ]; then
    rm -rf "${SKILLS_DIR}/vc"
fi
for old_skill in "${SKILLS_DIR}"/vc-*/; do
    if [ -d "${old_skill}" ]; then
        rm -rf "${old_skill}"
    fi
done
for old_agent in "${AGENTS_DIR}"/vc-*.md; do
    if [ -f "${old_agent}" ]; then
        rm -f "${old_agent}"
    fi
done
for old_cmd in "${COMMANDS_DIR}"/{screen,memo,terms,captable,model,kpi,compare,diligence,portfolio,returns}.md; do
    if [ -f "${old_cmd}" ]; then
        rm -f "${old_cmd}"
    fi
done

# Copy the vc skill (includes SKILL.md, commands/, agents/, references/, scripts/, config/)
mkdir -p "${SKILLS_DIR}"
cp -r "${SCRIPT_DIR}/skills/vc" "${SKILLS_DIR}/vc"

# Write version marker
echo "${VERSION} ${GIT_SHA}" > "${VERSION_FILE}"

echo "claude-vc v${VERSION} installed successfully."
echo ""
echo "Installed to:"
echo "  ${SKILLS_DIR}/vc/"
echo ""
echo "Usage: type /vc in Claude Code to get started."
echo "To update later: run ./update.sh or re-run ./install.sh"
