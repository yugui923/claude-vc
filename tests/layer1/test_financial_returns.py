"""Tests for calc_returns() using returns_basic.json fixture."""

from __future__ import annotations

from decimal import Decimal

from helpers import load_fixture, run_financial

from financial_model import calc_returns


def _load_result() -> dict:
    scenario = load_fixture("financial/returns_basic.json")
    return calc_returns(scenario)


def test_moic_equals_total_value_over_invested() -> None:
    scenario = load_fixture("financial/returns_basic.json")
    result = calc_returns(scenario)
    # Check first investment: AlphaWidget
    inv = result["investments"][0]
    alpha = scenario["investments"][0]
    dists = sum(Decimal(str(d["amount"])) for d in alpha["distributions"])
    nav = Decimal(str(alpha["current_nav"]))
    invested = Decimal(str(alpha["investment_amount"]))
    expected_moic = (dists + nav) / invested
    actual_moic = Decimal(inv["moic"].rstrip("x"))
    assert actual_moic == expected_moic


def test_dpi_equals_distributions_over_invested() -> None:
    result = _load_result()
    # AlphaWidget: fully exited, distributions = 200000 + 1500000 = 1700000
    inv = result["investments"][0]
    expected_dpi = Decimal("1700000") / Decimal("500000")
    actual_dpi = Decimal(inv["dpi"].rstrip("x"))
    assert actual_dpi == expected_dpi


def test_tvpi_equals_moic() -> None:
    result = _load_result()
    for inv in result["investments"]:
        moic = Decimal(inv["moic"].rstrip("x"))
        tvpi = Decimal(inv["tvpi"].rstrip("x"))
        assert moic == tvpi


def test_irr_within_expected_range() -> None:
    result = _load_result()
    # AlphaWidget: 500K in, 1.7M out over ~3.4 years = strong positive IRR
    irr_str = result["investments"][0]["irr"]
    irr = Decimal(irr_str.rstrip("%"))
    assert irr > Decimal("10"), f"AlphaWidget IRR {irr}% seems too low"
    assert irr < Decimal("200"), f"AlphaWidget IRR {irr}% seems unreasonably high"


def test_irr_fallback_no_distributions() -> None:
    """BetaCloud has no distributions -- IRR should still compute from NAV."""
    result = _load_result()
    inv = result["investments"][1]
    irr_str = inv["irr"]
    irr = Decimal(irr_str.rstrip("%"))
    assert irr > 0, "BetaCloud IRR should be positive (NAV > invested)"


def test_pme_present_when_benchmark_provided() -> None:
    result = _load_result()
    for inv in result["investments"]:
        assert "pme" in inv, f"PME missing for {inv['name']}"
    assert "pme" in result["portfolio"]


def test_portfolio_aggregate_totals() -> None:
    scenario = load_fixture("financial/returns_basic.json")
    result = calc_returns(scenario)
    portfolio = result["portfolio"]

    expected_invested = sum(
        Decimal(str(inv["investment_amount"])) for inv in scenario["investments"]
    )
    expected_nav = sum(
        Decimal(str(inv.get("current_nav", 0))) for inv in scenario["investments"]
    )
    expected_dists = Decimal(0)
    for inv in scenario["investments"]:
        for d in inv.get("distributions", []):
            expected_dists += Decimal(str(d["amount"]))

    assert Decimal(portfolio["total_invested"]) == expected_invested
    assert Decimal(portfolio["total_nav"]) == expected_nav
    assert Decimal(portfolio["total_distributions"]) == expected_dists


def test_assessment_strings_present() -> None:
    result = _load_result()
    assessment = result["assessment"]
    for key in ("moic", "irr", "dpi"):
        assert key in assessment
        assert isinstance(assessment[key], str)
        assert len(assessment[key]) > 0


def test_returns_cli_integration() -> None:
    result = run_financial("returns", "returns_basic.json")
    assert isinstance(result, dict)
    assert "investments" in result
    assert "portfolio" in result
    assert len(result["investments"]) == 3
