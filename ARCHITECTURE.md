# Claude-VC Architecture

> Living document. Update when core structure changes.

## Overview

Claude-VC is a Claude Cowork and Claude Code plugin for venture capital
workflows. It is distributed as a **single registered skill** (`vc`) that
exposes six functional sub-commands plus help, organized around the VC
workflow: evaluate deals, write memos, analyze terms, model equity, build
financials, and monitor portfolios.

The system is installed into `~/.claude/` and invoked via `/vc` slash
commands. It is **not** an MCP server or standalone application — it is a
single skill composed of markdown-based prompts, Python computation scripts,
and on-demand reference files that extend Claude's capabilities for VC
professionals. It works across both Claude Cowork (desktop app) and Claude
Code (CLI and IDE).

**Design principle**: The value of this tool is _judgment_, not data access.
The inputs are public data and user-provided documents. The intelligence is
knowing what to check, how to score, and what to recommend. Data
infrastructure (CRM, dashboards, scheduled pipelines) belongs in a proper
application, not a CLI skill. See
[ADR-004](docs/decisions/004-scope-boundaries.md) for full scope boundaries.

## System Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                       User Input                             │
│   /vc <url or file>           (default: screen → memo)       │
│   /vc screen <input(s)> [--full]                             │
│   /vc memo <input> [--diligence-only]                        │
│   /vc terms <file>                                           │
│   /vc captable <input>                                       │
│   /vc model <input>                                          │
│   /vc portfolio <data> [--kpi | --returns]                   │
│   /vc help                                                   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│       Orchestrator: skills/vc/SKILL.md                       │
│                                                              │
│  Parses the first argument, dispatches to a command prompt   │
│  via Read, or spawns parallel sub-agents (full screening).   │
│  Loads reference files on demand. Aggregates sub-agent       │
│  findings into unified output.                               │
└──┬─────────┬─────────┬─────────┬─────────┬──────────┬────────┘
   │         │         │         │         │          │
   ▼         ▼         ▼         ▼         ▼          ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌───────┐ ┌──────┐ ┌──────────┐
│screen│ │memo  │ │terms │ │captabl│ │model │ │portfolio │
│ .md  │ │ .md  │ │ .md  │ │ .md   │ │ .md  │ │ .md      │
└──┬───┘ └──┬───┘ └──────┘ └───────┘ └──────┘ └──────────┘
   │(--full)│(--comprehensive)
   ▼        ▼
┌──────────────────────────────────────────────────┐
│      Parallel Sub-Agents (skills/vc/agents/)     │
│  ┌─────────────┐  ┌─────────────┐                │
│  │financial.md │  │market.md    │                │
│  └─────────────┘  └─────────────┘                │
│  ┌─────────────┐  ┌─────────────┐                │
│  │technical.md │  │legal.md     │                │
│  └─────────────┘  └─────────────┘                │
│  ┌─────────────┐  ┌─────────────┐                │
│  │competitive  │  │team.md      │                │
│  │   .md       │  │             │                │
│  └─────────────┘  └─────────────┘                │
└──────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────┐
│  Python Scripts (skills/vc/scripts/) via Bash    │
│  - financial_model.py                            │
│  - captable.py                                   │
└──────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────┐
│  Extensions (optional MCP servers)               │
│  - Octagon AI ($17/mo, priority)                 │
│  - SEC EDGAR (free, raw filings)                 │
│  - Crunchbase (Enterprise, ~$10K+/yr)            │
│  - PitchBook (institutional)                     │
└──────────────────────────────────────────────────┘
```

## Directory Structure

```text
claude-vc/
├── .claude-plugin/
│   ├── plugin.json                     # Plugin manifest
│   └── marketplace.json                # Marketplace catalog
├── skills/
│   └── vc/                             # THE SINGLE REGISTERED SKILL
│       ├── SKILL.md                    # Orchestrator + routing + help
│       ├── commands/                   # Sub-command prompts (loaded via Read)
│       │   ├── screen.md               # screen + compare
│       │   ├── memo.md                 # memo + DD checklist (--diligence-only)
│       │   ├── terms.md
│       │   ├── captable.md
│       │   ├── model.md
│       │   └── portfolio.md            # portfolio + kpi (--kpi) + returns (--returns)
│       ├── agents/                     # Parallel sub-agent prompts (Agent/Task)
│       │   ├── team.md
│       │   ├── financial.md
│       │   ├── market.md
│       │   ├── technical.md
│       │   ├── legal.md
│       │   └── competitive.md
│       ├── references/                 # On-demand domain knowledge
│       │   ├── investment-criteria.md
│       │   ├── valuation-methods.md
│       │   ├── disclaimers.md
│       │   ├── due-diligence-checklist.md
│       │   ├── term-sheet-terms.md
│       │   ├── safe-mechanics.md
│       │   └── industry-multiples.md
│       ├── scripts/                    # Python computation
│       │   ├── financial_model.py
│       │   └── captable.py
│       └── config/                     # Firm customization (user-managed)
│           ├── README.md
│           ├── firm-criteria.md.example
│           └── firm-templates.md.example
├── extensions/                         # OPTIONAL MCP ADD-ONS
│   ├── octagon/                       # Priority: $17/mo, broadest VC data
│   │   ├── install.sh
│   │   ├── skills/vc-octagon/SKILL.md
│   │   └── agents/vc-octagon.md
│   └── sec-edgar/                     # Free, raw filing access
│       ├── install.sh
│       ├── skills/vc-edgar/SKILL.md
│       └── agents/vc-edgar.md
├── install.sh                          # Unix/macOS installer (fallback)
├── uninstall.sh
├── update.sh
├── package.json                        # npm metadata for npx skills distribution
├── docs/                               # Documentation
│   ├── decisions/                      # ADRs
│   ├── specs/                          # Skill specifications
│   └── plans/                          # Implementation plans
├── ARCHITECTURE.md                     # This file
├── LICENSE                             # MIT
└── README.md
```

### Installed Layout

The plugin marketplace copies the repo as-is; `install.sh` replicates the
same structure under `~/.claude/`.

```text
~/.claude/
└── skills/
    └── vc/
        ├── SKILL.md
        ├── commands/
        ├── agents/
        ├── references/
        ├── scripts/
        └── config/
