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

Or install via the [Agent Skills](https://agentskills.io) CLI:

```
npx skills add yugui923/claude-vc
```

### Try it

Once installed, type this into Claude:

```
/vc https://stripe.com
```

Claude will automatically screen the company and write an investment memo
(the memo already includes a tailored due diligence checklist). You can also
give it a pitch deck PDF or describe a company in your own words:

```
/vc /path/to/pitch-deck.pdf
/vc "B2B SaaS company doing $5M ARR in the developer tools space"
```

That's the `/vc` command — it chains everything together. For more control,
use one of the six sub-commands below.

## What You Can Do

Six commands cover the full VC workflow, organized by what you're doing:

| Command | What It Does |
| --- | --- |
| `/vc` | All-in-one — screens and writes a memo (with DD checklist built in) |
| `/vc screen <input(s)>` | Score one startup 0-100, or compare 2-4 side by side. `--full` spawns 6 specialist agents. |
| `/vc memo <input>` | Write a structured investment memo with DD checklist. `--diligence-only` emits just the checklist. |
| `/vc terms <file>` | Review a term sheet, SAFE, or convertible note and flag anything non-standard |
| `/vc captable <input>` | Model ownership, dilution, waterfall payouts, and exit scenarios |
| `/vc model <input>` | Build a 3-statement financial model with 3-5 year projections |
| `/vc portfolio <data>` | Portfolio report by default. `--kpi` for a single-company dashboard, `--returns` for IRR/MOIC/DPI/TVPI/PME. |

Type `/vc help` in Claude for the full argument reference, or see the
**[User Guide](docs/user-guide.md)** for detailed usage of each command.

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

## Disclaimer

This tool is for **informational and educational purposes only**. It does not
constitute investment advice, a recommendation to buy or sell any securities,
or an offer to invest. Always consult a qualified financial advisor and legal
counsel before making investment decisions.

## License

[MIT](LICENSE)
