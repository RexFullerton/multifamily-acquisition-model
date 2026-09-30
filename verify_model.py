#!/usr/bin/env python3
"""
verify_model.py -- independent recomputation of the Parkview Crossing model.

What it reads: ONLY literal input cells -- the blue inputs on the Assumptions
tab and on the Unit Mix tab (unit counts and rents live there per the model
spec). Every input is located by its row label, never by a row number, and
the script hard-fails if any cell it reads contains a formula. It never reads
a computed cell of the model to build its own numbers.

What it computes (its own engine, sharing no code with build_model.py):
10-year operating statement line by line (market GPR, loss-to-lease,
scheduled rent, vacancy, credit loss, concessions, other income, EGI, every
opex line, NOI, reserves, one-time capex, unlevered CF), the Day-0 NOI bridge
and cap rates, the tax-adjusted exit, Scenario B (new debt) sizing and
schedule, Scenario A (assumed first + supplemental loans, maturity refinance),
sources & uses for both, levered cash flows for both, the Scenario A
waterfall tier by tier, and IRR / equity multiple for everything.

What it then does: opens the recalculated workbook's cached values and
compares every line it computed, year by year, reporting any difference over
$1 (dollar lines) or 1 bp (rates, IRRs, multiples).

Usage:  python3 verify_model.py [recalculated.xlsx]
Exit code 0 = everything ties; 1 = at least one difference over tolerance.

The engine (load_inputs / run_model) is importable -- price_solve.py uses it.
"""
import sys
import openpyxl
import numpy_financial as npf

TOL_USD = 1.0
TOL_RATE = 0.0001  # 1 bp; also used for multiples (x)
NYEARS = 10        # operating model horizon
HOLD = 5           # structural hold (see Assumptions note)
UNIT_TYPES = ("Studio", "1BR/1BA", "2BR/1BA", "2BR/2BA")


# ---------------------------------------------------------------------------
# Input loading -- literal cells only
# ---------------------------------------------------------------------------
class InputIsFormula(Exception):
    pass


def _find_row(ws, label, col=1, exact=False, start=1, max_row=300):
    for r in range(start, max_row):
        v = ws.cell(row=r, column=col).value
        if isinstance(v, str) and (v.strip() == label if exact else label in v):
            return r
    raise KeyError(f"{ws.title}: no row label {'==' if exact else 'containing'} {label!r}")


def _literal(ws, r, c):
    v = ws.cell(row=r, column=c).value
    if isinstance(v, str) and v.startswith("="):
        raise InputIsFormula(f"{ws.title}!{ws.cell(row=r, column=c).coordinate} is a formula ({v}); "
                             f"verify_model.py only reads literal inputs")
    if not isinstance(v, (int, float)):
        raise ValueError(f"{ws.title}!{ws.cell(row=r, column=c).coordinate} is not numeric: {v!r}")
    return float(v)


def load_inputs(path):
    wb = openpyxl.load_workbook(path, data_only=False)  # formulas visible -> can assert literals
    a = wb["Assumptions"]

    def inp(label, exact=False):
        return _literal(a, _find_row(a, label, exact=exact), 3)

    I = {}
    I["price"] = inp("Purchase Price ($)")
    I["broker_cap"] = inp("Broker-Stated Cap Rate")
    I["closing_pct"] = inp("Closing Costs (% of Price)")
    I["millage"] = inp("Combined Millage Rate")
    I["seller_taxable"] = inp("Seller's Current TAXABLE Value")
    I["cos_factor"] = inp("Cost-of-Sale Factor")
    I["nonhs_cap"] = inp("Non-Homestead Assessment Cap")  # reference only (used by the change bridge's legacy case)
    I["reno_lines"] = [inp(x) for x in ("Kitchen (cabinet refacing", "Mini-split ductless AC",
                                        "Vinyl slider window", "Modern lighting fixtures", "LVP flooring",
                                        "Bathroom refresh", "Interior paint", "Turnover labor")]
    I["reno_contg_pct"] = inp("Contingency %", exact=True)
    I["reno_premium_mo"] = inp("Renovated-Unit Rent Premium over Market ($/month)")
    I["reno_y1_capture"] = inp("Year-1 Premium Capture %")
    I["vacancy"] = inp("Physical Vacancy %")
    I["credit_loss"] = inp("Credit Loss % (of GPR)")
    I["concessions"] = inp("Concessions % (of GPR)")
    I["other_income_mo"] = inp("Other Income ex-Utility Recovery")
    I["rubs_pct"] = inp("Utility Reimbursement (RUBS) Recovery %")
    I["burnoff_pct"] = inp("Loss-to-Lease Burn-off % per Turnover")
    I["turnover_rate"] = inp("Annual Turnover Rate %")
    I["reno_headstart"] = inp("Prior-Owner-Renovated Units: Starting Capture")
    I["growth"] = [inp(f"Year {i} Market Rent Growth") for i in range(1, NYEARS + 1)]
    I["exp_growth"] = inp("General Expense Growth %")
    I["ins_growth"] = inp("Insurance Growth %")
    I["payroll"] = inp("Payroll (on-site")
    I["repairs"] = inp("Repairs & Maintenance", exact=True)
    I["turnover_cost"] = inp("Turnover / Make-Ready", exact=True)
    I["contract_svc"] = inp("Contract Services (landscaping")
    I["utilities"] = inp("Utilities — Common-Area Electric")
    I["w_unit"] = inp("Water Service Charge per Unit")
    I["w_kgal"] = inp("Water Commodity Charge")
    I["s_unit"] = inp("Sewer Service Charge per Unit")
    I["s_kgal"] = inp("Sewer Flow Charge")
    I["kgal"] = inp("Water Use per Unit")
    I["meters"] = inp("Number of Water Meters")
    I["meter_chg"] = inp("Monthly Service Charge per 2-inch Meter")
    I["ws_growth"] = inp("Water & Sewer Cost Growth %")
    I["trash_n"] = inp("Trash Containers")
    I["trash_rate"] = inp("City Rate per 6-yd Container")
    I["ins_base"] = inp("Insurance — Base Case")
    I["ins_roof"] = inp("Insurance — If Roof Replaced")
    I["mgmt_fee_pct"] = inp("Management Fee (% of EGI)")
    I["nav"] = inp("Non-Ad Valorem Assessments ($/unit")
    I["ga"] = inp("G&A / Admin", exact=True)
    I["marketing"] = inp("Marketing", exact=True)
    I["reserves"] = inp("Replacement Reserves (below NOI)")
    I["roof_toggle"] = inp("Roof Replacement Scenario Toggle")
    I["roof_cost"] = inp("Roof Replacement Cost")
    I["recert_year"] = inp("Recertification Year")
    I["recert_inspect"] = inp("Recertification Inspection Cost")
    I["recert_remed"] = inp("Recertification Remediation Contingency")
    I["ust10"] = inp("10-Year Treasury Yield")
    I["agency_spread"] = inp("Agency Spread over 10-Year Treasury")
    I["ltv"] = inp("Maximum LTV %")
    I["min_dscr"] = inp("Minimum DSCR")
    I["io_years"] = inp("Interest-Only Period (years)")
    I["amort_years"] = inp("Amortization (years)")
    I["prepay"] = [inp(f"Prepayment Premium, Loan Year {i}", exact=True) for i in range(1, 11)]
    I["ust5"] = inp("5-Year Treasury Yield")
    I["prepay5"] = [inp(f"5-Year Fixed Prepayment Premium, Loan Year {i}", exact=True) for i in range(1, 6)]
    I["sofr30"] = inp("30-Day Average SOFR")
    I["b_term"] = inp("Scenario B Loan Term")
    I["float_spread"] = inp("Floating Spread over 30-Day Average SOFR")
    I["cap_strike"] = inp("Rate Cap Strike")
    I["cap_cost_pct"] = inp("2-Year Rate Cap Premium")
    I["float_io"] = inp("Floating Refi Interest-Only")
    I["float_prepay"] = inp("Floating Refi Prepayment Premium at Sale")
    I["a_plan"] = inp("Scenario A Exit Plan")
    I["a_first_bal"] = inp("First Mortgage Balance")
    I["a_first_rate"] = inp("First Mortgage Rate")
    I["a_mat"] = int(inp("First Mortgage Maturity"))
    I["a_supp_bal"] = inp("Supplemental Loan Balance")
    I["a_supp_rate"] = inp("Supplemental Loan Rate")
    I["a_io"] = inp("Both Loans Interest-Only")
    I["a_fee_pct"] = inp("Loan Assumption Fee")
    I["a_max_ltv"] = inp("Assumption Approval: Max LTV")
    I["exit_anchor"] = inp("Exit Cap — Market Anchor")
    I["exit_vintage"] = inp("Exit Cap — Spread for Class C")
    I["cos_exit"] = inp("Cost of Sale at Exit")
    I["sens_exit_step"] = inp("Sensitivity Step — Exit Cap")
    I["sens_price_step"] = inp("Sensitivity Step — Purchase Price")
    I["sens_growth_step"] = inp("Sensitivity Step — Market Rent Growth")
    I["sens_cost_step"] = inp("Sensitivity Step — Renovation Cost")
    I["sens_prem_step"] = inp("Sensitivity Step — Renovation Premium")
    I["pref"] = inp("Preferred Return %")
    I["t2_inv"] = inp("Tier 2 Investor Share")
    I["t2_promote"] = inp("Tier 2 GP Promote")
    I["t2_hurdle"] = inp("Tier 2 IRR Hurdle")
    I["t3_inv"] = inp("Tier 3 Investor Share")
    I["t3_promote"] = inp("Tier 3 GP Promote")
    I["gp_coinvest"] = inp("GP Co-Invest %")

    um = wb["Unit Mix"]
    types, r = [], 1
    while len(types) < len(UNIT_TYPES):  # stop before the Renovation Capex table, which reuses the names
        name = um.cell(row=r, column=1).value
        if name in UNIT_TYPES:
            types.append(dict(name=name, total=_literal(um, r, 2), classic=_literal(um, r, 3),
                              F=_literal(um, r, 6), H=_literal(um, r, 8)))
        r += 1
        if r > 50:
            raise KeyError("Unit Mix: did not find all 4 unit types")
    for t in types:  # recomputed here, NOT read from the model's column G / D
        t["renov"] = t["total"] - t["classic"]
        t["G"] = t["F"] + I["reno_headstart"] * (t["H"] - t["F"])
    I["types"] = types
    I["units"] = sum(t["total"] for t in types)
    I["classic_units"] = sum(t["classic"] for t in types)
    return I


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------
def _pmt(rate, n, pv):
    return pv * rate / (1 - (1 + rate) ** -n)


