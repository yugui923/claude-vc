# Skill System Specification

## Overview

Claude-VC consists of 1 orchestrator skill, 9 sub-skills, 6 parallel subagents, 7 reference files, 2 Python scripts, and 2+ optional extensions. This document specifies each component.

**Design principle**: The value is _judgment_, not data access. All core workflows operate on public data and user-provided documents. External data sources are optional extensions that supplement analysis, never a prerequisite.

## Orchestrator: `vc/SKILL.md`

### Frontmatter

```yaml
---
name: vc
description: >
  Venture capital analysis toolkit. Deal screening, investment memo
  generation, cap table modeling, term sheet analysis, financial
  modeling, KPI reporting, due diligence checklists, and portfolio
  reporting. Use when user says "vc", "deal screening",
  "investment memo", "cap table", "term sheet", "due diligence",
  "portfolio", "compare", "pitch deck", "startup analysis",
  "valuation", "SAFE", "convertible note", "funding round",
  "financial model", "3-statement", "projections", "P&L",
  "income statement", "balance sheet", "cash flow", "KPIs",
  "metrics", "SaaS metrics", "unit economics report",
  "burn multiple", "magic number", "Rule of 40",
  or "KPI dashboard".
---
```

### Routing Table

| Command            | Sub-Skill      | Description                             |
| ------------------ | -------------- | --------------------------------------- |
| `/vc screen <url>` | `vc-screen`    | Screen a startup from URL or pitch deck |
| `/vc memo`         | `vc-memo`      | Generate structured investment memo     |
| `/vc terms <file>` | `vc-terms`     | Analyze term sheet or SAFE              |
| `/vc captable`     | `vc-captable`  | Model cap table and dilution            |
| `/vc model`        | `vc-model`     | Generate 3-statement financial model    |
| `/vc kpi`          | `vc-kpi`       | Generate KPI report with benchmarks     |
| `/vc compare`      | `vc-compare`   | Side-by-side company comparison         |
| `/vc diligence`    | `vc-diligence` | Generate and track DD checklist         |
| `/vc portfolio`    | `vc-portfolio` | Aggregate and report on portfolio       |

### Orchestration Logic

The orchestrator handles two modes:

1. **Direct routing**: For single-skill commands (`/vc terms`, `/vc captable`, `/vc model`, `/vc kpi`), load the sub-skill and hand off.
2. **Parallel orchestration**: For `/vc screen --full` or `/vc memo --comprehensive`, spawn 6 subagents concurrently, collect results, and synthesize.

### Reference File Loading

```markdown
## Reference Files

Load these on-demand as needed -- do NOT load all at startup:

- `references/valuation-methods.md` -- DCF, comparables, VC method, Berkus
- `references/due-diligence-checklist.md` -- Comprehensive DD items by category
- `references/term-sheet-terms.md` -- NVCA model terms with market commentary
- `references/safe-mechanics.md` -- YC SAFE variants, conversion mechanics
- `references/industry-multiples.md` -- Revenue/EBITDA multiples by sector
- `references/investment-criteria.md` -- Scoring framework with default weights
```

## Sub-Skills

### `vc-screen` -- Deal Screening

```yaml
---
name: vc-screen
description: >
  Screen a startup for investment potential. Accepts a company URL,
  pitch deck, or description. Produces a Deal Score (0-100) with
  breakdown across market, team, product, financials, and timing.
  Supports quick screen (single-agent) and full screen (parallel
  agents). Use when user says "screen", "evaluate startup",
  "deal flow", "should I invest", or "quick look".
---
```

**Inputs**:

- Company URL (fetched via WebFetch)
- Pitch deck PDF (Claude reads PDFs natively via the Read tool -- no parsing script needed)
- Pitch deck file path (other formats read via Read tool)
- Natural language company description
- Optional: `--full` flag for parallel agent screening
- Optional: `--criteria <file>` for custom scoring criteria

**Outputs**:

- Deal Score (0-100) with dimension breakdown
- Key findings summary (3-5 bullet points)
- Red flags and concerns
- Comparable companies
- Recommendation: Pass / Further Diligence / Strong Interest
- Standard disclaimer (from `references/disclaimers.md`)

**Workflow (quick screen)**:

1. Fetch company website or read pitch deck
2. Load `references/investment-criteria.md` for scoring framework
3. Analyze across 5 dimensions: Market (25%), Team (25%), Product (20%), Financials (20%), Timing (10%)
4. Generate Deal Score and recommendation

