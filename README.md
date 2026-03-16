# Claude-VC

A plugin for venture capital workflows — inside Claude Cowork and Claude Code.

## Quick Start

Install the plugin:

```bash
# Claude Code (CLI)
claude plugin marketplace add yugui923/claude-vc
claude plugin install claude-vc@claude-vc

# Claude Cowork (desktop): Cowork > Customize > Browse plugins >
# Personal tab > Add marketplace from GitHub > yugui923/claude-vc
```

Then point it at a company:

```text
/vc https://example-startup.com
```

That's it. Claude will screen the company, generate an investment memo, and
produce a due diligence checklist — all in one shot. It works with URLs,
pitch deck PDFs, or just a description you type in.

For detailed usage of every command, see the **[User Guide](docs/user-guide.md)**.

## What It Does

`/vc` chains together deal screening, memo writing, and diligence
automatically. You can also run each step individually:

| Command | What It Does |
| --- | --- |
| `/vc screen` | Score a startup 0-100 across market, team, product, financials, timing |
| `/vc memo` | Write a 12-section investment memo |
| `/vc terms` | Red-flag non-standard provisions in a term sheet, SAFE, or note |
| `/vc captable` | Model ownership, dilution, SAFE conversion, liquidation waterfall |
| `/vc model` | Build a 3-statement financial model |
| `/vc kpi` | Generate KPI reports with benchmarks (auto-detects SaaS, marketplace, fintech, consumer) |
| `/vc compare` | Side-by-side comparison of 2-4 companies |
| `/vc diligence` | Stage- and sector-customized due diligence checklist |
| `/vc portfolio` | LP-ready portfolio report from your company data |

Each command is documented in detail in the **[User Guide](docs/user-guide.md)**.

## Installation

### Updating

**Cowork**: Updates appear automatically. **Claude Code**: `/plugin marketplace update`.

### Alternative Install (shell script)

```bash
curl -fsSL https://raw.githubusercontent.com/yugui923/claude-vc/main/install.sh | bash
```

### Team Setup

Auto-install for your org by adding to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "claude-vc": {
      "source": { "source": "github", "repo": "yugui923/claude-vc" }
    }
  },
  "enabledPlugins": { "claude-vc@claude-vc": true }
}
```

### Requirements

- Python 3.10+
- [Claude Cowork](https://claude.com/download) or [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (Pro, Max, Team, or Enterprise)

### Optional Extensions

```bash
./extensions/octagon/install.sh    # Private company data ($17/mo)
./extensions/sec-edgar/install.sh  # Public filings (free)
```

## More

- **[User Guide](docs/user-guide.md)** — detailed usage for every command
- **[AI Frontier](docs/frontier.md)** — what AI can and cannot do in VC today
- **[Contributing](CONTRIBUTING.md)** — dev setup, adding skills, PR process
- **[Architecture](ARCHITECTURE.md)** — system design and patterns
- **[Roadmap](docs/roadmap.md)** — what's planned next

## Disclaimer

This tool is for **informational and educational purposes only**. It does not
constitute investment advice. See [ADR-003](docs/decisions/003-regulatory-disclaimers.md)
for the full regulatory compliance framework.

## License

[MIT](LICENSE)
