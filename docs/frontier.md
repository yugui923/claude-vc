# The AI Frontier in Venture Capital

> Where AI capability ends and human judgment begins — a living record.

What AI can and cannot reliably do in venture capital, across **all AI tools on the market** — not only [claude-vc](https://github.com/yugui923/claude-vc).

## Scope of [claude-vc](https://github.com/yugui923/claude-vc)

[Claude-vc](https://github.com/yugui923/claude-vc) is an open-source Claude Code plugin for deal screening, investment memos, cap tables, term sheets, financial models, and KPI reports. It does not aim to replicate proprietary platforms like Harmonic (sourcing), Affinity (CRM), PitchBook (data), Luminance (legal), or Standard Metrics (portfolio monitoring).

Frontier-grade VC AI today requires a dozen+ MCP servers, data subscriptions, and specialized platforms — beyond what one open-source plugin can maintain. This document maps the full landscape, including capabilities claude-vc doesn't cover.

## Status key

- **Can Do** — AI handles reliably; reviewer sanity-checks, doesn't rewrite. For quantitative outputs, arithmetic and structure are correct given inputs; assumption quality is still human judgment.
- **WIP** — outputs need substantive rework, or simple cases work but edges/hybrids fail.
- **Cannot (capability)** — no viable AI path today.
- **Cannot (regulatory)** — technically possible, but licensing or fiduciary requirements prevent AI reliance. Marked with "Regulatory:" prefix in enabler; won't advance until regulation changes.
- **Enabler**[^1] — the AI advancement or product that made (or would make) this possible.

Last reviewed: 2026-05-07

---

### Deal Sourcing & Outreach

| Capability                                | Can Do | WIP | Cannot | Enabler                                      |
| ----------------------------------------- | :----: | :-: | :----: | -------------------------------------------- |
| Inbound pitch triage and initial scoring  |   ✓    |     |        | Extended thinking, Harmonic signal detection |
| New investment opportunity identification |        |  ✓  |        | Harmonic, Grata, EQT Motherbrain             |
| Founder relationship tracking             |        |  ✓  |        | Affinity AI, 4Degrees                        |
| Co-investor and syndicate coordination    |        |  ✓  |        | CRM integrations, email MCPs                 |
| Back-channel reference calls              |        |     |   ✓    | Needs real-world interaction                 |
| LP and stakeholder communications         |        |  ✓  |        | LLM drafting, email MCPs                     |

### Market Research

| Capability                                       | Can Do | WIP | Cannot | Enabler                                |
| ------------------------------------------------ | :----: | :-: | :----: | -------------------------------------- |
| Industry landscape synthesis from public sources |   ✓    |     |        | Web search, Perplexity, Claude         |
| Market sizing (TAM/SAM/SOM) from pitch materials |   ✓    |     |        | PDF vision, extended thinking          |
| Competitive landscape mapping from web research  |   ✓    |     |        | Web search tool use                    |
| Sector trend analysis from public data           |   ✓    |     |        | Web search, long-context reasoning     |
| Regulatory environment scanning                  |        |  ✓  |        | Web search, legal corpus MCPs          |
| Real-time market data and indices                |        |  ✓  |        | Bloomberg MCP, Refinitiv MCP           |
| Primary market research (surveys, interviews)    |        |  ✓  |        | DiligenceSquared AI voice agents       |
| Emerging market and whitespace identification    |        |  ✓  |        | Harmonic signals, Grata agentic search |

### Company Research

| Capability                                         | Can Do | WIP | Cannot | Enabler                                     |
| -------------------------------------------------- | :----: | :-: | :----: | ------------------------------------------- |
| Pitch deck data extraction (PDF)                   |   ✓    |     |        | PDF vision, multimodal understanding        |
| Public company profiling from web sources          |   ✓    |     |        | Web search tool use                         |
| Report generation (DOCX and markdown)              |   ✓    |     |        | Native file generation                      |
| Private company data access                        |   ✓    |     |        | PitchBook Navigator, Crunchbase, Grata      |
| Deal screening with structured scoring (0-100)     |   ✓    |     |        | Parallel subagents, extended thinking       |
| Investment memo generation (10-section format)     |   ✓    |     |        | Parallel subagents, long-context generation |
| KPI benchmarking by auto-detected company type     |   ✓    |     |        | Python tool use, extended thinking          |
| Comparable company analysis with market data       |   ✓    |     |        | PitchBook + Perplexity MCP                  |
| Factual claim verification against primary sources |        |  ✓  |        | Web search with source citations            |
| Systematic data room cross-referencing             |   ✓    |     |        | 1M context, self-verification               |

### Product Assessment

| Capability                                     | Can Do | WIP | Cannot | Enabler                                |
| ---------------------------------------------- | :----: | :-: | :----: | -------------------------------------- |
| Product claims extraction from pitch materials |   ✓    |     |        | PDF vision, multimodal understanding   |
| Feature set and roadmap summarization          |   ✓    |     |        | Long-context reasoning                 |
| Technical architecture assessment              |        |  ✓  |        | Code analysis tools, computer use      |
| User retention and engagement pattern analysis |        |  ✓  |        | Analytics platform MCPs                |
| Product-market fit validation                  |        |     |   ✓    | Needs usage data access, user research |
| Hands-on product testing and UX evaluation     |        |     |   ✓    | Needs computer use at scale            |

### Financial Analysis

| Capability                                     | Can Do | WIP | Cannot | Enabler                              |
| ---------------------------------------------- | :----: | :-: | :----: | ------------------------------------ |
| Burn rate and runway analysis                  |   ✓    |     |        | Python tool use                      |
| 3-statement model generation (P&L, BS, CF)     |   ✓    |     |        | Python tool use, self-verification   |
| Unit economics computation (LTV, CAC, payback) |   ✓    |     |        | Python tool use, self-verification   |
| Revenue projections (3-5 year forward)         |   ✓    |     |        | Python tool use, self-verification   |
| KPI auto-detection and health assessment       |   ✓    |     |        | Extended thinking, self-verification |
| Cohort and retention curve analysis            |        |  ✓  |        | Analytics MCPs, Python tool use      |
| Bulk portfolio-wide financial analysis         |        |  ✓  |        | ChatFin, Chronograph, 1M context     |
| Audit-grade financial statements               |        |     |   ✓    | Regulatory: formal verification      |

### Valuation

| Capability                                     | Can Do | WIP | Cannot | Enabler                                     |
| ---------------------------------------------- | :----: | :-: | :----: | ------------------------------------------- |
| Pre/post-money round modeling                  |   ✓    |     |        | Carta, Pulley, Python tool use              |
| Multiples-based valuation with industry ranges |   ✓    |     |        | Python tool use, web search                 |
| DCF analysis from user-provided assumptions    |   ✓    |     |        | Python tool use, self-verification          |
| Comparable company analysis with live data     |   ✓    |     |        | PitchBook + Perplexity MCP                  |
| Precedent transaction analysis                 |   ✓    |     |        | Grata, PitchBook + Perplexity MCP           |
| Conviction weighting on valuation outputs      |        |     |   ✓    | Needs calibrated confidence, human judgment |

### Deal Structuring & Negotiation

| Capability                                         | Can Do | WIP | Cannot | Enabler                                 |
| -------------------------------------------------- | :----: | :-: | :----: | --------------------------------------- |
| Cap table modeling and dilution analysis           |   ✓    |     |        | Carta, Pulley, Python tool use          |
| SAFE and convertible note conversion               |   ✓    |     |        | Carta, Pulley, OCF standard             |
| Multi-series liquidation waterfall                 |   ✓    |     |        | Carta, Pulley, Eqvista                  |
| Exit scenario modeling at multiple valuations      |   ✓    |     |        | Cap table platforms, Python tool use    |
| Term sheet red-flag identification (NVCA baseline) |   ✓    |     |        | Spellbook (10M+ contracts reviewed)     |
| Cap table platform sync (Carta, Pulley) via MCP    |        |  ✓  |        | Cap table platform MCPs                 |
| Negotiation strategy and counter-offer structuring |        |     |   ✓    | Needs relationship context, game theory |
| Binding legal document generation                  |        |     |   ✓    | Regulatory: legal licensing required    |

### Technical Due Diligence

| Capability                                    | Can Do | WIP | Cannot | Enabler                            |
| --------------------------------------------- | :----: | :-: | :----: | ---------------------------------- |
| Technical claims summarization from materials |   ✓    |     |        | Long-context reasoning             |
| Technology stack identification               |        |  ✓  |        | Web search, code analysis tool use |
| IP and patent strength evaluation             |        |  ✓  |        | IPRally, Patsnap, Patlytics        |
| Codebase quality and architecture review      |        |  ✓  |        | Code analysis agents, computer use |
| Scalability and infrastructure assessment     |        |     |   ✓    | Needs system access, load testing  |
| Technical team capability evaluation          |        |     |   ✓    | Needs real-world interaction       |

### Legal Due Diligence

| Capability                                        | Can Do | WIP | Cannot | Enabler                                 |
| ------------------------------------------------- | :----: | :-: | :----: | --------------------------------------- |
| Common provision pattern flagging                 |   ✓    |     |        | Spellbook, Luminance                    |
| NVCA baseline term comparison                     |   ✓    |     |        | Spellbook VC clause library             |
| Contract review (SHA, IP assignments, employment) |        |  ✓  |        | Luminance, Kira/Litera (64% Am Law 100) |
| Regulatory compliance analysis                    |        |  ✓  |        | Emerging legal AI tools                 |
| Legal opinions and formal advice                  |        |     |   ✓    | Regulatory: legal licensing required    |
| Cross-jurisdiction tax and structuring            |        |     |   ✓    | Regulatory: licensing + tax law MCPs    |

### Financial Due Diligence

| Capability                                  | Can Do | WIP | Cannot | Enabler                                 |
| ------------------------------------------- | :----: | :-: | :----: | --------------------------------------- |
| Individual financial document analysis      |   ✓    |     |        | Hebbia Matrix, PDF vision               |
| Private company financial data              |   ✓    |     |        | PitchBook, Morningstar, Grata           |
| Financial model internal consistency checks |   ✓    |     |        | Python tool use, self-verification      |
| Portfolio company data connectivity         |        |  ✓  |        | Standard Metrics, Chronograph MCPs      |
| Data room systematic cross-referencing      |   ✓    |     |        | 1M context, self-verification           |
| Historical financials verification          |        |     |   ✓    | Needs SEC EDGAR MCP, audit trail access |
| Tax and transfer pricing analysis           |        |     |   ✓    | Regulatory: licensing + tax law MCPs    |

### Portfolio Management

| Capability                            | Can Do | WIP | Cannot | Enabler                                        |
| ------------------------------------- | :----: | :-: | :----: | ---------------------------------------------- |
| CRM and deal pipeline tracking        |   ✓    |     |        | Affinity AI (auto-capture, relationship intel) |
| One-time portfolio summary generation |   ✓    |     |        | Extended thinking, structured output           |
| Board deck preparation assistance     |   ✓    |     |        | Long-context generation, native file output    |
| Ongoing portfolio monitoring          |        |  ✓  |        | Standard Metrics, Chronograph, ChatFin         |
| Scheduled recurring reports           |        |  ✓  |        | Standard Metrics, Visible.vc automation        |
| Anomaly detection and alerts          |        |  ✓  |        | ChatFin anomaly engine                         |
| LP reporting preparation              |   ✓    |     |        | claude-vc portfolio skill, Standard Metrics    |

### Investment Decision & Closing

| Capability                              | Can Do | WIP | Cannot | Enabler                                     |
| --------------------------------------- | :----: | :-: | :----: | ------------------------------------------- |
| IC preparation materials                |   ✓    |     |        | Extended thinking, long-context generation  |
| Decision framework structuring          |   ✓    |     |        | Extended thinking, structured output        |
| Invest/pass recommendation              |        |     |   ✓    | Needs calibrated confidence, human judgment |
| Founder and team qualitative assessment |        |     |   ✓    | Needs real-world interaction                |
| IC facilitation and voting              |        |     |   ✓    | Needs multi-user collaboration              |
| Closing coordination and execution      |        |     |   ✓    | Needs legal tooling, payment systems        |
| Post-closing deliverable management     |        |  ✓  |        | Workflow automation, persistent agents      |

---

## Changelog

Dates reflect when the enabler **shipped**, not when adoption matured.

| Date    | Change                                       | Capability affected                             | Direction        | Enabler                                                                              |
| ------- | -------------------------------------------- | ----------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------ |
| 2022-09 | AI contract drafting and review              | Common provision pattern flagging               | Human -> WIP     | Spellbook launch                                                                     |
| 2022-11 | AI-powered deal sourcing signals             | New investment opportunity identification       | Human -> WIP     | Harmonic Series A                                                                    |
| 2022-11 | Basic memo drafting and market summaries     | Investment memo generation                      | Human -> WIP     | ChatGPT (GPT-3.5)                                                                    |
| 2023-03 | Professional-grade investment analysis       | Industry landscape synthesis                    | WIP -> Can Do    | GPT-4 reasoning quality                                                              |
| 2023-06 | Structured API tool calling                  | KPI benchmarking, financial model checks        | Human -> WIP     | OpenAI function calling                                                              |
| 2023-07 | Full document analysis (100K context)        | Pitch deck data extraction                      | Human -> Can Do  | Claude 2                                                                             |
| 2023-09 | AI relationship intelligence in CRM          | Founder relationship tracking                   | Human -> WIP     | Affinity AI                                                                          |
| 2023-11 | Reliable structured data extraction          | KPI benchmarking, deal screening                | WIP -> Can Do    | GPT-4 Turbo, JSON mode, 128K context                                                 |
| 2024-03 | Pitch deck and chart visual analysis         | Pitch deck data extraction, product claims      | Human -> Can Do  | Claude 3 vision + 200K context                                                       |
| 2024-05 | AI-orchestrated multi-tool workflows         | Deal screening, financial model generation      | Human -> WIP     | Claude tool use GA                                                                   |
| 2024-06 | Cost-effective AI analysis at pipeline scale | Inbound pitch triage                            | WIP -> Can Do    | Claude 3.5 Sonnet                                                                    |
| 2024-08 | Perfect structured extraction (100% schema)  | KPI benchmarking, financial model checks        | WIP -> Can Do    | OpenAI structured outputs                                                            |
| 2024-09 | Native PDF document processing               | Pitch deck data extraction, document analysis   | Human -> Can Do  | Claude PDF support                                                                   |
| 2024-10 | Computer-use automation for legacy tools     | Technical architecture assessment               | Human -> WIP     | Claude computer use beta                                                             |
| 2024-10 | Multi-agent due diligence workflows          | Systematic data room cross-referencing          | Human -> WIP     | CrewAI maturity, AutoGen                                                             |
| 2024-11 | Natural-language private company queries     | Private company data access                     | Human -> WIP     | PitchBook Navigator + OpenAI                                                         |
| 2024-11 | Standardized AI-to-data connectivity         | Portfolio company data connectivity             | Human -> WIP     | MCP (Model Context Protocol)                                                         |
| 2025-02 | Deep financial reasoning on demand           | 3-statement model generation, DCF analysis      | Human -> WIP     | Extended thinking (Claude 3.7)                                                       |
| 2025-02 | Agentic coding for custom VC tools           | Unit economics computation, burn rate analysis  | Human -> WIP     | Claude Code research preview                                                         |
| 2025-03 | Real-time market intelligence in AI          | Sector trend analysis, competitive mapping      | Human -> Can Do  | Claude web search                                                                    |
| 2025-05 | Production-grade agentic VC tooling          | Report generation, exit scenario modeling       | WIP -> Can Do    | Claude Code GA                                                                       |
| 2025-07 | Standard Metrics MCP                         | Portfolio company data connectivity             | --               | Lookup-only; no anomaly detection or cross-fund aggregation                          |
| 2025-09 | End-to-end document production               | Report generation (DOCX), board deck prep       | Human -> Can Do  | Native file generation                                                               |
| 2025-11 | Private market data at scale via MCP         | Private company data access                     | WIP -> Can Do    | PitchBook Navigator MCP                                                              |
| 2026-02 | Full data room in single context             | Systematic data room cross-referencing          | Human -> Can Do  | 1M token context (Claude 4.6)                                                        |
| 2026-03 | PitchBook data in conversational AI          | Comparable analysis, precedent transactions     | WIP -> Can Do    | PitchBook + Perplexity MCP                                                           |
| 2026-03 | Fund-level return metrics                    | IRR, MOIC, DPI, TVPI, PME computation           | Human -> Can Do  | Python tool use, native file generation                                              |
| 2026-03 | XLSX export for financial outputs            | Spreadsheet generation for cap tables, models   | Human -> Can Do  | Native file generation + skill flags                                                 |
| 2026-03 | Parallel multi-agent deal screening          | Full screening with 6 concurrent agents         | WIP -> Can Do    | Multi-agent orchestration via subagents                                              |
| 2026-03 | Side-by-side company comparison              | Structured comparison of 2-4 companies          | WIP -> Can Do    | Long-context reasoning, structured output                                            |
| 2026-03 | Customizable due diligence checklists        | Stage+sector-specific DD checklist              | Cannot -> Can Do | Long-context generation, structured prompting                                        |
| 2026-03 | One-shot portfolio reporting for LPs         | LP-ready portfolio summary                      | Cannot -> Can Do | Extended thinking, native file generation                                            |
| 2026-04 | Multiples valuation                          | Multiples-based valuation with industry ranges  | WIP -> Can Do    | Python tool use, web search                                                          |
| 2026-04 | Self-verified financial analysis             | 3-stmt model, unit econ, DCF, consistency       | WIP -> Can Do    | Claude Opus 4.7 self-verification                                                    |
| 2026-04 | Improved reasoning (GPQA 94.2%)              | KPI auto-detection and health assessment        | WIP -> Can Do    | Claude Opus 4.7 extended thinking                                                    |
| 2026-04 | Opus 4.7 vision (3.75MP, 3x prior)           | High-res document and diagram analysis          | --               | Claude Opus 4.7                                                                      |
| 2026-04 | GPT-5.4 reaches 1.05M token context          | Full data room in single context (non-Claude)   | --               | GPT-5.4 (OpenAI)                                                                     |
| 2026-04 | Carta Plugins for Claude                     | Cap table platform sync via MCP                 | --               | Carta-hosted only; Pulley/AngelList/Eqvista excluded                                 |
| 2026-04 | Gemini Deep Research Max preview             | Long-horizon research synthesis with native MCP | --               | Gemini 3.1 Pro + announced (not GA) FactSet/S&P/PitchBook MCPs                       |
| 2026-04 | GPT-5.5 GA                                   | Frontier baseline                               | --               | 1M ctx, ARC-AGI-2 85%; AA-Omniscience: 86% confab on errors → Opus 4.7 for citations |
| 2026-04 | 1M-context reasoning on open weights         | Self-hosted full-data-room reasoning            | --               | DeepSeek V4-Pro                                                                      |
| 2026-04 | Affinity hosted MCP (beta)                   | Founder relationship tracking                   | --               | Scale+ tiers; internal signals only; no external discovery                           |
| 2026-04 | Agentic finance AI at 250+ institutions      | Systematic data room cross-referencing          | --               | Rogo Felix                                                                           |
| 2026-04 | AI contract redlining bundled in Word        | Common provision pattern flagging               | --               | Microsoft Legal Agent for Word (early-access)                                        |
| 2026-05 | GPT-5.5 Instant default in ChatGPT           | Investment memo quality                         | --               | OpenAI claims 52.5% fewer hallucinations; AA-Omniscience contradicts                 |
| 2026-05 | SEC EDGAR MCP servers in production          | Public comparables / IPO filings only           | --               | sec-edgar-mcp, EdgarTools — does NOT cover private companies                         |

---

## Methodology

### Changelog conventions

- Entries reflect industry-wide capability shifts, attributed to the model release, product, or integration that enabled them.
- **Regressions** logged as `Can Do → WIP` or `WIP → Cannot` with date and cause. None recorded yet — reflects the doc's youth (March 2026 baseline), not an assumption of one-way progress.

### Known limitations

1. **Enabler attribution is best-effort, not causal.** A capability became reliable around the time the enabler shipped.
2. **Anthropic-skewed.** The changelog over-indexes on Anthropic releases (what we test directly); other providers covered when materially frontier-changing.
3. **Self-verification** (Opus 4.7, April 2026) means the model writes checks for its own outputs — test assertions, re-reads, cross-checks — before reporting. Catches arithmetic and structural errors, not bad assumptions.

---

[^1]:
    **Enabler** = the AI product, feature, or integration that made (or would make) a capability possible. Either _intrinsic_ (available to any user of the model) or _integration-gated_ (requires third-party subscription or MCP).

    Common intrinsic: extended thinking, Python tool use, web search, PDF vision, native file generation, 1M context, structured output, self-verification.

    Common integration-gated: PitchBook Navigator, Carta/Pulley, Spellbook, Harmonic, Grata, Standard Metrics/Chronograph, Hebbia Matrix.

    A "Can Do" with an integration-gated enabler requires that subscription — it is not universally available.
