# ADR-004: Scope Boundaries -- What Claude-VC Should and Should Not Do

**Status**: Accepted
**Date**: 2026-03-13
**Deciders**: Yuri Gui

## Context

The SEO plugin works because **the hard part is judgment, not data access**. The data is a public webpage. The value is knowing what to check, how to score it, and what to recommend.

For VC workflows, the same question applies: **is the bottleneck data access or analysis?** Some VC tasks are judgment-heavy (analyzing a pitch deck, comparing term sheets, writing memos) and map perfectly to a Claude Cowork or Claude Code plugin. Others are data-infrastructure tasks (CRM pipelines, scheduled monitoring, large dataset processing) that belong in a proper application.

This ADR defines the boundary.

## Decision

### Claude-VC is the analysis and report generation layer

It is **not** the data infrastructure layer. Like the SEO plugin, it uses public data + user-provided documents + optional MCP extensions and focuses on judgment-heavy analysis.

### Strong Fit (in scope)

These workflows match the claude-seo pattern: public or user-provided inputs, judgment-heavy analysis, text output.

| Workflow                              | Why It Fits                                               |
| ------------------------------------- | --------------------------------------------------------- |
| Analyze a startup's website/product   | Same as SEO -- public pages, structured extraction        |
| Parse and analyze pitch deck PDFs     | Claude reads PDFs natively, extracts and scores           |
| Generate deal memo from provided data | Template-driven text generation with domain knowledge     |
| Analyze term sheets and SAFEs         | Document parsing + comparison against reference standards |
| Model cap tables and dilution         | Deterministic math (Python scripts) + scenario analysis   |
| Parse SEC/EDGAR filings               | Public data, text extraction, structured output           |
| Compare companies side-by-side        | Natural parallel subagent pattern (one agent per company) |
| Generate DD checklists                | Static domain knowledge + stage/sector customization      |

### Moderate Fit (in scope with caveats)

| Workflow                       | Caveat                                                                                                                                               |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Financial model generation     | Output CSV/Python scripts, not interactive spreadsheets. The real tool for financial models is a spreadsheet. Claude-VC generates the starting point |
| Portfolio company KPI tracking | Works for one-shot report generation from provided data. Does not replace a persistent tracking system                                               |
| LP report narrative            | Text generation from provided metrics. Does not aggregate data from multiple sources automatically                                                   |

### Weak Fit (out of scope)

These workflows require capabilities that Claude Cowork and Claude Code do not have. They belong in a proper application using the Claude API directly.

| Workflow                                      | Why It Doesn't Fit                                                                                                             |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Pull from PitchBook/Crunchbase/CB Insights    | Proprietary APIs, persistent auth, rate limits. Better as MCP extensions that _supplement_ analysis, not as core functionality |
| CRM integration (deal pipeline tracking)      | Needs OAuth flows, persistent state, database. Cowork/Code is stateless                                                        |
| Portfolio monitoring dashboards               | Cowork/Code is interactive, not a dashboard runtime                                                                            |
| Scheduled/automated data pulls                | Cowork/Code is on-demand, not a cron job                                                                                       |
| Large dataset processing (1000s of companies) | Context window limits, no persistent storage                                                                                   |
| Real-time deal flow alerts                    | Requires persistent process, push notifications                                                                                |
| Multi-user collaboration                      | Cowork/Code is single-user by design                                                                                           |

### The Three-Layer Architecture

For teams that need the out-of-scope capabilities, the recommended approach is layered:

1. **MCP servers** for authenticated data sources (Crunchbase, PitchBook, internal DB). These give Claude Cowork / Code access without baking credentials into skills. They are optional extensions, not core.

2. **Claude-VC skills** for the analysis layer. This is the judgment-heavy work: screening, memos, comparisons, term analysis, cap table modeling. All inputs are public data, user-provided documents, or data surfaced by MCP servers.

3. **A proper application** for anything needing persistence, scheduling, or a UI. Portfolio dashboards, deal pipelines, LP reporting portals. Use the Claude API directly here.

## Consequences

### Positive

- Clear scope prevents feature creep into areas where Cowork/Code is the wrong tool
- Core functionality works immediately without any API keys or external services
- Teams with existing data infrastructure can layer MCP extensions on top
- Avoids the trap of building a mediocre version of Carta, Visible, or Affinity inside a CLI tool

### Negative

- Users who want an all-in-one VC platform will be disappointed
- The "moderate fit" workflows may feel incomplete without a persistent data layer
- Portfolio monitoring is limited to one-shot analysis of provided data, not continuous tracking
