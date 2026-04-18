# Portfolio Command (portfolio + kpi + returns)

Post-investment analytics on portfolio data. Produces one of three artifacts:

- **Portfolio report** (default): LP-ready report with performance metrics,
  composition analysis, cohort breakdowns, and concentration risk.
- **KPI dashboard** (`--kpi`): Metrics report for a single company, with
  benchmarks and health assessments. Auto-detects company type.
- **Returns analysis** (`--returns`): Fund-level return metrics — IRR, MOIC,
  DPI, TVPI, PME — with benchmarks.

## Input Handling

Parse `$ARGUMENTS` and conversation context:

1. **CSV file path**: Read the CSV. Accept common header aliases (`company`,
   `co_name`, `amount`, `invested`, `valuation`, `arr`, `revenue`,
   `employees`, `team_size`).
2. **JSON file path**: Read the JSON (array of companies or object with
   `companies` key).
3. **Typed data in conversation**: Parse from the user's message (table,
   bullet list, or inline JSON).
4. **After a screening or memo** (for `--kpi` only): Use metrics already in
   context.
5. **No input**: Ask the user for portfolio data. Show the expected input
   fields below.

### Flags

- `--kpi`: Generate a single-company KPI dashboard (requires company data,
  not a portfolio).
- `--returns`: Generate fund-level returns analysis (IRR, MOIC, DPI, TVPI,
  PME). Requires per-investment data with cash flow timing.
- `--no-docx`: Skip DOCX export (portfolio report only).
- `--no-xlsx`: Skip XLSX export.
- `--docx <filename>` / `--xlsx <filename>`: Override default filenames.
- If neither `--kpi` nor `--returns` is set, generate the **default portfolio
  report**.

## Firm Customization

Before generating output, check
`${CLAUDE_SKILL_DIR}/config/firm-templates.md` for custom section headers,
summary format, and required fields. Check
`${CLAUDE_SKILL_DIR}/config/firm-criteria.md` for custom benchmarks and
thresholds (KPI mode). If absent, use defaults.

## Portfolio Report (Default)

### Input Fields per Company

| Field              | Required | Type   | Description                          |
| ------------------ | -------- | ------ | ------------------------------------ |
| `name`             | Yes      | string | Company name                         |
| `sector`           | Yes      | string | Sector (SaaS, fintech, etc)          |
| `stage`            | Yes      | string | Stage at investment (seed, A, B, ...) |
| `investment_amount`| Yes      | number | Total invested ($)                   |
| `current_valuation`| Yes      | number | Current estimated valuation ($)      |
| `status`           | Yes      | string | active, exited, dead, or written_off |
| `investment_date`  | Yes      | date   | YYYY-MM-DD or YYYY                   |
| `arr_or_revenue`   | No       | number | Most recent ARR or annual revenue ($) |
| `headcount`        | No       | number | Employees                            |
| `exit_value`       | No       | number | Realized proceeds if exited ($)      |
| `ownership_pct`    | No       | number | Fund's ownership % (0-100)           |
| `last_round_date`  | No       | date   | Most recent funding round            |
| `last_round_stage` | No       | string | Most recent round (A, B, C, ...)     |
| `notes`            | No       | string | Free-form notes                      |

If required fields are missing, ask the user. For optional fields, note data
gaps in the report but proceed.

### Validation

- All required fields present per company
- `status` is one of: active, exited, dead, written_off
- `investment_amount` and `current_valuation` positive numbers
- `investment_date` parses to a valid date
- `exit_value` provided for companies with status `exited`

Flag validation errors and ask for corrections. Proceed with valid rows.

Tell the user: **"Validated [N] companies. Generating 8-section portfolio
report..."**

### Report Sections

Generate all 8 sections in order. Use the data provided — do not fabricate.

**1. Portfolio Summary** — Compute and present as a summary card:

| Metric              | How to Compute                                               |
| ------------------- | ------------------------------------------------------------ |
| Total Invested      | Sum of `investment_amount`                                   |
| Total Current Value | Sum of `current_valuation` (active) + `exit_value` (exited)  |
| Total MOIC          | Total Current Value / Total Invested                         |
| Gross IRR Estimate  | `MOIC^(1/years) - 1` using weighted avg holding period        |
| Number of Companies | Count by status                                              |
| Unrealized Value    | Sum of `current_valuation` for active                        |
| Realized Value      | Sum of `exit_value` for exited                               |
| Loss Ratio          | (dead + written_off count) / total count                     |
| Avg Holding Period  | Mean of (today − investment_date) for active                 |

Flag that the IRR is an estimate; true IRR requires exact cash flow dates.

**2. Portfolio Composition** — Break down by sector, stage at entry, vintage
year. For each: count, total invested, total current value, MOIC. Highlight
best/worst per dimension.

