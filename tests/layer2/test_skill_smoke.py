"""Layer 2: Smoke tests using `claude -p` to invoke skills.

These tests require the `claude` CLI with an active subscription.
They are excluded from default test runs — use `pytest -m smoke` to run.
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


def run_claude(prompt: str, *, max_turns: int = 3, max_budget: float = 0.50) -> str:
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
        timeout=180,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, (
        f"claude -p failed (exit {result.returncode}): {result.stderr}"
    )
    return result.stdout


def test_vc_displays_commands_table() -> None:
    """Invoking /vc with no args should display the commands table."""
    output = run_claude("Run /vc with no arguments", max_turns=2)
    output_lower = output.lower()
    assert "screen" in output_lower
    assert "memo" in output_lower
    assert "captable" in output_lower or "cap table" in output_lower


def test_vc_model_prompts_for_inputs() -> None:
    """Invoking /vc model with no data should ask for inputs."""
    output = run_claude("Run /vc model", max_turns=2)
    output_lower = output.lower()
    assert any(
        kw in output_lower
        for kw in ["revenue", "growth", "assumption", "input", "provide", "need"]
    )


def test_vc_kpi_prompts_for_data() -> None:
    """Invoking /vc kpi with no data should ask for company data."""
    output = run_claude("Run /vc kpi", max_turns=2)
    output_lower = output.lower()
    assert any(
        kw in output_lower
        for kw in ["company", "data", "metrics", "type", "provide", "need"]
    )


def test_vc_captable_with_inline_data() -> None:
    """Invoking /vc captable with inline data should produce a cap table."""
    prompt = (
        "Run /vc captable. Use this data: "
        "Alice has 6M common shares, Bob has 4M common shares, "
        "ESOP has 1M option shares. Just show the cap table."
    )
    output = run_claude(prompt, max_turns=8, max_budget=1.50)
    output_lower = output.lower()
    assert "alice" in output_lower
    assert "bob" in output_lower


def test_vc_captable_output_includes_disclaimer() -> None:
    """Cap table output should include a disclaimer."""
    prompt = (
        "Run /vc captable. Use this data: "
        "Alice has 6M shares, Bob has 4M shares. Show the cap table."
    )
    output = run_claude(prompt, max_turns=8, max_budget=1.50)
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
