# User Guide

Everything you need to know about each Claude-VC command. For installation,
see the [README](../README.md).

---

## `/vc` — Analyze a Company (All-in-One)

The simplest way to use Claude-VC. Give it a company and it does the rest —
screens the deal, writes an investment memo, and creates a diligence checklist.

```
/vc https://example-startup.com
/vc /path/to/pitch-deck.pdf
/vc "B2B SaaS company doing $5M ARR in developer tools"
```

Works with website URLs, pitch deck PDFs, or plain-text descriptions. With
no arguments, it shows a list of all available commands.

---

## `/vc screen` — Score a Startup

Evaluates a company across five dimensions and gives it a Deal Score from
0 to 100.

```
/vc screen https://company.com
/vc screen /path/to/deck.pdf
```

**What you get**: a scoring table, key findings, red flags, a recommendation
(Pass / Cautious / Further Diligence / Strong Interest), and a list of
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

**Options**:
- `--full` — runs a deeper analysis using 6 specialist agents in parallel
  (financial, market, technical, legal, competitive, team). More thorough,
  uses more tokens.
- `--criteria <file>` — use your own scoring weights instead of the defaults.

---

## `/vc memo` — Write an Investment Memo

Generates a structured investment memo — the kind you'd present to an
investment committee.

```
/vc memo
/vc memo /path/to/deck.pdf
```

Best used after `/vc screen` in the same conversation. The memo automatically
draws on the screening results, so you don't need to re-enter company info.

**The 12 sections**: Executive Summary, Company Overview, Market Opportunity,
Product & Technology, Team, Business Model & Unit Economics, Competitive
Landscape, Traction & Metrics, Financial Projections, Key Risks, Terms &
Structure, Recommendation.

**Options**:

- `--comprehensive` — runs a full screening first, then writes the memo.
  Equivalent to `/vc screen --full` followed by `/vc memo`.
- `--no-docx` — skip the Word document; output markdown only. By default,
  both a markdown file and a DOCX are generated.

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

- `--no-docx` — skip the Word document; output markdown only. By default,
  both a markdown file and a DOCX are generated.

---

## `/vc kpi` — Create a KPI Dashboard

Generates a metrics report with industry benchmarks and a health check for
each metric (Healthy, Watch, or Concerning).

```
/vc kpi
/vc kpi /path/to/metrics.md
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

---

## `/vc compare` — Compare Companies Side by Side

Evaluates 2-4 companies in parallel and produces a comparison matrix.

```
/vc compare https://company-a.com https://company-b.com
/vc compare /path/to/deck-a.pdf /path/to/deck-b.pdf
```

Compares across six dimensions: market, team, product, financials, traction,
and valuation. Highlights a winner for each dimension and gives an overall
recommendation.

**Options**:
- `--criteria <file>` — use your own scoring weights.

---

## `/vc diligence` — Generate a Due Diligence Checklist

Creates a customized checklist of everything you should verify before
investing, tailored to the company's stage and industry.

```
/vc diligence
/vc diligence --stage seed --sector fintech
```

Covers six areas: Financial, Legal, Technical, Commercial, Team & HR, and
Regulatory. Each item is marked by priority:

- **[!] Critical** — must complete before closing
- **[*] Important** — should complete; flag if not possible
- **[-] Nice-to-have** — complete if time allows

If you've already run `/vc screen`, any red flags from the screening are
automatically added as company-specific checklist items.

**Options**:
- `--stage <stage>` — seed, series-a, series-b, or growth
- `--sector <sector>` — saas, fintech, deeptech, consumer, healthtech, or
  marketplace

---

## `/vc portfolio` — Create a Portfolio Report

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

**Options**:

- `--no-docx` — skip the Word document; output markdown only. By default,
  both a markdown file and a DOCX are generated.
