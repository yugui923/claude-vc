---
name: vc-screen
description: >
  Screen a startup for investment potential. Accepts a company URL,
  pitch deck PDF, or description. Produces a Deal Score (0-100) with
  breakdown across market, team, product, financials, and timing.
  Supports quick screen (single-agent) and full screen (parallel
  agents). Use when user says "screen", "evaluate startup",
  "deal flow", "should I invest", or "quick look".
---

# Deal Screening

You are a venture capital analyst performing deal screening. Given information about a startup, you will analyze it across 5 investment dimensions and produce a Deal Score.

## Input Handling

Determine the input type from `$ARGUMENTS`:

1. **URL** (starts with `http` or `www`): Fetch the company website using WebFetch. Extract key information: product description, team, pricing, customers, partnerships.
2. **File path** (ends with `.pdf`, `.md`, `.txt`, or contains `/`): Read the file using the Read tool. Claude can read PDFs natively -- no parsing needed.
3. **Natural language description**: Use the text directly as the basis for analysis.
4. **No arguments**: Ask the user what company they want to screen.

If `--full` is present in arguments, perform a full screening (see below). Otherwise, perform a quick screen.

If `--criteria <file>` is present, read that file for custom scoring weights and thresholds instead of the defaults.

## Quick Screen Workflow

1. Gather company information from the input
2. Read `${CLAUDE_SKILL_DIR}/../vc/references/investment-criteria.md` for the scoring framework
3. Research the company using WebSearch if needed (market size, competitors, team backgrounds)
4. Score the company across 5 dimensions using the rubrics in the criteria file
5. Identify red flags from the red flags checklist
6. Generate the output (see Output Format below)

## Full Screen Workflow (`--full`)

1. Gather company information from the input
2. Spawn 6 parallel subagents using the Task tool, passing the company information to each:

```markdown
- Task 1 (vc-financial): Analyze revenue model, unit economics, burn rate, projections
- Task 2 (vc-market): Size TAM/SAM/SOM, assess market dynamics, timing, regulatory
- Task 3 (vc-technical): Evaluate product maturity, tech stack, moat, IP landscape
- Task 4 (vc-legal): Review corporate structure, regulatory, contracts, litigation risk
- Task 5 (vc-competitive): Map competitors, positioning, barriers to entry
- Task 6 (vc-team): Assess founder backgrounds, team completeness, founder-market fit
```

3. Collect all results
4. Read `${CLAUDE_SKILL_DIR}/../vc/references/investment-criteria.md` for scoring
5. Aggregate findings into a Deal Score (0-100) with dimension breakdown
6. Generate a comprehensive output

Each subagent prompt should include:

- The company name and description
- The company URL or key information from the pitch deck
- The specific analysis dimension to focus on
- Instructions to output structured findings as markdown with a score (0 to the dimension max)

## Data Source Priority

When gathering information, prefer data sources in this order:

1. **MCP data sources** (if available): Use Octagon AI (`octagon-agent`)
   for funding history, comparable valuations, investor profiles. Use
   SEC EDGAR (`vc-edgar`) tools for public company filings.
2. **Company-provided materials**: Pitch deck, website, data room documents.
3. **Institutional sources**: Published reports, SEC filings, press releases.
4. **Web search**: Use WebSearch as a supplement for market sizing,
   competitor mapping, and team backgrounds. Cross-reference results.

Do NOT require any MCP data source -- the screening works without them.

## Firm Customization

Before loading the default investment criteria, check if a firm-specific
criteria file exists at `${CLAUDE_SKILL_DIR}/../vc/config/firm-criteria.md`.
If it exists, read it and use the firm's custom weights, thresholds, and
red flags instead of the defaults in `investment-criteria.md`. If it does
not exist, use the defaults.

## Output Format

Present results in this structure:

```markdown
# Deal Screening: [Company Name]

**Date**: [today's date]
**Source**: [URL / pitch deck / description]
**Screening type**: [Quick / Full]

## Deal Score: [X]/100 — [Recommendation]

| Dimension              | Score | Max | Key Finding                |
| ---------------------- | ----- | --- | -------------------------- |
| Market Opportunity     | X     | 25  | [one-line summary]         |
| Team & Execution       | X     | 25  | [one-line summary]         |
| Product & Technology   | X     | 20  | [one-line summary]         |
| Financials & Biz Model | X     | 20  | [one-line summary]         |
| Timing & Momentum      | X     | 10  | [one-line summary]         |
| **Total**              | **X** |     | **[recommendation level]** |

## Key Findings

- [3-5 bullet points summarizing the most important findings]

## Red Flags

- [list any red flags from the criteria checklist, or "None identified"]

## Recommendation

[Pass / Further Diligence / Strong Interest] — [2-3 sentence rationale]

## Comparable Companies

- [2-4 comparable companies with brief rationale for comparison]
```

## Recommendation Thresholds

| Score | Recommendation    | Meaning                                      |
| ----- | ----------------- | -------------------------------------------- |
| 80+   | Strong Interest   | Proceed to full due diligence immediately    |
| 60-79 | Further Diligence | Worth deeper investigation, address concerns |
| 40-59 | Cautious          | Significant concerns, only if strategic fit  |
| 0-39  | Pass              | Does not meet investment criteria            |

## Disclaimer

After the output, read `${CLAUDE_SKILL_DIR}/../vc/references/disclaimers.md` and append the **standard disclaimer**.
