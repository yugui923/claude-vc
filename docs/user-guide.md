# User Guide

Detailed documentation for every claude-vc command. For installation and
quick start, see the [README](../README.md).

---

## `/vc` — Full Pipeline

Runs screen + memo + diligence in one command.

```text
/vc https://example-startup.com
/vc /path/to/pitch-deck.pdf
/vc "B2B SaaS company doing $5M ARR in developer tools"
```

Accepts a URL, file path, or natural language description. With no arguments,
shows the available commands table.

---

## `/vc screen` — Deal Screening

Score a startup 0-100 across five investment dimensions.

```text
/vc screen https://company.com
/vc screen /path/to/deck.pdf
/vc screen "description of the company"
```

**Output**: Deal Score table, key findings, red flags, recommendation,
comparable companies, disclaimer.

| Dimension | Max Points |
| --- | --- |
| Market Opportunity | 25 |
| Team & Execution | 25 |
| Product & Technology | 20 |
| Financials & Biz Model | 20 |
| Timing & Momentum | 10 |

| Score | Recommendation |
| --- | --- |
| 80+ | Strong Interest — proceed to full diligence |
| 60-79 | Further Diligence — worth deeper investigation |
| 40-59 | Cautious — significant concerns |
| 0-39 | Pass |

### Flags

| Flag | Effect |
| --- | --- |
| `--full` | Spawn 6 parallel subagents (financial, market, technical, legal, competitive, team) for comprehensive analysis |
| `--criteria <file>` | Use custom scoring weights from a file |

---

## `/vc memo` — Investment Memo

Generate a structured 12-section investment memo.

```text
/vc memo                           # From prior screening context
/vc memo /path/to/deck.pdf        # From a pitch deck
/vc memo https://company.com      # From a URL
```

**Sections**: Executive Summary, Company Overview, Market Opportunity,
Product & Technology, Team & Organization, Business Model & Unit Economics,
Competitive Landscape, Traction & Metrics, Financial Projections & Valuation,
Key Risks & Mitigants, Terms & Structure, Recommendation.

Best used after `/vc screen` in the same conversation — the memo draws on
the screening results automatically.

### Flags

| Flag | Effect |
| --- | --- |
| `--comprehensive` | Run full parallel screening before generating memo |
| `--docx [filename]` | Export as a Word document |

---

## `/vc terms` — Term Sheet Analysis

Analyze a term sheet, SAFE, or convertible note against NVCA baseline terms.

```text
/vc terms /path/to/term-sheet.pdf
/vc terms /path/to/safe.docx
```

**Output**: Extracted terms table with market standard comparison, assessment
per term (Standard / Investor-favorable / Founder-favorable / Aggressive /
Missing), detailed flags on non-standard provisions with negotiation
suggestions, overall assessment, top 3 negotiation priorities.

Supports: priced round term sheets, post-money SAFEs, pre-money SAFEs,
convertible notes, side letters. Also supports side-by-side comparison of
multiple competing offers.

---

## `/vc captable` — Cap Table Modeling

Model ownership, dilution, SAFE/note conversion, and liquidation waterfalls.

```text
/vc captable
```

Provide data inline or interactively. Supports five operations:

| Operation | What It Does |
| --- | --- |
| `model` | Build cap table from founders, ESOP, SAFEs, notes, priced rounds |
| `dilution` | Show ownership impact of a new round |
| `waterfall` | Liquidation payouts with multi-series seniority ordering |
| `convert` | SAFE and note conversion details (cap vs discount) |
| `scenarios` | Payouts across multiple exit valuations |

**Supported instruments**: Common stock, preferred stock (with stock classes),
post-money SAFEs, pre-money SAFEs, MFN SAFEs, convertible notes (simple and
compound interest), options, warrants. Supports participating preferred with
caps and non-participating preferred.

All math runs in Python (`captable.py`) for Decimal-precision arithmetic.

---

## `/vc model` — Financial Model

Generate a 3-statement financial model (income statement, balance sheet,
cash flow) projecting 3-5 years forward.

```text
/vc model                              # Interactive — asks for inputs
/vc model /path/to/financials.md      # From a file
```

