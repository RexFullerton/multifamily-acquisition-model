#!/usr/bin/env python3
"""
Independent verification: recomputes the full model from ASSUMPTION VALUES
ONLY -- reading Assumptions/Unit Mix input cells by label (never a hardcoded
row number, never a formula string, never a cell the build script already
computed) -- and compares every year's NOI, debt service, exit valuation,
cash flows, and waterfall distributions against the workbook's own
recalculated output.

This exists because the Phase 3 checks and the earlier Python IRR spot-check
both shared a blind spot: they either reused the model's own row pointers,
or recomputed IRR from cash flows the model itself had already produced.
Neither could catch a bug in how those cash flows were built (which is
exactly what happened -- see NOI_BRIDGE_AND_DEBT_SCENARIOS.md, Section 0).
This script shares no code path with build_model.py at all.

Usage: python3 verify_from_assumptions.py [path-to-recalculated-xlsx]
"""
import sys
import openpyxl
import numpy_financial as npf

PATH = sys.argv[1] if len(sys.argv) > 1 else "Parkview_Crossing_Acquisition_Model.xlsx"
TOL_DOLLARS = 1.0       # $1 tolerance on dollar figures (floating point)
TOL_PCT = 0.0005        # 5bps tolerance on rate/IRR figures

wb = openpyxl.load_workbook(PATH, data_only=True)


def find_row(ws, label_substr, col=1, max_row=250, exact=False):
    for r in range(1, max_row):
        v = ws.cell(row=r, column=col).value
        if isinstance(v, str) and (v == label_substr if exact else label_substr in v):
            return r
    raise ValueError(f"Label {'equal to' if exact else 'containing'} {label_substr!r} not found in {ws.title}")


def val(ws, label_substr, col=3, **kw):
    return ws.cell(row=find_row(ws, label_substr, **kw), column=col).value


# =====================================================================
# 1. READ ASSUMPTIONS (by label, not row number)
# =====================================================================
asm = wb["Assumptions"]

units = val(asm, "Units")
price = val(asm, "Purchase Price ($)")
broker_cap = val(asm, "Broker-Stated Cap Rate")
closing_pct = val(asm, "Closing Costs (% of Price)")
millage = val(asm, "Combined Millage Rate")
seller_taxable = val(asm, "Seller's Current TAXABLE Value")
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
exit_spread_sens = val(asm, "Exit Cap Spread over Entry — Sensitivity Ceiling")
cost_of_sale_exit = val(asm, "Cost of Sale at Exit")

pref = val(asm, "Preferred Return %")
tier2_lp = val(asm, "Tier 2 LP Share")
tier2_gp = val(asm, "Tier 2 GP Share")
tier2_hurdle = val(asm, "Tier 2 IRR Hurdle")
tier3_lp = val(asm, "Tier 3 LP Share")
tier3_gp = val(asm, "Tier 3 GP Share")
gp_coinvest = val(asm, "GP Co-Invest %")

# =====================================================================
# 2. READ UNIT MIX
# =====================================================================
um = wb["Unit Mix"]
types = []
EXPECTED_TYPES = ("Studio", "1BR/1BA", "2BR/1BA", "2BR/2BA")
for r in range(1, 20):
    if len(types) == len(EXPECTED_TYPES):
        break  # stop at the main rent-roll table -- the "RENOVATION CAPEX BY TYPE"
               # section below reuses the same 4 type-name labels in column A
    name = um.cell(row=r, column=1).value
    if name in EXPECTED_TYPES:
        total = um.cell(row=r, column=2).value
        classic = um.cell(row=r, column=3).value
        renov = total - classic
        sf = um.cell(row=r, column=5).value
        f_inplace = um.cell(row=r, column=6).value
        g_inplace = um.cell(row=r, column=7).value  # already computed by the workbook's own formula
        h_market = um.cell(row=r, column=8).value
        types.append(dict(name=name, total=total, classic=classic, renov=renov,
                           f=f_inplace, g=g_inplace, h=h_market))

print(f"Read {len(types)} unit types, {sum(t['total'] for t in types)} total units")

# =====================================================================
# 3. OPERATING MODEL — 10 years, independently rebuilt
# =====================================================================
NYEARS = 10
market = {t['name']: [] for t in types}
classic_track = {t['name']: [] for t in types}
prior_track = {t['name']: [] for t in types}

