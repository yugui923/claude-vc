---
name: vc-terms
description: Term sheet analysis -- flag non-standard provisions against NVCA baseline
---

# Term Sheet Analysis

Analyze term sheets, SAFE agreements, and convertible notes against
NVCA model terms and market norms. Flag non-standard provisions and
explain implications.

## Input Handling

- **File path** (.pdf, .md, .txt, .docx): Read the document with the Read tool
- **URL**: Fetch with WebFetch
- **Pasted text**: Analyze directly
- **"SAFE" / "convertible note"**: Focus analysis on SAFE/note-specific terms
- **No input**: Ask the user for a term sheet to analyze

## Analysis Process

### Step 1: Read References

Load these reference files (on-demand, not all at once):
- `${CLAUDE_SKILL_DIR}/../vc/references/term-sheet-terms.md` — NVCA baseline and market norms
- `${CLAUDE_SKILL_DIR}/../vc/references/safe-mechanics.md` — if analyzing a SAFE or convertible note

### Step 2: Extract Terms

Parse the document and extract key terms into structured categories:

**Economics**:
- Pre-money / post-money valuation
- Investment amount and price per share
- Liquidation preference (multiple, participating/non-participating, cap)
- Anti-dilution protection (type)
- Dividends (type, rate)
- Pay-to-play provisions
- Valuation cap and discount (SAFEs/notes)

**Control**:
- Board composition
- Protective provisions (list each)
- Drag-along / tag-along rights
- Information rights
- Voting rights

**Founder Terms**:
- Vesting schedule and cliff
- Acceleration (single/double trigger)
- Non-compete / non-solicit
- IP assignment

**Investor Rights**:
- Pro-rata rights and major investor threshold
- ROFR and co-sale
- Registration rights
- Redemption rights

**Other**:
- No-shop / exclusivity period
- Conditions to closing
- Legal fees allocation
- Key representations and warranties

### Step 3: Compare Against Baseline

For each extracted term, compare against the reference baseline:

| Term | Proposed | Market Standard | Assessment |
|------|----------|----------------|------------|
| Liquidation pref | 1x participating | 1x non-participating | Investor-favorable |
| Anti-dilution | Full ratchet | Broad-based weighted avg | Aggressive |
| ... | ... | ... | ... |

Assessment categories:
- **Standard**: Matches NVCA model / market norm
- **Investor-favorable**: Benefits investor beyond market standard
- **Founder-favorable**: Benefits founder beyond market standard
- **Aggressive**: Significantly non-standard, warrants pushback
- **Missing**: Expected term not found in document

### Step 4: Flag Non-Standard Provisions

For each non-standard term:
1. **What it says**: Quote or paraphrase the specific provision
2. **Why it matters**: Concrete impact on founders/company
3. **Market context**: How common this is and when it's typically seen
4. **Negotiation suggestion**: What to propose instead

Prioritize flags by impact:
- **High impact**: Liquidation preferences >1x, full ratchet, investor
  board majority at early stage, aggressive protective provisions,
  no acceleration on CIC
- **Medium impact**: Participating preferred, narrow-based anti-dilution,
  unusual vesting, broad non-compete, high major investor threshold
- **Low impact**: Minor information rights expansions, standard ROFR
  variations, registration rights details

### Step 5: Summarize

Provide a summary section:

**Overall Assessment**: [Founder-favorable / Balanced / Investor-favorable / Aggressive]

**Top 3 Negotiation Priorities**:
1. Most impactful non-standard term → suggested counter
2. Second most impactful → suggested counter
3. Third most impactful → suggested counter

**Terms That Are Standard** (brief list to reassure)

**Missing Terms to Add** (if any expected provisions are absent)

## SAFE / Convertible Note Analysis

When analyzing a SAFE or convertible note specifically:

1. Identify the variant (post-money vs. pre-money, standard vs. MFN)
2. Evaluate the valuation cap against current market for stage
3. Assess the discount rate against standard range (15-25%)
4. Check for unusual provisions:
   - Qualified financing threshold (is it too high?)
   - Pro-rata rights (present or absent?)
   - MFN clause scope
   - Amendment provisions
   - Information rights

5. Run conversion scenario:
   - Use `captable.py convert` to show how the SAFE/note converts
   - Show resulting ownership at different round valuations

## Side-by-Side Comparison

If the user provides multiple term sheets (e.g., competing offers):

| Term | Offer A | Offer B | Offer C |
|------|---------|---------|---------|
| Pre-money | $15M | $12M | $18M |
| Liq pref | 1x non-part | 1x part | 1x non-part |
| ... | ... | ... | ... |

Highlight which offer is most founder-friendly on each dimension and
overall.

## Disclaimers

Read `${CLAUDE_SKILL_DIR}/../vc/references/disclaimers.md` and append the **enhanced disclaimer**
(term sheet analysis involves legal and financial provisions).

Remind the user: "This analysis identifies terms that deviate from market
norms but does not constitute legal advice. Engage qualified legal counsel
before signing any term sheet."
