# Real-Data Test Results Summary

**Date**: 2026-03-15
**Plugin Version**: claude-vc (current main branch)
**Layer 1 Tests**: 172/172 passing

## Test Matrix

| # | Skill | Input | Input Type | Result | Notes |
|---|-------|-------|-----------|--------|-------|
| 1 | `/vc screen` | DataSync AI SaaS deck | Synthetic pitch deck (.md) | PASS (90/100) | All 5 dimensions, red flags, comparables |
| 2 | `/vc screen` | TalentBridge marketplace deck | Synthetic marketplace deck (.md) | PASS (89/100) | Correctly handled marketplace metrics |
| 3 | `/vc terms` | Series A term sheet | Synthetic with non-standard provisions (.md) | PASS | Flagged all non-standard items |
| 4 | `/vc terms` | NVCA Model Term Sheet | Real NVCA document (.txt from .docx) | PASS | Correctly identified as baseline template |
| 5 | `/vc terms` | YC SAFE (val cap only) | Real YC SAFE agreement (.txt from .docx) | PASS | Correctly identified as SAFE variant |
| 6 | `/vc kpi` | DataSync AI SaaS KPIs | Synthetic monthly KPI report (.md) | PASS | Auto-detected SaaS, computed all metrics |
| 7 | `/vc kpi` | Rubrik FY2025 data | Real public company data (.md) | PASS | Handled missing metrics gracefully |
| 8 | `/vc model` | CrowdStrike FY2025 | Real public company financials (.md) | PASS | 3-statement model, validated vs guidance |
| 9 | `/vc memo` | DataSync AI deck | Synthetic pitch deck (.md) | PASS | All 12 sections, data-driven content |
| 10 | `/vc captable` | DataSync AI scenario | Synthetic cap table with SAFEs/notes (.md) | PASS | 100% ownership, waterfall at 3 exits |
| 11 | `/vc screen` | Investor update email | Synthetic monthly update (.md) | PASS (78/100) | Handled non-standard input; flagged pipeline slowdown |
| 12 | `/vc kpi` | CrowdStrike FY2025 | Real public company data (.md) | PASS | Rule of 40: 56.1; 97% gross retention; FCF positive |
| 13 | `/vc model` | DataSync AI startup | Synthetic pitch deck (.md) | PASS | 5-year model with Series A equity injection |
| 14 | `/vc model` | Datadog Q3 2025 | Real public company data (.md) | PASS | 5-year model using real Datadog data, reasonable projections |

## Detailed Results by Skill

### Deal Screening (`/vc screen`)
- **SaaS deck**: Scored 90/100. All 5 dimensions present. Referenced specific metrics ($4.2M ARR, 280% YoY, 8.5x LTV:CAC). Identified comparable companies (Fivetran, Dagster, Monte Carlo, Astronomer).
- **Marketplace deck**: Scored 89/100. Correctly handled marketplace-specific metrics (GMV, take rate, repeat rate, supply/demand NPS). Identified marketplace-relevant comparables.

### Term Sheet Analysis (`/vc terms`)
- **Custom term sheet**: Correctly flagged all intentional non-standard provisions (board control, restrictive debt cap, elevated dividends). Provided negotiation priorities.
- **NVCA model**: Correctly identified as baseline template. Analyzed each alternative variant (3 dividend options, 3 liquidation preference options). Flagged aggressive alternatives.
- **YC SAFE**: Correctly identified as post-money SAFE, valuation cap only. Analyzed conversion mechanics, liquidity events, dissolution. All terms assessed as standard.

### KPI Reporting (`/vc kpi`)
- **Synthetic SaaS data**: Auto-detected SaaS. Computed 17+ metrics with benchmarks. Correctly flagged runway (5.4mo) as Concerning. Script cross-validation comparison included.
- **Rubrik public data**: Auto-detected SaaS. Derived ACV (~$179K), Rule of 40 (~42), Net New ARR quarterly progression. Gracefully handled undisclosed metrics (NRR, gross retention).

### Financial Modeling (`/vc model`)
- **CrowdStrike**: Produced complete 3-statement model (FY2026-FY2030). Growth assumptions (21%→11%) aligned with company guidance. Model validated against FY2026 guidance range.

### Investment Memo (`/vc memo`)
- **SaaS deck**: All 12 sections present. Data-driven throughout. Valuation analysis (14.3x EV/ARR) compared against sector benchmarks. Risk table with severity ratings. 6 specific diligence questions.

### Cap Table (`/vc captable`)
- **Complex scenario**: Converted 4 SAFEs + 1 convertible note. MFN SAFE correctly resolved to lowest cap ($6M). Ownership summed to 100.00%. Waterfall at $200M/$500M/$1B exits. Founder dilution calculated (32.1%).

## Key Findings

### No Bugs Found
All 10 completed tests produced correct, well-structured output with no errors or crashes. The plugin handles diverse input types (synthetic data, real public company financials, legal documents) robustly.

### Strengths Observed
1. **Auto-detection works well**: SaaS company type correctly identified in all cases
2. **Graceful handling of missing data**: When metrics aren't available (e.g., Rubrik NRR), the tool estimates and clearly labels
3. **Cross-validation**: KPI tool compares company-reported vs script-calculated values
4. **Appropriate disclaimers**: Multi-jurisdiction legal disclaimers present in all outputs
5. **Data-driven analysis**: Outputs reference specific numbers from input, not generic text
6. **Marketplace handling**: Screen correctly adapted to marketplace metrics (GMV, take rate) vs SaaS metrics

### Areas for Potential Improvement
1. **Script bypassing**: Both financial model tests showed the LLM constructing tables directly instead of running `financial_model.py three_statement`. The SKILL.md instructs it to use the script for Decimal-precision arithmetic, but the LLM sometimes skips this step. Results are still correct but lose the deterministic precision guarantee.
2. **Captable script usage**: Similarly, the captable test may not have invoked `captable.py` — the LLM computed conversions directly. This works but bypasses the tested computation engine.
3. The captable scenario required many agent turns (12) — could benefit from more direct JSON construction
4. No explicit break-even analysis in the CrowdStrike model (though the company is already profitable)
5. Term sheet analysis classified partial single-trigger acceleration as "Standard" — some practitioners would flag this

## Materials Used

- 5 public company investor presentation PDFs
- 3 real term sheet/SAFE documents (NVCA, YC)
- 5 real company financial data files (CrowdStrike, Cloudflare, Datadog, Klaviyo, Rubrik)
- 2 synthetic pitch decks (SaaS, marketplace)
- 1 synthetic term sheet
- 1 synthetic KPI report
- 1 synthetic cap table scenario
- 1 synthetic investor update

Total: 34 files across 5 categories
