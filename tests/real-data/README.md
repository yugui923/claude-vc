# Real-World Test Data for Claude-VC Plugin

This directory contains publicly available materials for end-to-end testing of
the claude-vc plugin against realistic inputs. All materials are either
publicly available documents, derived from public company filings, or
synthetic scenarios built on realistic data.

## Directory Structure

```
real-data/
├── pitch-decks/              # Startup pitch decks (PDF and text)
├── investor-presentations/   # Public company quarterly earnings PDFs
├── term-sheets/              # Term sheet templates and examples
├── safe-agreements/          # Y Combinator SAFE agreement templates
├── financial-reports/        # Financial data, KPI reports, investor updates
└── test-results/             # Output from headless plugin tests
```

## Materials Inventory

### Pitch Decks (`pitch-decks/`)

| File | Description | Source | Tests |
|------|-------------|--------|-------|
| `sample-saas-startup-deck.md` | DataSync AI Series A deck (synthetic) | Created from realistic SaaS metrics | screen, memo, model |
| `sample-marketplace-startup-deck.md` | TalentBridge Series A deck (synthetic) | Created from realistic marketplace metrics | screen |
| `airbnb-seed-deck.pdf` | Airbnb original 2009 pitch deck | NC State University (public) | screen |
| `airbnb-pitch-deck-v2.pdf` | Airbnb pitch deck (alternate version) | BlueLion (public) | screen |
| `sequoia-pitch-deck-template.pdf` | Sequoia Capital pitch deck framework | UVic Gustavson (public) | reference |

### Investor Presentations (`investor-presentations/`)

| File | Description | Source |
|------|-------------|--------|
| `palantir-q4-2025.pdf` | Palantir Q4 2025 Investor Presentation | investors.palantir.com |
| `snowflake-q4-fy2025.pdf` | Snowflake Q4 FY2025 Investor Presentation | s26.q4cdn.com |
| `cloudflare-q3-2025.pdf` | Cloudflare Q3 2025 Investor Presentation | cloudflare IR |
| `crowdstrike-q4-fy2025.pdf` | CrowdStrike Q4 FY2025 Earnings Presentation | ir.crowdstrike.com |
| `datadog-feb2026.pdf` | Datadog February 2026 Investor Presentation | investors.datadoghq.com |
| `klaviyo-q2-2025.pdf` | Klaviyo Q2 2025 Investor Presentation | s203.q4cdn.com |
| `rubrik-q3-fy2025.pdf` | Rubrik Q3 FY2025 Investor Presentation | s203.q4cdn.com |
| `onestream-q2-2024.pdf` | OneStream Q2 2024 Earnings Presentation | investor.onestream.com |

### Term Sheets (`term-sheets/`)

| File | Description | Source | Tests |
|------|-------------|--------|-------|
| `sample-series-a-term-sheet.md` | DataSync AI Series A (synthetic, with intentional non-standard provisions) | Created | terms |
| `nvca-model-term-sheet-2020.docx` | NVCA Model Term Sheet v2020 | nvca.org | terms |
| `nvca-model-term-sheet-2020.txt` | Converted text version | Converted from DOCX | terms |
| `mit-vc-term-sheet-example.pdf` | MIT OCW VC term sheet example | ocw.mit.edu | reference |
| `klgates-term-sheet-anatomy.pdf` | K&L Gates term sheet anatomy guide | klgates.com | reference |
| `fenwick-convertible-note-template.pdf` | Fenwick seed convertible note | fenwick.com | reference |

### SAFE Agreements (`safe-agreements/`)

| File | Description | Source | Tests |
|------|-------------|--------|-------|
| `yc-safe-valuation-cap-only.docx` | YC Post-Money SAFE (val cap, no discount) | ycombinator.com | terms |
| `yc-safe-valuation-cap-only.txt` | Converted text version | Converted from DOCX | terms |
| `yc-safe-discount-only.docx` | YC Post-Money SAFE (discount, no cap) | ycombinator.com | reference |
| `yc-safe-discount-only.txt` | Converted text version | Converted from DOCX | reference |
| `yc-safe-valuation-cap-discount.pdf` | YC SAFE with both cap and discount | docdrop.org | reference |

### Financial Reports (`financial-reports/`)