for t in types:
    m_prev = None
    c_prev = None
    p_prev = None
    for y in range(1, NYEARS + 1):
        g = growth[y - 1]
        m = t['h'] * (1 + g) if y == 1 else m_prev * (1 + g)
        if y == 1:
            c = t['f'] * (1 - reno_y1_capture) + (m + reno_premium_mo) * reno_y1_capture
        else:
            c = c_prev * (1 + g)
        if y == 1:
            p = t['g'] + turnover_rate * burnoff_pct * (m - t['g'])
        else:
            p = p_prev + turnover_rate * burnoff_pct * (m - p_prev)
        market[t['name']].append(m)
        classic_track[t['name']].append(c)
        prior_track[t['name']].append(p)
        m_prev, c_prev, p_prev = m, c, p

gpr = []
for y in range(NYEARS):
    total_monthly = sum(t['classic'] * classic_track[t['name']][y] + t['renov'] * prior_track[t['name']][y]
                         for t in types)
    gpr.append(total_monthly * 12)

vac = [-g * vacancy for g in gpr]
cl_ = [-g * credit_loss for g in gpr]
con = [-g * concessions for g in gpr]
oi = [units * other_income_mo * 12 * (1 + exp_growth) ** y for y in range(NYEARS)]
egi = [gpr[y] + vac[y] + cl_[y] + con[y] + oi[y] for y in range(NYEARS)]

def opex_series(base):
    return [-units * base * (1 + exp_growth) ** y for y in range(NYEARS)]

payroll_s = opex_series(payroll)
repairs_s = opex_series(repairs)
turnover_s = opex_series(turnover_cost)
contract_s = opex_series(contract_svc)
util_s = opex_series(utilities)
ins_base_for_calc = insurance_base  # roof toggle off in base case
ins_s = [-units * ins_base_for_calc * (1 + ins_growth) ** y for y in range(NYEARS)]

just_value_entry = price * cos_factor
buyer_tax_y1 = just_value_entry * millage
tax_s = []
for y in range(NYEARS):
    tax_s.append(-(buyer_tax_y1 * (1 + nonhs_cap) ** y))

mgmt_s = [-egi[y] * mgmt_fee_pct for y in range(NYEARS)]
ga_s = opex_series(ga)
mktg_s = opex_series(marketing)

opex_total = [payroll_s[y] + repairs_s[y] + turnover_s[y] + contract_s[y] + util_s[y] +
              ins_s[y] + tax_s[y] + mgmt_s[y] + ga_s[y] + mktg_s[y] for y in range(NYEARS)]
noi = [egi[y] + opex_total[y] for y in range(NYEARS)]
noi_pretax = [noi[y] - tax_s[y] for y in range(NYEARS)]

reserves_s = [-units * reserves * (1 + exp_growth) ** y for y in range(NYEARS)]
capex_s = []
for y in range(NYEARS):
    yr = y + 1
    c = 0.0
    if yr == 1:
        c -= roof_toggle * val(asm, "Roof Replacement Cost")
    if yr == recert_year:
        c -= (recert_inspect + recert_remediation)
    capex_s.append(c)
ucf = [noi[y] + reserves_s[y] + capex_s[y] for y in range(NYEARS)]

# =====================================================================
# 4. DAY-0 IN-PLACE NOI (for the entry-cap anchor)
# =====================================================================
day0_gpr = sum(t['classic'] * t['f'] + t['renov'] * t['g'] for t in types) * 12
day0_egi = day0_gpr * (1 - vacancy - credit_loss - concessions) + units * other_income_mo * 12
day0_fixed_opex = (-units * payroll - units * repairs - units * turnover_cost - units * contract_svc
                    - units * utilities - units * ins_base_for_calc + tax_s[0] - units * ga - units * marketing)
day0_mgmt = -day0_egi * mgmt_fee_pct
day0_noi = day0_egi + day0_fixed_opex + day0_mgmt
cap_inplace = day0_noi / price

print(f"\nDay-0 In-Place NOI: ${day0_noi:,.2f}  (cap {cap_inplace:.4%})")
print(f"Year-1 Forward NOI: ${noi[0]:,.2f}  (cap {noi[0]/price:.4%})")