def _irr(cfs):
    try:
        v = npf.irr(cfs)
        return float(v)
    except Exception:
        return float("nan")


def waterfall(lev_cf, equity, I):
    """Pari passu waterfall, computed INDEPENDENTLY of the workbook's method.

    The workbook rolls two compounding hurdle balances forward year by year.
    Here each year's tier amounts are solved in closed form from the future
    value of the entire investor cash-flow history at each hurdle rate:
        shortfall_r(t) = max(0, E(1+r)^t - sum_{s<t} D_s (1+r)^(t-s))
    where D_s is everything investors (LP + GP co-invest) received in year s.
    Tier 1 = min(cash, pref shortfall); Tier 2 fills the Tier-2 shortfall at the
    investor share; Tier 3 takes the rest. Investor cash splits LP/GP pro rata
    to capital; the promote goes to GP. No state is carried except the history.
    Balance rows (for comparison only) are the same closed-form FVs restricted to
    the flows the workbook debits (Tier 1 for the pref balance; Tier 1 + investor
    Tier 2 for the Tier-2 balance)."""
    E, cash = equity, lev_cf[1:]
    p, h = I["pref"], I["t2_hurdle"]
    co = I["gp_coinvest"]
    D, T1, T2, T3, INV2, INV3, PR2, PR3 = [], [], [], [], [], [], [], []
    for t, av in enumerate(cash, start=1):
        fv_p = E * (1 + p) ** t - sum(D[s - 1] * (1 + p) ** (t - s) for s in range(1, t))
        t1 = min(av, max(0.0, fv_p))
        fv_h = E * (1 + h) ** t - sum(D[s - 1] * (1 + h) ** (t - s) for s in range(1, t)) - t1
        t2 = min(av - t1, max(0.0, fv_h) / I["t2_inv"])
        t3 = av - t1 - t2
        inv2, inv3 = t2 * I["t2_inv"], t3 * I["t3_inv"]
        T1.append(t1); T2.append(t2); T3.append(t3); INV2.append(inv2); INV3.append(inv3)
        PR2.append(t2 * I["t2_promote"]); PR3.append(t3 * I["t3_promote"])
        D.append(t1 + inv2 + inv3)
    n = len(cash)
    pref_bal = [E] + [E * (1 + p) ** t - sum(T1[s - 1] * (1 + p) ** (t - s) for s in range(1, t + 1)) for t in range(1, n + 1)]
    h_bal = [E] + [E * (1 + h) ** t - sum((T1[s - 1] + INV2[s - 1]) * (1 + h) ** (t - s) for s in range(1, t + 1))
                   for t in range(1, n + 1)]
    h_after_t1 = [h_bal[t - 1] * (1 + h) - T1[t - 1] for t in range(1, n + 1)]
    lp = [d * (1 - co) for d in D]
    gp_co = [d * co for d in D]
    promote = [PR2[i] + PR3[i] for i in range(n)]
    gp = [gp_co[i] + promote[i] for i in range(n)]
    lp_eq, gp_eq = E * (1 - co), E * co
    W = dict(avail=list(cash), t1=T1, t2=T2, t3=T3, inv2=INV2, inv3=INV3, pr2=PR2, pr3=PR3, inv_total=D,
             rem1=[cash[i] - T1[i] for i in range(n)], rem2=[cash[i] - T1[i] - T2[i] for i in range(n)],
             pref_bal=pref_bal, h_bal=h_bal, h_after_t1=h_after_t1, lp=lp, gp_co=gp_co, promote=promote, gp=gp,
             lp_eq=lp_eq, gp_eq=gp_eq, promote_total=sum(promote))
    W["lp_irr"], W["gp_irr"] = _irr([-lp_eq] + lp), _irr([-gp_eq] + gp)
    W["lp_em"], W["gp_em"] = sum(lp) / lp_eq, sum(gp) / gp_eq
    # structural assertions that hold for ANY correct pari passu waterfall
    for i in range(n):
        assert abs(lp[i] + gp[i] - cash[i]) < 1e-6, "LP + GP must equal available cash"
    if W["promote_total"] < 1e-9:
        assert abs(W["lp_irr"] - _irr(lev_cf)) < 1e-9 and abs(W["gp_irr"] - _irr(lev_cf)) < 1e-9, \
            "no promote => LP IRR = GP IRR = deal IRR"
    return W


# Pre-2026-09-29-evening inputs that no longer exist in the workbook. Used ONLY to reproduce the
# prior base case (5.20%) as the starting row of the change bridge (bridge.py). Values are the
# ones in commit efb3da1's Assumptions tab.
LEGACY_INPUTS = dict(other_income_mo=35.0, contract_svc=450.0, rate=0.0385 + 0.0325, ltv=0.65, min_dy=0.08,
                     io_years=2, exit_spread=0.005, sofr30=0.0374)
LEGACY_FLAGS = ("classic_bug", "tax10", "util_old", "exit_old", "debt_old", "no_prepay", "no_paydown", "plan10",
                "b10", "sofr_old")


