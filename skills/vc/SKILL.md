---
name: vc
description: >
  Venture capital analysis toolkit. Give it a URL or pitch deck and it
  runs screening + memo. Type "/vc help" for details on all 6 commands.
---

# Claude-VC

Venture capital analysis toolkit. A single skill with 6 sub-commands covering
the full VC workflow: evaluate deals, write memos, analyze terms, model
equity, build financials, and monitor portfolios.

## Commands

| Command                    | What it does                                             |
| -------------------------- | -------------------------------------------------------- |
| `/vc screen <input(s)>`    | Score a startup (1 input) or compare 2-4 companies       |
| `/vc memo <input>`         | Write a structured investment memo (with DD checklist)   |
| `/vc terms <file>`         | Analyze a term sheet, SAFE, or convertible note          |
| `/vc captable <input>`     | Model cap table, dilution, waterfall, exit scenarios     |
| `/vc model <input>`        | Generate a 3-statement financial model with projections  |
| `/vc portfolio <data>`     | Portfolio report, KPI dashboard, or returns analysis     |
| `/vc help`                 | Show help                                                |

## Routing Logic

When the user invokes `/vc`, parse `$ARGUMENTS`:

1. If the first argument is `help`, display the Help section (below) and stop.

2. If the first argument is one of the command names (`screen`, `memo`,
   `terms`, `captable`, `model`, `portfolio`), **read the corresponding
   command file and follow its instructions**, passing any remaining arguments:

   - `screen` → `${CLAUDE_SKILL_DIR}/commands/screen.md`
   - `memo` → `${CLAUDE_SKILL_DIR}/commands/memo.md`
   - `terms` → `${CLAUDE_SKILL_DIR}/commands/terms.md`
   - `captable` → `${CLAUDE_SKILL_DIR}/commands/captable.md`
   - `model` → `${CLAUDE_SKILL_DIR}/commands/model.md`
   - `portfolio` → `${CLAUDE_SKILL_DIR}/commands/portfolio.md`

3. If no recognized command is given, analyze the user's intent:
   - URL or file path provided → run the **default workflow** (see below)
   - Mentions "memo" or "write-up" → follow `commands/memo.md`
   - Mentions "terms", "SAFE", "convertible" → follow `commands/terms.md`
   - Mentions "cap table", "dilution", "ownership", "waterfall" → follow
     `commands/captable.md`
   - Mentions "financial model", "3-statement", "projections", "P&L",
     "income statement", "balance sheet", "cash flow" → follow
     `commands/model.md`
   - Mentions "compare", "versus", "side by side" → follow
     `commands/screen.md` (comparison mode)
   - Mentions "diligence", "DD", "checklist" → follow `commands/memo.md`
     with `--diligence-only`
   - Mentions "KPIs", "metrics", "SaaS metrics", "Rule of 40", "burn
     multiple", "magic number", "KPI dashboard" → follow
     `commands/portfolio.md` with `--kpi`
   - Mentions "IRR", "MOIC", "DPI", "TVPI", "PME", "fund performance",
     "returns" → follow `commands/portfolio.md` with `--returns`
   - Mentions "portfolio", "LP report" → follow `commands/portfolio.md`
   - Otherwise, ask the user which workflow they need

4. If the user invokes `/vc` with no arguments, display the Help section.

## Default Workflow (URL or Pitch Deck)

When the user provides `/vc <url>` or `/vc <file>` without a command name,
run screening and memo in serial. The memo now includes a tailored due
diligence checklist, so the chain is two steps instead of three:

1. Tell the user: **"Step 1/2 — Screening [company/input]..."**
2. **Screen**: Read `${CLAUDE_SKILL_DIR}/commands/screen.md` and perform a
   quick screen on the input. Present the Deal Score and screening results.
3. Tell the user: **"Step 2/2 — Writing investment memo with DD checklist..."**
4. **Memo**: Read `${CLAUDE_SKILL_DIR}/commands/memo.md` and generate the
   full memo using the screening results as context. The memo's Section 12
   is the tailored DD checklist.

## Full Screening Orchestration

When `/vc screen` is invoked with `--full`, or when `/vc memo` is used with
`--comprehensive`, orchestrate parallel analysis per `commands/screen.md`:

