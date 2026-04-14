# Plan: Consolidate Claude VC Slash Commands

**Date:** 2026-04-14
**Status:** Proposed
**Version bump:** 1.5.1 → 1.6.0 (breaking change)

## Context

Claude VC currently registers **18 skills**, which Claude Code surfaces as
**~34 entries** in the system-reminder (top-level name, `claude-vc:` short
name, and `claude-vc:vc-` full name — three registrations per skill). The
list is cluttered, hard to learn, and wastes context tokens.

Breakdown of the 18 skills:
- 1 orchestrator (`vc`)
- 11 user-facing sub-commands (screen, memo, terms, captable, model, kpi,
  compare, diligence, portfolio, returns, help)
- 6 internal parallel sub-agents (team, financial, market, technical,
  legal, competitive) — used only during `--full` screening, never meant
  for direct user invocation

Several user-facing commands overlap in purpose:
- `compare` is just `screen` with multiple inputs
- `diligence` checklist is already a standard section of a memo
- `kpi`, `returns`, and `portfolio` all operate on existing portfolio data

## Guiding Philosophy

**Maximum functionality, minimum cognitive load.** Fewer commands that each
do more, organized around how a VC actually works through a deal:

1. **Evaluate** a deal → `screen`
2. **Write it up** → `memo`
3. **Analyze deal documents** → `terms`
4. **Model equity structure** → `captable`
5. **Model financials** → `model`
6. **Monitor existing investments** → `portfolio`

Each command is scoped so a single invocation completes in a reasonable time
window (most paths under ~5 minutes; `--full` screening with 6 parallel
sub-agents remains the heavy option when depth is needed). Functionality is
preserved — nothing is removed, only regrouped.

## Command Consolidation

| New command | Replaces | Rationale |
|---|---|---|
| `/vc screen <input(s)> [--full]` | screen, compare | Multiple inputs → comparison. Same analysis, different N. |
| `/vc memo <input> [--diligence-only]` | memo, diligence | DD checklist is part of any memo; flag surfaces just the checklist when that's all you want. |
| `/vc terms <file>` | terms | Unchanged. |
| `/vc captable <input>` | captable | Unchanged. |
| `/vc model <input>` | model | Unchanged. |
| `/vc portfolio <data> [--kpi\|--returns]` | portfolio, kpi, returns | All three are post-investment analytics on portfolio data. Flags focus the output. |
| `/vc help` | help | Inlined into the orchestrator (no separate skill file). |

**Result: 10 user-facing sub-commands → 6 functional commands + help.**

## New Repository Structure

```
skills/vc/
  SKILL.md              ← the ONLY registered skill (orchestrator + help)
  commands/
    screen.md           ← screen + compare (multi-input aware)
    memo.md             ← memo + diligence checklist
    terms.md
    captable.md
    model.md
    portfolio.md        ← portfolio + kpi + returns
  agents/               ← internal prompts, not registered as skills
    team.md
    financial.md
    market.md
    technical.md
    legal.md
    competitive.md
  references/           ← unchanged (investment-criteria, disclaimers, etc.)
  scripts/              ← unchanged (captable.py, financial_model.py)
  config/               ← unchanged (firm-criteria.md.example, etc.)
```

**Deleted: all 17 `skills/vc-*/` directories.**

Since Claude Code only auto-discovers skills at `skills/*/SKILL.md`, nesting
them under `skills/vc/commands/` and `skills/vc/agents/` makes them invisible
to the registration system while remaining accessible to the orchestrator via
`Read` + "follow these instructions".

## Changes

### 1. Orchestrator (`skills/vc/SKILL.md`)

- Rewrite routing: each command dispatch becomes "Read
  `${CLAUDE_SKILL_DIR}/commands/<name>.md` and follow its instructions"
  instead of `Skill("vc-<name>", args)`.
- Inline the help block (kill vc-help entirely).
- Update intent-matching keywords:
  - "compare", "versus", "side by side" → `/vc screen` (multi-input)
  - "diligence", "DD", "checklist" → `/vc memo --diligence-only`
  - "KPI", "metrics", "benchmarks" → `/vc portfolio --kpi`
  - "IRR", "MOIC", "DPI", "returns" → `/vc portfolio --returns`
- Default workflow (URL with no command) remains: screen → memo (memo now
  includes diligence, so the chain shortens by one step).

### 2. Merged command files

- **`commands/screen.md`** — consolidate vc-screen + vc-compare. Detect N
  from the input count. If N=1, run single-company analysis. If N≥2, run
  comparison mode. Preserve `--full` for 6-agent parallel screening.
- **`commands/memo.md`** — consolidate vc-memo + vc-diligence. DD checklist
  is a standard memo section. `--diligence-only` emits just the checklist.
