"""Unit tests for captable.py internal helper functions."""

from __future__ import annotations

from decimal import Decimal

from captable import (
    CapDefinition,
    Holder,
    InterestType,
    InstrumentType,
    _calc_accrued_interest,
    _d,
    _fmt,
    _get_capitalization,
    _parse_note_terms,
    _parse_safe_terms,
    _parse_stock_classes,
)


# ---------------------------------------------------------------------------
# _d() – Decimal coercion
# ---------------------------------------------------------------------------


class TestD:
    def test_d_from_string(self) -> None:
        assert _d("123.45") == Decimal("123.45")

    def test_d_from_int(self) -> None:
        assert _d(42) == Decimal("42")

    def test_d_from_none(self) -> None:
        assert _d(None) == Decimal(0)

    def test_d_from_decimal(self) -> None:
        val = Decimal("99.99")
        assert _d(val) is val  # should return the same object

    def test_d_from_float(self) -> None:
        result = _d(1.5)
        assert result == Decimal("1.5")


# ---------------------------------------------------------------------------
# _fmt() – formatting
# ---------------------------------------------------------------------------


class TestFmt:
    def test_fmt_zero_places(self) -> None:
        assert _fmt(Decimal("1234.6")) == "1235"

    def test_fmt_two_places(self) -> None:
        assert _fmt(Decimal("1.2345"), 2) == "1.23"

    def test_fmt_rounds_half_up(self) -> None:
        assert _fmt(Decimal("2.5"), 0) == "3"
        assert _fmt(Decimal("3.5"), 0) == "4"

    def test_fmt_two_places_rounds_half_up(self) -> None:
        assert _fmt(Decimal("1.235"), 2) == "1.24"

    def test_fmt_zero_places_exact(self) -> None:
        assert _fmt(Decimal("100"), 0) == "100"


# ---------------------------------------------------------------------------
# _calc_accrued_interest()
# ---------------------------------------------------------------------------


class TestCalcAccruedInterest:
    def test_simple_zero_rate(self) -> None:
        result = _calc_accrued_interest(
            Decimal("100000"), Decimal("0"), 12, InterestType.SIMPLE
        )
        assert result == Decimal(0)

    def test_simple_zero_months(self) -> None:
        result = _calc_accrued_interest(
            Decimal("100000"), Decimal("0.08"), 0, InterestType.SIMPLE
        )
        assert result == Decimal(0)

    def test_simple_basic_calc(self) -> None:
        # 300000 * 0.08 * 12/12 = 24000
        result = _calc_accrued_interest(
            Decimal("300000"), Decimal("0.08"), 12, InterestType.SIMPLE
        )
        assert result == Decimal("24000")

    def test_simple_partial_year(self) -> None:
        # 100000 * 0.06 * 6/12 = 3000
        result = _calc_accrued_interest(
            Decimal("100000"), Decimal("0.06"), 6, InterestType.SIMPLE
        )
        assert result == Decimal("3000")

    def test_compound_monthly(self) -> None:
        # 300000 * ((1 + 0.08/12)^(12*18/12) - 1)
        result = _calc_accrued_interest(
            Decimal("300000"),
            Decimal("0.08"),
            18,
            InterestType.COMPOUND,
            compounding_frequency=12,
        )
        # Expected: ~38114
        assert abs(result - Decimal("38114")) < Decimal("1")

    def test_compound_quarterly(self) -> None:
        # 100000 * ((1 + 0.10/4)^(4*1) - 1) = 100000 * (1.025^4 - 1)
        result = _calc_accrued_interest(
            Decimal("100000"),
            Decimal("0.10"),
            12,
            InterestType.COMPOUND,
            compounding_frequency=4,
        )
        expected = Decimal("100000") * ((1 + Decimal("0.10") / 4) ** 4 - 1)
        assert abs(result - expected) < Decimal("0.01")


# ---------------------------------------------------------------------------
# _parse_stock_classes()
# ---------------------------------------------------------------------------


class TestParseStockClasses:
    def test_defaults(self) -> None:
        data = [{"class_id": "common", "name": "Common"}]
        result = _parse_stock_classes(data)
        assert "common" in result
        sc = result["common"]
        assert sc.class_id == "common"
        assert sc.name == "Common"
        assert sc.instrument_type == InstrumentType.PREFERRED  # default
        assert sc.seniority == 1
        assert sc.liquidation_multiple == Decimal(1)
        assert sc.participating is False
        assert sc.participation_cap is None
        assert sc.conversion_ratio == Decimal(1)
        assert sc.votes_per_share == Decimal(1)

    def test_full_fields(self) -> None:
        data = [
            {
                "class_id": "series_b",
                "name": "Series B",
                "instrument_type": "preferred",
                "seniority": 3,
                "liquidation_multiple": 1.5,
                "participating": True,
                "participation_cap": 3,
                "conversion_ratio": 2,
                "votes_per_share": 0,
            }
        ]
        result = _parse_stock_classes(data)
        sc = result["series_b"]
        assert sc.seniority == 3
        assert sc.liquidation_multiple == Decimal("1.5")
        assert sc.participating is True
        assert sc.participation_cap == Decimal("3")
        assert sc.conversion_ratio == Decimal("2")
        assert sc.votes_per_share == Decimal("0")

    def test_multiple_classes(self) -> None:
        data = [
            {"class_id": "common", "name": "Common", "instrument_type": "common"},
            {"class_id": "series_a", "name": "Series A", "seniority": 2},
        ]
        result = _parse_stock_classes(data)
        assert len(result) == 2
        assert "common" in result
        assert "series_a" in result


