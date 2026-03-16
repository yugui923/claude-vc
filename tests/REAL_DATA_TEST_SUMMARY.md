# Real-Data Test Summary — claude-vc v1.3.0

**Date**: 2026-03-16
**Plugin Version**: 1.3.0
**CLI Version**: Claude Code 2.1.76
**Layer 1 (unit/integration)**: 172/172 passing

---

## 1. Test Execution: 18 Headless Runs, 18 Passed

Each of the 6 skill modules was tested 3 times with different inputs
covering diverse company types, stages, and edge cases.

| Module | Run 1 | Run 2 | Run 3 |
|--------|-------|-------|-------|
| `/vc screen` | NovaByte DevTools (81/100) | Carto zero-revenue (72/100) | FarmOS AgTech (83/100) |
| `/vc terms` | NovaByte aggressive investor | PayLoop founder-friendly | GreenGrid impact investor |
| `/vc kpi` | PayLoop fintech | FarmOS seasonal AgTech | Datadog real $3.4B |
| `/vc model` | MedScribe healthtech | Cloudflare real $2.2B | GreenGrid marketplace |
| `/vc memo` | PayLoop fintech seed | MedScribe Series B | GreenGrid climate |
| `/vc captable` | VaultSync departed founder | DataSync SAFEs+notes | Inline text data |

### Input Diversity

- **Company types**: DevTools, Consumer Social, AgTech, Fintech, Healthtech,
  Climate/Marketplace, Cybersecurity, SaaS
- **Stages**: Pre-Seed, Seed, Series A, Series B
- **Revenue**: $0 to $3.4B (real Datadog data)
- **Edge cases**: Zero revenue, 45% customer concentration, 6% monthly churn,
  extreme seasonality, departed founder (pre-cliff), FDA pending, regulatory
  gray area, hardware+software margin mix

---

## 2. Fact-Check Results: Input vs Output Verification

Six fact-checking agents exhaustively compared every number, name, percentage,
and factual claim in each test output against its input data.

### Summary by Module

| Module | Claims Checked | Correct | Hallucinations | Inferences | Rate |
|--------|---------------|---------|----------------|------------|------|
| **screen** (3 runs) | ~110 | ~104 | 0 | ~6 (comps) | **0% hallucination** |
| **terms** (3 runs) | ~120 | ~116 | 0 | ~4 | **0% hallucination** |
| **kpi** (3 runs) | 97 | 95 | 1 | ~2 (computed) | **~1% hallucination** |
| **model** (3 runs) | ~60 | ~56 | 1 | ~3 | **~1.7% hallucination** |
| **memo** (3 runs) | 224 | 216 | 3 | 5 | **~1.3% hallucination** |
| **captable** (3 runs) | ~50 | ~45 | 0 | ~5 (math) | **0% hallucination** |
| **TOTAL** | **~600** | **~570** | **5** | **~25** | **~0.8% hallucination** |

### Hallucinations Found (5 total across ~600 claims)

**1. `/vc model` Run 2 (Cloudflare): Fabricated debt figure**
- Output claims "$1,300M convertible notes" as debt
- This is factually true about Cloudflare in reality, but the number does NOT
  appear in the input data file
- Not labeled as external research or estimate
- **Severity**: Low (real-world accurate but not sourced from input)

**2-3. `/vc memo` Run 1 (PayLoop): Competitor financials**
- Output states "Deel $12B+ valuation, $500M+ ARR" and "Remote $3B valuation"
  in the competitive landscape section
- These are plausible real-world figures but NOT in the pitch deck input
- Not explicitly labeled as external research
- **Severity**: Low (competitive section where external research is expected)

**4. `/vc kpi` Run 2 (FarmOS): Fabricated Magic Number**
- Output reports Magic Number of 0.66
- Magic Number requires S&M spend data, which is NOT in the FarmOS input
- The input gives headcount and total operating expenses but never breaks
  out sales & marketing as a dollar figure
- **Severity**: Medium (metric cannot be derived from provided data, but
  is presented without caveat)

