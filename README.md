# Claude-VC

Your AI-powered venture capital analyst — right inside Claude.

Claude-VC adds VC-specific tools to Claude: deal screening, investment memos,
cap table math, term sheet red-flags, financial models, KPI dashboards, and
portfolio reports. No spreadsheets, no switching tabs — just ask Claude.

## Get Started in 60 Seconds

### If you use the Claude desktop app (Cowork)

1. Open Claude and go to the **Cowork** tab
2. Click **Customize** in the left sidebar, then **Browse plugins**
3. Go to the **Personal** tab and click **Add marketplace from GitHub**
4. Paste this URL: `https://github.com/yugui923/claude-vc`
5. Make sure the plugin is **enabled**

### If you use Claude Code (terminal or VS Code / JetBrains)

Run these two commands:

```
claude plugin marketplace add yugui923/claude-vc
claude plugin install claude-vc@claude-vc
```

### Try it

Once installed, type this into Claude:

```
/vc https://example-startup.com
```

Claude will automatically screen the company, write an investment memo, and
generate a due diligence checklist. You can also give it a pitch deck PDF or
just describe a company in your own words:

```
/vc /path/to/pitch-deck.pdf
/vc "B2B SaaS company doing $5M ARR in the developer tools space"
```

That's the `/vc` command — it chains everything together. For more control,
you can run each step individually (see below).

## What You Can Do

| Command | What It Does |
| --- | --- |
| `/vc` | The all-in-one command — screens, writes a memo, and creates a diligence checklist |
| `/vc screen` | Scores a startup 0-100 across market, team, product, financials, and timing |
| `/vc memo` | Writes a structured investment memo (the kind you'd present to an IC) |
| `/vc terms` | Reviews a term sheet or SAFE and flags anything non-standard |
| `/vc captable` | Models ownership, dilution, and who gets what at exit |
| `/vc model` | Builds a financial model (income statement, balance sheet, cash flow) |
| `/vc kpi` | Creates a KPI dashboard with industry benchmarks |
| `/vc compare` | Compares 2-4 companies side by side |
| `/vc diligence` | Generates a due diligence checklist tailored to the company's stage and sector |
| `/vc portfolio` | Creates a portfolio report for LP updates |

Every command is explained in detail in the **[User Guide](docs/user-guide.md)**.

## Updating

- **Claude desktop app**: updates appear automatically in the Customize panel
- **Claude Code**: run `/plugin marketplace update`

## Requirements

- **Claude Pro, Max, Team, or Enterprise** subscription
- **Python 3.10 or newer** (used behind the scenes for financial calculations)

You don't need to install Python packages or manage dependencies — the plugin
handles that automatically.

## Optional: External Data Sources

Want richer analysis? These optional add-ons pull in real company data:

```
./extensions/octagon/install.sh    # Private company data ($17/mo)
./extensions/sec-edgar/install.sh  # SEC public filings (free)
```

## Team Setup

If you want everyone on your team to have Claude-VC automatically, add this
to your project's `.claude/settings.json`:

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

## Learn More

- **[User Guide](docs/user-guide.md)** — detailed docs for every command
- **[AI Frontier](docs/frontier.md)** — what AI can and cannot do in VC today
- **[Contributing](CONTRIBUTING.md)** — how to contribute (for developers)
- **[Roadmap](docs/roadmap.md)** — what's coming next

## Disclaimer

This tool is for **informational and educational purposes only**. It does not
constitute investment advice, a recommendation to buy or sell any securities,
or an offer to invest. Always consult a qualified financial advisor and legal
counsel before making investment decisions.

## License

[MIT](LICENSE)
