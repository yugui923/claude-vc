"""Subprocess integration tests for financial_model.py CLI."""

from __future__ import annotations

import subprocess
import sys
import tempfile

from helpers import SCRIPTS_DIR, run_financial


SCRIPT = str(SCRIPTS_DIR / "financial_model.py")


def _run_raw(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def test_dcf_returns_valid_json() -> None:
    result = run_financial("dcf", "dcf_gordon.json")
    assert isinstance(result, dict)
    assert "enterprise_value" in result


def test_unit_economics_returns_valid_json() -> None:
    result = run_financial("unit_economics", "unit_economics_saas.json")
    assert isinstance(result, dict)
    assert "arpu_monthly" in result


def test_projections_returns_valid_json() -> None:
    result = run_financial("projections", "projections_basic.json")
    assert isinstance(result, dict)
    assert "projections" in result


def test_multiples_returns_valid_json() -> None:
    result = run_financial("multiples", "multiples_basic.json")
    assert isinstance(result, dict)
    assert "valuations" in result


def test_three_statement_returns_valid_json() -> None:
    result = run_financial("three_statement", "three_statement_basic.json")
    assert isinstance(result, dict)
    assert "income_statement" in result


def test_missing_input_flag_nonzero_exit() -> None:
    proc = _run_raw(["dcf"])
    assert proc.returncode != 0


def test_invalid_json_nonzero_exit() -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("not valid json {{{")
        f.flush()
        proc = _run_raw(["dcf", "--input", f.name])
    assert proc.returncode != 0


def test_unknown_command_nonzero_exit() -> None:
    proc = _run_raw(["nonexistent_command", "--input", "dummy.json"])
    assert proc.returncode != 0
