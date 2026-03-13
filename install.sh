#!/usr/bin/env bash
set -euo pipefail

# Claude-VC installer
# Copies skill files into ~/.claude/ for Claude Code to discover

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"

echo "Installing claude-vc..."

# Create target directories
mkdir -p "${SKILLS_DIR}/vc/references"

# Copy orchestrator and references
cp "${SCRIPT_DIR}/vc/SKILL.md" "${SKILLS_DIR}/vc/SKILL.md"
if [ -d "${SCRIPT_DIR}/vc/references" ]; then
    cp "${SCRIPT_DIR}"/vc/references/*.md "${SKILLS_DIR}/vc/references/"
fi

# Copy sub-skills
for skill_dir in "${SCRIPT_DIR}"/skills/vc-*/; do
    if [ -d "${skill_dir}" ]; then
        skill_name="$(basename "${skill_dir}")"
        mkdir -p "${SKILLS_DIR}/${skill_name}"
        cp "${skill_dir}/SKILL.md" "${SKILLS_DIR}/${skill_name}/SKILL.md"
    fi
done

# Copy scripts (if any .py files exist)
if compgen -G "${SCRIPT_DIR}/scripts/*.py" >/dev/null 2>&1; then
    mkdir -p "${SKILLS_DIR}/vc/scripts"
    cp "${SCRIPT_DIR}"/scripts/*.py "${SKILLS_DIR}/vc/scripts/"
fi

# Copy agents (if any .md files exist)
if compgen -G "${SCRIPT_DIR}/agents/*.md" >/dev/null 2>&1; then
    mkdir -p "${AGENTS_DIR}"
    cp "${SCRIPT_DIR}"/agents/*.md "${AGENTS_DIR}/"
fi

echo "claude-vc installed successfully."
echo ""
echo "Installed to:"
echo "  Skills:     ${SKILLS_DIR}/vc/"

# List installed sub-skills
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
