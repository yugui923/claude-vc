"""Tests for calc_scenarios() from captable.py."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers import load_fixture, run_captable

from captable import calc_scenarios


class TestScenariosBasic:
    def test_correct_number_of_scenarios(self) -> None:
        result = calc_scenarios(load_fixture("captable/scenarios_basic.json"))
        assert len(result["scenarios"]) == 4

    def test_holder_names_match(self) -> None:
        result = calc_scenarios(load_fixture("captable/scenarios_basic.json"))
        assert result["holder_names"] == ["Founders", "ESOP", "Series A"]

    def test_higher_exit_improves_common_payout(self) -> None:
        result = calc_scenarios(load_fixture("captable/scenarios_basic.json"))
        scenarios = result["scenarios"]
        founders_payouts = [Decimal(s["Founders"]["payout"]) for s in scenarios]
        # Each scenario exit value is higher, so common payout should increase
        for i in range(1, len(founders_payouts)):
            assert founders_payouts[i] > founders_payouts[i - 1]

    def test_exit_values_present(self) -> None:
        result = calc_scenarios(load_fixture("captable/scenarios_basic.json"))
        exit_values = [s["exit_value"] for s in result["scenarios"]]
        assert exit_values == ["10000000", "25000000", "50000000", "100000000"]

    def test_series_a_at_low_exit_gets_preference(self) -> None:
        """At 10M exit, Series A (1x non-participating, 5M invested) gets 5M."""
        result = calc_scenarios(load_fixture("captable/scenarios_basic.json"))
        scenario_10m = result["scenarios"][0]
        assert scenario_10m["Series A"]["payout"] == "5000000"
        assert scenario_10m["Series A"]["return_multiple"] == "1.00x"

    def test_series_a_at_high_exit_converts(self) -> None:
        """At 50M exit, Series A converts: 2M/10M * 50M = 10M > 5M pref."""
        result = calc_scenarios(load_fixture("captable/scenarios_basic.json"))
        scenario_50m = result["scenarios"][2]
        assert scenario_50m["Series A"]["payout"] == "10000000"
        assert scenario_50m["Series A"]["return_multiple"] == "2.00x"

    def test_founders_payout_at_100m(self) -> None:
        result = calc_scenarios(load_fixture("captable/scenarios_basic.json"))
        scenario_100m = result["scenarios"][3]
        assert scenario_100m["Founders"]["payout"] == "70000000"

    def test_cli_returns_valid_json(self) -> None:
        result = run_captable("scenarios", "scenarios_basic.json")
        assert "scenarios" in result
        assert "holder_names" in result
