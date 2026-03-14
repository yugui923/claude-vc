# Industry Multiples Reference

> Revenue and EBITDA multiples by sector. Used by vc-memo and
> financial_model.py for comparable valuation analysis.
> Ranges reflect private growth-stage companies (2024-2025 data).

## SaaS / Software

| Metric | Low | Median | High | Notes |
|--------|-----|--------|------|-------|
| EV/Revenue | 5x | 10x | 25x+ | High-end for >40% growth + >80% gross margins |
| EV/ARR | 6x | 12x | 30x+ | ARR preferred over total revenue for recurring |
| EV/EBITDA | 15x | 25x | 50x+ | Many growth SaaS are EBITDA-negative |

**Key drivers**: Net revenue retention (>120% = premium), Rule of 40,
gross margin (>75%), CAC payback (<18mo).

## Fintech

| Metric | Low | Median | High | Notes |
|--------|-----|--------|------|-------|
| EV/Revenue | 4x | 8x | 20x | Higher for embedded finance / payments |
| EV/EBITDA | 12x | 20x | 40x | Lending models trade lower |

**Key drivers**: Regulatory moat, take rate, net revenue (vs. gross
transaction volume), compliance track record.

## E-Commerce / Marketplace

| Metric | Low | Median | High | Notes |
|--------|-----|--------|------|-------|
| EV/GMV | 0.3x | 0.5x | 1.5x | Use take rate to convert to revenue multiple |
| EV/Revenue | 1.5x | 3x | 8x | Higher for managed marketplaces |
| EV/EBITDA | 10x | 18x | 35x | Profitability heavily rewarded |

**Key drivers**: Take rate, repeat purchase rate, supply-side lock-in,
unit economics per transaction.

## Healthcare / Biotech

| Metric | Low | Median | High | Notes |
|--------|-----|--------|------|-------|
| EV/Revenue | 3x | 8x | 20x+ | Pre-revenue biotech valued on pipeline |
| EV/EBITDA | 12x | 22x | 45x | Health IT trades closer to SaaS |

**Key drivers**: Regulatory stage (FDA phase), reimbursement model,
clinical data, patent life remaining.

## Consumer / D2C

| Metric | Low | Median | High | Notes |
|--------|-----|--------|------|-------|
| EV/Revenue | 1x | 2.5x | 6x | Brand strength and retention drive premium |
| EV/EBITDA | 8x | 15x | 30x | CPG incumbents trade 15-20x |

**Key drivers**: Brand recognition, repeat rate, customer acquisition
efficiency, gross margin (>60% for premium).

## Hardware / Deep Tech

| Metric | Low | Median | High | Notes |
|--------|-----|--------|------|-------|
| EV/Revenue | 1x | 3x | 8x | Recurring revenue components trade higher |
| EV/EBITDA | 8x | 15x | 25x | Capital intensity discounts apply |

**Key drivers**: IP/patents, recurring service revenue, gross margin,
defensibility, manufacturing scalability.

## AI / ML

| Metric | Low | Median | High | Notes |
|--------|-----|--------|------|-------|
| EV/Revenue | 8x | 18x | 50x+ | Extreme variance; infrastructure vs. application |
| EV/ARR | 10x | 25x | 80x+ | Highest for foundational model companies |

**Key drivers**: Proprietary data/models, inference costs (gross margin),
switching costs, enterprise vs. consumer, defensibility.

## Climate / Clean Tech

| Metric | Low | Median | High | Notes |
|--------|-----|--------|------|-------|
| EV/Revenue | 2x | 5x | 15x | Software-like climate = higher |
| EV/EBITDA | 10x | 20x | 35x | Hardware climate = capital-intensive discount |

**Key drivers**: Carbon credit revenue, regulatory tailwinds (IRA, EU
taxonomy), technology readiness level, offtake agreements.

## Applying Multiples

### Growth Adjustments

- **>50% YoY growth**: 20-40% premium to median
- **25-50% YoY growth**: Median range
- **<25% YoY growth**: 20-30% discount to median
- **Declining revenue**: 40-60% discount; use EBITDA multiples instead

### Stage Adjustments

- **Seed/Series A**: Use higher multiples (growth expectations priced in)
- **Series B-C**: Use median multiples
- **Late-stage/Pre-IPO**: Use public comps with 15-25% private discount

### Private Company Discount

Apply 20-30% discount to public multiples for:
- Illiquidity
- Information asymmetry
- Key person risk
- Limited governance

### When to Use Which Multiple

- **Pre-revenue**: Berkus/Scorecard methods instead (see valuation-methods.md)
- **Revenue < $1M ARR**: Revenue multiples with heavy judgment
- **$1M-$10M ARR**: EV/ARR with growth adjustment
- **$10M+ ARR**: EV/ARR or EV/Revenue with public comps
- **Profitable**: EV/EBITDA becomes primary; revenue multiple secondary
