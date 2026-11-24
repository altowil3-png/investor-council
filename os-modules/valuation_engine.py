#!/usr/bin/env python3
"""
Institutional Investing OS — Standalone Valuation & Forensic Engine (v4)
=======================================================================
Zero external dependencies (Python 3 standard library only).

v4 changelog (Claude review + AGV conditions, Nov 24 2026):
  1. JSON INPUTS WITH PROVENANCE: `--input inputs/TICKER.json`. Every reported fact must carry
     `as_of_date` + (`source_url` or `filing_ref`) + `verification`; every judgment carries a `rationale`.
     `validate_company_json()` rejects files that break this contract.
  2. PER-SCENARIO TERMINAL VALUE: each DCF scenario may set its own `terminal_growth` or
     `exit_ev_ufcf_multiple` (e.g. Bear for AI-disruption risk = 0% growth) instead of one global 2.5%.
  3. PRICE CEILINGS USE ONLY PRICE-DEPENDENT LENSES: ceiling = min(Lens A: MOS vs Base DCF,
     Lens C: Risk/Reward vs Bear). The Constant-Multiple 5Y IRR is no longer a price ceiling (it barely
     moves with entry price); it is now a HURDLE GATE evaluated at today's price (tier min IRR).
  4. SENSITIVITY & ROUNDED RANGES: ceilings are reported as rounded ranges for Base growth ±1pp, with a
     full ±1pp / ±2pp sensitivity table. Cent-level ceilings are no longer published as verdicts.
  5. AUTO SUMMARY: `build_summary()` + `render_*()` feed `tools/sync_summaries.py`, which writes the
     generated blocks into analysis/README/INDEX and fails CI on drift (`--check`).
  The 9 legacy v3 acceptance tests are kept unchanged; v4 tests are appended after them.

v3 changelog (external audit round 2, Nov 24 2026):
  1. CASH LEDGER & DIVIDEND FUNDING GATE:
     - Tracks beginning free cash (ex-float), Clean FCF, cash drags, planned vs actual dividends,
       buybacks, and ending free cash every year (Y1-Y5).
     - Default policy 'strict_fail' REFUSES to output an IRR if dividends + cash drags exceed
       available free cash + FCF (no more phantom IRR from unfunded dividends).
     - Alternative policies: 'cap_to_available_cash' (cuts dividend to available cash) or
       'external_debt_funded' (borrows shortfall and deducts added debt + interest from Year-5 equity).
  2. WORKING CAPITAL & RECONCILIATION BRIDGE:
     - Direct P&L Unlevered FCF now deducts `ttm_normal_working_capital_investment` (ex-float ΔNWC),
       aligning 100% with Module 01 §2.3.
     - Prints an explicit Reconciliation Bridge comparing Cash-Flow FCF vs P&L-Implied Levered FCF
       and flags any unexplained residual > 5%.
     - Prints Implied Reinvestment Rate (g / ROIIC) for each DCF scenario so growth is sanity-checked.
  3. VALIDATED SOLVER & EXPLICIT STATUSES:
     - `solve_price_for_constant_multiple_irr()` returns `PriceSolveResult(status, price, verified_irr, reason)`
       with statuses: SOLVED | IMPOSSIBLE | UNBOUNDED_PASS | INFEASIBLE_CASH_PLAN | UNBRACKETED_ABOVE_MAX | UNBRACKETED_BELOW_MIN.
     - Impossible targets NEVER collapse to the lower search bound ($1.00); they propagate cleanly
       into Entry Zones as UNQUALIFIED.
  4. TERMINOLOGY & PORTFOLIO SEPARATION:
     - Renamed 'Zero-Rerating Floor' -> 'Constant-Multiple Case (Exit = Entry Multiple)' so it is
       never misread as a guaranteed downside floor.
     - Outputs single-stock price ceilings ONLY; reminds user of required portfolio inputs
       (see Module 05 SSOT) before assigning any % portfolio weight.

Usage:
  python3 valuation_engine.py --input inputs/BKNG.json               # Full v4 report from a JSON input file
  python3 valuation_engine.py --input inputs/BKNG.json --summary-md  # Generated summary block (markdown)
  python3 valuation_engine.py --input inputs/BKNG.json --summary-json
  python3 valuation_engine.py                                        # Legacy v3 fixture (regression only)
  python3 valuation_engine.py --self-test                            # Legacy + v4 acceptance suite
"""

from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import json
import math
import os
import re
import sys


# ==============================================================================
# 1. LEGACY v3 FIXTURE (BKNG — frozen Nov 2026 example used by the regression tests)
#    Live analysis inputs now live in `inputs/TICKER.json` (with provenance per number).
#    Do NOT edit these values to update an analysis — edit the JSON file instead.
#    All dollar figures in $ Millions, except per-share price ($) and DPS ($).
# ==============================================================================
COMPANY_DATA: Dict[str, object] = {
    "ticker": "BKNG",
    "company_name": "Booking Holdings Inc. (Audited Chairman Example)",
    "as_of_date": "2026-11-23",
    "currency": "USD",

    # Market & Macro Inputs (Match risk-free yield to cash-flow currency!)
    "share_price": 146.00,                    # Current share price ($)
    "diluted_shares_m": 749.00,               # Diluted share count (Millions)
    "risk_free_yield": 0.0493,                # Live matched-currency 10Y Sovereign Yield (US 10Y = 4.93%)

    # Balance Sheet & Float Separation ($M)
    "total_debt": 20652.0,                    # ST + LT debt + operating leases
    "total_cash_and_st_inv": 16249.0,         # Unrestricted Cash & Investments
    "customer_float_liability": 7450.0,       # $6,450M Deferred Merchant Bookings + $1,000M FTC Accrued Settlement
    "float_cash_coverage_ratio": 1.00,        # Fraction of Customer Float deducted from Unrestricted Cash (1.0 = strict)
    "minority_interest": 0.0,                 # Non-controlling interest / Preferred stock

    # Trailing 12M (TTM) Forensic P&L & Cash Flow ($M)
    "ttm_revenue": 29026.0,                   # TTM Adj. Revenue (ex-FTC one-off)
    "ttm_core_gaap_ebit": 10219.0,            # Core GAAP Operating Income (already ex-SBC & ex-D&A)
    "effective_tax_rate": 0.210,              # Normalized Effective Cash Tax Rate (21.0%)
    "ttm_depreciation_amort": 372.0,          # D&A (exclude acquisition intangibles amortization if outside Core EBIT)
    "ttm_capex": 324.0,                       # Maintenance + Growth CapEx
    "ttm_normal_working_capital_investment": 0.0,  # Normal operating ΔNWC outflow (Inv + AR - AP, ex-float); positive = cash use
    "ttm_sbc": 594.0,                         # Annual Stock-Based Compensation (deducted 100% as real cash cost from OCF)
    "ttm_ocf": 9561.0,                        # Reported Operating Cash Flow (already includes -ΔNWC_normal + float inflows)
    "ttm_float_inflow": 493.0,                # Non-sustainable float / WC windfall & normalization deducted from OCF
    "ttm_net_interest_expense": 310.0,        # Net Interest = Gross Interest Expense - Interest Income
    "annual_dividend_per_share": 1.68,        # Annual Cash Dividend per share ($)

    # Valuation Calibration
    "wacc": 0.0925,                           # Matched-currency Discount Rate (US 10Y 4.93% + Equity Spread -> 9.25%)
    "terminal_growth": 0.025,                 # Perpetual Terminal Growth Rate (2.5%)
    "assumed_incremental_roic": 0.35,         # Used for Reinvestment Rate sanity check (g / ROIIC)

    # Reverse DCF (Revenue form) cases — ALWAYS state margin path & fines next to the implied growth
    "reverse_dcf_cases": [
        {"label": "Flat margin, no extra fine",     "margin_change_5y": 0.000, "fine_m": 0.0,    "fine_year": 2},
        {"label": "Flat margin, EU fine $0.8B",     "margin_change_5y": 0.000, "fine_m": 800.0,  "fine_year": 2},
        {"label": "-100 bps margin, EU fine $0.8B", "margin_change_5y": -0.010, "fine_m": 800.0, "fine_year": 2},
        {"label": "-300 bps margin, fines $2.0B",   "margin_change_5y": -0.030, "fine_m": 2000.0, "fine_year": 2},
    ],

    # 4 Explicit 10-Year DCF Scenarios
    #   ufcf_cagr_1_5 : Annual UFCF growth years 1-5 (net of margin changes & reinvestment)
    #   ufcf_cagr_6_10: Annual UFCF growth years 6-10
    #   pv_cash_drag  : Present value of pending M&A cash outflows, legal fines, or extra CapEx ($M)
    #   driver_note   : Explicit link from Revenue / Margin / Reinvestment to UFCF growth
    "dcf_scenarios": {
        "Bear (AI + EU Squeeze)": {
            "ufcf_cagr_1_5": -0.025,
            "ufcf_cagr_6_10": 0.010,
            "pv_cash_drag": 1250.0,
            "driver_note": "Rev +2%, Margin -500bps, EU fine $1.5B",
        },
        "Conservative (Slowdown Floor)": {
            "ufcf_cagr_1_5": 0.025,
            "ufcf_cagr_6_10": 0.030,
            "pv_cash_drag": 840.0,
            "driver_note": "Rev +4.5%, Margin -250bps, EU fine $1.0B",
        },
        "Base (Audited Reality)": {
            "ufcf_cagr_1_5": 0.062,
            "ufcf_cagr_6_10": 0.050,
            "pv_cash_drag": 670.0,
            "driver_note": "Rev +7.0%, Margin -100bps, EU fine $0.8B",
        },
        "Bull (Thesis Realized)": {
            "ufcf_cagr_1_5": 0.097,
            "ufcf_cagr_6_10": 0.065,
            "pv_cash_drag": 420.0,
            "driver_note": "Rev +9.0%, Margin +100bps, EU fine $0.5B",
        },
    },

    # Self-Consistent 5-Year Forward IRR Model Assumptions
    "irr_model": {
        "base_clean_fcf_growth": 0.062,           # Annual Clean Levered FCF growth (before buybacks)
        "dividend_growth_rate": 0.070,            # Annual Dividend per share growth
        "fcf_allocation_to_buybacks": 0.85,       # Fraction of post-div, post-drag annual surplus used for buybacks
        "annual_cash_drag_m": 160.0,              # Annualized fine / bolt-on reserve ($800M / 5 yrs)
        # Policy when planned dividends exceed (beginning free cash + Clean FCF - cash_drag):
        #   'strict_fail'           -> Refuse to compute IRR; flag INFEASIBLE_UNFUNDED_DIVIDEND (recommended default)
        #   'cap_to_available_cash' -> Cut dividend to available cash; report dividend_cut_years
        #   'external_debt_funded'  -> Borrow shortfall at after_tax_debt_cost and deduct ending debt from Year-5 equity
        "dividend_funding_policy": "strict_fail",
        "after_tax_debt_cost": 0.045,             # Used only if dividend_funding_policy == 'external_debt_funded'
        "exit_multiple_scenarios": {
            "De-rating (-15% Multiple)": 0.85,
            "Constant-Multiple Case (1.00x)": 1.00,
            "Mild Re-rating (+15% Multiple)": 1.15,
        },
    },

    # Required Growth Table Inputs
    "operating_leverage_factor": 1.00,            # FCF growth / Revenue growth (1.00 = flat margin; 1.10 = mild expansion)

    # Single-Stock Entry Zone Rules — a tier qualifies ONLY if ALL 3 lenses pass; binding ceiling = lowest price.
    # NOTE: These are SINGLE-STOCK price ceilings only. Actual portfolio % sizing MUST follow Module 05 (SSOT).
    "entry_zone_rules": [
        {"tier": "Starter",   "min_mos": 0.15, "min_const_mult_irr": 0.11, "min_rr": 2.0},
        {"tier": "Core",      "min_mos": 0.25, "min_const_mult_irr": 0.13, "min_rr": 3.0},
        {"tier": "Fat Pitch", "min_mos": 0.35, "min_const_mult_irr": 0.15, "min_rr": 4.0},
    ],
}