**Workflow (full screen, `--full`)**:

1. Same as quick screen step 1
2. Spawn 6 parallel subagents: `vc-financial`, `vc-market`, `vc-technical`, `vc-legal`, `vc-competitive`, `vc-team`
3. Aggregate results into comprehensive Deal Score
4. Generate detailed investment memo via `vc-memo` sub-skill

### `vc-memo` -- Investment Memo Generation

```yaml
---
name: vc-memo
description: >
  Generate a structured investment memo. Can build from a completed
  screening, existing notes, or from scratch. Follows standard VC
  memo format. Use when user says "memo", "investment memo",
  "write up", "IC memo", or "investment committee".
---
```

**Outputs** (structured memo sections):

1. Executive Summary
2. Company Overview
3. Market Opportunity (TAM/SAM/SOM)
4. Product & Technology
5. Team & Organization
6. Business Model & Unit Economics
7. Competitive Landscape
8. Financial Projections & Valuation
9. Key Risks & Mitigants
10. Terms & Structure (if applicable)
11. Recommendation
12. Disclaimer

### `vc-terms` -- Term Sheet Analysis

```yaml
---
name: vc-terms
description: >
  Analyze a term sheet, SAFE, or convertible note. Compares terms
  against NVCA model provisions and current market standards. Flags
  non-standard, founder-unfriendly, or unusual provisions. Use when
  user says "term sheet", "SAFE", "convertible note", "terms",
  "analyze terms", or "review terms".
---
```

**Inputs**:

- File path to term sheet (PDF, DOCX, or text)
- Natural language description of terms
- Optional: `--perspective investor|founder` (default: neutral)

**Workflow**:

1. Read the term sheet document
2. Load `references/term-sheet-terms.md` for NVCA baseline
3. Load `references/safe-mechanics.md` if SAFE/convertible note
4. Extract and categorize each provision
5. Compare against market standard
6. Flag deviations with severity rating (Standard / Favorable / Unfavorable / Unusual)
7. Generate annotated analysis

**Outputs**:

- Term-by-term comparison table (Term | This Deal | Market Standard | Assessment)
- Key concerns and negotiation points
- Economic summary (valuation, dilution, liquidation preference)
- Protective provisions analysis
- Enhanced disclaimer (from `references/disclaimers.md`)

### `vc-captable` -- Cap Table Modeling

```yaml
---
name: vc-captable
description: >
  Cap table modeling -- ownership, dilution, SAFE conversion,
  multi-series liquidation waterfall, exit scenario analysis.
  Informed by the Open Cap Table Format (OCF) standard.
---
```

**Inputs**:

- Existing cap table (CSV, JSON, or natural language)
- Stock classes with seniority, liquidation multiples, participation rights
- SAFE/note conversion parameters (including MFN status, capitalization definition)
- Proposed round terms (for pro forma modeling)

**Workflow**:

1. Parse current ownership structure (supports OCF-informed data model)
2. If SAFEs/notes: resolve MFN to lowest cap, apply capitalization definitions
3. If new round: apply conversion mechanics and new investment
4. Invoke `scripts/captable.py` for precise calculations
5. Generate ownership tables, dilution analysis, waterfall distributions

**Commands**: `model`, `dilution`, `waterfall`, `convert`, `scenarios`

**Outputs**:

- Current ownership table (Holder | Class | Shares | Ownership % | Investment)
- Pro forma table (post-round)
- Dilution impact by shareholder class
- Multi-series waterfall distribution with seniority ordering
- SAFE/note conversion details (cap vs discount, MFN resolution, accrued interest)
- Multi-exit scenario matrix (payout per holder at different exit values)

### `vc-model` -- Financial Model Generation

```yaml
---
name: vc-model
description: >
  Generate a simplified 3-statement financial model (income statement,
  balance sheet, cash flow). Accepts pitch deck data, company financials,
  or assumptions. Projects 3-5 years forward. Use when user says
  "financial model", "3-statement", "projections", "P&L",
  "income statement", "balance sheet", or "cash flow".
---
```

**Inputs**:

- Pitch deck context, raw financials, or verbal assumptions
- Minimum: current revenue, growth rate, gross margin
- Optional: OpEx breakdown, cash on hand, projection period
- Optional: `--docx [filename]` for Word export

**Workflow**:

1. Gather company data from context or user input
2. Derive reasonable assumptions for missing inputs (stage/sector benchmarks)
3. Load `references/industry-multiples.md` for sector benchmarks
4. Build JSON scenario, invoke `scripts/financial_model.py three_statement`
5. Present 3 markdown tables + analysis (break-even, runway, sensitivities)

**Outputs**:

- Income Statement (Revenue → COGS → Gross Profit → OpEx → EBITDA → Net Income)
- Balance Sheet (Cash, AR, Assets, AP, Equity with A=L+E consistency)
- Cash Flow Statement (Operating, Investing, Financing, Ending Cash)
- Analysis: break-even timing, cash runway, margin progression, key sensitivities
- Optional: bull/base/bear scenario comparison

### `vc-kpi` -- KPI Reporting

```yaml
---
name: vc-kpi
description: >
  Generate KPI reports from company data. Auto-detects company type
  (SaaS, marketplace, consumer, fintech) and calculates relevant
  metrics with industry benchmarks. Use when user says "KPIs",
  "metrics", "SaaS metrics", "unit economics report", "burn multiple",
  "magic number", "Rule of 40", or "KPI dashboard".
---
```

**Inputs**:

- Company data (JSON, CSV, verbal description, or prior context)
- Company type auto-detected or user-specified

**Workflow**:

1. Parse company data and auto-detect business model type
2. For SaaS: invoke `scripts/financial_model.py unit_economics` + compute additional KPIs
3. For other types: compute KPIs directly
4. Load `references/industry-multiples.md` for benchmarking
5. Assign health status per metric (Healthy / Watch / Concerning)

**KPI sets by type**:

- **SaaS**: ARR, NRR, CAC, LTV, LTV:CAC, churn, payback, magic number, burn multiple, Rule of 40, gross margin, revenue/employee
- **Marketplace**: GMV, take rate, liquidity ratio, repeat rate, contribution margin
- **Consumer**: DAU/MAU, retention (D1/D7/D30), viral coefficient, ARPU
- **Fintech**: NIM, NPL ratio, CAC payback, take rate
- **General** (always included): Revenue growth, burn rate, runway, headcount

**Outputs**:

- KPI Report with company type, reporting period, data source
- Key metrics summary table (Metric | Value | Benchmark | Status)
- Detailed analysis by category (growth, unit economics, efficiency)
- Flags: Healthy metrics, Concerning metrics with explanations
- Recommendation synthesis

### `vc-compare` -- Company Comparison

```yaml
---
name: vc-compare
description: >
  Compare two or more companies side-by-side across all investment
  dimensions. Spawns parallel subagents (one per company) and
  generates a comparison matrix. Use when user says "compare",
  "versus", "side by side", "which is better", or "compare deals".
---
```

**Inputs**:

- 2-4 company URLs, pitch decks, or descriptions
- Optional: `--dimensions market,team,product` to focus comparison

**Workflow**:

1. For each company, spawn a screening subagent in parallel (same as `/vc screen`)
2. Collect structured results from each agent
3. Generate side-by-side comparison matrix across all dimensions
4. Highlight relative strengths and weaknesses
5. Provide a ranked recommendation with rationale

**Outputs**:

- Comparison matrix table (Dimension | Company A | Company B | ...)
- Dimension scores per company
- Relative advantages/disadvantages
- Overall ranking with confidence level
- Standard disclaimer

### `vc-diligence` -- Due Diligence

```yaml
---
name: vc-diligence
description: >
  Generate and manage a due diligence checklist. Customizable by
  deal stage, sector, and investment size. Track completion status.
  Use when user says "due diligence", "DD", "diligence checklist",
  "DD items", or "diligence tracker".
---
```

**Inputs**:

- Deal stage: Seed / Series A / Series B / Growth
- Sector: SaaS / Fintech / Healthcare / Consumer / DeepTech / General
- Optional: existing DD items to merge

**Workflow**:

1. Load `references/due-diligence-checklist.md`
2. Filter and customize for stage and sector
3. Generate prioritized checklist with categories
4. Optionally track item completion status across sessions

**Output Categories**:

- Financial DD (audited financials, projections, unit economics)
- Legal DD (corporate docs, IP, contracts, litigation)
- Technical DD (architecture, security, scalability)
- Commercial DD (customers, pipeline, churn, NPS)
- Team DD (backgrounds, references, org structure)
- Market DD (TAM validation, competitive dynamics)

### `vc-portfolio` -- Portfolio Reporting

