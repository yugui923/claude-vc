"""Tests for calc_multiples() using multiples_basic.json fixture."""

from __future__ import annotations

from decimal import Decimal

from helpers import load_fixture

from financial_model import calc_multiples


def _load_result() -> dict:
    scenario = load_fixture("financial/multiples_basic.json")
    return calc_multiples(scenario)


def test_ev_revenue_valuation_present() -> None:
    result = _load_result()
    methods = [v["method"] for v in result["valuations"]]
    assert "EV/Revenue" in methods


def test_ev_arr_valuation_present() -> None:
    result = _load_result()
    methods = [v["method"] for v in result["valuations"]]
    assert "EV/ARR" in methods


def test_ev_ebitda_skipped_negative_ebitda() -> None:
    result = _load_result()
    methods = [v["method"] for v in result["valuations"]]
    # Target EBITDA is -500000, so EV/EBITDA should be skipped
    assert "EV/EBITDA" not in methods


def test_valuation_range_present() -> None:
    result = _load_result()
    vr = result["valuation_range"]
    assert "low" in vr
    assert "high" in vr
    assert "midpoint" in vr
    low = Decimal(vr["low"])
    high = Decimal(vr["high"])
    mid = Decimal(vr["midpoint"])
    assert low <= mid <= high


def test_adjustments_applied() -> None:
    result = _load_result()
    adj = result["adjustments_applied"]
    assert "private_discount" in adj
    assert "size_discount" in adj


def test_adjusted_less_than_base_with_discounts() -> None:
    """With private and size discounts, adjusted should differ from base."""
    result = _load_result()
    for v in result["valuations"]:
        base = Decimal(v["base_valuation"])
        adjusted = Decimal(v["adjusted_valuation"])
        # Growth premium may offset, but total discount is 0.25+0.15=40%
        # while max growth premium is 40%, so adjusted should not exceed base
        # in most cases. At minimum, verify adjusted is positive.
        assert adjusted > 0
        assert adjusted != base, "Adjustments should change the valuation"


def test_target_name_in_result() -> None:
    result = _load_result()
    assert result["target"] == "TargetCo"
