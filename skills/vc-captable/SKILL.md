---
name: vc-captable
description: >
  Cap table modeling -- ownership, dilution, SAFE conversion,
  multi-series liquidation waterfall, exit scenario analysis.
  Informed by the Open Cap Table Format (OCF) standard.
---

# Cap Table Modeling

Model ownership structures, calculate dilution from new rounds, convert
SAFEs/notes into priced rounds, and run liquidation waterfall analysis
with multi-series seniority support.

## Input Handling

Parse the user's request to determine the operation:

- **"cap table" / "ownership"** → Build or display a cap table (`model`)
- **"dilution" / "new round"** → Show dilution impact (`dilution`)
- **"waterfall" / "liquidation" / "exit"** → Payout distribution (`waterfall`)
- **"convert" / "SAFE conversion" / "note conversion"** → Conversion details (`convert`)
- **"scenarios" / "what if" / "exit analysis"** → Multi-exit comparison (`scenarios`)
- **File path** → Read the file and determine operation from its contents
- **No clear operation** → Ask the user what they want to model

## Gathering Information

If the user hasn't provided enough detail, ask for the minimum required:

### For `model` (full cap table):
- Founders and their share counts
- Option pool size
- SAFEs: amount, valuation cap, type (post-money/pre-money), discount,
  MFN status
- Convertible notes: amount, cap, discount, interest rate and type
  (simple/compound), months outstanding
- Priced rounds: investment, pre-money valuation, option pool %

### For `waterfall`:
- Exit value (or multiple exit values for scenarios)
- Stock classes: name, seniority (higher = more senior), liquidation
  multiple, participating/non-participating, participation cap
- All holders: shares, stock class, investment amount

### For `convert`:
- Founders and shares
- SAFE/note details including MFN status and capitalization definition
- Priced round terms

## Running Calculations

1. Read `${CLAUDE_SKILL_DIR}/../vc/references/safe-mechanics.md` if SAFEs
   or notes are involved
2. Construct a JSON scenario object matching the script's expected format
3. Write the JSON to a temporary file
4. Run the calculation:

```bash
python3 "${CLAUDE_SKILL_DIR}/../vc/scripts/captable.py" <command> --input <temp.json>
```

Commands: `model`, `dilution`, `waterfall`, `convert`, `scenarios`

5. Parse the JSON output

## Stock Classes

When building waterfall or scenario analyses with multiple preferred
series, define stock classes in the JSON:

```json
{
  "stock_classes": [
    {"class_id": "common", "name": "Common", "instrument_type": "common", "seniority": 1},
    {"class_id": "series_a", "name": "Series A", "instrument_type": "preferred",
     "seniority": 2, "liquidation_multiple": 1, "participating": false},
    {"class_id": "series_b", "name": "Series B", "instrument_type": "preferred",
     "seniority": 3, "liquidation_multiple": 1.5, "participating": true, "participation_cap": 3}
  ]
}
```

Higher seniority = paid first in waterfall. Each holder references their
stock class via `stock_class_id`.

## Presenting Results

### Cap Table (`model`)

| Holder | Class | Shares | Ownership % | Investment |
|--------|-------|--------|-------------|------------|
| ... | ... | ... | ... | ... |

### Waterfall (`waterfall`)

Explain the distribution steps:
1. Liquidation preferences paid in seniority order (most senior first)
2. Participation rights (if applicable, with caps)
3. Non-participating preferred: convert if as-common payout is higher
4. Remaining distributed pro-rata to common holders

| Holder | Class | Investment | Payout | Multiple | ROI |
|--------|-------|------------|--------|----------|-----|

### Scenarios (`scenarios`)

Present a matrix showing each holder's payout at different exit values:

| Exit Value | Founder | ESOP | Series A | Series B |
|------------|---------|------|----------|----------|
| $10M | ... | ... | ... | ... |
| $25M | ... | ... | ... | ... |
| $50M | ... | ... | ... | ... |

### Conversion (`convert`)

Show each instrument's conversion details:
- Price from cap vs price from discount
- Which price was used and why
- MFN resolution (if applicable)
- Accrued interest (simple or compound)
- Shares issued

Then show the resulting cap table.

## Validation

After presenting results, verify:
- All ownership percentages sum to 100%
- Liquidation preferences don't exceed exit value
- Share counts are internally consistent
- MFN SAFEs resolved to the correct cap

## Disclaimers

Read `${CLAUDE_SKILL_DIR}/../vc/references/disclaimers.md` and append
the **enhanced disclaimer** (cap table outputs contain ownership
percentages and financial figures).