- **`commands/portfolio.md`** — consolidate vc-portfolio + vc-kpi +
  vc-returns. Auto-detect output type from input data, or dispatch via
  `--kpi` / `--returns` flag to focus on one artifact.

### 3. Unchanged command files (strip frontmatter only)

- `commands/terms.md` ← vc-terms
- `commands/captable.md` ← vc-captable
- `commands/model.md` ← vc-model

### 4. Agent files (6 files, strip frontmatter)

- Move all 6 sub-agent prompts to `skills/vc/agents/`.
- Update `commands/screen.md` to `Read` each agent file and spawn via the
  Agent/Task tool in parallel (preserves the 6-way concurrency of `--full`
  screening).

### 5. Documentation updates

- **`README.md`** — rewrite the command reference table, update all usage
  examples, update the "What it does" section to show 6 commands.
- **`CLAUDE.md`** — update the Key Paths section; remove references to the
  17 deleted directories.
- **`ARCHITECTURE.md`** — update the skill architecture diagram and
  description.
- **`docs/frontier.md`** — no capability changes, but add a changelog entry
  noting the consolidation (2026-04-14, organizational change).
- **`docs/user-guide.md`** — rewrite to teach the 6-command model.
- **`docs/decisions/`** — add an ADR recording this consolidation decision
  (`2026-04-14-slash-command-consolidation.md`).
- **`docs/specs/`** — review for stale path references; update if needed.

### 6. Plugin metadata

- **`.claude-plugin/plugin.json`** — bump version to `1.6.0`.
- **`package.json`** — bump version to `1.6.0`, update description if it
  references the old command list.
- **`.npmignore`** — verify `skills/vc/commands/` and `skills/vc/agents/`
  are included (they will be by default, but double-check no exclusion
  rules catch them).

### 7. Tests

- **Layer 1 (unit/integration)** — update any test in `tests/` that
  references old skill paths (`skills/vc-screen/`, etc.).
- **Layer 2 (smoke tests)** — rewrite to use the 6 new commands. Add a
  smoke test for each consolidation:
  - `/vc screen <url1> <url2>` → comparison mode works
  - `/vc memo --diligence-only` → emits checklist only
  - `/vc portfolio --kpi` and `--returns` → both focus modes work

## What's Preserved

- All existing analysis capabilities (zero feature loss).
- 6-agent parallel screening for `--full`.
- Python computation scripts unchanged.
- Reference files unchanged.
- Firm customization config unchanged.
- Export formats (markdown, DOCX, XLSX) unchanged.

## What's Lost (Acceptable)

- Direct top-level invocation of `/vc-screen`, `/vc-memo`, etc. Only
  `/vc <subcommand> ...` works. This is a breaking change, justifying the
  minor version bump.
- Internal sub-agents no longer show as slash commands (intentional —
  they never should have).

## Execution Order

1. Create `skills/vc/commands/` and `skills/vc/agents/` directories.
2. Write the 3 merged command files (screen, memo, portfolio) by combining
   content from source SKILL.md files.
3. Move the 3 unchanged commands (terms, captable, model), stripping
   frontmatter.
4. Move the 6 agent prompts, stripping frontmatter.
5. Rewrite `skills/vc/SKILL.md` with Read-based routing and inlined help.
6. Delete all 17 `skills/vc-*/` directories.
7. Update `README.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `docs/user-guide.md`,
   `docs/frontier.md`.
8. Write the ADR at `docs/decisions/2026-04-14-slash-command-consolidation.md`.
9. Update tests (Layer 1 + Layer 2).
10. Bump version to 1.6.0 in `plugin.json` + `package.json`.
11. Run: `ruff check`, `ruff format`, `pyright`, `uv run pytest`, `gitleaks`.
12. Commit (awaiting explicit user go-ahead, per CLAUDE.md).

## Verification

- `ls skills/` shows only `vc/` (no `vc-*/` directories).
- `uv run pytest` — all Layer 1 tests pass.
- `uv run pytest -m smoke` — Layer 2 smoke tests pass.
- System-reminder shows ~3 VC entries (down from ~34).
- `/vc help` displays exactly 6 commands.
- `/vc screen url1 url2` runs comparison.
- `/vc screen url --full` spawns 6 parallel agents.
- `/vc memo url --diligence-only` emits DD checklist only.
- `/vc portfolio data.csv --returns` computes IRR/MOIC/DPI.
- `/vc portfolio data.csv --kpi` computes company KPI dashboard.
- Old workflow still works: `/vc <url>` → default screen→memo chain.

## Open Questions

None — the user has approved the philosophy of max functionality with
consolidation, the 6-command target, and a full-repository revamp scope.
