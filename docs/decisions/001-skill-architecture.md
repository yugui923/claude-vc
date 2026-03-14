# ADR-001: Adopt Claude-SEO Skill Architecture Pattern

**Status**: Accepted
**Date**: 2026-03-13
**Deciders**: Yuri Gui

## Context

We need an architecture for a Claude Code extension that provides venture capital workflow automation. The key requirements are:

1. Multiple distinct workflows (screening, memos, cap tables, terms, portfolio)
2. Some workflows benefit from parallel analysis (e.g., screening needs financial, market, technical, and legal analysis simultaneously)
3. Domain knowledge must be available but cannot consume the entire context window
4. Computation-heavy tasks (financial models, cap tables) need Python, not just LLM reasoning
5. External data sources (Crunchbase, SEC EDGAR) should be optional add-ons
6. Distribution should be simple for individual users

## Decision

Adopt the **orchestrator + sub-skills pattern** from [claude-seo](https://github.com/AgriciDaniel/claude-seo), which has proven this architecture at scale (2,200+ stars).

### Architecture Components

| Component       | Claude-SEO                              | Claude-VC                            |
| --------------- | --------------------------------------- | ------------------------------------ |
| Orchestrator    | `seo/SKILL.md`                          | `skills/vc/SKILL.md`                 |
| Sub-skills      | 12 (`seo-audit`, `seo-schema`, ...)     | 6 (`vc-screen`, `vc-memo`, ...)      |
| Parallel agents | 7 (`seo-technical`, `seo-content`, ...) | 6 (`vc-financial`, `vc-market`, ...) |
| Reference files | 4 (`cwv-thresholds.md`, ...)            | 6 (`valuation-methods.md`, ...)      |
| Python scripts  | 4 (`fetch_page.py`, ...)                | 3 (`financial_model.py`, ...)        |
| Extensions      | 1 (DataForSEO)                          | 2+ (Crunchbase, SEC EDGAR)           |

### Key Architectural Decisions

1. **Skill per workflow, not skill per action**: Each `/vc` subcommand maps to a complete workflow, not an atomic operation. `/vc screen` orchestrates an entire screening process, not just "fetch company data."

2. **Agents for parallel analysis, sub-skills for focused workflows**: Agents are spawned when multiple independent analyses can run concurrently (financial + market + technical). Sub-skills handle sequential, focused workflows (cap table modeling, term sheet parsing).

3. **Progressive disclosure for domain knowledge**: Reference files (`valuation-methods.md`, `term-sheet-terms.md`) load only when the active sub-skill needs them. They never load at session startup.

4. **Python for computation, Claude for judgment**: Financial calculations (DCF, dilution math, waterfall distributions) run in Python scripts invoked via Bash. Claude handles interpretation, synthesis, and recommendation generation.

5. **Plugin format for distribution**: Use `.claude-plugin/plugin.json` manifest alongside `install.sh` for compatibility with both the plugin system and manual installation. Also support `npx skills` for the Agent Skills standard.

## Alternatives Considered

### MCP Server

Build a standalone MCP server that exposes VC tools.

**Rejected because**: MCP servers are best for stateless tool calls (API wrappers, data fetching). VC workflows are inherently multi-step and judgment-heavy. The skill pattern gives Claude the domain knowledge and workflow instructions that an MCP server cannot provide. Extensions that wrap external APIs (Crunchbase, SEC EDGAR) do use MCP servers -- this is the right boundary.

### Standalone CLI Application

Build a Python CLI that Claude Code invokes as a single tool.

**Rejected because**: This puts the orchestration logic outside Claude, losing the benefit of LLM judgment in routing and synthesis. It also makes the system opaque to users who want to customize workflows.

### Monolithic SKILL.md

Put all VC knowledge and workflows in a single large SKILL.md.

**Rejected because**: A comprehensive VC skill would exceed the 500-line / 5000-token limit. It would consume excessive context window on every invocation, even for simple tasks. Progressive disclosure requires splitting into orchestrator + sub-skills + reference files.

## Consequences

### Positive

- Proven architecture with community validation (claude-seo)
- Clean separation of concerns (routing vs. analysis vs. computation)
- Token-efficient through progressive disclosure
- Extensible via the extension system
- Distributable via multiple channels (install.sh, npx skills, plugin marketplace)

### Negative

- More files to maintain than a monolithic approach
- Users must install to `~/.claude/` (not project-scoped by default)
- Subagents cannot spawn other subagents (limits nesting depth to 1)
- Parallel agent results must be aggregated by the orchestrator, which can be token-intensive for large analyses
