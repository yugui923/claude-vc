#!/usr/bin/env bash
set -euo pipefail

# Claude-VC uninstaller
# Removes claude-vc files from ~/.claude/

CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"
COMMANDS_DIR="${CLAUDE_DIR}/commands"

echo "Uninstalling claude-vc..."

# Remove the vc skill
if [ -d "${SKILLS_DIR}/vc" ]; then
    rm -rf "${SKILLS_DIR}/vc"
    echo "  Removed ${SKILLS_DIR}/vc/"
fi

# Clean up artifacts from earlier versions (v1.5.x and earlier)
for skill_dir in "${SKILLS_DIR}"/vc-*/; do
    if [ -d "${skill_dir}" ]; then
        rm -rf "${skill_dir}"
        echo "  Removed ${skill_dir}"
    fi
done
for agent_file in "${AGENTS_DIR}"/vc-*.md; do
    if [ -f "${agent_file}" ]; then
        rm -f "${agent_file}"
        echo "  Removed ${agent_file}"
    fi
done
for cmd_file in "${COMMANDS_DIR}"/{screen,memo,terms,captable,model,kpi,compare,diligence,portfolio,returns}.md; do
    if [ -f "${cmd_file}" ]; then
        rm -f "${cmd_file}"
        echo "  Removed ${cmd_file}"
    fi
done

echo ""
echo "claude-vc uninstalled successfully."