# ==============================================================================
# 2. DATA STRUCTURES & CORE FINANCIAL FUNCTIONS
# ==============================================================================
@dataclass
class ForensicSummary:
    market_cap: float
    free_cash_ex_float: float
    float_adjusted_net_debt: float
    float_adjusted_ev: float
    reported_fcf: float
    true_fcf_ex_sbc: float
    clean_economic_fcf: float
    normal_nwc_investment: float
    unlevered_fcf_pl: float
    pl_implied_levered_fcf: float
    reconciliation_gap: float
    reconciliation_gap_pct: float
    clean_fcf_yield_mcap: float
    clean_fcf_yield_ev: float
    spread_vs_rf: float
    current_p_clean_fcf: float
    current_ev_ufcf: float


@dataclass
class YearCashLedger:
    year: int
    beg_cash: float
    clean_fcf: float
    cash_drag: float
    planned_div: float
    actual_div: float
    buyback: float
    debt_added: float
    end_cash: float
    shortfall: float


@dataclass
class IRRSimulationResult:
    feasible: bool
    status: str                          # OK | OK_DIVIDEND_CUT | OK_DEBT_FUNDED | INFEASIBLE_UNFUNDED_DIVIDEND | INFEASIBLE_OPERATING_DEFICIT
    irr: Optional[float]
    end_price: Optional[float]
    end_shares_m: float
    avg_net_buyback_rate: float
    ending_free_cash: float
    total_debt_added: float
    total_shortfall: float
    first_shortfall_year: Optional[int]
    dividend_cut_years: List[int]
    ledger: List[YearCashLedger]
    message: str


@dataclass
class PriceSolveResult:
    status: str                          # SOLVED | IMPOSSIBLE | UNBOUNDED_PASS | INFEASIBLE_CASH_PLAN | UNBRACKETED_ABOVE_MAX | UNBRACKETED_BELOW_MIN
    price: Optional[float]
    verified_irr: Optional[float]
    reason: str


def compute_forensic_metrics(d: Dict[str, object]) -> ForensicSummary:
    price = float(d["share_price"])
    shares = float(d["diluted_shares_m"])
    mcap = price * shares

    total_cash = float(d["total_cash_and_st_inv"])
    float_liab = float(d["customer_float_liability"])
    float_cov = float(d["float_cash_coverage_ratio"])
    free_cash = max(0.0, total_cash - float_liab * float_cov)
    unfunded_float = max(0.0, float_liab * float_cov - total_cash)

    net_debt = float(d["total_debt"]) + unfunded_float - free_cash
    ev = mcap + net_debt + float(d["minority_interest"])

    # Cash-Flow path (OCF already reflects -ΔNWC_normal + float inflows + SBC add-back - cash interest/taxes)
    reported_fcf = float(d["ttm_ocf"]) - float(d["ttm_capex"])
    true_fcf = reported_fcf - float(d["ttm_sbc"])
    clean_fcf = true_fcf - float(d["ttm_float_inflow"])

    # Direct P&L path (aligned with Module 01 §2.3: NOPAT + D&A - CapEx - Normal ΔNWC)
    tax_rate = float(d["effective_tax_rate"])
    nwc_inv = float(d.get("ttm_normal_working_capital_investment", 0.0))
    nopat = float(d["ttm_core_gaap_ebit"]) * (1.0 - tax_rate)
    ufcf_pl = nopat + float(d["ttm_depreciation_amort"]) - float(d["ttm_capex"]) - nwc_inv

    # Cross-check reconciliation bridge between Cash-Flow path and P&L path
    after_tax_net_int = float(d["ttm_net_interest_expense"]) * (1.0 - tax_rate)
    pl_implied_levered_fcf = ufcf_pl - after_tax_net_int
    rec_gap = clean_fcf - pl_implied_levered_fcf
    rec_gap_pct = rec_gap / abs(ufcf_pl) if abs(ufcf_pl) > 1e-9 else 0.0

    rf = float(d.get("risk_free_yield", d.get("us_10y_yield", 0.0)))

    return ForensicSummary(
        market_cap=mcap,
        free_cash_ex_float=free_cash,
        float_adjusted_net_debt=net_debt,
        float_adjusted_ev=ev,
        reported_fcf=reported_fcf,
        true_fcf_ex_sbc=true_fcf,
        clean_economic_fcf=clean_fcf,
        normal_nwc_investment=nwc_inv,
        unlevered_fcf_pl=ufcf_pl,
        pl_implied_levered_fcf=pl_implied_levered_fcf,
        reconciliation_gap=rec_gap,
        reconciliation_gap_pct=rec_gap_pct,
        clean_fcf_yield_mcap=clean_fcf / mcap if mcap > 0 else 0.0,
        clean_fcf_yield_ev=ufcf_pl / ev if ev > 0 else 0.0,
        spread_vs_rf=(clean_fcf / mcap - rf) if mcap > 0 else 0.0,
        current_p_clean_fcf=mcap / clean_fcf if clean_fcf > 0 else float("inf"),
        current_ev_ufcf=ev / ufcf_pl if ufcf_pl > 0 else float("inf"),
    )


def _bisect_bracketed(
    f,
    target: float,
    low: float,
    high: float,
    increasing: bool = True,
    iters: int = 160,
    tol: float = 1e-7,
) -> Optional[float]:
    """Safe bisection: returns None if target is NOT bracketed between f(low) and f(high)."""
    f_lo = f(low)
    f_hi = f(high)
    if f_lo is None or f_hi is None:
        return None
    if increasing:
        if target < f_lo - tol or target > f_hi + tol:
            return None
    else:
        if target > f_lo + tol or target < f_hi - tol:
            return None
    lo, hi = low, high
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        val = f(mid)
        if val is None:
            return None
        if abs(val - target) <= tol:
            return mid
        if (val < target) == increasing:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def irr_from_cash_flows(cfs: List[float]) -> Optional[float]:
    """True IRR on annual dated cash flows (cfs[0] at t=0, negative)."""
    if not cfs or cfs[0] >= 0.0:
        return None
    if sum(cfs[1:]) <= 0.0:
        return None
    def npv(r: float) -> float:
        return sum(cf / ((1.0 + r) ** t) for t, cf in enumerate(cfs))
    hi = 5.0
    while npv(hi) > 0.0 and hi < 1e9:
        hi *= 2.0
    return _bisect_bracketed(npv, 0.0, -0.95, hi, increasing=False, tol=1e-9)


def dcf_enterprise_value(
    ufcf_0: float,
    g_1_5: float,
    g_6_10: float,
    wacc: float,
    g_term: float,
    pv_cash_drag: float = 0.0,
    exit_multiple: Optional[float] = None,
) -> float:
    """10-year Explicit DCF + terminal value.

    Terminal value = Gordon Growth on year-10 UFCF (default), or — when `exit_multiple` is given —
    year-10 UFCF x exit EV/UFCF multiple (v4: lets a Bear case use e.g. 8-10x instead of a growth formula).
    """
    if exit_multiple is None and wacc <= g_term:
        raise ValueError("WACC must be strictly greater than terminal growth rate.")
    if exit_multiple is not None and exit_multiple <= 0.0:
        raise ValueError("Exit EV/UFCF multiple must be positive.")
    pv = 0.0
    cf = ufcf_0
    for yr in range(1, 11):
        g = g_1_5 if yr <= 5 else g_6_10
        cf *= (1.0 + g)
        pv += cf / ((1.0 + wacc) ** yr)
    if exit_multiple is not None:
        tv = cf * exit_multiple
    else:
        tv = cf * (1.0 + g_term) / (wacc - g_term)
    return pv + tv / ((1.0 + wacc) ** 10) - pv_cash_drag


def dcf_ev_revenue_path(
    rev_0: float,
    ufcf_0: float,
    rev_cagr: float,
    margin_change_5y: float,
    fine_m: float,
    fine_year: int,
    wacc: float,
    g_term: float,
) -> float:
    """10Y DCF driven by Revenue CAGR x UFCF margin path (linear phase-in Y1-Y5) minus a dated one-off fine."""
    if wacc <= g_term:
        raise ValueError("WACC must be strictly greater than terminal growth rate.")
    m0 = ufcf_0 / rev_0
    rev = rev_0
    pv = 0.0
    margin = m0
    for yr in range(1, 11):
        rev *= (1.0 + rev_cagr)
        margin = m0 + margin_change_5y * min(yr, 5) / 5.0
        cf = rev * margin - (fine_m if yr == fine_year else 0.0)
        pv += cf / ((1.0 + wacc) ** yr)
    tv = rev * margin * (1.0 + g_term) / (wacc - g_term)
    return pv + tv / ((1.0 + wacc) ** 10)


