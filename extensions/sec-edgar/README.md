# SEC EDGAR Extension

**Status**: Planned -- not yet implemented

## Overview

The [SEC EDGAR](https://www.sec.gov/edgar/) (Electronic Data Gathering,
Analysis, and Retrieval) system provides free access to public company
filings including 10-K annual reports, 10-Q quarterly reports, 8-K
current reports, and S-1 registration statements. This extension wraps
the EDGAR full-text search and filing retrieval APIs as MCP tools.

## Subscription

- **Cost**: Free -- no API key required
- **Rate limit**: 10 requests per second (requires a `User-Agent` header
  with contact email per SEC fair access policy)
- **Coverage**: All public US company filings since 1993 (full-text
  search since 2004)

## Expected MCP Tool Interface

Once implemented, this extension will expose the following tools via the
`vc-edgar` MCP server:

### `search_company`

Search for a company by name or CIK number.

```json
{
  "tool": "vc-edgar-search-company",
  "input": {
    "query": "Stripe Inc",
    "entity_type": "company"
  }
}
```

Returns: Matching companies with CIK numbers, SIC codes, state of
incorporation, and most recent filing dates.

### `get_filing`

Retrieve the full text of a specific filing.

```json
{
  "tool": "vc-edgar-get-filing",
  "input": {
    "cik": "0001234567",
    "filing_type": "10-K",
    "date_range": "2024-01-01:2024-12-31"
  }
}
```

Returns: Filing metadata and full text content. Supported filing types:
10-K, 10-Q, 8-K, S-1, S-3, DEF 14A, 13F-HR, SC 13D, Form D.

### `get_financial_statements`

Extract structured financial data from XBRL filings.

```json
{
  "tool": "vc-edgar-get-financials",
  "input": {
    "cik": "0001234567",
    "statement": "income_statement",
    "periods": 4
  }
}
```

Returns: Structured financial statement data (income statement, balance
sheet, cash flow statement) for the requested number of periods.

## Integration with VC Skills

The following skills will check for EDGAR tool availability and use it
to enrich their analysis when present:

| Skill            | Usage                                                     |
| ---------------- | --------------------------------------------------------- |
| `vc-screen`      | Pull public filing data for companies with SEC filings    |
| `vc-memo`        | Reference 10-K/S-1 data for market analysis and financials|
| `vc-model`       | Use historical financial statements as model inputs       |

EDGAR data is most useful for:

- Analyzing public comparables when valuing private companies
- Reviewing S-1 filings of recently-IPO'd competitors
- Pulling 13F filings to see institutional investor positions
- Checking Form D filings for private company fundraising disclosures

## Limitations

- Only covers US public company filings (not private companies, except
  Form D and some S-1s filed pre-IPO).
- XBRL structured data is available only for filings since ~2009.
- Full-text search covers filings since 2004; older filings require
  direct CIK lookup.
- Large filings (10-K annual reports) can exceed context window limits.
  The extension should extract relevant sections rather than returning
  full documents.

## Installation (Planned)

```bash
# Will be available via:
cd extensions/sec-edgar && bash install.sh
```

The install script will configure the MCP server in the user's Claude
settings. No API key is needed -- the script will prompt for a contact
email to use in the `User-Agent` header per SEC fair access policy.

See [ADR-002](../../docs/decisions/002-data-sources.md) for the data
source strategy and rationale.
