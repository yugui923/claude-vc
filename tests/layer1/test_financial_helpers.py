"""Unit tests for _d() and _fmt() helper functions in financial_model."""

from __future__ import annotations

from decimal import Decimal

from financial_model import _d, _fmt


def test_d_from_string() -> None:
    result = _d("123.45")
    assert result == Decimal("123.45")
    assert isinstance(result, Decimal)


def test_d_from_int() -> None:
    result = _d(42)
    assert result == Decimal("42")
    assert isinstance(result, Decimal)


def test_d_from_decimal() -> None:
    original = Decimal("99.99")
    result = _d(original)
    assert result is original


def test_d_from_float() -> None:
    result = _d(1.5)
    assert result == Decimal("1.5")


def test_fmt_zero_places() -> None:
    result = _fmt(Decimal("1234.567"), places=0)
    assert result == "1235"


def test_fmt_two_places() -> None:
    result = _fmt(Decimal("1234.5"), places=2)
    assert result == "1234.50"


def test_fmt_rounding_half_up() -> None:
    # 0.5 rounds up with ROUND_HALF_UP
    assert _fmt(Decimal("2.5"), places=0) == "3"
    assert _fmt(Decimal("3.5"), places=0) == "4"


def test_fmt_rounding_two_places() -> None:
    assert _fmt(Decimal("1.2350"), places=2) == "1.24"
    assert _fmt(Decimal("1.2349"), places=2) == "1.23"


def test_fmt_negative_value() -> None:
    assert _fmt(Decimal("-500.6"), places=0) == "-501"


def test_fmt_zero_value() -> None:
    assert _fmt(Decimal("0"), places=2) == "0.00"
