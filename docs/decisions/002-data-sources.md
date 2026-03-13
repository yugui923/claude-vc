# ADR-002: Data Source Strategy

**Status**: Accepted
**Date**: 2026-03-13
**Deciders**: Yuri Gui

## Context

VC workflows require external data: company information, market data, financial filings, competitive intelligence. We need to decide which data sources to support and how to integrate them.

Key considerations:

- Core functionality must work without any external API keys
- Some data sources have free tiers, others require paid subscriptions
- Data freshness vs. static reference material tradeoff
- Canadian/international users need sources that work globally

## Decision

### Three-Tier Data Architecture

**Tier 1 -- Built-in (no API keys)**:

- Claude's training data for general market knowledge
- WebFetch/WebSearch for public company websites and press releases
- Static reference files (valuation multiples, DD checklists, NVCA terms)
- User-provided documents (pitch decks, term sheets, cap tables)

**Tier 2 -- Free Extensions (free API keys)**:

- **SEC EDGAR**: US public company filings, free API (10 req/sec with User-Agent)
- **Crunchbase Basic API**: Company profiles, funding rounds (free tier: 200 req/day)
- **OpenCorporates**: Corporate registry data (free tier available)

**Tier 3 -- Paid Extensions (subscription required)**:

- **PitchBook**: Comprehensive private company data (institutional subscription)
- **Affinity CRM**: Deal flow and relationship tracking (team subscription)
- **CB Insights**: Market intelligence and trend data (enterprise subscription)

### Integration Pattern

Each external data source is implemented as an **extension** following the claude-seo pattern:

```
extensions/<source>/
├── install.sh              # Configures MCP server + API credentials
├── skills/<skill>/SKILL.md # Source-specific sub-skill
├── agents/<agent>.md       # Source-specific subagent
└── docs/                   # Setup documentation
```

The core orchestrator includes conditional sections:

```markdown
## Crunchbase Integration (Optional)

If Crunchbase MCP tools are available, enrich screening with:

- Funding history and investor details
- Employee count trends
- Technology signals
```

### Reference File Strategy

Static domain knowledge is encoded in reference files under `vc/references/`:

| File                         | Content                                                     | Update Frequency  |
| ---------------------------- | ----------------------------------------------------------- | ----------------- |
| `valuation-methods.md`       | DCF, comparables, precedent transactions, VC method, Berkus | Annual            |
| `due-diligence-checklist.md` | Financial, legal, technical, commercial DD items            | Quarterly         |
| `term-sheet-terms.md`        | NVCA model terms with market commentary                     | Annual            |
| `safe-mechanics.md`          | YC SAFE mechanics (pre-money, post-money, MFN, pro-rata)    | On SAFE updates   |
| `industry-multiples.md`      | Revenue/EBITDA multiples by sector and stage                | Quarterly         |
| `investment-criteria.md`     | Configurable scoring framework with default weights         | User-customizable |

## Alternatives Considered

### Require API Keys for Core Functionality

**Rejected**: Creates a high barrier to entry. Most users want to try the tool before committing to API subscriptions. The core screening and memo workflows should work with just a company URL and Claude's reasoning.

### Bundle All Data Sources in Core

**Rejected**: Would bloat installation, require complex dependency management, and force users to configure APIs they don't need. The extension pattern keeps the core lean.

### Use Only WebFetch for All External Data

**Rejected**: Web scraping is fragile and rate-limited. Structured APIs (SEC EDGAR, Crunchbase) provide more reliable and comprehensive data. However, WebFetch is the right fallback for company websites and press releases.

## Consequences

### Positive

- Zero-config startup experience (Tier 1 works immediately)
- Users add data sources incrementally as needed
- Each extension is independently installable and removable
- Free tiers cover most individual user needs

### Negative

- Quality of analysis varies significantly with data source availability
- Users with paid data sources get materially better results (acceptable tradeoff)
- Reference files need periodic updates to stay accurate
- Free API tiers have rate limits that may slow parallel agent execution