def solve_reverse_dcf_ufcf_cagr(target_ev: float, ufcf_0: float, wacc: float, g_term: float) -> Optional[float]:
    """Form (a): constant 10Y UFCF CAGR implied by Float-Adj EV (no margin path, no fines)."""
    return _bisect_bracketed(lambda g: dcf_enterprise_value(ufcf_0, g, g, wacc, g_term), target_ev, -0.40, 0.80)


def solve_reverse_dcf_revenue_cagr(target_ev: float, d: Dict[str, object], fs: ForensicSummary, case: Dict) -> Optional[float]:
    """Form (b): constant 10Y Revenue CAGR implied by Float-Adj EV under the stated margin path + fine."""
    return _bisect_bracketed(
        lambda g: dcf_ev_revenue_path(
            float(d["ttm_revenue"]), fs.unlevered_fcf_pl, g,
            float(case["margin_change_5y"]), float(case["fine_m"]), int(case["fine_year"]),
            float(d["wacc"]), float(d["terminal_growth"]),
        ),
        target_ev, -0.40, 0.80,
    )


def simulate_5y_forward_irr(
    d: Dict[str, object],
    fs: ForensicSummary,
    clean_fcf_growth: float,
    exit_multiple_ratio: float,
    entry_price: Optional[float] = None,
) -> IRRSimulationResult:
    """
    Self-consistent 5-Year Forward IRR simulation with explicit annual cash ledger.
    Enforces dividend & buyback funding against beginning free cash (ex-float) + annual Clean FCF - cash_drag.
    """
    cfg = d["irr_model"]
    price_0 = float(d["share_price"]) if entry_price is None else float(entry_price)
    shares = float(d["diluted_shares_m"])
    shares_0 = shares
    fcf = fs.clean_economic_fcf
    dps = float(d["annual_dividend_per_share"])
    div_g = float(cfg["dividend_growth_rate"])
    bb_alloc = float(cfg["fcf_allocation_to_buybacks"])
    cash_drag = float(cfg["annual_cash_drag_m"])
    policy = str(cfg.get("dividend_funding_policy", "strict_fail"))
    debt_cost = float(cfg.get("after_tax_debt_cost", 0.045))

    if price_0 <= 0.0 or fcf <= 0.0 or shares <= 0.0:
        return IRRSimulationResult(
            feasible=False, status="INFEASIBLE_OPERATING_DEFICIT", irr=None, end_price=None,
            end_shares_m=shares, avg_net_buyback_rate=0.0, ending_free_cash=fs.free_cash_ex_float,
            total_debt_added=0.0, total_shortfall=0.0, first_shortfall_year=1,
            dividend_cut_years=[], ledger=[], message="Non-positive starting price, shares, or Clean FCF.",
        )

    m0 = price_0 / (fs.clean_economic_fcf / shares_0)
    m_exit = m0 * exit_multiple_ratio

    cash = fs.free_cash_ex_float
    cum_debt_added = 0.0
    total_shortfall = 0.0
    first_shortfall_year: Optional[int] = None
    dividend_cut_years: List[int] = []
    ledger: List[YearCashLedger] = []
    cash_flows: List[float] = [-price_0]
    infeasible_status: Optional[str] = None

    for yr in range(1, 6):
        beg_cash = cash
        fcf *= (1.0 + clean_fcf_growth)
        dps *= (1.0 + div_g)
        extra_interest = cum_debt_added * debt_cost if policy == "external_debt_funded" else 0.0
        fcf_after_extra_int = fcf - extra_interest
        available_before_div = beg_cash + fcf_after_extra_int - cash_drag
        planned_div = dps * shares

        debt_added = 0.0
        shortfall = 0.0
        buyback = 0.0

        if available_before_div < 0.0 and policy != "external_debt_funded":
            shortfall = planned_div - available_before_div
            total_shortfall += shortfall
            if first_shortfall_year is None:
                first_shortfall_year = yr
            infeasible_status = "INFEASIBLE_OPERATING_DEFICIT"
            actual_div = 0.0
            actual_dps = 0.0
            end_cash = 0.0
        elif planned_div > available_before_div + 1e-9:
            shortfall = planned_div - max(0.0, available_before_div)
            total_shortfall += shortfall
            if first_shortfall_year is None:
                first_shortfall_year = yr
            if policy == "strict_fail":
                infeasible_status = infeasible_status or "INFEASIBLE_UNFUNDED_DIVIDEND"
                actual_div = 0.0
                actual_dps = 0.0
                end_cash = 0.0  # All available cash would be exhausted trying to meet the planned dividend
            elif policy == "cap_to_available_cash":
                actual_div = max(0.0, available_before_div)
                actual_dps = actual_div / shares
                dividend_cut_years.append(yr)
                end_cash = 0.0
            elif policy == "external_debt_funded":
                debt_added = planned_div - available_before_div
                cum_debt_added += debt_added
                actual_div = planned_div
                actual_dps = dps
                end_cash = 0.0
            else:
                raise ValueError(f"Unknown dividend_funding_policy: {policy}")
        else:
            actual_div = planned_div
            actual_dps = dps
            # Buybacks funded strictly from annual surplus (never draining prior cash balance)
            annual_surplus = max(0.0, fcf_after_extra_int - actual_div - cash_drag)
            buyback = min(annual_surplus * bb_alloc, available_before_div - actual_div)
            m_yr = m0 + (m_exit - m0) * (yr / 5.0)
            est_share_price = (fcf_after_extra_int / shares) * m_yr
            if est_share_price > 0.0 and buyback > 0.0:
                shares = max(shares * 0.5, shares - buyback / est_share_price)
            end_cash = available_before_div - actual_div - buyback

        cash = end_cash
        cash_flows.append(actual_dps)
        ledger.append(YearCashLedger(
            year=yr, beg_cash=beg_cash, clean_fcf=fcf_after_extra_int, cash_drag=cash_drag,
            planned_div=planned_div, actual_div=actual_div, buyback=buyback,
            debt_added=debt_added, end_cash=end_cash, shortfall=shortfall,
        ))

    avg_net_bb_rate = 1.0 - (shares / shares_0) ** (1.0 / 5.0)

    if infeasible_status is not None:
        return IRRSimulationResult(
            feasible=False, status=infeasible_status, irr=None, end_price=None,
            end_shares_m=shares, avg_net_buyback_rate=avg_net_bb_rate,
            ending_free_cash=cash, total_debt_added=cum_debt_added,
            total_shortfall=total_shortfall, first_shortfall_year=first_shortfall_year,
            dividend_cut_years=dividend_cut_years, ledger=ledger,
            message=f"Plan infeasible ({infeasible_status}): cash shortfall starts Y{first_shortfall_year}, total ${total_shortfall:,.1f}M.",
        )

    # Year-5 equity value: multiple on ending FCF, less any extra debt borrowed under external_debt_funded
    ending_fcf = ledger[-1].clean_fcf
    end_equity_val = max(0.0, ending_fcf * m_exit - cum_debt_added)
    end_price = end_equity_val / shares
    cash_flows[-1] += end_price
    irr = irr_from_cash_flows(cash_flows)

    if dividend_cut_years:
        status = "OK_DIVIDEND_CUT"
        msg = f"Dividends capped to available cash in year(s) {dividend_cut_years} (total cut ${total_shortfall:,.1f}M)."
    elif cum_debt_added > 0.0:
        status = "OK_DEBT_FUNDED"
        msg = f"Dividends funded with ${cum_debt_added:,.1f}M added debt (deducted from Year-5 equity)."
    else:
        status = "OK"
        msg = "Fully self-funded from beginning free cash + Clean FCF."

    return IRRSimulationResult(
        feasible=True, status=status, irr=irr, end_price=end_price,
        end_shares_m=shares, avg_net_buyback_rate=avg_net_bb_rate,
        ending_free_cash=cash, total_debt_added=cum_debt_added,
        total_shortfall=total_shortfall, first_shortfall_year=first_shortfall_year,
        dividend_cut_years=dividend_cut_years, ledger=ledger, message=msg,
    )


def solve_required_fcf_growth(d: Dict[str, object], fs: ForensicSummary, target_irr: float, ratio: float) -> Optional[float]:
    """Required annual Clean FCF growth to achieve target 5Y IRR at today's price (returns None if unbracketed/infeasible)."""
    def f(g: float) -> Optional[float]:
        res = simulate_5y_forward_irr(d, fs, g, ratio)
        return res.irr if res.feasible else None

    # Find lowest feasible growth in [-0.25, 0.60]
    lo, hi = -0.25, 0.60
    if f(hi) is None or f(hi) < target_irr:
        return None
    if f(lo) is None:
        # Advance lower bound until feasible
        for step in range(1, 86):
            cand = lo + step * 0.01
            if f(cand) is not None:
                lo = cand
                break
        else:
            return None
    return _bisect_bracketed(f, target_irr, lo, hi, increasing=True, tol=1e-6)


