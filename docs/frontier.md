# The AI Frontier in Venture Capital

> Where AI capability ends and human judgment begins — a living record.

This document tracks what AI can and cannot reliably do in venture capital
analysis. It reflects the **state of the art across all AI tools on the
market** — not only what [claude-vc](https://github.com/yugui923/claude-vc)
provides.

## Scope of [claude-vc](https://github.com/yugui923/claude-vc)

[Claude-vc](https://github.com/yugui923/claude-vc) is an open-source Claude
Code skill plugin focused on deal screening, investment memos, cap table
modeling, term sheet analysis, financial modeling, and KPI reporting. It does
not intend to be an all-encompassing VC platform. It will gradually expand, but
it does not aim to replicate proprietary tools like Harmonic (deal sourcing),
Affinity (CRM), PitchBook (data), Luminance (legal review), or Standard
Metrics (portfolio monitoring).

Achieving state-of-the-art performance in venture capital AI today requires
integrating a dozen or more MCP servers, proprietary data subscriptions, and
specialized platforms. Without a larger maintainer community, it is not feasible
for a single open-source plugin to maintain those integrations. This document
therefore serves as a map — it tells you what is possible with the right
combination of tools, even where
[claude-vc](https://github.com/yugui923/claude-vc) does not yet cover it.

## Status key

- **Can Do**: The best AI tools on the market handle this reliably today
- **WIP**: AI can attempt this, but outputs need human verification or
  integration is still maturing
- **Cannot**: Requires human judgment, licensed professionals, or capabilities
  with no viable near-term path
- **Enabler**[^1]: The AI advancement or product that made or would make this
  possible

Last reviewed: 2026-04-18

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

| Capability                                         | Can Do | WIP | Cannot | Enabler                                       |
| -------------------------------------------------- | :----: | :-: | :----: | --------------------------------------------- |
| Pitch deck data extraction (PDF)                   |   ✓    |     |        | PDF vision, multimodal understanding          |
| Public company profiling from web sources          |   ✓    |     |        | Web search tool use                           |
| Report generation (DOCX and markdown)              |   ✓    |     |        | Native file generation                        |
| Private company data access                        |   ✓    |     |        | PitchBook Navigator, Crunchbase, Grata        |
| Deal screening with structured scoring (0-100)     |   ✓    |     |        | Parallel subagents, extended thinking         |
| Investment memo generation (10-section format)     |   ✓    |     |        | Parallel subagents, long-context generation   |
| KPI benchmarking by auto-detected company type     |   ✓    |     |        | Python tool use, extended thinking            |
| Comparable company analysis with market data       |   ✓    |     |        | PitchBook + Perplexity MCP                    |
| Factual claim verification against primary sources |        |  ✓  |        | Web search with source citations              |
| Systematic data room cross-referencing             |   ✓    |     |        | 1M context, self-verification                 |

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

| Capability                                     | Can Do | WIP | Cannot | Enabler                                |
| ---------------------------------------------- | :----: | :-: | :----: | -------------------------------------- |
| Burn rate and runway analysis                  |   ✓    |     |        | Python tool use                        |
| 3-statement model generation (P&L, BS, CF)     |   ✓    |     |        | Python tool use, self-verification     |
| Unit economics computation (LTV, CAC, payback) |   ✓    |     |        | Python tool use, self-verification     |
| Revenue projections (3-5 year forward)         |   ✓    |     |        | Python tool use, self-verification     |
| KPI auto-detection and health assessment       |   ✓    |     |        | Extended thinking, self-verification   |
| Cohort and retention curve analysis            |        |  ✓  |        | Analytics MCPs, Python tool use        |
| Bulk portfolio-wide financial analysis         |        |  ✓  |        | ChatFin, Chronograph, 1M context       |
| Audit-grade financial statements               |        |     |   ✓    | Needs formal verification, licensing   |

### Valuation

| Capability                                     | Can Do | WIP | Cannot | Enabler                                         |
| ---------------------------------------------- | :----: | :-: | :----: | ----------------------------------------------- |
| Pre/post-money round modeling                  |   ✓    |     |        | Carta, Pulley, Python tool use                  |
| Multiples-based valuation with industry ranges |   ✓    |     |        | Python tool use, web search                     |
| DCF analysis from user-provided assumptions    |   ✓    |     |        | Python tool use, self-verification              |
| Comparable company analysis with live data     |   ✓    |     |        | PitchBook + Perplexity MCP                      |
| Precedent transaction analysis                 |   ✓    |     |        | Grata, PitchBook + Perplexity MCP               |
| Conviction weighting on valuation outputs      |        |     |   ✓    | Needs calibrated confidence, human judgment     |

### Deal Structuring & Negotiation

| Capability                                         | Can Do | WIP | Cannot | Enabler                                    |
| -------------------------------------------------- | :----: | :-: | :----: | ------------------------------------------ |
| Cap table modeling and dilution analysis           |   ✓    |     |        | Carta, Pulley, Python tool use             |
| SAFE and convertible note conversion               |   ✓    |     |        | Carta, Pulley, OCF standard                |
| Multi-series liquidation waterfall                 |   ✓    |     |        | Carta, Pulley, Eqvista                     |
| Exit scenario modeling at multiple valuations      |   ✓    |     |        | Cap table platforms, Python tool use       |
| Term sheet red-flag identification (NVCA baseline) |   ✓    |     |        | Spellbook (10M+ contracts reviewed)        |
| Cap table platform sync (Carta, Pulley) via MCP    |        |  ✓  |        | Cap table platform MCPs                    |
| Negotiation strategy and counter-offer structuring |        |     |   ✓    | Needs relationship context, game theory    |
| Binding legal document generation                  |        |     |   ✓    | Needs legal licensing, formal verification |

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

| Capability                                        | Can Do | WIP | Cannot | Enabler                                    |
| ------------------------------------------------- | :----: | :-: | :----: | ------------------------------------------ |
| Common provision pattern flagging                 |   ✓    |     |        | Spellbook, Luminance                       |
| NVCA baseline term comparison                     |   ✓    |     |        | Spellbook VC clause library                |
| Contract review (SHA, IP assignments, employment) |        |  ✓  |        | Luminance, Kira/Litera (64% Am Law 100)    |
| Regulatory compliance analysis                    |        |  ✓  |        | Emerging legal AI tools                    |
| Legal opinions and formal advice                  |        |     |   ✓    | Needs legal licensing                      |
| Cross-jurisdiction tax and structuring            |        |     |   ✓    | Needs tax law MCPs, licensed professionals |

### Financial Due Diligence

| Capability                                  | Can Do | WIP | Cannot | Enabler                                    |
| ------------------------------------------- | :----: | :-: | :----: | ------------------------------------------ |
| Individual financial document analysis      |   ✓    |     |        | Hebbia Matrix, PDF vision                  |
| Private company financial data              |   ✓    |     |        | PitchBook, Morningstar, Grata              |
| Financial model internal consistency checks |   ✓    |     |        | Python tool use, self-verification         |
| Portfolio company data connectivity         |        |  ✓  |        | Standard Metrics, Chronograph MCPs         |
| Data room systematic cross-referencing      |   ✓    |     |        | 1M context, self-verification              |
| Historical financials verification          |        |     |   ✓    | Needs SEC EDGAR MCP, audit trail access    |
| Tax and transfer pricing analysis           |        |     |   ✓    | Needs tax law MCPs, licensed professionals |

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

Track when capabilities cross the frontier — things that became feasible, and
things we discovered AI still can't do. Dates reflect when the enabling product
or feature shipped, not when adoption reached maturity.

| Date    | Change                                        | Capability affected                            | Direction       | Enabler                              |
| ------- | --------------------------------------------- | ---------------------------------------------- | --------------- | ------------------------------------ |
| 2022-09 | AI contract drafting and review               | Common provision pattern flagging              | Human -> WIP    | Spellbook launch                     |
| 2022-11 | AI-powered deal sourcing signals              | New investment opportunity identification      | Human -> WIP    | Harmonic Series A, early product     |
| 2022-11 | Basic memo drafting and market summaries      | Investment memo generation                     | Human -> WIP    | ChatGPT (GPT-3.5)                    |
| 2023-03 | Professional-grade investment analysis        | Industry landscape synthesis                   | WIP -> Can Do   | GPT-4 reasoning quality              |
| 2023-06 | Structured API tool calling for data access   | KPI benchmarking, financial model checks       | Human -> WIP    | OpenAI function calling              |
| 2023-07 | Full document analysis (100K context)         | Pitch deck data extraction                     | Human -> Can Do | Claude 2                             |
| 2023-09 | AI relationship intelligence in CRM           | Founder relationship tracking                  | Human -> WIP    | Affinity AI features                 |
| 2023-11 | Reliable structured data extraction           | KPI benchmarking, deal screening               | WIP -> Can Do   | GPT-4 Turbo, JSON mode, 128K context |
| 2024-03 | Pitch deck and chart visual analysis          | Pitch deck data extraction, product claims     | Human -> Can Do | Claude 3 vision + 200K context       |
| 2024-05 | AI-orchestrated multi-tool workflows          | Deal screening, financial model generation     | Human -> WIP    | Claude tool use GA                   |
| 2024-06 | Cost-effective AI analysis at pipeline scale  | Inbound pitch triage                           | WIP -> Can Do   | Claude 3.5 Sonnet                    |
| 2024-08 | Perfect structured extraction (100% schema)   | KPI benchmarking, financial model checks       | WIP -> Can Do   | OpenAI structured outputs            |
| 2024-09 | Native PDF document processing                | Pitch deck data extraction, document analysis  | Human -> Can Do | Claude PDF support                   |
| 2024-10 | Computer-use automation for legacy tools      | Technical architecture assessment              | Human -> WIP    | Claude computer use beta             |
| 2024-10 | Multi-agent due diligence workflows           | Systematic data room cross-referencing         | Human -> WIP    | CrewAI maturity, AutoGen             |
| 2024-11 | Natural-language private company data queries | Private company data access                    | Human -> WIP    | PitchBook Navigator + OpenAI         |
| 2024-11 | Standardized AI-to-data connectivity          | Portfolio company data connectivity            | Human -> WIP    | MCP (Model Context Protocol)         |
| 2025-02 | Deep financial reasoning on demand            | 3-statement model generation, DCF analysis     | Human -> WIP    | Extended thinking (Claude 3.7)       |
| 2025-02 | Agentic coding for custom VC tools            | Unit economics computation, burn rate analysis | Human -> WIP    | Claude Code research preview         |
| 2025-03 | Real-time market intelligence in AI           | Sector trend analysis, competitive mapping     | Human -> Can Do | Claude web search                    |
| 2025-05 | Production-grade agentic VC tooling           | Report generation, exit scenario modeling      | WIP -> Can Do   | Claude Code GA                       |
| 2025-09 | End-to-end document production                | Report generation (DOCX), board deck prep      | Human -> Can Do | Native file generation               |
| 2025-11 | AI-accessible private market data at scale    | Private company data access                    | WIP -> Can Do   | PitchBook Navigator MCP              |
| 2026-02 | Full data room in single context              | Systematic data room cross-referencing         | Human -> Can Do | 1M token context (Claude 4.6)        |
| 2026-03 | PitchBook data in conversational AI           | Comparable company analysis, precedent txns    | WIP -> Can Do   | PitchBook + Perplexity MCP           |
| 2026-03 | Fund-level return metric calculations         | IRR, MOIC, DPI, TVPI, PME computation          | Human -> Can Do | claude-vc v1.5.0 returns command     |
| 2026-03 | XLSX export for financial outputs             | Spreadsheet generation for cap tables, models  | Human -> Can Do | Native file generation + skill flags |
| 2026-03 | claude-vc v1.2.0 baseline                     | --                                             | --              | Initial AI Frontier assessment       |
| 2026-03 | Parallel multi-agent deal screening           | Full screening with 6 concurrent agents        | WIP -> Can Do   | claude-vc v1.3.0 parallel agents     |
| 2026-03 | Side-by-side company comparison               | Structured comparison of 2-4 companies         | WIP -> Can Do   | claude-vc v1.3.0 vc-compare          |
| 2026-03 | Customizable due diligence checklists         | Stage+sector-specific DD checklist generation  | Cannot -> Can Do | claude-vc v1.3.0 vc-diligence        |
| 2026-03 | One-shot portfolio reporting for LPs          | LP-ready portfolio summary from provided data  | Cannot -> Can Do | claude-vc v1.3.0 vc-portfolio        |
| 2026-04 | Single-skill consolidation (6 sub-commands)   | Organizational change — no capability shift    | --              | claude-vc v2.0.0 consolidation       |
| 2026-04 | Self-verified financial analysis (Opus 4.7)   | 3-stmt model, unit econ, DCF, consistency      | WIP -> Can Do   | Claude Opus 4.7 self-verification    |
| 2026-04 | Opus 4.7 improved reasoning (GPQA 94.2%)      | KPI auto-detection and health assessment       | WIP -> Can Do   | Claude Opus 4.7 extended thinking    |
| 2026-04 | Opus 4.7 3.75MP vision (3x prior resolution)  | High-res document and diagram analysis         | --              | Claude Opus 4.7 vision upgrade       |
| 2026-04 | GPT-5.4 reaches 1.05M token context window    | Full data room in single context (non-Claude)  | --              | GPT-5.4 (OpenAI)                     |
| 2026-04 | Resolve table/changelog inconsistencies       | Comps, precedent txns, data room, rev proj     | WIP -> Can Do   | See changelog 2026-02 and 2026-03    |
| 2026-04 | Multiples valuation (simpler than DCF)        | Multiples-based valuation with industry ranges | WIP -> Can Do   | Python tool use, web search          |

---

[^1]:
    **Enabler** = the AI product, feature, or integration that made (or would
    make) this capability possible. Common enablers: _extended thinking_
    (chain-of-thought reasoning), _Python tool use_ (script execution for
    verified calculations), _web search_ (real-time public information),
    _PDF vision_ (multimodal document understanding), _MCP_ (Model Context
    Protocol server integrations), _native file generation_ (DOCX/XLSX/PPTX
    output), _1M context_ (full data room ingestion), _structured output_
    (reliable JSON schema adherence), _self-verification_ (model checks its
    own outputs before reporting back). Product names (Harmonic, PitchBook,
    Spellbook, etc.) refer to best-in-class commercial tools.
