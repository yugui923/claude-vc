"""Shared fixtures and helpers for claude-vc tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "skills" / "vc" / "scripts"
TESTS_DIR = Path(__file__).parent

# Add skills/vc/scripts/ and tests/ to sys.path so that:
# - test files can `import captable` / `import financial_model` directly
# - subdirectory tests can `from helpers import ...`
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(TESTS_DIR))

# Re-export helpers so existing `from conftest import ...` in top-level tests
# still works (pytest auto-discovers conftest but it isn't importable as a module
# from subdirectories — those use `from helpers import ...` instead).
from helpers import (  # noqa: F401, E402
    assert_ownership_sums_to_100,
    load_fixture,
    run_captable,
    run_financial,
    run_script,
)


@pytest.fixture
def fixtures_dir() -> Path:
    return TESTS_DIR / "fixtures"


@pytest.fixture
def captable_fixtures(fixtures_dir: Path) -> Path:
    return fixtures_dir / "captable"


@pytest.fixture
def financial_fixtures(fixtures_dir: Path) -> Path:
    return fixtures_dir / "financial"