**3. Performance Dashboard** — One row per company:

| Company | Sector | Stage | Invested | Current Val | MOIC | Status | Trajectory |

Trajectory from available data:
- **Up**: Current val > 2x investment OR ARR growing OR advanced to later stage
- **Flat**: Current val between 0.8x and 2x investment
- **Down**: Current val < 0.8x investment OR dead/written_off
- **Exited**: status is exited

Sort by MOIC descending.

**4. Cohort Analysis** — By vintage year and by stage at entry. For each
cohort: count, total invested, total current value, MOIC, % exits, % write-offs.
Note cohorts with <3 companies as too small for meaningful analysis.

**5. Risk Concentration** — Sector, stage, and single-company concentration:
- Flag if any single sector > 40% of total invested
- Flag if any single sector > 50% of total current value
- Flag if any single company > 25% of total current value
- Flag if top 3 companies > 60% of total current value

Severity: Low (no flags) / Moderate (1 flag) / High (2+ flags).

**6. Follow-On Analysis** — For each active company:

| Company | Current Stage | Last Round | Time Since Last | Est. Runway | Follow-On Need |

Heuristics:
- **Likely needs follow-on**: >18 months since last round and pre-B stage
- **Bridge candidate**: >24 months since last round with flat/down trajectory
- **Self-sustaining**: Revenue suggests near-profitability, or late stage
- **N/A**: Exited, dead, or written_off

Summarize total companies likely needing follow-on and rough capital need.

**7. Exits & Write-Offs**

Realized returns table for exited companies:
| Company | Invested | Exit Value | MOIC | Holding Period | Exit Type |

Loss analysis for dead + written_off:
| Company | Invested | Status | Holding Period | Sector | Stage |

Summaries: realized MOIC, average exit, best/worst; loss rate; any sector /
stage / vintage clustering in losses.

**8. LP Executive Summary** — 2-3 paragraph narrative for an LP update:

- Paragraph 1: Fund performance (MOIC, IRR estimate, portfolio size,
  deployment pace). Compare to industry benchmarks if possible (top-quartile
  VC funds target 3x+ net MOIC).
- Paragraph 2: Portfolio highlights — best performers, notable exits,
  strong-trajectory companies. Be specific with numbers.
- Paragraph 3: Risk and outlook — concentration, follow-on needs, losses,
  market conditions. End forward-looking.

### Formatting

- Dollar amounts with commas and units ($1.2M, $500K)
- Percentages to one decimal (12.3%)
- MOIC to one decimal (3.2x)
- Consistent dates (YYYY-MM-DD or MMM YYYY)
- Bold key metrics in summary
- Report should be scannable in under 5 minutes

## KPI Mode (`--kpi`)

Generate a KPI report from a single company's data.

### Auto-Detection

Determine company type from the data and tell the user:
**"Detected [type] company. Computing KPIs and benchmarking..."**

- **SaaS**: ARR/MRR, churn, NRR, subscriptions mentioned
- **Marketplace**: GMV, take rate, supply/demand mentioned
- **Consumer**: DAU/MAU, retention, sessions mentioned
- **Fintech**: NIM, NPL, interchange, loan volume mentioned
- **General**: Default; ask user to confirm

### SaaS KPIs