# ---------------------------------------------------------------------------
# _parse_safe_terms()
# ---------------------------------------------------------------------------


class TestParseSafeTerms:
    def test_post_money_safe(self) -> None:
        data = {
            "valuation_cap": 10000000,
            "is_post_money": True,
        }
        terms = _parse_safe_terms(data)
        assert terms.valuation_cap == Decimal("10000000")
        assert terms.is_post_money is True
        assert terms.mfn is False
        assert terms.discount is None

    def test_pre_money_safe(self) -> None:
        data = {
            "valuation_cap": 8000000,
            "is_post_money": False,
            "discount": 0.2,
        }
        terms = _parse_safe_terms(data)
        assert terms.valuation_cap == Decimal("8000000")
        assert terms.is_post_money is False
        assert terms.discount == Decimal("0.2")

    def test_mfn_safe(self) -> None:
        data = {"is_post_money": True, "mfn": True}
        terms = _parse_safe_terms(data)
        assert terms.mfn is True
        assert terms.valuation_cap is None

    def test_capitalization_definition_default(self) -> None:
        data = {"valuation_cap": 5000000}
        terms = _parse_safe_terms(data)
        assert terms.capitalization_definition == CapDefinition.ALL_OUTSTANDING


# ---------------------------------------------------------------------------
# _parse_note_terms()
# ---------------------------------------------------------------------------


class TestParseNoteTerms:
    def test_simple_interest(self) -> None:
        data = {
            "valuation_cap": 10000000,
            "discount": 0.2,
            "interest_rate": 0.08,
            "interest_type": "simple",
            "months_outstanding": 12,
        }
        terms = _parse_note_terms(data)
        assert terms.valuation_cap == Decimal("10000000")
        assert terms.discount == Decimal("0.2")
        assert terms.interest_rate == Decimal("0.08")
        assert terms.interest_type == InterestType.SIMPLE
        assert terms.months_outstanding == 12
        assert terms.compounding_frequency == 12  # default

    def test_compound_interest(self) -> None:
        data = {
            "valuation_cap": 10000000,
            "interest_rate": 0.08,
            "interest_type": "compound",
            "compounding_frequency": 4,
            "months_outstanding": 18,
        }
        terms = _parse_note_terms(data)
        assert terms.interest_type == InterestType.COMPOUND
        assert terms.compounding_frequency == 4
        assert terms.months_outstanding == 18

    def test_defaults(self) -> None:
        data: dict = {}
        terms = _parse_note_terms(data)
        assert terms.valuation_cap is None
        assert terms.discount is None
        assert terms.interest_rate == Decimal(0)
        assert terms.interest_type == InterestType.SIMPLE
        assert terms.compounding_frequency == 12
        assert terms.months_outstanding == 0


# ---------------------------------------------------------------------------
# _get_capitalization()
# ---------------------------------------------------------------------------


class TestGetCapitalization:
    def _make_holders(self) -> list[Holder]:
        return [
            Holder(name="A", instrument=InstrumentType.COMMON, shares=Decimal("6000")),
            Holder(
                name="B", instrument=InstrumentType.PREFERRED, shares=Decimal("2000")
            ),
            Holder(name="C", instrument=InstrumentType.OPTIONS, shares=Decimal("1000")),
            Holder(
                name="D",
                instrument=InstrumentType.SAFE_POST,
                shares=Decimal("500"),
            ),
        ]

    def test_all_outstanding(self) -> None:
        holders = self._make_holders()
        total_shares = Decimal("9500")
        result = _get_capitalization(
            holders, total_shares, CapDefinition.ALL_OUTSTANDING
        )
        assert result == Decimal("9500")

    def test_shares_only(self) -> None:
        holders = self._make_holders()
        total_shares = Decimal("9500")
        result = _get_capitalization(holders, total_shares, CapDefinition.SHARES_ONLY)
        # common (6000) + preferred (2000)
        assert result == Decimal("8000")

    def test_shares_and_options(self) -> None:
        holders = self._make_holders()
        total_shares = Decimal("9500")
        result = _get_capitalization(
            holders, total_shares, CapDefinition.SHARES_AND_OPTIONS
        )
        # common (6000) + preferred (2000) + options (1000)
        assert result == Decimal("9000")
