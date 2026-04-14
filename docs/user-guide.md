# User Guide

Everything you need to know about each Claude-VC command. For installation,
see the [README](../README.md).

Claude-VC has **six commands** plus help, organized around how a VC actually
works a deal. Each command takes one or more inputs (a URL, a pitch deck, a
CSV, or a description) and produces the analysis.

---

## `/vc` — Analyze a Company (All-in-One)

The simplest way to use Claude-VC. Give it a company and it does the rest —
screens the deal and writes an investment memo with a tailored due diligence
checklist built in.

```
/vc https://example-startup.com
/vc /path/to/pitch-deck.pdf
/vc "B2B SaaS company doing $5M ARR in developer tools"
```

Works with website URLs, pitch deck PDFs, or plain-text descriptions. With
no arguments, it shows a list of all available commands.

---

## `/vc screen` — Score a Startup (or Compare Several)

Evaluates one company across five dimensions and gives it a Deal Score from
0 to 100. If you pass 2-4 inputs, it produces a side-by-side comparison
instead.

```
/vc screen https://company.com
/vc screen /path/to/deck.pdf
/vc screen https://company-a.com https://company-b.com       # comparison
/vc screen /path/to/deck-a.pdf /path/to/deck-b.pdf /path/to/deck-c.pdf
```

**Single-company output**: scoring table, key findings, red flags, a
recommendation (Pass / Cautious / Further Diligence / Strong Interest), and
comparable companies.

The five scoring dimensions:

| Dimension | Max Points | What It Looks At |
| --- | --- | --- |
| Market Opportunity | 25 | Market size, growth rate, timing |
| Team & Execution | 25 | Founder backgrounds, team gaps, domain fit |
| Product & Technology | 20 | Differentiation, technical moat, maturity |
| Financials & Business Model | 20 | Revenue, margins, unit economics, burn |
| Timing & Momentum | 10 | Why now, traction trajectory |

What the scores mean:

| Score | Recommendation | What To Do |
| --- | --- | --- |
| 80+ | Strong Interest | Move to full due diligence immediately |
| 60-79 | Further Diligence | Worth a deeper look — address the concerns first |
| 40-59 | Cautious | Significant issues — only pursue if strategic fit |
| 0-39 | Pass | Does not meet investment criteria |

**Comparison output** (2-4 inputs): side-by-side matrix across six
dimensions (market, team, product, financials, traction, valuation), with a
winner highlighted per dimension and an overall recommendation.

**Options**:

- `--full` — deeper analysis using 6 specialist agents in parallel
  (financial, market, technical, legal, competitive, team). More thorough,
  uses more tokens. Works in both single-company and comparison mode.
- `--criteria <file>` — use your own scoring weights instead of the defaults.

---

## `/vc memo` — Write an Investment Memo (with DD Checklist)

Generates a structured investment memo — the kind you'd present to an
investment committee — and ends with a due diligence checklist tailored to
the company's stage and sector.

```
/vc memo
/vc memo /path/to/deck.pdf
```

Best used after `/vc screen` in the same conversation. The memo automatically
draws on the screening results, so you don't need to re-enter company info.

**The 12 sections**: Executive Summary, Company Overview, Market Opportunity,
Product & Technology, Team, Business Model & Unit Economics, Competitive
Landscape, Traction & Metrics, Financial Projections, Key Risks, Terms &
Structure, and **Due Diligence Checklist** (tailored to stage and sector).

**Options**:

- `--comprehensive` — runs a full screening first (6 parallel agents), then
  writes the memo. Equivalent to `/vc screen --full` followed by the memo.
- `--diligence-only` — emit only the DD checklist (Section 12) as a
  standalone document. Use this when you already have a memo and just want
  the checklist refreshed for a specific stage or sector.
- `--stage <stage>` — explicit stage override for the DD checklist (seed,
  series-a, series-b, growth).
- `--sector <sector>` — explicit sector override for the DD checklist
  (saas, fintech, deeptech, consumer, healthtech, marketplace).
- `--no-docx` — skip the Word document; output markdown only. By default,
  both a markdown file and a DOCX are generated.

### The Due Diligence Checklist

Six categories: Financial, Legal, Technical, Commercial, Team & HR, and
Regulatory. Each item is marked by priority:

- **[!] Critical** — must complete before closing
- **[*] Important** — should complete; flag if not possible
- **[-] Nice-to-have** — complete if time allows

If you've already run `/vc screen`, any red flags from the screening are
automatically added as company-specific checklist items.

---

## `/vc terms` — Review a Term Sheet

Reads a term sheet, SAFE agreement, or convertible note and compares every
provision against industry-standard (NVCA) terms. Flags anything unusual.

```
/vc terms /path/to/term-sheet.pdf
/vc terms /path/to/safe-agreement.docx
```

