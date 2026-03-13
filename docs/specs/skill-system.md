# Skill System Specification

## Overview

Claude-VC consists of 1 orchestrator skill, 6 sub-skills, 6 parallel subagents, 6 reference files, 3 Python scripts, and 2+ optional extensions. This document specifies each component.

## Orchestrator: `vc/SKILL.md`

### Frontmatter

```yaml
---
name: vc
description: >
  Venture capital analysis toolkit. Deal screening, investment memo
  generation, cap table modeling, term sheet analysis, due diligence
  checklists, and portfolio monitoring. Use when user says "vc",
  "deal screening", "investment memo", "cap table", "term sheet",
  "due diligence", "portfolio", "startup analysis", "valuation",
  "SAFE", "convertible note", or "funding round".
---
```

### Routing Table

| Command            | Sub-Skill      | Description                             |
| ------------------ | -------------- | --------------------------------------- |
| `/vc screen <url>` | `vc-screen`    | Screen a startup from URL or pitch deck |
| `/vc memo`         | `vc-memo`      | Generate structured investment memo     |
| `/vc terms <file>` | `vc-terms`     | Analyze term sheet or SAFE              |
| `/vc captable`     | `vc-captable`  | Model cap table and dilution            |
| `/vc diligence`    | `vc-diligence` | Generate and track DD checklist         |
| `/vc portfolio`    | `vc-portfolio` | Aggregate and report on portfolio       |

### Orchestration Logic

The orchestrator handles two modes:

1. **Direct routing**: For single-skill commands (`/vc terms`, `/vc captable`), load the sub-skill and hand off.
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
- Pitch deck file path (read via Read tool)
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
  Model cap tables, dilution scenarios, and waterfall distributions.
  Parse existing cap tables or build from scratch. Supports common
  stock, preferred stock, SAFEs, convertible notes, and option pools.
  Use when user says "cap table", "dilution", "waterfall", "ownership",
  "option pool", or "pro forma".
---
```

**Inputs**:

- Existing cap table (CSV, JSON, or natural language)
- Proposed round terms (for pro forma modeling)
- SAFE/note conversion parameters

**Workflow**:

1. Parse current ownership structure
2. If new round: apply conversion mechanics and new investment
3. Invoke `scripts/captable.py` for precise calculations
4. Generate ownership tables and dilution analysis

**Outputs**:

- Current ownership table (Shareholder | Shares | % Ownership | $ Value)
- Pro forma table (post-round)
- Dilution impact by shareholder class
- Waterfall distribution at multiple exit valuations
- Option pool analysis (size, available, burn rate)

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

### `vc-portfolio` -- Portfolio Monitoring

```yaml
---
name: vc-portfolio
description: >
  Aggregate portfolio company data and generate reports. Parse
  company updates, track KPIs against benchmarks, produce LP-ready
  summaries. Use when user says "portfolio", "portfolio review",
  "LP report", "company updates", "KPIs", or "quarterly report".
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

**Purpose**: Financial calculations that require precision (DCF, revenue projections, unit economics).

**CLI Interface**:

```
python financial_model.py dcf --revenue 5000000 --growth-rate 0.8 --discount-rate 0.25 --terminal-multiple 10 --years 5
python financial_model.py unit-economics --cac 500 --ltv 5000 --payback-months 12 --churn-rate 0.05
python financial_model.py revenue-projection --current-arr 2000000 --growth-rates 1.0,0.8,0.6,0.4,0.3
```

**Output**: JSON with calculation results and methodology notes.

**Dependencies**: stdlib only (no external packages).

### `scripts/captable.py`

**Purpose**: Cap table calculations, SAFE/note conversions, waterfall distributions.

**CLI Interface**:

```
python captable.py ownership --input cap_table.json
python captable.py dilution --input cap_table.json --new-round '{"pre_money": 20000000, "investment": 5000000}'
python captable.py waterfall --input cap_table.json --exit-values 50000000,100000000,200000000
python captable.py safe-convert --safe '{"invested": 500000, "cap": 10000000, "discount": 0.2}' --round '{"pre_money": 15000000}'
```

**Output**: JSON with ownership tables, dilution percentages, and waterfall distributions.

**Dependencies**: stdlib only.

### `scripts/fetch_company.py`

**Purpose**: Fetch and normalize company data from public sources.

**CLI Interface**:

```
python fetch_company.py --url https://example.com
python fetch_company.py --domain example.com --sources web,linkedin
```

**Output**: JSON with normalized company profile (name, description, team, funding, metrics).

**Dependencies**: `httpx` (async HTTP client).

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

## Extension System

### Extension Structure

```
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

**Crunchbase (Tier 2 -- free API key)**:

- Company profiles and funding rounds
- Investor and people lookup
- Trend data and market maps
- Rate limit: 200 requests/day on free tier

**SEC EDGAR (Tier 2 -- free, no key needed)**:

- Public company filings (10-K, 10-Q, S-1, 8-K)
- XBRL financial data extraction
- Company search and CIK lookup
- Rate limit: 10 requests/second with User-Agent header

**PitchBook (Tier 3 -- paid subscription)**:

- Comprehensive private company data
- Deal and fund data
- Investor profiles
- Requires institutional subscription

**Affinity CRM (Tier 3 -- paid subscription)**:

- Deal flow tracking
- Relationship intelligence
- Pipeline management
- Requires team subscription