def solve_price_for_constant_multiple_irr(
    d: Dict[str, object],
    fs: ForensicSummary,
    target_irr: float,
    p_min: float = 0.01,
    p_max: Optional[float] = None,
) -> PriceSolveResult:
    """
    Finds the highest entry price that still delivers `target_irr` under the Constant-Multiple Case
    (exit P/Clean-FCF == entry P/Clean-FCF). Validates feasibility, bracketing, and post-solve residual.
    """
    g = float(d["irr_model"]["base_clean_fcf_growth"])
    p_ref = float(d["share_price"])
    hi = max(p_ref * 10.0, 1000.0) if p_max is None else float(p_max)

    res_ref = simulate_5y_forward_irr(d, fs, g, 1.0, entry_price=p_ref)
    if not res_ref.feasible or res_ref.irr is None:
        return PriceSolveResult(
            status="INFEASIBLE_CASH_PLAN", price=None, verified_irr=None,
            reason=f"Cash plan infeasible ({res_ref.status}): {res_ref.message}",
        )

    # Check if IRR is invariant to entry price (zero dividends AND zero buybacks)
    res_lo = simulate_5y_forward_irr(d, fs, g, 1.0, entry_price=p_min)
    res_hi = simulate_5y_forward_irr(d, fs, g, 1.0, entry_price=hi)
    if not res_lo.feasible or res_lo.irr is None or not res_hi.feasible or res_hi.irr is None:
        return PriceSolveResult(
            status="INFEASIBLE_CASH_PLAN", price=None, verified_irr=None,
            reason="Cash plan infeasible across test price range.",
        )

    # Price-invariant degeneracy check (e.g., 0 dividend & 0 buyback -> IRR == FCF growth for all p > 0)
    if abs(res_lo.irr - res_hi.irr) < 1e-6:
        if res_lo.irr >= target_irr - 1e-6:
            return PriceSolveResult(
                status="UNBOUNDED_PASS", price=None, verified_irr=res_lo.irr,
                reason=f"IRR is price-invariant at {res_lo.irr*100:.2f}% >= target {target_irr*100:.2f}%; no upper price cap from IRR.",
            )
        return PriceSolveResult(
            status="IMPOSSIBLE", price=None, verified_irr=res_lo.irr,
            reason=f"IRR is price-invariant at {res_lo.irr*100:.2f}% < target {target_irr*100:.2f}% for all positive prices (0 cash returned).",
        )

    # Adaptively expand upper bound if even hi still passes target_irr
    max_cap = max(p_ref * 1e6, 1e8)
    while res_hi.irr > target_irr and hi < max_cap:
        hi *= 5.0
        res_hi = simulate_5y_forward_irr(d, fs, g, 1.0, entry_price=hi)
        if not res_hi.feasible or res_hi.irr is None:
            break

    if res_hi.irr is not None and res_hi.irr > target_irr:
        if g >= target_irr - 1e-6:
            return PriceSolveResult(
                status="UNBOUNDED_PASS", price=None, verified_irr=res_hi.irr,
                reason=f"FCF growth ({g*100:.2f}%) >= target ({target_irr*100:.2f}%); IRR exceeds target at every positive price.",
            )
        return PriceSolveResult(
            status="UNBRACKETED_ABOVE_MAX", price=None, verified_irr=res_hi.irr,
            reason=f"Target IRR still exceeded at upper test bound ${hi:,.2f} (IRR={res_hi.irr*100:.2f}%).",
        )

    # Check lower bound
    if res_lo.irr < target_irr:
        # Test smaller price to distinguish mathematically impossible vs below p_min
        res_tiny = simulate_5y_forward_irr(d, fs, g, 1.0, entry_price=1e-4)
        if res_tiny.irr is None or res_tiny.irr < target_irr:
            return PriceSolveResult(
                status="IMPOSSIBLE", price=None, verified_irr=res_lo.irr,
                reason=f"Even near $0 (${p_min}), IRR ({res_lo.irr*100:.2f}%) cannot reach target {target_irr*100:.2f}%.",
            )
        return PriceSolveResult(
            status="UNBRACKETED_BELOW_MIN", price=None, verified_irr=res_lo.irr,
            reason=f"Solution lies below search floor ${p_min:,.2f}.",
        )

    # Bracketed: r(p_min) >= target_irr >= r(hi)
    def irr_at(p: float) -> Optional[float]:
        r = simulate_5y_forward_irr(d, fs, g, 1.0, entry_price=p)
        return r.irr if r.feasible else None

    p_star = _bisect_bracketed(irr_at, target_irr, p_min, hi, increasing=False, tol=1e-7)
    if p_star is None:
        return PriceSolveResult(status="IMPOSSIBLE", price=None, verified_irr=None, reason="Solver failed to bracket root.")

    verify = simulate_5y_forward_irr(d, fs, g, 1.0, entry_price=p_star)
    if not verify.feasible or verify.irr is None or abs(verify.irr - target_irr) > 1e-4:
        return PriceSolveResult(
            status="IMPOSSIBLE", price=None, verified_irr=verify.irr,
            reason=f"Post-solve verification failed at ${p_star:,.2f}.",
        )

    return PriceSolveResult(
        status="SOLVED", price=p_star, verified_irr=verify.irr,
        reason=f"Verified IRR = {verify.irr*100:.2f}% at ${p_star:,.2f} ({verify.status}).",
    )


# ==============================================================================
# 2b. v4 — JSON INPUTS (PROVENANCE), PER-SCENARIO TERMINAL VALUE,
#     2-LENS PRICE CEILINGS + IRR HURDLE GATE, SENSITIVITY RANGES, SUMMARY
# ==============================================================================
SCHEMA_VERSION = "4.0"

# Reported numbers: each needs as_of_date + (source_url or filing_ref) + verification level.
FACT_FIELDS: Tuple[str, ...] = (
    "share_price", "diluted_shares_m", "risk_free_yield",
    "total_debt", "total_cash_and_st_inv", "customer_float_liability", "minority_interest",
    "ttm_revenue", "ttm_core_gaap_ebit", "ttm_depreciation_amort", "ttm_capex", "ttm_sbc",
    "ttm_ocf", "ttm_net_interest_expense", "annual_dividend_per_share",
)
# Analyst judgments: each needs a written rationale.
ASSUMPTION_FIELDS: Tuple[str, ...] = (
    "effective_tax_rate", "ttm_normal_working_capital_investment", "ttm_float_inflow",
    "float_cash_coverage_ratio", "wacc", "terminal_growth", "assumed_incremental_roic",
    "operating_leverage_factor",
)
VERIFICATION_LEVELS: Tuple[str, ...] = ("verified", "partially_verified", "carried_over_unverified")
DEFAULT_SENSITIVITY_DELTAS: Tuple[float, ...] = (-0.02, -0.01, 0.0, 0.01, 0.02)
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _is_number(x: object) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def validate_company_json(raw: Dict[str, object]) -> List[str]:
    """Returns a list of human-readable errors (empty list = valid v4 input file)."""
    errs: List[str] = []
    for key in ("schema_version", "ticker", "company_name", "as_of_date", "currency", "facts",
                "assumptions", "reverse_dcf_cases", "dcf_scenarios", "irr_model", "entry_zone_rules"):
        if key not in raw:
            errs.append(f"missing top-level key: {key}")
    if errs:
        return errs
    if str(raw["schema_version"]).split(".")[0] != SCHEMA_VERSION.split(".")[0]:
        errs.append(f"schema_version {raw['schema_version']} != {SCHEMA_VERSION}")
    if not _DATE_RE.match(str(raw["as_of_date"])):
        errs.append("as_of_date must be YYYY-MM-DD")

    facts = raw["facts"]
    for k in FACT_FIELDS:
        f = facts.get(k) if isinstance(facts, dict) else None
        if not isinstance(f, dict):
            errs.append(f"facts.{k}: missing")
            continue
        if not _is_number(f.get("value")):
            errs.append(f"facts.{k}: value must be a number")
        if not _DATE_RE.match(str(f.get("as_of_date", ""))):
            errs.append(f"facts.{k}: as_of_date must be YYYY-MM-DD")
        if not (str(f.get("source_url", "")).strip() or str(f.get("filing_ref", "")).strip()):
            errs.append(f"facts.{k}: needs source_url or filing_ref")
        if f.get("verification") not in VERIFICATION_LEVELS:
            errs.append(f"facts.{k}: verification must be one of {VERIFICATION_LEVELS}")

    assumptions = raw["assumptions"]
    for k in ASSUMPTION_FIELDS:
        a = assumptions.get(k) if isinstance(assumptions, dict) else None
        if not isinstance(a, dict):
            errs.append(f"assumptions.{k}: missing")
            continue
        if not _is_number(a.get("value")):
            errs.append(f"assumptions.{k}: value must be a number")
        if not str(a.get("rationale", "")).strip():
            errs.append(f"assumptions.{k}: needs a rationale")

    wacc = assumptions.get("wacc", {}).get("value") if isinstance(assumptions, dict) else None
    scen = raw["dcf_scenarios"]
    if not isinstance(scen, dict) or not any(n.startswith("Base") for n in scen) or not any(n.startswith("Bear") for n in scen):
        errs.append("dcf_scenarios must include one 'Base...' and one 'Bear...' scenario")
    elif isinstance(scen, dict):
        for name, cfg in scen.items():
            for k in ("ufcf_cagr_1_5", "ufcf_cagr_6_10", "pv_cash_drag"):
                if not _is_number(cfg.get(k)):
                    errs.append(f"dcf_scenarios.{name}.{k}: must be a number")
            if "terminal_growth" in cfg and "exit_ev_ufcf_multiple" in cfg:
                errs.append(f"dcf_scenarios.{name}: set terminal_growth OR exit_ev_ufcf_multiple, not both")
            if "terminal_growth" in cfg and _is_number(wacc) and float(cfg["terminal_growth"]) >= float(wacc):
                errs.append(f"dcf_scenarios.{name}.terminal_growth must be < wacc")
            if "exit_ev_ufcf_multiple" in cfg and not (_is_number(cfg["exit_ev_ufcf_multiple"]) and cfg["exit_ev_ufcf_multiple"] > 0):
                errs.append(f"dcf_scenarios.{name}.exit_ev_ufcf_multiple must be > 0")
            if not str(cfg.get("driver_note", "")).strip():
                errs.append(f"dcf_scenarios.{name}: needs driver_note")

    rules = raw["entry_zone_rules"]
    if not isinstance(rules, list) or not rules:
        errs.append("entry_zone_rules must be a non-empty list")
    else:
        for r in rules:
            for k in ("min_mos", "min_const_mult_irr", "min_rr"):
                if not _is_number(r.get(k)):
                    errs.append(f"entry_zone_rules[{r.get('tier')}].{k}: must be a number")
    return errs


