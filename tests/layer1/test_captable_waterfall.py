"""Tests for calc_waterfall() from captable.py."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers import load_fixture, run_captable

from captable import calc_waterfall


# ---------------------------------------------------------------------------
# Simple non-participating preferred (waterfall_simple.json)
# ---------------------------------------------------------------------------


class TestWaterfallSimple:
    def test_preferred_gets_preference_amount(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_simple.json"))
        wf = result["waterfall"]
        series_a = next(r for r in wf if r["name"] == "Series A")
        # Non-participating 1x preference: 5M investment -> 5M payout
        # Converting as common: 2M/10M * 20M = 4M (worse), so takes preference
        assert series_a["payout"] == "5000000"

    def test_preferred_converts_when_better(self) -> None:
        """At $20M exit with 2M/10M shares, converting gives $4M < $5M pref.
        Series A takes the preference, remaining $15M split among common."""
        result = calc_waterfall(load_fixture("captable/waterfall_simple.json"))
        wf = result["waterfall"]
        # The fact that payout is exactly 5M (1x) means they did NOT convert
        series_a = next(r for r in wf if r["name"] == "Series A")
        assert series_a["return_multiple"] == "1.00x"

    def test_founders_payout(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_simple.json"))
        wf = result["waterfall"]
        founders = next(r for r in wf if r["name"] == "Founders")
        assert founders["payout"] == "13125000"

    def test_esop_payout(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_simple.json"))
        wf = result["waterfall"]
        esop = next(r for r in wf if r["name"] == "ESOP")
        assert esop["payout"] == "1875000"

    def test_payouts_sum_to_exit_value(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_simple.json"))
        wf = result["waterfall"]
        total_payout = sum(Decimal(r["payout"]) for r in wf)
        assert total_payout == Decimal("20000000")


# ---------------------------------------------------------------------------
# Multi-series with seniority (waterfall_multi_series.json)
# ---------------------------------------------------------------------------


class TestWaterfallMultiSeries:
    def test_series_b_paid_before_series_a(self) -> None:
        """Series B (seniority 3) gets preference before Series A (seniority 2)."""
        result = calc_waterfall(load_fixture("captable/waterfall_multi_series.json"))
        wf = result["waterfall"]
        series_b = next(r for r in wf if r["name"] == "Series B")
        # 1.5x preference on 10M = 15M
        assert Decimal(series_b["payout"]) >= Decimal("15000000")

    def test_series_b_payout(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_multi_series.json"))
        wf = result["waterfall"]
        series_b = next(r for r in wf if r["name"] == "Series B")
        assert series_b["payout"] == "21000000"

    def test_series_a_payout(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_multi_series.json"))
        wf = result["waterfall"]
        series_a = next(r for r in wf if r["name"] == "Series A")
        assert series_a["payout"] == "7250000"

    def test_founders_payout(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_multi_series.json"))
        wf = result["waterfall"]
        founders = next(r for r in wf if r["name"] == "Founders")
        assert founders["payout"] == "18125000"

    def test_payouts_sum_to_exit_value(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_multi_series.json"))
        wf = result["waterfall"]
        total_payout = sum(Decimal(r["payout"]) for r in wf)
        assert total_payout == Decimal("50000000")


# ---------------------------------------------------------------------------
# Participating preferred with cap (waterfall_participating.json)
# ---------------------------------------------------------------------------


class TestWaterfallParticipating:
    def test_participating_preferred_payout(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_participating.json"))
        wf = result["waterfall"]
        series_a = next(r for r in wf if r["name"] == "Series A")
        # 1x preference = 5M + participation (capped at 3x = 15M total)
        assert series_a["payout"] == "10000000"

    def test_participating_preferred_return_multiple(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_participating.json"))
        wf = result["waterfall"]
        series_a = next(r for r in wf if r["name"] == "Series A")
        assert series_a["return_multiple"] == "2.00x"

    def test_founders_payout(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_participating.json"))
        wf = result["waterfall"]
        founders = next(r for r in wf if r["name"] == "Founders")
        assert founders["payout"] == "17500000"

    def test_payouts_sum_to_exit_value(self) -> None:
        result = calc_waterfall(load_fixture("captable/waterfall_participating.json"))
        wf = result["waterfall"]
        total_payout = sum(Decimal(r["payout"]) for r in wf)
        assert total_payout == Decimal("30000000")


# ---------------------------------------------------------------------------
# Zero exit
# ---------------------------------------------------------------------------


class TestWaterfallZeroExit:
    def test_all_payouts_zero(self) -> None:
        scenario = {
            "exit_value": 0,
            "total_shares": 10000000,
            "stock_classes": [
                {
                    "class_id": "common",
                    "name": "Common",
                    "instrument_type": "common",
                    "seniority": 1,
                },
                {
                    "class_id": "series_a",
                    "name": "Series A",
                    "instrument_type": "preferred",
                    "seniority": 2,
                    "liquidation_multiple": 1,
                    "participating": False,
                },
            ],
            "holders": [
                {
                    "name": "Founders",
                    "instrument": "common",
                    "shares": 7000000,
                    "investment": 0,
                    "stock_class_id": "common",
                },
                {
                    "name": "ESOP",
                    "instrument": "options",
                    "shares": 1000000,
                    "investment": 0,
                },
                {
                    "name": "Series A",
                    "instrument": "preferred",
                    "shares": 2000000,
                    "investment": 5000000,
                    "stock_class_id": "series_a",
                },
            ],
        }
        result = calc_waterfall(scenario)
        wf = result["waterfall"]
        for row in wf:
            assert row["payout"] == "0"

    def test_payouts_sum_to_zero_exit(self) -> None:
        scenario = {
            "exit_value": 0,
            "total_shares": 10000000,
            "stock_classes": [],
            "holders": [
                {
                    "name": "Founders",
                    "instrument": "common",
                    "shares": 7000000,
                    "investment": 0,
                },
                {
                    "name": "Series A",
                    "instrument": "preferred",
                    "shares": 3000000,
                    "investment": 5000000,
                },
            ],
        }
        result = calc_waterfall(scenario)
        wf = result["waterfall"]
        total_payout = sum(Decimal(r["payout"]) for r in wf)
        assert total_payout == Decimal(0)


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------


class TestWaterfallCli:
    def test_cli_returns_valid_json(self) -> None:
        result = run_captable("waterfall", "waterfall_simple.json")
        assert "waterfall" in result
        assert "exit_value" in result