def run_model(I, price=None, exit_cap=None, legacy=()):
    """Full model. `price` overrides the purchase price (bid-price solve and sensitivity grids):
    reassessed tax, closing costs, the Scenario B LTV leg, the assumption paydown test and equity
    move with it. `exit_cap` overrides the direct exit-cap input (sensitivity grids).
    `legacy` switches individual changes OFF to rebuild the prior base case for the change bridge;
    the default (empty) is the current model. Flags: classic_bug, tax10, util_old, exit_old,
    debt_old, no_prepay, no_paydown."""
    L = set(legacy)
    assert L <= set(LEGACY_FLAGS), L
    P = I["price"] if price is None else price
    Y = range(NYEARS)
    ex = [(1 + I["exp_growth"]) ** y for y in Y]
    u = I["units"]
    m = {}

    # rent tracks
    mk, cl, pr = {}, {}, {}
    for t in I["types"]:
        a, b, c = [], [], []
        for y in Y:
            g = I["growth"][y]
            mv = t["H"] * (1 + g) if y == 0 else a[-1] * (1 + g)
            if y == 0:  # renovation program runs through Year 1: blended in-place / renovated rent
                cv = t["F"] * (1 - I["reno_y1_capture"]) + (mv + I["reno_premium_mo"]) * I["reno_y1_capture"]
            elif "classic_bug" in L:  # prior model: kept compounding the Year-1 blend (never reached market)
                cv = b[-1] * (1 + g)
            else:  # renovated from Year 2 on: market rent plus any premium
                cv = mv + I["reno_premium_mo"]
            base = t["G"] if y == 0 else c[-1]
            pv = base + I["turnover_rate"] * I["burnoff_pct"] * (mv - base)
            a.append(mv); b.append(cv); c.append(pv)
        mk[t["name"]], cl[t["name"]], pr[t["name"]] = a, b, c
    m["track_market"], m["track_classic"], m["track_prior"] = mk, cl, pr

    m["market_gpr"] = [sum(t["total"] * mk[t["name"]][y] for t in I["types"]) * 12 for y in Y]
    m["sched"] = [sum(t["classic"] * cl[t["name"]][y] + t["renov"] * pr[t["name"]][y] for t in I["types"]) * 12
                  for y in Y]
    m["ltl"] = [m["sched"][y] - m["market_gpr"][y] for y in Y]
    m["vac"] = [-x * I["vacancy"] for x in m["sched"]]
    m["cl"] = [-x * I["credit_loss"] for x in m["sched"]]
    m["con"] = [-x * I["concessions"] for x in m["sched"]]

    # --- utilities: owner-paid water/sewer (city tariff build) + trash (city rate), RUBS recovery
    if "util_old" in L:
        oi_mo, contract = LEGACY_INPUTS["other_income_mo"], LEGACY_INPUTS["contract_svc"]
        m["ws_unit_yr"] = m["trash_unit_yr"] = 0.0
        rubs_pct = 0.0
    else:
        oi_mo, contract = I["other_income_mo"], I["contract_svc"]
        monthly = (I["w_unit"] + I["kgal"] * I["w_kgal"]) + (I["s_unit"] + I["kgal"] * I["s_kgal"])
        m["ws_unit_yr"] = monthly * 12 + I["meters"] * I["meter_chg"] * 12 / u
        m["trash_unit_yr"] = I["trash_n"] * I["trash_rate"] * 12 / u
        rubs_pct = I["rubs_pct"]
    m["ws"] = [-u * m["ws_unit_yr"] * (1 + I["ws_growth"]) ** y for y in Y]
    m["trash"] = [-u * m["trash_unit_yr"] * ex[y] for y in Y]
    m["oi"] = [u * oi_mo * 12 * ex[y] for y in Y]
    m["rubs"] = [-rubs_pct * (m["ws"][y] + m["trash"][y]) for y in Y]
    m["egi"] = [m["sched"][y] + m["vac"][y] + m["cl"][y] + m["con"][y] + m["oi"][y] + m["rubs"][y] for y in Y]

    def line(base):
        return [-u * base * ex[y] for y in Y]
    m["payroll"], m["repairs"], m["turnover"] = line(I["payroll"]), line(I["repairs"]), line(I["turnover_cost"])
    m["contract"], m["util"] = line(contract), line(I["utilities"])
    ins_base = I["ins_roof"] if I["roof_toggle"] == 1 else I["ins_base"]
    m["ins"] = [-u * ins_base * (1 + I["ins_growth"]) ** y for y in Y]
    # Property tax: reassessed at purchase (price x cost-of-sale factor x millage), then grows with
    # JUST VALUE. The model ties just-value growth to its terminal market rent growth. The 10% cap
    # (Fla. Stat. 193.1555(3)) is a ceiling on assessed-value increases for non-school levies, not
    # a growth rate; it does not bind at 3%.
    m["tax_growth"] = I["nonhs_cap"] if "tax10" in L else I["growth"][-1]
    tax_y1 = P * I["cos_factor"] * I["millage"]
    m["tax"] = [-tax_y1 * (1 + m["tax_growth"]) ** y for y in Y]
    m["mgmt"] = [-m["egi"][y] * I["mgmt_fee_pct"] for y in Y]
    m["ga"], m["mktg"] = line(I["ga"]), line(I["marketing"])
    m["nav"] = line(I["nav"])  # per-unit non-ad valorem charges: not value-based
    fixed_keys = ["payroll", "repairs", "turnover", "contract", "util", "ws", "trash", "ins", "tax", "nav", "ga", "mktg"]
    m["opex"] = [sum(m[k][y] for k in fixed_keys) + m["mgmt"][y] for y in Y]
    m["noi"] = [m["egi"][y] + m["opex"][y] for y in Y]
    m["noi_pretax"] = [m["noi"][y] - m["tax"][y] for y in Y]
    m["reserves"] = [-u * I["reserves"] * ex[y] for y in Y]
    m["capex"] = [-(I["roof_toggle"] * I["roof_cost"] if y == 0 else 0.0)
                  - ((I["recert_inspect"] + I["recert_remed"]) if (y + 1) == I["recert_year"] else 0.0) for y in Y]
    m["ucf"] = [m["noi"][y] + m["reserves"][y] + m["capex"][y] for y in Y]

    # Day-0 bridge and cap rates (other income + RUBS at Year-1 levels; fixed opex = Year 1)
    oi0 = m["oi"][0] + m["rubs"][0]
    loss_pct = I["vacancy"] + I["credit_loss"] + I["concessions"]
    m["day0_gpr"] = sum(t["classic"] * t["F"] + t["renov"] * t["G"] for t in I["types"]) * 12
    m["day0_egi"] = m["day0_gpr"] * (1 - loss_pct) + oi0
    fixed0 = sum(m[k][0] for k in fixed_keys)
    m["day0_noi"] = m["day0_egi"] + fixed0 - m["day0_egi"] * I["mgmt_fee_pct"]
    s2_gpr = (sum(t["classic"] * t["F"] for t in I["types"])
              + sum(t["renov"] * (t["G"] + I["turnover_rate"] * I["burnoff_pct"] * (mk[t["name"]][0] - t["G"]))
                    for t in I["types"])) * 12
    s2_egi = s2_gpr * (1 - loss_pct) + oi0
    m["s2_noi"] = s2_egi + fixed0 - s2_egi * I["mgmt_fee_pct"]
    m["burnoff_effect"] = m["s2_noi"] - m["day0_noi"]
    m["capture_effect"] = m["noi"][0] - m["s2_noi"]
    m["cap_broker"] = I["broker_cap"]
    m["cap_inplace"] = m["day0_noi"] / P
    m["cap_y1fwd"] = m["noi"][0] / P

    # Exit cap: a direct market input (anchor + Class C / vintage spread), NOT derived from this deal
    if exit_cap is not None:
        m["exit_cap"] = exit_cap
    elif "exit_old" in L:
        m["exit_cap"] = m["cap_inplace"] + LEGACY_INPUTS["exit_spread"]
    else:
        m["exit_cap"] = I["exit_anchor"] + I["exit_vintage"]
    m["eff_tax_exit"] = I["millage"] * I["cos_factor"]
    m["fwd_noi_pretax"] = m["noi_pretax"][HOLD]  # Year 6
    m["exit_price"] = m["fwd_noi_pretax"] / (m["exit_cap"] + m["eff_tax_exit"])
    m["cost_of_sale"] = -m["exit_price"] * I["cos_exit"]
    m["net_unlev"] = m["exit_price"] + m["cost_of_sale"]

    # Sources & uses (Scenario B base) and unlevered returns
    reno_per_unit = sum(I["reno_lines"]) * (1 + I["reno_contg_pct"])
    m["reno_total"] = reno_per_unit * I["classic_units"]
    m["closing"] = P * I["closing_pct"]
    m["uses_b"] = P + m["closing"] + m["reno_total"]
    m["unlev_cf"] = [-m["uses_b"]] + [m["ucf"][y] for y in range(HOLD)]
    m["unlev_cf"][HOLD] += m["net_unlev"]
    m["unlev_irr"] = _irr(m["unlev_cf"])
    m["unlev_em"] = sum(m["unlev_cf"][1:]) / m["uses_b"]

    # ---- debt terms: agency fixed (10-yr UST + spread), sized on LTV and DSCR on AMORTIZING debt service
    old = "debt_old" in L
    rate = LEGACY_INPUTS["rate"] if old else I["ust10"] + I["agency_spread"]
    ltv = LEGACY_INPUTS["ltv"] if old else I["ltv"]
    io = LEGACY_INPUTS["io_years"] if old else I["io_years"]
    am = I["amort_years"]
    const = _pmt(rate, am, 1.0)  # annual mortgage constant
    m["rate"], m["const"] = rate, const

    def size(noi, value):
        legs = {"LTV": value * ltv}
        if old:
            legs["Debt Yield"] = noi / LEGACY_INPUTS["min_dy"]
            legs["DSCR"] = noi / (I["min_dscr"] * rate)  # prior model sized DSCR on IO debt service
        else:
            legs["DSCR"] = noi / (I["min_dscr"] * const)
        amt = min(legs.values())
        return amt, legs, next(k for k, v in legs.items() if v == amt)

    def prepay_pct(loan_year):
        if "no_prepay" in L or loan_year < 1:
            return 0.0
        return I["prepay"][int(loan_year) - 1]

    # ---- Scenario B: new agency debt at closing. Current: 5-year fixed (5-yr UST + spread) whose term
    # matches the 5-year hold, so it is repaid at maturity with no prepayment premium. Legacy "b10": the
    # prior 10-year fixed loan with the 10-year declining premium (loan year 5 = 3%).
    B = {}
    noi1 = m["noi"][0]
    b10 = "b10" in L
    b_rate = rate if b10 else I["ust5"] + I["agency_spread"]
    B["rate"], B["const"] = b_rate, _pmt(b_rate, am, 1.0)
    if b10:
        B["loan"], legs, B["binding"] = size(noi1, P)
    else:
        legs = {"LTV": P * ltv, "DSCR": noi1 / (I["min_dscr"] * B["const"])}
        B["loan"] = min(legs.values())
        B["binding"] = next(k for k, v in legs.items() if v == B["loan"])
    B["loan_ltv"], B["loan_dscr"] = legs["LTV"], legs["DSCR"]
    B["loan_dy"] = legs.get("Debt Yield")
    B["pmt"] = _pmt(b_rate, am, B["loan"])
    B["beg"], B["int"], B["prin"], B["ds"], B["end"] = [], [], [], [], []
    bal = B["loan"]
    for y in range(1, HOLD + 1):
        i_ = bal * b_rate
        p_ = 0.0 if y <= io else B["pmt"] - i_
        B["beg"].append(bal); B["int"].append(i_); B["prin"].append(p_); B["ds"].append(i_ + p_)
        bal -= p_
        B["end"].append(bal)
    B["dscr1"] = noi1 / B["ds"][0]
    B["equity"] = m["uses_b"] - B["loan"]
    B["lp_eq"], B["gp_eq"] = B["equity"] * (1 - I["gp_coinvest"]), B["equity"] * I["gp_coinvest"]
    B["payoff"] = -B["end"][-1]
    if b10:
        B["prepay_pct"] = prepay_pct(HOLD)  # 10-yr loan sold at the end of loan year 5
    else:  # 5-yr loan: repaid at maturity when the sale coincides with it; otherwise the 5-4-3-2-1 schedule
        B["prepay_pct"] = 0.0 if HOLD >= I["b_term"] else I["prepay5"][HOLD - 1]
    B["prepay"] = -B["end"][-1] * B["prepay_pct"]
    B["net_proceeds"] = m["exit_price"] + m["cost_of_sale"] + B["payoff"] + B["prepay"]
    B["lev_ops"] = [m["ucf"][y] - B["ds"][y] for y in range(HOLD)]
    B["lev_cf"] = [-B["equity"]] + list(B["lev_ops"])
    B["lev_cf"][HOLD] += B["net_proceeds"]
    B["irr"], B["em"] = _irr(B["lev_cf"]), sum(B["lev_cf"][1:]) / B["equity"]
    B["coc"] = [x / B["equity"] for x in B["lev_ops"]]

    # ---- Scenario A: assumed first + supplemental (after any lender-required paydown), refi after maturity
    A = {}
    mat = I["a_mat"]
    L0 = I["a_first_bal"] + I["a_supp_bal"]
    A["max_assumable"] = P * I["a_max_ltv"]
    A["assume_paydown"] = 0.0 if "no_paydown" in L else max(0.0, L0 - A["max_assumable"])
    A["paydown_supp"] = min(A["assume_paydown"], I["a_supp_bal"])
    A["paydown_first"] = A["assume_paydown"] - A["paydown_supp"]
    first0 = I["a_first_bal"] - A["paydown_first"]
    supp0 = I["a_supp_bal"] - A["paydown_supp"]
    for key, bal0, r_ in (("first", first0, I["a_first_rate"]), ("supp", supp0, I["a_supp_rate"])):
        beg, int_, prin, end = [], [], [], []
        bal = bal0
        pmt_ = _pmt(r_, am, bal0)
        for y in range(1, HOLD + 1):
            if y <= mat:
                i_ = bal * r_
                p_ = 0.0 if I["a_io"] == 1 else pmt_ - i_
                beg.append(bal); int_.append(i_); prin.append(p_)
                bal -= p_
                end.append(bal)
            else:
                beg.append(0.0); int_.append(0.0); prin.append(0.0); end.append(0.0)
        A[key] = dict(beg=beg, int=int_, prin=prin, end=end)
    A["payoff"] = A["first"]["end"][mat - 1] + A["supp"]["end"][mat - 1]
    pre_ds = [A["first"]["int"][y] + A["first"]["prin"][y] + A["supp"]["int"][y] + A["supp"]["prin"][y] for y in range(HOLD)]
    A["loan"] = first0 + supp0
    A["fee"] = A["loan"] * I["a_fee_pct"]
    A["uses"] = m["uses_b"] + A["fee"]
    A["equity"] = A["uses"] - A["loan"]
    A["lp_eq"], A["gp_eq"] = A["equity"] * (1 - I["gp_coinvest"]), A["equity"] * I["gp_coinvest"]
    A["refi_noi"] = m["noi"][mat]  # NOI of the first post-maturity year
    A["refi_value"] = A["refi_noi"] / m["exit_cap"]  # lender appraisal proxy: in-place NOI / market cap

    def finish(pl):
        """Common tail for every exit plan: equity, IRR, multiple, capital call."""
        pl["lev_cf"] = [-A["equity"]] + list(pl["lev_ops"])
        pl["lev_cf"][pl["sale_year"]] += pl["net_proceeds"]
        pl["irr"], pl["em"] = _irr(pl["lev_cf"]), sum(pl["lev_cf"][1:]) / A["equity"]
        pl["capital_call"] = max(0.0, -min(pl["lev_ops"][:pl["sale_year"]]))
        pl["peak_equity"] = A["equity"] + pl["capital_call"]
        return pl

    # Plan 1 -- sell when the 3.0% loan matures (end of Year `mat`), priced on Year mat+1 NOI
    sale = dict(sale_year=mat)
    sale["exit_price"] = m["noi_pretax"][mat] / (m["exit_cap"] + m["eff_tax_exit"])
    sale["cost_of_sale"] = -sale["exit_price"] * I["cos_exit"]
    sale["payoff"] = -A["payoff"]
    sale["net_proceeds"] = sale["exit_price"] + sale["cost_of_sale"] + sale["payoff"]
    sale["lev_ops"] = [(m["ucf"][y] - pre_ds[y]) if (y + 1) <= mat else 0.0 for y in range(HOLD)]
    finish(sale)

    # Refinance variants at maturity, held to the Year-HOLD sale
    def refi_plan(rate_, size_rate, io_yrs, upfront_pct, prepay_at_sale, legacy_size=False):
        pl = dict(sale_year=HOLD, rate=rate_, size_rate=size_rate)
        if legacy_size:
            pl["loan"], legs, pl["binding"] = size(A["refi_noi"], A["refi_value"])
        else:
            legs = {"LTV": A["refi_value"] * I["ltv"],
                    "DSCR": A["refi_noi"] / (I["min_dscr"] * _pmt(size_rate, am, 1.0))}
            pl["loan"] = min(legs.values())
            pl["binding"] = next(k for k, v in legs.items() if v == pl["loan"])
        pl["ltv_leg"], pl["dscr_leg"] = legs["LTV"], legs["DSCR"]
        pl["pmt"] = _pmt(rate_, am, pl["loan"])
        pl["upfront"] = pl["loan"] * upfront_pct  # rate-cap premium, paid at the refinance closing
        pl["cash_required"] = A["payoff"] - pl["loan"] + pl["upfront"]
        beg, int_, prin, end_ = [], [], [], []
        bal = 0.0
        for y in range(1, HOLD + 1):
            if y > mat:
                if y == mat + 1:
                    bal = pl["loan"]
                i_ = bal * rate_
                p_ = 0.0 if (y - mat) <= io_yrs else pl["pmt"] - i_
                beg.append(bal); int_.append(i_); prin.append(p_)
                bal -= p_
                end_.append(bal)
            else:
                beg.append(0.0); int_.append(0.0); prin.append(0.0); end_.append(0.0)
        pl.update(beg=beg, int=int_, prin=prin, end=end_)
        pl["ds"] = [pre_ds[y] + int_[y] + prin[y] for y in range(HOLD)]
        pl["prepay_pct"] = prepay_at_sale
        pl["prepay"] = -end_[-1] * prepay_at_sale
        pl["exit_price"], pl["cost_of_sale"] = m["exit_price"], m["cost_of_sale"]
        pl["payoff"] = -end_[-1]
        pl["net_proceeds"] = m["exit_price"] + m["cost_of_sale"] + pl["payoff"] + pl["prepay"]
        pl["lev_ops"] = [m["ucf"][y] - pl["ds"][y] - (pl["cash_required"] if (y + 1) == mat else 0.0) for y in range(HOLD)]
        # financing cost over the refi loan's life in the hold: interest + cap premium + prepayment premium
        pl["fin_cost"] = sum(int_) + pl["upfront"] - pl["prepay"]
        pl["fin_cost_pct_yr"] = pl["fin_cost"] / pl["loan"] / (HOLD - mat)
        return finish(pl)

    loan_yr_at_sale = HOLD - mat
    old_debt = "debt_old" in L
    plans = {"sale": sale}
    # Short refi (a): floating, 30-day Average SOFR + spread, priced rate cap, sized on the capped rate
    sofr30 = LEGACY_INPUTS["sofr30"] if "sofr_old" in L else I["sofr30"]
    plans["float"] = refi_plan(sofr30 + I["float_spread"], I["cap_strike"] + I["float_spread"],
                               HOLD if I["float_io"] == 1 else 0, I["cap_cost_pct"], I["float_prepay"])
    # Short refi (b): 5-year agency fixed, 5-yr UST + agency spread, 5-4-3-2-1 declining premium
    plans["fixed5"] = refi_plan(I["ust5"] + I["agency_spread"], I["ust5"] + I["agency_spread"], io, 0.0,
                                I["prepay5"][loan_yr_at_sale - 1])
    # Comparison only: 10-year agency fixed (the prior structure), 10-yr declining premium
    plans["fixed10"] = refi_plan(rate, rate, io, 0.0, prepay_pct(loan_yr_at_sale), legacy_size=old_debt)
    A["plans"] = plans
    A["short_choice"] = "float" if plans["float"]["fin_cost_pct_yr"] <= plans["fixed5"]["fin_cost_pct_yr"] else "fixed5"
    plan_code = 3 if "plan10" in L else int(I["a_plan"])
    A["plan_code"] = plan_code
    A["plan_key"] = {1: "sale", 2: A["short_choice"], 3: "fixed10"}[plan_code]
    sel = plans[A["plan_key"]]
    for k in ("lev_ops", "lev_cf", "irr", "em", "capital_call", "peak_equity", "net_proceeds", "sale_year"):
        A[k] = sel[k]
    A["coc1"] = A["lev_ops"][0] / A["equity"]

    # ---- Waterfalls (pari passu investor capital + GP promote), both scenarios
    W = waterfall(A["lev_cf"], A["equity"], I)
    B["W"] = waterfall(B["lev_cf"], B["equity"], I)

    m["B"], m["A"], m["W"] = B, A, W
    m["price"] = P
    return m