**Minimum inputs needed**: current revenue, growth rate, gross margin. The
model fills in reasonable defaults for everything else based on stage and
sector.

**Output**: Three markdown tables (income statement, balance sheet, cash flow
statement), assumptions table with sources, analysis section covering
break-even timing, runway, margin progression, and key sensitivities.

All math runs in Python (`financial_model.py`) with balance sheet identity
verification (Assets = Liabilities + Equity).

### Flags

| Flag | Effect |
| --- | --- |
| `--docx [filename]` | Export as a Word document |

---

## `/vc kpi` — KPI Report

Generate a KPI report with industry benchmarks and health assessments.

```text
/vc kpi                             # Interactive — asks for data
/vc kpi /path/to/metrics.md       # From a file
```

Auto-detects company type and applies the right metrics:

| Type | Key Metrics |
| --- | --- |
| **SaaS** | ARR, MRR growth, NRR, gross churn, CAC, LTV, CAC payback, Magic Number, burn multiple, Rule of 40, gross margin |
| **Marketplace** | GMV, take rate, liquidity, supply/demand growth, contribution margin, repeat rate |
| **Consumer** | DAU/MAU, stickiness, D1/D7/D30 retention, session frequency, ARPU, viral coefficient |
| **Fintech** | NIM, NPL ratio, CAC payback, take rate, regulatory capital |

Each metric gets a health status: **Healthy**, **Watch**, or **Concerning**
based on industry benchmarks. The report includes a flags section and
actionable recommendations.

---

## `/vc compare` — Company Comparison

Side-by-side comparison of 2-4 companies.

```text
/vc compare https://company-a.com https://company-b.com
/vc compare /path/to/deck-a.pdf /path/to/deck-b.pdf
```

Spawns parallel agents to analyze each company independently, then produces
a comparison matrix across six dimensions (market, team, product, financials,
traction, valuation). Includes a winner-by-dimension assessment and overall
recommendation.

### Flags

| Flag | Effect |
| --- | --- |
| `--criteria <file>` | Use custom scoring weights |

---

## `/vc diligence` — Due Diligence Checklist

Generate a customizable due diligence checklist.

```text
/vc diligence                                    # Interactive
/vc diligence --stage seed --sector fintech     # Specify stage and sector
```

Produces a categorized checklist across 6 areas: Financial, Legal, Technical,
Commercial, Team & HR, Regulatory. Each item is tagged by priority:

- `[!]` Critical — must complete before closing
- `[*]` Important — should complete, flag if not possible
- `[-]` Nice-to-have — complete if time allows

After a screening, red flags are automatically added as company-specific
items. Includes a suggested 3-week timeline and key management questions.

### Flags

| Flag | Effect |
| --- | --- |
| `--stage <stage>` | Override stage detection (seed, series-a, series-b, growth) |
| `--sector <sector>` | Override sector detection (saas, fintech, deeptech, consumer, healthtech, marketplace) |

---

## `/vc portfolio` — Portfolio Report

Generate an LP-ready portfolio report from provided company data.

```text
/vc portfolio /path/to/portfolio.csv
/vc portfolio /path/to/portfolio.json
```

**Required fields per company**: name, sector, stage, investment_amount,
current_valuation, status (active/exited/written_off/dead), investment_date.

**Optional fields**: arr_or_revenue, headcount, last_round_date,
ownership_pct, board_seat, follow_on_reserved, notes.

The 8-section report covers:

1. **Portfolio Summary** — total invested, current value, MOIC, IRR estimate
2. **Portfolio Composition** — by sector, stage, vintage year
3. **Performance Dashboard** — per-company metrics with trajectory indicators
4. **Cohort Analysis** — by vintage year and entry stage
5. **Risk Concentration** — sector, stage, and single-company concentration
6. **Follow-On Analysis** — estimated capital needs
7. **Exits & Write-Offs** — realized returns and loss patterns
8. **LP Executive Summary** — professional narrative for LP updates

### Flags

| Flag | Effect |
| --- | --- |
| `--docx [filename]` | Export as a Word document |
