#!/usr/bin/env python3
"""
Solves for the maximum purchase price that achieves each of three targets
under Scenario A (assumed debt, the base case):
  - LP IRR >= 8% (clears the preferred return)
  - Levered IRR (deal-level) >= 12%
  - Levered IRR (deal-level) >= 15%

Reuses the exact mechanics verified in verify_from_assumptions.py (same
formulas, same design), just parameterized on price with everything else
held at the Assumptions-tab values. Note: the assumed debt balance
(first + supplemental mortgage) is a FIXED, disclosed dollar amount --
it does NOT resize with price, because it's an existing loan being
assumed, not new debt sized against the purchase price. Only the Year-3
refinance loan is price-sensitive (its LTV leg scales with price).

Usage: python3 price_solve.py [path-to-recalculated-xlsx]
"""
import sys
import openpyxl
import numpy_financial as npf
from scipy.optimize import brentq

PATH = sys.argv[1] if len(sys.argv) > 1 else "Parkview_Crossing_Acquisition_Model.xlsx"
wb = openpyxl.load_workbook(PATH, data_only=True)


def find_row(ws, label_substr, col=1, max_row=250, exact=False):
    for r in range(1, max_row):
        v = ws.cell(row=r, column=col).value
        if isinstance(v, str) and (v == label_substr if exact else label_substr in v):
            return r
    raise ValueError(f"Label {'equal to' if exact else 'containing'} {label_substr!r} not found in {ws.title}")


def val(ws, label_substr, col=3, **kw):
    return ws.cell(row=find_row(ws, label_substr, **kw), column=col).value


asm = wb["Assumptions"]
units = val(asm, "Units")
base_price = val(asm, "Purchase Price ($)")
closing_pct = val(asm, "Closing Costs (% of Price)")
millage = val(asm, "Combined Millage Rate")
cos_factor = val(asm, "Cost-of-Sale Factor")
nonhs_cap = val(asm, "Non-Homestead Annual Assessment Cap")

reno_lines = ["Kitchen (cabinet refacing", "Mini-split ductless AC", "Vinyl slider window",
              "Modern lighting fixtures", "LVP flooring", "Bathroom refresh", "Interior paint",
              "Turnover labor"]
reno_subtotal = sum(val(asm, lbl) for lbl in reno_lines)
reno_contg_pct = val(asm, "Contingency %", max_row=40)
reno_per_unit = reno_subtotal * (1 + reno_contg_pct)
reno_premium_mo = val(asm, "Renovated-Unit Rent Premium ($/month)")
reno_y1_capture = val(asm, "Year-1 Premium Capture %")

vacancy = val(asm, "Physical Vacancy %")
credit_loss = val(asm, "Credit Loss %")
concessions = val(asm, "Concessions % (of GPR)")
other_income_mo = val(asm, "Other Income ($/unit/month)")
burnoff_pct = val(asm, "Loss-to-Lease Burn-off %")
turnover_rate = val(asm, "Annual Turnover Rate %")
reno_headstart = val(asm, "Prior-Owner-Renovated Units")
growth = [val(asm, f"Year {i} Market Rent Growth") for i in range(1, 11)]
exp_growth = val(asm, "General Expense Growth %")
ins_growth = val(asm, "Insurance Growth %")
payroll = val(asm, "Payroll (on-site")
repairs = val(asm, "Repairs & Maintenance")
turnover_cost = val(asm, "Turnover / Make-Ready")
contract_svc = val(asm, "Contract Services")
utilities = val(asm, "Utilities (owner-paid")
insurance_base = val(asm, "Insurance — Base Case")
mgmt_fee_pct = val(asm, "Management Fee (% of EGI)")
ga = val(asm, "G&A / Admin")
marketing = val(asm, "Marketing")
reserves = val(asm, "Replacement Reserves")
roof_cost_input = val(asm, "Roof Replacement Cost")
roof_toggle = val(asm, "Roof Replacement Scenario Toggle")
recert_year = val(asm, "Recertification Year")
recert_inspect = val(asm, "Recertification Inspection Cost")
recert_remediation = val(asm, "Recertification Remediation Contingency")
sofr = val(asm, "1-Month SOFR")
spread = val(asm, "Spread (bps")
rate = sofr + spread
ltv = val(asm, "Maximum LTV %")
min_dscr = val(asm, "Minimum DSCR")
min_debt_yield = val(asm, "Minimum Debt Yield %")
io_years = val(asm, "Interest-Only Period (years)")
amort_years = val(asm, "Amortization (years)")
assum_first_bal = val(asm, "First Mortgage Balance")
assum_first_rate = val(asm, "First Mortgage Rate")
assum_first_maturity_yr = int(val(asm, "First Mortgage Maturity"))
assum_supp_bal = val(asm, "Supplemental Loan Balance")
assum_supp_rate = val(asm, "Supplemental Loan Rate")
assum_io = val(asm, "Both Loans Interest-Only")
assum_fee_pct = val(asm, "Loan Assumption Fee")
hold_years = int(val(asm, "Hold Period (years)"))
exit_spread_base = val(asm, "Exit Cap Spread over Entry — Base Case")
cost_of_sale_exit = val(asm, "Cost of Sale at Exit")
pref = val(asm, "Preferred Return %")
tier2_lp = val(asm, "Tier 2 LP Share")
tier2_gp = val(asm, "Tier 2 GP Share")
tier2_hurdle = val(asm, "Tier 2 IRR Hurdle")
tier3_lp = val(asm, "Tier 3 LP Share")
tier3_gp = val(asm, "Tier 3 GP Share")
gp_coinvest = val(asm, "GP Co-Invest %")

