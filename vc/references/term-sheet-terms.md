# Term Sheet Terms Reference

> NVCA model term benchmarks and market commentary. Used by vc-terms
> sub-skill to flag non-standard provisions.

## Economics

### Liquidation Preference

| Variant | Standard? | Description |
|---------|-----------|-------------|
| 1x non-participating | Yes | Investor gets 1x back OR converts to common (whichever is greater) |
| 1x participating | Cautious | 1x back AND pro-rata share of remaining proceeds |
| 1x participating w/ cap | Moderate | Same as above but participation capped (typically 2-3x) |
| >1x non-participating | Non-standard | Multiple on return before common sees anything |
| >1x participating | Aggressive | Rare; typically only in distressed rounds |

**Market norm**: 1x non-participating preferred. Participating preferred is
more common in later stages or investor-favorable markets.

### Anti-Dilution

| Variant | Standard? | Description |
|---------|-----------|-------------|
| Broad-based weighted average | Yes | Adjusts conversion price using all outstanding shares |
| Narrow-based weighted average | Cautious | Uses only preferred shares in denominator; more dilutive |
| Full ratchet | Aggressive | Resets price to new lower price regardless of round size |

**Market norm**: Broad-based weighted average is standard. Full ratchet is
rare except in down rounds or distressed situations.

### Dividends

| Variant | Standard? | Description |
|---------|-----------|-------------|
| Non-cumulative, when declared | Yes | Only paid when board declares; no accrual |
| Cumulative | Non-standard | Accrues whether declared or not; adds to liquidation preference |

**Market norm**: Non-cumulative. Cumulative dividends effectively increase
liquidation preference over time.

### Pay-to-Play

Requires existing investors to participate pro-rata in future rounds or
lose their preferred rights (convert to common). **Increasingly common** in
Series A+ as a founder protection mechanism.

## Control

### Board Composition

| Structure | Standard? | Notes |
|-----------|-----------|-------|
| Founder majority | Standard (Seed-A) | 2 founders + 1 investor, or 2F+1I+1 independent |
| Balanced | Standard (Series B) | Equal founder + investor seats + 1-2 independents |
| Investor majority | Non-standard | Rare before Series C; flag if proposed at early stage |

**Market norm**: Founders maintain board control through Series A. Shift
toward balance at Series B. Independent directors increasingly expected.

### Protective Provisions

Standard set (NVCA model):

- Changes to charter/bylaws affecting preferred
- Issuance of shares senior to or pari passu with preferred
- Dividend declarations
- Liquidation, dissolution, or merger
- Increase in authorized shares
- Changes to board size
- Incurrence of debt above a threshold

**Non-standard additions** (flag these):

- Approval rights over annual budgets
- Veto on hiring/firing key executives
- Approval for individual expenditures above a threshold
- Veto on new product lines or market entry
- Approval for any contract above a threshold

### Drag-Along

Standard: Majority of common + majority of preferred can force all
shareholders to approve a sale. **Non-standard**: Lower thresholds
(e.g., only preferred holders can trigger drag).

### Information Rights

Standard: Annual audited financials, quarterly unaudited, annual budget,
monthly reporting (varies). **Non-standard**: Weekly reporting, access to
all internal tools, attendance at all-hands.

## Founder Terms

### Vesting

| Term | Standard | Non-standard |
|------|----------|--------------|
| Schedule | 4 years | <3 or >5 years |
| Cliff | 1 year | No cliff or >1 year |
| Acceleration | Single-trigger on CIC (partial or full) | No acceleration |
| Credit for time served | Yes if >6 months pre-funding | None for pre-funding time |

**Market norm**: 4-year vesting with 1-year cliff. Single-trigger partial
acceleration on change of control is increasingly standard.

### Non-Compete / Non-Solicit

- **Non-compete**: 12 months post-departure is standard. >18 months is
  aggressive. Note: unenforceable in many jurisdictions (CA, CO, MN, etc.)
- **Non-solicit**: 12-18 months for employees; 12 months for customers

### IP Assignment

All IP must be assigned to the company (standard, non-negotiable). Prior
inventions should be carved out explicitly. Flag if assignment is missing.

## Investor Rights

### Pro-Rata Rights

Right to participate in future rounds to maintain ownership percentage.
Standard for institutional investors. **Major investor threshold** varies
(common: $250K-$1M minimum investment).

### Right of First Refusal (ROFR) and Co-Sale

- **ROFR**: Company and/or investors can match any founder share sale
- **Co-sale / tag-along**: Investors can sell proportionally alongside
  founders

Both are standard. Flag if absent.

### Registration Rights

- **Demand registration**: Investors can force IPO registration (standard
  after 3-5 years)
- **S-3 registration**: Piggyback on S-3 filings (standard, 2 per year)
- **Piggyback registration**: Join any company-initiated registration

Standard provisions; mostly relevant at later stages.

## Conversion

### Voluntary Conversion

Preferred converts to common at holder's option at any time. Standard
(1:1 ratio, adjusted for anti-dilution).

### Automatic Conversion

Preferred automatically converts on:

- IPO above a minimum price (typically 2-3x original purchase price)
- Vote of majority of preferred

**Flag**: Unusually high auto-conversion thresholds (>5x).

## SAFE / Convertible Note Specific

### Valuation Cap

Maximum valuation at which the instrument converts. Lower cap = more
investor-friendly. Compare to current market valuations for stage.

### Discount

Typical: 15-25%. Applies to price per share in the qualified financing.
Stacks on top of cap if both are present (investor gets the better of
the two, not both combined).

### Qualified Financing Threshold

Minimum round size that triggers conversion. Standard: $1M for notes,
no threshold for post-money SAFEs. Flag if threshold is unusually high
(may prevent conversion).

### Interest Rate (Notes Only)

Typical: 4-8% simple interest. Accrues and converts into equity at the
conversion event. Higher rates effectively increase the discount.

### Maturity Date (Notes Only)

Typical: 18-24 months. At maturity, note either converts at a negotiated
cap or becomes repayable (though repayment is rarely enforced in
practice).
