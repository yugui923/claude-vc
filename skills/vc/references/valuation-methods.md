# Valuation Methods

## Method Selection by Stage

| Stage               | Primary Methods                         | Secondary Methods                         |
| ------------------- | --------------------------------------- | ----------------------------------------- |
| Pre-seed / Idea     | Berkus, Scorecard                       | Risk Factor Summation                     |
| Seed (pre-revenue)  | Scorecard, VC Method                    | Berkus, Comparable Transactions           |
| Seed (with revenue) | VC Method, Comparable Transactions      | Revenue Multiples                         |
| Series A            | Revenue Multiples, VC Method            | Comparable Companies, DCF (if profitable) |
| Series B+           | Revenue Multiples, Comparable Companies | DCF, Precedent Transactions               |
| Growth / Pre-IPO    | DCF, Comparable Companies               | Precedent Transactions, LBO               |

## Discounted Cash Flow (DCF)

Best for: companies with predictable cash flows (Series B+, profitable companies).

1. Project free cash flows for 5-10 years
2. Calculate terminal value (typically Gordon Growth or exit multiple)
3. Discount to present value using appropriate discount rate

**Discount rates by stage**:

| Stage            | Typical Discount Rate |
| ---------------- | --------------------- |
| Seed             | 50-70%                |
| Series A         | 40-60%                |
| Series B         | 30-50%                |
| Series C+        | 20-35%                |
| Growth / Pre-IPO | 15-25%                |
| Public company   | 8-15% (WACC)          |

**Terminal value**: typically 60-80% of total DCF value. Use exit multiples (EV/Revenue or EV/EBITDA) from comparable public companies applied to terminal year financials.

## Comparable Company Analysis

Best for: companies with revenue and identifiable public/private peers.

1. Identify 5-10 comparable companies (similar sector, stage, growth rate, geography)
2. Calculate relevant multiples (EV/Revenue, EV/EBITDA, P/E)
3. Apply median or mean multiple to the target company's metrics
4. Adjust for differences in growth rate, profitability, scale

**Common adjustments**:

- Growth premium: companies growing >50% faster than median comp warrant 20-40% premium
- Profitability discount: unprofitable companies typically trade at 20-30% discount to profitable peers
- Scale discount: smaller companies warrant 15-25% illiquidity/scale discount
- Private company discount: 20-30% discount vs. public comparables for lack of liquidity

## Precedent Transactions

Best for: when recent M&A or funding rounds exist for comparable companies.

1. Identify recent transactions (last 2-3 years) in the same sector and stage
2. Calculate implied multiples (EV/Revenue, EV/EBITDA)
3. Apply to target company metrics
4. Adjust for market conditions (transactions in bull markets carry premium)

**Control premium**: M&A transactions typically include a 20-40% control premium over public trading multiples. Subtract this when using M&A precedents for minority investment valuation.

## VC Method

Best for: early-stage companies where an exit can be estimated.

1. Estimate exit value at target horizon (typically 5-7 years)
2. Estimate exit revenue and apply appropriate exit multiple
3. Divide by target return multiple to get post-money valuation today

**Target return multiples by stage**:

| Stage    | Target Return | Implied at 5yr exit                |
| -------- | ------------- | ---------------------------------- |
| Seed     | 20-30x        | ~100x revenue multiple tolerance   |
| Series A | 10-15x        | ~30-50x revenue multiple tolerance |
| Series B | 5-8x          | ~15-25x revenue multiple tolerance |
| Series C | 3-5x          | ~8-15x revenue multiple tolerance  |

**Formula**: Post-money today = Exit value / Target return multiple

## Berkus Method

Best for: pre-revenue startups. Assigns value to 5 risk factors.

| Factor                      | Max Value |
| --------------------------- | --------- |
| Sound idea (basic value)    | $500K     |
| Prototype (technology risk) | $500K     |
| Quality management team     | $500K     |
| Strategic relationships     | $500K     |
| Product rollout or sales    | $500K     |

**Total pre-money valuation**: sum of applicable factors, max $2.5M. Originally designed for angel-stage companies. Adjust maximums upward for later stages or hot markets.

## Scorecard Method

Best for: pre-revenue startups, benchmarked against regional averages.

1. Determine average pre-money valuation for comparable deals in the region/sector
2. Score the company vs. average across weighted factors:

| Factor                         | Weight |
| ------------------------------ | ------ |
| Strength of management         | 30%    |
| Size of opportunity            | 25%    |
| Product/technology             | 15%    |
| Competitive environment        | 10%    |
| Marketing/sales channels       | 10%    |
| Need for additional investment | 5%     |
| Other factors                  | 5%     |

3. Multiply regional average valuation by the weighted score to get adjusted pre-money

## First Chicago Method

Best for: multi-scenario analysis across outcomes.

1. Build three scenarios: Bull (success), Base (moderate), Bear (failure/pivot)
2. Assign probability to each scenario (e.g., 25% / 50% / 25%)
3. Value the company under each scenario using appropriate methods
4. Calculate probability-weighted average valuation

This method is useful for presenting a valuation range rather than a single point estimate. Show the investor the upside case, the base case, and the downside risk.

## Output Guidelines

When presenting valuations:

- Always state the method(s) used and key assumptions
- Present a range, not a single number
- Note sensitivity to key assumptions (growth rate, discount rate, exit multiple)
- Compare across multiple methods when possible
- Flag when limited data makes any method unreliable
- Append the enhanced disclaimer from `references/disclaimers.md`