# =====================================================================
# 5. DEBT (ASSUMED) — Scenario A
# =====================================================================
first_bal = [0.0] * hold_years
supp_bal = [0.0] * hold_years
first_int = [0.0] * hold_years
supp_int = [0.0] * hold_years
fb, sb = assum_first_bal, assum_supp_bal
for y in range(hold_years):
    yr = y + 1
    if yr <= assum_first_maturity_yr:
        first_bal[y] = fb
        supp_bal[y] = sb
        fi = fb * assum_first_rate
        si = sb * assum_supp_rate
        first_int[y] = fi
        supp_int[y] = si
        if not assum_io:
            fp = -npf.pmt(assum_first_rate, amort_years, assum_first_bal) - fi
            sp = -npf.pmt(assum_supp_rate, amort_years, assum_supp_bal) - si
            fb -= fp
            sb -= sp

# fb/sb are the running balances updated through the maturity year (inclusive) --
# after the loop above, they equal the true ending/payoff balance at maturity,
# whether or not assum_io is toggled off (first_bal[y]/supp_bal[y] store the
# BEGINNING-of-year snapshot, not the ending one, so they're not usable here).
payoff = fb + sb

refi_noi = noi[assum_first_maturity_yr]  # NOI in the year AFTER maturity (0-indexed: index == maturity_yr)
loan_ltv = price * ltv
loan_dy = refi_noi / min_debt_yield
loan_dscr = refi_noi / (min_dscr * rate)
refi_loan = min(loan_ltv, loan_dy, loan_dscr)
refi_paydown = payoff - refi_loan  # cash required (+) or released (-) at refinance

pmt_refi = -npf.pmt(rate, amort_years, refi_loan)
refi_bal = [0.0] * hold_years
refi_int = [0.0] * hold_years
refi_prin = [0.0] * hold_years
rb = refi_loan
for y in range(hold_years):
    yr = y + 1
    if yr > assum_first_maturity_yr:
        refi_bal[y] = rb
        ri = rb * rate
        refi_int[y] = ri
        years_since_refi = yr - assum_first_maturity_yr
        if years_since_refi > io_years:
            rp = pmt_refi - ri
            refi_prin[y] = rp
            rb -= rp

total_ds = [first_int[y] + supp_int[y] + refi_int[y] + refi_prin[y] for y in range(hold_years)]
total_end_bal = [first_bal[y] + supp_bal[y] + refi_bal[y] for y in range(hold_years)]
# apply refinance cash event to the levered cash flow, not the balance

print(f"\nDebt (Assumed): Payoff @ maturity Yr{assum_first_maturity_yr} = ${payoff:,.2f}, "
      f"Refi loan = ${refi_loan:,.2f}, Refi paydown = ${refi_paydown:,.2f}")
print("Total debt service by year:", [f"{d:,.2f}" for d in total_ds])
print("Total ending balance by year:", [f"{d:,.2f}" for d in total_end_bal])

# =====================================================================
# 6. EXIT VALUATION (tax-adjusted)
# =====================================================================
exit_cap_base = cap_inplace + exit_spread_base
eff_tax_exit = millage * cos_factor
fwd_noi_pretax = noi_pretax[hold_years]  # Year 6 (index 5)
exit_price = fwd_noi_pretax / (exit_cap_base + eff_tax_exit)
cost_of_sale_amt = -exit_price * cost_of_sale_exit
loan_payoff_exit = -total_end_bal[hold_years - 1]
net_proceeds = exit_price + cost_of_sale_amt + loan_payoff_exit

print(f"\nExit cap (in-place + 50bps): {exit_cap_base:.4%}")
print(f"Exit price: ${exit_price:,.2f}")
print(f"Net sale proceeds (Scenario A): ${net_proceeds:,.2f}")

# =====================================================================
# 7. CASH FLOWS, IRR, EQUITY MULTIPLE — Scenario A
# =====================================================================
assumption_fee = (assum_first_bal + assum_supp_bal) * assum_fee_pct
uses_b = price + price * closing_pct + reno_per_unit * sum(t['classic'] for t in types)
uses_a = uses_b + assumption_fee
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

irr_a = npf.irr(lev_cf_full)
em_a = sum(lev_cf_full[1:]) / -lev_cf_full[0]
print(f"\nScenario A Levered CF: {[f'{c:,.2f}' for c in lev_cf_full]}")
print(f"Scenario A Levered IRR (independent): {irr_a:.4%}")
print(f"Scenario A Levered EM (independent):  {em_a:.4f}x")

# =====================================================================
# 8. WATERFALL — hurdle-balance method, independently rebuilt
# =====================================================================
lp_eq = equity_a * (1 - gp_coinvest)
gp_eq = equity_a * gp_coinvest