def company_dict_from_json(raw: Dict[str, object], source_path: str = "") -> Dict[str, object]:
    """Flattens a validated v4 JSON document into the legacy engine dict (plus provenance metadata)."""
    errs = validate_company_json(raw)
    if errs:
        raise ValueError("Invalid v4 input file:\n  - " + "\n  - ".join(errs))
    d: Dict[str, object] = {
        "ticker": raw["ticker"],
        "company_name": raw["company_name"],
        "as_of_date": raw["as_of_date"],
        "currency": raw["currency"],
        "analysis_path": raw.get("analysis_path", ""),
    }
    for k in FACT_FIELDS:
        d[k] = float(raw["facts"][k]["value"])
    for k in ASSUMPTION_FIELDS:
        d[k] = float(raw["assumptions"][k]["value"])
    for k in ("reverse_dcf_cases", "dcf_scenarios", "irr_model", "entry_zone_rules"):
        d[k] = deepcopy(raw[k])
    d["sensitivity_growth_deltas"] = list(raw.get("sensitivity_growth_deltas", DEFAULT_SENSITIVITY_DELTAS))
    d["_provenance"] = {
        level: sorted(k for k in FACT_FIELDS if raw["facts"][k]["verification"] == level)
        for level in VERIFICATION_LEVELS
    }
    d["_source_path"] = source_path
    return d


def load_company_json(path: str) -> Dict[str, object]:
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    return company_dict_from_json(raw, source_path=path)


def _find_scenario(d: Dict[str, object], prefix: str) -> Tuple[str, Dict[str, object]]:
    for name, cfg in d["dcf_scenarios"].items():
        if name.startswith(prefix):
            return name, cfg
    raise ValueError(f"No DCF scenario starting with '{prefix}'")


def scenario_terminal_label(d: Dict[str, object], cfg: Dict[str, object]) -> str:
    if "exit_ev_ufcf_multiple" in cfg:
        return f"exit {float(cfg['exit_ev_ufcf_multiple']):.1f}x"
    return f"g {float(cfg.get('terminal_growth', d['terminal_growth']))*100:.1f}%"


def scenario_fair_value(d: Dict[str, object], fs: ForensicSummary, cfg: Dict[str, object], growth_delta: float = 0.0) -> float:
    """Per-share fair value of one DCF scenario; growth_delta shifts BOTH 1-5Y and 6-10Y UFCF growth."""
    exit_mult = cfg.get("exit_ev_ufcf_multiple")
    ev = dcf_enterprise_value(
        fs.unlevered_fcf_pl,
        float(cfg["ufcf_cagr_1_5"]) + growth_delta,
        float(cfg["ufcf_cagr_6_10"]) + growth_delta,
        float(d["wacc"]),
        float(cfg.get("terminal_growth", d["terminal_growth"])),
        float(cfg["pv_cash_drag"]),
        exit_multiple=float(exit_mult) if exit_mult is not None else None,
    )
    return (ev - fs.float_adjusted_net_debt - float(d["minority_interest"])) / float(d["diluted_shares_m"])


@dataclass
class TierAssessment:
    tier: str
    min_mos: float
    min_rr: float
    min_irr: float
    lens_a_mos: float          # price ceiling from MOS vs Base DCF
    lens_c_rr: float           # price ceiling from Risk/Reward vs Bear
    ceiling: float             # min(lens A, lens C)
    binder: str                # "MOS" | "R/R"
    price_ok: bool             # today's price <= ceiling
    irr_gate_ok: bool          # Constant-Multiple 5Y IRR at today's price >= min_irr
    qualifies_today: bool


@dataclass
class EntryAssessment:
    growth_delta: float
    price: float
    base_fv: float
    bear_fv: float
    mos_today: float
    rr_today: float
    irr_today: Optional[float]
    irr_status: str
    tiers: List[TierAssessment]
    tier_today: Optional[str]
    reason: str


def assess_entry(d: Dict[str, object], fs: ForensicSummary, growth_delta: float = 0.0) -> EntryAssessment:
    """v4 entry assessment: price ceilings from Lens A + Lens C only; Constant-Multiple IRR = hurdle gate at today's price."""
    price = float(d["share_price"])
    _, base_cfg = _find_scenario(d, "Base")
    _, bear_cfg = _find_scenario(d, "Bear")
    base_fv = scenario_fair_value(d, fs, base_cfg, growth_delta)
    bear_fv = scenario_fair_value(d, fs, bear_cfg, 0.0)

    irr_res = simulate_5y_forward_irr(d, fs, float(d["irr_model"]["base_clean_fcf_growth"]) + growth_delta, 1.0)
    irr_today = irr_res.irr if (irr_res.feasible and irr_res.irr is not None) else None

    up = base_fv - price
    down = price - bear_fv
    rr_today = (up / down) if down > 1e-9 else float("inf")
    mos_today = 1.0 - price / base_fv if base_fv > 0 else float("-inf")

    tiers: List[TierAssessment] = []
    tier_today: Optional[str] = None
    for rule in d["entry_zone_rules"]:
        mos, k, min_irr = float(rule["min_mos"]), float(rule["min_rr"]), float(rule["min_const_mult_irr"])
        p_a = base_fv * (1.0 - mos)
        p_c = (base_fv + k * bear_fv) / (1.0 + k)
        ceiling, binder = (p_a, "MOS") if p_a <= p_c else (p_c, "R/R")
        price_ok = price <= ceiling + 1e-9
        gate_ok = irr_today is not None and irr_today >= min_irr - 1e-12
        qualifies = price_ok and gate_ok
        if qualifies:
            tier_today = str(rule["tier"])
        tiers.append(TierAssessment(str(rule["tier"]), mos, k, min_irr, p_a, p_c, ceiling, binder, price_ok, gate_ok, qualifies))

    if tier_today is not None:
        reason = f"ผ่านเกณฑ์ {tier_today}"
    elif tiers and not tiers[0].price_ok:
        reason = f"ราคาสูงกว่าเพดาน {tiers[0].tier}"
    elif irr_today is None:
        reason = f"แผนเงินสดเป็นไปไม่ได้ ({irr_res.status})"
    else:
        reason = f"ผลตอบแทน 5 ปี {irr_today*100:.1f}% ต่ำกว่าเกณฑ์ขั้นต่ำ {tiers[0].min_irr*100:.0f}%"
    return EntryAssessment(growth_delta, price, base_fv, bear_fv, mos_today, rr_today, irr_today,
                           irr_res.status, tiers, tier_today, reason)


def price_step(p: float) -> float:
    """Display rounding step so ceilings never look more precise than the inputs."""
    p = abs(p)
    if p < 20:
        return 0.5
    if p < 100:
        return 1.0
    if p < 500:
        return 5.0
    if p < 2000:
        return 10.0
    return 50.0


def round_to_step(x: float, step: float) -> float:
    return round(round(x / step) * step, 2)


def _fmt_money(x: float) -> str:
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def build_summary(d: Dict[str, object]) -> Dict[str, object]:
    """Machine-readable v4 summary used for reports, generated markdown blocks and the CI drift check."""
    fs = compute_forensic_metrics(d)
    deltas = sorted(set([float(x) for x in d.get("sensitivity_growth_deltas", DEFAULT_SENSITIVITY_DELTAS)] + [-0.01, 0.0, 0.01]))
    by_delta = {dl: assess_entry(d, fs, dl) for dl in deltas}
    central = by_delta[0.0]
    step = price_step(central.price)

    tiers_out = []
    for i, t in enumerate(central.tiers):
        lo = round_to_step(by_delta[-0.01].tiers[i].ceiling, step)
        hi = round_to_step(by_delta[0.01].tiers[i].ceiling, step)
        tiers_out.append({
            "tier": t.tier,
            "rule": {"min_mos": t.min_mos, "min_rr": t.min_rr, "min_irr": t.min_irr},
            "central": round_to_step(t.ceiling, step),
            "range_low": min(lo, hi),
            "range_high": max(lo, hi),
            "binder": t.binder,
            "irr_gate_ok_today": t.irr_gate_ok,
            "qualifies_today": t.qualifies_today,
        })

    rows = []
    for dl in deltas:
        a = by_delta[dl]
        rows.append({
            "growth_delta_pp": round(dl * 100, 2),
            "base_fv": round_to_step(a.base_fv, step),
            "rr_today": round(a.rr_today, 2) if math.isfinite(a.rr_today) else None,
            "irr_today_pct": round(a.irr_today * 100, 1) if a.irr_today is not None else None,
            "ceilings": {t.tier: round_to_step(t.ceiling, step) for t in a.tiers},
            "tier_today": a.tier_today or "Watchlist",
        })

    implied = solve_reverse_dcf_ufcf_cagr(fs.float_adjusted_ev, fs.unlevered_fcf_pl, float(d["wacc"]), float(d["terminal_growth"]))
    prov = d.get("_provenance", {})
    return {
        "schema_version": SCHEMA_VERSION,
        "ticker": d["ticker"],
        "company_name": d["company_name"],
        "as_of_date": d["as_of_date"],
        "currency": d.get("currency", "USD"),
        "price": round(central.price, 2),
        "rounding_step": step,
        "base_fv": round_to_step(central.base_fv, step),
        "bear_fv": round_to_step(central.bear_fv, step),
        "bear_terminal": scenario_terminal_label(d, _find_scenario(d, "Bear")[1]),
        "mos_today_pct": round(central.mos_today * 100, 1),
        "rr_today": round(central.rr_today, 2) if math.isfinite(central.rr_today) else None,
        "irr_today_pct": round(central.irr_today * 100, 1) if central.irr_today is not None else None,
        "implied_ufcf_cagr_pct": round(implied * 100, 1) if implied is not None else None,
        "clean_fcf_yield_pct": round(fs.clean_fcf_yield_mcap * 100, 2),
        "tier_today": central.tier_today or "Watchlist",
        "tier_reason": central.reason,
        "tiers": tiers_out,
        "sensitivity": rows,
        "facts_unverified": list(prov.get("carried_over_unverified", [])),
        "facts_partially_verified": list(prov.get("partially_verified", [])),
        "input_file": os.path.relpath(str(d.get("_source_path", "")), _repo_root()) if d.get("_source_path") else "",
        "analysis_path": d.get("analysis_path", ""),
    }


def _repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _range_txt(t: Dict[str, object]) -> str:
    return f"~{_fmt_money(t['central'])} (ช่วง {_fmt_money(t['range_low'])}–{_fmt_money(t['range_high'])})"


