# Testing Strategy

Claude-VC uses a two-layer testing strategy that separates fast, deterministic
script tests from slower skill-level integration tests.

## Layer 1: Script Unit & Integration Tests

**Location:** `tests/layer1/`
**Run:** `uv run pytest` (default, runs automatically)
**Requirements:** Python 3.10+, dev dependencies (`uv sync`)

Layer 1 tests exercise the Python scripts (`captable.py`, `financial_model.py`)
directly — both by importing functions and by running the CLI as a subprocess.
They require no API keys, no network access, and no Claude CLI.

### What Layer 1 covers

| Test file                           | Script               | Command           | Tests                                                                                                                                         |
| ----------------------------------- | -------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `test_captable_helpers.py`          | `captable.py`        | —                 | `_d()`, `_fmt()`, `_calc_accrued_interest()`, `_parse_stock_classes()`, `_parse_safe_terms()`, `_parse_note_terms()`, `_get_capitalization()` |
| `test_captable_model.py`            | `captable.py`        | `model`           | Founders-only, SAFEs (post/pre-money), MFN resolution, notes with interest, full stack                                                        |
| `test_captable_dilution.py`         | `captable.py`        | `dilution`        | Dilution percentages, share counts, price per share                                                                                           |
| `test_captable_waterfall.py`        | `captable.py`        | `waterfall`       | Non-participating preferred, multi-series seniority, participating with cap, zero exit                                                        |
| `test_captable_convert.py`          | `captable.py`        | `convert`         | SAFE cap-vs-discount, note compound interest, resulting cap table                                                                             |
| `test_captable_scenarios.py`        | `captable.py`        | `scenarios`       | Multiple exit values, preference-vs-conversion crossover                                                                                      |
| `test_captable_cli.py`              | `captable.py`        | all               | CLI JSON output validity, error handling (missing flags, bad JSON, unknown commands)                                                          |
| `test_financial_helpers.py`         | `financial_model.py` | —                 | `_d()`, `_fmt()`                                                                                                                              |
| `test_financial_dcf.py`             | `financial_model.py` | `dcf`             | Gordon growth, exit multiple, error cases                                                                                                     |
| `test_financial_unit_economics.py`  | `financial_model.py` | `unit_economics`  | ARPU, CAC, LTV/CAC, Rule of 40, NRR                                                                                                           |
| `test_financial_projections.py`     | `financial_model.py` | `projections`     | Revenue growth, break-even, runway                                                                                                            |
| `test_financial_multiples.py`       | `financial_model.py` | `multiples`       | EV/Revenue, EV/ARR, adjustments, valuation range                                                                                              |
| `test_financial_three_statement.py` | `financial_model.py` | `three_statement` | A=L+E consistency, cash flow linkage, net income flow, equity injections                                                                      |
| `test_financial_cli.py`             | `financial_model.py` | all               | CLI JSON output validity, error handling                                                                                                      |

### Key invariants tested

- **Ownership sums to 100%** — every cap table model test verifies this
- **Payouts sum to exit value** — every waterfall test verifies this
- **A = L + E** — every 3-statement test verifies balance sheet identity
- **Net income flows correctly** — income statement net income matches cash flow statement
- **Ending cash matches** — cash flow ending cash equals balance sheet cash

### Running Layer 1

```bash
# All Layer 1 tests (default)
uv run pytest

# With verbose output
uv run pytest -v

# Parallel execution
uv run pytest -n auto

# Single test file
uv run pytest tests/layer1/test_captable_model.py

# Single test
uv run pytest tests/layer1/test_captable_model.py::TestModelBasic::test_ownership_sums_to_100
```

## Layer 2: Skill Smoke Tests

**Location:** `tests/layer2/`
**Run:** `uv run pytest -m smoke`
**Requirements:** Claude CLI with active subscription, installed skills

Layer 2 tests invoke skills end-to-end using `claude -p` (headless print mode).
They verify that the orchestrator routes correctly, sub-skills respond
appropriately, and script output is surfaced to the user.

### What Layer 2 covers

| Test                                          | Skill          | Validates                                |
| --------------------------------------------- | -------------- | ---------------------------------------- |
| `test_vc_displays_commands_table`             | `/vc`          | Orchestrator shows available commands    |
| `test_vc_model_prompts_for_inputs`            | `/vc model`    | Sub-skill asks for financial assumptions |
| `test_vc_kpi_prompts_for_data`                | `/vc kpi`      | Sub-skill asks for company data          |
| `test_vc_captable_with_inline_data`           | `/vc captable` | End-to-end cap table from inline data    |
| `test_vc_captable_output_includes_disclaimer` | `/vc captable` | Disclaimer present in output             |