Build a JSON scenario and run:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/financial_model.py" unit_economics --input <temp.json>
```

Present script output plus these Claude-computed KPIs:

| Metric                | Formula                           | Benchmark                    |
| --------------------- | --------------------------------- | ---------------------------- |
| ARR                   | MRR × 12                          | Stage-dependent              |
| MRR Growth            | (MRR_now − MRR_prior) / MRR_prior | >10% m/m (seed), >5% (A)     |
| Net Revenue Retention | (from script output)              | >120% excellent, >100% good  |
| Gross Churn           | Lost MRR / Starting MRR           | <2% monthly, <5% acceptable  |
| CAC                   | (from script output)              | Varies by ACV                |
| LTV                   | (from script output)              | Minimum 3× CAC               |
| CAC Payback           | (from script output)              | <12mo good, <18mo acceptable |
| Magic Number          | (from script output)              | >0.75 efficient              |
| Burn Multiple         | Net burn / Net new ARR            | <1x excellent, <2x good      |
| Rule of 40            | Revenue growth % + FCF margin %   | >40 healthy                  |
| Gross Margin          | (Revenue − COGS) / Revenue        | >75% SaaS standard           |
| Revenue per Employee  | ARR / headcount                   | >$100K seed, >$200K A        |

### Marketplace KPIs

| Metric              | Formula                                  | Benchmark                |
| ------------------- | ---------------------------------------- | ------------------------ |
| GMV                 | Total transaction volume                 | Stage-dependent          |
| GMV Growth          | (GMV_now − GMV_prior) / GMV_prior        | >20% m/m early           |
| Take Rate           | Revenue / GMV                            | 5-30% varies by category |
| Liquidity           | Completed / Listed transactions          | >30% healthy             |
| Supply Growth       | New sellers or listings                  | Balanced with demand     |
| Demand Growth       | New buyers or orders                     | Balanced with supply     |
| Contribution Margin | (Revenue − variable costs) / transaction | Positive at scale        |
| Repeat Rate         | Repeat buyers / total buyers             | >30% good                |

### Consumer KPIs

| Metric            | Formula                        | Benchmark             |
| ----------------- | ------------------------------ | --------------------- |
| DAU / MAU         | Daily and monthly active users | Stage-dependent       |
| DAU/MAU Ratio     | Stickiness                     | >25% good, >50% great |
| D1 Retention      | Users returning day 1          | >40% good             |
| D7 Retention      | Users returning day 7          | >20% good             |
| D30 Retention     | Users returning day 30         | >10% good             |
| Session Frequency | Sessions per user per day      | Category-dependent    |
| ARPU              | Revenue / active users         | Category-dependent    |
| Viral Coefficient | Invites × conversion rate      | >1 viral growth       |

### Fintech KPIs

| Metric             | Formula                                    | Benchmark         |
| ------------------ | ------------------------------------------ | ----------------- |
| NIM                | (Interest earned − Interest paid) / assets | >3% for lending   |
| NPL Ratio          | Non-performing loans / total loans         | <5% healthy       |
| CAC Payback        | CAC / monthly profit per customer          | <12mo             |
| Take Rate          | Revenue / transaction volume               | Varies by product |
| Regulatory Capital | Capital / risk-weighted assets             | Above minimums    |

### General KPIs (Always Included)

| Metric         | Formula                  | Benchmark           |
| -------------- | ------------------------ | ------------------- |
| Revenue        | Monthly or annual        | Stage-dependent     |
| Revenue Growth | YoY or MoM               | Stage-dependent     |
| Burn Rate      | Monthly net cash outflow | Relative to revenue |
| Runway         | Cash / monthly burn      | >12 months          |
| Headcount      | Total employees          | Context-dependent   |

### Benchmarking & Health

Read `${CLAUDE_SKILL_DIR}/references/industry-multiples.md` for sector
benchmarks. Assign each metric a status:

- **Healthy**: At or above benchmark range
- **Watch**: Below benchmark but within acceptable range
- **Concerning**: Significantly below benchmark or trending poorly

### KPI Output Format

```markdown
# KPI Report: [Company Name]

**Company Type**: SaaS | Marketplace | Consumer | Fintech
**Reporting Period**: [date range or point-in-time]
**Data Source**: [user-provided / pitch deck / investor update]

## Key Metrics Summary

| Metric | Value | Benchmark | Status                       |
| ------ | ----- | --------- | ---------------------------- |
| ...    | ...   | ...       | Healthy / Watch / Concerning |

## Detailed Analysis

### Growth Metrics
[metrics with trend analysis]

### Unit Economics
[metrics with assessment]

### Efficiency Metrics
[metrics with assessment]

## Flags

### Healthy
- [metrics that look good, brief explanation]

### Concerning
- [metrics that need attention, brief explanation]

## Recommendation
[brief synthesis of KPI health and areas to monitor]
```

## Returns Mode (`--returns`)

Compute fund-level return metrics from investment data.

### Required Fields per Investment

- **Name**: Company or investment identifier
- **Investment date**: When capital was deployed
- **Investment amount**: Total capital invested
- **Distributions**: List of (date, amount) pairs for cash returned
- **Current NAV**: Current fair market value of remaining position (0 if
  fully exited)
- **As-of date**: Valuation date for NAV (defaults to today)

### Optional Fields

- **Benchmark IRR**: Public market benchmark for PME (default: 15%)

### Computation

Tell the user: **"Computing fund-level returns for [N] investments (IRR,
MOIC, DPI, TVPI, PME)..."**

Build a JSON scenario and run:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/financial_model.py" returns --input <temp.json>
```

Metrics computed per-investment and portfolio-level:

| Metric | Definition                                         |
| ------ | -------------------------------------------------- |
| MOIC   | (Distributions + NAV) / Invested                   |
| DPI    | Distributions / Invested (cash-on-cash)            |
| TVPI   | (Distributions + NAV) / Invested (total value)     |
| IRR    | Annualized return (XIRR on actual cash flow dates) |
| PME    | Actual return / benchmark return (>1x = outperform) |

### Returns Output Format

