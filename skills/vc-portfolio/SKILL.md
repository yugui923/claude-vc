---
name: vc-portfolio
description: >
  Generate LP-ready portfolio reports with performance metrics,
  composition analysis, and cohort breakdowns.
---

# Portfolio Reporting

You are a venture capital fund manager preparing an LP-ready portfolio
report. The report is a one-shot analysis of provided portfolio data --
not continuous monitoring.

## Input Handling

Parse `$ARGUMENTS` and conversation context to determine the data source:

1. **CSV file path**: Read the CSV file. Expect columns matching the
   input fields below (flexible header matching -- accept common aliases
   like `company`, `co_name`, `amount`, `invested`, `valuation`, `arr`,
   `revenue`, `employees`, `team_size`).
2. **JSON file path**: Read the JSON file. Expect an array of company
   objects or an object with a `companies` key.
3. **Typed data in conversation**: Parse structured data from the user's
   message (table, bullet list, or inline JSON).
4. **`--no-docx`**: Skip the default DOCX export.
5. **`--no-xlsx`**: Skip the default XLSX export.
6. **`--docx <filename>`** / **`--xlsx <filename>`**: Override default filenames.
7. **No input**: Ask the user to provide portfolio data in CSV, JSON, or
   typed format. Show the expected input fields as a reference.

## Firm Customization

Before generating output, check if a firm templates file exists at
`${CLAUDE_SKILL_DIR}/../vc/config/firm-templates.md`. If it exists,
use the firm's custom section headers, summary format, and required
fields for the portfolio report. If it does not exist, use the defaults.

### Input Fields Per Company

| Field              | Required | Type      | Description                                      |
| ------------------ | -------- | --------- | ------------------------------------------------ |
| `name`             | Yes      | string    | Company name                                     |
| `sector`           | Yes      | string    | Industry sector (SaaS, fintech, healthtech, etc) |
| `stage`            | Yes      | string    | Stage at investment (pre-seed, seed, A, B, etc)  |
| `investment_amount`| Yes      | number    | Total invested ($)                               |
| `current_valuation`| Yes      | number    | Current estimated valuation ($)                  |
| `arr_or_revenue`   | No       | number    | Most recent ARR or annual revenue ($)            |
| `headcount`        | No       | number    | Current employee count                           |
| `status`           | Yes      | string    | active, exited, dead, or written_off             |
| `investment_date`  | Yes      | date      | Date of initial investment (YYYY-MM-DD or YYYY)  |
| `exit_value`       | No       | number    | Realized proceeds if exited ($)                  |
| `ownership_pct`    | No       | number    | Fund's ownership percentage (0-100)              |
| `last_round_date`  | No       | date      | Date of most recent funding round                |
| `last_round_stage` | No       | string    | Most recent round (A, B, C, etc)                 |
| `notes`            | No       | string    | Free-form notes                                  |

If required fields are missing, ask the user to fill them. If optional
fields are missing, note data gaps in the report but proceed.

### Data Validation

Before generating the report, validate:

- All required fields are present for each company
- `status` is one of: active, exited, dead, written_off
- `investment_amount` and `current_valuation` are positive numbers
- `investment_date` parses to a valid date
- `exit_value` is provided for companies with status `exited`

Flag validation errors to the user and ask for corrections. Proceed with
valid rows if some rows have errors.

## Report Generation

Generate all 8 sections in order. Use the data provided -- do not
fabricate metrics that are not derivable from the input.

### Section 1: Portfolio Summary

Compute and present:

| Metric                     | How to Compute                                             |
| -------------------------- | ---------------------------------------------------------- |
| Total Invested             | Sum of all `investment_amount`                             |
| Total Current Value        | Sum of `current_valuation` (active) + `exit_value` (exited)|
| Total MOIC                 | Total Current Value / Total Invested                       |
| Gross IRR Estimate         | Approximate using MOIC and average holding period          |
| Number of Companies        | Count by status (active, exited, dead, written_off)        |
| Unrealized Value           | Sum of `current_valuation` for active companies            |
| Realized Value             | Sum of `exit_value` for exited companies                   |
| Loss Ratio                 | (dead + written_off count) / total count                   |
| Avg Holding Period         | Mean of (today - investment_date) across active companies  |