### Running Layer 2

```bash
# Run smoke tests (requires claude CLI)
uv run pytest -m smoke

# Run with higher verbosity to see claude output
uv run pytest -m smoke -v -s
```

### Configuration

Each smoke test has budget and turn limits to prevent runaway costs:

- `max_turns`: Maximum agent turns (default: 3, higher for captable tests)
- `max_budget`: Maximum USD spend per test (default: $0.50, $1.00 for captable)
- `timeout`: 120 seconds per test

## Test Fixtures

**Location:** `tests/fixtures/`

JSON fixtures provide deterministic inputs for script tests. They are organized
by script:

```
tests/fixtures/
├── captable/
│   ├── model_basic.json          # Founders + ESOP only
│   ├── model_with_safes.json     # Post-money and pre-money SAFEs
│   ├── model_mfn_safes.json      # MFN SAFE resolution
│   ├── model_with_notes.json     # Convertible note with simple interest
│   ├── model_full.json           # All instrument types + priced round
│   ├── dilution_basic.json       # Series A dilution scenario
│   ├── waterfall_simple.json     # Non-participating preferred
│   ├── waterfall_multi_series.json  # Series A + B with seniority
│   ├── waterfall_participating.json # Participating preferred with cap
│   ├── convert_basic.json        # SAFE + note conversion to priced round
│   └── scenarios_basic.json      # Multiple exit value scenarios
└── financial/
    ├── dcf_gordon.json           # DCF with Gordon growth terminal value
    ├── dcf_exit_multiple.json    # DCF with exit multiple terminal value
    ├── dcf_error.json            # Invalid: discount <= growth rate
    ├── unit_economics_saas.json  # SaaS unit economics inputs
    ├── projections_basic.json    # Revenue projection inputs
    ├── multiples_basic.json      # Comparable company multiples
    ├── three_statement_basic.json    # 5-year 3-statement model
    └── three_statement_equity.json   # 3-year model with equity injection
```

## Test Infrastructure

### Shared helpers (`tests/helpers.py`)

Non-fixture utility functions importable from any test subdirectory:

- `load_fixture(name)` — Load a JSON fixture by relative path
- `run_script(script, command, fixture_path)` — Run a script CLI and parse JSON output
- `run_captable(command, fixture_name)` — Shortcut for captable.py
- `run_financial(command, fixture_name)` — Shortcut for financial_model.py
- `assert_ownership_sums_to_100(cap_table)` — Verify ownership invariant
- `SCRIPTS_DIR` / `PROJECT_ROOT` — Path constants

### Conftest (`tests/conftest.py`)

Sets up `sys.path` for script imports and provides pytest fixtures:

- `fixtures_dir` — Path to `tests/fixtures/`
- `captable_fixtures` — Path to `tests/fixtures/captable/`
- `financial_fixtures` — Path to `tests/fixtures/financial/`

### Pytest configuration (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "slow: marks tests as slow",
    "smoke: marks Layer 2 smoke tests using claude -p",
]
addopts = "-m 'not smoke'"  # Exclude smoke tests by default
```

## Adding New Tests

### Adding a Layer 1 test

1. Create a JSON fixture in `tests/fixtures/<script>/` if needed
2. Add test functions to the appropriate `test_<script>_<command>.py` file
3. Import helpers: `from helpers import load_fixture, run_captable`
4. Import script functions directly: `from captable import build_cap_table`
5. Run `uv run pytest tests/layer1/<your_file>.py -v` to verify

### Adding a Layer 2 smoke test

1. Add a test function to `tests/layer2/test_skill_smoke.py`
2. Use `run_claude(prompt, max_turns=N, max_budget=N)` to invoke
3. Assert on keywords in the output (case-insensitive)
4. Keep budget limits conservative
5. Run `uv run pytest -m smoke -k your_test_name` to verify

## Quality Gates

Before committing, all of these must pass:

```bash
uv run ruff check .            # Linter
uv run ruff format --check .   # Formatter
uv run pyright scripts/ tests/ # Type checker
uv run pytest                  # Layer 1 tests (172 tests)
```

Layer 2 smoke tests are optional in local development but should be run
before releasing new skill versions.
