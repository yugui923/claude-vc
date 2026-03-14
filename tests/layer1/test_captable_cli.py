"""Subprocess integration tests for captable.py CLI."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


from helpers import SCRIPTS_DIR, run_captable


CAPTABLE_SCRIPT = str(SCRIPTS_DIR / "captable.py")
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "captable"


def _run_raw(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    """Run captable.py with raw args and return the CompletedProcess."""
    return subprocess.run(
        [sys.executable, CAPTABLE_SCRIPT, *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


# ---------------------------------------------------------------------------
# Each command returns valid JSON
# ---------------------------------------------------------------------------


class TestCliValidJson:
    def test_model_returns_valid_json(self) -> None:
        result = run_captable("model", "model_basic.json")
        assert isinstance(result, dict)
        assert "cap_table" in result

    def test_dilution_returns_valid_json(self) -> None:
        result = run_captable("dilution", "dilution_basic.json")
        assert isinstance(result, dict)
        assert "dilution_table" in result

    def test_waterfall_returns_valid_json(self) -> None:
        result = run_captable("waterfall", "waterfall_simple.json")
        assert isinstance(result, dict)
        assert "waterfall" in result

    def test_convert_returns_valid_json(self) -> None:
        result = run_captable("convert", "convert_basic.json")
        assert isinstance(result, dict)
        assert "conversions" in result

    def test_scenarios_returns_valid_json(self) -> None:
        result = run_captable("scenarios", "scenarios_basic.json")
        assert isinstance(result, dict)
        assert "scenarios" in result


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


class TestCliErrors:
    def test_missing_input_flag_model(self) -> None:
        proc = _run_raw(["model"])
        assert proc.returncode != 0

    def test_missing_input_flag_dilution(self) -> None:
        proc = _run_raw(["dilution"])
        assert proc.returncode != 0

    def test_invalid_json_returns_nonzero(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            tmp.write("{invalid json content")
            tmp_path = tmp.name

        proc = _run_raw(["model", "--input", tmp_path])
        assert proc.returncode != 0

    def test_unknown_command_returns_error(self) -> None:
        proc = _run_raw(["nonexistent_command"])
        assert proc.returncode != 0

    def test_no_command_returns_error(self) -> None:
        proc = _run_raw([])
        assert proc.returncode != 0

    def test_missing_file_returns_nonzero(self) -> None:
        proc = _run_raw(["model", "--input", "/nonexistent/path/file.json"])
        assert proc.returncode != 0
