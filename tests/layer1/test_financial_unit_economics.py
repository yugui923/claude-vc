"""Tests for calc_unit_economics() using unit_economics_saas.json fixture."""

from __future__ import annotations

from decimal import Decimal

from helpers import load_fixture

from financial_model import calc_unit_economics


def _load_result() -> dict:
    scenario = load_fixture("financial/unit_economics_saas.json")
    return calc_unit_economics(scenario)


def test_arpu_equals_revenue_over_customers() -> None:
    scenario = load_fixture("financial/unit_economics_saas.json")
    result = calc_unit_economics(scenario)
    expected_arpu = Decimal(str(scenario["monthly_revenue"])) / Decimal(
        str(scenario["total_customers"])
    )
    assert Decimal(result["arpu_monthly"]) == expected_arpu


def test_cac_equals_sm_over_new_customers() -> None:
    scenario = load_fixture("financial/unit_economics_saas.json")
    result = calc_unit_economics(scenario)
    expected_cac = Decimal(str(scenario["sales_marketing_spend_monthly"])) / Decimal(
        str(scenario["new_customers_per_month"])
    )
    assert Decimal(result["cac"]) == expected_cac


def test_ltv_cac_ratio_nonnegative() -> None:
    result = _load_result()
    ltv_cac = Decimal(result["ltv_cac_ratio"])
    assert ltv_cac >= 0


def test_assessment_strings_present() -> None:
    result = _load_result()
    assessment = result["assessment"]
    assert "ltv_cac" in assessment
    assert "cac_payback" in assessment
    assert "nrr" in assessment
    assert "rule_of_40" in assessment
    # Each value should be a non-empty string
    for key in ("ltv_cac", "cac_payback", "nrr", "rule_of_40"):
        assert isinstance(assessment[key], str)
        assert len(assessment[key]) > 0


def test_rule_of_40_score_is_number() -> None:
    result = _load_result()
    score = Decimal(result["rule_of_40_score"])
    assert isinstance(score, Decimal)


def test_arr_equals_monthly_revenue_times_12() -> None:
    scenario = load_fixture("financial/unit_economics_saas.json")
    result = calc_unit_economics(scenario)
    expected_arr = Decimal(str(scenario["monthly_revenue"])) * 12
    assert Decimal(result["arr"]) == expected_arr


def test_nrr_is_percentage_string() -> None:
    result = _load_result()
    assert result["net_revenue_retention_pct"].endswith("%")


def test_cac_payback_positive() -> None:
    result = _load_result()
    payback = Decimal(result["cac_payback_months"])
    assert payback > 0