```yaml
---
name: vc-portfolio
description: >
  Generate portfolio reports from provided company data. Parse
  company updates, compare KPIs against benchmarks, produce
  LP-ready narrative summaries. One-shot report generation, not
  continuous monitoring (use a proper app for dashboards). Use
  when user says "portfolio", "portfolio review", "LP report",
  "company updates", "KPIs", or "quarterly report".
---
```

**Inputs**:

- Portfolio company updates (email text, files, structured data)
- KPI targets and benchmarks
- Reporting period

**Workflow**:

1. Parse and normalize company update data
2. Load `references/industry-multiples.md` for benchmark context
3. Extract KPIs (ARR, MRR growth, burn rate, runway, headcount, NRR)
4. Compare against benchmarks and prior periods
5. Generate portfolio summary

**Outputs**:

- Portfolio overview dashboard (text-based table)
- Per-company KPI summary with trend indicators
- Outlier alerts (companies significantly above/below benchmarks)
- Aggregate portfolio metrics
- LP-ready narrative summary

## Parallel Subagents

Agents are spawned by the orchestrator during full deal screenings. Each runs independently in a forked context.

### Agent Definition Format

```yaml
---
name: <agent-name>
description: <role description>
tools: Read, Bash, WebFetch, WebSearch, Glob, Grep
---

You are a <role>. When given company information:
1. <analysis step 1>
2. <analysis step 2>
...

## Output Format
<structured output specification>
```

### `vc-financial` -- Financial Analyst

**Tools**: `Read, Bash, WebFetch, WebSearch, Glob, Grep`

**Analysis**:

- Revenue model assessment (recurring vs. transactional, pricing strategy)
- Unit economics (CAC, LTV, LTV:CAC ratio, payback period)
- Burn rate and runway calculation
- Revenue growth rate and trajectory
- Gross margin analysis
- Working capital requirements

**Output**: Structured financial summary with metrics table and risk assessment.

### `vc-market` -- Market Researcher

**Tools**: `Read, WebFetch, WebSearch, Glob, Grep`

**Analysis**:

- Total Addressable Market (TAM) sizing with methodology
- Serviceable Addressable Market (SAM) and Serviceable Obtainable Market (SOM)
- Market growth rate and dynamics
- Regulatory environment
- Market timing assessment
- Key market trends and tailwinds/headwinds

**Output**: Market analysis with sizing methodology and confidence level.

### `vc-technical` -- Technical Reviewer

**Tools**: `Read, WebFetch, WebSearch, Glob, Grep`

**Analysis**:

- Product maturity assessment
- Technology stack evaluation (if discoverable)
- Technical moat and defensibility
- Scalability considerations
- IP and patent landscape
- Build vs. buy assessment

**Output**: Technical assessment with moat strength rating.

### `vc-legal` -- Legal Reviewer

**Tools**: `Read, WebFetch, WebSearch, Glob, Grep`

**Analysis**:

- Corporate structure and jurisdiction
- Regulatory requirements and compliance
- IP ownership and protection
- Key contract dependencies
- Litigation risk assessment
- Employment and equity structure concerns

**Output**: Legal risk summary with severity ratings.

### `vc-competitive` -- Competitive Analyst

**Tools**: `Read, WebFetch, WebSearch, Glob, Grep`

**Analysis**:

- Direct competitor identification and mapping
- Competitive positioning (price, features, market segment)
- Competitive advantages and disadvantages
- Market share estimates
- Barrier to entry analysis
- Potential acquirer landscape

**Output**: Competitive landscape matrix with positioning analysis.

### `vc-team` -- Team Assessor

**Tools**: `Read, WebFetch, WebSearch, Glob, Grep`

**Analysis**:

- Founder backgrounds and track records
- Team completeness (key roles filled/missing)
- Domain expertise match
- Advisory board quality
- Hiring velocity and talent strategy
- Founder-market fit assessment

**Output**: Team scorecard with key hire recommendations.

## Python Scripts

### `scripts/financial_model.py`

**Purpose**: Financial calculations that require precision (DCF, revenue projections, unit economics, 3-statement models). Generates starting-point models and structured JSON output. The real tool for interactive financial modeling is a spreadsheet -- Claude-VC generates the foundation, not the final model.

**CLI Interface**:

```bash
# All commands use JSON-in/JSON-out via --input flag
python financial_model.py dcf --input scenario.json
python financial_model.py unit_economics --input scenario.json
python financial_model.py projections --input scenario.json
python financial_model.py multiples --input scenario.json
python financial_model.py three_statement --input scenario.json
```