1. Gather the company information.
2. Tell the user: **"Launching 6 parallel analysts: financial, market, technical, legal, competitive, team..."**
3. Spawn 6 parallel sub-agents using the Agent/Task tool. For each, read the
   prompt file at `${CLAUDE_SKILL_DIR}/agents/<name>.md` and use it as the
   sub-agent's instructions:
   - `agents/financial.md` — Revenue, unit economics, burn, projections
   - `agents/market.md` — TAM/SAM/SOM, dynamics, timing, regulatory
   - `agents/technical.md` — Product maturity, tech stack, moat, IP
   - `agents/legal.md` — Corporate structure, regulatory, contracts, litigation
   - `agents/competitive.md` — Competitor mapping, positioning, barriers
   - `agents/team.md` — Founder backgrounds, completeness, founder-market fit
4. Collect all results (each sub-agent ends with a `FINDINGS_SUMMARY` line).
5. Tell the user: **"All 6 analyses complete. Aggregating Deal Score..."**
6. Aggregate into a Deal Score (0-100) with dimension breakdown.
7. Proceed with the requesting command's output format.

## Reference Files

Load these on-demand as needed — do NOT load all at startup:

- `${CLAUDE_SKILL_DIR}/references/investment-criteria.md` — Scoring framework
  with default weights
- `${CLAUDE_SKILL_DIR}/references/valuation-methods.md` — DCF, comparables,
  VC method, Berkus
- `${CLAUDE_SKILL_DIR}/references/disclaimers.md` — Regulatory disclaimers
  for all outputs
- `${CLAUDE_SKILL_DIR}/references/due-diligence-checklist.md` — Comprehensive
  DD items by category
- `${CLAUDE_SKILL_DIR}/references/term-sheet-terms.md` — NVCA model terms
  with market commentary
- `${CLAUDE_SKILL_DIR}/references/safe-mechanics.md` — YC SAFE variants,
  conversion mechanics
- `${CLAUDE_SKILL_DIR}/references/industry-multiples.md` — Revenue/EBITDA
  multiples by sector

## Disclaimer Requirement

**Every output** from any `/vc` command must end with the appropriate
disclaimer from `${CLAUDE_SKILL_DIR}/references/disclaimers.md`. Read that
file and append the standard or enhanced disclaimer based on the output type:

- Standard disclaimer: for screening, memos, portfolio reports, comparisons,
  DD checklists
- Enhanced disclaimer: for valuations, term sheet analysis, cap table
  outputs, financial models, KPI reports, returns analysis

## Optional Extensions

If MCP tools from extensions are available, commands and sub-agents can use
them to enrich analysis:

- **Octagon AI**: If `octagon-agent` tool is available, use it for private
  company data, funding rounds, investor profiles, and SEC filing analysis
- **SEC EDGAR**: If `vc-edgar` tools are available, use them for raw public
  company filing access

## Help

When the user types `/vc help` or `/vc` with no arguments, display the
following help text and ask what they'd like to do:

```
Claude-VC — venture capital analysis toolkit

Usage:
  /vc <url or file>          Screen → Memo (the default workflow)
  /vc <command> [args]       Run a specific command

Commands:
  screen <input(s)>          Score a startup 0-100 (1 input) or compare (2-4 inputs)
                               Flags: --full (6 parallel agents), --criteria <file>
  memo <input>               Write a structured investment memo + DD checklist
                               Flags: --comprehensive, --diligence-only,
                                      --stage <stage>, --sector <sector>, --no-docx
  terms <file>               Review a term sheet, SAFE, or convertible note
  captable <input>           Model cap table, dilution, waterfall, exit scenarios
                               Flags: --no-xlsx
  model <input>              Build a 3-statement financial model (3-5 year projection)
                               Flags: --no-docx, --no-xlsx
  portfolio <data>           Portfolio report by default
                               Flags: --kpi (KPI dashboard for one company)
                                      --returns (fund-level IRR/MOIC/DPI/TVPI/PME)
                                      --no-docx, --no-xlsx
  help                       Show this help message

Examples:
  /vc https://ramp.com                     Screen Ramp and write an investment memo
  /vc pitch-deck.pdf                       Screen a startup from its pitch deck
  /vc screen https://ramp.com --full       Deep screen with 6 parallel analysts
  /vc screen a.pdf b.pdf c.pdf             Compare 3 companies side by side
  /vc memo https://notion.so               Write a 12-section memo for Notion
  /vc memo --diligence-only --stage seed   Generate just the DD checklist for a seed deal
  /vc terms safe-agreement.pdf             Analyze a SAFE against NVCA standards
  /vc captable                             Model your cap table interactively
  /vc model --no-xlsx                      Build a 3-statement model (markdown only)
  /vc portfolio portfolio.csv              LP-ready portfolio report from a CSV
  /vc portfolio metrics.json --kpi         KPI dashboard for a single company
  /vc portfolio investments.csv --returns  Fund-level IRR, MOIC, DPI, TVPI analysis
  /vc status                               Check which data sources are connected
```
