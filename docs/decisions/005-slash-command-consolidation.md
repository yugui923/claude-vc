# ADR-005: Consolidate to a Single Skill with Six Sub-Commands

**Status**: Accepted
**Date**: 2026-04-14
**Deciders**: Yuri Gui
**Supersedes partial aspects of**: [ADR-001](001-skill-architecture.md)
**Version**: Shipped in v2.0.0

## Context

Up through v1.5.1, claude-vc shipped 18 separate skill directories under
`skills/`: 1 orchestrator (`vc`), 11 user-facing sub-skills (`vc-screen`,
`vc-memo`, `vc-terms`, `vc-captable`, `vc-model`, `vc-kpi`, `vc-compare`,
`vc-diligence`, `vc-portfolio`, `vc-returns`, `vc-help`), and 6 internal
parallel sub-agents (`vc-financial`, `vc-market`, `vc-technical`,
`vc-legal`, `vc-competitive`, `vc-team`).

Claude Code auto-discovers every `skills/*/SKILL.md` and registers each
under multiple names (top-level, plugin-namespaced short name, and
plugin-namespaced full name), producing approximately 34 slash command
entries from these 18 skills. The slash command registry became cluttered
and difficult to learn. The 6 internal sub-agents — never intended for
direct user invocation — were also surfaced as slash commands, even though
they only run inside `/vc screen --full`.

Additionally, several user-facing commands overlapped in purpose:

- `compare` was `screen` with multiple inputs.
- `diligence` produced a DD checklist that was also a standard section of
  a memo.
- `kpi`, `returns`, and `portfolio` all operated on post-investment data
  with different focal outputs.

## Decision

Consolidate claude-vc into a **single registered skill** (`vc`) with six
functional sub-commands plus help, organized by what the user is doing in a
VC workflow:

| Sub-command           | Replaces                     | Purpose                                                |
| --------------------- | ---------------------------- | ------------------------------------------------------ |
| `/vc screen`          | `screen` + `compare`         | 1 input = screen, 2-4 inputs = comparison              |
| `/vc memo`            | `memo` + `diligence`         | Memo with DD checklist built in (`--diligence-only`)   |
| `/vc terms`           | `terms`                      | Unchanged                                              |
| `/vc captable`        | `captable`                   | Unchanged                                              |
| `/vc model`           | `model`                      | Unchanged                                              |
| `/vc portfolio`       | `portfolio` + `kpi` + `returns` | Default = portfolio report; `--kpi`, `--returns` flags |
| `/vc help`            | `help`                       | Inlined into orchestrator (no separate file)           |

### Structural Changes

1. **Only `skills/vc/SKILL.md` is registered as a skill.** All 17
   `skills/vc-*/` directories are deleted.

2. **Sub-command prompts move to `skills/vc/commands/`.** The orchestrator
   dispatches via `Read` + "follow these instructions" instead of the
   `Skill` tool.

3. **Sub-agent prompts move to `skills/vc/agents/`.** The screen command
   spawns them via the `Agent/Task` tool after reading the prompt file,
   preserving the parallel-execution pattern from ADR-001.

4. **The top-level `commands/` directory is removed.** Earlier versions
   included thin slash-command wrappers (e.g. `commands/screen.md`) so
   `/screen` would route to `vc-screen`. These wrappers contributed to
   the registry clutter and are no longer needed — all commands go through
   `/vc <subcommand>`.

### Principle

**Maximum functionality, minimum cognitive load.** Fewer commands, each
doing more, organized around how a VC actually works a deal. Functionality
is preserved — nothing is removed, only regrouped under flags.

## Alternatives Considered

### Keep all 11 user-facing sub-skills, just hide the 6 internal sub-agents

Would only remove 6 of the ~34 registry entries. The slash command list
would still be ~22 entries and would not solve the overlap problems
(compare vs. screen, diligence vs. memo, kpi/returns vs. portfolio).

**Rejected because**: half-measure that leaves most of the clutter and
doesn't simplify the user's mental model.

### Keep the orchestrator + sub-skill pattern; just rename to reduce clutter

Claude Code's registration mechanism is filesystem-based — it registers
every `skills/*/SKILL.md` regardless of naming. Renaming alone would not
prevent registration.

**Rejected because**: can't solve the problem without restructuring.

### Monolithic `SKILL.md`

Inline all command and sub-agent logic into a single SKILL.md file.

**Rejected because**: the file would exceed the 500-line / 5000-token
constraint from ADR-001, consume excessive context on every invocation,
and defeat progressive disclosure.

## Consequences

### Positive

- **~34 slash-command registry entries → ~3**. Much cleaner slash command
  surface in the system-reminder.
- **Internal sub-agents are no longer user-visible.** They can only run
  inside `/vc screen --full`, as intended.
- **Fewer, more functional commands.** Six commands cover the full VC
  workflow — each combines related capabilities under clear flag names
  (`--kpi`, `--returns`, `--diligence-only`, comparison via multiple
  inputs).
- **Single installation unit.** `install.sh` copies one directory; there
  is no risk of partial installation or version drift between sub-skills.
- **Progressive disclosure is preserved.** The orchestrator loads command
  prompts on demand via `Read`. Reference files still load only when
  needed.
- **Parallel execution is preserved.** Full screening still spawns 6
  concurrent sub-agents via `Agent/Task`.

### Negative

- **Breaking change for direct invocations.** Users who called
  `/vc-screen`, `/vc-memo`, etc. at the top level, or `/screen`, `/memo`
  via the `commands/` wrappers, must now use `/vc screen`, `/vc memo`.
  This justifies the major version bump to 2.0.0.
- **Installation must clean up prior versions.** `install.sh` explicitly
  removes the old `skills/vc-*/`, `commands/vc-*`, and `agents/vc-*.md`
  files so users upgrading from 1.5.x do not see stale entries.
- **Contribution patterns change.** The CONTRIBUTING guide's "Adding a
  New Sub-Skill" section was rewritten. Contributors now add files under
  `skills/vc/commands/` and `skills/vc/agents/`, not new top-level skill
  directories.
- **`skills/vc/SKILL.md` becomes slightly longer** (inlined help block,
  expanded routing table). Still well under the 500-line limit.

## Relationship to Prior ADRs

[ADR-001](001-skill-architecture.md) established the orchestrator +
sub-skills + sub-agents pattern. This ADR preserves the **logical** pattern
— orchestration, on-demand prompt loading, parallel sub-agents — but
changes the **file-system representation** so that only one directory is
auto-registered as a skill. The architectural benefits ADR-001 articulated
(progressive disclosure, Python for computation, extension system,
parallel agents) are all intact.
