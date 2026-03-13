---
name: vc-captable
description: Cap table modeling -- ownership, dilution, SAFE conversion, liquidation waterfall
---

# Cap Table Modeling

Model ownership structures, calculate dilution from new rounds, convert
SAFEs/notes into priced rounds, and run liquidation waterfall analysis.

## Input Handling

Parse the user's request to determine the operation:

- **"cap table" / "ownership"** → Build or display a cap table (`model`)
- **"dilution" / "new round"** → Show dilution impact (`dilution`)
- **"waterfall" / "liquidation" / "exit"** → Payout distribution (`waterfall`)
- **"convert" / "SAFE conversion" / "note conversion"** → SAFE/note conversion details (`convert`)
- **File path** → Read the file and determine operation from its contents
- **No clear operation** → Ask the user what they want to model

## Gathering Information

If the user hasn't provided enough detail, ask for the minimum required:

### For `model` (full cap table):
- Founders and their share counts
- Option pool size
- Any SAFEs or convertible notes (amount, cap, type)
- Any priced rounds (investment, pre-money valuation, option pool %)

### For `dilution`:
- Current holders and shares
- Total shares outstanding
- New round terms (investment, pre-money, option pool %)

### For `waterfall`:
- Exit value
- All holders: shares, instrument type, investment, liquidation preference
  details (multiple, participating, cap)

### For `convert`:
- Founders and shares
- SAFE/note details (amount, cap, discount, type)
- Priced round terms

## Running Calculations

1. Read `references/safe-mechanics.md` if SAFEs or notes are involved
2. Construct a JSON scenario object matching the script's expected format
3. Write the JSON to a temporary file
4. Run the calculation:

```bash
python3 "${CLAUDE_SKILL_DIR}/../scripts/captable.py" <command> --input <temp.json>
```

Commands: `model`, `dilution`, `waterfall`, `convert`

5. Parse the JSON output

## Presenting Results

### Cap Table (`model`)

Present as a markdown table:

| Holder | Instrument | Shares | Ownership % | Investment |
|--------|-----------|--------|-------------|------------|
| ... | ... | ... | ... | ... |

Include total shares and price per share below the table.

### Dilution (`dilution`)

Present as a before/after table:

| Holder | Shares | Pre-Round % | Post-Round % | Dilution % |
|--------|--------|------------|-------------|------------|
| ... | ... | ... | ... | ... |

Include post-money valuation and price per share.

### Waterfall (`waterfall`)

Present as a payout table:

| Holder | Instrument | Investment | Payout | Return Multiple | ROI |
|--------|-----------|------------|--------|----------------|-----|
| ... | ... | ... | ... | ... | ... |

Explain the waterfall steps:
1. Liquidation preferences paid first
2. Participation (if applicable)
3. Remaining distributed to common + converting preferred

### Conversion (`convert`)

Show each SAFE/note's conversion details:
- Price from cap vs. price from discount
- Which price was used (lower = better for investor)
- Shares issued

Then show the resulting cap table.

## Scenario Analysis

If the user asks "what if" questions, run multiple scenarios:

1. Build the base case
2. Modify the relevant parameter
3. Run both and present side-by-side comparison
4. Highlight the differences

Common scenarios:
- "What if the valuation is $X instead of $Y?"
- "What if we add another SAFE?"
- "What happens at different exit values?"

For exit scenarios, run the waterfall at 3+ exit values (e.g., 0.5x, 1x,
2x, 5x, 10x of last round post-money) to show how different stakeholders
fare.

## Validation

After presenting results, verify:
- All ownership percentages sum to 100%
- Conversion math is consistent with reference/safe-mechanics.md
- Liquidation preferences don't exceed exit value
- Share counts are internally consistent

## Disclaimers

Read `references/disclaimers.md` and append the **enhanced disclaimer**
(cap table outputs contain ownership percentages and financial figures).
