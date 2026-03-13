#!/usr/bin/env bash
set -euo pipefail

# Claude-VC uninstaller
# Removes skill files from ~/.claude/

CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"

echo "Uninstalling claude-vc..."

# Remove orchestrator and references
if [ -d "${SKILLS_DIR}/vc" ]; then
    rm -rf "${SKILLS_DIR}/vc"
    echo "  Removed ${SKILLS_DIR}/vc/"
fi

# Remove sub-skills
for skill_dir in "${SKILLS_DIR}"/vc-*/; do
    if [ -d "${skill_dir}" ]; then
        rm -rf "${skill_dir}"
        echo "  Removed ${skill_dir}"
    fi
done

# Remove agents
for agent_file in "${AGENTS_DIR}"/vc-*.md; do
    if [ -f "${agent_file}" ]; then
        rm -f "${agent_file}"
        echo "  Removed ${agent_file}"
    fi
done

echo ""
echo "claude-vc uninstalled successfully."
