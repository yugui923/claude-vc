"""Layer 2: Smoke tests using `claude -p` to invoke skills.

These tests require the `claude` CLI with an active subscription.
They are excluded from default test runs — use `pytest -m smoke` to run.

Turn and budget allowances include ~50% headroom above the minimum observed
to pass. This reflects the one-extra-turn cost of the v2.0.0 orchestrator
hop (orchestrator reads the command file, then follows its instructions)
and prevents flakes from model variability.
"""

from __future__ import annotations

import subprocess
import shutil

import pytest

PROJECT_ROOT = __import__("pathlib").Path(__file__).parent.parent.parent

pytestmark = [pytest.mark.smoke, pytest.mark.slow]


@pytest.fixture(autouse=True)
def _skip_if_no_claude() -> None:
    """Skip all smoke tests if claude CLI is not available."""
    if not shutil.which("claude"):
        pytest.skip("claude CLI not found")


def run_claude(
    prompt: str,
    *,
    max_turns: int = 3,
    max_budget: float = 0.75,
    timeout: int = 240,
) -> str:
    """Run claude -p and return the text output."""
    result = subprocess.run(
        [
            "claude",
            "-p",
            "--max-turns",
            str(max_turns),
            "--max-budget-usd",
            str(max_budget),
            "--dangerously-skip-permissions",
            "--output-format",
            "text",
            prompt,
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, (
        f"claude -p failed (exit {result.returncode}): {result.stderr}"
    )
    return result.stdout


# ---------------------------------------------------------------------------
# Help and basic invocation
# ---------------------------------------------------------------------------


def test_vc_displays_commands_table() -> None:
    """Invoking /vc with no args should display the commands table."""
    output = run_claude("Run /vc with no arguments", max_turns=3)
    output_lower = output.lower()
    assert "screen" in output_lower
    assert "memo" in output_lower
    assert "captable" in output_lower or "cap table" in output_lower


# ---------------------------------------------------------------------------
# model and captable (unchanged commands)
# ---------------------------------------------------------------------------


def test_vc_model_prompts_for_inputs() -> None:
    """Invoking /vc model with no data should ask for inputs."""
    output = run_claude("Run /vc model", max_turns=3)
    output_lower = output.lower()
    assert any(
        kw in output_lower
        for kw in ["revenue", "growth", "assumption", "input", "provide", "need"]
    )


def test_vc_captable_with_inline_data() -> None:
    """Invoking /vc captable with inline data should produce a cap table."""
    prompt = (
        "Run /vc captable. Use this data: "
        "Alice has 6M common shares, Bob has 4M common shares, "
        "ESOP has 1M option shares. Just show the cap table."
    )
    output = run_claude(prompt, max_turns=12, max_budget=2.50)
    output_lower = output.lower()
    assert "alice" in output_lower
    assert "bob" in output_lower


def test_vc_captable_output_includes_disclaimer() -> None:
    """Cap table output should include a disclaimer."""
    prompt = (
        "Run /vc captable. Use this data: "
        "Alice has 6M shares, Bob has 4M shares. Show the cap table."
    )
    output = run_claude(prompt, max_turns=12, max_budget=2.50)
    output_lower = output.lower()
    assert any(
        kw in output_lower
        for kw in [
            "disclaimer",
            "not constitute",
            "informational",
            "not investment advice",
        ]
    )


# ---------------------------------------------------------------------------
# screen (single-company and comparison mode)
# ---------------------------------------------------------------------------


def test_vc_screen_multi_input_comparison() -> None:
    """Passing 2+ inputs to /vc screen should produce a comparison."""
    prompt = (
        "Run /vc screen. Compare these two companies: "
        "Company A is a SaaS startup with $5M ARR, 200% growth, 80% margins, "
        "team from Google and Stripe, in the devtools space. "
        "Company B is a marketplace startup with $3M GMV, 300% growth, 25% take rate, "
        "team from Uber and Airbnb, in the logistics space."
    )
    output = run_claude(prompt, max_turns=9, max_budget=2.50)
    output_lower = output.lower()
    assert "company a" in output_lower or "saas" in output_lower
    assert "company b" in output_lower or "marketplace" in output_lower


def test_vc_screen_full_produces_comprehensive_output() -> None:
    """Invoking /vc screen --full should reference parallel analysis.

    This is the most expensive test: the orchestrator reads SKILL.md, routes
    to commands/screen.md, reads 6 agent prompt files from agents/, spawns 6
    parallel Task sub-agents, aggregates findings, and produces a Deal Score.
    Turn and budget allowances include ~50% headroom above observed minimums.
    """
    prompt = (
        "Run /vc screen --full "
        "tests/real-data/pitch-decks/synthetic-novabyte-series-a-deck.md"
    )
    # Subprocess timeout bumped to 9 minutes with 50% headroom — 6 parallel
    # Task sub-agents + aggregation routinely exceeds the default 4-minute cap.
    output = run_claude(prompt, max_turns=25, max_budget=8.00, timeout=540)
    output_lower = output.lower()
    # Full screen should produce a Deal Score with multiple dimensions
    assert "score" in output_lower or "deal score" in output_lower
    assert any(kw in output_lower for kw in ["market", "team", "product", "financial"])


# ---------------------------------------------------------------------------
# memo (with --diligence-only flag — replaces the old diligence command)
# ---------------------------------------------------------------------------


def test_vc_memo_diligence_only_prompts_for_stage() -> None:
    """Invoking /vc memo --diligence-only with no context should ask for stage/sector."""
    output = run_claude("Run /vc memo --diligence-only", max_turns=3)
    output_lower = output.lower()
    assert any(
        kw in output_lower
        for kw in ["stage", "company", "sector", "provide", "need", "series"]
    )


def test_vc_memo_diligence_only_generates_checklist() -> None:
    """Invoking /vc memo --diligence-only with stage/sector should produce a checklist."""
    prompt = (
        "Run /vc memo --diligence-only for a Series A SaaS company "
        "in the developer tools space called NovaByte."
    )
    output = run_claude(prompt, max_turns=6, max_budget=2.00)
    output_lower = output.lower()
    assert any(kw in output_lower for kw in ["financial", "legal", "technical"])
    assert any(kw in output_lower for kw in ["checklist", "diligence", "[ ]", "[x]"])


# ---------------------------------------------------------------------------
# portfolio (default, --kpi, --returns)
# ---------------------------------------------------------------------------


def test_vc_portfolio_prompts_for_data() -> None:
    """Invoking /vc portfolio with no data should ask for portfolio data."""
    output = run_claude("Run /vc portfolio", max_turns=3)
    output_lower = output.lower()
    assert any(
        kw in output_lower
        for kw in ["portfolio", "company", "data", "provide", "need", "list"]
    )


def test_vc_portfolio_with_inline_data() -> None:
    """Invoking /vc portfolio with inline company data should produce a report."""
    prompt = (
        "Run /vc portfolio. Here is my portfolio data: "
        "Company A: SaaS, Series A, invested $2M in 2024, current valuation $20M, "
        "$5M ARR, 40 employees, status active. "
        "Company B: Fintech, Seed, invested $500K in 2023, current valuation $8M, "
        "$1M ARR, 12 employees, status active. "
        "Company C: Consumer, Series A, invested $1.5M in 2022, written off."
    )
    output = run_claude(prompt, max_turns=9, max_budget=2.50)
    output_lower = output.lower()
    assert "company a" in output_lower or "saas" in output_lower
    assert any(
        kw in output_lower
        for kw in ["portfolio", "invested", "valuation", "summary", "total"]
    )


def test_vc_portfolio_kpi_prompts_for_data() -> None:
    """Invoking /vc portfolio --kpi with no data should ask for company data.

    Needs extra turns: the model reads the orchestrator, then
    commands/portfolio.md, may consult references (industry-multiples,
    firm-criteria/firm-templates config) before prompting. Generous budget
    accommodates this exploration variability.
    """
    output = run_claude("Run /vc portfolio --kpi", max_turns=8)
    output_lower = output.lower()
    assert any(
        kw in output_lower
        for kw in ["company", "data", "metrics", "type", "provide", "need"]
    )