```

Only **one** skill is registered (`vc`), which produces one top-level slash
command (`/vc`) with six sub-commands plus help.

## Key Design Patterns

### 1. Single Registered Skill with Sub-Commands

Claude Code auto-discovers every `skills/*/SKILL.md` at install time and
registers each as a slash command. Earlier versions of Claude-VC (v1.5.x
and below) shipped 18 separate `vc-*` skill directories, which Claude Code
registered multiple times each (top-level, `claude-vc:` short name,
`claude-vc:vc-` full name), producing ~34 entries in the slash command
registry.

In v2.0.0 this was consolidated: the orchestrator (`skills/vc/SKILL.md`) is
the only registered skill, and its sub-commands and sub-agent prompts live
as plain markdown files under `skills/vc/commands/` and `skills/vc/agents/`.
The orchestrator loads them on demand via the `Read` tool and follows their
instructions, or passes them to the `Agent/Task` tool for parallel execution.

See [ADR-005](docs/decisions/005-slash-command-consolidation.md) for the
rationale.

### 2. Parallel Sub-Agents

For comprehensive analyses (`/vc screen --full` or
`/vc memo --comprehensive`), the orchestrator spawns 6 sub-agents
concurrently via the Agent/Task tool. Each agent is loaded from its prompt
file in `skills/vc/agents/` and runs in a forked context with its own
persona and tool access. Each produces a structured markdown output ending
in a `FINDINGS_SUMMARY` line that the orchestrator aggregates into a unified
Deal Score and memo.

### 3. Progressive Disclosure

Only the orchestrator's name and description load into context at session
start. The full `SKILL.md` instructions load on invocation. Command and
sub-agent prompt files load only when needed. Reference files (valuation
methods, DD checklists, SAFE mechanics) load only when the active command
needs them. This is critical for token efficiency.

### 4. Python Scripts for Computation

Financial modeling, cap table calculations, and fund returns are implemented
as CLI Python scripts in `skills/vc/scripts/`. Claude invokes them via the
Bash tool. Scripts use `argparse` for CLI interface and output JSON for
structured results.

### 5. Data Source Hierarchy

All research-oriented commands and sub-agents follow a consistent priority
when gathering information:

1. **MCP data sources** (if available): Octagon AI, SEC EDGAR, or other MCP
   tools provide the most reliable structured data.
2. **Company-provided materials**: Pitch decks, websites, data room
   documents.
3. **Institutional sources**: Published reports, SEC filings, press releases.
4. **Web search**: Last resort, always cross-referenced.

No MCP data source is ever required — all analysis works without them. This
pattern ensures data quality improves automatically as MCP integrations come
online without changing command logic.

### 6. Firm Customization

Users can drop firm-specific config files into `skills/vc/config/` to
override default scoring criteria, output templates, and formatting.
Commands check for config files before loading defaults. See
`skills/vc/config/README.md` for details.

### 7. Extension System

Optional extensions integrate external data via MCP servers. **Octagon AI**
($17/mo) is the priority extension — it provides private company data,
funding rounds, investor profiles, and SEC analysis through a single MCP
server. SEC EDGAR is free for raw filing access. Each extension has its own
installer, skills, agents, and MCP configuration. Extensions are fully
independent — the core system works without them.

## Scope Boundaries

Claude-VC is the **analysis and report generation layer**, not the data
infrastructure layer.

**In scope** (judgment-heavy, text in/text out):

- Analyze startup websites and products (public pages)
- Parse and score pitch deck PDFs (Claude reads PDFs natively)
- Generate deal memos from provided data
- Analyze term sheets and SAFEs against market standards
- Model cap tables and dilution scenarios
- Parse SEC/EDGAR public filings
- Compare companies side-by-side (parallel sub-agent pattern)
- Generate DD checklists (as part of the memo command)

**Out of scope** (data infrastructure, needs a proper app):

- CRM/pipeline tracking (needs persistent state, OAuth)
- Portfolio monitoring dashboards (needs a UI runtime)
- Scheduled/automated data pulls (needs a cron process)
- Large dataset processing (context window limits)
- Real-time deal flow alerts (needs push notifications)

See [ADR-004](docs/decisions/004-scope-boundaries.md) for the full analysis.

## Data Flow

### Default Workflow (`/vc <url>`)

1. Orchestrator parses the URL or file input.
2. Loads `commands/screen.md` and performs a quick screen, producing a Deal
   Score.
3. Loads `commands/memo.md` and generates the full 12-section memo using the
   screening results as context. The memo's Section 12 is the tailored DD
   checklist.

### Deal Screening (`/vc screen <url>`)

1. Orchestrator loads `commands/screen.md`.
2. **1 input, no `--full`**: Quick screen. Fetches company data, runs
   scoring, produces single-company output.
3. **1 input with `--full`**: Spawns 6 parallel sub-agents
   (`agents/financial.md`, `market.md`, `technical.md`, `legal.md`,
   `competitive.md`, `team.md`). Aggregates into Deal Score with breakdown.
4. **2-4 inputs**: Comparison mode. Spawns one scoring agent per company,
   builds a side-by-side comparison matrix.

### Memo Generation (`/vc memo <input>`)

1. Orchestrator loads `commands/memo.md`.
2. Uses prior screening context if available, otherwise fetches input data.
3. With `--comprehensive`: triggers the same 6-agent parallel analysis as
   `/vc screen --full` before writing the memo.
4. With `--diligence-only`: emits just the DD checklist (Section 12) as a
   standalone document.
5. Generates 12 sections and a stage/sector-tailored DD checklist.

### Cap Table Modeling (`/vc captable <input>`)

1. Orchestrator loads `commands/captable.md`.
2. Claude parses input (CSV, JSON, or natural language) into a JSON scenario.
3. Invokes `skills/vc/scripts/captable.py <command>` for mathematical
   computation (model, dilution, waterfall, convert, scenarios).
4. Returns ownership breakdown, dilution scenarios, and waterfall analysis.

### Financial Model (`/vc model <input>`)

1. Orchestrator loads `commands/model.md`.
2. Derives reasonable defaults from stage and sector; loads
   `references/industry-multiples.md` for benchmarks.
3. Invokes `scripts/financial_model.py three_statement`.
4. Returns 3-statement model (income statement, balance sheet, cash flow)
   with analysis.

### Portfolio Analytics (`/vc portfolio <data>`)

1. Orchestrator loads `commands/portfolio.md`.
2. **Default**: Full portfolio report — summary, composition, dashboard,
   cohort analysis, concentration risk, follow-on needs, exits/write-offs,
   LP narrative. Exports markdown + DOCX + XLSX.
3. **`--kpi`**: KPI dashboard for a single company. Auto-detects company
   type (SaaS, marketplace, consumer, fintech). For SaaS, invokes
   `scripts/financial_model.py unit_economics`. Loads
   `references/industry-multiples.md` for benchmarks.
4. **`--returns`**: Fund-level returns. Invokes
   `scripts/financial_model.py returns` for IRR, MOIC, DPI, TVPI, PME.

### Term Sheet Analysis (`/vc terms <file>`)

1. Orchestrator loads `commands/terms.md`.
2. Loads `references/term-sheet-terms.md` for NVCA baseline and
   `references/safe-mechanics.md` if analyzing a SAFE or convertible note.
3. Flags non-standard or founder-unfriendly terms.
4. Generates annotated analysis with market comparisons.

## Technology Stack

| Component       | Technology                                     | Rationale                                                                                |
| --------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Skill & prompts | Markdown + YAML frontmatter                    | Claude Cowork / Code native format                                                       |
| Computation     | Python 3.10+ (stdlib only)                     | Financial calculations Claude can't do natively                                          |
| Extensions      | MCP servers                                    | Standard Claude Cowork / Code extension pattern                                          |
| Distribution    | Plugin marketplace, `npx skills`, `install.sh` | Marketplace preferred; `npx skills add` for cross-agent compat; shell script as fallback |
| License         | MIT                                            | Matches claude-seo precedent                                                             |

## Constraints

- `SKILL.md` must stay under 500 lines / 5000 tokens
- Each command and sub-agent prompt file should stay under 500 lines
- Reference files must stay under 200 lines where practical
- Python scripts must use only stdlib for core functionality (httpx/pydantic
  for optional features)
- Sub-agents cannot spawn other sub-agents (Claude Cowork / Code limitation)
- All financial outputs include regulatory disclaimers (see ADR-003)
- No investment advice — tool is for analysis and information only

## Related Documents

- [ADR-001: Skill Architecture](docs/decisions/001-skill-architecture.md)
- [ADR-002: Data Sources](docs/decisions/002-data-sources.md)
- [ADR-003: Regulatory Disclaimers](docs/decisions/003-regulatory-disclaimers.md)
- [ADR-004: Scope Boundaries](docs/decisions/004-scope-boundaries.md)
- [ADR-005: Slash Command Consolidation](docs/decisions/005-slash-command-consolidation.md)
- [Skill System Spec](docs/specs/skill-system.md)
