# ADR-002: Data Source Strategy

**Status**: Accepted (revised 2026-03-13)
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
- **SEC EDGAR**: US public company filings, truly free API (10 req/sec with User-Agent header, no key needed)

**Tier 2 -- Low-Cost Paid Extensions ($17-50/mo)**:

- **Octagon AI** (priority): Private company data (3M+ companies), funding rounds (500K+ deals), investor profiles, SEC filings analysis, earnings transcripts, 13F holdings. $17/mo Plus plan (200 credits/mo), 15-day trial. Natural language queries via MCP -- the most accessible VC-relevant data API
- **OpenCorporates**: Corporate registry data (free tier available, paid for bulk)

**Tier 3 -- Premium Paid Extensions (institutional pricing)**:

- **Crunchbase**: Company profiles and funding rounds. Note: API access requires Enterprise tier (~$10K+/year). The free web tier has no API access, making it unsuitable as an MCP extension
- **PitchBook**: Comprehensive private company data (institutional subscription)
- **Affinity CRM**: Deal flow and relationship tracking (team subscription)
- **CB Insights**: Market intelligence and trend data (enterprise subscription)

### Why Octagon AI Is Prioritized

Octagon AI occupies a unique position in the VC data landscape:

1. **Lowest barrier to entry**: $17/mo vs. Crunchbase API at ~$10K+/year or PitchBook at institutional pricing. This aligns with the tool's target audience of individual practitioners and small funds
2. **Broadest VC coverage in one API**: Private companies, funding rounds, investor profiles, SEC filings, earnings transcripts, stock data, and 13F holdings -- all through a single MCP server
3. **MCP-native**: Already published as an MCP server (`octagon-mcp` on npm), requiring minimal integration work. Just configure the API key and the tools are available
4. **Natural language interface**: Queries are free-form text, so Claude can compose queries naturally without learning a structured API schema

### Octagon AI Limitations

- **Not truly free**: The MCP server is MIT-licensed, but every query consumes paid credits. No permanent free tier
- **Credit-limited throughput**: 200 credits/mo on Plus. Deep Research costs 2 credits/call (100 queries/mo). Not suitable for high-volume batch processing
- **Agent-mediated responses**: Returns AI-synthesized text, not raw structured data. Response format is not deterministic, making it unsuitable for data pipelines
- **Data provenance**: Private market data sources are not disclosed. SEC data presumably comes from EDGAR
- **Cloud-dependent**: All queries go to Octagon's API. No offline, caching, or self-hosting option

### Integration Pattern

Each external data source is implemented as an **extension** following the claude-seo pattern:

```text
extensions/<source>/
├── install.sh              # Configures MCP server + API credentials
├── skills/<skill>/SKILL.md # Source-specific sub-skill
├── agents/<agent>.md       # Source-specific subagent
└── docs/                   # Setup documentation
```

The core orchestrator includes conditional sections:

```markdown
## Octagon AI Integration (Optional)

If Octagon MCP tools are available, enrich screening with:

- Private company financials and metrics
- Funding history with deal terms and investor details
- Investor profiles with fund sizes and investment criteria
- SEC filing analysis and earnings transcript data
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

### Use Crunchbase Free Tier as Default Data Source

**Rejected on investigation**: Crunchbase's free tier has no API access. The API is exclusively Enterprise-tier (~$10K+/year), making it inaccessible to individual practitioners. Octagon AI at $17/mo provides comparable private market coverage with actual API access.

### Use Only WebFetch for All External Data

**Rejected**: Web scraping is fragile and rate-limited. Structured APIs (SEC EDGAR, Octagon) provide more reliable and comprehensive data. However, WebFetch is the right fallback for company websites and press releases.

## Consequences

### Positive

- Zero-config startup experience (Tier 1 works immediately, including SEC EDGAR)
- Users add data sources incrementally as needed
- Each extension is independently installable and removable
- Octagon AI at $17/mo makes professional-grade VC data accessible to individuals

### Negative

- Quality of analysis varies significantly with data source availability
- Users with paid data sources get materially better results (acceptable tradeoff)
- Reference files need periodic updates to stay accurate
- Octagon credit limits may slow parallel agent execution when multiple agents query simultaneously
- Dependency on Octagon AI's continued operation and pricing stability