def render_summary_block(s: Dict[str, object]) -> str:
    """Generated block for the analysis file. Never hand-edit: run tools/sync_summaries.py --write."""
    L: List[str] = []
    L.append(f"> สร้างอัตโนมัติจาก `{s['input_file']}` ด้วย `valuation_engine.py` v4 — ห้ามแก้ด้วยมือ (รัน `python3 tools/sync_summaries.py --write`)")
    L.append("")
    L.append("| รายการ | ค่า (ณ " + str(s["as_of_date"]) + ") |")
    L.append("| :--- | :--- |")
    L.append(f"| ราคาอ้างอิง | {_fmt_money(s['price'])} |")
    L.append(f"| **สถานะวันนี้ (ตามกฎ v4)** | **{s['tier_today']}** — {s['tier_reason']} |")
    L.append(f"| มูลค่ากรณีฐาน / กรณีหมี | ~{_fmt_money(s['base_fv'])} / ~{_fmt_money(s['bear_fv'])} (กรณีหมีใช้ {s['bear_terminal']}) |")
    L.append(f"| ส่วนเผื่อความปลอดภัยวันนี้ / อัตราได้ต่อเสีย | {s['mos_today_pct']}% / {s['rr_today']} : 1 |")
    L.append(f"| ผลตอบแทน 5 ปี ณ ราคาวันนี้ (ตัวคูณคงที่ — ใช้เป็นด่านขั้นต่ำ ไม่ใช่เพดานราคา) | {s['irr_today_pct']}% |")
    L.append(f"| ตลาดคาด UFCF โตปีละ (reverse DCF) | {s['implied_ufcf_cagr_pct']}% |")
    for t in s["tiers"]:
        r = t["rule"]
        gate = "ผ่าน" if t["irr_gate_ok_today"] else "ไม่ผ่าน"
        L.append(f"| เพดาน {t['tier']} (MOS ≥{r['min_mos']*100:.0f}%, ได้ต่อเสีย ≥{r['min_rr']:.0f}:1; ด่าน IRR ≥{r['min_irr']*100:.0f}% ณ ราคาวันนี้: {gate}) | {_range_txt(t)} — ผูกมัดโดย {t['binder']} |")
    L.append("")
    L.append("ตารางความอ่อนไหว (เลื่อนอัตราโต FCF กรณีฐานทั้ง 10 ปี):")
    L.append("")
    tier_names = [t["tier"] for t in s["tiers"]]
    L.append("| อัตราโตเปลี่ยน | มูลค่าฐาน | IRR 5 ปีวันนี้ | ได้ต่อเสีย | " + " | ".join(f"เพดาน {n}" for n in tier_names) + " | สถานะ |")
    L.append("| :---: | :---: | :---: | :---: | " + " | ".join(":---:" for _ in tier_names) + " | :--- |")
    for r in s["sensitivity"]:
        irr = f"{r['irr_today_pct']}%" if r["irr_today_pct"] is not None else "N/A"
        rr = f"{r['rr_today']}" if r["rr_today"] is not None else "∞"
        L.append(f"| {r['growth_delta_pp']:+.0f} จุด | {_fmt_money(r['base_fv'])} | {irr} | {rr} | "
                 + " | ".join(_fmt_money(r["ceilings"][n]) for n in tier_names) + f" | {r['tier_today']} |")
    if s["facts_unverified"] or s["facts_partially_verified"]:
        L.append("")
        L.append(f"⚠️ ตัวเลขที่ยังไม่ได้เทียบเอกสารยื่นทางการ: {', '.join(s['facts_unverified']) or '-'} | เทียบได้บางส่วน: {', '.join(s['facts_partially_verified']) or '-'}")
    return "\n".join(L)


def render_index_rows(summaries: List[Dict[str, object]]) -> str:
    L = ["| Ticker | บริษัท | ราคา ณ วันที่ | สถานะ v4 | เพดาน Starter | เพดาน Core | ไฟล์ |",
         "| :--- | :--- | :---: | :--- | :---: | :---: | :--- |"]
    for s in summaries:
        t = {x["tier"]: x for x in s["tiers"]}
        st, co = t.get("Starter"), t.get("Core")
        path = str(s["analysis_path"])
        rel = path[len("analyses/"):] if path.startswith("analyses/") else path
        L.append(f"| **{s['ticker']}** | {s['company_name']} | {_fmt_money(s['price'])} ({s['as_of_date']}) | **{s['tier_today']}** | "
                 f"{_range_txt(st) if st else '-'} | {_range_txt(co) if co else '-'} | [{os.path.basename(path)}](./{rel}) |")
    return "\n".join(L)


def render_readme_items(summaries: List[Dict[str, object]]) -> str:
    L = []
    for s in summaries:
        t = {x["tier"]: x for x in s["tiers"]}
        st = t.get("Starter")
        L.append(f"* [{s['ticker']} — {s['company_name']}](./{s['analysis_path']}) *(v4 ณ {s['as_of_date']} ที่ {_fmt_money(s['price'])} — "
                 f"สถานะ: **{s['tier_today']}**; เพดาน Starter {_range_txt(st) if st else '-'}; ผลตอบแทน 5 ปี {s['irr_today_pct']}%)*")
    return "\n".join(L)


