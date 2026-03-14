"""Tests for calc_three_statement() using three_statement fixtures.

CRITICAL: These tests validate internal consistency of the 3-statement model.
"""

from __future__ import annotations

from decimal import Decimal

from helpers import load_fixture

from financial_model import calc_three_statement


def _load_basic() -> dict:
    scenario = load_fixture("financial/three_statement_basic.json")
    return calc_three_statement(scenario)


def _load_equity() -> dict:
    scenario = load_fixture("financial/three_statement_equity.json")
    return calc_three_statement(scenario)


# ---------------------------------------------------------------------------
# Balance sheet: A = L + E
# ---------------------------------------------------------------------------


def test_assets_equal_liabilities_plus_equity_basic() -> None:
    result = _load_basic()
    for bs in result["balance_sheet"]:
        total_assets = Decimal(bs["total_assets"])
        total_le = Decimal(bs["total_liabilities_equity"])
        assert total_assets == total_le, (
            f"Year {bs['year']}: A ({total_assets}) != L+E ({total_le})"
        )


def test_assets_equal_liabilities_plus_equity_equity() -> None:
    result = _load_equity()
    for bs in result["balance_sheet"]:
        total_assets = Decimal(bs["total_assets"])
        total_le = Decimal(bs["total_liabilities_equity"])
        assert total_assets == total_le, (
            f"Year {bs['year']}: A ({total_assets}) != L+E ({total_le})"
        )


# ---------------------------------------------------------------------------
# Cash consistency: ending cash in CF == cash in BS
# ---------------------------------------------------------------------------


def test_ending_cash_cf_equals_bs_basic() -> None:
    result = _load_basic()
    for cf, bs in zip(result["cash_flow_statement"], result["balance_sheet"]):
        cf_cash = Decimal(cf["ending_cash"])
        bs_cash = Decimal(bs["cash"])
        assert cf_cash == bs_cash, (
            f"Year {cf['year']}: CF ending cash ({cf_cash}) != BS cash ({bs_cash})"
        )


def test_ending_cash_cf_equals_bs_equity() -> None:
    result = _load_equity()
    for cf, bs in zip(result["cash_flow_statement"], result["balance_sheet"]):
        cf_cash = Decimal(cf["ending_cash"])
        bs_cash = Decimal(bs["cash"])
        assert cf_cash == bs_cash, (
            f"Year {cf['year']}: CF ending cash ({cf_cash}) != BS cash ({bs_cash})"
        )


# ---------------------------------------------------------------------------
# Net income consistency: IS net_income == CF net_income
# ---------------------------------------------------------------------------


def test_net_income_is_equals_cf_basic() -> None:
    result = _load_basic()
    for is_stmt, cf in zip(result["income_statement"], result["cash_flow_statement"]):
        is_ni = Decimal(is_stmt["net_income"])
        cf_ni = Decimal(cf["net_income"])
        assert is_ni == cf_ni, (
            f"Year {is_stmt['year']}: IS NI ({is_ni}) != CF NI ({cf_ni})"
        )


def test_net_income_is_equals_cf_equity() -> None:
    result = _load_equity()
    for is_stmt, cf in zip(result["income_statement"], result["cash_flow_statement"]):
        is_ni = Decimal(is_stmt["net_income"])
        cf_ni = Decimal(cf["net_income"])
        assert is_ni == cf_ni, (
            f"Year {is_stmt['year']}: IS NI ({is_ni}) != CF NI ({cf_ni})"
        )


# ---------------------------------------------------------------------------
# Income statement internal consistency
# ---------------------------------------------------------------------------


def test_gross_profit_equals_revenue_minus_cogs() -> None:
    result = _load_basic()
    for stmt in result["income_statement"]:
        revenue = Decimal(stmt["revenue"])
        cogs = Decimal(stmt["cogs"])
        gp = Decimal(stmt["gross_profit"])
        assert gp == revenue - cogs, (
            f"Year {stmt['year']}: GP ({gp}) != Rev-COGS ({revenue - cogs})"
        )


def test_ebitda_equals_gross_profit_minus_opex() -> None:
    result = _load_basic()
    for stmt in result["income_statement"]:
        gp = Decimal(stmt["gross_profit"])
        opex = Decimal(stmt["total_opex"])
        ebitda = Decimal(stmt["ebitda"])
        # Allow +/- 1 for independent rounding of each component
        assert abs(ebitda - (gp - opex)) <= 1, (
            f"Year {stmt['year']}: EBITDA ({ebitda}) != GP-OpEx ({gp - opex})"
        )


# ---------------------------------------------------------------------------
# Cash flow internal consistency
# ---------------------------------------------------------------------------


def test_operating_cf_formula() -> None:
    """Operating CF = net_income + depreciation - delta_AR + delta_AP."""
    result = _load_basic()
    for cf in result["cash_flow_statement"]:
        ni = Decimal(cf["net_income"])
        dep = Decimal(cf["depreciation_add_back"])
        # change_in_ar is stored as negative of the delta (since AR increase is cash outflow)
        change_ar = Decimal(cf["change_in_ar"])
        change_ap = Decimal(cf["change_in_ap"])
        ocf = Decimal(cf["operating_cash_flow"])
        expected = ni + dep + change_ar + change_ap
        # Allow +/- 1 for independent rounding of each component
        assert abs(ocf - expected) <= 1, (
            f"Year {cf['year']}: OCF ({ocf}) != expected ({expected})"
        )


# ---------------------------------------------------------------------------
# Equity injection
# ---------------------------------------------------------------------------


def test_equity_injection_increases_cash() -> None:
    """In three_statement_equity, year 2 has a $10M injection. Cash should jump."""
    result = _load_equity()
    bs = result["balance_sheet"]
    # Find year 2 cash flow
    cf_year2 = result["cash_flow_statement"][1]
    assert Decimal(cf_year2["equity_raised"]) == Decimal("10000000")

    # Cash in year 2 should be substantially higher than year 1 due to injection
    year1_cash = Decimal(bs[0]["cash"])
    year2_cash = Decimal(bs[1]["cash"])
    # The injection is $10M so even with operating losses, year 2 cash should exceed year 1
    assert year2_cash > year1_cash, (
        f"Equity injection should increase cash: Y1={year1_cash}, Y2={year2_cash}"
    )


def test_equity_injection_reflected_in_financing_cf() -> None:
    result = _load_equity()
    cf_year2 = result["cash_flow_statement"][1]
    assert Decimal(cf_year2["financing_cash_flow"]) == Decimal("10000000")
