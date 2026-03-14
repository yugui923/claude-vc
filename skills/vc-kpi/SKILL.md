---
name: vc-kpi
description: >
  Generate KPI reports from company data. Auto-detects company type
  (SaaS, marketplace, consumer, fintech) and calculates relevant
  metrics with industry benchmarks. Use when user says "KPIs",
  "metrics", "SaaS metrics", "unit economics report", "burn multiple",
  "magic number", "Rule of 40", or "KPI dashboard".
---

# KPI Reporting

Generate structured KPI reports from company-provided data. Auto-detects
the business model type and computes the most relevant metrics with
benchmark comparisons and health assessments.

## Input Handling

1. **Structured data** (JSON or CSV): Parse directly into metrics.
2. **Verbal description**: Extract metrics from natural language.
3. **File path**: Read the file (investor update, financial report).
4. **After a screening or memo**: Use metrics already in context.
5. **No input**: Ask for the company type and key metrics.

### Auto-Detection

Determine the company type from the data provided:

- **SaaS**: ARR/MRR, churn, NRR, subscriptions mentioned
- **Marketplace**: GMV, take rate, supply/demand mentioned
- **Consumer**: DAU/MAU, retention, sessions mentioned
- **Fintech**: NIM, NPL, interchange, loan volume mentioned
- **General**: Default if type unclear; ask user to confirm

## KPI Computation

### SaaS KPIs

For SaaS companies, build a JSON scenario and run:

```bash
python3 "${CLAUDE_SKILL_DIR}/../vc/scripts/financial_model.py" unit_economics --input <temp.json>
```

Present script output plus these additional KPIs (computed by Claude):

| Metric | How to Compute | Benchmark |
|--------|---------------|-----------|
| ARR | MRR x 12 | Stage-dependent |
| MRR Growth | (MRR_now - MRR_prior) / MRR_prior | >10% m/m (seed), >5% (A) |
| Net Revenue Retention | (from script output) | >120% excellent, >100% good |
| Gross Churn | Lost MRR / Starting MRR | <2% monthly, <5% acceptable |
| CAC | (from script output) | Varies by ACV |
| LTV | (from script output) | Minimum 3x CAC |
| CAC Payback | (from script output) | <12mo good, <18mo acceptable |
| Magic Number | (from script output) | >0.75 efficient |
| Burn Multiple | Net burn / Net new ARR | <1x excellent, <2x good |
| Rule of 40 | Revenue growth % + FCF margin % | >40 healthy |
| Gross Margin | (Revenue - COGS) / Revenue | >75% SaaS standard |
| Revenue per Employee | ARR / headcount | >$100K seed, >$200K A |

### Marketplace KPIs

Compute directly (no script needed):

| Metric | How to Compute | Benchmark |
|--------|---------------|-----------|
| GMV | Total transaction volume | Stage-dependent |
| GMV Growth | (GMV_now - GMV_prior) / GMV_prior | >20% m/m early |
| Take Rate | Revenue / GMV | 5-30% varies by category |
| Liquidity | Completed / Listed transactions | >30% healthy |
| Supply Growth | New sellers or listings | Balanced with demand |
| Demand Growth | New buyers or orders | Balanced with supply |
| Contribution Margin | (Revenue - variable costs) / transaction | Positive at scale |
| Repeat Rate | Repeat buyers / total buyers | >30% good |

### Consumer KPIs

Compute directly:

| Metric | How to Compute | Benchmark |
|--------|---------------|-----------|
| DAU / MAU | Daily and monthly active users | Stage-dependent |
| DAU/MAU Ratio | Stickiness metric | >25% good, >50% great |
| D1 Retention | Users returning day 1 | >40% good |
| D7 Retention | Users returning day 7 | >20% good |
| D30 Retention | Users returning day 30 | >10% good |
| Session Frequency | Sessions per user per day | Category-dependent |
| ARPU | Revenue / active users | Category-dependent |
| Viral Coefficient | Invites sent x conversion rate | >1 viral growth |

### Fintech KPIs

Compute directly:

| Metric | How to Compute | Benchmark |
|--------|---------------|-----------|
| NIM | (Interest earned - Interest paid) / assets | >3% for lending |
| NPL Ratio | Non-performing loans / total loans | <5% healthy |
| CAC Payback | CAC / monthly profit per customer | <12mo |
| Take Rate | Revenue / transaction volume | Varies by product |
| Regulatory Capital | Capital / risk-weighted assets | Above minimums |

### General KPIs (Always Included)

| Metric | How to Compute | Benchmark |
|--------|---------------|-----------|
| Revenue | Monthly or annual | Stage-dependent |
| Revenue Growth | YoY or MoM | Stage-dependent |
| Burn Rate | Monthly net cash outflow | Relative to revenue |
| Runway | Cash / monthly burn | >12 months |
| Headcount | Total employees | Context-dependent |

## Benchmarking

Read `${CLAUDE_SKILL_DIR}/../vc/references/industry-multiples.md` for
sector benchmarks. Compare each metric against the benchmark range.

### Health Assessment

Assign each metric a status:

- **Healthy**: At or above benchmark range
- **Watch**: Below benchmark but within acceptable range
- **Concerning**: Significantly below benchmark or trending poorly

## Output Format

```markdown
# KPI Report: [Company Name]

**Company Type**: SaaS | Marketplace | Consumer | Fintech
**Reporting Period**: [date range or point-in-time]
**Data Source**: [user-provided / pitch deck / investor update]

## Key Metrics Summary

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| ... | ... | ... | Healthy / Watch / Concerning |

## Detailed Analysis

### Growth Metrics
[metrics with trend analysis]

### Unit Economics
[metrics with assessment]

### Efficiency Metrics
[metrics with assessment]

## Flags

### Healthy
- [metrics that look good, brief explanation]

### Concerning
- [metrics that need attention, brief explanation]

## Recommendation
[brief synthesis of KPI health and areas to monitor]
```

## Disclaimer

Read `${CLAUDE_SKILL_DIR}/../vc/references/disclaimers.md` and append
the **enhanced disclaimer** (contains financial figures).
