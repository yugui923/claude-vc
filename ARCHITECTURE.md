# Claude-VC Architecture

> Living document. Update when core structure changes.

## Overview

Claude-VC is a Claude Cowork and Claude Code plugin for venture capital workflows. It follows the **orchestrator + sub-skills** pattern established by [claude-seo](https://github.com/AgriciDaniel/claude-seo), adapted for deal screening, investment memo generation, cap table modeling, term sheet analysis, financial modeling, KPI reporting, and portfolio monitoring.

The system is installed into `~/.claude/` and invoked via `/vc` slash commands. It is **not** an MCP server or standalone application -- it is a collection of markdown-based skills, agent definitions, Python computation scripts, and on-demand reference files that extend Claude's capabilities for VC professionals. It works across both Claude Cowork (desktop app) and Claude Code (CLI and IDE).

**Design principle**: The value of this tool is _judgment_, not data access. Like claude-seo, the inputs are public data and user-provided documents. The intelligence is knowing what to check, how to score, and what to recommend. Data infrastructure (CRM, dashboards, scheduled pipelines) belongs in a proper application, not a CLI skill. See [ADR-004](docs/decisions/004-scope-boundaries.md) for full scope boundaries.

## System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     User Input                              │
│              /vc screen <url>                               │
│              /vc memo                                       │
│              /vc terms <file>                               │
│              /vc captable                                   │
│              /vc model                                      │
│              /vc kpi                                        │
│              /vc compare <url1> <url2>                      │
│              /vc portfolio                                  │
│              /vc returns                                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│           Orchestrator (skills/vc/SKILL.md)                 │
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
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Extensions (optional MCP servers)      │
│  - Octagon AI ($17/mo, priority)        │
│  - SEC EDGAR (free, raw filings)        │
│  - Crunchbase (Enterprise, ~$10K+/yr)   │
│  - PitchBook (institutional)            │
└─────────────────────────────────────────┘
```

## Directory Structure

```text
claude-vc/
├── .claude-plugin/
│   ├── plugin.json                     # Plugin manifest
│   └── marketplace.json                # Marketplace catalog
├── commands/                           # SLASH COMMAND WRAPPERS
│   ├── screen.md                      # /screen → vc-screen skill
│   ├── memo.md                        # /memo → vc-memo skill
│   ├── terms.md, captable.md, ...     # One per user-facing command
│   └── returns.md                     # /returns → vc-returns skill
├── skills/                             # ALL SKILLS
│   ├── vc/                             # ORCHESTRATOR
│   │   ├── SKILL.md                    # Entry point + routing table
│   │   ├── references/                 # On-demand domain knowledge
│   │   │   ├── valuation-methods.md
│   │   │   ├── due-diligence-checklist.md
│   │   │   ├── term-sheet-terms.md
│   │   │   ├── safe-mechanics.md
│   │   │   ├── industry-multiples.md
│   │   │   ├── investment-criteria.md
│   │   │   └── disclaimers.md
│   │   ├── scripts/                    # Python computation
│   │   │   ├── financial_model.py
│   │   │   └── captable.py
│   │   └── config/                     # Firm customization (user-managed)
│   │       ├── README.md
│   │       ├── firm-criteria.md.example
│   │       └── firm-templates.md.example
│   ├── vc-screen/SKILL.md              # SUB-SKILLS
│   ├── vc-memo/SKILL.md
│   ├── vc-terms/SKILL.md
│   ├── vc-captable/SKILL.md
│   ├── vc-model/SKILL.md
│   ├── vc-kpi/SKILL.md
│   ├── vc-compare/SKILL.md
│   ├── vc-diligence/SKILL.md
│   ├── vc-portfolio/SKILL.md
│   └── vc-returns/SKILL.md
├── agents/                             # PARALLEL SUBAGENTS
│   ├── vc-financial.md
│   ├── vc-market.md
│   ├── vc-technical.md
│   ├── vc-legal.md
│   ├── vc-competitive.md
│   └── vc-team.md
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

The repository's `skills/` directory maps directly to the installed layout. The plugin marketplace copies the repo as-is; `install.sh` replicates the same structure under `~/.claude/skills/`.

```text
~/.claude/
├── skills/
│   ├── vc/                             # Orchestrator + references + scripts
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── vc-screen/SKILL.md
│   ├── vc-memo/SKILL.md
│   ├── vc-terms/SKILL.md
│   ├── vc-captable/SKILL.md
│   ├── vc-model/SKILL.md
│   ├── vc-kpi/SKILL.md
│   ├── vc-compare/SKILL.md
│   ├── vc-diligence/SKILL.md
│   ├── vc-portfolio/SKILL.md
│   └── vc-returns/SKILL.md
├── commands/
│   └── *.md                           # Thin command wrappers
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

### 5. Data Source Hierarchy

All research-oriented skills follow a consistent priority when gathering information:

1. **MCP data sources** (if available): Octagon AI, SEC EDGAR, or other MCP tools provide the most reliable structured data.
2. **Company-provided materials**: Pitch decks, websites, data room documents.
3. **Institutional sources**: Published reports, SEC filings, press releases.
4. **Web search**: Last resort, always cross-referenced.

No MCP data source is ever required -- all analysis works without them. This pattern ensures data quality improves automatically as MCP integrations come online without changing skill logic.

### 6. Commands Directory

Thin `.md` wrapper files in `commands/` provide discoverability and metadata for each user-facing command. Each file contains YAML frontmatter (`description`, `argument-hint`) and a one-line body that routes to the corresponding skill. This follows the emerging plugin standard from Anthropic's financial-services-plugins.

### 7. Firm Customization

Users can drop firm-specific config files into `skills/vc/config/` to override default scoring criteria, output templates, and formatting. Skills check for config files before loading defaults. See `skills/vc/config/README.md` for details.

### 8. Extension System

Optional extensions integrate external data via MCP servers. **Octagon AI** ($17/mo) is the priority extension -- it provides private company data, funding rounds, investor profiles, and SEC analysis through a single MCP server. SEC EDGAR is free for raw filing access. Each extension has its own installer, skills, agents, and MCP configuration. Extensions are fully independent -- the core system works without them.

## Scope Boundaries

Claude-VC is the **analysis and report generation layer**, not the data infrastructure layer.

**In scope** (judgment-heavy, text in/text out):

- Analyze startup websites and products (public pages)
- Parse and score pitch deck PDFs (Claude reads PDFs natively)
- Generate deal memos from provided data
- Analyze term sheets and SAFEs against market standards
- Model cap tables and dilution scenarios
- Parse SEC/EDGAR public filings
- Compare companies side-by-side (parallel subagent pattern)
- Generate DD checklists

**Out of scope** (data infrastructure, needs a proper app):

- CRM/pipeline tracking (needs persistent state, OAuth)
- Portfolio monitoring dashboards (needs a UI runtime)
- Scheduled/automated data pulls (needs a cron process)
- Large dataset processing (context window limits)
- Real-time deal flow alerts (needs push notifications)

See [ADR-004](docs/decisions/004-scope-boundaries.md) for the full analysis.

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
3. Invokes `skills/vc/scripts/captable.py` for mathematical computation
4. Returns ownership breakdown, dilution scenarios, waterfall analysis

### Financial Model (`/vc model`)

1. Sub-skill loads, gathers company data (pitch deck context, raw financials, or assumptions)
2. Claude derives reasonable defaults for missing inputs based on stage and sector
3. Loads `skills/vc/references/industry-multiples.md` for sector benchmarks
4. Invokes `skills/vc/scripts/financial_model.py three_statement` for computation
5. Returns 3-statement model (income statement, balance sheet, cash flow) with analysis

### KPI Report (`/vc kpi`)

1. Sub-skill loads, parses company data (JSON, CSV, verbal, or prior context)
2. Auto-detects company type (SaaS, marketplace, consumer, fintech)
3. For SaaS: invokes `skills/vc/scripts/financial_model.py unit_economics` for core calculations
4. Loads `skills/vc/references/industry-multiples.md` for benchmark comparison
5. Returns structured KPI report with traffic-light health assessment

### Term Sheet Analysis (`/vc terms <file>`)

1. Sub-skill loads, reads the term sheet file
2. Loads `skills/vc/references/term-sheet-terms.md` for NVCA baseline comparison
3. Flags non-standard or founder-unfriendly terms
4. Generates annotated analysis with market comparisons

### Company Comparison (`/vc compare <url1> <url2>`)

1. Orchestrator spawns one screening subagent per company (parallel)
2. Each subagent independently analyzes its company
3. Results are aggregated into a side-by-side comparison matrix
4. Dimensions compared: market, team, product, financials, competitive position

### Returns Analysis (`/vc returns`)

1. Sub-skill loads, parses investment data (CSV, JSON, verbal, or prior portfolio context)
2. Claude builds a JSON scenario with investment dates, amounts, distributions, and NAV
3. Invokes `skills/vc/scripts/financial_model.py returns` for computation
4. Returns per-investment and portfolio-level IRR, MOIC, DPI, TVPI, PME with benchmarks

### Pitch Deck Analysis (`/vc screen <file.pdf>`)

1. `vc-screen` sub-skill detects PDF input (Claude reads PDFs natively)
2. Extracts structured data: team, market, product, financials, ask
3. Scores against investment criteria framework
4. Optionally spawns parallel agents for deep analysis (`--full`)

## Technology Stack

| Component       | Technology                       | Rationale                                       |
| --------------- | -------------------------------- | ----------------------------------------------- |
| Skills & agents | Markdown + YAML frontmatter      | Claude Cowork / Code native format              |
| Computation     | Python 3.10+ (stdlib only)       | Financial calculations Claude can't do natively |
| Extensions      | MCP servers                      | Standard Claude Cowork / Code extension pattern |
| Distribution    | Plugin marketplace, `npx skills`, `install.sh` | Marketplace preferred; `npx skills add` for cross-agent compat; shell script as fallback |
| License         | MIT                              | Matches claude-seo precedent                    |

## Constraints

- SKILL.md files must stay under 500 lines / 5000 tokens
- Reference files must stay under 200 lines
- Python scripts must use only stdlib for core functionality (httpx/pydantic for optional features)
- Subagents cannot spawn other subagents (Claude Cowork / Code limitation)
- All financial outputs include regulatory disclaimers (see ADR-003)
- No investment advice -- tool is for analysis and information only

## Related Documents

- [ADR-001: Skill Architecture](docs/decisions/001-skill-architecture.md)
- [ADR-002: Data Sources](docs/decisions/002-data-sources.md)
- [ADR-003: Regulatory Disclaimers](docs/decisions/003-regulatory-disclaimers.md)
- [ADR-004: Scope Boundaries](docs/decisions/004-scope-boundaries.md)
- [Skill System Spec](docs/specs/skill-system.md)
