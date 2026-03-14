"""Tests for calc_dcf() using DCF fixture files."""

from __future__ import annotations

from decimal import Decimal

from helpers import load_fixture, run_financial

from financial_model import calc_dcf


def test_dcf_gordon_enterprise_value() -> None:
    scenario = load_fixture("financial/dcf_gordon.json")
    result = calc_dcf(scenario)
    ev = Decimal(result["enterprise_value"])
    assert ev > 0, "Enterprise value must be positive"


def test_dcf_gordon_equity_value() -> None:
    scenario = load_fixture("financial/dcf_gordon.json")
    result = calc_dcf(scenario)
    ev = Decimal(result["enterprise_value"])
    eq = Decimal(result["equity_value"])
    net_debt = Decimal(result["net_debt"])
    assert eq == ev - net_debt, "equity_value = enterprise_value - net_debt"


def test_dcf_gordon_per_share() -> None:
    scenario = load_fixture("financial/dcf_gordon.json")
    result = calc_dcf(scenario)
    eq = Decimal(result["equity_value"])
    shares = Decimal(result["shares_outstanding"])
    per_share = Decimal(result["value_per_share"])
    # Per-share is equity / shares, both rounded so check within tolerance
    expected = eq / shares
    assert abs(per_share - expected) < Decimal("0.01")


def test_dcf_gordon_terminal_percentage_valid() -> None:
    scenario = load_fixture("financial/dcf_gordon.json")
    result = calc_dcf(scenario)
    pct_str = result["terminal_pct_of_total"]
    assert pct_str.endswith("%")
    pct_val = Decimal(pct_str.rstrip("%"))
    assert Decimal(0) < pct_val < Decimal(100)


def test_dcf_exit_multiple_terminal_value() -> None:
    scenario = load_fixture("financial/dcf_exit_multiple.json")
    result = calc_dcf(scenario)
    # Terminal value should be last_cf * exit_multiple
    last_cf = scenario["cash_flows"][-1]
    multiple = scenario["exit_multiple"]
    expected_tv = Decimal(str(last_cf)) * Decimal(str(multiple))
    assert Decimal(result["terminal_value"]) == expected_tv


def test_dcf_exit_multiple_net_debt_deducted() -> None:
    scenario = load_fixture("financial/dcf_exit_multiple.json")
    result = calc_dcf(scenario)
    ev = Decimal(result["enterprise_value"])
    eq = Decimal(result["equity_value"])
    net_debt = Decimal(result["net_debt"])
    assert net_debt == Decimal("500000")
    assert eq == ev - net_debt


def test_dcf_error_discount_lte_growth() -> None:
    scenario = load_fixture("financial/dcf_error.json")
    result = calc_dcf(scenario)
    assert "error" in result
    assert "Discount rate must exceed" in result["error"]


def test_dcf_gordon_cli_returns_json() -> None:
    result = run_financial("dcf", "dcf_gordon.json")
    assert "enterprise_value" in result
    assert "equity_value" in result