um = wb["Unit Mix"]
types = []
EXPECTED_TYPES = ("Studio", "1BR/1BA", "2BR/1BA", "2BR/2BA")
for r in range(1, 20):
    if len(types) == len(EXPECTED_TYPES):
        break
    name = um.cell(row=r, column=1).value
    if name in EXPECTED_TYPES:
        total = um.cell(row=r, column=2).value
        classic = um.cell(row=r, column=3).value
        renov = total - classic
        f_inplace = um.cell(row=r, column=6).value
        g_inplace = um.cell(row=r, column=7).value
        h_market = um.cell(row=r, column=8).value
        types.append(dict(name=name, total=total, classic=classic, renov=renov,
                           f=f_inplace, g=g_inplace, h=h_market))

NYEARS = 10
reno_capex_total = reno_per_unit * sum(t['classic'] for t in types)
assumption_fee = (assum_first_bal + assum_supp_bal) * assum_fee_pct


def compute(price):
    """Returns a dict of results for a given purchase price, everything else
    held at the Assumptions-tab values. Mirrors verify_from_assumptions.py."""
    just_value_entry = price * cos_factor
    buyer_tax_y1 = just_value_entry * millage

    market = {t['name']: [] for t in types}
    classic_track = {t['name']: [] for t in types}
    prior_track = {t['name']: [] for t in types}
    for t in types:
        m_prev = c_prev = p_prev = None
        for y in range(1, NYEARS + 1):
            g = growth[y - 1]
            m = t['h'] * (1 + g) if y == 1 else m_prev * (1 + g)
            c = (t['f'] * (1 - reno_y1_capture) + (m + reno_premium_mo) * reno_y1_capture) if y == 1 \
                else c_prev * (1 + g)
            p = (t['g'] + turnover_rate * burnoff_pct * (m - t['g'])) if y == 1 \
                else p_prev + turnover_rate * burnoff_pct * (m - p_prev)
            market[t['name']].append(m); classic_track[t['name']].append(c); prior_track[t['name']].append(p)
            m_prev, c_prev, p_prev = m, c, p

    gpr = [sum(t['classic'] * classic_track[t['name']][y] + t['renov'] * prior_track[t['name']][y]
               for t in types) * 12 for y in range(NYEARS)]
    oi = [units * other_income_mo * 12 * (1 + exp_growth) ** y for y in range(NYEARS)]
    egi = [gpr[y] * (1 - vacancy - credit_loss - concessions) + oi[y] for y in range(NYEARS)]

    def opex_series(base):
        return [-units * base * (1 + exp_growth) ** y for y in range(NYEARS)]
    payroll_s, repairs_s = opex_series(payroll), opex_series(repairs)
    turnover_s, contract_s = opex_series(turnover_cost), opex_series(contract_svc)
    util_s = opex_series(utilities)
    ins_s = [-units * insurance_base * (1 + ins_growth) ** y for y in range(NYEARS)]
    tax_s = [-(buyer_tax_y1 * (1 + nonhs_cap) ** y) for y in range(NYEARS)]
    mgmt_s = [-egi[y] * mgmt_fee_pct for y in range(NYEARS)]
    ga_s, mktg_s = opex_series(ga), opex_series(marketing)
    opex_total = [payroll_s[y] + repairs_s[y] + turnover_s[y] + contract_s[y] + util_s[y] +
                  ins_s[y] + tax_s[y] + mgmt_s[y] + ga_s[y] + mktg_s[y] for y in range(NYEARS)]
    noi = [egi[y] + opex_total[y] for y in range(NYEARS)]
    noi_pretax = [noi[y] - tax_s[y] for y in range(NYEARS)]  # price-independent, see report

    reserves_s = [-units * reserves * (1 + exp_growth) ** y for y in range(NYEARS)]
    capex_s = []
    for y in range(NYEARS):
        yr = y + 1
        c = -roof_toggle * roof_cost_input if yr == 1 else 0.0
        if yr == recert_year:
            c -= (recert_inspect + recert_remediation)
        capex_s.append(c)
    ucf = [noi[y] + reserves_s[y] + capex_s[y] for y in range(NYEARS)]

    day0_gpr = sum(t['classic'] * t['f'] + t['renov'] * t['g'] for t in types) * 12
    day0_egi = day0_gpr * (1 - vacancy - credit_loss - concessions) + units * other_income_mo * 12
    day0_fixed_opex = (-units * payroll - units * repairs - units * turnover_cost - units * contract_svc
                        - units * utilities - units * insurance_base + tax_s[0] - units * ga - units * marketing)
    day0_mgmt = -day0_egi * mgmt_fee_pct
    day0_noi = day0_egi + day0_fixed_opex + day0_mgmt
    cap_inplace = day0_noi / price

    # Debt (Assumed) -- fixed balance, does NOT resize with price
    first_bal = supp_bal = None
    fb, sb = assum_first_bal, assum_supp_bal
    first_int = [0.0] * hold_years
    supp_int = [0.0] * hold_years
    for y in range(hold_years):
        yr = y + 1
        if yr <= assum_first_maturity_yr:
            first_int[y] = fb * assum_first_rate
            supp_int[y] = sb * assum_supp_rate
            if not assum_io:
                fp = -npf.pmt(assum_first_rate, amort_years, assum_first_bal) - first_int[y]
                sp = -npf.pmt(assum_supp_rate, amort_years, assum_supp_bal) - supp_int[y]
                fb -= fp; sb -= sp
    payoff = fb + sb

    refi_noi = noi[assum_first_maturity_yr]
    loan_ltv = price * ltv
    loan_dy = refi_noi / min_debt_yield
    loan_dscr = refi_noi / (min_dscr * rate)
    refi_loan = min(loan_ltv, loan_dy, loan_dscr)
    refi_paydown = payoff - refi_loan
    pmt_refi = -npf.pmt(rate, amort_years, refi_loan)

    refi_bal = [0.0] * hold_years
    refi_int = [0.0] * hold_years
    refi_prin = [0.0] * hold_years
    rb = refi_loan
    for y in range(hold_years):
        yr = y + 1
        if yr > assum_first_maturity_yr:
            refi_bal[y] = rb
            refi_int[y] = rb * rate
            if (yr - assum_first_maturity_yr) > io_years:
                rp = pmt_refi - refi_int[y]
                refi_prin[y] = rp
                rb -= rp
    total_ds = [first_int[y] + supp_int[y] + refi_int[y] + refi_prin[y] for y in range(hold_years)]
    total_end_bal = []
    fb2, sb2 = assum_first_bal, assum_supp_bal
    for y in range(hold_years):
        yr = y + 1
        if yr <= assum_first_maturity_yr:
            if not assum_io:
                fb2 -= (-npf.pmt(assum_first_rate, amort_years, assum_first_bal) - fb2 * assum_first_rate)
                sb2 -= (-npf.pmt(assum_supp_rate, amort_years, assum_supp_bal) - sb2 * assum_supp_rate)
            total_end_bal.append(fb2 + sb2)
        else:
            total_end_bal.append(refi_bal[y] - refi_prin[y])

    exit_cap_base = cap_inplace + exit_spread_base
    eff_tax_exit = millage * cos_factor
    fwd_noi_pretax = noi_pretax[hold_years]
    exit_price = fwd_noi_pretax / (exit_cap_base + eff_tax_exit)
    cost_of_sale_amt = -exit_price * cost_of_sale_exit
    loan_payoff_exit = -total_end_bal[hold_years - 1]
    net_proceeds = exit_price + cost_of_sale_amt + loan_payoff_exit

    uses_a = price * (1 + closing_pct) + reno_capex_total + assumption_fee
    equity_a = uses_a - (assum_first_bal + assum_supp_bal)

    lev_cf_ops = []
    for y in range(hold_years):
        cf = ucf[y] - total_ds[y]
        if (y + 1) == assum_first_maturity_yr:
            cf -= refi_paydown
        lev_cf_ops.append(cf)
    lev_cf = list(lev_cf_ops)
    lev_cf[hold_years - 1] += net_proceeds
    lev_cf_full = [-equity_a] + lev_cf
    deal_irr = npf.irr(lev_cf_full)
    deal_em = sum(lev_cf_full[1:]) / -lev_cf_full[0]

    lp_eq = equity_a * (1 - gp_coinvest)
    gp_eq = equity_a * gp_coinvest
    t1_bal = lp_eq
    t2_bal = lp_eq
    lp_dist = []
    for y in range(hold_years):
        avail = lev_cf[y]
        t1_boy = t1_bal * (1 + pref)
        t1_d = min(avail, t1_boy)
        t1_bal = t1_boy - t1_d
        remaining_after_t1 = avail - t1_d
        t2_boy = t2_bal * (1 + tier2_hurdle)
        t2_after_t1 = t2_boy - t1_d
        t2_total = min(remaining_after_t1, max(0, t2_after_t1) / tier2_lp)
        lp_t2 = t2_total * tier2_lp
        t2_bal = t2_after_t1 - lp_t2
        remaining_after_t2 = remaining_after_t1 - t2_total
        lp_t3 = remaining_after_t2 * tier3_lp
        lp_dist.append(t1_d + lp_t2 + lp_t3)
    lp_cf_full = [-lp_eq] + lp_dist
    lp_irr = npf.irr(lp_cf_full)

    return dict(price=price, cap_inplace=cap_inplace, equity_a=equity_a, deal_irr=deal_irr,
                deal_em=deal_em, lp_irr=lp_irr, refi_loan=refi_loan)