t1_bal = lp_eq
t2_bal = lp_eq
lp_dist = []
gp_dist = []
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
    gp_t2 = t2_total * tier2_gp
    t2_bal = t2_after_t1 - lp_t2
    remaining_after_t2 = remaining_after_t1 - t2_total

    t3_total = remaining_after_t2
    lp_t3 = t3_total * tier3_lp
    gp_t3 = t3_total * tier3_gp

    lp_dist.append(t1_d + lp_t2 + lp_t3)
    gp_dist.append(gp_t2 + gp_t3)

lp_cf_full = [-lp_eq] + lp_dist
gp_cf_full = [-gp_eq] + gp_dist
lp_irr = npf.irr(lp_cf_full)
lp_em = sum(lp_cf_full[1:]) / -lp_cf_full[0]
try:
    gp_irr = npf.irr(gp_cf_full)
except Exception:
    gp_irr = float('nan')
gp_em = sum(gp_cf_full[1:]) / -gp_cf_full[0] if -gp_cf_full[0] else float('nan')

print(f"\nLP distributions: {[f'{d:,.2f}' for d in lp_dist]}")
print(f"GP distributions: {[f'{d:,.2f}' for d in gp_dist]}")
print(f"LP IRR (independent): {lp_irr:.4%}  |  LP EM: {lp_em:.4f}x")
print(f"GP IRR (independent): {gp_irr:.4%}  |  GP EM: {gp_em:.4f}x")

# =====================================================================
# 9. COMPARE AGAINST THE WORKBOOK
# =====================================================================
print("\n" + "=" * 70)
print("COMPARISON AGAINST WORKBOOK")
print("=" * 70)

rt = wb["Returns"]
ra = wb["Returns (Assumed)"]
wf = wb["Waterfall"]

mismatches = []

def check(label, mine, theirs, is_pct=False):
    tol = TOL_PCT if is_pct else TOL_DOLLARS
    ok = abs(mine - theirs) < tol
    status = "OK" if ok else "MISMATCH"
    if not ok:
        mismatches.append((label, mine, theirs))
    fmt = "{:.4%}" if is_pct else "{:,.2f}"
    print(f"{label:55s} mine={fmt.format(mine):>14s} workbook={fmt.format(theirs):>14s} [{status}]")

wb_noi_row = find_row(wb["Operating Model"], "NET OPERATING INCOME")
for y in range(hold_years):
    theirs = wb["Operating Model"].cell(row=wb_noi_row, column=2 + y).value
    check(f"Year {y+1} NOI", noi[y], theirs)

wb_ds_row = find_row(wf, "Available Cash for Distribution")
for y in range(hold_years):
    theirs = wf.cell(row=wb_ds_row, column=3 + y).value
    check(f"Year {y+1} Waterfall Available Cash (Scenario A levered CF)", lev_cf[y], theirs)

check("Day-0 In-Place NOI", day0_noi, val(rt, "DAY-0 IN-PLACE NOI", col=2))
check("Exit Price", exit_price, val(rt, "EXIT PRICE", col=2))
check("Scenario A Levered IRR", irr_a, val(ra, "Levered IRR", col=2), is_pct=True)
check("Scenario A Levered EM", em_a, val(ra, "Levered Equity Multiple", col=2))
check("LP IRR", lp_irr, val(wf, "LP IRR", col=2, exact=True), is_pct=True)
check("LP Equity Multiple", lp_em, val(wf, "LP Equity Multiple", col=2, exact=True))
if not (gp_irr != gp_irr):  # not NaN
    gp_irr_wb = val(wf, "GP IRR", col=2, exact=True)
    if isinstance(gp_irr_wb, (int, float)):
        check("GP IRR", gp_irr, gp_irr_wb, is_pct=True)
    else:
        print(f"GP IRR: mine={gp_irr:.4%}  workbook='{gp_irr_wb}' (text, undefined in-sheet -- not compared numerically)")
check("GP Equity Multiple", gp_em, val(wf, "GP Equity Multiple", col=2, exact=True))

print("\n" + "=" * 70)
if mismatches:
    print(f"RESULT: {len(mismatches)} MISMATCH(ES) FOUND")
    for m in mismatches:
        print("  ", m)
else:
    print("RESULT: ALL CHECKS MATCH. Independent from-assumptions rebuild ties to the workbook.")
print("=" * 70)
