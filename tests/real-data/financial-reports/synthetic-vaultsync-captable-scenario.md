# VaultSync — Cap Table Scenario for Series A
## Company Type: Enterprise Security (Secrets Management / Vault Orchestration)
## Date: March 2026

### Background
VaultSync was founded in June 2023 by three co-founders with unequal equity splits.
The company raised pre-seed via SAFEs from multiple investors at different caps, took
a convertible note bridge, and is now negotiating a $15M Series A at $65M pre-money.

One co-founder departed after 8 months, creating a partial vesting situation.

### Founders — Common Stock

**Active Founders:**
- Alex Rivera (CEO): 5,000,000 shares (50% of founder pool)
  - 4-year vest, 1-year cliff, monthly thereafter
  - Fully vested (started June 2023, cliff passed, 33 months elapsed)
- Jordan Osei (CTO): 3,000,000 shares (30% of founder pool)
  - 4-year vest, 1-year cliff, monthly thereafter
  - Fully vested through month 33 of 48
  - Vested shares: 2,062,500 (33/48 x 3,000,000)
  - Unvested shares: 937,500

**Departed Founder:**
- Taylor Nguyen (former VP Eng): 2,000,000 shares (20% of founder pool)
  - 4-year vest, 1-year cliff, monthly thereafter
  - Departed after 8 months (before cliff)
  - Vested shares: 0 (cliff not reached)
  - Forfeited shares: 2,000,000 (returned to company pool)
  - Note: Taylor's departure triggered anti-dilution provision in SAFE #2 — see below

### Employee Stock Option Pool (ESOP)
- Original pool: 1,000,000 shares
- Granted options: 620,000 shares (to 8 employees)
  - Average strike price: $0.15/share (409A at time of grant)
  - Average vesting: 28 months remaining
- Forfeited from Taylor Nguyen: 2,000,000 shares returned to pool
- Unallocated pool: 2,380,000 shares
- Total ESOP reserved: 3,000,000 shares
- Target post-Series A ESOP: 12% of fully diluted

### Outstanding SAFEs (4 Investors, Different Caps)

**SAFE #1 — Horizon Ventures**
- Amount: $300,000
- Type: Post-money SAFE
- Valuation Cap: $10,000,000
- Discount: None
- Date: September 2023
- Pro rata rights: Yes

**SAFE #2 — Nexus Angels**
- Amount: $250,000
- Type: Post-money SAFE
- Valuation Cap: $15,000,000
- Discount: None
- Date: January 2024
- Pro rata rights: Yes
- Special provision: Anti-dilution adjustment if any founder departs before cliff
  (triggered by Taylor's departure — cap adjusts down to $13,500,000)

**SAFE #3 — Individual Angel (Dana Park)**
- Amount: $150,000
- Type: Post-money SAFE
- Valuation Cap: $20,000,000
- Discount: None
- Date: April 2024
- Pro rata rights: No
- MFN provision: Yes (can adopt terms of any later SAFE if more favorable)

**SAFE #4 — TechStars Fund**
- Amount: $100,000
- Type: Post-money SAFE
- Valuation Cap: $10,000,000
- Discount: None
- Date: June 2024
- Pro rata rights: No

### Convertible Note

**Bridge Note — Cascade Capital**
- Principal: $300,000
- Interest Rate: 6% annual (simple interest)
- Issue Date: December 2024
- Outstanding Period: 15 months (as of March 2026)
- Accrued Interest: $22,500 (300K x 6% x 15/12)
- Total Converting Amount: $322,500
- Valuation Cap: $12,000,000
- Discount: 20%
- Conversion trigger: Qualified financing of $5M+
- Maturity: December 2026

### Series A Terms

**Lead Investor: Granite Ventures**
- Pre-money Valuation: $65,000,000
- Investment Amount: $15,000,000
- Post-money Valuation: $80,000,000
- Price per share: TBD based on fully diluted pre-money share count
- ESOP expansion: increase to 12% of post-money (before pricing round)

**Series A Investor Syndicate:**
| Investor | Amount | Notes |
|----------|--------|-------|
| Granite Ventures (Lead) | $10,000,000 | Board seat, standard protective provisions |
| Stratos Capital | $3,000,000 | |
| Horizon Ventures (pro rata) | $1,200,000 | Exercising pro rata from SAFE |
| Nexus Angels (pro rata) | $800,000 | Exercising pro rata from SAFE |

**Series A Preferred Terms:**
- 1x non-participating liquidation preference
- Board: 2 common (founders), 1 preferred (Granite), 2 independent
- Protective provisions: standard (veto on new equity, debt >$500K, M&A)
- Anti-dilution: broad-based weighted average
- Drag-along: 60% of preferred + majority of common

### Requested Analysis
1. Calculate SAFE conversion prices (accounting for Nexus adjusted cap and MFN)
2. Calculate convertible note conversion (price vs discount — use more favorable to holder)
3. Determine ESOP expansion shares needed to reach 12% post-money
4. Build fully diluted cap table post-Series A with all ownership percentages
5. Run waterfall analysis at exit values: $100M, $250M, $500M, $1B
6. Show founder dilution progression: founding -> post-SAFE -> post-note -> post-Series A
7. Model the impact if Dana Park exercises MFN to match SAFE #1 terms ($10M cap)