**Commands**:

| Command | Description |
|---------|-------------|
| `dcf` | Discounted cash flow valuation |
| `unit_economics` | CAC, LTV, LTV:CAC, payback, magic number, NRR |
| `projections` | Revenue projections with growth decay |
| `multiples` | Valuation via revenue/EBITDA multiples |
| `three_statement` | Income statement, balance sheet, cash flow (internally consistent) |

**`three_statement` details**: Produces a 3-5 year projection with:
- Income Statement: Revenue, COGS, gross profit, S&M, R&D, G&A, EBITDA, D&A, EBIT, interest, tax, net income
- Balance Sheet: Cash, AR, total assets, AP, debt, equity (A=L+E enforced)
- Cash Flow: Operating CF (net income + D&A + WC changes), investing CF (capex), financing CF, ending cash
- Summary: break-even year, ending cash, terminal EBITDA margin

**Output**: JSON with calculation results.

**Dependencies**: stdlib only (no external packages).

### `scripts/captable.py`

**Purpose**: Cap table calculations, SAFE/note conversions, multi-series waterfall distributions, exit scenario analysis. Data model informed by the Open Cap Table Format (OCF) standard.

**CLI Interface**:

```bash
# All commands use JSON-in/JSON-out via --input flag
python captable.py model --input cap_table.json
python captable.py dilution --input cap_table.json
python captable.py waterfall --input cap_table.json
python captable.py convert --input cap_table.json
python captable.py scenarios --input cap_table.json
```

**Commands**:

| Command | Description |
|---------|-------------|
| `model` | Build and display cap table with ownership percentages |
| `dilution` | Show dilution impact from a new round |
| `waterfall` | Liquidation waterfall distribution at a given exit value |
| `convert` | SAFE and convertible note conversion details |
| `scenarios` | Run waterfall at multiple exit values for comparison |

**Key features** (OCF-informed):
- **Stock classes**: `StockClass` with seniority, liquidation multiple, participating/non-participating, participation cap
- **Multi-series waterfall**: Preferences paid in seniority order (highest first), non-participating preferred converts if as-common payout is higher
- **MFN SAFE resolution**: Scans non-MFN SAFEs for lowest cap, applies to MFN SAFEs
- **Capitalization definitions**: `all_outstanding`, `shares_only`, `shares_and_options` — controls SAFE conversion denominator
- **Compound interest**: Notes support simple and compound interest with configurable compounding frequency
**Output**: JSON with ownership tables, dilution percentages, waterfall distributions, and conversion details.

**Dependencies**: stdlib only.

## Reference Files

All reference files live under `vc/references/` and are loaded on-demand by sub-skills via the Read tool.

### `valuation-methods.md` (target: ~150 lines)

- Discounted Cash Flow (DCF): methodology, discount rates by stage
- Comparable company analysis: how to select comps, adjustment factors
- Precedent transactions: sourcing and applying multiples
- VC method: expected return by stage, probability-weighted outcomes
- Berkus method: pre-revenue valuation framework
- Scorecard method: comparison against regional averages
- First Chicago method: multi-scenario analysis

### `due-diligence-checklist.md` (target: ~200 lines)

- Financial DD items (25 items): audited statements, projections, cap table, debt
- Legal DD items (20 items): incorporation, contracts, IP, litigation, compliance
- Technical DD items (15 items): architecture, security, scalability, code quality
- Commercial DD items (15 items): customers, pipeline, churn, references
- Team DD items (10 items): backgrounds, references, org chart, incentives
- Stage-specific modifiers: which items apply at Seed vs. Series A vs. Growth

### `term-sheet-terms.md` (target: ~200 lines)

- Economic terms: valuation, option pool, anti-dilution, dividends, liquidation preference
- Control terms: board composition, protective provisions, information rights
- Process terms: no-shop, exclusivity, conditions precedent, expiration
- For each term: NVCA model position, current market standard, founder-friendly vs. investor-friendly assessment

### `safe-mechanics.md` (target: ~150 lines)

- Post-money SAFE (current YC standard): mechanics, cap, discount, MFN
- Pre-money SAFE (legacy): key differences
- Conversion triggers: equity financing, liquidity event, dissolution
- Pro-rata rights side letter
- Multiple SAFE stacking scenarios
- Common pitfalls and edge cases

### `industry-multiples.md` (target: ~100 lines)

