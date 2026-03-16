# Octagon AI Extension

**Status**: Planned -- not yet implemented

## Overview

[Octagon AI](https://www.octagonagents.com/) provides access to private
company data, funding history, investor profiles, and SEC filing analysis
through a natural language MCP interface. It covers 3M+ companies and
500K+ funding deals, making it the most accessible VC-relevant data API
for individual practitioners and small funds.

## Subscription

- **Required plan**: Octagon Plus ($17/month)
- **Credits**: 200 credits/month (Deep Research costs 2 credits/call)
- **Free trial**: 15-day trial available
- **Note**: The MCP server (`octagon-mcp` on npm) is MIT-licensed, but
  every query consumes paid credits. There is no permanent free tier.

## Expected MCP Tool Interface

Once implemented, this extension will expose the following tools via the
`octagon-agent` MCP server:

### `query_company`

Query private company data by name or domain.

```json
{
  "tool": "octagon-agent",
  "input": "What is the latest valuation, revenue, and headcount for <company>?"
}
```

Returns: AI-synthesized company profile including financials, metrics,
key personnel, and recent news.

### `query_investor`

Query investor profiles, fund sizes, and investment history.

```json
{
  "tool": "octagon-agent",
  "input": "What is <investor>'s fund size, investment thesis, and recent deals?"
}
```

Returns: Investor profile with AUM, investment criteria, portfolio
companies, and recent activity.

### `query_funding_round`

Query funding round details for a specific company.

```json
{
  "tool": "octagon-agent",
  "input": "Show all funding rounds for <company> with amounts, valuations, and investors."
}
```

Returns: Funding history with round sizes, pre/post-money valuations,
lead investors, and participation details.

## Integration with VC Skills

The following skills will check for Octagon tool availability and use it
to enrich their analysis when present:

| Skill            | Usage                                                     |
| ---------------- | --------------------------------------------------------- |
| `vc-screen`      | Enrich screening with private company financials and metrics |
| `vc-memo`        | Pull funding history, investor profiles, and comparable data |
| `vc-compare`     | Source metrics for side-by-side company comparison         |
| `vc-diligence`   | Verify company claims against Octagon data                |

## Limitations

- Responses are AI-synthesized text, not raw structured data. Response
  format is not deterministic, so it is unsuitable for data pipelines.
- Credit limits (200/month) may constrain parallel agent execution when
  multiple skills query simultaneously during full screening mode.
- Private market data sources are not disclosed by Octagon.
- Cloud-dependent -- all queries go to Octagon's API with no offline or
  caching option.

## Installation (Planned)

```bash
# Will be available via:
cd extensions/octagon && bash install.sh
```

The install script will configure the MCP server in the user's Claude
settings and prompt for the Octagon API key.

See [ADR-002](../../docs/decisions/002-data-sources.md) for the data
source strategy and rationale for prioritizing Octagon AI.
