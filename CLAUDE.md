# Claude-VC Project Instructions

## Project Overview

Claude-VC is a Claude Cowork and Claude Code plugin for venture capital
analysis. It provides deal screening, investment memos, cap table modeling,
term sheet analysis, financial modeling, and KPI reporting through the `/vc`
command.

## Key Paths

- `skills/vc/SKILL.md` — orchestrator skill (entry point and routing table)
- `skills/vc/commands/` — sub-command prompt files (screen, memo, terms,
  captable, model, portfolio). Loaded via Read by the orchestrator, not
  registered as separate skills.
- `skills/vc/agents/` — sub-agent prompt files (team, financial, market,
  technical, legal, competitive) for parallel screening via Agent/Task tool.
- `skills/vc/references/` — domain reference files loaded on demand.
- `skills/vc/scripts/` — Python computation scripts (captable.py,
  financial_model.py).
- `skills/vc/config/` — user-managed firm customization (criteria, templates).
- `tests/` — two-layer test suite (see `tests/TESTING.md`).
- `docs/` — specs, ADRs, plans.

## The AI Frontier

**Read [`docs/frontier.md`](docs/frontier.md) before making changes.**

This document tracks what AI can and cannot reliably do in VC analysis across
**all AI tools on the market** — not only claude-vc. It serves as a living
map of state-of-the-art capability. When you add or improve a capability:

1. Check if the change moves something across status columns (Cannot -> WIP,
   WIP -> Can Do)
2. If so, update `docs/frontier.md` — move the checkmark, add a changelog
   entry with today's date, direction, and enabler
3. If you discover a new limitation, add it
4. If a capability degrades or proves unreliable, move it back and log it as
   `Can Do -> WIP` or `WIP -> Cannot`
5. When a new AI product or feature ships that changes what's possible in VC,
   add a changelog entry even if claude-vc doesn't implement it

The frontier is a living record. Keep it honest.

## Audience

This project serves both **non-technical users** (VCs, analysts, founders)
and **technical users** (developers, contributors). When writing documentation
(README, user guide, skill descriptions), use plain language first — avoid
jargon, explain acronyms on first use, and include concrete examples. A
partner at a VC firm who has never used a CLI should be able to follow the
README and User Guide without confusion.

## Development

- **Python 3.10+**, stdlib only (no third-party runtime deps)
- **Dev tools**: `uv sync` for dev deps, `ruff` for lint/format, `pyright`
  for type checking, `pytest` for tests
- **Tests**: `uv run pytest` runs Layer 1 (172 unit/integration tests).
  `uv run pytest -m smoke` runs Layer 2 (5 skill-level smoke tests, requires
  Claude CLI)
- **Before committing**: run ruff check, ruff format, pyright, and pytest.
  All must pass
