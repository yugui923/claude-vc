"""Tests for build_cap_table() from captable.py."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers import assert_ownership_sums_to_100, load_fixture, run_captable

from captable import build_cap_table


# ---------------------------------------------------------------------------
# Founders only (model_basic.json)
# ---------------------------------------------------------------------------


class TestModelBasic:
    def test_founders_ownership_alice(self) -> None:
        result = build_cap_table(load_fixture("captable/model_basic.json"))
        cap = result["cap_table"]
        alice = next(r for r in cap if r["name"] == "Alice")
        assert alice["ownership_pct"] == "54.55"

    def test_founders_ownership_bob(self) -> None:
        result = build_cap_table(load_fixture("captable/model_basic.json"))
        cap = result["cap_table"]
        bob = next(r for r in cap if r["name"] == "Bob")
        assert bob["ownership_pct"] == "36.36"

    def test_esop_ownership(self) -> None:
        result = build_cap_table(load_fixture("captable/model_basic.json"))
        cap = result["cap_table"]
        esop = next(r for r in cap if r["name"] == "ESOP")
        assert esop["ownership_pct"] == "9.09"

    def test_total_shares(self) -> None:
        result = build_cap_table(load_fixture("captable/model_basic.json"))
        assert result["total_shares"] == "11000000"

    def test_no_price_per_share(self) -> None:
        result = build_cap_table(load_fixture("captable/model_basic.json"))
        assert result["price_per_share"] == "N/A"

    def test_ownership_sums_to_100(self) -> None:
        result = build_cap_table(load_fixture("captable/model_basic.json"))
        assert_ownership_sums_to_100(result["cap_table"])

    def test_cli_returns_valid_json(self) -> None:
        result = run_captable("model", "model_basic.json")
        assert "cap_table" in result
        assert len(result["cap_table"]) == 3


# ---------------------------------------------------------------------------
# With post-money and pre-money SAFEs (model_with_safes.json)
# ---------------------------------------------------------------------------


class TestModelWithSafes:
    def test_safe_investor_a_present(self) -> None:
        result = build_cap_table(load_fixture("captable/model_with_safes.json"))
        cap = result["cap_table"]
        safe_a = next(r for r in cap if r["name"] == "SAFE Investor A")
        assert safe_a["instrument"] == "safe_post_money"
        assert Decimal(safe_a["ownership_pct"]) > Decimal(0)

    def test_safe_investor_b_present(self) -> None:
        result = build_cap_table(load_fixture("captable/model_with_safes.json"))
        cap = result["cap_table"]
        safe_b = next(r for r in cap if r["name"] == "SAFE Investor B")
        assert safe_b["instrument"] == "safe_pre_money"
        assert Decimal(safe_b["ownership_pct"]) > Decimal(0)

    def test_post_money_safe_ownership(self) -> None:
        result = build_cap_table(load_fixture("captable/model_with_safes.json"))
        cap = result["cap_table"]
        safe_a = next(r for r in cap if r["name"] == "SAFE Investor A")
        assert safe_a["ownership_pct"] == "4.85"

    def test_pre_money_safe_ownership(self) -> None:
        result = build_cap_table(load_fixture("captable/model_with_safes.json"))
        cap = result["cap_table"]
        safe_b = next(r for r in cap if r["name"] == "SAFE Investor B")
        assert safe_b["ownership_pct"] == "3.03"

    def test_ownership_sums_to_100(self) -> None:
        result = build_cap_table(load_fixture("captable/model_with_safes.json"))
        assert_ownership_sums_to_100(result["cap_table"])

    def test_total_shares_increased(self) -> None:
        result = build_cap_table(load_fixture("captable/model_with_safes.json"))
        # Founders + ESOP = 11M, SAFEs add more
        assert Decimal(result["total_shares"]) > Decimal("11000000")


# ---------------------------------------------------------------------------
# MFN SAFEs (model_mfn_safes.json)
# ---------------------------------------------------------------------------


class TestModelMfnSafes:
    def test_mfn_resolves_to_lowest_non_mfn_cap(self) -> None:
        """MFN SAFE should use the lowest non-MFN cap (8M from SAFE B)."""
        result = build_cap_table(load_fixture("captable/model_mfn_safes.json"))
        cap = result["cap_table"]
        mfn = next(r for r in cap if r["name"] == "SAFE MFN")
        # MFN with 200K at 8M cap should get ~2.50% ownership
        assert mfn["ownership_pct"] == "2.50"

    def test_safe_b_has_higher_ownership_than_mfn(self) -> None:
        """SAFE B (300K at 8M) should own more than MFN (200K at 8M)."""
        result = build_cap_table(load_fixture("captable/model_mfn_safes.json"))
        cap = result["cap_table"]
        safe_b = next(r for r in cap if r["name"] == "SAFE B")
        mfn = next(r for r in cap if r["name"] == "SAFE MFN")
        assert Decimal(safe_b["ownership_pct"]) > Decimal(mfn["ownership_pct"])

    def test_safe_a_ownership(self) -> None:
        result = build_cap_table(load_fixture("captable/model_mfn_safes.json"))
        cap = result["cap_table"]
        safe_a = next(r for r in cap if r["name"] == "SAFE A")
        assert safe_a["ownership_pct"] == "4.69"

    def test_ownership_sums_to_100(self) -> None:
        result = build_cap_table(load_fixture("captable/model_mfn_safes.json"))
        assert_ownership_sums_to_100(result["cap_table"])


# ---------------------------------------------------------------------------
# With notes (model_with_notes.json)
# ---------------------------------------------------------------------------


class TestModelWithNotes:
    def test_note_holder_present(self) -> None:
        result = build_cap_table(load_fixture("captable/model_with_notes.json"))
        cap = result["cap_table"]
        note = next(r for r in cap if r["name"] == "Note Holder")
        assert note["instrument"] == "convertible_note"

    def test_note_includes_simple_interest(self) -> None:
        """Note with 8% simple interest for 12 months on 300K -> 24K accrued.
        Total converting: 324K. At 10M cap / 11M shares -> PPS ~0.909.
        Shares = 324000 / 0.909... = 356400.
        """
        result = build_cap_table(load_fixture("captable/model_with_notes.json"))
        cap = result["cap_table"]
        note = next(r for r in cap if r["name"] == "Note Holder")
        assert note["shares"] == "356400"

    def test_note_ownership(self) -> None:
        result = build_cap_table(load_fixture("captable/model_with_notes.json"))
        cap = result["cap_table"]
        note = next(r for r in cap if r["name"] == "Note Holder")
        assert note["ownership_pct"] == "3.14"

    def test_ownership_sums_to_100(self) -> None:
        result = build_cap_table(load_fixture("captable/model_with_notes.json"))
        assert_ownership_sums_to_100(result["cap_table"])


# ---------------------------------------------------------------------------
# Full stack (model_full.json)
# ---------------------------------------------------------------------------


class TestModelFull:
    def test_all_holder_types_present(self) -> None:
        result = build_cap_table(load_fixture("captable/model_full.json"))
        cap = result["cap_table"]
        instruments = {r["instrument"] for r in cap}
        assert "common" in instruments
        assert "options" in instruments
        assert "safe_post_money" in instruments
        assert "convertible_note" in instruments
        assert "preferred" in instruments

    def test_series_a_ownership(self) -> None:
        result = build_cap_table(load_fixture("captable/model_full.json"))
        cap = result["cap_table"]
        series_a = next(r for r in cap if r["name"] == "Series A")
        assert series_a["ownership_pct"] == "20.00"

    def test_alice_ownership(self) -> None:
        result = build_cap_table(load_fixture("captable/model_full.json"))
        cap = result["cap_table"]
        alice = next(r for r in cap if r["name"] == "Alice")
        assert alice["ownership_pct"] == "29.87"

    def test_price_per_share(self) -> None:
        result = build_cap_table(load_fixture("captable/model_full.json"))
        assert result["price_per_share"] == "1.867016"

    def test_ownership_sums_to_100(self) -> None:
        result = build_cap_table(load_fixture("captable/model_full.json"))
        assert_ownership_sums_to_100(result["cap_table"])

    def test_holder_count(self) -> None:
        result = build_cap_table(load_fixture("captable/model_full.json"))
        assert len(result["cap_table"]) == 6