# ---------------------------------------------------------------------------
# Comparison against the recalculated workbook
# ---------------------------------------------------------------------------
class Comparator:
    def __init__(self, path):
        self.wb = openpyxl.load_workbook(path, data_only=True)
        self.rows = []  # (sheet, line, max_diff, tol, n_points, ok, detail)

    def ws(self, name):
        return self.wb[name]

    def _record(self, sheet, line, mine, theirs, tol):
        diffs = []
        for i, (a, b) in enumerate(zip(mine, theirs)):
            if not isinstance(b, (int, float)):
                diffs.append((i, a, b, float("inf")))
            else:
                diffs.append((i, a, b, abs(a - b)))
        worst = max(diffs, key=lambda d: d[3])
        ok = worst[3] <= tol
        self.rows.append((sheet, line, worst[3], tol, len(diffs), ok, worst))

    def series(self, sheet, label, mine, cols, tol=TOL_USD, exact=False, after=None, col_label=1):
        ws = self.ws(sheet)
        start = _find_row(ws, after) + 1 if after else 1
        r = _find_row(ws, label, col=col_label, exact=exact, start=start)
        theirs = [ws.cell(row=r, column=c).value for c in cols]
        self._record(sheet, label.strip(), mine, theirs, tol)

    def scalar(self, sheet, label, mine, col=2, tol=TOL_USD, exact=False, after=None):
        self.series(sheet, label, [mine], [col], tol=tol, exact=exact, after=after)

    def text_after(self, sheet, label, mine, after, col=2):
        ws = self.ws(sheet)
        theirs = ws.cell(row=_find_row(ws, label, start=_find_row(ws, after) + 1), column=col).value
        self.rows.append((sheet, label, 0.0 if theirs == mine else float("inf"), 0, 1, theirs == mine,
                          (0, mine, theirs, 0)))

    def text(self, sheet, label, mine, col=2):
        ws = self.ws(sheet)
        theirs = ws.cell(row=_find_row(ws, label), column=col).value
        self.rows.append((sheet, label, 0.0 if theirs == mine else float("inf"), 0, 1, theirs == mine,
                          (0, mine, theirs, 0)))


