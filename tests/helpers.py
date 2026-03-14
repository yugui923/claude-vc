"""Shared helper functions for claude-vc tests.

This module contains non-fixture helpers that need to be importable from
subdirectory test files.  pytest conftest.py cannot be imported as a regular
module from sub-packages, so shared utilities live here instead.
"""

from __future__ import annotations

import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def load_fixture(name: str) -> dict[str, Any]:
    """Load a JSON fixture file by relative path under tests/fixtures/."""
    path = Path(__file__).parent / "fixtures" / name
    with open(path) as f:
        return json.load(f)


def run_script(script: str, command: str, fixture_path: str | Path) -> dict[str, Any]:
    """Run a Python script CLI command and return parsed JSON output."""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / script),
            command,
            "--input",
            str(fixture_path),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"{script} {command} failed: {result.stderr}"
    return json.loads(result.stdout)


def run_captable(command: str, fixture_name: str) -> dict[str, Any]:
    """Run captable.py with a fixture from tests/fixtures/captable/."""
    path = Path(__file__).parent / "fixtures" / "captable" / fixture_name
    return run_script("captable.py", command, path)


def run_financial(command: str, fixture_name: str) -> dict[str, Any]:
    """Run financial_model.py with a fixture from tests/fixtures/financial/."""
    path = Path(__file__).parent / "fixtures" / "financial" / fixture_name
    return run_script("financial_model.py", command, path)


def assert_ownership_sums_to_100(cap_table: list[dict[str, Any]]) -> None:
    """Assert that ownership percentages in a cap table sum to ~100%."""
    total = sum(Decimal(row["ownership_pct"]) for row in cap_table)
    assert abs(total - Decimal(100)) < Decimal("0.1"), (
        f"Ownership sums to {total}, expected ~100%"
    )
