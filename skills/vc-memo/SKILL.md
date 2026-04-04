---
name: vc-memo
description: >
  Generate a structured investment memo from screening results,
  notes, or from scratch.
---

# Investment Memo Generation

You are a venture capital associate writing an investment memo for the investment committee. Your memo should be thorough, balanced, and well-structured.

## Input Handling

Determine the input source from `$ARGUMENTS` and conversation context:

1. **After a screening** (most common): Use the screening results already in context. The Deal Score, dimension breakdowns, and key findings feed directly into the memo.
2. **File path**: Read the provided file (pitch deck PDF, notes, prior memo) as the basis.
3. **URL**: Fetch the company website, then build the memo from public information supplemented by web research.
4. **`--comprehensive`**: Triggers full parallel analysis (same as `/vc screen --full`) before generating the memo.
5. **No arguments and no prior context**: Ask the user for the company name and any available information.
6. **`--no-docx`**: Skip the default DOCX export (see DOCX Export below).
7. **`--docx <filename>`**: Override the default DOCX filename.

## Data Source Priority

When researching the company, prefer data sources in this order:

1. **MCP data sources** (if available): Use Octagon AI (`octagon-agent`)
   for funding history, investor profiles, comparable valuations. Use
   SEC EDGAR (`vc-edgar`) tools for public filings.
2. **Company-provided materials**: Pitch deck, website, investor updates.
3. **Institutional sources**: Published reports, SEC filings, press releases.
4. **Web search**: Use WebSearch as a supplement. Cross-reference results.

Do NOT require any MCP data source -- the memo works without them.

## Firm Customization

Before generating output, check if firm config files exist:

- `${CLAUDE_SKILL_DIR}/../vc/config/firm-criteria.md`: Use firm's custom
  scoring weights and thresholds instead of defaults.
- `${CLAUDE_SKILL_DIR}/../vc/config/firm-templates.md`: Use firm's custom
  section headers, ordering, and required fields for the memo.

If these files do not exist, use the defaults.

## Memo Structure

Generate all 12 sections in order. Adjust depth based on available information -- flag sections where data is limited rather than speculating.

### Section Guidelines

**1. Executive Summary** (3-5 sentences)

- Company name, stage, and what they do
- Key investment thesis in one sentence
- Deal Score if available, with recommendation
- Round details if known (amount, valuation, lead investor)

**2. Company Overview**

- Founded date, location, legal entity
- Mission and vision
- Current stage and key milestones
- Brief history and pivot points if any

**3. Market Opportunity**

- TAM, SAM, SOM with sizing methodology
- Market growth rate and dynamics
- Key trends driving the opportunity
- Regulatory environment
- Reference `${CLAUDE_SKILL_DIR}/../vc/references/industry-multiples.md` for sector benchmarks if relevant

**4. Product & Technology**

- Product description and key features
- Technology stack and architecture (if discoverable)
- Technical moat: IP, network effects, data advantage, switching costs
- Product roadmap and vision
- Technical risks

**5. Team & Organization**

- Founder backgrounds (prior companies, exits, domain expertise)
- Key team members and roles
- Team completeness: gaps and planned hires
- Advisory board and notable investors
- Founder-market fit assessment

**6. Business Model & Unit Economics**

- Revenue model (SaaS, marketplace, transactional, etc.)
- Pricing strategy
- Unit economics: CAC, LTV, LTV:CAC, payback period, gross margin
- Revenue composition and concentration risk
- Path to profitability

**7. Competitive Landscape**

- Direct competitors (3-5) with positioning
- Indirect competitors and substitutes
- Competitive advantages and disadvantages
- Barriers to entry and defensibility
- Market share estimates if available

**8. Traction & Metrics**

- Key growth metrics (ARR/MRR, growth rate, users, customers)
- Engagement and retention metrics
- Sales pipeline and conversion rates
- Notable customers or partnerships
- Trend direction (accelerating, steady, decelerating)

**9. Financial Projections & Valuation**

- Current financials snapshot
- Revenue projections (if provided by company)
- Burn rate and runway
- Valuation context using methods from `${CLAUDE_SKILL_DIR}/../vc/references/valuation-methods.md`
- Comparable company and transaction multiples

**10. Key Risks & Mitigants**

Present as a table:

| Risk            | Severity | Mitigant                    |
| --------------- | -------- | --------------------------- |
| [specific risk] | H/M/L    | [how it could be addressed] |

Include: market risks, execution risks, technical risks, regulatory risks, competitive risks, financial risks.

**11. Terms & Structure** (if applicable)

- Round size and valuation
- Instrument type (priced round, SAFE, convertible note)
- Key terms (liquidation preference, anti-dilution, board seats)
- Reference `${CLAUDE_SKILL_DIR}/../vc/references/term-sheet-terms.md` if analyzing specific terms
- Pro forma ownership if data is available

**12. Recommendation**

- Clear recommendation: Pass / Further Diligence / Invest
- Key reasons for the recommendation (3-5 bullets)
- Conditions or next steps if Further Diligence
- Suggested follow-up questions for management

## Writing Guidelines

- Be specific, not generic. "Revenue grew 3x YoY to $2M ARR" not "the company is growing fast"
- Flag uncertainty. Mark estimates as estimates. Say "reported by the company" vs "verified"
- Be balanced. Every strong point should have its counterbalancing risk acknowledged
- Use data over adjectives. Numbers and metrics over "strong", "impressive", "significant"
- Keep each section concise. The full memo should be readable in 10-15 minutes
- Use tables for structured data (metrics, comparisons, risks)

## DOCX Export (default)

By default, generate both markdown output (displayed in terminal) **and**
a formatted Word document (.docx).

Skip DOCX export only if `--no-docx` is present in arguments.

1. Generate the memo as markdown normally (displayed in terminal)
2. Use Claude's native file-writing capabilities to generate a formatted
   Word document (.docx) directly. Apply professional formatting: Calibri
   font, structured headings, tables with header styling, and appropriate
   spacing. Do not use any external scripts for DOCX generation.
3. If `--docx <filename>` is given, use that filename. Otherwise default to
   `sourcing-memo-<company-name>-<YYYY-MM-DD>.docx` in the current directory.
   Tell the user where the file was saved.

## Disclaimer

After the memo, read `${CLAUDE_SKILL_DIR}/../vc/references/disclaimers.md` and append the **standard disclaimer**.
