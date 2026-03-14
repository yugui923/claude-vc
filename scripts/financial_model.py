#!/usr/bin/env python3
"""Financial modeling: DCF, unit economics, revenue projections.

Usage:
    python3 financial_model.py <command> [options]

Commands:
    dcf             Discounted cash flow valuation
    unit_economics  CAC, LTV, payback period, margins
    projections     Revenue and expense projections
    multiples       Comparable company valuation via multiples

Input is always a JSON file (--input). Output is JSON to stdout.
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from typing import Any


def _d(val: Any) -> Decimal:
    if isinstance(val, Decimal):
        return val
    return Decimal(str(val))


def _fmt(val: Decimal, places: int = 0) -> str:
    if places == 0:
        return str(val.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    q = Decimal(10) ** -places
    return str(val.quantize(q, rounding=ROUND_HALF_UP))


# ---------------------------------------------------------------------------
# DCF
# ---------------------------------------------------------------------------


def calc_dcf(scenario: dict[str, Any]) -> dict[str, Any]:
    """Discounted cash flow valuation.

    Expected JSON:
    {
        "cash_flows": [100000, 200000, 350000, 500000, 700000],
        "discount_rate": 0.50,
        "terminal_growth_rate": 0.03,
        "terminal_method": "gordon" | "exit_multiple",
        "exit_multiple": 10,
        "net_debt": 0,
        "shares_outstanding": 10000000
    }
    """
    cfs = [_d(cf) for cf in scenario["cash_flows"]]
    r = _d(scenario["discount_rate"])
    terminal_method = scenario.get("terminal_method", "gordon")
    net_debt = _d(scenario.get("net_debt", 0))
    shares = _d(scenario.get("shares_outstanding", 1))

    # PV of projected cash flows
    pv_cfs = []
    total_pv = Decimal(0)
    for i, cf in enumerate(cfs, 1):
        discount_factor = (1 + r) ** i
        pv = cf / discount_factor
        pv_cfs.append(
            {
                "year": i,
                "cash_flow": _fmt(cf),
                "discount_factor": _fmt(discount_factor, 4),
                "present_value": _fmt(pv),
            }
        )
        total_pv += pv

    # Terminal value
    last_cf = cfs[-1]
    n = len(cfs)

    if terminal_method == "gordon":
        g = _d(scenario.get("terminal_growth_rate", "0.03"))
        if r <= g:
            return {
                "error": "Discount rate must exceed terminal growth rate for Gordon Growth model"
            }
        tv = last_cf * (1 + g) / (r - g)
    else:
        multiple = _d(scenario.get("exit_multiple", 10))
        tv = last_cf * multiple

    tv_pv = tv / ((1 + r) ** n)

    enterprise_value = total_pv + tv_pv
    equity_value = enterprise_value - net_debt
    per_share = equity_value / shares if shares > 0 else Decimal(0)

    return {
        "projected_cash_flows": pv_cfs,
        "pv_of_cash_flows": _fmt(total_pv),
        "terminal_value": _fmt(tv),
        "terminal_method": terminal_method,
        "pv_of_terminal_value": _fmt(tv_pv),
        "enterprise_value": _fmt(enterprise_value),
        "net_debt": _fmt(net_debt),
        "equity_value": _fmt(equity_value),
        "shares_outstanding": _fmt(shares),
        "value_per_share": _fmt(per_share, 4),
        "terminal_pct_of_total": _fmt(tv_pv / enterprise_value * 100, 1) + "%",
    }


# ---------------------------------------------------------------------------
# Unit Economics
# ---------------------------------------------------------------------------


def calc_unit_economics(scenario: dict[str, Any]) -> dict[str, Any]:
    """Calculate unit economics metrics.

    Expected JSON:
    {
        "monthly_revenue": 100000,
        "total_customers": 500,
        "new_customers_per_month": 50,
        "monthly_churn_rate": 0.03,
        "gross_margin": 0.80,
        "sales_marketing_spend_monthly": 75000,
        "avg_contract_value_monthly": null,
        "avg_contract_value_annual": 2400,
        "expansion_revenue_monthly": 5000
    }
    """
    monthly_rev = _d(scenario["monthly_revenue"])
    customers = _d(scenario["total_customers"])
    new_custs = _d(scenario["new_customers_per_month"])
    churn = _d(scenario["monthly_churn_rate"])
    gross_margin = _d(scenario["gross_margin"])
    sm_spend = _d(scenario["sales_marketing_spend_monthly"])

    # ARPU
    arpu_monthly = monthly_rev / customers if customers > 0 else Decimal(0)
    arpu_annual = arpu_monthly * 12

    # CAC
    cac = sm_spend / new_custs if new_custs > 0 else Decimal(0)

    # LTV (simple: ARPU * gross margin / churn)
    if churn > 0:
        avg_lifetime_months = Decimal(1) / churn
        ltv = arpu_monthly * gross_margin / churn
    else:
        avg_lifetime_months = Decimal("999")
        ltv = arpu_monthly * gross_margin * 60  # cap at 5 years

    ltv_cac_ratio = ltv / cac if cac > 0 else Decimal("999")

    # CAC payback (months)
    monthly_gross_profit_per_cust = arpu_monthly * gross_margin
    cac_payback = (
        cac / monthly_gross_profit_per_cust
        if monthly_gross_profit_per_cust > 0
        else Decimal("999")
    )

    # Net revenue retention
    expansion = _d(scenario.get("expansion_revenue_monthly", 0))
    beginning_rev = monthly_rev - expansion + (monthly_rev * churn)
    nrr = monthly_rev / beginning_rev * 100 if beginning_rev > 0 else Decimal(100)

    # Magic number (annualized net new ARR / prior quarter S&M)
    net_new_arr = new_custs * arpu_annual - (customers * churn * arpu_annual)
    quarterly_sm = sm_spend * 3
    magic_number = net_new_arr / quarterly_sm if quarterly_sm > 0 else Decimal(0)

    # Rule of 40
    arr = monthly_rev * 12
    growth_rate = (
        (new_custs - customers * churn) / customers * 100
        if customers > 0
        else Decimal(0)
    )
    # Approximate FCF margin from gross margin and S&M ratio
    sm_pct = sm_spend / monthly_rev * 100 if monthly_rev > 0 else Decimal(0)
    approx_margin = gross_margin * 100 - sm_pct
    rule_of_40 = growth_rate + approx_margin

    return {
        "arpu_monthly": _fmt(arpu_monthly, 2),
        "arpu_annual": _fmt(arpu_annual, 2),
        "cac": _fmt(cac, 2),
        "ltv": _fmt(ltv, 2),
        "ltv_cac_ratio": _fmt(ltv_cac_ratio, 2),
        "cac_payback_months": _fmt(cac_payback, 1),
        "avg_customer_lifetime_months": _fmt(avg_lifetime_months, 1),
        "gross_margin_pct": _fmt(gross_margin * 100, 1) + "%",
        "net_revenue_retention_pct": _fmt(nrr, 1) + "%",
        "magic_number": _fmt(magic_number, 2),
        "arr": _fmt(arr),
        "monthly_burn_rate": _fmt(sm_spend + monthly_rev * (1 - gross_margin)),
        "rule_of_40_score": _fmt(rule_of_40, 1),
        "assessment": {
            "ltv_cac": "Healthy (>3x)"
            if ltv_cac_ratio >= 3
            else "Concerning (<3x)"
            if ltv_cac_ratio >= 1
            else "Unsustainable (<1x)",
            "cac_payback": "Good (<12mo)"
            if cac_payback < 12
            else "Acceptable (12-18mo)"
            if cac_payback < 18
            else "Slow (>18mo)",
            "nrr": "Excellent (>120%)"
            if nrr > 120
            else "Good (>100%)"
            if nrr > 100
            else "Net contraction (<100%)",
            "rule_of_40": "Above threshold" if rule_of_40 >= 40 else "Below threshold",
        },
    }


# ---------------------------------------------------------------------------
# Revenue Projections
# ---------------------------------------------------------------------------


def calc_projections(scenario: dict[str, Any]) -> dict[str, Any]:
    """Project revenue and expenses forward.

    Expected JSON:
    {
        "current_arr": 1200000,
        "growth_rates": [1.0, 0.8, 0.6, 0.4, 0.3],
        "gross_margin": 0.80,
        "opex_pct_of_revenue": 0.90,
        "opex_improvement_per_year": 0.05,
        "starting_cash": 5000000,
        "monthly_burn": 150000,
        "fundraise_in_month": null,
        "fundraise_amount": null
    }
    """
    arr = _d(scenario["current_arr"])
    growth_rates = [_d(g) for g in scenario["growth_rates"]]
    gm = _d(scenario["gross_margin"])
    opex_pct = _d(scenario["opex_pct_of_revenue"])
    opex_improve = _d(scenario.get("opex_improvement_per_year", "0.05"))
    starting_cash = _d(scenario.get("starting_cash", 0))
    monthly_burn = _d(scenario.get("monthly_burn", 0))

    projections = []
    cash = starting_cash
    runway_months = None

    for i, rate in enumerate(growth_rates):
        year = i + 1
        arr = arr * (1 + rate)
        revenue = arr
        gross_profit = revenue * gm
        opex = revenue * opex_pct
        ebitda = gross_profit - opex
        ebitda_margin = ebitda / revenue * 100 if revenue > 0 else Decimal(0)
        fcf = ebitda  # simplified

        # Cash position (simplified annual)
        cash += fcf

        projections.append(
            {
                "year": year,
                "arr": _fmt(arr),
                "yoy_growth": _fmt(rate * 100, 1) + "%",
                "revenue": _fmt(revenue),
                "gross_profit": _fmt(gross_profit),
                "gross_margin": _fmt(gm * 100, 1) + "%",
                "opex": _fmt(opex),
                "ebitda": _fmt(ebitda),
                "ebitda_margin": _fmt(ebitda_margin, 1) + "%",
                "ending_cash": _fmt(cash),
            }
        )

        opex_pct = max(Decimal("0.3"), opex_pct - opex_improve)

    # Runway calculation
    if monthly_burn > 0 and starting_cash > 0:
        runway_months = int(starting_cash / monthly_burn)

    # Break-even year
    breakeven_year = None
    for p in projections:
        if Decimal(p["ebitda"]) > 0:
            breakeven_year = p["year"]
            break

    return {
        "projections": projections,
        "starting_arr": _fmt(_d(scenario["current_arr"])),
        "ending_arr": _fmt(arr),
        "total_growth": _fmt((arr / _d(scenario["current_arr"]) - 1) * 100, 1) + "%",
        "runway_months": runway_months,
        "breakeven_year": breakeven_year,
    }


# ---------------------------------------------------------------------------
# Comparable Multiples Valuation
# ---------------------------------------------------------------------------


def calc_multiples(scenario: dict[str, Any]) -> dict[str, Any]:
    """Value a company using comparable multiples.

    Expected JSON:
    {
        "target": {
            "name": "TargetCo",
            "arr": 5000000,
            "revenue": 4500000,
            "ebitda": -500000,
            "yoy_growth": 0.80,
            "gross_margin": 0.82
        },
        "comparables": [
            {"name": "CompA", "ev_revenue": 12, "ev_arr": 14, "ev_ebitda": null,
             "yoy_growth": 0.50, "gross_margin": 0.78}
        ],
        "adjustments": {
            "private_discount": 0.25,
            "growth_premium": true,
            "size_discount": 0.15
        }
    }
    """
    target = scenario["target"]
    comps = scenario["comparables"]
    adj = scenario.get("adjustments", {})

    # Calculate median multiples
    ev_rev_multiples = [_d(c["ev_revenue"]) for c in comps if c.get("ev_revenue")]
    ev_arr_multiples = [_d(c["ev_arr"]) for c in comps if c.get("ev_arr")]
    ev_ebitda_multiples = [_d(c["ev_ebitda"]) for c in comps if c.get("ev_ebitda")]

    results: dict[str, Any] = {"target": target["name"], "valuations": []}

    def _median(vals: list[Decimal]) -> Decimal:
        if not vals:
            return Decimal(0)
        s = sorted(vals)
        n = len(s)
        if n % 2 == 0:
            return (s[n // 2 - 1] + s[n // 2]) / 2
        return s[n // 2]

    def _apply_adjustments(base_val: Decimal) -> Decimal:
        val = base_val
        if adj.get("private_discount"):
            val *= 1 - _d(adj["private_discount"])
        if adj.get("size_discount"):
            val *= 1 - _d(adj["size_discount"])
        if adj.get("growth_premium") and target.get("yoy_growth"):
            # Compare target growth to comp median
            comp_growths = [_d(c["yoy_growth"]) for c in comps if c.get("yoy_growth")]
            if comp_growths:
                median_growth = _median(comp_growths)
                target_growth = _d(target["yoy_growth"])
                if target_growth > median_growth:
                    premium = min(
                        (target_growth - median_growth) * Decimal("0.5"), Decimal("0.4")
                    )
                    val *= 1 + premium
        return val

    # EV/Revenue
    if ev_rev_multiples and target.get("revenue"):
        med = _median(ev_rev_multiples)
        base = med * _d(target["revenue"])
        adjusted = _apply_adjustments(base)
        results["valuations"].append(
            {
                "method": "EV/Revenue",
                "median_multiple": _fmt(med, 1) + "x",
                "base_valuation": _fmt(base),
                "adjusted_valuation": _fmt(adjusted),
            }
        )

    # EV/ARR
    if ev_arr_multiples and target.get("arr"):
        med = _median(ev_arr_multiples)
        base = med * _d(target["arr"])
        adjusted = _apply_adjustments(base)
        results["valuations"].append(
            {
                "method": "EV/ARR",
                "median_multiple": _fmt(med, 1) + "x",
                "base_valuation": _fmt(base),
                "adjusted_valuation": _fmt(adjusted),
            }
        )

    # EV/EBITDA
    if ev_ebitda_multiples and target.get("ebitda") and _d(target["ebitda"]) > 0:
        med = _median(ev_ebitda_multiples)
        base = med * _d(target["ebitda"])
        adjusted = _apply_adjustments(base)
        results["valuations"].append(
            {
                "method": "EV/EBITDA",
                "median_multiple": _fmt(med, 1) + "x",
                "base_valuation": _fmt(base),
                "adjusted_valuation": _fmt(adjusted),
            }
        )

    # Summary range
    if results["valuations"]:
        vals = [_d(v["adjusted_valuation"]) for v in results["valuations"]]
        results["valuation_range"] = {
            "low": _fmt(min(vals)),
            "high": _fmt(max(vals)),
            "midpoint": _fmt(sum(vals) / len(vals)),
        }
        results["adjustments_applied"] = {k: v for k, v in adj.items() if v}

    return results


# ---------------------------------------------------------------------------
# Three-Statement Financial Model
# ---------------------------------------------------------------------------


def calc_three_statement(scenario: dict[str, Any]) -> dict[str, Any]:
    """Generate a simplified 3-statement financial model.

    Expected JSON:
    {
        "company_name": "ExampleCo",
        "projection_years": 5,
        "income_statement": {
            "revenue_year_0": 1200000,
            "revenue_growth_rates": [1.0, 0.8, 0.6, 0.4, 0.3],
            "cogs_pct_of_revenue": 0.20,
            "cogs_improvement_per_year": 0.01,
            "opex_breakdown": {
                "sales_marketing_pct": 0.40,
                "research_development_pct": 0.25,
                "general_admin_pct": 0.15
            },
            "opex_improvement_per_year": 0.03,
            "depreciation_pct_of_revenue": 0.02,
            "interest_expense_annual": 0,
            "tax_rate": 0.0
        },
        "balance_sheet": {
            "starting_cash": 5000000,
            "accounts_receivable_days": 45,
            "accounts_payable_days": 30,
            "debt_balance": 0,
            "other_assets": 0,
            "equity_injections": []
        },
        "cash_flow": {
            "capex_pct_of_revenue": 0.03,
            "working_capital_change_auto": true
        }
    }
    """
    is_cfg = scenario.get("income_statement", {})
    bs_cfg = scenario.get("balance_sheet", {})
    cf_cfg = scenario.get("cash_flow", {})

    revenue = _d(is_cfg.get("revenue_year_0", 0))
    growth_rates = [_d(g) for g in is_cfg.get("revenue_growth_rates", [])]
    n_years = int(scenario.get("projection_years", len(growth_rates)))

    # Pad growth rates if needed
    while len(growth_rates) < n_years:
        growth_rates.append(growth_rates[-1] if growth_rates else Decimal("0.2"))

    cogs_pct = _d(is_cfg.get("cogs_pct_of_revenue", "0.20"))
    cogs_improve = _d(is_cfg.get("cogs_improvement_per_year", 0))
    opex_bk = is_cfg.get("opex_breakdown", {})
    sm_pct = _d(opex_bk.get("sales_marketing_pct", "0.40"))
    rd_pct = _d(opex_bk.get("research_development_pct", "0.25"))
    ga_pct = _d(opex_bk.get("general_admin_pct", "0.15"))
    opex_improve = _d(is_cfg.get("opex_improvement_per_year", "0.03"))
    dep_pct = _d(is_cfg.get("depreciation_pct_of_revenue", "0.02"))
    interest = _d(is_cfg.get("interest_expense_annual", 0))
    tax_rate = _d(is_cfg.get("tax_rate", 0))

    starting_cash = _d(bs_cfg.get("starting_cash", 0))
    ar_days = _d(bs_cfg.get("accounts_receivable_days", 45))
    ap_days = _d(bs_cfg.get("accounts_payable_days", 30))
    debt = _d(bs_cfg.get("debt_balance", 0))
    other_assets = _d(bs_cfg.get("other_assets", 0))
    equity_injections = bs_cfg.get("equity_injections", [])

    capex_pct = _d(cf_cfg.get("capex_pct_of_revenue", "0.03"))

    income_statements = []
    balance_sheets = []
    cash_flows = []

    cash = starting_cash
    prev_ar = Decimal(0)
    prev_ap = Decimal(0)
    cumulative_net_income = Decimal(0)

    for i in range(n_years):
        year = i + 1
        revenue = revenue * (1 + growth_rates[i])

        # Income Statement
        cogs = revenue * cogs_pct
        gross_profit = revenue - cogs
        gm = gross_profit / revenue * 100 if revenue > 0 else Decimal(0)

        sm_exp = revenue * sm_pct
        rd_exp = revenue * rd_pct
        ga_exp = revenue * ga_pct
        total_opex = sm_exp + rd_exp + ga_exp

        ebitda = gross_profit - total_opex
        ebitda_margin = ebitda / revenue * 100 if revenue > 0 else Decimal(0)

        depreciation = revenue * dep_pct
        ebit = ebitda - depreciation
        ebt = ebit - interest
        tax = max(Decimal(0), ebt * tax_rate)
        net_income = ebt - tax

        income_statements.append(
            {
                "year": year,
                "revenue": _fmt(revenue),
                "cogs": _fmt(cogs),
                "gross_profit": _fmt(gross_profit),
                "gross_margin_pct": _fmt(gm, 1) + "%",
                "sales_marketing": _fmt(sm_exp),
                "research_development": _fmt(rd_exp),
                "general_admin": _fmt(ga_exp),
                "total_opex": _fmt(total_opex),
                "ebitda": _fmt(ebitda),
                "ebitda_margin_pct": _fmt(ebitda_margin, 1) + "%",
                "depreciation": _fmt(depreciation),
                "ebit": _fmt(ebit),
                "interest_expense": _fmt(interest),
                "ebt": _fmt(ebt),
                "tax": _fmt(tax),
                "net_income": _fmt(net_income),
            }
        )

        # Balance Sheet
        ar = revenue * ar_days / Decimal(365)
        cogs_annual = cogs
        ap = cogs_annual * ap_days / Decimal(365)

        # Equity injection for this year
        yr_injection = Decimal(0)
        for inj in equity_injections:
            if int(inj.get("year", 0)) == year:
                yr_injection = _d(inj["amount"])

        # Cash Flow Statement
        change_ar = ar - prev_ar
        change_ap = ap - prev_ap
        operating_cf = net_income + depreciation - change_ar + change_ap

        capex = revenue * capex_pct
        investing_cf = -capex

        financing_cf = yr_injection
        net_change = operating_cf + investing_cf + financing_cf
        cash = cash + net_change

        cumulative_net_income += net_income

        total_assets = cash + ar + other_assets
        total_liabilities = ap + debt
        equity = total_assets - total_liabilities

        balance_sheets.append(
            {
                "year": year,
                "cash": _fmt(cash),
                "accounts_receivable": _fmt(ar),
                "other_assets": _fmt(other_assets),
                "total_assets": _fmt(total_assets),
                "accounts_payable": _fmt(ap),
                "debt": _fmt(debt),
                "total_liabilities": _fmt(total_liabilities),
                "equity": _fmt(equity),
                "total_liabilities_equity": _fmt(total_liabilities + equity),
            }
        )

        cash_flows.append(
            {
                "year": year,
                "net_income": _fmt(net_income),
                "depreciation_add_back": _fmt(depreciation),
                "change_in_ar": _fmt(-change_ar),
                "change_in_ap": _fmt(change_ap),
                "operating_cash_flow": _fmt(operating_cf),
                "capex": _fmt(-capex),
                "investing_cash_flow": _fmt(investing_cf),
                "equity_raised": _fmt(yr_injection),
                "debt_change": "0",
                "financing_cash_flow": _fmt(financing_cf),
                "net_change_in_cash": _fmt(net_change),
                "ending_cash": _fmt(cash),
            }
        )

        prev_ar = ar
        prev_ap = ap

        # Improve margins over time
        cogs_pct = max(Decimal("0.05"), cogs_pct - cogs_improve)
        sm_pct = max(Decimal("0.10"), sm_pct - opex_improve * Decimal("0.5"))
        rd_pct = max(Decimal("0.10"), rd_pct - opex_improve * Decimal("0.3"))
        ga_pct = max(Decimal("0.05"), ga_pct - opex_improve * Decimal("0.2"))

    # Summary
    breakeven_year = None
    for stmt in income_statements:
        if Decimal(stmt["net_income"]) > 0:
            breakeven_year = stmt["year"]
            break

    return {
        "company_name": scenario.get("company_name", ""),
        "income_statement": income_statements,
        "balance_sheet": balance_sheets,
        "cash_flow_statement": cash_flows,
        "summary": {
            "projection_years": n_years,
            "starting_revenue": _fmt(_d(is_cfg.get("revenue_year_0", 0))),
            "ending_revenue": income_statements[-1]["revenue"]
            if income_statements
            else "0",
            "break_even_year": breakeven_year,
            "ending_cash": balance_sheets[-1]["cash"] if balance_sheets else "0",
            "terminal_ebitda_margin": income_statements[-1]["ebitda_margin_pct"]
            if income_statements
            else "0%",
        },
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Financial modeling: DCF, unit economics, projections, multiples, 3-statement."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for cmd in ["dcf", "unit_economics", "projections", "multiples", "three_statement"]:
        p = sub.add_parser(cmd)
        p.add_argument("--input", required=True, help="Path to JSON scenario file")

    args = parser.parse_args()

    with open(args.input) as f:
        scenario = json.load(f)

    commands = {
        "dcf": calc_dcf,
        "unit_economics": calc_unit_economics,
        "projections": calc_projections,
        "multiples": calc_multiples,
        "three_statement": calc_three_statement,
    }

    result = commands[args.command](scenario)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
