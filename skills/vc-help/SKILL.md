---
name: vc-help
description: Show available /vc commands and usage examples.
---

# Help

Display the following help text and ask the user what they'd like to do.

```
Claude-VC — venture capital analysis toolkit

Usage:
  /vc <url or file>          Screen → Memo → Diligence (the full workflow)
  /vc <command> [args]       Run a specific command

Commands:
  screen <url or file>       Score a startup 0-100 across five dimensions
  memo                       Write a structured investment memo
  terms <file>               Review a term sheet or SAFE for red flags
  captable                   Model ownership, dilution, and exit waterfalls
  model                      Build a 3-statement financial model
  kpi                        Generate a KPI dashboard with benchmarks
  compare <url1> <url2>      Compare 2-4 companies side by side
  diligence                  Generate a due diligence checklist
  portfolio                  Create an LP-ready portfolio report
  returns                    Calculate fund return metrics (IRR, MOIC, etc.)
  help                       Show this help message

Examples:
  /vc https://example.com
  /vc /path/to/pitch-deck.pdf
  /vc screen https://example.com --full
  /vc memo
  /vc terms /path/to/term-sheet.pdf
  /vc kpi
```