def compare(path, I, m):
    C = Comparator(path)
    OP, Y10 = "Operating Model", list(range(2, 2 + NYEARS))  # B..K = Years 1..10
    Y5 = list(range(3, 3 + HOLD))      # C..G = Years 1..5 on Returns / Returns (Assumed) / Waterfall
    Y05 = [2] + Y5                     # B..G = Years 0..5
    D5 = list(range(2, 2 + HOLD))      # B..F = Years 1..5 on Debt (Assumed)
    B, A, W = m["B"], m["A"], m["W"]

    # units consistency (the model's Units cell is a formula to the Unit Mix total) + computed Assumptions cells
    C.scalar("Assumptions", "Units (formula", I["units"], col=3, tol=0)
    C.scalar("Assumptions", "Property Tax Growth after Reassessment", m["tax_growth"], col=3, tol=TOL_RATE)
    C.scalar("Assumptions", "Water & Sewer Cost ($/unit/year)", m["ws_unit_yr"], col=3)
    C.scalar("Assumptions", "Trash Cost ($/unit/year)", m["trash_unit_yr"], col=3)
    C.scalar("Assumptions", "All-In Fixed Rate", m["rate"], col=3, tol=TOL_RATE)
    C.scalar("Assumptions", "EXIT CAP RATE (base case)", m["exit_cap"], col=3, tol=TOL_RATE)

    # Operating model, every line, 10 years
    for t in I["types"]:
        n = t["name"]
        C.series(OP, f"{n} — Market Rent/mo", m["track_market"][n], Y10)
        C.series(OP, f"{n} — Classic-Unit Track Rent/mo", m["track_classic"][n], Y10)
        C.series(OP, f"{n} — Prior-Renovated Track Rent/mo", m["track_prior"][n], Y10)
    for lab, key, ex in [("Gross Potential Rent at Market", "market_gpr", False), ("Less: Loss-to-Lease", "ltl", False),
                         ("Gross Scheduled Rent", "sched", False), ("Less: Physical Vacancy", "vac", False),
                         ("Less: Credit Loss", "cl", False), ("Less: Concessions", "con", False),
                         ("Plus: Other Income (laundry", "oi", False), ("Plus: Utility Reimbursement", "rubs", False),
                         ("Effective Gross Income (EGI)", "egi", False),
                         ("Payroll", "payroll", True), ("Repairs & Maintenance", "repairs", True),
                         ("Turnover / Make-Ready", "turnover", True), ("Contract Services", "contract", True),
                         ("Utilities — common-area", "util", False), ("Water & Sewer (owner-paid", "ws", False),
                         ("Trash (owner-paid", "trash", False), ("Insurance", "ins", True),
                         ("Property Tax (reassessed at purchase", "tax", False), ("Non-Ad Valorem Assessments", "nav", False),
                         ("Management Fee (% of EGI)", "mgmt", True),
                         ("G&A / Admin", "ga", True), ("Marketing", "mktg", True),
                         ("Total Operating Expenses", "opex", True), ("NET OPERATING INCOME (NOI)", "noi", True),
                         ("memo: NOI Before Property Tax", "noi_pretax", False),
                         ("Less: Replacement Reserves", "reserves", True), ("Less: One-Time Capex", "capex", False),
                         ("UNLEVERED CASH FLOW", "ucf", False)]:
        C.series(OP, lab, m[key], Y10, exact=ex)

    # NOI bridge, cap rates, exit (Returns tab)
    R = "Returns"
    C.scalar(R, "Day-0 Gross Potential Rent", m["day0_gpr"])
    C.scalar(R, "Day-0 Effective Gross Income", m["day0_egi"])
    C.scalar(R, "DAY-0 IN-PLACE NOI", m["day0_noi"])
    C.scalar(R, "S2 NOI", m["s2_noi"])
    C.scalar(R, "+ Loss-to-lease burn-off effect", m["burnoff_effect"])
    C.scalar(R, "+ Renovation-premium partial-year capture effect", m["capture_effect"])
    C.scalar(R, "= YEAR-1 FORWARD NOI", m["noi"][0])
    C.scalar(R, "1. Broker-Stated Cap Rate", m["cap_broker"], tol=TOL_RATE)
    C.scalar(R, "2. In-Place Cap Rate", m["cap_inplace"], tol=TOL_RATE)
    C.scalar(R, "3. Year-1 FORWARD Cap Rate", m["cap_y1fwd"], tol=TOL_RATE)
    C.scalar(R, "Exit Cap Rate — base case", m["exit_cap"], tol=TOL_RATE)
    C.scalar(R, "memo: exit cap minus in-place", m["exit_cap"] - m["cap_inplace"], tol=TOL_RATE)
    C.scalar(R, "Effective Tax Rate at Exit", m["eff_tax_exit"], tol=TOL_RATE)
    C.scalar(R, "Forward NOI Before Property Tax", m["fwd_noi_pretax"])
    C.scalar(R, "EXIT PRICE", m["exit_price"])
    C.scalar(R, "Less: Cost of Sale", m["cost_of_sale"])
    C.scalar(R, "Net Sale Proceeds, UNLEVERED", m["net_unlev"])
    C.series(R, "TOTAL UNLEVERED CASH FLOW TO EQUITY", m["unlev_cf"], Y05)
    C.scalar(R, "Unlevered IRR (debt-agnostic)", m["unlev_irr"], tol=TOL_RATE)
    C.scalar(R, "Unlevered Equity Multiple (debt-agnostic)", m["unlev_em"], tol=TOL_RATE)

    # Scenario B -- Capital, Debt, Returns
    C.scalar("Capital", "Purchase Price", m["price"])
    C.scalar("Capital", "Closing Costs", m["closing"])
    C.scalar("Capital", "Renovation Capex", m["reno_total"])
    C.scalar("Capital", "TOTAL USES", m["uses_b"])
    C.scalar("Capital", "Senior Loan", B["loan"])
    C.scalar("Capital", "Sponsor Equity (plug)", B["equity"])
    C.scalar("Capital", "LP Equity", B["lp_eq"], exact=True)
    C.scalar("Capital", "GP Equity (co-invest)", B["gp_eq"])
    C.scalar("Debt", "Annual Mortgage Constant", B["const"], col=3, tol=1e-7)
    C.scalar("Assumptions", "Scenario B All-In Rate", B["rate"], col=3, tol=TOL_RATE)
    C.scalar("Assumptions", "Scenario B Prepayment Premium at Sale", B["prepay_pct"], col=3, tol=TOL_RATE)
    C.scalar("Debt", "Loan Amount — LTV Constraint", B["loan_ltv"], col=3)
    C.scalar("Debt", "Loan Amount — DSCR Constraint", B["loan_dscr"], col=3)
    C.scalar("Debt", "Resulting DSCR (Year 1)", B["dscr1"], col=3, tol=TOL_RATE)
    C.scalar("Debt", "Prepayment Premium % at Sale", B["prepay_pct"], col=3, tol=TOL_RATE)
    C.scalar("Debt", "SIZED LOAN AMOUNT", B["loan"], col=3)
    C.text("Debt", "Binding Constraint", B["binding"], col=3)
    C.scalar("Debt", "Annual P&I Payment (post-IO)", B["pmt"])
    dws = C.ws("Debt")
    yr_rows = {dws.cell(row=r, column=1).value: r for r in range(1, dws.max_row + 1)
               if isinstance(dws.cell(row=r, column=1).value, int)}
    for col, key, lab in [(2, "beg", "Beg. Balance"), (3, "int", "Interest"), (4, "prin", "Principal"),
                          (5, "ds", "Debt Service"), (6, "end", "End Balance")]:
        theirs = [dws.cell(row=yr_rows[y], column=col).value for y in range(1, HOLD + 1)]
        C._record("Debt", f"Scenario B schedule: {lab}", B[key], theirs, TOL_USD)
    C.series(R, "Less: Debt Service (Scenario B)", [-x for x in B["ds"]], Y5)
    C.series(R, "Levered CF from Operations (Scenario B)", B["lev_ops"], Y5)
    C.scalar(R, "Less: Loan Payoff (Scenario B", B["payoff"])
    C.scalar(R, "Less: Prepayment Premium (Scenario B", B["prepay"])
    C.scalar(R, "NET SALE PROCEEDS TO EQUITY — SCENARIO B", B["net_proceeds"])
    C.series(R, "TOTAL LEVERED CASH FLOW TO EQUITY — SCENARIO B", B["lev_cf"], Y05)
    C.scalar(R, "Levered IRR — SCENARIO B", B["irr"], tol=TOL_RATE)
    C.scalar(R, "Levered Equity Multiple — SCENARIO B", B["em"], tol=TOL_RATE)
    C.series(R, "CASH-ON-CASH BY YEAR", B["coc"], Y5, tol=TOL_RATE, after=None)  # label row itself is a header
    # (CoC values sit on the row after the header -- re-point)
    C.rows.pop()
    rws = C.ws(R)
    hr = _find_row(rws, "CASH-ON-CASH BY YEAR")
    C._record(R, "Cash-on-cash by year (Scenario B)", B["coc"], [rws.cell(row=hr + 1, column=c).value for c in Y5],
              TOL_RATE)

    # Scenario A -- Debt (Assumed)
    DA = "Debt (Assumed)"
    C.scalar(DA, "Max Assumable Balance", A["max_assumable"])
    C.scalar(DA, "Required Paydown at Closing", A["assume_paydown"])
    C.scalar(DA, "First Mortgage Balance Assumed", A["loan"] - (I["a_supp_bal"] - A["paydown_supp"]))
    C.scalar(DA, "Supplemental Balance Assumed", I["a_supp_bal"] - A["paydown_supp"])
    for sect, key in [("FIRST MORTGAGE", "first"), ("SUPPLEMENTAL LOAN", "supp")]:
        C.series(DA, "Beginning Balance", A[key]["beg"], D5, after=sect)
        C.series(DA, "Interest", A[key]["int"], D5, exact=True, after=sect)
        C.series(DA, "Principal", A[key]["prin"], D5, after=sect)
        C.series(DA, "Ending Balance", A[key]["end"], D5, after=sect)
        C.rows[-4:] = [(s_, f"{key}: {l}", d, t, n, ok, w) for (s_, l, d, t, n, ok, w) in C.rows[-4:]]
    pre_ds = [A["first"]["int"][y] + A["first"]["prin"][y] + A["supp"]["int"][y] + A["supp"]["prin"][y] for y in range(HOLD)]
    C.series(DA, "Assumed Loans Debt Service", pre_ds, D5)
    C.scalar(DA, "Payoff Balance at Maturity", A["payoff"])
    C.scalar(DA, "NOI in the first post-maturity year", A["refi_noi"])
    C.scalar(DA, "Value at Refinance", A["refi_value"])
    for key, sect in [("float", "REFI OPTION 2a"), ("fixed5", "REFI OPTION 2b"), ("fixed10", "COMPARISON ONLY — 10-YEAR")]:
        pl = A["plans"][key]
        n0 = len(C.rows)
        C.scalar(DA, "All-in rate", pl["rate"], tol=TOL_RATE, after=sect)
        C.scalar(DA, "Sizing rate for the DSCR test", pl["size_rate"], tol=TOL_RATE, after=sect)
        C.scalar(DA, "Loan — LTV constraint", pl["ltv_leg"], after=sect)
        C.scalar(DA, "Loan — DSCR constraint", pl["dscr_leg"], after=sect)
        C.scalar(DA, "REFI LOAN AMOUNT", pl["loan"], after=sect)
        C.text_after(DA, "Binding constraint", pl["binding"], sect)
        C.scalar(DA, "Annual P&I payment", pl["pmt"], after=sect)
        C.scalar(DA, "Upfront cost at refinance", pl["upfront"], after=sect)
        C.scalar(DA, "Cash Required at Refinance", pl["cash_required"], after=sect)
        C.series(DA, "Refi Loan Beginning Balance", pl["beg"], D5, after=sect)
        C.series(DA, "Refi Loan Interest", pl["int"], D5, after=sect)
        C.series(DA, "Refi Loan Principal", pl["prin"], D5, after=sect)
        C.series(DA, "Refi Loan Ending Balance", pl["end"], D5, after=sect)
        C.series(DA, "TOTAL DEBT SERVICE", pl["ds"], D5, after=sect)
        C.scalar(DA, "Prepayment premium % at the Year-5 sale", pl["prepay_pct"], tol=TOL_RATE, after=sect)
        C.scalar(DA, "Prepayment premium $ at sale", -pl["prepay"], after=sect)
        C.scalar(DA, "Financing cost over the refi", pl["fin_cost"], after=sect)
        C.scalar(DA, "Financing cost, % of loan per year", pl["fin_cost_pct_yr"], tol=TOL_RATE, after=sect)
        C.rows[n0:] = [(s_, f"{key}: {l}", d, t, n, ok, w) for (s_, l, d, t, n, ok, w) in C.rows[n0:]]
    C.scalar(DA, "Short-refi choice", 1 if A["short_choice"] == "float" else 2, tol=0)

    # Scenario A -- Returns (Assumed): sources & uses, each exit plan, selected base case
    RA = "Returns (Assumed)"
    C.scalar(RA, "Loan Assumption Fee", A["fee"])
    C.scalar(RA, "Total Uses (Scenario B uses + assumption fee)", A["uses"])
    C.scalar(RA, "Assumed Debt (First + Supplemental", A["loan"])
    C.scalar(RA, "Sponsor Equity", A["equity"], exact=True)
    C.scalar(RA, "LP Equity (90%)", A["lp_eq"])
    C.scalar(RA, "GP Equity (10%", A["gp_eq"])
    C.scalar(RA, "memo: required paydown at assumption", A["assume_paydown"])
    C.series(RA, "Unlevered CF (same as Scenario B", [m["ucf"][y] for y in range(HOLD)], Y5)
    sale = A["plans"]["sale"]
    n0 = len(C.rows)
    C.scalar(RA, "Exit price = Year-4 NOI before tax", sale["exit_price"], after="PLAN 1")
    C.scalar(RA, "Less: cost of sale", sale["cost_of_sale"], after="PLAN 1")
    C.scalar(RA, "Less: payoff of the assumed loans at maturity", sale["payoff"], after="PLAN 1")
    C.scalar(RA, "Net sale proceeds at maturity", sale["net_proceeds"], after="PLAN 1")
    C.rows[n0:] = [(s_, f"sale: {l}", d, t, n, ok, w) for (s_, l, d, t, n, ok, w) in C.rows[n0:]]
    for key, sect in [("sale", "PLAN 1"), ("float", "PLAN 2a"), ("fixed5", "PLAN 2b"), ("fixed10", "PLAN 3")]:
        pl = A["plans"][key]
        n0 = len(C.rows)
        if key != "sale":
            C.scalar(RA, "Less: refi loan payoff", pl["payoff"], after=sect)
            C.scalar(RA, "Less: prepayment premium", pl["prepay"], after=sect)
            C.scalar(RA, "Net sale proceeds (Year 5)", pl["net_proceeds"], after=sect)
        C.series(RA, "Levered CF from operations", pl["lev_ops"], Y5, after=sect)
        C.series(RA, "Total levered cash flow to equity", pl["lev_cf"], Y05, after=sect)
        C.scalar(RA, "Levered IRR", pl["irr"], tol=TOL_RATE, after=sect)
        C.scalar(RA, "Levered equity multiple", pl["em"], tol=TOL_RATE, after=sect)
        C.scalar(RA, "Capital call", pl["capital_call"], after=sect)
        C.scalar(RA, "Peak equity", pl["peak_equity"], after=sect)
        C.rows[n0:] = [(s_, f"{key}: {l}", d, t, n, ok, w) for (s_, l, d, t, n, ok, w) in C.rows[n0:]]
    labels = {"sale": "1. Sell at maturity", "float": "2a. Short refi: floating + cap", "fixed5": "2b. Short refi: 5-yr fixed",
              "fixed10": "3. 10-yr fixed refi (comparison)"}
    C.text(RA, "Exit plan in the base case", labels[A["plan_key"]])
    C.series(RA, "Levered CF from Operations", A["lev_ops"], Y5, exact=True, after="SELECTED BASE CASE")
    C.series(RA, "TOTAL LEVERED CASH FLOW TO EQUITY — SCENARIO A", A["lev_cf"], Y05)
    C.scalar(RA, "Levered IRR — SCENARIO A", A["irr"], tol=TOL_RATE)
    C.scalar(RA, "Levered Equity Multiple — SCENARIO A", A["em"], tol=TOL_RATE)
    C.scalar(RA, "Year-1 Cash-on-Cash — SCENARIO A", A["coc1"], tol=TOL_RATE)
    C.scalar(RA, "Capital Call Required", A["capital_call"])
    C.scalar(RA, "PEAK EQUITY — SCENARIO A", A["peak_equity"])
    # Waterfall (Scenario A), tier by tier -- engine uses a different (closed-form) method
    WF = "Waterfall"
    C.series(WF, "Available Cash for Distribution", W["avail"], Y5)
    C.scalar(WF, "Investor Capital, Year 0", A["equity"])
    C.series(WF, "Investor Pref Hurdle Balance, End of Year", W["pref_bal"], Y05)
    C.series(WF, "Tier 1 Distribution to Investors", W["t1"], Y5)
    C.series(WF, "Remaining Cash After Tier 1", W["rem1"], Y5)
    C.series(WF, "Investor Tier-2 Hurdle Balance, End of Year", W["h_bal"], Y05)
    C.series(WF, "Tier-2 Hurdle Balance After Tier-1 Cash Applied", W["h_after_t1"], Y5)
    C.series(WF, "Tier 2 Total Distribution", W["t2"], Y5)
    C.series(WF, "Tier 2 to investors", W["inv2"], Y5)
    C.series(WF, "Tier 2 GP promote", W["pr2"], Y5)
    C.series(WF, "Remaining Cash After Tier 2", W["rem2"], Y5)
    C.series(WF, "Tier 3 Total Distribution", W["t3"], Y5)
    C.series(WF, "Tier 3 to investors", W["inv3"], Y5)
    C.series(WF, "Tier 3 GP promote", W["pr3"], Y5)
    C.series(WF, "Total to Investors", [0.0] + W["inv_total"], Y05)
    C.series(WF, "LP Total Distribution", [-W["lp_eq"]] + W["lp"], Y05)
    C.series(WF, "GP Co-Invest Distribution", [-W["gp_eq"]] + W["gp_co"], Y05)
    C.series(WF, "GP Promote (Tier 2 + Tier 3)", [0.0] + W["promote"], Y05)
    C.series(WF, "GP Total Distribution", [-W["gp_eq"]] + W["gp"], Y05)
    C.scalar(WF, "LP IRR", W["lp_irr"], tol=TOL_RATE, exact=True)
    C.scalar(WF, "GP IRR (co-invest + promote)", W["gp_irr"], tol=TOL_RATE)
    C.scalar(WF, "LP Equity Multiple", W["lp_em"], tol=TOL_RATE, exact=True)
    C.scalar(WF, "GP Equity Multiple (co-invest + promote)", W["gp_em"], tol=TOL_RATE)
    C.scalar(WF, "Total GP Promote over the hold", W["promote_total"])

    # Summary headline cells (what gets quoted)
    SM = "Summary"
    C.scalar(SM, "Levered IRR (deal-level, Scenario A)", A["irr"], tol=TOL_RATE)
    C.scalar(SM, "Levered Equity Multiple (deal-level, Scenario A)", A["em"], tol=TOL_RATE)
    C.scalar(SM, "Unlevered IRR (debt-agnostic)", m["unlev_irr"], tol=TOL_RATE)
    C.scalar(SM, "LP IRR (Scenario A)", W["lp_irr"], tol=TOL_RATE)
    C.scalar(SM, "GP IRR (Scenario A)", W["gp_irr"], tol=TOL_RATE)
    C.scalar(SM, "2. In-Place Cap Rate", m["cap_inplace"], tol=TOL_RATE)
    C.scalar(SM, "Exit Cap Rate (base case", m["exit_cap"], tol=TOL_RATE)
    C.scalar(SM, "Sponsor Equity", A["equity"], exact=True)
    compare_sensitivity(C, I, m)
    return C


