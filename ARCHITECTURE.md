# Claude-VC Architecture

> Living document. Update when core structure changes.

## Overview

Claude-VC is a Claude Code skill ecosystem for venture capital workflows. It follows the **orchestrator + sub-skills** pattern established by [claude-seo](https://github.com/AgriciDaniel/claude-seo), adapted for deal screening, investment memo generation, cap table modeling, term sheet analysis, and portfolio monitoring.

The system is installed into `~/.claude/` and invoked via `/vc` slash commands. It is **not** an MCP server or standalone application -- it is a collection of markdown-based skills, agent definitions, Python computation scripts, and on-demand reference files that extend Claude Code's capabilities for VC professionals.

## System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     User Input                              │
│              /vc screen <url>                               │
│              /vc memo                                       │
│              /vc terms <file>                               │
│              /vc captable                                   │
│              /vc portfolio                                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Orchestrator (vc/SKILL.md)                     │
│                                                             │
│  Routes commands to sub-skills or spawns parallel agents    │
│  Loads reference files on demand                            │
│  Aggregates results into unified output                     │
└──────┬──────────┬──────────┬──────────┬─────────────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Sub-Skill│ │ Sub-Skill│ │ Sub-Skill│ │ Sub-Skill│
│ vc-screen│ │ vc-terms │ │vc-captab │ │vc-portfo │
│          │ │          │ │          │ │          │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
       │
       ▼  (full screening spawns parallel agents)
┌─────────────────────────────────────────┐
│         Parallel Subagents              │
│  ┌───────────┐  ┌───────────┐          │
│  │vc-financia│  │vc-market  │          │
│  └───────────┘  └───────────┘          │
│  ┌───────────┐  ┌───────────┐          │
│  │vc-technica│  │vc-legal   │          │
│  └───────────┘  └───────────┘          │
│  ┌───────────┐  ┌───────────┐          │
│  │vc-competit│  │vc-team    │          │
│  └───────────┘  └───────────┘          │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Python Scripts (via Bash tool)         │
│  - financial_model.py                   │
│  - captable.py                          │
│  - fetch_company.py                     │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Extensions (optional MCP servers)      │
│  - Crunchbase (free tier)               │
│  - SEC EDGAR (free)                     │
│  - PitchBook (paid, optional)           │
│  - Affinity CRM (paid, optional)        │
└─────────────────────────────────────────┘
```

## Directory Structure

```text
claude-vc/
├── .claude-plugin/
│   └── plugin.json                     # Plugin manifest
├── vc/                                 # ORCHESTRATOR
│   ├── SKILL.md                        # Entry point + routing table
│   └── references/                     # On-demand domain knowledge
│       ├── valuation-methods.md
│       ├── due-diligence-checklist.md
│       ├── term-sheet-terms.md
│       ├── safe-mechanics.md
│       ├── industry-multiples.md
│       └── investment-criteria.md
├── skills/                             # SUB-SKILLS
│   ├── vc-screen/SKILL.md
│   ├── vc-memo/SKILL.md
│   ├── vc-terms/SKILL.md
│   ├── vc-captable/SKILL.md
│   ├── vc-diligence/SKILL.md
│   └── vc-portfolio/SKILL.md
├── agents/                             # PARALLEL SUBAGENTS
│   ├── vc-financial.md
│   ├── vc-market.md
│   ├── vc-technical.md
│   ├── vc-legal.md
│   ├── vc-competitive.md
│   └── vc-team.md
├── scripts/                            # PYTHON COMPUTATION
│   ├── financial_model.py
│   ├── captable.py
│   └── fetch_company.py
├── extensions/                         # OPTIONAL MCP ADD-ONS
│   ├── crunchbase/
│   │   ├── install.sh
│   │   ├── skills/vc-crunchbase/SKILL.md
│   │   └── agents/vc-crunchbase.md
│   └── sec-edgar/
│       ├── install.sh
│       ├── skills/vc-edgar/SKILL.md
│       └── agents/vc-edgar.md
├── install.sh                          # Unix/macOS installer
├── install.ps1                         # Windows installer
├── uninstall.sh
├── requirements.txt                    # Python dependencies
├── docs/                               # Documentation
│   ├── decisions/                      # ADRs
│   ├── specs/                          # Skill specifications
│   ├── plans/                          # Implementation plans
│   └── roadmap.md
├── ARCHITECTURE.md                     # This file
├── LICENSE                             # MIT
└── README.md
```

### Installed Layout

After `install.sh`, files are copied to:

```text
~/.claude/
├── skills/
│   ├── vc/                             # Orchestrator + references
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── vc-screen/SKILL.md
│   ├── vc-memo/SKILL.md
│   ├── vc-terms/SKILL.md
│   ├── vc-captable/SKILL.md
│   ├── vc-diligence/SKILL.md
│   └── vc-portfolio/SKILL.md
└── agents/
    ├── vc-financial.md
    ├── vc-market.md
    ├── vc-technical.md
    ├── vc-legal.md
    ├── vc-competitive.md
    └── vc-team.md
```

## Key Design Patterns

### 1. Orchestrator + Sub-Skills

The `/vc` command routes to specialized sub-skills. Each sub-skill is independently invokable (`/vc screen`, `/vc terms`, etc.) and self-contained. The orchestrator coordinates multi-skill workflows like full deal screening.

### 2. Parallel Subagents

For comprehensive analyses (e.g., `/vc screen` with `--full`), the orchestrator spawns 6 subagents concurrently via the Task tool. Each agent runs in a forked context with its own persona and tool access. Results are aggregated into a unified investment memo.

### 3. Progressive Disclosure

Only skill names and descriptions load into context at session start. Full SKILL.md instructions load on invocation. Reference files (valuation methods, DD checklists, SAFE mechanics) load only when the active skill needs them. This is critical for token efficiency.

### 4. Python Scripts for Computation

Financial modeling, cap table calculations, and data fetching are implemented as CLI Python scripts. Claude invokes them via the Bash tool. Scripts use `argparse` for CLI interface and output JSON for structured results.

### 5. Extension System

Optional extensions (Crunchbase, SEC EDGAR) integrate external data via MCP servers. Each extension has its own installer, skills, agents, and MCP configuration. Extensions are fully independent -- the core system works without them.

## Data Flow

### Deal Screening (`/vc screen <url>`)

1. Orchestrator receives URL, determines screening depth (quick vs full)
2. **Quick screen**: Loads `vc-screen` sub-skill, fetches company data, runs scoring
3. **Full screen**: Spawns 6 parallel subagents:
   - `vc-financial`: Revenue analysis, burn rate, unit economics
   - `vc-market`: TAM/SAM/SOM, market dynamics, timing
   - `vc-technical`: Product/tech assessment, moat analysis
   - `vc-legal`: Corporate structure, IP, regulatory
   - `vc-competitive`: Competitive landscape, positioning
   - `vc-team`: Founders, advisors, key hires
4. Aggregates results into Deal Score (0-100) with breakdown
5. Generates structured output (memo, scorecard, or pass/consider/invest recommendation)

### Cap Table Modeling (`/vc captable`)

1. Sub-skill loads, prompts for current cap table data
2. Claude parses input (CSV, JSON, or natural language)
3. Invokes `scripts/captable.py` for mathematical computation
4. Returns ownership breakdown, dilution scenarios, waterfall analysis

### Term Sheet Analysis (`/vc terms <file>`)

1. Sub-skill loads, reads the term sheet file
2. Loads `references/term-sheet-terms.md` for NVCA baseline comparison
3. Flags non-standard or founder-unfriendly terms
4. Generates annotated analysis with market comparisons

## Technology Stack

| Component       | Technology                          | Rationale                                       |
| --------------- | ----------------------------------- | ----------------------------------------------- |
| Skills & agents | Markdown + YAML frontmatter         | Claude Code native format                       |
| Computation     | Python 3.13+ (stdlib only for core) | Financial calculations Claude can't do natively |
| Data fetching   | Python httpx (async)                | External API integration                        |
| Data modeling   | Pydantic                            | Structured output validation                    |
| Extensions      | MCP servers                         | Standard Claude Code extension pattern          |
| Distribution    | `install.sh` + `npx skills`         | Multiple installation paths                     |
| License         | MIT                                 | Matches claude-seo precedent                    |

## Constraints

- SKILL.md files must stay under 500 lines / 5000 tokens
- Reference files must stay under 200 lines
- Python scripts must use only stdlib for core functionality (httpx/pydantic for optional features)
- Subagents cannot spawn other subagents (Claude Code limitation)
- All financial outputs include regulatory disclaimers (see ADR-003)
- No investment advice -- tool is for analysis and information only

## Related Documents

- [ADR-001: Skill Architecture](docs/decisions/001-skill-architecture.md)
- [ADR-002: Data Sources](docs/decisions/002-data-sources.md)
- [ADR-003: Regulatory Disclaimers](docs/decisions/003-regulatory-disclaimers.md)
- [Skill System Spec](docs/specs/skill-system.md)
- [Roadmap](docs/roadmap.md)