| File | Description | Source | Tests |
|------|-------------|--------|-------|
| `crowdstrike-fy2025-financials.md` | CrowdStrike FY2025 full financial data | Official press release | model, kpi |
| `cloudflare-q3-2025-financials.md` | Cloudflare Q3 2025 financial data | Official press release | model, kpi |
| `datadog-q3-2025-financials.md` | Datadog Q3 2025 financial data | Official press release | model, kpi |
| `klaviyo-q3-2025-financials.md` | Klaviyo Q3 2025 financial data | Official press release | kpi |
| `rubrik-fy2025-financials.md` | Rubrik FY2025 financial data | Official press release | kpi |
| `synthetic-datasync-ai-monthly-kpi.md` | DataSync AI monthly KPI report (synthetic) | Created | kpi |
| `rubrik-fy2025-kpi-data.md` | Rubrik KPI data formatted for testing | Derived from public data | kpi |
| `synthetic-datasync-ai-captable-scenario.md` | DataSync AI cap table scenario (synthetic) | Created | captable |
| `synthetic-datasync-ai-investor-update.md` | DataSync AI monthly investor update (synthetic) | Created | screen |
| `synthetic-payloop-seed-kpi.md/.docx/.pdf` | PayLoop fintech KPI report — negative unit economics, FX exposure, high churn | Created | kpi |
| `synthetic-medscribe-ai-quarterly-financials.md/.docx/.pdf` | MedScribe AI healthtech quarterly — lumpy deferred revenue, FDA costs, negative working capital | Created | model, kpi |
| `synthetic-greengrid-annual-financials.md/.docx/.pdf` | GreenGrid carbon marketplace annual — extreme Q4 seasonality, take rate erosion | Created | model, kpi |
| `synthetic-skillforge-monthly-investor-update.md/.docx/.pdf` | SkillForge edtech investor update — completion-driven churn, viral TikTok CAC | Created | screen, kpi |
| `synthetic-vaultsync-captable-scenario.md/.docx/.pdf` | VaultSync complex cap table — unequal splits, departed founder, 4 SAFEs at different caps, convertible note | Created | captable |
| `synthetic-farmos-seasonal-kpi.md/.docx/.pdf` | FarmOS agtech seasonal KPI — extreme seasonality, hardware+software mix, low NRR | Created | kpi |

## Test Results (`test-results/`)

Test results from headless plugin invocations using `claude -p`.

## Running Tests

```bash
# Screen a pitch deck
claude -p --max-turns 6 --max-budget-usd 2.00 \
  --dangerously-skip-permissions --output-format text \
  "Run /vc screen tests/real-data/pitch-decks/sample-saas-startup-deck.md"

# Analyze a term sheet
claude -p --max-turns 6 --max-budget-usd 2.00 \
  --dangerously-skip-permissions --output-format text \
  "Run /vc terms tests/real-data/term-sheets/sample-series-a-term-sheet.md"

# Generate KPI report
claude -p --max-turns 8 --max-budget-usd 2.00 \
  --dangerously-skip-permissions --output-format text \
  "Run /vc kpi tests/real-data/financial-reports/synthetic-datasync-ai-monthly-kpi.md"

# Build financial model
claude -p --max-turns 10 --max-budget-usd 2.00 \
  --dangerously-skip-permissions --output-format text \
  "Run /vc model tests/real-data/financial-reports/crowdstrike-fy2025-financials.md"

# Generate investment memo
claude -p --max-turns 8 --max-budget-usd 2.00 \
  --dangerously-skip-permissions --output-format text \
  "Run /vc memo tests/real-data/pitch-decks/sample-saas-startup-deck.md"

# Cap table with scenario
claude -p --max-turns 12 --max-budget-usd 3.00 \
  --dangerously-skip-permissions --output-format text \
  "Run /vc captable. Read tests/real-data/financial-reports/synthetic-datasync-ai-captable-scenario.md"
```

## Data Sources

All data in this directory comes from publicly available sources:
- **SEC EDGAR**: 10-K, 10-Q, 8-K filings and earnings press releases
- **Investor Relations**: Official company investor presentations
- **Y Combinator**: Open-source SAFE agreement templates
- **NVCA**: Model legal documents
- **Academic**: MIT OCW course materials
- **Law firms**: Public term sheet templates (K&L Gates, Fenwick)

Synthetic data (synthetic-*) is created from realistic metrics based on
publicly available industry benchmarks. Each synthetic file is available
in .md, .docx, and .pdf formats (generated via `_generate_docs.py`).