def _grid(ws, title_prefix):
    """Locate a sensitivity table by its section title; return (irr_rows, em_rows) as 5x5 value lists."""
    t = _find_row(ws, title_prefix, max_row=ws.max_row + 1)
    hdr = _find_row(ws, "rows \\ cols", start=t, max_row=ws.max_row + 1)
    irr = [[ws.cell(row=hdr + 1 + i, column=2 + j).value for j in range(5)] for i in range(5)]
    em = [[ws.cell(row=hdr + 7 + i, column=2 + j).value for j in range(5)] for i in range(5)]
    return irr, em


def compare_sensitivity(C, I, m):
    """Every sensitivity cell (100 IRRs + 100 multiples) recomputed by a FULL re-run of this engine with
    the axis inputs changed -- not by re-implementing the workbook's per-scenario calculation blocks."""
    import copy
    ws = C.ws("Sensitivity")
    ks = [-2, -1, 0, 1, 2]
    ec0, P0 = m["exit_cap"], I["price"]
    es, ps, gs, cs, prs = (I["sens_exit_step"], I["sens_price_step"], I["sens_growth_step"],
                           I["sens_cost_step"], I["sens_prem_step"])

    def rec(tab, mine_irr, mine_em, theirs_irr, theirs_em, cols=range(5)):
        for i in range(5):
            C._record("Sensitivity", f"{tab} IRR row {i+1}", [mine_irr[i][j] for j in cols],
                      [theirs_irr[i][j] for j in cols], TOL_RATE)
            C._record("Sensitivity", f"{tab} EM row {i+1}", [mine_em[i][j] for j in cols],
                      [theirs_em[i][j] for j in cols], TOL_RATE)

    # Table 1 (A) and Table 4 (B): exit cap x price
    for tab, scen, title in (("T1", "A", "TABLE 1 "), ("T4", "B", "TABLE 4 ")):
        gi, ge = _grid(ws, title)
        mi, me = [[None] * 5 for _ in range(5)], [[None] * 5 for _ in range(5)]
        for i, ki in enumerate(ks):
            for j, kj in enumerate(ks):
                r_ = run_model(I, price=P0 * (1 + kj * ps), exit_cap=ec0 + ki * es)[scen]
                mi[i][j], me[i][j] = r_["irr"], r_["em"]
        rec(tab, mi, me, gi, ge)
    # Table 3 (A): premium x reno cost
    gi, ge = _grid(ws, "TABLE 3 ")
    mi, me = [[None] * 5 for _ in range(5)], [[None] * 5 for _ in range(5)]
    for i, ki in enumerate([0, 1, 2, 3, 4]):
        for j, kj in enumerate(ks):
            J = copy.deepcopy(I)
            J["reno_premium_mo"] = I["reno_premium_mo"] + ki * prs
            J["reno_lines"] = [x * (1 + kj * cs) for x in I["reno_lines"]]
            r_ = run_model(J)["A"]
            mi[i][j], me[i][j] = r_["irr"], r_["em"]
    rec("T3", mi, me, gi, ge)
    # Table 2 (A): exit cap x rent growth shift (added to every year's growth; tax growth follows terminal growth)
    gi, ge = _grid(ws, "TABLE 2 ")
    mi, me = [[None] * 5 for _ in range(5)], [[None] * 5 for _ in range(5)]
    for i, ki in enumerate(ks):
        for j, kj in enumerate(ks):
            J = copy.deepcopy(I)
            J["growth"] = [g + kj * gs for g in I["growth"]]
            r_ = run_model(J, exit_cap=ec0 + ki * es)["A"]
            mi[i][j], me[i][j] = r_["irr"], r_["em"]
    rec("T2", mi, me, gi, ge)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "Parkview_Crossing_Acquisition_Model.xlsx"
    I = load_inputs(path)
    m = run_model(I)
    C = compare(path, I, m)
    fails = [r for r in C.rows if not r[5]]
    n_points = sum(r[4] for r in C.rows)
    print(f"verify_model.py -- {path}")
    print(f"Inputs read: {sum(1 for k in I if k not in ('types',))} scalar/list inputs + {len(I['types'])} unit types "
          f"(all asserted literal, none a formula). Units = {I['units']:.0f}.\n")
    print(f"{'Sheet':18s} {'Line':62s} {'pts':>4s} {'max |diff|':>14s}  status")
    for sheet, line, d, tol, n, ok, worst in C.rows:
        dstr = "inf" if d == float("inf") else (f"{d:.6f}" if tol < 1 else f"{d:,.4f}")
        print(f"{sheet[:18]:18s} {line[:62]:62s} {n:>4d} {dstr:>14s}  {'OK' if ok else 'DIFF'}")
    print(f"\n{len(C.rows)} lines, {n_points} individual figures compared "
          f"(tolerance: ${TOL_USD:.0f} on dollar lines, {TOL_RATE*1e4:.0f} bp on rates/IRRs/multiples).")
    if fails:
        print(f"RESULT: {len(fails)} LINE(S) DIFFER BEYOND TOLERANCE")
        for sheet, line, d, tol, n, ok, (i, mine, theirs, dd) in fails:
            print(f"  {sheet} / {line}: point {i}: mine={mine!r} workbook={theirs!r}")
        sys.exit(1)
    print("RESULT: every compared figure ties to the workbook within tolerance.")
    print(f"\nHeadline (recomputed independently): unlevered IRR {m['unlev_irr']:.2%} | "
          f"Scen A levered IRR {m['A']['irr']:.2%} / {m['A']['em']:.2f}x | "
          f"Scen B levered IRR {m['B']['irr']:.2%} / {m['B']['em']:.2f}x | "
          f"LP IRR {m['W']['lp_irr']:.2%} / {m['W']['lp_em']:.2f}x | GP IRR {m['W']['gp_irr']:.2%} | promote ${m['W']['promote_total']:,.0f}")


if __name__ == "__main__":
    main()
