---
name: vc
description: >
  Venture capital analysis toolkit. Deal screening, investment memo
  generation, cap table modeling, term sheet analysis, financial
  modeling, KPI reporting, due diligence checklists, and portfolio
  reporting. Use when user says "vc", "deal screening",
  "investment memo", "cap table", "term sheet", "due diligence",
  "portfolio", "compare", "pitch deck", "startup analysis",
  "valuation", "SAFE", "convertible note", "funding round",
  "financial model", "3-statement", "projections", "P&L",
  "income statement", "balance sheet", "cash flow", "KPIs",
  "metrics", "SaaS metrics", "unit economics report",
  "burn multiple", "magic number", "Rule of 40",
  or "KPI dashboard".
---

# Claude-VC

Venture capital analysis toolkit. Routes to specialized sub-skills based on the command.

## Commands

| Command                     | What it does                                           |
| --------------------------- | ------------------------------------------------------ |
| `/vc screen <url or file>`  | Screen a startup from URL or pitch deck PDF            |
| `/vc memo`                  | Generate a structured investment memo                  |
| `/vc terms <file>`          | Analyze a term sheet, SAFE, or convertible note        |
| `/vc captable`              | Model cap table, dilution, and waterfall distributions |
| `/vc model`                 | Generate a simplified 3-statement financial model      |
| `/vc kpi`                   | Generate KPI reports with benchmarks and health scores |
| `/vc compare <url1> <url2>` | Side-by-side company comparison                        |
| `/vc diligence`             | Generate a due diligence checklist                     |
| `/vc portfolio`             | Generate portfolio reports from provided data          |

## Routing Logic

When the user provides arguments after `/vc`, determine the command:

1. If the first argument is one of the command names above (`screen`, `memo`, `terms`, `captable`, `model`, `kpi`, `compare`, `diligence`, `portfolio`), invoke the corresponding sub-skill by name (`vc-screen`, `vc-memo`, `vc-model`, `vc-kpi`, etc.) using the Skill tool, passing any remaining arguments.

2. If no recognized command is given, analyze the user's intent:
   - URL or file path provided -> run the **default workflow** (see below)
   - Mentions "memo" or "write-up" -> route to `vc-memo`
   - Mentions "terms", "SAFE", "convertible" -> route to `vc-terms`
   - Mentions "cap table", "dilution", "ownership" -> route to `vc-captable`
   - Mentions "financial model", "3-statement", "projections", "P&L", "income statement", "balance sheet", "cash flow" -> route to `vc-model`
   - Mentions "KPIs", "metrics", "SaaS metrics", "unit economics report", "burn multiple", "magic number", "Rule of 40", "KPI dashboard" -> route to `vc-kpi`
   - Mentions "compare", "versus", "side by side" -> route to `vc-compare`
   - Mentions "diligence", "DD", "checklist" -> route to `vc-diligence`
   - Mentions "portfolio", "LP report", "KPIs" -> route to `vc-portfolio`
   - Otherwise, ask the user which workflow they need

3. If the user invokes `/vc` with no arguments, display the commands table above and ask what they'd like to do.

## Default Workflow (URL or Pitch Deck)

When the user provides `/vc <url>` or `/vc <file>` without a command name, run screening, memo, and diligence in serial:

1. **Screen**: Perform the `vc-screen` workflow on the input. Present the Deal Score and screening results.
2. **Memo**: Perform the `vc-memo` workflow using the screening results as context. Generate the full investment memo.
3. **Diligence**: Perform the `vc-diligence` workflow to generate a due diligence checklist tailored to the company's stage and sector.

This gives the user a complete analysis in one command. Read the sub-skill files to get the full instructions:

- `${CLAUDE_SKILL_DIR}/../vc-screen/SKILL.md`
- `${CLAUDE_SKILL_DIR}/../vc-memo/SKILL.md`
- `${CLAUDE_SKILL_DIR}/../vc-diligence/SKILL.md`

## Full Screening Orchestration

When `/vc screen` is invoked with `--full`, or when `/vc memo --comprehensive` is used, orchestrate parallel analysis:

1. Gather the company information (URL, pitch deck, or description)
2. Spawn 6 parallel subagents using the Task tool:
   - `vc-financial`: Revenue model, unit economics, burn rate, projections
   - `vc-market`: TAM/SAM/SOM, market dynamics, timing, regulatory
   - `vc-technical`: Product maturity, tech stack, moat, IP landscape
   - `vc-legal`: Corporate structure, regulatory, contracts, litigation risk
   - `vc-competitive`: Competitor mapping, positioning, barriers to entry
   - `vc-team`: Founder backgrounds, team completeness, founder-market fit
3. Collect all results
4. Aggregate into a Deal Score (0-100) with dimension breakdown
5. Generate a comprehensive investment memo

## Reference Files

Load these on-demand as needed -- do NOT load all at startup:

- `${CLAUDE_SKILL_DIR}/references/investment-criteria.md` -- Scoring framework with default weights
- `${CLAUDE_SKILL_DIR}/references/valuation-methods.md` -- DCF, comparables, VC method, Berkus
- `${CLAUDE_SKILL_DIR}/references/disclaimers.md` -- Regulatory disclaimers for all outputs
- `${CLAUDE_SKILL_DIR}/references/due-diligence-checklist.md` -- Comprehensive DD items by category
- `${CLAUDE_SKILL_DIR}/references/term-sheet-terms.md` -- NVCA model terms with market commentary
- `${CLAUDE_SKILL_DIR}/references/safe-mechanics.md` -- YC SAFE variants, conversion mechanics
- `${CLAUDE_SKILL_DIR}/references/industry-multiples.md` -- Revenue/EBITDA multiples by sector

## Disclaimer Requirement

**Every output** from any `/vc` command must end with the appropriate disclaimer from `${CLAUDE_SKILL_DIR}/references/disclaimers.md`. Read that file and append the standard or enhanced disclaimer based on the output type:

- Standard disclaimer: for screening, memos, portfolio reports
- Enhanced disclaimer: for valuations, term sheet analysis, cap table outputs

## Optional Extensions

If MCP tools from extensions are available, sub-skills can use them to enrich analysis:

- **Octagon AI**: If `octagon-agent` tool is available, use it for private company data, funding rounds, investor profiles, and SEC filing analysis
- **SEC EDGAR**: If `vc-edgar` tools are available, use them for raw public company filing access
