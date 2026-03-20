---
name: vc-model
description: >
  Generate a simplified 3-statement financial model (income statement,
  balance sheet, cash flow). Accepts pitch deck data, company financials,
  or assumptions. Projects 3-5 years forward. Use when user says
  "financial model", "3-statement", "projections", "P&L",
  "income statement", "balance sheet", or "cash flow".
---

# Financial Model Generation

Build a simplified 3-statement financial model suitable for early-stage
startup analysis. Designed for seed through Series B companies where many
line items are zero or estimated.

## Input Handling

Determine the data source from `$ARGUMENTS` and conversation context:

1. **After a screening or memo** (most common): Use existing context — revenue
   figures, growth rates, and business model details already gathered.
2. **File path**: Read the pitch deck, financials spreadsheet, or investor
   update for the raw data.
3. **URL**: Fetch the company website for public financials or pricing data.
4. **Verbal description**: User provides key assumptions directly.
5. **No input**: Ask for the minimum required inputs (see below).
6. **`--no-docx`**: Skip the default DOCX export.
7. **`--no-xlsx`**: Skip the default XLSX export.
8. **`--docx <filename>`** / **`--xlsx <filename>`**: Override default filenames.

### Minimum Required Inputs

If data is insufficient, ask for these (in priority order):

1. **Current revenue** (ARR, MRR, or annual revenue)
2. **Revenue growth rate** (or rates for each projected year)
3. **Gross margin** (or COGS as % of revenue)
4. **Key OpEx lines** (S&M, R&D, G&A as % of revenue, or total OpEx)
5. **Cash on hand** (starting cash position)
6. **Projection period** (default: 5 years)

For any missing inputs, derive reasonable assumptions based on the
company's stage, sector, and comparable companies. Reference
`${CLAUDE_SKILL_DIR}/../vc/references/industry-multiples.md` for
sector benchmarks. State all assumptions explicitly.

## Building the Model

### Step 1: Construct Assumptions

Build a JSON scenario matching the script's expected format. Key
decisions Claude must make:

**Revenue growth**: Use company-provided projections if available.
Otherwise estimate based on stage:

- Seed: 100-200% Y1, decaying 20-30% per year
- Series A: 80-120% Y1, decaying 15-25% per year
- Series B: 50-80% Y1, decaying 10-20% per year

**COGS / Gross margin**: Derive from business model:

- SaaS: 75-85% gross margin (COGS = hosting, support)
- Marketplace: 60-75% (COGS = payment processing, fulfillment)
- Hardware: 30-50% (COGS = manufacturing, materials)

**OpEx breakdown** (as % of revenue, improving over time):

- S&M: 30-50% early, declining to 15-25% at scale
- R&D: 20-35% early, declining to 15-20% at scale
- G&A: 10-20% early, declining to 5-10% at scale

**Balance sheet**: AR days (30-60 for B2B SaaS, 0-15 for consumer),
AP days (15-45), capex 2-5% of revenue.

### Step 2: Run Calculation

Write the JSON scenario to a temporary file and run:

```bash
python3 "${CLAUDE_SKILL_DIR}/../vc/scripts/financial_model.py" three_statement --input <temp.json>
```

### Step 3: Present Results

Parse the JSON output and present as three markdown tables:

**Income Statement**

| Line Item        | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
| ---------------- | ------ | ------ | ------ | ------ | ------ |
| Revenue          | ...    | ...    | ...    | ...    | ...    |
| COGS             | ...    | ...    | ...    | ...    | ...    |
| **Gross Profit** | ...    | ...    | ...    | ...    | ...    |
| S&M              | ...    | ...    | ...    | ...    | ...    |
| R&D              | ...    | ...    | ...    | ...    | ...    |
| G&A              | ...    | ...    | ...    | ...    | ...    |
| **EBITDA**       | ...    | ...    | ...    | ...    | ...    |
| D&A              | ...    | ...    | ...    | ...    | ...    |
| **Net Income**   | ...    | ...    | ...    | ...    | ...    |

**Balance Sheet** (simplified)

| Line Item           | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
| ------------------- | ------ | ------ | ------ | ------ | ------ |
| Cash                | ...    | ...    | ...    | ...    | ...    |
| Accounts Receivable | ...    | ...    | ...    | ...    | ...    |
| **Total Assets**    | ...    | ...    | ...    | ...    | ...    |
| Accounts Payable    | ...    | ...    | ...    | ...    | ...    |
| **Equity**          | ...    | ...    | ...    | ...    | ...    |

**Cash Flow Statement** (simplified)

| Line Item      | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
| -------------- | ------ | ------ | ------ | ------ | ------ |
| Operating CF   | ...    | ...    | ...    | ...    | ...    |
| CapEx          | ...    | ...    | ...    | ...    | ...    |
| **Net Change** | ...    | ...    | ...    | ...    | ...    |
| Ending Cash    | ...    | ...    | ...    | ...    | ...    |

### Step 4: Analysis

After presenting the tables, add a brief analysis:

- **Break-even timing**: When does the company reach profitability?
- **Cash runway**: How long until cash runs out at current burn?
- **Margin progression**: How do margins improve over time?
- **Key sensitivities**: Which assumptions matter most?

## Scenario Comparison

If the user asks for scenarios (bull/base/bear), run three models with
different growth and margin assumptions and present side-by-side.

## Office Format Exports (default)

By default, generate markdown output **and** both a DOCX report and an
XLSX workbook. Skip with `--no-docx` or `--no-xlsx`.

### DOCX Export

1. Generate a formatted Word document with the 3-statement tables and
   analysis narrative. Professional formatting: Calibri font, structured
   headings, tables with header styling.
2. Default filename: `financial-model-<YYYY-MM-DD>.docx`

### XLSX Export

1. Generate an Excel workbook (.xlsx) with:
   - **Income Statement** worksheet: revenue through net income
   - **Balance Sheet** worksheet: assets, liabilities, equity
   - **Cash Flow** worksheet: operating, investing, financing activities
   - Header rows with bold formatting, number formatting for dollar amounts
2. Default filename: `financial-model-<YYYY-MM-DD>.xlsx`

## Disclaimer

Read `${CLAUDE_SKILL_DIR}/../vc/references/disclaimers.md` and append
the **enhanced disclaimer** (contains financial projections).