**5. `/vc memo` Run 3 (GreenGrid): Competitor scandal claim**
- Output states South Pole suffered "reputational damage from 2023 scandals"
- The deck lists South Pole only in the competition table; no mention of
  scandals or reputational damage
- External knowledge injected without labeling
- **Severity**: Low (in competitive analysis section, factually accurate)

### Issues Found (non-hallucination)

**1. Model CapEx derivation mismatch (Cloudflare)**
- Output claims CapEx is "12% of revenue, derived from Q3 OCF-FCF"
- Actual Q3 derivation yields ~17%, not 12%
- The 12% figure is reasonable but the stated derivation is incorrect
- **Type**: Misleading sourcing (not a hallucination — the assumption is
  reasonable, but the claimed derivation doesn't match)

**2. Terms internal math inconsistency (NovaByte)**
- Output gives two different figures for the 5-year redemption amount
  ($25.6M in one section, ~$23.6M in another)
- The ~$23.6M figure is correct (8% compounding on $12M for 5 years)
- **Type**: Internal inconsistency (not a hallucination from input)

**3. Captable SAFE conversion prices vary (VaultSync)**
- Three SAFEs with the same effective $10M cap show slightly different
  conversion prices ($0.8818, $0.8525, $0.8440)
- This may reflect iterative post-money SAFE math where each SAFE's
  denominator accounts for dilution from other SAFEs
- **Type**: Mathematical methodology question (not clearly wrong, but
  not explained)

**4. Captable exit scenarios (VaultSync)**
- Input requested waterfall at $100M/$250M/$500M/$1B
- Output provided $100M/$300M/$500M (swapped $250M for $300M, dropped $1B)
- The user's prompt overrode the file's request (asked for $100M/$300M/$500M)
- **Type**: Prompt-following vs file-following conflict

**5. Captable discount price systematic bug**
- In ALL 3 captable runs, the discount-derived conversion price is wrong
- Run 1: stated $4.73, should be ~$4.27
- Run 2: stated $4.49, should be ~$3.81
- Run 3: stated $1.74, should be ~$1.59
- In all cases the cap price wins so the final conversion is unaffected
- **Type**: Systematic math error — would produce incorrect results if a
  scenario arose where the discount price should be the better deal
- **Severity**: Medium (masked by cap winning in all test cases)

**6. Model growth rate inconsistency (GreenGrid)**
- Output says growth is "decelerating from 64% YoY" but uses 70% for
  Year 1 — which is an acceleration, not deceleration
- The narrative contradicts the actual assumption used
- **Type**: Internal inconsistency between text and numbers

### Math Verification Results

The fact-checkers verified arithmetic in the financial model and KPI outputs:

**Financial Model math** (spot-checked 15+ calculations per run):
- Revenue projections: All correct (growth rate × prior year)
- Gross Profit = Revenue × Gross Margin: Correct across all years
- EBITDA = Gross Profit - OpEx: Correct (±$0.1M rounding)
- Net Income = EBITDA - D&A: Correct
- Cash flow chain (ending cash = prior + net change): Correct

**KPI computed metrics** (verified derivations):
- Rule of 40 = growth% + margin%: Correct (PayLoop 130, FarmOS 29, Datadog 52.2)
- Burn Multiple = net burn / net new ARR: Correct (PayLoop 7.1x, FarmOS 1.02x)
- LTV/CAC: Correct where input provided (PayLoop 2.26x)
- NRR annualization: Correct (PayLoop monthly 93.6% → annual ~45%)

**Cap table ownership**: All 3 runs sum to exactly **100.00%**

---

## 3. Module-Specific Findings

### `/vc screen` — Excellent
- Zero hallucinations across 3 runs (~110 claims checked)
- Correctly adapted scoring to company type (DevTools vs Consumer vs AgTech)
- Identified all planted edge cases (45% concentration, missing VP Sales,
  zero revenue, hardware margins, seasonality)
- Comparable companies are external research (appropriately in a dedicated
  section), not hallucinated data claims

### `/vc terms` — Excellent
- Zero hallucinations across 3 runs (~120 claims checked)
- Every dollar amount, percentage, provision, and investor name verified
- Correctly classified aggressive vs founder-friendly vs impact terms
- One minor internal math inconsistency (redemption calculation)

### `/vc kpi` — Good (1 fabrication)
- One fabricated metric: FarmOS Magic Number (0.66) cannot be derived from
  the input data (no S&M spend breakdown provided). Presented without caveat
- All other 96 computed metrics mathematically verified across 3 runs
- Auto-detection worked for Fintech, AgTech (SaaS + IoT Hardware), and SaaS
- Correctly handled billion-dollar scale (Datadog) and extreme seasonality
  (FarmOS)
- Caught a data inconsistency in the FarmOS input (operating income vs
  quarterly sum mismatch) — a sign of analytical rigor

### `/vc model` — Good (1 minor hallucination)
- One fabricated data point: Cloudflare $1,300M debt (real-world true but
  not in input file)
- One misleading derivation claim (CapEx 12% "derived from Q3" doesn't match
  the actual Q3 math)
- All financial statement math verified correct
- Revenue projections, margin progression, and cash flow chains all
  internally consistent

### `/vc memo` — Good (3 minor hallucinations)
- Three external facts injected without labeling: Deel valuation ($12B+),
  Remote valuation ($3B), South Pole "2023 scandals"
- All appeared in Competitive Landscape sections where external research
  is standard, but were not labeled as external
- All company-specific data points (revenue, team, product, market size)
  verified correct against input decks — zero hallucinations in data extraction
- Every person name and background checked across all 3 runs — all matched
- 224 total claims checked; 216 correct from input (96.4%)

### `/vc captable` — Good (systematic discount price bug)
- Zero hallucinations — all investor names, amounts, and terms verified
- Ownership invariant holds: all 3 runs = 100.00%
- Waterfall payouts verified consistent with ownership percentages
- **Bug found**: Discount-derived conversion prices are systematically
  miscalculated in all 3 runs. In every case the cap price wins so results
  are correct, but the bug would produce wrong conversions if discount
  > cap. This is the most actionable finding from the fact-check
- Post-money SAFE conversion math uses iterative methodology; prices are
  plausible but the exact formula is not shown in output

---

## 4. Overall Assessment

| Metric | Value |
|--------|-------|
| Tests run | 18 |
| Tests passed | 18 (100%) |
| Total claims fact-checked | ~600 |
| Hallucination rate | ~0.8% (5/~600) |
| Hallucination severity | 4 Low, 1 Medium (KPI fabricated metric) |
| Math errors | 1 systematic (captable discount price) |
| Cap table ownership invariant | 100.00% (all 3 runs) |
| Disclaimers present | 18/18 (100%) |
| Auto-detection accuracy | 6/6 company types correct |

### Verdict

The plugin produces highly accurate, data-grounded outputs. The 0.8%
hallucination rate is low and all instances fall into two categories:
(1) external knowledge injected in analytical sections without labeling
(4 of 5), and (2) a fabricated metric where input data was insufficient
(1 of 5). Zero hallucinations were found in core data extraction —
every number, name, and percentage pulled from input files was verified
correct across all 18 runs.

The most actionable finding is the **systematic discount price bug** in
captable: discount-derived conversion prices are wrong in all 3 runs.
Currently masked because the cap always wins, but this would produce
incorrect conversions in scenarios where discount > cap.

### Recommendations

1. **Fix captable discount price calculation**: The discount price is
   systematically miscalculated (e.g., $4.73 instead of $4.27). This is
   a real bug that would affect results if cap and discount were close
2. **Label external knowledge**: When the model adds real-world data not
   from the input (competitor valuations, debt figures, competitor scandals),
   it should explicitly note "based on public information, not from the
   provided document"
3. **Don't fabricate metrics when data is insufficient**: The KPI skill
   should skip metrics it cannot compute (like Magic Number without S&M
   data) rather than generating a plausible-looking number
4. **Verify derivation claims**: When stating "derived from X", verify the
   math matches (the CapEx 12% "derived from Q3" actually yields 17%)
5. **SAFE conversion transparency**: Show the formula used for post-money
   SAFE conversion to make the math auditable
6. **Consistent exit scenarios**: When both a file and prompt specify
   exit values, clarify which takes precedence