```markdown
# Returns Analysis

**As of**: [date]
**Benchmark**: [benchmark_irr]% (for PME)

## Individual Investments

| Investment | Invested | Distributions | NAV    | MOIC | DPI  | IRR  | PME  |
| ---------- | -------- | ------------- | ------ | ---- | ---- | ---- | ---- |
| [name]     | $[amt]   | $[amt]        | $[amt] | [x]x | [x]x | [x]% | [x]x |

## Portfolio Summary

| Metric              | Value  |
| ------------------- | ------ |
| Total Invested      | $[amt] |
| Total Distributions | $[amt] |
| Total NAV           | $[amt] |
| Total Value         | $[amt] |
| Portfolio MOIC      | [x]x   |
| Portfolio DPI       | [x]x   |
| Portfolio TVPI      | [x]x   |
| Portfolio IRR       | [x]%   |
| Portfolio PME       | [x]x   |

## Assessment

[Assessment text from script output: MOIC, IRR, DPI ratings]
```

### Benchmark Context (Returns)

| Metric | Top Quartile | Median     | Bottom Quartile |
| ------ | ------------ | ---------- | --------------- |
| IRR    | >25%         | 15-25%     | <8%             |
| MOIC   | >3.0x        | 2.0-3.0x   | <1.5x           |
| DPI    | >1.0x        | 0.5-1.0x   | <0.3x           |

## Portfolio Report Output Format

```markdown
# Portfolio Report

**Fund**: [name or "Portfolio"]
**Report Date**: [today's date]
**Companies**: [count] | **Total Invested**: $[amount]
**Data Source**: [CSV / JSON / user-provided]

## 1. Portfolio Summary
[summary card]

## 2. Portfolio Composition
### By Sector
### By Stage
### By Vintage Year

## 3. Performance Dashboard
[company table sorted by MOIC]

## 4. Cohort Analysis
### By Vintage Year
### By Stage at Entry

## 5. Risk Concentration
[concentration analysis with severity rating]

## 6. Follow-On Analysis
[follow-on needs and summary]

## 7. Exits & Write-Offs
### Realized Returns
### Loss Analysis

## 8. LP Executive Summary
[2-3 paragraph narrative]
```

## Export Formats

| Mode           | Default Exports        | Skip Flags          |
| -------------- | ---------------------- | ------------------- |
| Portfolio      | markdown + DOCX + XLSX | `--no-docx`, `--no-xlsx` |
| `--kpi`        | markdown + XLSX         | `--no-xlsx`         |
| `--returns`    | markdown + XLSX         | `--no-xlsx`         |

### Filenames

| Mode        | Markdown                             | DOCX                                 | XLSX                          |
| ----------- | ------------------------------------ | ------------------------------------ | ----------------------------- |
| Portfolio   | `portfolio-report-<YYYY-MM-DD>.md`   | `portfolio-report-<YYYY-MM-DD>.docx` | `portfolio-<YYYY-MM-DD>.xlsx` |
| `--kpi`     | `kpi-report-<YYYY-MM-DD>.md`         | —                                    | `kpi-report-<YYYY-MM-DD>.xlsx` |
| `--returns` | `returns-<YYYY-MM-DD>.md`            | —                                    | `returns-<YYYY-MM-DD>.xlsx`   |

Override with `--docx <filename>` / `--xlsx <filename>`. Tell the user where
each file was saved.

### XLSX Contents

**Portfolio report**:
- **Summary** — fund-level metrics and dashboard
- **Composition** — per-company holdings table
- **Cohorts** — vintage year analysis
- **Risk** — concentration and loss analysis

**KPI report**:
- **Key Metrics** — all computed KPIs with health assessment
- **Benchmarks** — industry benchmarks by company type

**Returns**:
- **Investments** — per-investment metrics
- **Portfolio Summary** — aggregate metrics
- **Cash Flows** — all dated cash flows for audit trail

Header rows bold; number formatting for dollars, percentages, multiples;
conditional formatting for health (KPI).

## Edge Cases

- **Single company**: Portfolio-level metrics not meaningful — skip cohort
  and concentration sections.
- **All companies same status**: Skip exits section if no exits, skip loss
  analysis if no write-offs.
- **Missing optional fields**: Proceed; note which analyses are limited.
- **Mixed currencies**: Ask user to confirm or convert. Do not mix in
  aggregations.
- **Very small portfolio** (<5 companies): Note that statistical patterns
  have limited significance.
- **Very large portfolio** (>50 companies): Focus on top/bottom performers
  and aggregates. Do not discuss every company individually in the LP summary.

## Disclaimer

After the output, read `${CLAUDE_SKILL_DIR}/references/disclaimers.md`:

- Portfolio report → **standard disclaimer**
- `--kpi` → **enhanced disclaimer** (contains financial figures)
- `--returns` → **enhanced disclaimer** (contains specific financial figures)