**What you get**: a table showing each term, the proposed value, the market
standard, and an assessment (Standard, Investor-favorable, Founder-favorable,
Aggressive, or Missing). Non-standard terms get a detailed explanation of
why they matter and what to negotiate instead.

Also works for comparing multiple competing offers side by side.

---

## `/vc captable` — Model a Cap Table

Calculates ownership percentages, shows how new funding rounds dilute
existing shareholders, and models what everyone gets at different exit
prices.

```
/vc captable
```

You can type in your data interactively or provide it inline. The five
things it can do:

| Operation | What It Does |
| --- | --- |
| Model | Build a cap table from founders, employee stock pool, SAFEs, notes, and priced rounds |
| Dilution | Show how a new funding round changes everyone's ownership |
| Waterfall | Calculate who gets paid what at exit, respecting liquidation preferences |
| Convert | Show how SAFEs and convertible notes convert to equity |
| Scenarios | Compare payouts across different exit prices (e.g., $50M, $200M, $1B) |

Handles all common instruments: common stock, preferred stock, post-money
SAFEs, pre-money SAFEs, MFN (most-favored-nation) SAFEs, convertible notes
with interest, stock options, and warrants. Supports participating preferred
with caps.

All calculations run in Python for precision — not LLM estimation.

---

## `/vc model` — Build a Financial Model

Creates a 3-statement financial model: income statement (P&L), balance
sheet, and cash flow statement. Projects 3-5 years into the future.

```
/vc model
/vc model /path/to/financials.md
```

At minimum, you need to provide the company's current revenue, growth rate,
and gross margin. Claude fills in reasonable defaults for everything else
based on the company's stage and industry.

**What you get**: three financial tables, an assumptions summary showing
where each number came from, and an analysis covering when the company
reaches profitability, how long the cash lasts, and which assumptions
matter most.

**Options**:

- `--no-docx` — skip the Word document; output markdown only.
- `--no-xlsx` — skip the Excel workbook.
- By default, both markdown, DOCX, and XLSX are generated.

---

## `/vc portfolio` — Portfolio Analytics

Post-investment analytics on portfolio data. Produces one of three artifacts
depending on the flags:

### Default: Portfolio Report

Generates a professional portfolio report suitable for LP (limited partner)
updates.

```
/vc portfolio /path/to/portfolio.csv
/vc portfolio /path/to/portfolio.json
```

Provide a spreadsheet or data file with your portfolio companies. Each
company needs: name, sector, stage, amount invested, current valuation,
status (active, exited, or written off), and investment date.

**The report includes**:

1. **Portfolio Summary** — total invested, current value, return multiple
   (MOIC), estimated IRR
2. **Composition** — breakdown by sector, stage, and year of investment
3. **Performance Dashboard** — each company's key metrics and trajectory
4. **Cohort Analysis** — how different investment vintages are performing
5. **Concentration Risk** — flags if too much is riding on one company or
   sector
6. **Follow-On Needs** — which companies will need more capital
7. **Exits & Write-Offs** — realized returns and losses
8. **LP Summary** — a professional narrative paragraph for your update letter

### `--kpi` — KPI Dashboard

Generates a metrics report for a single company with industry benchmarks
and a health check for each metric (Healthy, Watch, or Concerning).

```
/vc portfolio /path/to/metrics.md --kpi
/vc portfolio --kpi
```

Claude automatically detects the type of company and picks the right
metrics:

| Company Type | Example Metrics |
| --- | --- |
| **SaaS** (software subscriptions) | ARR, churn, net retention, CAC, LTV, burn multiple, Rule of 40 |
| **Marketplace** | GMV, take rate, liquidity, repeat rate |
| **Consumer** | DAU/MAU, retention curves, viral coefficient |
| **Fintech** | Net interest margin, default rate, take rate |

Each metric is compared against benchmarks for the company's stage and
sector, so you can quickly spot what's strong and what needs attention.

### `--returns` — Fund Returns Analysis

Calculates fund-level return metrics (IRR, MOIC, DPI, TVPI, PME) from your
investment data.

```
/vc portfolio /path/to/investments.csv --returns
```

**What you get**: per-investment and portfolio-level metrics with benchmark
comparisons (top quartile, median, bottom quartile).

| Metric | What It Means |
| --- | --- |
| MOIC | Total multiple on invested capital |
| DPI | Distributions / Invested (cash-on-cash return) |
| TVPI | Total Value / Invested |
| IRR | Annualized return (XIRR on actual cash flow dates) |
| PME | Actual return vs. public market benchmark |

### Options (all portfolio modes)

- `--no-docx` — skip the Word document (portfolio report only)
- `--no-xlsx` — skip the Excel workbook
- By default, markdown + XLSX are generated (and DOCX for the default
  portfolio report)