# ==============================================================================
# 3. REPORT GENERATOR
# ==============================================================================
def run_valuation_report(d: Dict[str, object]) -> None:
    fs = compute_forensic_metrics(d)
    price = float(d["share_price"])
    wacc = float(d["wacc"])
    g_term = float(d["terminal_growth"])
    rf = float(d.get("risk_free_yield", d.get("us_10y_yield", 0.0)))
    roiic = float(d.get("assumed_incremental_roic", 0.0))

    print("=" * 100)
    print(f"INSTITUTIONAL VALUATION ENGINE v4 | {d['ticker']} — {d['company_name']} ({d.get('currency', 'USD')})")
    print(f"As of: {d['as_of_date']} | Price: ${price:,.2f} | Matched 10Y Rf: {rf*100:.2f}% | WACC: {wacc*100:.2f}%")
    print("=" * 100)

    print("\n[1] FORENSIC BALANCE SHEET, CASH FLOW & RECONCILIATION BRIDGE ($M)")
    print(f"  Market Cap                     : ${fs.market_cap:>10,.1f}M")
    print(f"  Free Cash (ex-Customer Float)  : ${fs.free_cash_ex_float:>10,.1f}M")
    print(f"  Float-Adjusted Net Debt        : ${fs.float_adjusted_net_debt:>10,.1f}M")
    print(f"  Float-Adjusted Enterprise Val  : ${fs.float_adjusted_ev:>10,.1f}M")
    print("-" * 72)
    print(f"  Cash-Flow Path: OCF (${float(d['ttm_ocf']):,.1f}M) - CapEx (${float(d['ttm_capex']):,.1f}M) = Reported FCF ${fs.reported_fcf:,.1f}M")
    print(f"                  - SBC (${float(d['ttm_sbc']):,.1f}M) = True FCF ${fs.true_fcf_ex_sbc:,.1f}M")
    print(f"                  - Float/WC Windfall (${float(d['ttm_float_inflow']):,.1f}M) = Clean Economic FCF ${fs.clean_economic_fcf:,.1f}M  (P/Clean FCF = {fs.current_p_clean_fcf:.1f}x)")
    print(f"  Direct P&L Path: NOPAT + D&A - CapEx - Normal ΔNWC (${fs.normal_nwc_investment:,.1f}M) = UFCF ${fs.unlevered_fcf_pl:,.1f}M  (EV/UFCF = {fs.current_ev_ufcf:.1f}x)")
    print(f"  Reconciliation : P&L-Implied Levered FCF = ${fs.pl_implied_levered_fcf:,.1f}M vs Clean FCF = ${fs.clean_economic_fcf:,.1f}M "
          f"(Gap: ${fs.reconciliation_gap:+,.1f}M / {fs.reconciliation_gap_pct*100:+.1f}%)")
    if abs(fs.reconciliation_gap_pct) > 0.05:
        print("  [!] RECONCILIATION WARNING: Gap > 5% — verify cash vs book taxes, leases, or double-counted ΔNWC/float!")
    print(f"  Clean FCF Yield (on MCap)      : {fs.clean_fcf_yield_mcap*100:>9.2f}%  (Spread vs Rf: {fs.spread_vs_rf*100:+.2f}%)")

    print("\n[2] REVERSE DCF (MARKET-IMPLIED EXPECTATIONS) — variable, margin path & fines stated explicitly")
    print(f"  WACC = {wacc*100:.2f}%, Terminal g = {g_term*100:.2f}% (Implied Exit EV/UFCF = {1/(wacc-g_term):.1f}x)")
    ufcf_cagr = solve_reverse_dcf_ufcf_cagr(fs.float_adjusted_ev, fs.unlevered_fcf_pl, wacc, g_term)
    ufcf_str = f"{ufcf_cagr*100:+.2f}% / yr" if ufcf_cagr is not None else "UNBRACKETED"
    print(f"  (a) Implied 10Y UFCF CAGR    | no margin change, no fines          : {ufcf_str}")
    for case in d["reverse_dcf_cases"]:
        rc = solve_reverse_dcf_revenue_cagr(fs.float_adjusted_ev, d, fs, case)
        rc_str = f"{rc*100:+.2f}% / yr" if rc is not None else "UNBRACKETED"
        print(f"  (b) Implied 10Y Revenue CAGR | {case['label']:<36}: {rc_str}")

    print("\n[3] EXPLICIT 10-YEAR DCF (4 SCENARIOS, PER-SCENARIO TERMINAL VALUE + REINVESTMENT SANITY CHECK)")
    print(f"  {'Scenario':<32} | {'1-5Y g':>6} | {'6-10Y g':>7} | {'Terminal':>10} | {'Drag':>6} | {'Reinv*':>6} | {'Fair Val':>8} | {'Upside':>7}")
    print("  " + "-" * 101)
    for name, cfg in d["dcf_scenarios"].items():
        g15 = float(cfg["ufcf_cagr_1_5"])
        fv = scenario_fair_value(d, fs, cfg)
        reinv_str = f"{max(0.0, g15)/roiic*100:>5.0f}%" if roiic > 0 else "  N/A "
        print(f"  {name:<32} | {g15*100:>5.1f}% | {cfg['ufcf_cagr_6_10']*100:>6.1f}% | {scenario_terminal_label(d, cfg):>10} | "
              f"{cfg['pv_cash_drag']:>6,.0f} | {reinv_str:>6} | ${fv:>7,.2f} | {(fv/price-1)*100:>+6.1f}%")
    if roiic > 0:
        print(f"  *Implied Reinvestment Rate = max(0, 1-5Y g) / Assumed Incremental ROIC ({roiic*100:.0f}%).")

    print("\n[4] SELF-CONSISTENT 5-YEAR FORWARD IRR (Dated Dividends + Explicit Cash Ledger)")
    base_g = float(d["irr_model"]["base_clean_fcf_growth"])
    policy = str(d["irr_model"].get("dividend_funding_policy", "strict_fail"))
    print(f"  Base Clean FCF g = {base_g*100:.1f}%/yr | Buyback Alloc = {d['irr_model']['fcf_allocation_to_buybacks']*100:.0f}% | Funding Policy = '{policy}'")
    print(f"  {'Exit Multiple Scenario':<34} | {'Exit P/FCF':>10} | {'Yr5 Price':>9} | {'Net BB/yr':>9} | {'5Y IRR':>8} | {'Status'}")
    print("  " + "-" * 96)
    const_res: Optional[IRRSimulationResult] = None
    for label, ratio in d["irr_model"]["exit_multiple_scenarios"].items():
        res = simulate_5y_forward_irr(d, fs, base_g, float(ratio))
        if abs(float(ratio) - 1.0) < 1e-9:
            const_res = res
        p_str = f"${res.end_price:>8,.2f}" if res.end_price is not None else "      N/A"
        irr_str = f"{res.irr*100:>+7.2f}%" if res.irr is not None else "     N/A"
        print(f"  {label:<34} | {fs.current_p_clean_fcf*ratio:>9.1f}x | {p_str} | {res.avg_net_buyback_rate*100:>8.2f}% | {irr_str} | {res.status}")

    if const_res is not None and const_res.ledger:
        print("\n  [4b] 5-Year Cash Ledger (Constant-Multiple Case, $M)")
        print(f"  {'Yr':>2} | {'Beg Cash':>9} | {'Clean FCF':>9} | {'Drag':>6} | {'Plan Div':>8} | {'Paid Div':>8} | {'Buyback':>8} | {'End Cash':>9} | {'Shortfall':>9}")
        print("  " + "-" * 88)
        for row in const_res.ledger:
            print(f"  {row.year:>2} | {row.beg_cash:>9,.1f} | {row.clean_fcf:>9,.1f} | {row.cash_drag:>6,.1f} | "
                  f"{row.planned_div:>8,.1f} | {row.actual_div:>8,.1f} | {row.buyback:>8,.1f} | {row.end_cash:>9,.1f} | {row.shortfall:>9,.1f}")

    print("\n[5] REQUIRED GROWTH TABLE (Growth needed at today's price for target 5Y IRR)")
    op_lev = float(d["operating_leverage_factor"])
    print(f"  (Operating Leverage Assumption: FCF Growth = {op_lev:.2f}x Revenue Growth)")
    print(f"  {'Exit Multiple Case':<32} | {'10% IRR (FCF / Rev)':>19} | {'12% IRR (FCF / Rev)':>19} | {'15% IRR (FCF / Rev)':>19}")
    print("  " + "-" * 97)
    for label, ratio in d["irr_model"]["exit_multiple_scenarios"].items():
        cols = []
        for tgt in (0.10, 0.12, 0.15):
            g_req = solve_required_fcf_growth(d, fs, tgt, float(ratio))
            cols.append(f"{g_req*100:>5.1f}% / {g_req/op_lev*100:>5.1f}%" if g_req is not None else "    N/A /   N/A")
        print(f"  {label:<32} | {cols[0]:>19} | {cols[1]:>19} | {cols[2]:>19}")

    print("\n[6] v4 SINGLE-STOCK ENTRY CEILINGS — Ceiling = min(Lens A: MOS vs Base DCF, Lens C: Risk/Reward vs Bear)")
    print("    + HURDLE GATE: Constant-Multiple 5Y IRR at TODAY's price must be >= tier minimum (not a price ceiling)")
    summ = build_summary(d)
    ea = assess_entry(d, fs)
    print(f"  Base FV ${ea.base_fv:,.2f} | Bear FV ${ea.bear_fv:,.2f} ({summ['bear_terminal']}) | Today ${price:,.2f}: "
          f"MOS {ea.mos_today*100:.1f}% | R/R {ea.rr_today:.2f}:1 | Const-Mult 5Y IRR "
          + (f"{ea.irr_today*100:.2f}%" if ea.irr_today is not None else f"N/A ({ea.irr_status})"))
    print(f"  {'Tier':<10} | {'MOS/RR/IRR rule':<16} | {'Lens A':>9} | {'Lens C':>9} | {'Binds':>5} | {'IRR gate':>8} | {'Rounded ceiling (Base g ±1pp)':<34}")
    print("  " + "-" * 104)
    for t, ts in zip(ea.tiers, summ["tiers"]):
        rule_txt = f"{t.min_mos*100:.0f}%/{t.min_rr:.0f}:1/{t.min_irr*100:.0f}%"
        print(f"  {t.tier:<10} | {rule_txt:<16} | ${t.lens_a_mos:>8,.2f} | ${t.lens_c_rr:>8,.2f} | {t.binder:>5} | "
              f"{('PASS' if t.irr_gate_ok else 'FAIL'):>8} | ~${ts['central']:,.0f} (range ${ts['range_low']:,.0f}-${ts['range_high']:,.0f})")
    print(f"  -> Single-Stock Tier Today: {summ['tier_today']} ({summ['tier_reason']})")
    print("\n  [6b] SENSITIVITY — Base-case UFCF growth (Y1-10) and IRR-model FCF growth shifted together")
    names = [t.tier for t in ea.tiers]
    print(f"  {'Δg':>6} | {'Base FV':>8} | {'5Y IRR':>7} | {'R/R':>5} | " + " | ".join(f"{n:>9}" for n in names) + " | Tier today")
    print("  " + "-" * (46 + 12 * len(names)))
    for r in summ["sensitivity"]:
        irr_s = f"{r['irr_today_pct']:>6.1f}%" if r["irr_today_pct"] is not None else "    N/A"
        rr_s = f"{r['rr_today']:>5.2f}" if r["rr_today"] is not None else "  inf"
        print(f"  {r['growth_delta_pp']:>+5.0f}pp | ${r['base_fv']:>7,.0f} | {irr_s} | {rr_s} | "
              + " | ".join(f"${r['ceilings'][n]:>8,.0f}" for n in names) + f" | {r['tier_today']}")
    if summ["facts_unverified"] or summ["facts_partially_verified"]:
        print(f"  [PROVENANCE] Unverified facts: {', '.join(summ['facts_unverified']) or '-'}")
        print(f"               Partially verified: {', '.join(summ['facts_partially_verified']) or '-'}")
    print("  [PORTFOLIO GATE] Single-stock ceilings DO NOT assign portfolio %. Before sizing, verify Module 05 SSOT:")
    print("                   (1) Cash % & Best Alternative IRR, (2) Correlated Basket Cap, (3) Joint Drawdown Stress, (4) ADV Liquidity.")
    print("=" * 100)


# ==============================================================================
# 4. BUILT-IN ADVERSARIAL SELF-TESTS (Codex Audit Round 2 Acceptance Suite)
# ==============================================================================
def run_self_tests() -> None:
    print("Running v3 adversarial acceptance tests...")

    # Test 1A: Unfunded dividend under strict_fail MUST fail and report $250M shortfall (no phantom 15% IRR)
    d1 = deepcopy(COMPANY_DATA)
    d1.update(
        share_price=10.0, diluted_shares_m=100.0, total_debt=0.0,
        total_cash_and_st_inv=0.0, customer_float_liability=0.0,
        ttm_ocf=100.0, ttm_capex=0.0, ttm_sbc=0.0, ttm_float_inflow=0.0,
        annual_dividend_per_share=1.50,
    )
    d1["irr_model"].update(
        base_clean_fcf_growth=0.0, dividend_growth_rate=0.0,
        annual_cash_drag_m=0.0, fcf_allocation_to_buybacks=0.0,
        dividend_funding_policy="strict_fail",
    )
    fs1 = compute_forensic_metrics(d1)
    r1 = simulate_5y_forward_irr(d1, fs1, 0.0, 1.0)
    assert not r1.feasible and r1.status == "INFEASIBLE_UNFUNDED_DIVIDEND", r1
    assert r1.irr is None and abs(r1.total_shortfall - 250.0) < 1e-6 and r1.first_shortfall_year == 1, r1

    # Test 1B: Same company under cap_to_available_cash -> pays $100M/yr -> true IRR = 10.00%
    d1b = deepcopy(d1)
    d1b["irr_model"]["dividend_funding_policy"] = "cap_to_available_cash"
    r1b = simulate_5y_forward_irr(d1b, fs1, 0.0, 1.0)
    assert r1b.feasible and r1b.status == "OK_DIVIDEND_CUT" and abs(r1b.irr - 0.10) < 1e-6, r1b

    # Test 1C: Same company with $300M beginning free cash -> fully funded! Ending cash = $50M, IRR = 15.00%
    d1c = deepcopy(d1)
    d1c["total_cash_and_st_inv"] = 300.0
    fs1c = compute_forensic_metrics(d1c)
    r1c = simulate_5y_forward_irr(d1c, fs1c, 0.0, 1.0)
    assert r1c.feasible and r1c.status == "OK" and abs(r1c.ending_free_cash - 50.0) < 1e-6 and abs(r1c.irr - 0.15) < 1e-6, r1c

    # Test 2: Working capital distinction (100 before ΔNWC -> 80 with ΔNWC=20 vs 100 with ΔNWC=0) + 0 reconciliation gap
    d2a = deepcopy(COMPANY_DATA)
    d2a.update(ttm_core_gaap_ebit=125.0, effective_tax_rate=0.20, ttm_depreciation_amort=10.0, ttm_capex=10.0,
               ttm_normal_working_capital_investment=20.0, ttm_ocf=90.0, ttm_sbc=0.0, ttm_float_inflow=0.0, ttm_net_interest_expense=0.0)
    d2b = deepcopy(d2a)
    d2b.update(ttm_normal_working_capital_investment=0.0, ttm_ocf=110.0)
    fs2a, fs2b = compute_forensic_metrics(d2a), compute_forensic_metrics(d2b)
    assert abs(fs2a.unlevered_fcf_pl - 80.0) < 1e-9 and abs(fs2b.unlevered_fcf_pl - 100.0) < 1e-9, (fs2a.unlevered_fcf_pl, fs2b.unlevered_fcf_pl)
    assert abs(fs2a.reconciliation_gap) < 1e-9 and abs(fs2b.reconciliation_gap) < 1e-9, (fs2a.reconciliation_gap, fs2b.reconciliation_gap)

    # Test 3A: Impossible target IRR (6.2% growth, 0 div, 0 buyback -> target 11% MUST be IMPOSSIBLE, never $1.00)
    d3 = deepcopy(d1)
    d3["annual_dividend_per_share"] = 0.0
    d3["irr_model"]["base_clean_fcf_growth"] = 0.062
    fs3 = compute_forensic_metrics(d3)
    sol3 = solve_price_for_constant_multiple_irr(d3, fs3, 0.11)
    assert sol3.status == "IMPOSSIBLE" and sol3.price is None, sol3

    # Test 3B: Always-passing target IRR (15% growth, 0 div, 0 buyback -> target 11% MUST be UNBOUNDED_PASS)
    d3b = deepcopy(d3)
    d3b["irr_model"]["base_clean_fcf_growth"] = 0.15
    sol3b = solve_price_for_constant_multiple_irr(d3b, fs3, 0.11)
    assert sol3b.status == "UNBOUNDED_PASS" and sol3b.price is None, sol3b

    # Test 4: BKNG baseline & Lens B SOLVED sanity check
    fs_bkng = compute_forensic_metrics(COMPANY_DATA)
    r_bkng = simulate_5y_forward_irr(COMPANY_DATA, fs_bkng, 0.062, 1.0)
    assert r_bkng.feasible and r_bkng.status == "OK" and abs(r_bkng.irr - 0.1330) < 0.0005, r_bkng
    for tgt in (0.11, 0.13, 0.15):
        sol_bkng = solve_price_for_constant_multiple_irr(COMPANY_DATA, fs_bkng, tgt)
        assert sol_bkng.status == "SOLVED" and sol_bkng.price is not None and abs(sol_bkng.verified_irr - tgt) < 1e-4, sol_bkng

    # Test 5: External debt-funded dividend policy deducts debt from Year-5 equity (cannot manufacture 15% IRR)
    d5 = deepcopy(d1)
    d5["irr_model"]["dividend_funding_policy"] = "external_debt_funded"
    r5 = simulate_5y_forward_irr(d5, fs1, 0.0, 1.0)
    assert r5.feasible and r5.status == "OK_DEBT_FUNDED" and r5.total_debt_added > 250.0 and r5.irr < 0.12, r5

    print("ALL 9 ADVERSARIAL ACCEPTANCE TESTS PASSED.")

    run_v4_self_tests()


