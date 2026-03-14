"""Tests for convert_safes_to_round() from captable.py."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers import assert_ownership_sums_to_100, load_fixture, run_captable

from captable import convert_safes_to_round


class TestConvertBasic:
    def test_safe_conversion_shows_cap_price(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        safe_conv = next(
            c for c in result["conversions"] if c["name"] == "SAFE Investor"
        )
        assert safe_conv["price_from_cap"] == "0.681818"
        assert safe_conv["price_from_discount"] == "N/A"

    def test_safe_conversion_price_used(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        safe_conv = next(
            c for c in result["conversions"] if c["name"] == "SAFE Investor"
        )
        assert safe_conv["price_used"] == "cap"

    def test_safe_shares_issued(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        safe_conv = next(
            c for c in result["conversions"] if c["name"] == "SAFE Investor"
        )
        assert safe_conv["shares_issued"] == "733333"

    def test_note_conversion_includes_accrued_interest(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        note_conv = next(c for c in result["conversions"] if c["name"] == "Note Holder")
        accrued = Decimal(note_conv["accrued_interest"])
        assert accrued > Decimal(0)
        # Compound interest on 300K at 8% for 18 months should be ~38114
        assert abs(accrued - Decimal("38114")) < Decimal("1")

    def test_note_total_converting(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        note_conv = next(c for c in result["conversions"] if c["name"] == "Note Holder")
        total = Decimal(note_conv["total_converting"])
        investment = Decimal(note_conv["investment"])
        accrued = Decimal(note_conv["accrued_interest"])
        assert total == investment + accrued

    def test_note_conversion_price(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        note_conv = next(c for c in result["conversions"] if c["name"] == "Note Holder")
        # Cap price (0.852273) < discount price (1.163636), so cap is used
        assert note_conv["price_from_cap"] == "0.852273"
        assert note_conv["conversion_price"] == "0.852273"

    def test_note_interest_type(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        note_conv = next(c for c in result["conversions"] if c["name"] == "Note Holder")
        assert note_conv["interest_type"] == "compound"

    def test_resulting_cap_table_sums_to_100(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        assert_ownership_sums_to_100(result["cap_table"])

    def test_round_price_per_share(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        assert result["round_price_per_share"] == "1.319038"

    def test_post_money_valuation(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        assert result["post_money_valuation"] == "20000000"

    def test_conversion_count(self) -> None:
        result = convert_safes_to_round(load_fixture("captable/convert_basic.json"))
        assert len(result["conversions"]) == 2

    def test_cli_returns_valid_json(self) -> None:
        result = run_captable("convert", "convert_basic.json")
        assert "conversions" in result
        assert "cap_table" in result
