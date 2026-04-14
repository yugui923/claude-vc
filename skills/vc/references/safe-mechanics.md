# SAFE Mechanics Reference

> YC SAFE variants and conversion calculations. Used by the `/vc captable`
> and `/vc terms` commands.

## SAFE Variants

### Post-Money SAFE (Current Standard, 2018+)

The valuation cap is the **post-money valuation** including the SAFE itself.
Investor ownership is simply: `investment / valuation cap`.

- **Standard**: Valuation cap only (no discount)
- **MFN (Most Favored Nation)**: No cap; converts on terms of the next SAFE
  that has a cap or better terms

**Key property**: Post-money SAFEs are dilutive to founders, not to each
other. Each new post-money SAFE dilutes the founders' percentage.

### Pre-Money SAFE (Legacy)

The valuation cap is the **pre-money valuation** excluding the SAFE.
Ownership depends on how much total capital converts.

- Conversion creates a "pile-on" effect: more SAFEs = more dilution to
  each SAFE holder (and to founders)
- Harder to calculate exact ownership before a priced round

### Key Differences

| Aspect             | Post-Money              | Pre-Money                       |
| ------------------ | ----------------------- | ------------------------------- |
| Cap basis          | Includes SAFE amount    | Excludes SAFE amount            |
| Investor ownership | Known at signing        | Unknown until conversion        |
| Multiple SAFEs     | Don't dilute each other | Dilute each other               |
| Founder dilution   | More dilutive per SAFE  | Less dilutive per SAFE          |
| Market prevalence  | Standard (2018+)        | Legacy; still seen occasionally |

## Conversion Mechanics

### Post-Money SAFE Conversion

When a priced equity round (qualified financing) occurs:

1. **SAFE conversion price** = `valuation_cap / company_capitalization`
   - Company capitalization = all shares outstanding + option pool +
     all converting SAFEs (for post-money)
2. **Shares issued** = `investment_amount / conversion_price`
3. If SAFE has a discount: `discounted_price = round_price * (1 - discount)`
4. Investor gets the **lower** of cap-derived price and discounted price
   (i.e., more shares)

### Pre-Money SAFE Conversion

1. **SAFE conversion price** = `valuation_cap / company_capitalization`
   - Company capitalization = all shares outstanding + option pool
     (excluding converting SAFEs for pre-money)
2. **Shares issued** = `investment_amount / conversion_price`
3. Discount comparison same as post-money

### Option Pool

The option pool (ESOP) is typically set or increased **before** conversion:

- New option pool size negotiated in the priced round term sheet
- "Option pool shuffle": investors want the pool created pre-money
  (dilutes founders, not investors)
- Standard pool sizes: 10-15% at seed, 15-20% at Series A

## Multiple SAFE Stacking

### Scenario: Two Post-Money SAFEs + Priced Round

Given:

- SAFE A: $500K at $5M cap → owns 10% ($500K / $5M)
- SAFE B: $1M at $10M cap → owns 10% ($1M / $10M)
- Series A: $3M at $15M pre-money

Result:

- SAFE A owns 10% (fixed at signing)
- SAFE B owns 10% (fixed at signing)
- Series A owns ~16.7% ($3M / $18M post-money)
- Founders + ESOP own remaining ~63.3%

### Scenario: Two Pre-Money SAFEs + Priced Round

Same amounts but with pre-money caps:

- SAFE A: $500K at $5M cap
- SAFE B: $1M at $10M cap
- Conversion prices depend on total shares at conversion time
- Both SAFEs dilute each other (ownership not fixed at signing)

## Conversion at Cap Table Level

### Step-by-Step (Post-Money SAFE)

1. **Start**: Founders hold N shares (e.g., 10,000,000)
2. **Calculate SAFE ownership**: Each post-money SAFE's % = investment / cap
3. **Set option pool**: Per term sheet (e.g., 15% post-financing)
4. **Calculate pre-round shares**:
   `total_shares = founder_shares / (1 - sum_of_SAFE_pcts - esop_pct)`
5. **Issue SAFE shares**: Each SAFE gets `total_shares * safe_pct` shares
6. **Issue ESOP shares**: `total_shares * esop_pct`
7. **Price the round**: `pre_money_valuation / total_shares = price_per_share`
8. **Issue new shares**: `round_size / price_per_share`
9. **Final cap table**: Founders + SAFE holders + ESOP + new investors

### Dilution Tracking

Key metrics to compute after each round:

- **Ownership %**: shares held / total shares outstanding
- **Dilution from round**: (pre-round % - post-round %) / pre-round %
- **Effective price**: investment amount / shares received
- **Step-up multiple**: current price / previous round price

## Common Edge Cases

### Discount + Cap

Investor gets the **better** of:

- Cap-derived price: `valuation_cap / capitalization`
- Discounted price: `round_price * (1 - discount_rate)`

The lower price per share = more shares = better for investor.

### No Cap (MFN Only)

MFN SAFE converts at the same terms as the most favorable future SAFE.
If no future SAFE is issued, MFN converts at the priced round price
(no discount unless explicitly stated).

### Pro-Rata Rights on SAFEs

Some SAFEs include a pro-rata right: the right to invest additional
capital in the next priced round to maintain ownership percentage.
Standard on post-money SAFEs with >$250K investment.

### Dissolution / Acquisition Before Priced Round

- **Post-money SAFE**: Investor gets back their investment OR their
  ownership % of proceeds (whichever is greater)
- **Pre-money SAFE**: Investor gets back their investment amount
  (no ownership calculation possible without a conversion event)