def run_v4_self_tests() -> None:
    print("Running v4 acceptance tests (JSON provenance, per-scenario terminal, 2-lens ceilings, IRR gate, sensitivity)...")
    n = 0

    # V4-1: Every committed inputs/*.json validates, and BKNG loads into the legacy engine dict.
    inputs_dir = os.path.join(_repo_root(), "inputs")
    files = sorted(f for f in os.listdir(inputs_dir) if f.endswith(".json")) if os.path.isdir(inputs_dir) else []
    assert "BKNG.json" in files, f"inputs/BKNG.json missing (found {files})"
    for fname in files:
        with open(os.path.join(inputs_dir, fname), encoding="utf-8") as fh:
            errs = validate_company_json(json.load(fh))
        assert not errs, (fname, errs)
    bk_path = os.path.join(inputs_dir, "BKNG.json")
    d_bk = load_company_json(bk_path)
    assert d_bk["ticker"] == "BKNG" and all(isinstance(d_bk[k], float) for k in FACT_FIELDS)
    n += 1

    # V4-2: Provenance contract — a fact without source, or an assumption without rationale, is rejected.
    with open(bk_path, encoding="utf-8") as fh:
        raw = json.load(fh)
    bad = deepcopy(raw)
    bad["facts"]["ttm_ocf"]["source_url"] = ""
    bad["facts"]["ttm_ocf"]["filing_ref"] = ""
    assert any(e.startswith("facts.ttm_ocf") for e in validate_company_json(bad))
    bad2 = deepcopy(raw)
    bad2["assumptions"]["wacc"]["rationale"] = " "
    assert any(e.startswith("assumptions.wacc") for e in validate_company_json(bad2))
    bad3 = deepcopy(raw)
    bad3["facts"]["share_price"]["verification"] = "trust_me"
    assert any(e.startswith("facts.share_price") for e in validate_company_json(bad3))
    try:
        company_dict_from_json(bad)
        raise AssertionError("invalid file must raise")
    except ValueError:
        pass
    n += 1

    # V4-3: Per-scenario terminal value — 0% terminal growth < 2.5%; exit multiple matches hand calculation;
    #       legacy call signature (no exit multiple) is unchanged.
    ev_25 = dcf_enterprise_value(100.0, 0.0, 0.0, 0.10, 0.025)
    ev_00 = dcf_enterprise_value(100.0, 0.0, 0.0, 0.10, 0.0)
    manual = sum(100.0 / 1.1 ** t for t in range(1, 11)) + 800.0 / 1.1 ** 10
    assert ev_00 < ev_25
    assert abs(dcf_enterprise_value(100.0, 0.0, 0.0, 0.10, 0.025, exit_multiple=8.0) - manual) < 1e-6
    assert abs(ev_25 - (sum(100.0 / 1.1 ** t for t in range(1, 11)) + 100.0 * 1.025 / 0.075 / 1.1 ** 10)) < 1e-6
    fs_fx = compute_forensic_metrics(COMPANY_DATA)
    d_t = deepcopy(COMPANY_DATA)
    bear_name, _ = _find_scenario(d_t, "Bear")
    fv_global = scenario_fair_value(d_t, fs_fx, d_t["dcf_scenarios"][bear_name])
    d_t["dcf_scenarios"][bear_name]["terminal_growth"] = 0.0
    fv_zero = scenario_fair_value(d_t, fs_fx, d_t["dcf_scenarios"][bear_name])
    assert abs(fv_global - 108.89) < 0.01 and fv_zero < fv_global - 10.0, (fv_global, fv_zero)
    n += 1

    # V4-4: Ceilings = min(Lens A, Lens C) only, and do NOT move when the IRR-model growth changes (Lens B removed).
    a0 = assess_entry(COMPANY_DATA, fs_fx)
    for t in a0.tiers:
        p_a = a0.base_fv * (1.0 - t.min_mos)
        p_c = (a0.base_fv + t.min_rr * a0.bear_fv) / (1.0 + t.min_rr)
        assert abs(t.ceiling - min(p_a, p_c)) < 1e-9
    d_g = deepcopy(COMPANY_DATA)
    d_g["irr_model"]["base_clean_fcf_growth"] = 0.02
    a_g = assess_entry(d_g, fs_fx)
    assert all(abs(x.ceiling - y.ceiling) < 1e-9 for x, y in zip(a0.tiers, a_g.tiers))
    # Regression vs v3 fixture: Starter/Core unchanged (R/R-bound); Fat Pitch now MOS-bound $124.90 (was Lens B $119.13)
    assert abs(a0.tiers[0].ceiling - 136.64) < 0.01 and abs(a0.tiers[1].ceiling - 129.70) < 0.01
    assert abs(a0.tiers[2].ceiling - 124.90) < 0.01 and a0.tiers[2].binder == "MOS"
    assert a0.tier_today is None and not a0.tiers[0].price_ok  # $146 > Starter ceiling -> Watchlist
    n += 1

    # V4-5: IRR hurdle gate — a cheap price passes every ceiling, but a shrinking business fails the 11% gate.
    d_c = deepcopy(COMPANY_DATA)
    d_c["share_price"] = 100.0
    a_c = assess_entry(d_c, compute_forensic_metrics(d_c))
    assert all(t.price_ok for t in a_c.tiers) and a_c.tier_today == "Fat Pitch", a_c
    d_s = deepcopy(d_c)
    d_s["irr_model"]["base_clean_fcf_growth"] = -0.10
    a_s = assess_entry(d_s, compute_forensic_metrics(d_s))
    assert a_s.irr_today is not None and a_s.irr_today < 0.11
    assert all(t.price_ok and not t.irr_gate_ok for t in a_s.tiers) and a_s.tier_today is None, a_s
    n += 1

    # V4-6: Sensitivity is monotonic in growth and published ranges bracket the central ceiling.
    s_bk = build_summary(d_bk)
    rows = sorted(s_bk["sensitivity"], key=lambda r: r["growth_delta_pp"])
    for tier in [t["tier"] for t in s_bk["tiers"]]:
        vals = [r["ceilings"][tier] for r in rows]
        assert all(a <= b for a, b in zip(vals, vals[1:])), (tier, vals)
    for t in s_bk["tiers"]:
        assert t["range_low"] <= t["central"] <= t["range_high"], t
        assert abs(t["central"] / s_bk["rounding_step"] - round(t["central"] / s_bk["rounding_step"])) < 1e-9
    assert price_step(146.0) == 5.0 and round_to_step(136.64, 5.0) == 135.0 and price_step(42.0) == 1.0
    n += 1

    # V4-7: Generated markdown is deterministic (required for the CI drift check).
    assert render_summary_block(build_summary(d_bk)) == render_summary_block(build_summary(load_company_json(bk_path)))
    n += 1

    print(f"ALL {n} V4 ACCEPTANCE TESTS PASSED.")


def _arg_value(argv: List[str], flag: str) -> Optional[str]:
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv):
            return argv[i + 1]
        raise SystemExit(f"{flag} needs a value")
    return None


def main(argv: List[str]) -> int:
    if "--self-test" in argv:
        run_self_tests()
        return 0
    path = _arg_value(argv, "--input")
    d = load_company_json(path) if path else COMPANY_DATA
    if "--summary-json" in argv:
        print(json.dumps(build_summary(d), ensure_ascii=False, indent=2))
        return 0
    if "--summary-md" in argv:
        print(render_summary_block(build_summary(d)))
        return 0
    if not path:
        print("[LEGACY v3 FIXTURE] Regression example only — run with `--input inputs/BKNG.json` for the audited v4 view.")
    run_valuation_report(d)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
