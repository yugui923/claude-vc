#!/usr/bin/env bash
set -euo pipefail

# Claude-VC updater
# Pulls latest from the repository and re-installs.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${HOME}/.claude/skills"
VERSION_FILE="${SKILLS_DIR}/vc/.version"

# Show current installed version
if [ -f "${VERSION_FILE}" ]; then
    echo "Currently installed: v$(cat "${VERSION_FILE}")"
else
    echo "No existing installation detected."
fi

# Pull latest changes
echo "Pulling latest from origin..."
if ! git -C "${SCRIPT_DIR}" pull --ff-only; then
    echo "Error: git pull failed. You may have local changes." >&2
    echo "Run 'git -C ${SCRIPT_DIR} status' to check." >&2
    exit 1
fi

# Read new version
NEW_VERSION=$(python3 -c "import json; print(json.load(open('${SCRIPT_DIR}/.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo "unknown")
NEW_SHA=$(git -C "${SCRIPT_DIR}" rev-parse --short HEAD 2>/dev/null || echo "unknown")
echo "Latest version: v${NEW_VERSION} (${NEW_SHA})"

# Re-run installer
echo ""
exec "${SCRIPT_DIR}/install.sh"
