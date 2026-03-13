#!/usr/bin/env python3
"""Cap table modeling: ownership, dilution, SAFE conversion, waterfall.

Usage:
    python3 captable.py <command> [options]

Commands:
    model       Build a cap table from a JSON scenario file
    dilution    Show dilution impact of a new round
    waterfall   Calculate liquidation waterfall / payout distribution
    convert     Convert SAFEs/notes into a priced round

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
# Data model
# ---------------------------------------------------------------------------


class InstrumentType(str, Enum):
    COMMON = "common"
    PREFERRED = "preferred"
    SAFE_POST = "safe_post_money"
    SAFE_PRE = "safe_pre_money"
    NOTE = "convertible_note"
    OPTIONS = "options"


@dataclass
class Holder:
    name: str
    instrument: InstrumentType
    shares: Decimal = Decimal(0)
    investment: Decimal = Decimal(0)
    valuation_cap: Decimal | None = None
    discount: Decimal | None = None
    liquidation_multiple: Decimal = Decimal(1)
    participating: bool = False
    participation_cap: Decimal | None = None
    interest_rate: Decimal | None = None  # for notes
    months_outstanding: int = 0  # for notes


@dataclass
class Round:
    name: str
    investment: Decimal
    pre_money: Decimal
    option_pool_pct: Decimal = Decimal(0)  # target ESOP % post-round


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
            rows.append(
                {
                    "name": h.name,
                    "instrument": h.instrument.value,
                    "shares": _fmt(h.shares),
                    "ownership_pct": _fmt(pct, 2),
                    "investment": _fmt(h.investment),
                }
            )
        return rows


def _d(val: Any) -> Decimal:
    """Convert to Decimal."""
    if isinstance(val, Decimal):
        return val
    return Decimal(str(val))


def _fmt(val: Decimal, places: int = 0) -> str:
    if places == 0:
        return str(val.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    q = Decimal(10) ** -places
    return str(val.quantize(q, rounding=ROUND_HALF_UP))


# ---------------------------------------------------------------------------
# Core calculations
# ---------------------------------------------------------------------------


def build_cap_table(scenario: dict[str, Any]) -> dict[str, Any]:
    """Build a cap table from a full scenario definition.

    Expected JSON structure:
    {
        "founders": [{"name": "...", "shares": 10000000}, ...],
        "option_pool": {"shares": 1000000, "name": "ESOP"},
        "safes": [{"name": "...", "investment": 500000, "valuation_cap": 5000000,
                    "type": "post_money", "discount": null}, ...],
        "notes": [{"name": "...", "investment": ..., "valuation_cap": ...,
                    "interest_rate": 0.05, "months": 12, "discount": 0.2}, ...],
        "rounds": [{"name": "Series A", "investment": 3000000,
                     "pre_money": 15000000, "option_pool_pct": 0.15}, ...]
    }
    """
    holders: list[Holder] = []
    total_shares = Decimal(0)

    # Founders
    for f in scenario.get("founders", []):
        shares = _d(f["shares"])
        h = Holder(name=f["name"], instrument=InstrumentType.COMMON, shares=shares)
        holders.append(h)
        total_shares += shares

    # Existing option pool
    esop = scenario.get("option_pool")
    if esop:
        shares = _d(esop.get("shares", 0))
        h = Holder(
            name=esop.get("name", "ESOP"),
            instrument=InstrumentType.OPTIONS,
            shares=shares,
        )
        holders.append(h)
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
        )
        holders, total_shares, pps = _apply_round(holders, total_shares, r)

    cap = CapTable(holders=holders, total_shares=total_shares, price_per_share=pps)
    return {
        "cap_table": cap.ownership_table(),
        "total_shares": _fmt(total_shares),
        "price_per_share": _fmt(pps, 6) if pps else "N/A",
    }


def _convert_safes(
    holders: list[Holder], total_shares: Decimal, safes: list[dict]
) -> tuple[list[Holder], Decimal]:
    """Convert SAFEs into shares (typically at a priced round)."""
    # Post-money SAFEs: ownership = investment / cap
    # Pre-money SAFEs: ownership depends on total pre-money capitalization

    post_safes = [s for s in safes if s.get("type", "post_money") == "post_money"]
    pre_safes = [s for s in safes if s.get("type") == "pre_money"]

    # Post-money: each SAFE's ownership is fixed
    for s in post_safes:
        inv = _d(s["investment"])
        cap = _d(s["valuation_cap"])
        pct = inv / cap  # ownership fraction
        # shares = existing_total / (1 - sum_of_pcts) * pct
        # but we need to handle sequentially for simplicity
        new_shares = total_shares * pct / (1 - pct)
        h = Holder(
            name=s["name"],
            instrument=InstrumentType.SAFE_POST,
            shares=new_shares,
            investment=inv,
            valuation_cap=cap,
            discount=_d(s["discount"]) if s.get("discount") else None,
        )
        holders.append(h)
        total_shares += new_shares

    # Pre-money: ownership based on pre-conversion capitalization
    pre_cap_shares = total_shares  # snapshot before pre-money conversions
    for s in pre_safes:
        inv = _d(s["investment"])
        cap = _d(s["valuation_cap"])
        price = cap / pre_cap_shares
        new_shares = inv / price
        h = Holder(
            name=s["name"],
            instrument=InstrumentType.SAFE_PRE,
            shares=new_shares,
            investment=inv,
            valuation_cap=cap,
            discount=_d(s["discount"]) if s.get("discount") else None,
        )
        holders.append(h)
        total_shares += new_shares

    return holders, total_shares


def _convert_notes(
    holders: list[Holder], total_shares: Decimal, notes: list[dict]
) -> tuple[list[Holder], Decimal]:
    """Convert convertible notes into shares."""
    for n in notes:
        inv = _d(n["investment"])
        rate = _d(n.get("interest_rate", 0))
        months = int(n.get("months", 0))
        accrued = inv * rate * Decimal(months) / Decimal(12)
        total_inv = inv + accrued

        cap = _d(n["valuation_cap"]) if n.get("valuation_cap") else None
        discount = _d(n["discount"]) if n.get("discount") else None

        # Price from cap
        if cap:
            price_from_cap = cap / total_shares
        else:
            price_from_cap = None

        # We'll use the cap price (discount is applied against round price,
        # which isn't known yet at this stage)
        if price_from_cap:
            new_shares = total_inv / price_from_cap
        else:
            # No cap -- will convert at round price with discount
            # For modeling purposes, use a placeholder
            new_shares = Decimal(0)

        h = Holder(
            name=n["name"],
            instrument=InstrumentType.NOTE,
            shares=new_shares,
            investment=inv,
            valuation_cap=cap,
            discount=discount,
            interest_rate=rate,
            months_outstanding=months,
        )
        holders.append(h)
        total_shares += new_shares

    return holders, total_shares


def _apply_round(
    holders: list[Holder], total_shares: Decimal, r: Round
) -> tuple[list[Holder], Decimal, Decimal]:
    """Apply a priced equity round to the cap table."""
    # Expand option pool if needed
    if r.option_pool_pct > 0:
        post_money = r.pre_money + r.investment
        target_esop_shares = (
            post_money * r.option_pool_pct / (Decimal(1) - r.option_pool_pct)
        )
        target_esop_shares = target_esop_shares / (r.pre_money / total_shares)

        # Find or create ESOP holder
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

    # Price per share
    pps = r.pre_money / total_shares

    # Issue new shares
    new_shares = r.investment / pps
    investor = Holder(
        name=r.name,
        instrument=InstrumentType.PREFERRED,
        shares=new_shares,
        investment=r.investment,
    )
    holders.append(investor)
    total_shares += new_shares

    return holders, total_shares, pps


def calc_dilution(scenario: dict[str, Any]) -> dict[str, Any]:
    """Calculate dilution impact of a new round on existing holders.

    Expected JSON:
    {
        "existing_holders": [{"name": "...", "shares": ..., "investment": ...}, ...],
        "total_shares": 10000000,
        "new_round": {"name": "Series A", "investment": 3000000,
                       "pre_money": 15000000, "option_pool_pct": 0.15}
    }
    """
    total_shares = _d(scenario["total_shares"])
    existing = scenario["existing_holders"]

    pre_ownership = {}
    for h in existing:
        shares = _d(h["shares"])
        pre_ownership[h["name"]] = {
            "shares": shares,
            "pct": shares / total_shares * 100,
        }

    # Apply round
    r = scenario["new_round"]
    round_obj = Round(
        name=r["name"],
        investment=_d(r["investment"]),
        pre_money=_d(r["pre_money"]),
        option_pool_pct=_d(r.get("option_pool_pct", 0)),
    )

    holders_objs = [
        Holder(name=h["name"], instrument=InstrumentType.COMMON, shares=_d(h["shares"]))
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


def calc_waterfall(scenario: dict[str, Any]) -> dict[str, Any]:
    """Calculate liquidation waterfall / payout distribution.

    Expected JSON:
    {
        "exit_value": 50000000,
        "holders": [
            {"name": "...", "shares": ..., "instrument": "preferred",
             "investment": ..., "liquidation_multiple": 1,
             "participating": false, "participation_cap": null},
            {"name": "...", "shares": ..., "instrument": "common"}
        ],
        "total_shares": 15000000
    }
    """
    exit_val = _d(scenario["exit_value"])
    total_shares = _d(scenario["total_shares"])
    holders_data = scenario["holders"]

    holders = []
    for h in holders_data:
        inst = InstrumentType(h.get("instrument", "common"))
        holders.append(
            Holder(
                name=h["name"],
                instrument=inst,
                shares=_d(h.get("shares", 0)),
                investment=_d(h.get("investment", 0)),
                liquidation_multiple=_d(h.get("liquidation_multiple", 1)),
                participating=h.get("participating", False),
                participation_cap=_d(h["participation_cap"])
                if h.get("participation_cap")
                else None,
            )
        )

    remaining = exit_val
    payouts: dict[str, Decimal] = {h.name: Decimal(0) for h in holders}

    # Step 1: Liquidation preferences (preferred holders, in reverse seniority)
    preferred = [h for h in holders if h.instrument == InstrumentType.PREFERRED]
    for h in preferred:
        pref_amount = h.investment * h.liquidation_multiple
        payout = min(pref_amount, remaining)
        payouts[h.name] += payout
        remaining -= payout

    # Step 2: Participation (if applicable)
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

        # Check if non-participating preferred would do better converting
        for h in non_part_preferred:
            as_common_payout = (h.shares / total_shares) * (exit_val)
            if as_common_payout > payouts[h.name]:
                # Convert: reset payout, add to common pool
                remaining += payouts[h.name]
                payouts[h.name] = Decimal(0)
                common_holders.append(h)

        total_common_shares = sum(h.shares for h in common_holders)
        if total_common_shares > 0:
            for h in common_holders:
                pro_rata = (h.shares / total_common_shares) * remaining
                payouts[h.name] += pro_rata
            remaining = Decimal(0)

    results = []
    for h in holders:
        payout = payouts[h.name]
        roi = (payout / h.investment - 1) * 100 if h.investment > 0 else None
        results.append(
            {
                "name": h.name,
                "instrument": h.instrument.value,
                "investment": _fmt(h.investment),
                "payout": _fmt(payout),
                "return_multiple": _fmt(payout / h.investment, 2) + "x"
                if h.investment > 0
                else "N/A",
                "roi_pct": _fmt(roi, 1) if roi is not None else "N/A",
            }
        )

    return {
        "exit_value": _fmt(exit_val),
        "waterfall": results,
        "remaining_undistributed": _fmt(remaining if remaining > 0 else Decimal(0)),
    }


def convert_safes_to_round(scenario: dict[str, Any]) -> dict[str, Any]:
    """Show SAFE/note conversion into a priced round.

    Expected JSON:
    {
        "founders": [{"name": "...", "shares": 10000000}],
        "option_pool": {"shares": 1000000},
        "safes": [...],
        "notes": [...],
        "round": {"name": "Series A", "investment": 3000000,
                   "pre_money": 15000000, "option_pool_pct": 0.15}
    }
    """
    # Build pre-round state
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
    round_pps = _d(round_data["pre_money"]) / total_shares  # approximate

    # Convert each SAFE/note and show conversion details
    conversions = []
    for s in safes:
        inv = _d(s["investment"])
        cap = _d(s["valuation_cap"]) if s.get("valuation_cap") else None
        discount = _d(s["discount"]) if s.get("discount") else None
        is_post = s.get("type", "post_money") == "post_money"

        price_from_cap = None
        if cap:
            if is_post:
                # Post-money: price = cap / fully diluted shares at cap
                # Simplified: ownership = inv / cap
                pct = inv / cap
                shares_at_cap = total_shares / (1 - pct)
                price_from_cap = cap / shares_at_cap
            else:
                price_from_cap = cap / total_shares

        price_from_discount = round_pps * (1 - discount) if discount else None

        # Best price for investor (lowest)
        prices = [p for p in [price_from_cap, price_from_discount] if p is not None]
        conv_price = min(prices) if prices else round_pps
        new_shares = inv / conv_price

        conversions.append(
            {
                "name": s["name"],
                "instrument": "SAFE (post-money)" if is_post else "SAFE (pre-money)",
                "investment": _fmt(inv),
                "valuation_cap": _fmt(cap) if cap else "None",
                "discount": f"{_fmt(discount * 100, 0)}%" if discount else "None",
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
                name=s["name"],
                instrument=InstrumentType.SAFE_POST
                if is_post
                else InstrumentType.SAFE_PRE,
                shares=new_shares,
                investment=inv,
            )
        )
        total_shares += new_shares

    for n in notes:
        inv = _d(n["investment"])
        rate = _d(n.get("interest_rate", 0))
        months = int(n.get("months", 0))
        accrued = inv * rate * Decimal(months) / Decimal(12)
        total_inv = inv + accrued

        cap = _d(n["valuation_cap"]) if n.get("valuation_cap") else None
        discount = _d(n["discount"]) if n.get("discount") else None

        price_from_cap = cap / total_shares if cap else None
        price_from_discount = round_pps * (1 - discount) if discount else None

        prices = [p for p in [price_from_cap, price_from_discount] if p is not None]
        conv_price = min(prices) if prices else round_pps
        new_shares = total_inv / conv_price

        conversions.append(
            {
                "name": n["name"],
                "instrument": "Convertible Note",
                "investment": _fmt(inv),
                "accrued_interest": _fmt(accrued),
                "total_converting": _fmt(total_inv),
                "valuation_cap": _fmt(cap) if cap else "None",
                "discount": f"{_fmt(discount * 100, 0)}%" if discount else "None",
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

    # Apply the priced round
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
        description="Cap table modeling: ownership, dilution, waterfall, SAFE conversion."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for cmd in ["model", "dilution", "waterfall", "convert"]:
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
    }

    result = commands[args.command](scenario)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