- Revenue multiples by sector: SaaS, Fintech, Healthcare, Consumer, DeepTech
- EBITDA multiples by sector (for later-stage companies)
- Stage adjustments: Seed, Series A, Series B, Growth
- Public comp benchmarks for late-stage reference
- Update cadence: quarterly refresh recommended

### `investment-criteria.md` (target: ~100 lines)

- Default scoring framework with 5 dimensions and weights
- Dimension rubrics: what constitutes a 1-10 score for each
- Customization instructions: how users can override weights and criteria
- Stage-specific scoring adjustments
- Red flag checklist (automatic dealbreakers)

### `disclaimers.md` (target: ~50 lines)

- Standard disclaimer for screening, memos, portfolio reports
- Enhanced disclaimer for valuations, term sheet analysis, cap table outputs, financial projections
- Regulatory compliance language (not investment advice, not registered)

## Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| Orchestrator (`vc/SKILL.md`) | Complete | Routes 9 commands |
| `vc-screen` | Complete | Quick + full screen modes |
| `vc-memo` | Complete | 12-section memo, native DOCX export |
| `vc-terms` | Complete | NVCA baseline comparison |
| `vc-captable` | Complete | OCF-informed, multi-series waterfall |
| `vc-model` | Complete | 3-statement model generation |
| `vc-kpi` | Complete | Auto-detect type, benchmarks, health assessment |
| `vc-compare` | Planned (Phase 3) | Parallel per-company agents |
| `vc-diligence` | Planned (Phase 3) | Stage/sector-customized checklists |
| `vc-portfolio` | Planned (Phase 4) | One-shot report generation |
| `captable.py` | Complete | 5 commands, stock classes, MFN, compound interest |
| `financial_model.py` | Complete | 5 commands including three_statement |
| Parallel subagents | Planned (Phase 3) | 6 specialist agents |
| Octagon AI extension | Planned (Phase 4) | MCP server integration |
| SEC EDGAR extension | Planned (Phase 4) | Free raw filing access |

## Error Handling

Python scripts follow these patterns:
- Invalid JSON input → clear error message with expected format
- Missing required fields → error listing which fields are missing
- Invalid numeric values → error with field name and constraint
- All errors output as JSON: `{"error": "message"}`
- Exit code 1 on error, 0 on success

## Extension System

### Extension Structure

```text
extensions/<name>/
├── README.md               # Setup documentation
├── install.sh              # Installer (configures MCP server)
├── install.ps1             # Windows installer
├── uninstall.sh
├── skills/<name>/SKILL.md  # Extension sub-skill
├── agents/<name>.md        # Extension subagent (optional)
└── docs/                   # Additional docs
```

### Planned Extensions

**Octagon AI (Tier 2 -- priority, $17/mo Plus plan)**:

- 3M+ private company profiles with financials, revenue, valuations, employee counts
- 500K+ funding deals with 70+ queryable fields (deal size, pre/post-money, investors, terms)
- Investor profiles: fund sizes, investment criteria, portfolio data, dry powder
- SEC filings analysis (10-K, 10-Q, 8-K, S-1) for 8K+ public companies
- Earnings call transcripts (10yr history), 13F institutional holdings
- Stock market data (10K+ tickers, historical + current)
- Deep research: multi-source web aggregation and synthesis
- MCP server: `npx -y octagon-mcp` (already published, MIT-licensed)
- Natural language queries -- Claude composes queries without learning a structured API
- 200 credits/mo on Plus plan (1-3 credits per query depending on type)

**SEC EDGAR (Tier 1 -- free, no key needed, built-in)**:

- Public company filings (10-K, 10-Q, S-1, 8-K)
- XBRL financial data extraction
- Company search and CIK lookup
- Rate limit: 10 requests/second with User-Agent header
- Note: Octagon AI also covers SEC filings with AI-synthesized analysis. SEC EDGAR extension provides direct access to raw filing text

**Crunchbase (Tier 3 -- Enterprise pricing ~$10K+/year)**:

- Company profiles and funding rounds
- Investor and people lookup
- Note: The free web tier has no API access. API requires Enterprise subscription
- Consider only if user already has Crunchbase Enterprise access

**PitchBook (Tier 3 -- institutional subscription)**:

- Comprehensive private company data
- Deal and fund data
- Investor profiles
- Requires institutional subscription

**Affinity CRM (Tier 3 -- team subscription)**:

- Deal flow tracking
- Relationship intelligence
- Pipeline management
- Requires team subscription