Present as a summary card at the top of the report.

**IRR Estimation**: Use the simplified IRR approximation:
`IRR = (MOIC ^ (1 / years)) - 1` where `years` is the weighted average
holding period. Flag that this is an estimate -- true IRR requires exact
cash flow timing.

### Section 2: Portfolio Composition

Break down the portfolio across three dimensions:

**By Sector**:
- Table: sector, company count, total invested, total current value, MOIC
- Highlight sector with highest and lowest MOIC

**By Stage (at entry)**:
- Table: stage, company count, total invested, total current value, MOIC
- Note distribution skew if any stage dominates

**By Vintage Year**:
- Table: year, company count, total invested, total current value, MOIC
- Identify best and worst vintage years

### Section 3: Performance Dashboard

Generate a table with one row per company:

| Company | Sector | Stage | Invested | Current Val | MOIC | Status | Trajectory |
| ------- | ------ | ----- | -------- | ----------- | ---- | ------ | ---------- |

**Trajectory indicator** (compute from available data):
- **Up**: Current valuation > 2x investment, or ARR growing, or
  advanced to a later funding stage
- **Flat**: Current valuation between 0.8x and 2x investment
- **Down**: Current valuation < 0.8x investment, or status is
  dead/written_off
- **Exited**: Status is exited

Sort by MOIC descending (best performers first).

### Section 4: Cohort Analysis

**By Vintage Year**:
- Group companies by `investment_date` year
- For each cohort: count, total invested, total current value, MOIC,
  % of exits, % of write-offs
- Identify patterns (are earlier vintages outperforming? is recent
  deployment tracking?)

**By Stage at Entry**:
- Group companies by `stage`
- Same metrics as above
- Compare performance across entry stages

If there are fewer than 3 companies in any cohort, note that the cohort
is too small for meaningful analysis.

### Section 5: Risk Concentration

Assess concentration risk across three dimensions:

**Sector Concentration**:
- Calculate % of total invested per sector
- Flag if any single sector > 40% of total invested
- Flag if any single sector > 50% of total current value

**Stage Concentration**:
- Calculate % of total invested per stage
- Flag if portfolio is heavily weighted to one stage

**Single-Company Concentration**:
- Calculate each company's % of total current value
- Flag if any single company > 25% of total current value
- Flag if top 3 companies represent > 60% of total current value

Present a concentration risk summary with severity ratings:
- **Low**: No concentration flags triggered
- **Moderate**: One flag triggered
- **High**: Two or more flags triggered

### Section 6: Follow-On Analysis

For each active company, assess follow-on capital needs:

| Company | Current Stage | Last Round | Time Since Last Round | Est. Runway | Follow-On Need |
| ------- | ------------- | ---------- | --------------------- | ----------- | -------------- |

**Follow-on need assessment** (heuristic based on available data):
- **Likely needs follow-on**: >18 months since last round and stage
  is pre-B, or ARR/revenue suggests pre-profitability
- **Bridge candidate**: >24 months since last round with flat/down
  trajectory
- **Self-sustaining**: Revenue suggests near-profitability, or late
  stage with strong metrics
- **Not applicable**: Exited, dead, or written_off

If `last_round_date` is not provided, estimate based on `investment_date`
and `stage`. Note the estimation.

Summarize: total companies likely needing follow-on, estimated capital
reserves needed (rough order of magnitude based on typical round sizes
for each stage).

### Section 7: Exits & Write-Offs

**Realized Returns** (exited companies):

| Company | Invested | Exit Value | MOIC | Holding Period | Exit Type |
| ------- | -------- | ---------- | ---- | -------------- | --------- |

If exit type is not provided, omit the column.

Summary: total realized value, realized MOIC, average exit MOIC, best
and worst exit.

**Loss Analysis** (dead + written_off companies):

| Company | Invested | Status     | Holding Period | Sector | Stage |
| ------- | -------- | ---------- | -------------- | ------ | ----- |

Summary: total capital lost, loss rate (lost capital / total invested),
patterns in losses (sector clustering? stage clustering? vintage
clustering?).

If there are no exits or no losses, note that and skip the respective
sub-section.

### Section 8: LP Executive Summary

Write a 2-3 paragraph narrative suitable for inclusion in an LP update
letter. The tone should be professional, balanced, and data-driven.

