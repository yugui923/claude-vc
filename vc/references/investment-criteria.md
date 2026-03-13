# Investment Criteria & Scoring Framework

## Deal Score (0-100)

The Deal Score is a weighted composite across 5 dimensions. Each dimension is scored 0-20, then weighted to produce a total out of 100.

| Dimension                   | Weight | Max Points |
| --------------------------- | ------ | ---------- |
| Market Opportunity          | 25%    | 25         |
| Team & Execution            | 25%    | 25         |
| Product & Technology        | 20%    | 20         |
| Financials & Business Model | 20%    | 20         |
| Timing & Momentum           | 10%    | 10         |

## Dimension Rubrics

### Market Opportunity (0-25)

| Score | Criteria                                                        |
| ----- | --------------------------------------------------------------- |
| 21-25 | TAM >$10B, growing >20%/yr, clear wedge, regulatory tailwinds   |
| 16-20 | TAM $1-10B, growing >10%/yr, identifiable wedge                 |
| 11-15 | TAM $500M-1B, moderate growth, some differentiation possible    |
| 6-10  | TAM <$500M or stagnant market, crowded space                    |
| 0-5   | Shrinking market, heavy regulation blocking entry, unclear need |

### Team & Execution (0-25)

| Score | Criteria                                                                                   |
| ----- | ------------------------------------------------------------------------------------------ |
| 21-25 | Repeat founders with relevant exits, complete team, deep domain expertise, strong advisors |
| 16-20 | Experienced operators, most key roles filled, relevant industry background                 |
| 11-15 | First-time founders with strong backgrounds, some gaps in team                             |
| 6-10  | Inexperienced team, significant skill gaps, no domain expertise                            |
| 0-5   | Solo founder with no relevant experience, no advisory support                              |

### Product & Technology (0-20)

| Score | Criteria                                                                                   |
| ----- | ------------------------------------------------------------------------------------------ |
| 17-20 | Live product with traction, defensible technology, strong moat (IP, network effects, data) |
| 13-16 | Working product, early traction, some technical differentiation                            |
| 9-12  | MVP or beta, limited traction, technology not clearly differentiated                       |
| 5-8   | Pre-product or prototype only, no clear technical advantage                                |
| 0-4   | Idea stage, no technical feasibility demonstrated                                          |

### Financials & Business Model (0-20)

| Score | Criteria                                                                      |
| ----- | ----------------------------------------------------------------------------- |
| 17-20 | Proven unit economics (LTV:CAC >3x), >$1M ARR, clear path to profitability    |
| 13-16 | Early revenue, positive unit economics trend, viable business model           |
| 9-12  | Pre-revenue with credible monetization plan, comparable business models exist |
| 5-8   | Pre-revenue, unclear monetization, unproven business model                    |
| 0-4   | No revenue model, unsustainable economics, unrealistic projections            |

### Timing & Momentum (0-10)

| Score | Criteria                                                                 |
| ----- | ------------------------------------------------------------------------ |
| 9-10  | Category-defining moment, strong recent traction, favorable macro trends |
| 7-8   | Good timing, market is ready, some momentum indicators                   |
| 5-6   | Neutral timing, market exists but not accelerating                       |
| 3-4   | Possibly too early or too late, uncertain market readiness               |
| 0-2   | Bad timing, market headwinds, declining interest                         |

## Recommendation Thresholds

| Deal Score | Recommendation    | Action                                              |
| ---------- | ----------------- | --------------------------------------------------- |
| 80-100     | Strong Interest   | Proceed to full due diligence immediately           |
| 60-79      | Further Diligence | Worth deeper investigation, address key concerns    |
| 40-59      | Cautious          | Significant concerns, only proceed if strategic fit |
| 0-39       | Pass              | Does not meet investment criteria                   |

## Red Flags (Automatic Concerns)

These issues should always be flagged regardless of overall score:

- Solo non-technical founder building a technology product
- No clear revenue model after 2+ years of operation
- Founder team has no relevant industry experience
- Key IP is not owned by the company
- Abnormally high burn rate relative to traction
- Previous failed fundraises without clear explanation
- Customer concentration >50% in a single account
- Regulatory risk with no compliance strategy
- Cap table issues (excessive early dilution, complex structures)
- No reference customers willing to speak

## Customization

Users can override these weights and thresholds by providing a custom criteria file with `--criteria <file>`. The custom file should follow the same structure but with adjusted weights, score ranges, or additional red flags specific to the user's investment thesis.
