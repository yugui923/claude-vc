"""Tests for calc_dilution() from captable.py."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers import load_fixture, run_captable

from captable import calc_dilution


class TestDilutionBasic:
    def test_all_existing_holders_diluted(self) -> None:
        result = calc_dilution(load_fixture("captable/dilution_basic.json"))
        table = result["dilution_table"]
        existing = [r for r in table if r["dilution_pct"] != "N/A"]
        assert len(existing) == 3
        for row in existing:
            assert Decimal(row["dilution_pct"]) > Decimal(0)

    def test_alice_dilution(self) -> None:
        result = calc_dilution(load_fixture("captable/dilution_basic.json"))
        table = result["dilution_table"]
        alice = next(r for r in table if r["name"] == "Alice")
        assert alice["pre_pct"] == "60.00"
        assert alice["post_pct"] == "48.00"
        assert alice["dilution_pct"] == "20.00"

    def test_bob_dilution(self) -> None:
        result = calc_dilution(load_fixture("captable/dilution_basic.json"))
        table = result["dilution_table"]
        bob = next(r for r in table if r["name"] == "Bob")
        assert bob["pre_pct"] == "30.00"
        assert bob["post_pct"] == "24.00"
        assert bob["dilution_pct"] == "20.00"

    def test_new_investor_shows_na_dilution(self) -> None:
        result = calc_dilution(load_fixture("captable/dilution_basic.json"))
        table = result["dilution_table"]
        series_a = next(r for r in table if r["name"] == "Series A")
        assert series_a["dilution_pct"] == "N/A"
        assert series_a["pre_pct"] == "0.00"
        assert series_a["post_pct"] == "20.00"

    def test_post_money_equals_pre_plus_investment(self) -> None:
        result = calc_dilution(load_fixture("captable/dilution_basic.json"))
        assert result["post_money_valuation"] == "25000000"
        # pre_money=20M + investment=5M = 25M

    def test_existing_share_counts_unchanged(self) -> None:
        result = calc_dilution(load_fixture("captable/dilution_basic.json"))
        table = result["dilution_table"]
        alice = next(r for r in table if r["name"] == "Alice")
        bob = next(r for r in table if r["name"] == "Bob")
        esop = next(r for r in table if r["name"] == "ESOP")
        assert alice["shares"] == "6000000"
        assert bob["shares"] == "3000000"
        assert esop["shares"] == "1000000"

    def test_total_shares_increased(self) -> None:
        result = calc_dilution(load_fixture("captable/dilution_basic.json"))
        assert Decimal(result["total_shares_after"]) > Decimal(
            result["total_shares_before"]
        )

    def test_price_per_share(self) -> None:
        result = calc_dilution(load_fixture("captable/dilution_basic.json"))
        assert result["price_per_share"] == "2.000000"

    def test_cli_returns_valid_json(self) -> None:
        result = run_captable("dilution", "dilution_basic.json")
        assert "dilution_table" in result
        assert len(result["dilution_table"]) == 4
