# Claude-VC

A Claude Code skill ecosystem for venture capital workflows. Deal screening, investment memo generation, cap table modeling, term sheet analysis, and portfolio monitoring -- all from your terminal.

## What Is This?

Claude-VC is a set of [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills) that extend Claude with VC-specific domain knowledge and computational tools. It follows the [orchestrator + sub-skills pattern](docs/decisions/001-skill-architecture.md) proven by [claude-seo](https://github.com/AgriciDaniel/claude-seo).

It is **not** a standalone app or MCP server. It installs into `~/.claude/` and is invoked via `/vc` slash commands inside Claude Code.

## Commands

| Command            | Description                                            |
| ------------------ | ------------------------------------------------------ |
| `/vc screen <url>` | Screen a startup from URL or pitch deck                |
| `/vc memo`         | Generate a structured investment memo                  |
| `/vc terms <file>` | Analyze a term sheet, SAFE, or convertible note        |
| `/vc captable`     | Model cap table, dilution, and waterfall distributions |
| `/vc diligence`    | Generate a due diligence checklist                     |
| `/vc portfolio`    | Aggregate portfolio updates and KPIs                   |

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/yugui923/claude-vc/main/install.sh | bash
```

Or clone and install manually:

```bash
git clone https://github.com/yugui923/claude-vc.git
cd claude-vc
./install.sh
```

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- Python 3.13+ (for computation scripts)
- Git

### Optional Extensions

Enrich analysis with external data sources:

```bash
# SEC EDGAR (free, no API key needed)
./extensions/sec-edgar/install.sh

# Crunchbase (free tier, requires API key)
./extensions/crunchbase/install.sh
```

## How It Works

### Quick Screen

```
/vc screen https://example-startup.com
```

Claude fetches the company website, analyzes it against a [configurable scoring framework](docs/specs/skill-system.md#investment-criteriamd-target-100-lines), and produces a Deal Score (0-100) with a Pass / Further Diligence / Strong Interest recommendation.

### Full Screen

```
/vc screen https://example-startup.com --full
```

Spawns 6 parallel subagents (financial, market, technical, legal, competitive, team) for comprehensive analysis. Results are aggregated into a detailed investment memo.

### Cap Table Modeling

```
/vc captable
```

Interactively build or import a cap table. Model new rounds, SAFE conversions, option pool expansion, and waterfall distributions at various exit valuations. Math runs in Python for precision.

### Term Sheet Analysis

```
/vc terms /path/to/term-sheet.pdf
```

Compares each provision against NVCA model terms and current market standards. Flags non-standard or unusual provisions with severity ratings.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system design.

```
claude-vc/
├── vc/                     # Orchestrator skill + reference files
├── skills/                 # 6 sub-skills (screen, memo, terms, ...)
├── agents/                 # 6 parallel subagents (financial, market, ...)
├── scripts/                # Python computation (cap table, DCF, ...)
├── extensions/             # Optional data source integrations
└── docs/                   # ADRs, specs, roadmap
```

Key design patterns:

- **Orchestrator + sub-skills**: One router delegates to specialized workflows
- **Parallel subagents**: Full screenings run 6 analysts concurrently
- **Progressive disclosure**: Only load domain knowledge when needed
- **Python for math**: Financial calculations run in scripts, not LLM reasoning
- **Extension system**: External data sources are optional add-ons

## Disclaimer

This tool is for **informational and educational purposes only**. It does not constitute investment advice, a recommendation to buy or sell securities, or an offer to invest. All financial projections and valuations are estimates based on limited information. Consult a qualified financial advisor and legal counsel before making any investment decisions. The creators of this tool are not registered as investment advisers, broker-dealers, or exempt market dealers in any jurisdiction.

See [ADR-003](docs/decisions/003-regulatory-disclaimers.md) for the full regulatory compliance framework.

## License

[MIT](LICENSE)
