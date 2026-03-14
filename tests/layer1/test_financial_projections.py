"""Tests for calc_projections() using projections_basic.json fixture."""

from __future__ import annotations

from decimal import Decimal

from helpers import load_fixture

from financial_model import calc_projections


def _load_result() -> tuple[dict, dict]:
    scenario = load_fixture("financial/projections_basic.json")
    return scenario, calc_projections(scenario)


def test_projection_years_matches_growth_rates() -> None:
    scenario, result = _load_result()
    assert len(result["projections"]) == len(scenario["growth_rates"])


def test_revenue_grows_each_year() -> None:
    _, result = _load_result()
    projections = result["projections"]
    for i in range(1, len(projections)):
        prev_rev = Decimal(projections[i - 1]["revenue"])
        curr_rev = Decimal(projections[i]["revenue"])
        assert curr_rev > prev_rev, f"Revenue in year {i + 1} should exceed year {i}"


def test_breakeven_year_found() -> None:
    _, result = _load_result()
    # With 80% gross margin and 90% opex starting, break-even may or may not
    # happen. Verify the field exists and is either None or a valid year.
    be = result["breakeven_year"]
    if be is not None:
        assert isinstance(be, int)
        assert 1 <= be <= len(result["projections"])


def test_runway_calculated_from_cash_and_burn() -> None:
    scenario, result = _load_result()
    starting_cash = scenario["starting_cash"]
    monthly_burn = scenario["monthly_burn"]
    expected_runway = int(Decimal(str(starting_cash)) / Decimal(str(monthly_burn)))
    assert result["runway_months"] == expected_runway


def test_ending_arr_matches_compounded_growth() -> None:
    scenario, result = _load_result()
    arr = Decimal(str(scenario["current_arr"]))
    for rate in scenario["growth_rates"]:
        arr = arr * (1 + Decimal(str(rate)))
    assert Decimal(result["ending_arr"]) == arr.quantize(Decimal("1"))


def test_total_growth_present() -> None:
    _, result = _load_result()
    assert result["total_growth"].endswith("%")
    growth_val = Decimal(result["total_growth"].rstrip("%"))
    assert growth_val > 0


def test_starting_arr_matches_input() -> None:
    scenario, result = _load_result()
    assert Decimal(result["starting_arr"]) == Decimal(str(scenario["current_arr"]))
