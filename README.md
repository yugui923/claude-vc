# Claude-VC

A plugin for venture capital workflows. Deal screening, investment memo generation, cap table modeling, term sheet analysis, financial modeling, KPI reporting, and portfolio monitoring -- inside Claude Code and Claude Cowork.

## Quick Start

### Claude Cowork (desktop app)

1. Open the Claude desktop app and go to the **Cowork** tab
2. Click **Customize** in the left sidebar, then **Browse plugins**
3. Click **Upload plugin** and paste the GitHub repo URL:
   ```
   https://github.com/yugui923/claude-vc
   ```
4. Click **Install**

Once installed, type `/` or click **+** to see available skills. Use `/vc screen`, `/vc memo`, `/vc captable`, and more.

### Claude Code (CLI)

```bash
claude plugin marketplace add yugui923/claude-vc
claude plugin install claude-vc@claude-vc
```

Then use `/vc` commands in your Claude Code session.

### Claude Code (IDE -- VS Code, JetBrains)

Run these in the Claude Code panel input:

```text
/plugin marketplace add yugui923/claude-vc
/plugin install claude-vc@claude-vc
```

## What Is This?

Claude-VC is a [Claude plugin](https://code.claude.com/docs/en/plugins) that extends Claude with VC-specific domain knowledge and computational tools. It follows the [orchestrator + sub-skills pattern](docs/decisions/001-skill-architecture.md) proven by [claude-seo](https://github.com/AgriciDaniel/claude-seo).

It is **not** a standalone app or MCP server. It bundles skills, agents, and Python computation scripts into a plugin that works across Claude Cowork and Claude Code.

## Commands

| Command            | Description                                            |
| ------------------ | ------------------------------------------------------ |
| `/vc screen <url>` | Screen a startup from URL or pitch deck                |
| `/vc memo`         | Generate a structured investment memo                  |
| `/vc terms <file>` | Analyze a term sheet, SAFE, or convertible note        |
| `/vc captable`     | Model cap table, dilution, and waterfall distributions |
| `/vc model`        | Generate a simplified 3-statement financial model      |
| `/vc kpi`          | Generate KPI reports with benchmarks and health scores |
| `/vc compare`      | Side-by-side company comparison                        |
| `/vc diligence`    | Generate a due diligence checklist                     |
| `/vc portfolio`    | Generate portfolio reports from provided data          |

## Installation Details

### Updating

**Cowork**: Plugin updates appear automatically in the Customize panel.

**Claude Code**: Run `/plugin marketplace update` or enable auto-updates in the `/plugin` Marketplaces tab.

### Shell Script (alternative for CLI)

If you prefer a manual install without the plugin marketplace:

```bash
curl -fsSL https://raw.githubusercontent.com/yugui923/claude-vc/main/install.sh | bash
```

Or clone and install manually:

```bash
git clone https://github.com/yugui923/claude-vc.git
cd claude-vc
./install.sh
```

To update: run `./update.sh` from the cloned repo.

### Team Setup (auto-install for your org)

Add claude-vc to your project's `.claude/settings.json` so team members are automatically prompted to install it when they open the project:

```json
{
  "extraKnownMarketplaces": {
    "claude-vc": {
      "source": {
        "source": "github",
        "repo": "yugui923/claude-vc"
      }
    }
  },
  "enabledPlugins": {
    "claude-vc@claude-vc": true
  }
}
```

### Requirements

- Python 3.13+ (for financial computation scripts)
- One of:
  - [Claude desktop app](https://claude.com/download) with Cowork (Pro, Max, Team, or Enterprise plan)
  - [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI or IDE extension

### Optional Extensions

Enrich analysis with external data sources:

```bash
# Octagon AI (recommended, $17/mo -- private companies, funding, investors)
./extensions/octagon/install.sh

# SEC EDGAR (free, no API key needed -- raw public filings)
./extensions/sec-edgar/install.sh
```

## How It Works

### Quick Screen

```text
/vc screen https://example-startup.com
```

Claude fetches the company website, analyzes it against a [configurable scoring framework](docs/specs/skill-system.md#investment-criteriamd-target-100-lines), and produces a Deal Score (0-100) with a Pass / Further Diligence / Strong Interest recommendation.

Also works with pitch deck PDFs -- Claude reads them natively:

```text
/vc screen /path/to/pitch-deck.pdf
```

### Full Screen

```text
/vc screen https://example-startup.com --full
```

Spawns 6 parallel subagents (financial, market, technical, legal, competitive, team) for comprehensive analysis. Results are aggregated into a detailed investment memo.

### Compare Companies

```text
/vc compare https://company-a.com https://company-b.com
```

Spawns parallel agents to analyze each company independently, then generates a side-by-side comparison matrix across all investment dimensions.

### Cap Table Modeling

```text
/vc captable
```

Interactively build or import a cap table. Model new rounds, SAFE conversions, option pool expansion, and waterfall distributions at various exit valuations. Math runs in Python for precision.

### Term Sheet Analysis

```text
/vc terms /path/to/term-sheet.pdf
```

Compares each provision against NVCA model terms and current market standards. Flags non-standard or unusual provisions with severity ratings.

### Financial Model

```text
/vc model
```

Generate a simplified 3-statement financial model (income statement, balance sheet, cash flow) from pitch deck data, company financials, or verbal assumptions. Projects 3-5 years forward with stage-appropriate defaults. Supports bull/base/bear scenario comparison.

### KPI Report

```text
/vc kpi
```

Generate a KPI report from company data. Auto-detects company type (SaaS, marketplace, consumer, fintech) and calculates relevant metrics with industry benchmarks and health assessments (Healthy / Watch / Concerning).

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system design.

```text
claude-vc/
├── skills/
│   ├── vc/                 # Orchestrator skill + references + Python scripts
│   ├── vc-screen/          # Sub-skills (screen, memo, terms, captable, model, kpi, ...)
│   └── ...
├── agents/                 # 6 parallel subagents (financial, market, ...)
├── .claude-plugin/         # Plugin manifest + marketplace metadata
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