base = compute(base_price)
print(f"Sanity check at asking price ${base_price:,.0f}: "
      f"deal IRR {base['deal_irr']:.4%}, LP IRR {base['lp_irr']:.4%} "
      f"(cf. Summary tab: deal 8.07%, LP 9.96%)")

PRICE_FLOOR = assum_first_bal + assum_supp_bal  # below this, "assuming" this loan implies cash-out at close
print(f"\nStructural floor: assumed debt (${PRICE_FLOOR:,.0f}) must not exceed Total Uses. "
      f"That requires price >= ${(PRICE_FLOOR - reno_capex_total - assumption_fee) / (1 + closing_pct):,.0f} "
      f"(closing costs are the only price-scaled Use; reno capex and the assumption fee are fixed).")


FLOOR_PRICE = (PRICE_FLOOR - reno_capex_total - assumption_fee) / (1 + closing_pct)


def solve(target_fn, target_val, label):
    # Search only above the structural floor: below it, equity_a goes negative
    # (the fixed assumed-debt balance would exceed Total Uses), which breaks
    # the IRR sign-change assumption and isn't a coherent "assume this loan"
    # scenario anyway.
    lo, hi = FLOOR_PRICE + 1000, 30_000_000
    f_lo = target_fn(compute(lo)) - target_val
    f_hi = target_fn(compute(hi)) - target_val
    if f_lo * f_hi > 0:
        direction = "even at the structural floor" if f_lo < 0 else "even at $30M"
        print(f"\n{label}: UNREACHABLE ({direction}) within a price range where the assumed "
              f"${PRICE_FLOOR:,.0f} loan still makes structural sense (price >= ${FLOOR_PRICE:,.0f}).")
        print(f"  At the floor (${lo:,.0f}): {target_fn(compute(lo)):.4%}. At $30M: {target_fn(compute(hi)):.4%}.")
        return None
    price = brentq(lambda p: target_fn(compute(p)) - target_val, lo, hi, xtol=1.0)
    r = compute(price)
    below_floor = price < FLOOR_PRICE
    print(f"\n{label}")
    print(f"  Max price: ${price:,.0f}  ({(price/base_price - 1):+.1%} vs. ${base_price:,.0f} asking)")
    print(f"  Implied in-place cap rate at that price: {r['cap_inplace']:.4%}")
    print(f"  Deal IRR: {r['deal_irr']:.4%}  |  LP IRR: {r['lp_irr']:.4%}  |  Deal EM: {r['deal_em']:.2f}x")
    print(f"  Equity required: ${r['equity_a']:,.0f}  |  Refi loan at maturity: ${r['refi_loan']:,.0f}")
    if below_floor:
        print(f"  *** WARNING: this price (${price:,.0f}) is BELOW the ${FLOOR_PRICE:,.0f} floor at which "
              f"assuming the full ${PRICE_FLOOR:,.0f} loan still makes sense -- the assumed balance would "
              f"exceed Total Uses, implying a cash-out at close. Treat this target as unreachable under a "
              f"clean 'assume the existing loan' structure at this price.")
    return dict(**r, below_floor=below_floor)


print("\n" + "=" * 70)
print("BID PRICE SOLVE (Scenario A, assumed debt)")
print("=" * 70)
r1 = solve(lambda r: r['lp_irr'], 0.08, "TARGET 1: LP clears the 8% preferred return (LP IRR = 8%)")
r2 = solve(lambda r: r['deal_irr'], 0.12, "TARGET 2: Levered IRR (deal-level) = 12%")
r3 = solve(lambda r: r['deal_irr'], 0.15, "TARGET 3: Levered IRR (deal-level) = 15%")
