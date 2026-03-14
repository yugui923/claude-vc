#!/usr/bin/env python3
"""Cap table modeling: ownership, dilution, SAFE conversion, waterfall.

Informed by the Open Cap Table Format (OCF) standard for data modeling.
Uses stock classes with seniority for multi-series waterfall analysis,
supports MFN SAFEs, capitalization definitions, and compound interest.

Usage:
    python3 captable.py <command> [options]

Commands:
    model       Build a cap table from a JSON scenario file
    dilution    Show dilution impact of a new round
    waterfall   Calculate liquidation waterfall / payout distribution
    convert     Convert SAFEs/notes into a priced round
    scenarios   Run waterfall at multiple exit values

Input is always a JSON file (--input). Output is JSON to stdout.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Data model (OCF-informed)
# ---------------------------------------------------------------------------


class InstrumentType(str, Enum):
    COMMON = "common"
    PREFERRED = "preferred"
    SAFE_POST = "safe_post_money"
    SAFE_PRE = "safe_pre_money"
    NOTE = "convertible_note"
    OPTIONS = "options"
    WARRANT = "warrant"


class InterestType(str, Enum):
    SIMPLE = "simple"
    COMPOUND = "compound"


class DayCountConvention(str, Enum):
    ACTUAL_365 = "actual_365"
    ACTUAL_360 = "actual_360"
    THIRTY_360 = "thirty_360"


class CapDefinition(str, Enum):
    ALL_OUTSTANDING = "all_outstanding"
    SHARES_ONLY = "shares_only"
    SHARES_AND_OPTIONS = "shares_and_options"


@dataclass
class StockClass:
    """OCF-informed stock class. Defines terms for a class of shares."""

    class_id: str
    name: str
    instrument_type: InstrumentType
    seniority: int = 1
    liquidation_multiple: Decimal = Decimal(1)
    participating: bool = False
    participation_cap: Decimal | None = None
    conversion_ratio: Decimal = Decimal(1)
    votes_per_share: Decimal = Decimal(1)


@dataclass
class SAFETerms:
    """SAFE conversion parameters (OCF SAFEConversionMechanism)."""

    valuation_cap: Decimal | None = None
    discount: Decimal | None = None
    is_post_money: bool = True
    mfn: bool = False
    exit_multiple: Decimal | None = None
    capitalization_definition: CapDefinition = CapDefinition.ALL_OUTSTANDING


@dataclass
class NoteTerms:
    """Convertible note parameters (OCF NoteConversionMechanism)."""

    valuation_cap: Decimal | None = None
    discount: Decimal | None = None
    interest_rate: Decimal = Decimal(0)
    interest_type: InterestType = InterestType.SIMPLE
    compounding_frequency: int = 12
    months_outstanding: int = 0


@dataclass
class Holder:
    name: str
    instrument: InstrumentType
    shares: Decimal = Decimal(0)
    investment: Decimal = Decimal(0)
    stock_class_id: str | None = None
    safe_terms: SAFETerms | None = None
    note_terms: NoteTerms | None = None
    # Waterfall fields — populated from StockClass during waterfall parsing
    liquidation_multiple: Decimal = Decimal(1)
    participating: bool = False
    participation_cap: Decimal | None = None


@dataclass
class Round:
    name: str
    investment: Decimal
    pre_money: Decimal
    option_pool_pct: Decimal = Decimal(0)
    stock_class_id: str | None = None


@dataclass
class CapTable:
    holders: list[Holder] = field(default_factory=list)
    total_shares: Decimal = Decimal(0)
    price_per_share: Decimal = Decimal(0)

    def ownership_table(self) -> list[dict[str, Any]]:
        rows = []
        for h in self.holders:
            pct = (
                (h.shares / self.total_shares * 100)
                if self.total_shares
                else Decimal(0)
            )
            row: dict[str, Any] = {
                "name": h.name,
                "instrument": h.instrument.value,
                "shares": _fmt(h.shares),
                "ownership_pct": _fmt(pct, 2),
                "investment": _fmt(h.investment),
            }
            if h.stock_class_id:
                row["stock_class"] = h.stock_class_id
            rows.append(row)
        return rows


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _d(val: Any) -> Decimal:
    if isinstance(val, Decimal):
        return val
    if val is None:
        return Decimal(0)
    return Decimal(str(val))


def _fmt(val: Decimal, places: int = 0) -> str:
    if places == 0:
        return str(val.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    q = Decimal(10) ** -places
    return str(val.quantize(q, rounding=ROUND_HALF_UP))


def _calc_accrued_interest(
    principal: Decimal,
    rate: Decimal,
    months: int,
    interest_type: InterestType = InterestType.SIMPLE,
    compounding_frequency: int = 12,
) -> Decimal:
    if rate == 0 or months == 0:
        return Decimal(0)
    if interest_type == InterestType.SIMPLE:
        return principal * rate * Decimal(months) / Decimal(12)
    n = Decimal(compounding_frequency)
    t = Decimal(months) / Decimal(12)
    return principal * ((1 + rate / n) ** (n * t)) - principal


def _parse_stock_classes(data: list[dict]) -> dict[str, StockClass]:
    classes = {}
    for c in data:
        sc = StockClass(
            class_id=c["class_id"],
            name=c["name"],
            instrument_type=InstrumentType(c.get("instrument_type", "preferred")),
            seniority=int(c.get("seniority", 1)),
            liquidation_multiple=_d(c.get("liquidation_multiple", 1)),
            participating=c.get("participating", False),
            participation_cap=_d(c["participation_cap"])
            if c.get("participation_cap")
            else None,
            conversion_ratio=_d(c.get("conversion_ratio", 1)),
            votes_per_share=_d(c.get("votes_per_share", 1)),
        )
        classes[sc.class_id] = sc
    return classes


def _parse_safe_terms(data: dict) -> SAFETerms:
    return SAFETerms(
        valuation_cap=_d(data["valuation_cap"]) if data.get("valuation_cap") else None,
        discount=_d(data["discount"]) if data.get("discount") else None,
        is_post_money=data.get("is_post_money", True),
        mfn=data.get("mfn", False),
        exit_multiple=_d(data["exit_multiple"]) if data.get("exit_multiple") else None,
        capitalization_definition=CapDefinition(
            data.get("capitalization_definition", "all_outstanding")
        ),
    )


def _parse_note_terms(data: dict) -> NoteTerms:
    return NoteTerms(
        valuation_cap=_d(data["valuation_cap"]) if data.get("valuation_cap") else None,
        discount=_d(data["discount"]) if data.get("discount") else None,
        interest_rate=_d(data.get("interest_rate", 0)),
        interest_type=InterestType(data.get("interest_type", "simple")),
        compounding_frequency=int(data.get("compounding_frequency", 12)),
        months_outstanding=int(data.get("months_outstanding", 0)),
    )


def _get_capitalization(
    holders: list[Holder],
    total_shares: Decimal,
    cap_def: CapDefinition,
) -> Decimal:
    """Compute capitalization based on definition (what counts in denominator)."""
    if cap_def == CapDefinition.ALL_OUTSTANDING:
        return total_shares
    if cap_def == CapDefinition.SHARES_ONLY:
        return sum(
            (
                h.shares
                for h in holders
                if h.instrument in (InstrumentType.COMMON, InstrumentType.PREFERRED)
            ),
            Decimal(0),
        )
    # SHARES_AND_OPTIONS
    return sum(
        (
            h.shares
            for h in holders
            if h.instrument
            in (InstrumentType.COMMON, InstrumentType.PREFERRED, InstrumentType.OPTIONS)
        ),
        Decimal(0),
    )


# ---------------------------------------------------------------------------
# Core calculations
# ---------------------------------------------------------------------------


def build_cap_table(scenario: dict[str, Any]) -> dict[str, Any]:
    """Build a cap table from a full scenario definition."""
    holders: list[Holder] = []
    total_shares = Decimal(0)

    # Founders
    for f in scenario.get("founders", []):
        shares = _d(f["shares"])
        holders.append(
            Holder(
                name=f["name"],
                instrument=InstrumentType.COMMON,
                shares=shares,
                stock_class_id=f.get("stock_class_id", "common"),
            )
        )
        total_shares += shares

    # Option pool
    esop = scenario.get("option_pool")
    if esop:
        shares = _d(esop.get("shares", 0))
        holders.append(
            Holder(
                name=esop.get("name", "ESOP"),
                instrument=InstrumentType.OPTIONS,
                shares=shares,
            )
        )
        total_shares += shares

    # Convert SAFEs
    safes = scenario.get("safes", [])
    if safes:
        holders, total_shares = _convert_safes(holders, total_shares, safes)

    # Convert notes
    notes = scenario.get("notes", [])
    if notes:
        holders, total_shares = _convert_notes(holders, total_shares, notes)

    # Apply priced rounds
    pps = Decimal(0)
    for r_data in scenario.get("rounds", []):
        r = Round(
            name=r_data["name"],
            investment=_d(r_data["investment"]),
            pre_money=_d(r_data["pre_money"]),
            option_pool_pct=_d(r_data.get("option_pool_pct", 0)),
            stock_class_id=r_data.get("stock_class_id"),
        )
        holders, total_shares, pps = _apply_round(holders, total_shares, r)

    cap = CapTable(holders=holders, total_shares=total_shares, price_per_share=pps)
    return {
        "cap_table": cap.ownership_table(),
        "total_shares": _fmt(total_shares),
        "price_per_share": _fmt(pps, 6) if pps else "N/A",
    }


def _convert_safes(
    holders: list[Holder],
    total_shares: Decimal,
    safes: list[dict],
) -> tuple[list[Holder], Decimal]:
    """Convert SAFEs into shares with MFN and capitalization definition support."""
    parsed = [(s, _parse_safe_terms(s)) for s in safes]

    # Resolve MFN: find lowest cap among non-MFN SAFEs
    non_mfn_caps = [
        t.valuation_cap for _, t in parsed if not t.mfn and t.valuation_cap is not None
    ]
    mfn_cap = min(non_mfn_caps) if non_mfn_caps else None

    # Separate by type
    post_safes = [(s, t) for s, t in parsed if t.is_post_money]
    pre_safes = [(s, t) for s, t in parsed if not t.is_post_money]

    # Post-money SAFEs
    for s, terms in post_safes:
        inv = _d(s["investment"])
        cap = terms.valuation_cap
        if terms.mfn and mfn_cap is not None:
            cap = mfn_cap

        if cap and cap > 0:
            pct = inv / cap
            cap_shares = _get_capitalization(
                holders, total_shares, terms.capitalization_definition
            )
            new_shares = cap_shares * pct / (1 - pct)
        else:
            new_shares = Decimal(0)

        holders.append(
            Holder(
                name=s["name"],
                instrument=InstrumentType.SAFE_POST,
                shares=new_shares,
                investment=inv,
                safe_terms=terms,
            )
        )
        total_shares += new_shares

    # Pre-money SAFEs
    pre_cap_shares = total_shares
    for s, terms in pre_safes:
        inv = _d(s["investment"])
        cap = terms.valuation_cap
        if terms.mfn and mfn_cap is not None:
            cap = mfn_cap

        if cap and cap > 0:
            cap_shares = _get_capitalization(
                holders, pre_cap_shares, terms.capitalization_definition
            )
            price = cap / cap_shares if cap_shares > 0 else cap
            new_shares = inv / price
        else:
            new_shares = Decimal(0)

        holders.append(
            Holder(
                name=s["name"],
                instrument=InstrumentType.SAFE_PRE,
                shares=new_shares,
                investment=inv,
                safe_terms=terms,
            )
        )
        total_shares += new_shares

    return holders, total_shares


def _convert_notes(
    holders: list[Holder],
    total_shares: Decimal,
    notes: list[dict],
) -> tuple[list[Holder], Decimal]:
    """Convert convertible notes with compound interest support."""
    for n in notes:
        terms = _parse_note_terms(n)
        inv = _d(n["investment"])
        accrued = _calc_accrued_interest(
            inv,
            terms.interest_rate,
            terms.months_outstanding,
            terms.interest_type,
            terms.compounding_frequency,
        )
        total_inv = inv + accrued

        if terms.valuation_cap and terms.valuation_cap > 0:
            price_from_cap = terms.valuation_cap / total_shares
            new_shares = total_inv / price_from_cap
        else:
            new_shares = Decimal(0)

        holders.append(
            Holder(
                name=n["name"],
                instrument=InstrumentType.NOTE,
                shares=new_shares,
                investment=inv,
                note_terms=terms,
            )
        )
        total_shares += new_shares

    return holders, total_shares


def _apply_round(
    holders: list[Holder],
    total_shares: Decimal,
    r: Round,
) -> tuple[list[Holder], Decimal, Decimal]:
    """Apply a priced equity round to the cap table."""
    if r.option_pool_pct > 0:
        post_money = r.pre_money + r.investment
        esop_holder = None
        for h in holders:
            if h.instrument == InstrumentType.OPTIONS:
                esop_holder = h
                break
        if not esop_holder:
            esop_holder = Holder(name="ESOP", instrument=InstrumentType.OPTIONS)
            holders.append(esop_holder)

        esop_target = post_money * r.option_pool_pct
        pps_pre = r.pre_money / total_shares
        esop_target_shares = esop_target / pps_pre
        new_esop = esop_target_shares - esop_holder.shares
        if new_esop > 0:
            esop_holder.shares += new_esop
            total_shares += new_esop

    pps = r.pre_money / total_shares
    new_shares = r.investment / pps
    investor = Holder(
        name=r.name,
        instrument=InstrumentType.PREFERRED,
        shares=new_shares,
        investment=r.investment,
        stock_class_id=r.stock_class_id,
    )
    holders.append(investor)
    total_shares += new_shares

    return holders, total_shares, pps


# ---------------------------------------------------------------------------
# Dilution
# ---------------------------------------------------------------------------


def calc_dilution(scenario: dict[str, Any]) -> dict[str, Any]:
    """Calculate dilution impact of a new round on existing holders."""
    total_shares = _d(scenario["total_shares"])
    existing = scenario["existing_holders"]

    pre_ownership = {}
    for h in existing:
        shares = _d(h["shares"])
        pre_ownership[h["name"]] = {
            "shares": shares,
            "pct": shares / total_shares * 100,
        }

    r = scenario["new_round"]
    round_obj = Round(
        name=r["name"],
        investment=_d(r["investment"]),
        pre_money=_d(r["pre_money"]),
        option_pool_pct=_d(r.get("option_pool_pct", 0)),
    )

    holders_objs = [
        Holder(
            name=h["name"],
            instrument=InstrumentType(h.get("instrument", "common")),
            shares=_d(h["shares"]),
        )
        for h in existing
    ]

    holders_objs, new_total, pps = _apply_round(holders_objs, total_shares, round_obj)

    results = []
    for h in holders_objs:
        pre = pre_ownership.get(h.name)
        post_pct = h.shares / new_total * 100
        if pre:
            dilution = (pre["pct"] - post_pct) / pre["pct"] * 100
            results.append(
                {
                    "name": h.name,
                    "shares": _fmt(h.shares),
                    "pre_pct": _fmt(pre["pct"], 2),
                    "post_pct": _fmt(post_pct, 2),
                    "dilution_pct": _fmt(dilution, 2),
                }
            )
        else:
            results.append(
                {
                    "name": h.name,
                    "shares": _fmt(h.shares),
                    "pre_pct": "0.00",
                    "post_pct": _fmt(post_pct, 2),
                    "dilution_pct": "N/A",
                }
            )

    return {
        "dilution_table": results,
        "total_shares_before": _fmt(total_shares),
        "total_shares_after": _fmt(new_total),
        "price_per_share": _fmt(pps, 6),
        "post_money_valuation": _fmt(round_obj.pre_money + round_obj.investment),
    }


# ---------------------------------------------------------------------------
# Waterfall (multi-series, seniority-aware)
# ---------------------------------------------------------------------------


def calc_waterfall(scenario: dict[str, Any]) -> dict[str, Any]:
    """Calculate liquidation waterfall with multi-series seniority support.

    Uses `stock_classes` array for per-class liquidation terms (seniority,
    multiples, participation). Preferred holders without a stock class
    default to 1x non-participating.
    """
    exit_val = _d(scenario["exit_value"])
    total_shares = _d(scenario["total_shares"])
    stock_classes = _parse_stock_classes(scenario.get("stock_classes", []))

    holders = _parse_waterfall_holders(scenario["holders"], stock_classes)

    payouts = _run_waterfall(holders, total_shares, exit_val, stock_classes)

    results = _format_waterfall_results(holders, payouts)

    return {
        "exit_value": _fmt(exit_val),
        "waterfall": results,
        "remaining_undistributed": "0",
    }


def _parse_waterfall_holders(
    holders_data: list[dict], stock_classes: dict[str, StockClass]
) -> list[Holder]:
    holders = []
    for h in holders_data:
        inst = InstrumentType(h.get("instrument", "common"))
        class_id = h.get("stock_class_id")

        # Get liquidation terms from stock class (defaults: 1x non-participating)
        liq_mult = Decimal(1)
        participating = False
        part_cap = None
        if class_id and class_id in stock_classes:
            sc = stock_classes[class_id]
            liq_mult = sc.liquidation_multiple
            participating = sc.participating
            part_cap = sc.participation_cap

        holders.append(
            Holder(
                name=h["name"],
                instrument=inst,
                shares=_d(h.get("shares", 0)),
                investment=_d(h.get("investment", 0)),
                stock_class_id=class_id,
                liquidation_multiple=liq_mult,
                participating=participating,
                participation_cap=part_cap,
            )
        )
    return holders


def _run_waterfall(
    holders: list[Holder],
    total_shares: Decimal,
    exit_val: Decimal,
    stock_classes: dict[str, StockClass],
) -> dict[str, Decimal]:
    """Execute the waterfall distribution algorithm."""
    remaining = exit_val
    payouts: dict[str, Decimal] = {h.name: Decimal(0) for h in holders}

    preferred = [h for h in holders if h.instrument == InstrumentType.PREFERRED]

    # Sort preferred by seniority (most senior first)
    if stock_classes:
        preferred.sort(
            key=lambda h: (
                stock_classes.get(
                    h.stock_class_id or "", StockClass("", "", InstrumentType.PREFERRED)
                ).seniority
            ),
            reverse=True,
        )

    # Step 1: Liquidation preferences in seniority order
    for h in preferred:
        pref_amount = h.investment * h.liquidation_multiple
        payout = min(pref_amount, remaining)
        payouts[h.name] += payout
        remaining -= payout

    # Step 2: Participation
    for h in preferred:
        if h.participating and remaining > 0:
            pro_rata = (h.shares / total_shares) * remaining
            if h.participation_cap:
                cap_remaining = h.participation_cap * h.investment - payouts[h.name]
                pro_rata = min(pro_rata, max(Decimal(0), cap_remaining))
            payouts[h.name] += pro_rata
            remaining -= pro_rata

    # Step 3: Remaining to common (and non-participating preferred who convert)
    if remaining > 0:
        common_holders = [
            h
            for h in holders
            if h.instrument in (InstrumentType.COMMON, InstrumentType.OPTIONS)
        ]
        non_part_preferred = [h for h in preferred if not h.participating]

        for h in non_part_preferred:
            as_common_payout = (h.shares / total_shares) * exit_val
            if as_common_payout > payouts[h.name]:
                remaining += payouts[h.name]
                payouts[h.name] = Decimal(0)
                common_holders.append(h)

        total_common_shares = sum(h.shares for h in common_holders)
        if total_common_shares > 0:
            for h in common_holders:
                pro_rata = (h.shares / total_common_shares) * remaining
                payouts[h.name] += pro_rata
            remaining = Decimal(0)

    return payouts


def _format_waterfall_results(
    holders: list[Holder], payouts: dict[str, Decimal]
) -> list[dict[str, Any]]:
    results = []
    for h in holders:
        payout = payouts[h.name]
        roi = (payout / h.investment - 1) * 100 if h.investment > 0 else None
        row: dict[str, Any] = {
            "name": h.name,
            "instrument": h.instrument.value,
            "investment": _fmt(h.investment),
            "payout": _fmt(payout),
            "return_multiple": _fmt(payout / h.investment, 2) + "x"
            if h.investment > 0
            else "N/A",
            "roi_pct": _fmt(roi, 1) if roi is not None else "N/A",
        }
        if h.stock_class_id:
            row["stock_class"] = h.stock_class_id
        results.append(row)
    return results


# ---------------------------------------------------------------------------
# Scenarios (waterfall at multiple exit values)
# ---------------------------------------------------------------------------


def calc_scenarios(scenario: dict[str, Any]) -> dict[str, Any]:
    """Run waterfall at multiple exit values for scenario comparison."""
    exit_values = [_d(v) for v in scenario["exit_values"]]
    total_shares = _d(scenario["total_shares"])
    stock_classes = _parse_stock_classes(scenario.get("stock_classes", []))
    holders = _parse_waterfall_holders(scenario["holders"], stock_classes)

    holder_names = [h.name for h in holders]
    scenarios = []

    for ev in exit_values:
        payouts = _run_waterfall(holders, total_shares, ev, stock_classes)
        row: dict[str, Any] = {"exit_value": _fmt(ev)}
        for h in holders:
            payout = payouts[h.name]
            row[h.name] = {
                "payout": _fmt(payout),
                "return_multiple": _fmt(payout / h.investment, 2) + "x"
                if h.investment > 0
                else "N/A",
            }
        scenarios.append(row)

    return {
        "holder_names": holder_names,
        "scenarios": scenarios,
    }


# ---------------------------------------------------------------------------
# SAFE/Note Conversion
# ---------------------------------------------------------------------------


def convert_safes_to_round(scenario: dict[str, Any]) -> dict[str, Any]:
    """Show SAFE/note conversion into a priced round with detailed breakdown."""
    holders: list[Holder] = []
    total_shares = Decimal(0)

    for f in scenario.get("founders", []):
        shares = _d(f["shares"])
        holders.append(
            Holder(name=f["name"], instrument=InstrumentType.COMMON, shares=shares)
        )
        total_shares += shares

    esop = scenario.get("option_pool")
    if esop:
        shares = _d(esop.get("shares", 0))
        holders.append(
            Holder(name="ESOP", instrument=InstrumentType.OPTIONS, shares=shares)
        )
        total_shares += shares

    safes = scenario.get("safes", [])
    notes = scenario.get("notes", [])

    round_data = scenario["round"]
    round_pps = _d(round_data["pre_money"]) / total_shares

    conversions = []

    # Resolve MFN cap
    parsed_safes = [_parse_safe_terms(s) for s in safes]
    non_mfn_caps = [
        t.valuation_cap for t in parsed_safes if not t.mfn and t.valuation_cap
    ]
    mfn_cap = min(non_mfn_caps) if non_mfn_caps else None

    for s, terms in zip(safes, parsed_safes):
        inv = _d(s["investment"])
        cap = terms.valuation_cap
        if terms.mfn and mfn_cap is not None:
            cap = mfn_cap

        price_from_cap = None
        if cap and cap > 0:
            if terms.is_post_money:
                pct = inv / cap
                cap_shares = _get_capitalization(
                    holders, total_shares, terms.capitalization_definition
                )
                shares_at_cap = cap_shares / (1 - pct)
                price_from_cap = cap / shares_at_cap
            else:
                cap_shares = _get_capitalization(
                    holders, total_shares, terms.capitalization_definition
                )
                price_from_cap = cap / cap_shares if cap_shares > 0 else None

        price_from_discount = (
            round_pps * (1 - terms.discount) if terms.discount else None
        )

        prices = [p for p in [price_from_cap, price_from_discount] if p is not None]
        conv_price = min(prices) if prices else round_pps
        new_shares = inv / conv_price

        conv_entry: dict[str, Any] = {
            "name": s["name"],
            "instrument": "SAFE (post-money)"
            if terms.is_post_money
            else "SAFE (pre-money)",
            "investment": _fmt(inv),
            "valuation_cap": _fmt(cap) if cap else "None",
            "discount": f"{_fmt(terms.discount * 100, 0)}%"
            if terms.discount
            else "None",
            "price_from_cap": _fmt(price_from_cap, 6) if price_from_cap else "N/A",
            "price_from_discount": _fmt(price_from_discount, 6)
            if price_from_discount
            else "N/A",
            "conversion_price": _fmt(conv_price, 6),
            "shares_issued": _fmt(new_shares),
            "price_used": "cap"
            if price_from_cap
            and (not price_from_discount or price_from_cap <= price_from_discount)
            else "discount",
        }
        if terms.mfn:
            conv_entry["mfn_resolved_cap"] = (
                _fmt(mfn_cap) if mfn_cap else "No cap found"
            )
        conversions.append(conv_entry)

        holders.append(
            Holder(
                name=s["name"],
                instrument=InstrumentType.SAFE_POST
                if terms.is_post_money
                else InstrumentType.SAFE_PRE,
                shares=new_shares,
                investment=inv,
            )
        )
        total_shares += new_shares

    for n in notes:
        terms = _parse_note_terms(n)
        inv = _d(n["investment"])
        accrued = _calc_accrued_interest(
            inv,
            terms.interest_rate,
            terms.months_outstanding,
            terms.interest_type,
            terms.compounding_frequency,
        )
        total_inv = inv + accrued

        cap = terms.valuation_cap
        price_from_cap = cap / total_shares if cap and cap > 0 else None
        price_from_discount = (
            round_pps * (1 - terms.discount) if terms.discount else None
        )

        prices = [p for p in [price_from_cap, price_from_discount] if p is not None]
        conv_price = min(prices) if prices else round_pps
        new_shares = total_inv / conv_price

        conversions.append(
            {
                "name": n["name"],
                "instrument": "Convertible Note",
                "investment": _fmt(inv),
                "accrued_interest": _fmt(accrued),
                "interest_type": terms.interest_type.value,
                "total_converting": _fmt(total_inv),
                "valuation_cap": _fmt(cap) if cap else "None",
                "discount": f"{_fmt(terms.discount * 100, 0)}%"
                if terms.discount
                else "None",
                "price_from_cap": _fmt(price_from_cap, 6) if price_from_cap else "N/A",
                "price_from_discount": _fmt(price_from_discount, 6)
                if price_from_discount
                else "N/A",
                "conversion_price": _fmt(conv_price, 6),
                "shares_issued": _fmt(new_shares),
            }
        )

        holders.append(
            Holder(
                name=n["name"],
                instrument=InstrumentType.NOTE,
                shares=new_shares,
                investment=inv,
            )
        )
        total_shares += new_shares

    r = Round(
        name=round_data["name"],
        investment=_d(round_data["investment"]),
        pre_money=_d(round_data["pre_money"]),
        option_pool_pct=_d(round_data.get("option_pool_pct", 0)),
    )
    holders, total_shares, final_pps = _apply_round(holders, total_shares, r)

    cap_table = CapTable(
        holders=holders, total_shares=total_shares, price_per_share=final_pps
    )
    return {
        "conversions": conversions,
        "round_price_per_share": _fmt(final_pps, 6),
        "post_money_valuation": _fmt(r.pre_money + r.investment),
        "cap_table": cap_table.ownership_table(),
        "total_shares": _fmt(total_shares),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cap table modeling: ownership, dilution, waterfall, SAFE conversion, scenarios."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for cmd in ["model", "dilution", "waterfall", "convert", "scenarios"]:
        p = sub.add_parser(cmd)
        p.add_argument("--input", required=True, help="Path to JSON scenario file")

    args = parser.parse_args()

    with open(args.input) as f:
        scenario = json.load(f)

    commands = {
        "model": build_cap_table,
        "dilution": calc_dilution,
        "waterfall": calc_waterfall,
        "convert": convert_safes_to_round,
        "scenarios": calc_scenarios,
    }

    result = commands[args.command](scenario)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
