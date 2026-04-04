---
name: vc-returns
description: >
  Calculate fund-level return metrics (IRR, MOIC, DPI, TVPI, PME)
  from investment data.
---

# Returns Analysis

Calculate fund-level return metrics for individual investments or an
entire portfolio. Produces IRR, MOIC, DPI, TVPI, and PME with
assessment benchmarks.

## Input Handling

1. **Structured data** (JSON or CSV): Parse directly into investments.
2. **Verbal description**: Extract investment dates, amounts,
   distributions, and current NAV from natural language.
3. **File path**: Read the file and extract investment data.
4. **After a portfolio report**: Use investment data already in context.
5. **No input**: Ask for the minimum required fields per investment.

### Required Fields Per Investment

- **Name**: Company or investment identifier
- **Investment date**: When the capital was deployed
- **Investment amount**: Total capital invested
- **Distributions**: List of (date, amount) pairs for cash returned
- **Current NAV**: Current fair market value of remaining position
  (0 if fully exited)
- **As-of date**: Valuation date for NAV (defaults to today)

### Optional Fields

- **Benchmark IRR**: Public market benchmark rate for PME calculation
  (default: 15% if not specified, representing median VC benchmark)

## Computation

Build a JSON scenario and run:

```bash
python3 "${CLAUDE_SKILL_DIR}/../vc/scripts/financial_model.py" returns --input <temp.json>
```

The script computes per-investment and portfolio-level:

| Metric | Definition                                       |
| ------ | ------------------------------------------------ |
| MOIC   | (Distributions + NAV) / Invested                 |
| DPI    | Distributions / Invested (cash-on-cash)           |
| TVPI   | (Distributions + NAV) / Invested (total value)    |
| IRR    | Annualized return (XIRR on actual cash flow dates)|
| PME    | Actual return / benchmark return (>1x = outperform)|

## Output Format

Present results as:

```markdown
# Returns Analysis

**As of**: [date]
**Benchmark**: [benchmark_irr]% (for PME)

## Individual Investments

| Investment  | Invested | Distributions | NAV    | MOIC  | DPI   | IRR   | PME   |
| ----------- | -------- | ------------- | ------ | ----- | ----- | ----- | ----- |
| [name]      | $[amt]   | $[amt]        | $[amt] | [x]x  | [x]x  | [x]%  | [x]x  |

## Portfolio Summary

| Metric              | Value    |
| ------------------- | -------- |
| Total Invested      | $[amt]   |
| Total Distributions | $[amt]   |
| Total NAV           | $[amt]   |
| Total Value         | $[amt]   |
| Portfolio MOIC      | [x]x     |
| Portfolio DPI       | [x]x     |
| Portfolio TVPI      | [x]x     |
| Portfolio IRR       | [x]%     |
| Portfolio PME       | [x]x     |

## Assessment

[Assessment text from script output: MOIC, IRR, DPI ratings]
```

## Benchmark Context

Provide context for the return metrics:

| Metric | Top Quartile | Median     | Bottom Quartile |
| ------ | ------------ | ---------- | --------------- |
| IRR    | >25%         | 15-25%     | <8%             |
| MOIC   | >3.0x        | 2.0-3.0x   | <1.5x           |
| DPI    | >1.0x        | 0.5-1.0x   | <0.3x           |

## XLSX Export (default)

By default, generate both markdown output **and** an Excel workbook.
Skip XLSX export only if `--no-xlsx` is present in arguments.

1. Generate the returns analysis as markdown normally
2. Generate an Excel workbook with:
   - **Investments** worksheet: per-investment metrics table
   - **Portfolio Summary** worksheet: aggregate metrics
   - **Cash Flows** worksheet: all dated cash flows for audit trail
3. If `--xlsx <filename>` is given, use that filename. Otherwise default to
   `returns-<YYYY-MM-DD>.xlsx` in the current directory.
   Tell the user where the file was saved.

## Disclaimer

Read `${CLAUDE_SKILL_DIR}/../vc/references/disclaimers.md` and append the
**enhanced** disclaimer (this output contains specific financial figures).
