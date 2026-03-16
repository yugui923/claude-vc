# Claude-VC Roadmap

> High-level development priorities. Update when priorities shift.

## Phase 1: Foundation (MVP)

Goal: Core skill infrastructure and two highest-impact workflows.

### Deliverables

- [x] Orchestrator (`vc/SKILL.md`) with routing table and progressive disclosure
- [x] Deal screening sub-skill (`vc-screen/SKILL.md`) -- quick screen mode (URL + pitch deck PDF)
- [x] Investment memo sub-skill (`vc-memo/SKILL.md`)
- [x] Reference files: `investment-criteria.md`, `valuation-methods.md`
- [x] Reference file: `disclaimers.md` (regulatory compliance)
- [x] `install.sh` and `uninstall.sh`
- [x] `.claude-plugin/plugin.json` manifest
- [x] README with installation and usage instructions

### Success Criteria

- `/vc screen <url>` and `/vc screen <file.pdf>` produce a scored Deal Score with recommendation
- `/vc memo` generates a structured 10-section investment memo
- Install script works on macOS and Linux
- All outputs include regulatory disclaimers

## Phase 2: Financial Tools

Goal: Cap table modeling and term sheet analysis -- the two workflows with no good existing AI tool.

### Deliverables

- [x] Cap table sub-skill (`vc-captable/SKILL.md`)
- [x] `scripts/captable.py` -- ownership, dilution, waterfall calculations
- [x] Term sheet analysis sub-skill (`vc-terms/SKILL.md`)
- [x] Reference files: `term-sheet-terms.md`, `safe-mechanics.md`
- [x] `scripts/financial_model.py` -- DCF, unit economics, projections
- [x] Reference file: `industry-multiples.md`
- [x] Financial model sub-skill (`vc-model/SKILL.md`) -- 3-statement model generation
- [x] KPI reporting sub-skill (`vc-kpi/SKILL.md`) -- auto-detect company type, benchmark KPIs
- [x] OCF-informed `captable.py` rewrite -- stock classes, multi-series waterfall, MFN SAFEs, compound interest, scenarios command
- [x] `financial_model.py` `three_statement` command -- income statement, balance sheet, cash flow with internal consistency
- [x] Removed `memo_to_docx.py` -- Claude generates DOCX natively
- [x] Updated `vc-memo/SKILL.md` to use Claude's native DOCX generation

### Success Criteria

- `/vc captable` correctly models SAFE conversions and multi-round dilution
- `/vc captable` supports multi-series liquidation waterfall with seniority ordering
- `/vc captable` resolves MFN SAFEs and supports compound interest on notes
- `/vc terms` identifies non-standard provisions against NVCA baseline
- `/vc model` generates internally consistent 3-statement model (A=L+E, cash flows match)
- `/vc kpi` auto-detects company type and benchmarks metrics with health assessment
- Python scripts produce verified-correct financial calculations
- All cap table math validated against manual spreadsheet calculations
- Python scripts pass ruff check and ruff format

## Phase 3: Parallel Agents and Full Screening

Goal: Concurrent subagent analysis for comprehensive deal evaluation.

### Deliverables

- [x] 6 parallel subagents: `vc-financial`, `vc-market`, `vc-technical`, `vc-legal`, `vc-competitive`, `vc-team`
- [x] Full screening mode (`/vc screen --full`) with parallel orchestration
- [x] Company comparison sub-skill (`vc-compare/SKILL.md`) -- parallel per-company agents
- [x] Aggregated Deal Score with dimension breakdown
- [x] Due diligence sub-skill (`vc-diligence/SKILL.md`)
- [x] Reference file: `due-diligence-checklist.md`

### Success Criteria

- 6 agents execute concurrently and return structured results
- Full screening produces comprehensive investment memo
- `/vc compare` generates side-by-side matrix for 2-4 companies
- DD checklist customizable by stage and sector

## Phase 4: Portfolio and Extensions

Goal: Portfolio monitoring and external data integration.

### Deliverables

- [ ] Portfolio reporting sub-skill (`vc-portfolio/SKILL.md`) -- one-shot report generation, not continuous monitoring
- [ ] Octagon AI extension (`extensions/octagon/`) -- priority data source ($17/mo, 3M+ companies, 500K+ deals, investor profiles)
- [ ] SEC EDGAR extension (`extensions/sec-edgar/`) -- free raw filing access
- [ ] `scripts/fetch_company.py` for data normalization
- [ ] `npx skills` distribution support
- [ ] Windows installer (`install.ps1`)

### Success Criteria

- `/vc portfolio` generates LP-ready summary from provided company data
- Octagon AI extension provides private company data, funding rounds, and investor profiles
- SEC EDGAR extension provides raw filing text access
- Installable via `npx skills add` for cross-agent compatibility

## Phase 5: Polish and Community

Goal: Production quality, documentation, and community readiness.

### Deliverables

- [ ] Comprehensive test suite for Python scripts
- [ ] User guide and workflow tutorials
- [ ] Video demos
- [ ] Contributing guide
- [x] Plugin marketplace submission
- [ ] Community feedback integration

## Future Considerations

Items not currently planned but worth tracking:

- **OCF import/export**: Full Open Cap Table Format JSON import and export for interoperability with cap table management tools
- **Vesting schedule modeling**: DAG-based vesting with cliff, acceleration, and milestone triggers (informed by OCF VestingTerms)
- **Fund modeling**: LP/GP economics, management fees, carry calculations
- **PitchBook extension**: Premium data source integration
- **Multi-language**: Localization for non-English markets
- **Custom scoring models**: ML-trained scoring on user's historical deals

## Explicitly Out of Scope

These belong in a proper application using the Claude API, not a CLI skill:

- CRM/pipeline tracking (needs persistent state, OAuth, database)
- Portfolio monitoring dashboards (needs a UI runtime)
- Scheduled/automated data pulls (needs a cron process)
- Large dataset processing (context window limits)
- Real-time deal flow alerts (needs push notifications)
- Multi-user collaboration features

See [ADR-004](decisions/004-scope-boundaries.md) for rationale.