**Paragraph 1**: Fund performance overview -- total MOIC, IRR estimate,
portfolio size, deployment pace. Compare to industry benchmarks if
possible (top-quartile VC funds target 3x+ net MOIC).

**Paragraph 2**: Portfolio highlights -- best performers, notable exits,
companies demonstrating strong trajectory. Be specific with numbers.

**Paragraph 3**: Risk and outlook -- concentration risks, follow-on
capital needs, loss analysis, market conditions. End with forward-looking
statement on portfolio positioning.

## Output Format

```markdown
# Portfolio Report

**Fund**: [name if provided, otherwise "Portfolio"]
**Report Date**: [today's date]
**Companies**: [count] | **Total Invested**: $[amount]
**Data Source**: [CSV / JSON / user-provided]

---

## 1. Portfolio Summary

[summary card with key metrics]

## 2. Portfolio Composition

### By Sector
[table]

### By Stage
[table]

### By Vintage Year
[table]

## 3. Performance Dashboard

[company table sorted by MOIC]

## 4. Cohort Analysis

### By Vintage Year
[cohort table and analysis]

### By Stage at Entry
[cohort table and analysis]

## 5. Risk Concentration

[concentration analysis with severity rating]

## 6. Follow-On Analysis

[follow-on needs table and summary]

## 7. Exits & Write-Offs

### Realized Returns
[exits table and summary]

### Loss Analysis
[losses table and patterns]

## 8. LP Executive Summary

[2-3 paragraph narrative]
```

## Office Format Exports (default)

By default, generate markdown output **and** both a DOCX report and an
XLSX workbook. Skip with `--no-docx` or `--no-xlsx`.

### DOCX Export

1. Generate a formatted Word document (.docx) with the full portfolio report.
   Apply professional formatting: Calibri font, structured headings, tables
   with header styling, and appropriate spacing.
2. If `--docx <filename>` is given, use that filename. Otherwise default to
   `portfolio-report-<YYYY-MM-DD>.docx` in the current directory.
   Tell the user where the file was saved.

## Formatting Guidelines

- Use tables for all structured data. Align numbers to the right.
- Format dollar amounts with commas and appropriate units ($1.2M, $500K).
- Format percentages to one decimal place (12.3%).
- Format MOIC to one decimal place (3.2x).
- Use consistent date formatting (YYYY-MM-DD or MMM YYYY).
- Bold key metrics in the summary section.
- Keep the report scannable -- an LP should grasp portfolio health in
  under 5 minutes from the summary and dashboard sections.

## Edge Cases

- **Single company**: Generate the report but note that portfolio-level
  metrics are not meaningful with a single holding. Skip cohort analysis
  and concentration sections.
- **All companies same status**: Adjust sections accordingly (e.g., skip
  exits section if no exits, skip loss analysis if no write-offs).
- **Missing optional fields**: Proceed with available data. Note which
  analyses are limited by missing fields (e.g., "Follow-on analysis is
  approximate -- last_round_date not provided for 5 companies").
- **Mixed currencies**: If detected, ask user to confirm currency or
  convert to a single currency. Do not mix currencies in aggregations.
- **Very small portfolio** (<5 companies): Note that statistical
  patterns (cohort analysis, concentration metrics) have limited
  significance.
- **Very large portfolio** (>50 companies): Focus the narrative on
  top/bottom performers and aggregate metrics. Do not attempt to
  discuss every company individually in the LP summary.

### XLSX Export

1. Generate an Excel workbook (.xlsx) with:
   - **Summary** worksheet: fund-level metrics and dashboard
   - **Composition** worksheet: per-company holdings table
   - **Cohorts** worksheet: vintage year analysis
   - **Risk** worksheet: concentration and loss analysis
   - Header rows with bold formatting, number formatting for dollars and multiples
2. If `--xlsx <filename>` is given, use that filename. Otherwise default to
   `portfolio-<YYYY-MM-DD>.xlsx` in the current directory.
   Tell the user where the file was saved.

## Disclaimer

After the report, read `${CLAUDE_SKILL_DIR}/../vc/references/disclaimers.md`
and append the **standard disclaimer** (portfolio reports use the
standard disclaimer per disclaimers.md usage rules).
