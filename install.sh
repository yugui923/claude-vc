#!/usr/bin/env bash
set -euo pipefail

# Claude-VC installer
# Copies skill files into ~/.claude/ for Claude Code to discover.
# Safe to re-run: cleans stale vc files before copying, writes a
# version marker so `update.sh` can detect what's installed.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"
VERSION_FILE="${SKILLS_DIR}/vc/.version"

# Read version from plugin manifest
VERSION=$(python3 -c "import json; print(json.load(open('${SCRIPT_DIR}/.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo "unknown")
GIT_SHA=$(git -C "${SCRIPT_DIR}" rev-parse --short HEAD 2>/dev/null || echo "unknown")

echo "Installing claude-vc v${VERSION} (${GIT_SHA})..."

# Clean previous installation to remove stale files
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

# Copy orchestrator (includes references and scripts)
mkdir -p "${SKILLS_DIR}"
cp -r "${SCRIPT_DIR}/skills/vc" "${SKILLS_DIR}/vc"

# Copy sub-skills
for skill_dir in "${SCRIPT_DIR}"/skills/vc-*/; do
    if [ -d "${skill_dir}" ]; then
        skill_name="$(basename "${skill_dir}")"
        mkdir -p "${SKILLS_DIR}/${skill_name}"
        cp "${skill_dir}/SKILL.md" "${SKILLS_DIR}/${skill_name}/SKILL.md"
    fi
done

# Copy agents (if any .md files exist)
if compgen -G "${SCRIPT_DIR}/agents/*.md" >/dev/null 2>&1; then
    mkdir -p "${AGENTS_DIR}"
    cp "${SCRIPT_DIR}"/agents/*.md "${AGENTS_DIR}/"
fi

# Write version marker
echo "${VERSION} ${GIT_SHA}" > "${VERSION_FILE}"

echo "claude-vc v${VERSION} installed successfully."
echo ""
echo "Installed to:"
echo "  Skills:     ${SKILLS_DIR}/vc/"

for skill_dir in "${SKILLS_DIR}"/vc-*/; do
    if [ -d "${skill_dir}" ]; then
        echo "              ${skill_dir}"
    fi
done

if [ -d "${AGENTS_DIR}" ] && ls "${AGENTS_DIR}"/vc-*.md &>/dev/null; then
    echo "  Agents:     ${AGENTS_DIR}/vc-*.md"
fi

echo ""
echo "Usage: type /vc in Claude Code to get started."
echo "To update later: run ./update.sh or re-run ./install.sh"
