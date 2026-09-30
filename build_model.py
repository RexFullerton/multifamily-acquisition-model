#!/usr/bin/env python3
"""
Builds the Parkview Crossing acquisition model as a live-formula .xlsx.
All inputs live on ASSUMPTIONS / UNIT MIX; every other tab is formulas only.
"""
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
wb.remove(wb.active)

BLUE = Font(color="0000FF")
BLACK = Font(color="000000")
BOLD = Font(bold=True)
BOLD_BLUE = Font(bold=True, color="0000FF")
TITLE = Font(bold=True, size=14)
SECTION = Font(bold=True, size=11, color="FFFFFF")
SECTION_FILL = PatternFill("solid", fgColor="2F5496")
NOTE = Font(italic=True, size=9, color="808080")
PCT = "0.00%"
PCT1 = "0.0%"
USD = "#,##0"
USD2 = "#,##0.00"
USDC = '"$"#,##0'

def sheet(name):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    return ws

def title(ws, row, text):
    c = ws.cell(row=row, column=1, value=text)
    c.font = TITLE
    return row + 2

def section(ws, row, text, span=6):
    for col in range(1, span + 1):
        c = ws.cell(row=row, column=col)
        c.fill = SECTION_FILL
        c.font = SECTION
    ws.cell(row=row, column=1, value=text)
    return row + 1

def safe_note(note):
    # Excel/LibreOffice treat any cell string starting with "=" as a formula.
    if note and note.lstrip().startswith("="):
        note = "i.e." + note.lstrip()[1:]
    return note

def inp(ws, row, label, value, fmt=None, note=None, col=3, bold=False):
    ws.cell(row=row, column=1, value=label)
    c = ws.cell(row=row, column=col, value=value)
    c.font = BOLD_BLUE if bold else BLUE
    if fmt:
        c.number_format = fmt
    note = safe_note(note)
    if note:
        n = ws.cell(row=row, column=col + 2, value=note)
        n.font = NOTE
    return f"'{ws.title}'!${get_column_letter(col)}${row}"

def frm(ws, row, label, formula, fmt=None, note=None, col=3, bold=False):
    ws.cell(row=row, column=1, value=label)
    c = ws.cell(row=row, column=col, value=formula)
    c.font = BOLD if bold else BLACK
    if fmt:
        c.number_format = fmt
    note = safe_note(note)
    if note:
        n = ws.cell(row=row, column=col + 2, value=note)
        n.font = NOTE
    return f"'{ws.title}'!${get_column_letter(col)}${row}"

def colwidths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

# =====================================================================
# 1. ASSUMPTIONS
# =====================================================================
ws = sheet("Assumptions")
colwidths(ws, [42, 2, 16, 3, 46])
A = {}  # logical name -> cell address
r = 1
r = title(ws, r, "ASSUMPTIONS — Parkview Crossing, 901-951 NW 8th Ave, Pompano Beach, FL 33060")
ws.cell(row=r, column=1, value="Blue = input. Black = formula. Every number elsewhere in this workbook traces back to a cell on this tab or Unit Mix.").font = NOTE
r += 2

r = section(ws, r, "ACQUISITION")
A['units'] = frm(ws, r, "Units (formula = Unit Mix total, not an input)", 0, "0", "Single source of truth: sums the Unit Mix tab = 97. SOURCE: Broward County Property Appraiser, 3 parcels owned by Channel Grove LLC: folio 4842-35-00-0460 (951 NW 8 Ave, 20 units), 4842-35-00-0471 (901 NW 8 Ave, 18 units), 4842-35-00-0480 (930-980 NW 9 Ave, 59 units). The listing unit-type breakdown sums to 98, so one 1BR/1BA unit is removed on the Unit Mix tab pending the actual rent roll."); r += 1
A['price'] = inp(ws, r, "Purchase Price ($)", 13800000, USDC, "Broker-stated asking price (LoopNet)"); r += 1
A['broker_cap'] = inp(ws, r, "Broker-Stated Cap Rate", 0.07, PCT1, "LoopNet advertised cap rate"); r += 1
A['broker_noi'] = frm(ws, r, "Broker-Implied NOI ($)", f"={A['price']}*{A['broker_cap']}", USDC, "i.e. Price x Broker Cap (not used downstream)"); r += 1
A['closing_pct'] = inp(ws, r, "Closing Costs (% of Price)", 0.015, PCT1, "Broward doc stamps $0.70/$100 + title/legal/reports"); r += 1
A['closing_cost'] = frm(ws, r, "Closing Costs ($)", f"={A['price']}*{A['closing_pct']}", USDC); r += 1
r += 1

r = section(ws, r, "PROPERTY TAX REASSESSMENT")
A['millage'] = inp(ws, r, "Combined Millage Rate", 0.020171, "0.000000", "BCPA millage code 1512 (Pompano Beach), all 3 parcels. 2026 PROPOSED = 20.1710 mills (BCPA 2026 Proposed Millage Rate Table); 2025 FINAL = 20.2573. Using 2026 proposed as closest to the Year-1 (2027) levy; final 2026 rates are adopted at September budget hearings."); r += 1
A['seller_taxable'] = inp(ws, r, "Seller's Current TAXABLE Value ($)", 10318700, USDC, "BCPA-CONFIRMED: 2025 certified taxable value, sum of the 3 folios ($2,166,930 + $2,063,740 + $6,088,030). Matches the LoopNet figure. For reference, BCPA 2026 working just value = $11,650,640 (vs. model's statutory-method reassessment of $11,730,000)."); r += 1
A['cos_factor'] = inp(ws, r, "Cost-of-Sale Factor (DOR customary)", 0.85, PCT1, "Fla. Stat. 193.011(8): DOR sales-ratio studies customarily net sale price by 15% cost-of-sale allowance. Set to 100% to run the conservative (full-price) case instead."); r += 1
A['nonhs_cap'] = inp(ws, r, "Non-Homestead Assessment Cap (Fla. Stat. 193.1555) -- REFERENCE ONLY, not used in formulas", 0.10, PCT1, "Fla. Stat. 193.1555(3): for 'nonresidential' property, which under 193.1554(1) includes residential property of 10+ units, annual increases in ASSESSED value are capped at 10% for non-school levies (193.1555(2) excludes school district levies). Reset to just value the Jan 1 after a change of ownership (193.1555(5)). It is a ceiling, not a growth rate. Amendment 3 (Nov 2026 ballot, 5% cap) not modeled."); r += 1
A['tax_growth_row'] = r
A['tax_growth'] = frm(ws, r, "Property Tax Growth after Reassessment (= just-value growth = terminal market rent growth)", 0, PCT1, "After the sale resets assessed value to just value, assessed value tracks just value, so tax grows with market value, not at the 10% cap. Tied by formula to the model's terminal market rent growth (3.0%). The 10% cap is not binding at this rate. Prior model grew tax at 10%/yr, which was a misreading of the cap."); r += 1
A['just_value_entry'] = frm(ws, r, "Reassessed Just Value at Purchase ($)", f"={A['price']}*{A['cos_factor']}", USDC, "i.e. Purchase Price x Cost-of-Sale Factor"); r += 1
A['seller_tax'] = frm(ws, r, "Seller's Current Annual Tax ($)", f"={A['seller_taxable']}*{A['millage']}", USDC); r += 1
A['buyer_tax_y1'] = frm(ws, r, "Buyer's Year-1 Tax ($)", f"={A['just_value_entry']}*{A['millage']}", USDC, "Simplification: taxed on the reassessed value from Year 1. Strictly, reassessment takes effect the Jan 1 AFTER the sale; BCPA's 2026 working just value ($11.65M) is already within 1% of the reassessed $11.73M, so the difference is small."); r += 1
r += 1

r = section(ws, r, "RENOVATION PROGRAM — bottom-up scope, per classic unit")
reno_lines = [
    ("Kitchen (cabinet refacing, counter, appliance pkg)", 7000),
    ("Mini-split ductless AC system", 3500),
    ("Vinyl slider window replacement (~3 openings)", 1500),
    ("Modern lighting fixtures + ceiling fans", 400),
    ("LVP flooring (~700 SF)", 4000),
    ("Bathroom refresh (vanity, fixtures, re-caulk)", 1200),
    ("Interior paint", 500),
    ("Turnover labor / make-ready cleaning", 500),
]
reno_cells = []
for label, val in reno_lines:
    addr = inp(ws, r, label, val, USDC)
    reno_cells.append(addr)
    r += 1
A['reno_subtotal'] = frm(ws, r, "Subtotal ($/unit)", "=" + "+".join(reno_cells), USDC, bold=True); r += 1
A['reno_contg_pct'] = inp(ws, r, "Contingency %", 0.10, PCT1); r += 1
A['reno_contg'] = frm(ws, r, "Contingency ($/unit)", f"={A['reno_subtotal']}*{A['reno_contg_pct']}", USDC); r += 1
A['reno_per_unit'] = frm(ws, r, "TOTAL Renovation Cost ($/unit)", f"={A['reno_subtotal']}+{A['reno_contg']}", USDC, bold=True); r += 1
A['reno_units_mo'] = inp(ws, r, "Renovation Pace (units/month)", 4, "0"); r += 1
A['reno_premium_mo'] = inp(ws, r, "Renovated-Unit Rent Premium over Market ($/month)", 0, USDC, "Set to $0 (decision 2026-09-29). Renovated classic units reach MARKET rent, the same finish standard the prior owner used on the other 74 units, so a premium above market would double-count. The renovation's value is closing the in-place-to-market gap. Was $175."); r += 1
A['reno_premium_yr'] = frm(ws, r, "Renovated-Unit Rent Premium ($/year)", f"={A['reno_premium_mo']}*12", USDC); r += 1
A['reno_y1_capture'] = inp(ws, r, "Year-1 Premium Capture % (mid-program convention)", 0.5, PCT1, "6-month program starting month 1 of the hold -> average unit captures ~half a year of uplift in Year 1"); r += 1
r += 1

r = section(ws, r, "OPERATING ASSUMPTIONS")
A['vacancy'] = inp(ws, r, "Physical Vacancy %", 0.065, PCT1, "vs. 92% disclosed occupancy; nudged for renovation downtime"); r += 1
A['credit_loss'] = inp(ws, r, "Credit Loss % (of GPR)", 0.01, PCT1); r += 1
A['concessions'] = inp(ws, r, "Concessions % (of GPR)", 0.005, PCT1); r += 1
A['other_income_mo'] = inp(ws, r, "Other Income ex-Utility Recovery ($/unit/month)", 15, USDC, "JUDGMENT: laundry room, application/late fees, pet. Was $35 including RUBS; utility recovery is now its own line tied to the owner's actual water/sewer/trash cost (below)."); r += 1
A['rubs_pct'] = inp(ws, r, "Utility Reimbursement (RUBS) Recovery % of Owner Water/Sewer/Trash Cost", 0.60, PCT1, "JUDGMENT, flagged. Share of the owner's water/sewer/trash bill recovered from tenants via RUBS, net of vacancy, lease clauses not yet in place, and caps. Fully implemented programs are often cited higher; 60% is deliberately below that because it is not known whether current leases carry a RUBS clause. DILIGENCE: lease form + rent roll."); r += 1
A['burnoff_pct'] = inp(ws, r, "Loss-to-Lease Burn-off % per Turnover", 0.50, PCT1, "of remaining gap to market rent, closed at each turnover"); r += 1
A['turnover_rate'] = inp(ws, r, "Annual Turnover Rate %", 0.55, PCT1, "general Class B/C garden-apartment convention, not property-specific"); r += 1
A['reno_headstart'] = inp(ws, r, "Prior-Owner-Renovated Units: Starting Capture of Total Uplift", 0.65, PCT1, "judgment split of the disclosed 20.76% blended upside between already-renovated (partial capture) and classic (zero capture) units"); r += 1
r += 1

r = section(ws, r, "MARKET RENT GROWTH SCHEDULE (Broward/Pompano-sourced, capped at 3.0% terminal)")
growth_vals = [0.010, 0.0175, 0.025, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030]
growth_notes = [
    "Yardi Matrix (via MIAMI REALTORS+RWorld South Florida Rental Market Report, May 2026): Broward County Class C/C+ asking rents +0.2% YoY — near-flat current read, nudged to 1.0% for a full forward year",
    "judgment, gradual convergence",
    "judgment, gradual convergence",
    "capped at 3.0% per instruction — no source supports going higher for a multi-year terminal rate",
    "capped", "capped", "capped", "capped", "capped", "capped",
]
A['growth'] = []
for i, (v, n) in enumerate(zip(growth_vals, growth_notes), start=1):
    addr = inp(ws, r, f"Year {i} Market Rent Growth", v, PCT1, n)
    A['growth'].append(addr)
    r += 1
r += 1
ws.cell(row=A['tax_growth_row'], column=3, value=f"={A['growth'][-1]}")  # tax growth = terminal market rent growth

r = section(ws, r, "EXPENSE GROWTH")
A['exp_growth'] = inp(ws, r, "General Expense Growth % (ex-insurance, ex-tax)", 0.035, PCT1); r += 1
A['ins_growth'] = inp(ws, r, "Insurance Growth %", 0.07, PCT1, "above general expense growth given the recent ~37% two-year South Florida trend"); r += 1
r += 1

r = section(ws, r, "OPERATING EXPENSES (Year 1, $/unit/year unless noted)")
A['payroll'] = inp(ws, r, "Payroll (on-site mgmt + maintenance)", 1400, USDC); r += 1
A['repairs'] = inp(ws, r, "Repairs & Maintenance", 1100, USDC, "nudged up for 1958 vintage / undisclosed roof"); r += 1
A['turnover_cost'] = inp(ws, r, "Turnover / Make-Ready", 350, USDC); r += 1
A['contract_svc'] = inp(ws, r, "Contract Services (landscaping, pest; trash now its own line)", 280, USDC, "Was $450 including trash. Trash is now built from the city rate schedule (~$170/unit, below), so this line is reduced by the same amount; the total is unchanged. Judgment."); r += 1
A['utilities'] = inp(ws, r, "Utilities — Common-Area Electric & Vacant Units", 500, USDC, "JUDGMENT. Units have individual mini-split AC, so unit electric is assumed tenant-paid. This line covers common-area lighting, gates, laundry room, and vacant-unit electric."); r += 1
A['insurance_base'] = inp(ws, r, "Insurance — Base Case ($/unit)", 2400, USDC, "vintage-risk-adjusted above the general $2,000/unit South Florida average"); r += 1
A['insurance_roof'] = inp(ws, r, "Insurance — If Roof Replaced ($/unit)", 1900, USDC, "scenario only — see Roof section below"); r += 1
A['mgmt_fee_pct'] = inp(ws, r, "Management Fee (% of EGI)", 0.035, PCT1); r += 1
A['nav'] = inp(ws, r, "Non-Ad Valorem Assessments ($/unit, fire etc.)", 375, USDC, "BCPA tax history: 2025 total bills on the 3 folios = $245,413; ad valorem at 20.2573 mills on $10,318,700 taxable = $209,026; remainder $36,387 / 97 units = $375/unit (charged per unit, not on value). Consistent with the city residential fire assessment ($331/unit, $20-30 increases proposed for FY2026)."); r += 1
A['ga'] = inp(ws, r, "G&A / Admin", 250, USDC); r += 1
A['marketing'] = inp(ws, r, "Marketing", 150, USDC); r += 1
A['reserves'] = inp(ws, r, "Replacement Reserves (below NOI)", 300, USDC); r += 1
r += 1

r = section(ws, r, "WATER / SEWER / TRASH — OWNER-PAID (ASSUMED: listing silent -- DILIGENCE ITEM)")
ws.cell(row=r, column=1, value=(
    "The LoopNet/Crexi listings say nothing about who pays water, sewer or trash (the OM is gated). Per instruction, "
    "modeled as OWNER-PAID with RUBS recovery. Rates: City of Pompano Beach Code 50.03 (water) and 51.05 (wastewater), "
    "multifamily classification, charges effective 10/1/2026 (FY2027); solid waste: City of Pompano Beach Rate Schedule "
    "2025-2026 (eff. 10/1/2025), multifamily containerized non-compacted, 2x/week (the city minimum for multifamily).")).font = NOTE
r += 1
A['w_unit'] = inp(ws, r, "Water Service Charge per Unit ($/unit/month, FY2027)", 7.10, USD2, "Code 50.03(D)(2)(b): each additional unit on the same meter"); r += 1
A['w_kgal'] = inp(ws, r, "Water Commodity Charge ($/1,000 gal, 0-7,000 gal tier, FY2027)", 3.90, USD2, "Code 50.03(D)(2)(c), per-unit tier"); r += 1
A['s_unit'] = inp(ws, r, "Sewer Service Charge per Unit ($/unit/month, FY2027)", 16.10, USD2, "Code 51.05(D)(2)(a)"); r += 1
A['s_kgal'] = inp(ws, r, "Sewer Flow Charge ($/1,000 gal, FY2027)", 4.88, USD2, "Code 51.05(D)(2)(b)"); r += 1
A['kgal'] = inp(ws, r, "Water Use per Unit (1,000 gal/month)", 3.0, "0.0", "JUDGMENT: small units (studios/1BR, ~1-2 occupants). Replace with actual water bills."); r += 1
A['meters'] = inp(ws, r, "Number of Water Meters (judgment: one 2-inch per building)", 7, "0", "JUDGMENT: 7 buildings per listing; meter count/size unknown"); r += 1
A['meter_chg'] = inp(ws, r, "Monthly Service Charge per 2-inch Meter ($, FY2027)", 40.64, USD2, "Code 50.03(D)(2)(a), multifamily, 2-inch"); r += 1
A['ws_cost'] = frm(ws, r, "Water & Sewer Cost ($/unit/year)",
                   f"=(({A['w_unit']}+{A['kgal']}*{A['w_kgal']})+({A['s_unit']}+{A['kgal']}*{A['s_kgal']}))*12+{A['meters']}*{A['meter_chg']}*12/{A['units']}",
                   USDC, bold=True); r += 1
A['ws_growth'] = inp(ws, r, "Water & Sewer Cost Growth %", 0.06, PCT1, "Adopted city schedule through FY2029: per-unit bill at 3,000 gal rises ~5.8-6.0%/yr (water commodity +9.5%/yr, sewer flow +7.5%/yr, sewer base flat)"); r += 1
A['trash_n'] = inp(ws, r, "Trash Containers (6-yd, 2x/week; count is judgment)", 3, "0", "JUDGMENT: 97 units, 2x/week minimum pickup"); r += 1
A['trash_rate'] = inp(ws, r, "City Rate per 6-yd Container, 2x/week ($/month)", 457.63, USD2, "Pompano Beach Solid Waste Rate Schedule 2025-2026, multifamily containerized (non-compacted)"); r += 1
A['trash_cost'] = frm(ws, r, "Trash Cost ($/unit/year)", f"={A['trash_n']}*{A['trash_rate']}*12/{A['units']}", USDC, bold=True); r += 1
r += 1

r = section(ws, r, "ROOF & RECERTIFICATION — diligence items, not confident estimates")
A['roof_toggle'] = inp(ws, r, "Roof Replacement Scenario Toggle (1=on, 0=off)", 0, "0"); r += 1
A['roof_cost'] = inp(ws, r, "Roof Replacement Cost ($, one-time, Year 1 if toggled)", 235000, USDC, "~23,480 SF est. roof area x $8-12/SF hurricane-code TPO/mod-bit; midpoint of $188k-282k range"); r += 1
A['recert_year'] = inp(ws, r, "Recertification Year (model Year #)", 2, "0", "next 40/50-Year Program cycle due ~2028; Year 2 of the hold if closing is late 2026/early 2027"); r += 1
A['recert_inspect'] = inp(ws, r, "Recertification Inspection Cost ($, one-time)", 10000, USDC, "placeholder — no sourced fee"); r += 1
A['recert_remediation'] = inp(ws, r, "Recertification Remediation Contingency ($, one-time)", 150000, USDC, "placeholder — genuinely unknowable without an engineer's report"); r += 1
r += 1

r = section(ws, r, "DEBT — AGENCY FIXED-RATE TERMS (Scenario B new debt AND the Scenario A refinance)")
ws.cell(row=r, column=1, value=(
    "Fannie Mae Small Mortgage Loan program (loans up to $9M; max LTV 80%; min DSCR 1.25x; 5-30 yr terms; up to "
    "30-yr amortization; declining prepayment premium available) -- multifamily.fanniemae.com term sheet. Both the "
    "new loan (~$8M) and the Year-4 refinance fall under the $9M cap. Replaces the prior 7.10% floating bridge-style "
    "assumption, which had no rate-cap cost.")).font = NOTE
r += 1
A['ust10'] = inp(ws, r, "10-Year Treasury Yield", 0.0524, PCT, "FRED series DGS10, 9/28/2026 (latest print). Held flat; no forward curve."); r += 1
A['agency_spread'] = inp(ws, r, "Agency Spread over 10-Year Treasury", 0.0200, PCT, "JUDGMENT within broker-sourced ranges: multifamily.loans cites agency spreads 'generally 200-250 bps'; its Aug-2026 Fannie/Freddie small-loan quotes (6.10-8.20% vs a 4.70% 10-yr) imply 140-350 bps; apartmentloanstore.com Fannie quotes on 9/29/2026 (6.28-6.87%) imply ~105-165 bps over today's 10-yr for larger/better assets. 200 bps reflects small balance, 1958 Class C, and a declining-prepay (not yield-maintenance) structure. Indicative, not a term sheet."); r += 1
A['rate'] = frm(ws, r, "All-In Fixed Rate (10-yr fixed)", f"={A['ust10']}+{A['agency_spread']}", PCT, bold=True); r += 1
A['ltv'] = inp(ws, r, "Maximum LTV %", 0.75, PCT1, "Program max 80%; 75% used for a 1958 Class C asset (judgment). Refinance LTV applies to value at refinance (NOI / exit cap)."); r += 1
A['min_dscr'] = inp(ws, r, "Minimum DSCR (on amortizing debt service)", 1.25, "0.00x", "Fannie Small Loan minimum. Sized on the fully amortizing payment, as agencies do."); r += 1
A['io_years'] = inp(ws, r, "Interest-Only Period (years)", 0, "0", "JUDGMENT: DSCR-constrained agency loans generally do not get interest-only; partial IO usually requires lower leverage."); r += 1
A['amort_years'] = inp(ws, r, "Amortization (years)", 30, "0"); r += 1
A['prepay'] = []
for i, v in enumerate([0.05, 0.05, 0.04, 0.04, 0.03, 0.03, 0.02, 0.02, 0.01, 0.01], start=1):
    note = ("Fannie Mae Declining Prepayment Premium, 10-year fixed structure 5-5-4-4-3-3-2-2-1-1, no lockout "
            "(multifamily.fanniemae.com term sheet). Scenario B sale = loan year 5; refi loan sale = loan year (5 - maturity year).") if i == 1 else None
    A['prepay'].append(inp(ws, r, f"Prepayment Premium, Loan Year {i}", v, PCT1, note)); r += 1
A['prepay_range'] = f"{A['prepay'][0]}:{A['prepay'][-1].split('!')[1]}"
r += 1

r = section(ws, r, "DEBT — SCENARIO A: ASSUMABLE EXISTING DEBT (broker-disclosed, LoopNet/Crexi)")
A['assum_first_bal'] = inp(ws, r, "First Mortgage Balance ($)", 5887000, USDC, "Crexi listing (\"Non-Agency\"); LoopNet shows $5,908,933.50 -- small discrepancy, likely different as-of dates. Used the Crexi figure since paired with the explicit 4.2% blended-rate confirmation."); r += 1
A['assum_first_rate'] = inp(ws, r, "First Mortgage Rate (fixed)", 0.030, PCT1, "LoopNet + Crexi, both state 3.0% fixed"); r += 1
A['assum_first_maturity_yr'] = inp(ws, r, "First Mortgage Maturity (model Year #)", 3, "0", "Broker states \"fixed until December 2029.\" If Year 1 = calendar 2027, Dec 2029 falls in model Year 3 -- adjust this cell if your actual closing date shifts the calendar mapping."); r += 1
A['assum_supp_bal'] = inp(ws, r, "Supplemental Loan Balance ($)", 3563000, USDC, "LoopNet + Crexi, both state $3,563,000"); r += 1
A['assum_supp_rate'] = inp(ws, r, "Supplemental Loan Rate", 0.062, PCT1, "LoopNet + Crexi, both state 6.20%"); r += 1
A['assum_blended_rate'] = frm(ws, r, "Blended Rate (formula, weighted avg -- ties to broker's stated 4.2%)",
                                f"=({A['assum_first_bal']}*{A['assum_first_rate']}+{A['assum_supp_bal']}*{A['assum_supp_rate']})/({A['assum_first_bal']}+{A['assum_supp_bal']})",
                                PCT1); r += 1
A['assum_io'] = inp(ws, r, "Both Loans Interest-Only Through First's Maturity (1=yes)", 1, "0", "JUDGMENT -- amortization/IO status is NOT disclosed publicly for either loan. IO is a common structure for non-agency assumable loans marketed on a cash-flow basis, and is roughly consistent with the broker's \"almost 10% cash-on-cash Day 1\" claim. Flagged, not confirmed."); r += 1
A['assum_fee_pct'] = inp(ws, r, "Loan Assumption Fee (% of assumed balance)", 0.005, PCT1, "JUDGMENT -- not disclosed. 0.5-1.0% is a commonly cited range for CMBS/balance-sheet loan assumption fees; used the low end. Also assumes ~30-60 days of lender consent/underwriting, not separately costed."); r += 1
A['assum_max_ltv'] = inp(ws, r, "Assumption Approval: Max LTV on Purchase Price (paydown test)", 0.75, PCT1, "JUDGMENT: the lender's assumption test is not disclosed. If assumed balances exceed this % of the new purchase price, the buyer must pay the loan down at closing (applied to the 6.2% supplemental first). Binds below ~$12.6M. Year-1 DSCR (~2.3x) is not a constraint, so no DSCR test is modeled."); r += 1
r += 1

r = section(ws, r, "SCENARIO A EXIT PLAN — what happens when the 3.0% loan matures (end of Year 3, Dec 2029)")
ws.cell(row=r, column=1, value=(
    "Three realistic plans are modeled side by side on Debt (Assumed) / Returns (Assumed): (1) sell at maturity; "
    "(2) short refinance that can be prepaid cheaply at the Year-5 sale -- a floating loan with a purchased 2-year cap, or a "
    "5-year agency fixed loan with a 5-4-3-2-1 prepayment schedule, whichever has the lower financing cost; (3) the prior "
    "10-year agency fixed refinance, kept as a comparison row only. The selector below picks the base case.")).font = NOTE
r += 1
A['a_plan'] = inp(ws, r, "Scenario A Exit Plan (1 = sell at maturity; 2 = short refi, cheaper of floating/5-yr fixed; 3 = 10-yr fixed refi, comparison)", 2, "0",
                  "BASE CASE = 2 (short refinance; the floating loan with a cap is the cheaper of the two). See README section 6 for why a sponsor would choose it."); r += 1
A['sofr30'] = inp(ws, r, "30-Day Average SOFR", 0.0374, PCT, "FRED series SOFR30DAYAVG, 9/29/2026: 3.739%. Held flat to the Dec-2029 refinance (no forward curve)."); r += 1
A['float_spread'] = inp(ws, r, "Floating Spread over 30-Day Average SOFR", 0.0300, PCT, "multifamily-usa.com rates page (reviewed 9/6/2026): bridge, 12-month floating + extensions, lease-up / light value-add, 'SOFR + ~275-325 bps before cap'. Midpoint used (JUDGMENT). Agency floating is not available at this size: Freddie Optigo floating minimum $10M (term sheet 4/26); Fannie SARM minimum $25M."); r += 1
A['float_rate'] = frm(ws, r, "Floating Refi All-In Rate (SOFR + spread)", f"={A['sofr30']}+{A['float_spread']}", PCT, bold=True); r += 1
A['cap_strike'] = inp(ws, r, "Rate Cap Strike (SOFR)", 0.045, PCT, "JUDGMENT: ~75 bps above today's 30-day average SOFR. The loan is sized on the capped rate (strike + spread), so DSCR holds at the worst case."); r += 1
A['cap_cost_pct'] = inp(ws, r, "2-Year Rate Cap Premium (% of loan, paid at refinance)", 0.0108, PCT, "BlueGamma SOFR cap calculator, priced 9/29/2026: 2-year cap, monthly reset, 4.50% strike, $10M notional = $108,000 (1.08% of notional). Indicative mid-market; excludes bank/broker charges. Today's price used for a cap bought in 2029."); r += 1
A['float_sizing_rate'] = frm(ws, r, "Floating Refi Sizing Rate (cap strike + spread)", f"={A['cap_strike']}+{A['float_spread']}", PCT); r += 1
A['float_io'] = inp(ws, r, "Floating Refi Interest-Only (1 = yes)", 1, "0", "JUDGMENT: bridge-style floating loans are normally interest-only."); r += 1
A['float_prepay'] = inp(ws, r, "Floating Refi Prepayment Premium at Sale (%)", 0.0, PCT1, "JUDGMENT: bridge loans are typically open after a 12-month minimum-interest period; the sale is in loan year 2."); r += 1
A['ust5'] = inp(ws, r, "5-Year Treasury Yield", 0.0506, PCT, "FRED series DGS5, 9/28/2026. Held flat."); r += 1
A['rate5'] = frm(ws, r, "5-Year Agency Fixed Rate (5-yr UST + agency spread)", f"={A['ust5']}+{A['agency_spread']}", PCT, "Uses the same 200 bps agency spread judgment as the 10-year loan. The multifamily-usa.com page shows 5-year agency spreads ~30 bps wider than 10-year for stabilized assets; not added.", bold=True); r += 1
A['prepay5'] = []
for i, v in enumerate([0.05, 0.04, 0.03, 0.02, 0.01], start=1):
    note = "Fannie Mae Declining Prepayment Premium, 5-year fixed structure 5-4-3-2-1, no lockout (term sheet). Sale is in loan year 2 -> 4%." if i == 1 else None
    A['prepay5'].append(inp(ws, r, f"5-Year Fixed Prepayment Premium, Loan Year {i}", v, PCT1, note)); r += 1
A['prepay5_range'] = f"{A['prepay5'][0]}:{A['prepay5'][-1].split('!')[1]}"
r += 1

r = section(ws, r, "HOLD & EXIT")
A['hold_years'] = frm(ws, r, "Hold Period (years) -- STRUCTURAL, not a live input", 5, "0", "The model is built for a 5-year hold (5 cash-flow columns, exit on Year-6 forward NOI). Changing this cell does NOT change the model -- shown black, not blue, for that reason."); r += 1
A['exit_anchor'] = inp(ws, r, "Exit Cap — Market Anchor (Fort Lauderdale multifamily average)", 0.056, PCT, "Matthews, Fort Lauderdale Multifamily Market Report Q3 2025 (pub. 11/20/2025): average cap rate 5.6%, $283K/unit. Cross-check: Colliers South Florida Multifamily Q1 2026 (4/24/2026): cap rates 'near 5.0%' (all classes, tri-county). Used the higher, Broward-specific figure. NOT this deal's own cap rate."); r += 1
A['exit_vintage'] = inp(ws, r, "Exit Cap — Spread for Class C / 1958 Vintage at Exit", 0.010, PCT, "JUDGMENT. Market averages are dominated by newer stock; at exit this will be a ~73-year-old Class C building. CBRE's H1 2026 Cap Rate Survey (8/12/2026) reports expectations for cap-rate expansion are strongest for Class C, but its market-level tables are gated, so no sourced Class C spread is available. Named comps checked: Cascades at the Hammocks (Miami-Dade, 264 units, 1988, $65.5M / $248,106/unit, May 2026, Freddie loans assumed) and Savona Grand (Palm Beach County, 214 units, bought by American Landmark July 2026) -- neither has a publicly reported price-and-NOI pair, so no implied cap is available."); r += 1
A['exit_cap'] = frm(ws, r, "EXIT CAP RATE (base case) = market anchor + vintage spread", f"={A['exit_anchor']}+{A['exit_vintage']}", PCT, "Direct input, not tied to entry. Sensitivity tables run it +/-100 bps. Also used as the lender's cap rate for the refinance appraisal.", bold=True); r += 1
A['cost_of_sale_exit'] = inp(ws, r, "Cost of Sale at Exit (%)", 0.02, PCT1); r += 1
r += 1

r = section(ws, r, "SENSITIVITY AXES (step sizes; each grid runs the base case +/- 2 steps)")
A['sens_exit_step'] = inp(ws, r, "Sensitivity Step — Exit Cap (per step)", 0.005, PCT, "2 steps = +/-100 bps"); r += 1
A['sens_price_step'] = inp(ws, r, "Sensitivity Step — Purchase Price (% per step)", 0.05, PCT1); r += 1
A['sens_growth_step'] = inp(ws, r, "Sensitivity Step — Market Rent Growth (added to every year, per step)", 0.005, PCT); r += 1
A['sens_cost_step'] = inp(ws, r, "Sensitivity Step — Renovation Cost (% per step)", 0.10, PCT1); r += 1
A['sens_prem_step'] = inp(ws, r, "Sensitivity Step — Renovation Premium ($/month per step; grid runs base + 0..4 steps)", 50, USDC); r += 1
r += 1

r = section(ws, r, "WATERFALL")
A['pref'] = inp(ws, r, "Preferred Return % (on ALL investor capital: LP + GP co-invest, pari passu)", 0.08, PCT1); r += 1
A['tier2_lp'] = inp(ws, r, "Tier 2 Investor Share (LP + GP co-invest, pro rata)", 0.70, PCT1); r += 1
A['tier2_gp'] = inp(ws, r, "Tier 2 GP Promote", 0.30, PCT1); r += 1
A['tier2_hurdle'] = inp(ws, r, "Tier 2 IRR Hurdle (measured on investor capital)", 0.12, PCT1); r += 1
A['tier3_lp'] = inp(ws, r, "Tier 3 Investor Share (LP + GP co-invest, pro rata)", 0.50, PCT1); r += 1
A['tier3_gp'] = inp(ws, r, "Tier 3 GP Promote", 0.50, PCT1); r += 1
A['gp_coinvest'] = inp(ws, r, "GP Co-Invest % (pari passu with LP; no fees modeled)", 0.10, PCT1); r += 1

print("Assumptions built through row", r)

# =====================================================================
# 2. UNIT MIX / RENT ROLL
# =====================================================================
um = sheet("Unit Mix")
colwidths(um, [16, 11, 11, 11, 9, 13, 15, 13])
r = 1
r = title(um, r, "UNIT MIX / RENT ROLL — 97 units (Broward Property Appraiser); 1BR/1BA reduced 52 -> 51, see note")
um.cell(row=r, column=1, value="75% of units already renovated by prior owner (LoopNet/Crexi). Classic-unit counts below are a proportional allocation of that disclosed 75/25 split across unit types — judgment, not unit-type-level disclosed data. FLAG: total = 97 per Broward Property Appraiser (20 + 18 + 59 units on 3 folios). The listing breakdown (19/52/17/10) sums to 98, so one 1BR/1BA unit (the most common type) was removed, taken from the renovated count. Replace with the actual rent roll.").font = NOTE
r += 2

hdr_row = r
headers = ["Unit Type", "Total Units", "Classic Units", "Renovated Units", "Avg SF",
           "Classic In-Place Rent/mo", "Renovated In-Place Rent/mo", "Market Rent/mo (at close)"]
for i, h in enumerate(headers, start=1):
    c = um.cell(row=hdr_row, column=i, value=h)
    c.font = BOLD
r += 1
data_start = r
types = [
    ("Studio", 19, 5, 645, 1275, 1550),
    ("1BR/1BA", 51, 13, 685, 1475, 1780),  # listing breakdown says 52; -1 so total = 97 per BCPA
    ("2BR/1BA", 17, 4, 740, 1700, 2050),
    ("2BR/2BA", 10, 2, 740, 1825, 2200),
]
UM = {'rows': []}
for name, total, classic, sf, in_place, market in types:
    um.cell(row=r, column=1, value=name)
    tc = um.cell(row=r, column=2, value=total); tc.font = BLUE; tc.number_format = "0"
    cc = um.cell(row=r, column=3, value=classic); cc.font = BLUE; cc.number_format = "0"
    rc = um.cell(row=r, column=4, value=f"=B{r}-C{r}"); rc.number_format = "0"
    sfc = um.cell(row=r, column=5, value=sf); sfc.font = BLUE; sfc.number_format = "0"
    ipc = um.cell(row=r, column=6, value=in_place); ipc.font = BLUE; ipc.number_format = USDC
    rrc = um.cell(row=r, column=7, value=f"=F{r}+{A['reno_headstart']}*(H{r}-F{r})")
    rrc.number_format = USDC
    mrc = um.cell(row=r, column=8, value=market); mrc.font = BLUE; mrc.number_format = USDC
    UM['rows'].append(r)
    r += 1
total_row = r
um.cell(row=total_row, column=1, value="TOTAL / WEIGHTED AVG").font = BOLD
um.cell(row=total_row, column=2, value=f"=SUM(B{data_start}:B{r-1})").font = BOLD
um.cell(row=total_row, column=2).number_format = "0"
um.cell(row=total_row, column=3, value=f"=SUM(C{data_start}:C{r-1})").font = BOLD
um.cell(row=total_row, column=3).number_format = "0"
um.cell(row=total_row, column=4, value=f"=SUM(D{data_start}:D{r-1})").font = BOLD
um.cell(row=total_row, column=4).number_format = "0"
UM['total_row'] = total_row
UM['data_start'] = data_start
UM['data_end'] = r - 1
r = total_row + 2

r = section(um, r, "RENOVATION CAPEX BY TYPE (classic units only)", span=4)
hdr2 = r
for i, h in enumerate(["Unit Type", "Classic Units", "Cost/Unit", "Total Cost"], start=1):
    um.cell(row=hdr2, column=i, value=h).font = BOLD
r += 1
capex_start = r
for row_i in UM['rows']:
    tname = um.cell(row=row_i, column=1).value
    um.cell(row=r, column=1, value=tname)
    um.cell(row=r, column=2, value=f"=C{row_i}").number_format = "0"
    um.cell(row=r, column=3, value=f"={A['reno_per_unit']}").number_format = USDC
    um.cell(row=r, column=4, value=f"=B{r}*C{r}").number_format = USDC
    r += 1
capex_end = r - 1
UM['capex_total_row'] = r
um.cell(row=r, column=1, value="TOTAL").font = BOLD
um.cell(row=r, column=4, value=f"=SUM(D{capex_start}:D{capex_end})").font = BOLD
um.cell(row=r, column=4).number_format = USDC
UM['reno_total_addr'] = f"'Unit Mix'!$D${r}"
UM['classic_total_addr'] = f"'Unit Mix'!$C${total_row}"
r += 2

print("Unit Mix built through row", r, "| reno total:", UM['reno_total_addr'])
_units_cell = A['units'].split('!')[1].replace('$', '')
wb["Assumptions"][_units_cell] = f"='Unit Mix'!$B${UM['total_row']}"
wb["Assumptions"][_units_cell].font = BOLD

# =====================================================================
# 3. OPERATING MODEL (annual, 10 years)
# =====================================================================
op = sheet("Operating Model")
NYEARS = 10
YEAR_COLS = list(range(2, 2 + NYEARS))  # B..K
colwidths(op, [34] + [11] * NYEARS)
r = 1
r = title(op, r, "OPERATING MODEL — Annual, 10 Years (property-level, debt-agnostic: identical under Scenario A and B)")
r += 1

yr_row = r
op.cell(row=yr_row, column=1, value="Year").font = BOLD
for i, col in enumerate(YEAR_COLS, start=1):
    c = op.cell(row=yr_row, column=col, value=i)
    c.font = BOLD
    c.number_format = "0"
r += 1
cal_row = r
op.cell(row=cal_row, column=1, value="Calendar Year")
op.cell(row=cal_row, column=2, value=2027).number_format = "0"
op.cell(row=cal_row, column=2).font = BLUE
for col in YEAR_COLS[1:]:
    op.cell(row=cal_row, column=col, value=f"={get_column_letter(col-1)}{cal_row}+1").number_format = "0"
r += 1
grow_row = r
op.cell(row=grow_row, column=1, value="Market Rent Growth (this year)")
for i, col in enumerate(YEAR_COLS):
    op.cell(row=grow_row, column=col, value=f"={A['growth'][i]}").number_format = PCT1
r += 2

OP = {'grow_row': grow_row}

r = section(op, r, "MARKET & ACHIEVED RENT BY UNIT TYPE ($/unit/month)", span=1 + NYEARS)
type_blocks = []
for idx, row_i in enumerate(UM['rows']):
    tname = um.cell(row=row_i, column=1).value
    op.cell(row=r, column=1, value=f"{tname} — Market Rent/mo").font = BOLD
    market_row = r
    for i, col in enumerate(YEAR_COLS):
        cl = get_column_letter(col)
        if i == 0:
            f = f"='Unit Mix'!$H${row_i}*(1+{cl}${grow_row})"
        else:
            prev = get_column_letter(col - 1)
            f = f"={prev}{market_row}*(1+{cl}${grow_row})"
        op.cell(row=r, column=col, value=f).number_format = USDC
    r += 1

    op.cell(row=r, column=1, value=f"{tname} — Classic-Unit Track Rent/mo")
    classic_row = r
    for i, col in enumerate(YEAR_COLS):
        cl = get_column_letter(col)
        if i == 0:
            # Year 1: renovation program under way -- blend of in-place and renovated rent
            f = (f"='Unit Mix'!$F${row_i}*(1-{A['reno_y1_capture']})"
                 f"+({cl}{market_row}+{A['reno_premium_mo']})*{A['reno_y1_capture']}")
        else:
            # Year 2+: renovated -> market rent (+ premium, $0 in base). Prior model compounded the
            # Year-1 blend forward, so these units never reached market (bug fixed 2026-09-29).
            f = f"={cl}{market_row}+{A['reno_premium_mo']}"
        op.cell(row=r, column=col, value=f).number_format = USDC
    r += 1

    op.cell(row=r, column=1, value=f"{tname} — Prior-Renovated Track Rent/mo")
    prior_row = r
    for i, col in enumerate(YEAR_COLS):
        cl = get_column_letter(col)
        if i == 0:
            f = f"='Unit Mix'!$G${row_i}+{A['turnover_rate']}*{A['burnoff_pct']}*({cl}{market_row}-'Unit Mix'!$G${row_i})"
        else:
            prev = get_column_letter(col - 1)
            f = f"={prev}{prior_row}+{A['turnover_rate']}*{A['burnoff_pct']}*({cl}{market_row}-{prev}{prior_row})"
        op.cell(row=r, column=col, value=f).number_format = USDC
    r += 1

    type_blocks.append({'name': tname, 'row_i': row_i, 'market': market_row,
                         'classic': classic_row, 'prior': prior_row})
r += 1

r = section(op, r, "INCOME", span=1 + NYEARS)
market_gpr_row = r
ltl_row = r + 1
op.cell(row=market_gpr_row, column=1, value="Gross Potential Rent at Market (all units at market rent)").font = BOLD
op.cell(row=ltl_row, column=1, value="Less: Loss-to-Lease (in-place below market; net of renovation premium)")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    mterms = [f"'Unit Mix'!$B${tb['row_i']}*{cl}{tb['market']}" for tb in type_blocks]
    op.cell(row=market_gpr_row, column=col, value="=(" + "+".join(mterms) + ")*12").number_format = USDC
    op.cell(row=market_gpr_row, column=col).font = BOLD
    op.cell(row=ltl_row, column=col, value=f"={cl}{ltl_row + 1}-{cl}{market_gpr_row}").number_format = USDC
r += 2
gpr_row = r
op.cell(row=gpr_row, column=1, value="Gross Scheduled Rent (Market GPR less Loss-to-Lease)").font = BOLD
for col in YEAR_COLS:
    cl = get_column_letter(col)
    terms = []
    for tb in type_blocks:
        terms.append(f"'Unit Mix'!$C${tb['row_i']}*{cl}{tb['classic']}")
        terms.append(f"'Unit Mix'!$D${tb['row_i']}*{cl}{tb['prior']}")
    f = "=(" + "+".join(terms) + ")*12"
    op.cell(row=r, column=col, value=f).number_format = USDC
    op.cell(row=r, column=col).font = BOLD
r += 1

vac_row = r
op.cell(row=r, column=1, value="Less: Physical Vacancy")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"=-{cl}{gpr_row}*{A['vacancy']}").number_format = USDC
r += 1
cl_row = r
op.cell(row=r, column=1, value="Less: Credit Loss")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"=-{cl}{gpr_row}*{A['credit_loss']}").number_format = USDC
r += 1
con_row = r
op.cell(row=r, column=1, value="Less: Concessions")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"=-{cl}{gpr_row}*{A['concessions']}").number_format = USDC
r += 1
oi_row = r
op.cell(row=r, column=1, value="Plus: Other Income (laundry, fees, pet; ex-utility recovery)")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"={A['units']}*{A['other_income_mo']}*12*(1+{A['exp_growth']})^({cl}${yr_row}-1)").number_format = USDC
r += 1
rubs_row = r
op.cell(row=r, column=1, value="Plus: Utility Reimbursement (RUBS, % of owner water/sewer/trash)")
r += 1  # formulas filled in after the water/sewer and trash expense rows exist
egi_row = r
op.cell(row=r, column=1, value="Effective Gross Income (EGI)").font = BOLD
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"=SUM({cl}{gpr_row}:{cl}{rubs_row})").number_format = USDC
    op.cell(row=r, column=col).font = BOLD
r += 1
OP.update(gpr_row=gpr_row, egi_row=egi_row, market_gpr_row=market_gpr_row, ltl_row=ltl_row,
          vac_row=vac_row, cl_row=cl_row, con_row=con_row, oi_row=oi_row, rubs_row=rubs_row)
r += 1

r = section(op, r, "OPERATING EXPENSES", span=1 + NYEARS)
def opex_line(label, base_addr, growth_addr, row_out):
    op.cell(row=row_out, column=1, value=label)
    for col in YEAR_COLS:
        cl = get_column_letter(col)
        f = f"=-{A['units']}*{base_addr}*(1+{growth_addr})^({cl}${yr_row}-1)"
        op.cell(row=row_out, column=col, value=f).number_format = USDC
    return row_out

payroll_row = opex_line("Payroll", A['payroll'], A['exp_growth'], r); r += 1
repairs_row = opex_line("Repairs & Maintenance", A['repairs'], A['exp_growth'], r); r += 1
turnover_row = opex_line("Turnover / Make-Ready", A['turnover_cost'], A['exp_growth'], r); r += 1
contract_row = opex_line("Contract Services", A['contract_svc'], A['exp_growth'], r); r += 1
util_row = opex_line("Utilities — common-area electric & vacant units", A['utilities'], A['exp_growth'], r); r += 1
ws_row = opex_line("Water & Sewer (owner-paid, city tariff)", A['ws_cost'], A['ws_growth'], r); r += 1
trash_row = opex_line("Trash (owner-paid, city rate)", A['trash_cost'], A['exp_growth'], r); r += 1
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=rubs_row, column=col, value=f"=-{A['rubs_pct']}*({cl}{ws_row}+{cl}{trash_row})").number_format = USDC

ins_row = r
op.cell(row=r, column=1, value="Insurance")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    base = f"IF({A['roof_toggle']}=1,{A['insurance_roof']},{A['insurance_base']})"
    f = f"=-{A['units']}*({base})*(1+{A['ins_growth']})^({cl}${yr_row}-1)"
    op.cell(row=r, column=col, value=f).number_format = USDC
r += 1

tax_row = r
op.cell(row=r, column=1, value="Property Tax (reassessed at purchase; grows with just value)")
for i, col in enumerate(YEAR_COLS):
    cl = get_column_letter(col)
    if i == 0:
        f = f"=-{A['buyer_tax_y1']}"
    else:
        prev = get_column_letter(col - 1)
        f = f"={prev}{tax_row}*(1+{A['tax_growth']})"
    op.cell(row=r, column=col, value=f).number_format = USDC
r += 1
nav_row = opex_line("Non-Ad Valorem Assessments (fire etc., per unit)", A['nav'], A['exp_growth'], r); r += 1

mgmt_row = r
op.cell(row=r, column=1, value="Management Fee (% of EGI)")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"=-{cl}{egi_row}*{A['mgmt_fee_pct']}").number_format = USDC
r += 1
ga_row = opex_line("G&A / Admin", A['ga'], A['exp_growth'], r); r += 1
mktg_row = opex_line("Marketing", A['marketing'], A['exp_growth'], r); r += 1

opex_total_row = r
op.cell(row=r, column=1, value="Total Operating Expenses").font = BOLD
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"=SUM({cl}{payroll_row}:{cl}{mktg_row})").number_format = USDC
    op.cell(row=r, column=col).font = BOLD
r += 2

noi_row = r
op.cell(row=r, column=1, value="NET OPERATING INCOME (NOI)").font = BOLD
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"={cl}{egi_row}+{cl}{opex_total_row}").number_format = USDC
    op.cell(row=r, column=col).font = BOLD
r += 1
noi_pretax_row = r
op.cell(row=r, column=1, value="  memo: NOI Before Property Tax (for exit valuation)")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"={cl}{noi_row}-{cl}{tax_row}").number_format = USDC
r += 2

r = section(op, r, "BELOW-NOI ITEMS", span=1 + NYEARS)
reserves_row = r
op.cell(row=r, column=1, value="Less: Replacement Reserves")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"=-{A['units']}*{A['reserves']}*(1+{A['exp_growth']})^({cl}${yr_row}-1)").number_format = USDC
r += 1

capex_row = r
op.cell(row=r, column=1, value="Less: One-Time Capex (roof scenario / recertification)")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    f = (f"=-IF({cl}${yr_row}=1,{A['roof_toggle']}*{A['roof_cost']},0)"
         f"-IF({cl}${yr_row}={A['recert_year']},{A['recert_inspect']}+{A['recert_remediation']},0)")
    op.cell(row=r, column=col, value=f).number_format = USDC
r += 1

ucf_row = r
op.cell(row=r, column=1, value="UNLEVERED CASH FLOW (before renovation capex, before debt)").font = BOLD
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"={cl}{noi_row}+{cl}{reserves_row}+{cl}{capex_row}").number_format = USDC
    op.cell(row=r, column=col).font = BOLD
r += 2

OP.update(nav_row=nav_row, payroll_row=payroll_row, repairs_row=repairs_row, turnover_row=turnover_row,
          contract_row=contract_row, util_row=util_row, ws_row=ws_row, trash_row=trash_row,
          ins_row=ins_row, tax_row=tax_row,
          mgmt_row=mgmt_row, ga_row=ga_row, mktg_row=mktg_row, opex_total_row=opex_total_row,
          noi_row=noi_row, noi_pretax_row=noi_pretax_row, reserves_row=reserves_row,
          capex_row=capex_row, ucf_row=ucf_row, yr_row=yr_row)

print("Operating Model built through row", r)

OPS = "'Operating Model'!"
noi_y1 = f"{OPS}${get_column_letter(YEAR_COLS[0])}${OP['noi_row']}"

# =====================================================================
# 4. DEBT
# =====================================================================
db = sheet("Debt")
colwidths(db, [34, 13, 13, 13, 13, 13])
r = 1
r = title(db, r, "DEBT — SCENARIO B (ALTERNATIVE): new agency fixed-rate loan, sized on the binding constraint (no circularity)")
r += 1

r = section(db, r, "SIZING", span=3)
db.cell(row=r, column=1, value="Year 1 NOI (from Operating Model)")
db.cell(row=r, column=3, value=f"={noi_y1}").number_format = USDC
noi_y1_ref = f"'Debt'!$C${r}"
r += 1
const_row = r
db.cell(row=r, column=1, value="Annual Mortgage Constant (fixed rate, full amortization)")
db.cell(row=r, column=3, value=f"=-PMT({A['rate']},{A['amort_years']},1)").number_format = "0.0000%"
const_addr = f"'Debt'!$C${const_row}"
r += 1
loan_ltv_row = r
db.cell(row=r, column=1, value="Loan Amount — LTV Constraint")
db.cell(row=r, column=3, value=f"={A['price']}*{A['ltv']}").number_format = USDC
r += 1
loan_dscr_row = r
db.cell(row=r, column=1, value="Loan Amount — DSCR Constraint (amortizing debt service)")
db.cell(row=r, column=3, value=f"={noi_y1_ref}/({A['min_dscr']}*{const_addr})").number_format = USDC
r += 1
loan_row = r
db.cell(row=r, column=1, value="SIZED LOAN AMOUNT (binding = minimum)").font = BOLD
db.cell(row=r, column=3, value=f"=MIN(C{loan_ltv_row},C{loan_dscr_row})").number_format = USDC
db.cell(row=r, column=3).font = BOLD
loan_addr = f"'Debt'!$C${loan_row}"
r += 1
bind_row = r
db.cell(row=r, column=1, value="Binding Constraint")
db.cell(row=r, column=3, value=f'=IF(C{loan_row}=C{loan_ltv_row},"LTV","DSCR")')
r += 1
db.cell(row=r, column=1, value="Resulting LTV")
db.cell(row=r, column=3, value=f"={loan_addr}/{A['price']}").number_format = PCT1
r += 1
db.cell(row=r, column=1, value="Resulting Debt Yield (memo; agencies do not size on it)")
db.cell(row=r, column=3, value=f"={noi_y1_ref}/{loan_addr}").number_format = PCT1
r += 1
dscr1_row = r
db.cell(row=r, column=1, value="Resulting DSCR (Year 1)")
r += 2

r = section(db, r, "AMORTIZATION SCHEDULE (Years 1-5, matching the hold period)", span=6)
hdr = r
for i, h in enumerate(["Year", "Beg. Balance", "Interest", "Principal", "Debt Service", "End Balance"], start=1):
    db.cell(row=hdr, column=i, value=h).font = BOLD
r += 1
pmt_formula = f"=-PMT({A['rate']},{A['amort_years']},{loan_addr})"
db.cell(row=r, column=1, value="Annual P&I Payment (post-IO)")
db.cell(row=r, column=2, value=pmt_formula).number_format = USDC
pi_addr = f"'Debt'!$B${r}"
r += 1
amort_start = r  # first Year-1..5 data row -- must point HERE, not at the P&I payment label row above
for y in range(1, 6):
    db.cell(row=r, column=1, value=y).number_format = "0"
    if y == 1:
        db.cell(row=r, column=2, value=f"={loan_addr}").number_format = USDC
    else:
        db.cell(row=r, column=2, value=f"=F{r-1}").number_format = USDC
    db.cell(row=r, column=3, value=f"=B{r}*{A['rate']}").number_format = USDC
    # IO period read from Assumptions (was a hardcoded 2 -- a typed number in a formula tab)
    db.cell(row=r, column=4, value=f"=IF(A{r}<={A['io_years']},0,{pi_addr}-C{r})").number_format = USDC
    db.cell(row=r, column=5, value=f"=C{r}+D{r}").number_format = USDC
    db.cell(row=r, column=6, value=f"=B{r}-D{r}").number_format = USDC
    r += 1
amort_end = r - 1
db.cell(row=dscr1_row, column=3, value=f"={noi_y1_ref}/E{amort_start}").number_format = "0.00\"x\""
r += 1
prepay_b_row = r
db.cell(row=r, column=1, value="Prepayment Premium % at Sale (loan year = hold period)")
db.cell(row=r, column=3, value=f"=INDEX({A['prepay_range']},{A['hold_years']})").number_format = PCT1
prepay_b_addr = f"'Debt'!$C${r}"
r += 1
DEBT = dict(loan_addr=loan_addr, amort_start=amort_start, amort_end=amort_end,
            bind_row=bind_row, loan_ltv_row=loan_ltv_row,
            loan_dscr_row=loan_dscr_row, loan_row=loan_row, noi_y1_ref=noi_y1_ref,
            const_addr=const_addr, prepay_b_addr=prepay_b_addr)

print("Debt built through row", r, "| loan:", loan_addr)
wb.save("model_wip.xlsx")

# =====================================================================
# 5. CAPITAL (Sources & Uses)
# =====================================================================
cap = sheet("Capital")
colwidths(cap, [34, 15, 15])
r = 1
r = title(cap, r, "CAPITAL — Sources & Uses, SCENARIO B (ALTERNATIVE: new debt). Scenario A S&U is on Returns (Assumed).")
r += 1

r = section(cap, r, "USES", span=2)
u1 = r; cap.cell(row=r, column=1, value="Purchase Price"); cap.cell(row=r, column=2, value=f"={A['price']}").number_format = USDC; r += 1
u2 = r; cap.cell(row=r, column=1, value="Closing Costs"); cap.cell(row=r, column=2, value=f"={A['closing_cost']}").number_format = USDC; r += 1
u3 = r; cap.cell(row=r, column=1, value="Renovation Capex (24 classic units)"); cap.cell(row=r, column=2, value=f"={UM['reno_total_addr']}").number_format = USDC; r += 1
uses_total_row = r
cap.cell(row=r, column=1, value="TOTAL USES").font = BOLD
cap.cell(row=r, column=2, value=f"=SUM(B{u1}:B{u3})").font = BOLD
cap.cell(row=r, column=2).number_format = USDC
uses_total_addr = f"'Capital'!$B${uses_total_row}"
r += 2

r = section(cap, r, "SOURCES", span=2)
s1 = r; cap.cell(row=r, column=1, value="Senior Loan (sized on Debt tab)"); cap.cell(row=r, column=2, value=f"={DEBT['loan_addr']}").number_format = USDC; r += 1
s2 = r; cap.cell(row=r, column=1, value="Sponsor Equity (plug)"); cap.cell(row=r, column=2, value=f"={uses_total_addr}-B{s1}").number_format = USDC
equity_addr = f"'Capital'!$B${s2}"
r += 1
sources_total_row = r
cap.cell(row=r, column=1, value="TOTAL SOURCES").font = BOLD
cap.cell(row=r, column=2, value=f"=SUM(B{s1}:B{s2})").font = BOLD
cap.cell(row=r, column=2).number_format = USDC
sources_total_addr = f"'Capital'!$B${sources_total_row}"
r += 2

r = section(cap, r, "EQUITY SPLIT", span=2)
lp_eq_row = r
cap.cell(row=r, column=1, value="LP Equity"); cap.cell(row=r, column=2, value=f"={equity_addr}*(1-{A['gp_coinvest']})").number_format = USDC
lp_eq_addr = f"'Capital'!$B${lp_eq_row}"
r += 1
gp_eq_row = r
cap.cell(row=r, column=1, value="GP Equity (co-invest)"); cap.cell(row=r, column=2, value=f"={equity_addr}*{A['gp_coinvest']}").number_format = USDC
gp_eq_addr = f"'Capital'!$B${gp_eq_row}"
r += 1

r += 1
chk_row = r
cap.cell(row=r, column=1, value="CHECK: Sources - Uses")
cap.cell(row=r, column=2, value=f"={sources_total_addr}-{uses_total_addr}").number_format = USDC
cap_check_addr = f"'Capital'!$B${chk_row}"

CAP = dict(uses_total_addr=uses_total_addr, sources_total_addr=sources_total_addr,
           equity_addr=equity_addr, lp_eq_addr=lp_eq_addr, gp_eq_addr=gp_eq_addr,
           cap_check_addr=cap_check_addr)
print("Capital built through row", r, "| equity:", equity_addr)
wb.save("model_wip.xlsx")

# =====================================================================
# 6. RETURNS
# =====================================================================
rt = sheet("Returns")
HOLD = 5
RCOLS = list(range(3, 3 + HOLD))  # C..G = Year1..Year5; column B reserved for Year 0
colwidths(rt, [38, 13] + [13] * HOLD)
r = 1
r = title(rt, r, "RETURNS — Unlevered (debt-agnostic) & Levered SCENARIO B (ALTERNATIVE: new debt), 5-Year Hold")
r += 1

# =====================================================================
# NOI BRIDGE — broker-stated -> true Day-0 in-place -> Year-1 forward
# Built live so the "in-place" cap rate is a real, auditable formula,
# not just report prose. Day-0 uses Unit Mix's raw in-place rents
# directly (F/G columns) with NO market-rent growth, NO loss-to-lease
# burn-off, and NO renovation-premium capture -- i.e. what the property
# actually collects on day one, before any of the business plan's own
# value creation. Everything non-revenue (fixed $/unit opex lines,
# reassessed property tax) is identical to Year 1 already, since none
# of those lines depend on the rent-growth/burn-off/capture engine.
# =====================================================================
r = section(rt, r, "NOI BRIDGE — Broker-Stated -> True In-Place (Day 0) -> Year-1 Forward", span=2)
rt.cell(row=r, column=1, value=(
    "Day-0 = raw in-place rents from Unit Mix, no growth/burn-off/renovation credit. "
    "Year-1 Forward = the Operating Model's Year-1 column (includes a partial year of business-plan execution). "
    "These are two different concepts; only Day-0 is a conventional 'going-in' NOI.")).font = NOTE
r += 1

day0_gpr_row = r
rt.cell(row=r, column=1, value="Day-0 Gross Potential Rent (raw in-place, no growth/burnoff/capture)")
day0_gpr_f = (f"=(SUMPRODUCT('Unit Mix'!$C${UM['data_start']}:$C${UM['data_end']},"
              f"'Unit Mix'!$F${UM['data_start']}:$F${UM['data_end']})"
              f"+SUMPRODUCT('Unit Mix'!$D${UM['data_start']}:$D${UM['data_end']},"
              f"'Unit Mix'!$G${UM['data_start']}:$G${UM['data_end']}))*12")
rt.cell(row=r, column=2, value=day0_gpr_f).number_format = USDC
day0_gpr_addr = f"'Returns'!$B${r}"
r += 1
day0_vac_row = r
rt.cell(row=r, column=1, value="Less: Physical Vacancy")
rt.cell(row=r, column=2, value=f"=-{day0_gpr_addr}*{A['vacancy']}").number_format = USDC
r += 1
day0_cl_row = r
rt.cell(row=r, column=1, value="Less: Credit Loss")
rt.cell(row=r, column=2, value=f"=-{day0_gpr_addr}*{A['credit_loss']}").number_format = USDC
r += 1
day0_con_row = r
rt.cell(row=r, column=1, value="Less: Concessions")
rt.cell(row=r, column=2, value=f"=-{day0_gpr_addr}*{A['concessions']}").number_format = USDC
r += 1
day0_oi_row = r
rt.cell(row=r, column=1, value="Plus: Other Income + Utility Reimbursement (Year-1 levels)")
day0_oi_expr = f"({OPS}$B${OP['oi_row']}+{OPS}$B${OP['rubs_row']})"
rt.cell(row=r, column=2, value=f"={day0_oi_expr}").number_format = USDC
r += 1
day0_egi_row = r
rt.cell(row=r, column=1, value="Day-0 Effective Gross Income").font = BOLD
rt.cell(row=r, column=2, value=f"=SUM(B{day0_gpr_row}:B{day0_oi_row})").font = BOLD
rt.cell(row=r, column=2).number_format = USDC
day0_egi_addr = f"'Returns'!$B${day0_egi_row}"
r += 1
day0_fixedopex_row = r
rt.cell(row=r, column=1, value="Fixed Opex Lines (payroll..marketing, ex-mgmt-fee -- identical to Year 1, no growth applied in Year 1)")
fixed_opex_terms = "+".join([f"{OPS}$B${OP[k]}" for k in
                              ["payroll_row", "repairs_row", "turnover_row", "contract_row",
                               "util_row", "ws_row", "trash_row", "ins_row", "tax_row", "nav_row", "ga_row", "mktg_row"]])
rt.cell(row=r, column=2, value=f"={fixed_opex_terms}").number_format = USDC
r += 1
day0_mgmt_row = r
rt.cell(row=r, column=1, value="Management Fee (3.5% of Day-0 EGI)")
rt.cell(row=r, column=2, value=f"=-{day0_egi_addr}*{A['mgmt_fee_pct']}").number_format = USDC
r += 1
day0_noi_row = r
rt.cell(row=r, column=1, value="DAY-0 IN-PLACE NOI (reassessed-tax basis)").font = BOLD
rt.cell(row=r, column=2, value=f"={day0_egi_addr}+B{day0_fixedopex_row}+B{day0_mgmt_row}").font = BOLD
rt.cell(row=r, column=2).number_format = USDC
day0_noi_addr = f"'Returns'!$B${day0_noi_row}"
r += 2

r = section(rt, r, "Decomposition of the gap to Year-1 Forward NOI (each effect isolated via live counterfactual, not estimated)", span=2)
rt.cell(row=r, column=1, value=(
    "Counterfactual S2 = burn-off ON (55% turnover x 50% burn-off, on the 73 prior-renovated units, toward "
    "Year-1's growth-adjusted market rent) but renovation-premium capture OFF (24 classic units stay at raw "
    "in-place). Isolates the burn-off effect cleanly because market-rent growth only enters Year-1 GPR THROUGH "
    "the burn-off and capture mechanisms -- with both off, growth alone has zero effect on Year-1 (verified).")).font = NOTE
r += 1

s2_classic_sum = f"SUMPRODUCT('Unit Mix'!$C${UM['data_start']}:$C${UM['data_end']},'Unit Mix'!$F${UM['data_start']}:$F${UM['data_end']})"
s2_renov_terms = []
for tb in type_blocks:
    row_i = tb['row_i']; market_row = tb['market']
    term = (f"'Unit Mix'!$D${row_i}*('Unit Mix'!$G${row_i}+{A['turnover_rate']}*{A['burnoff_pct']}"
            f"*({OPS}$B${market_row}-'Unit Mix'!$G${row_i}))")
    s2_renov_terms.append(term)
s2_gpr_row = r
rt.cell(row=r, column=1, value="  S2 GPR: Day-0 classic (raw in-place) + burn-off-adjusted prior-renovated tracks")
rt.cell(row=r, column=2, value=f"=({s2_classic_sum}+{'+'.join(s2_renov_terms)})*12").number_format = USDC
s2_gpr_addr = f"'Returns'!$B${s2_gpr_row}"
r += 1
s2_egi_row = r
rt.cell(row=r, column=1, value="  S2 EGI (same vacancy/credit-loss/concessions/%/other-income rates as Day-0)")
rt.cell(row=r, column=2,
        value=f"={s2_gpr_addr}*(1-{A['vacancy']}-{A['credit_loss']}-{A['concessions']})+{day0_oi_expr}").number_format = USDC
s2_egi_addr = f"'Returns'!$B${s2_egi_row}"
r += 1
s2_noi_row = r
rt.cell(row=r, column=1, value="  S2 NOI (Day-0 fixed opex + mgmt fee on S2 EGI)")
rt.cell(row=r, column=2, value=f"={s2_egi_addr}+B{day0_fixedopex_row}-{s2_egi_addr}*{A['mgmt_fee_pct']}").number_format = USDC
s2_noi_addr = f"'Returns'!$B${s2_noi_row}"
r += 2

b_day0_row = r
rt.cell(row=r, column=1, value="  Day-0 In-Place NOI")
rt.cell(row=r, column=2, value=f"={day0_noi_addr}").number_format = USDC
r += 1
b_burnoff_row = r
rt.cell(row=r, column=1, value="  + Loss-to-lease burn-off effect (isolated: S2 NOI - Day-0 NOI)")
rt.cell(row=r, column=2, value=f"={s2_noi_addr}-{day0_noi_addr}").number_format = USDC
r += 1
b_capture_row = r
rt.cell(row=r, column=1, value="  + Renovation-premium partial-year capture effect (isolated: Year-1 actual - S2 NOI)")
rt.cell(row=r, column=2, value=f"={noi_y1}-{s2_noi_addr}").number_format = USDC
r += 1
b_y1_row = r
rt.cell(row=r, column=1, value="  = YEAR-1 FORWARD NOI (Operating Model, ties out exactly)").font = BOLD
rt.cell(row=r, column=2, value=f"=B{b_day0_row}+B{b_burnoff_row}+B{b_capture_row}").font = BOLD
rt.cell(row=r, column=2).number_format = USDC
r += 2

r = section(rt, r, "CAP RATE, THREE WAYS", span=2)
cap_broker_row = r
rt.cell(row=r, column=1, value="1. Broker-Stated Cap Rate (seller's current tax basis)")
rt.cell(row=r, column=2, value=f"={A['broker_cap']}").number_format = PCT1
r += 1
cap_inplace_row = r
rt.cell(row=r, column=1, value="2. In-Place Cap Rate, Day-0, REASSESSED tax (the true going-in number)").font = BOLD
rt.cell(row=r, column=2, value=f"={day0_noi_addr}/{A['price']}").font = BOLD
rt.cell(row=r, column=2).number_format = PCT1
cap_inplace_addr = f"'Returns'!$B${cap_inplace_row}"
r += 1
cap_y1fwd_row = r
rt.cell(row=r, column=1, value="3. Year-1 FORWARD Cap Rate (includes partial-year business plan execution -- NOT a going-in number)")
rt.cell(row=r, column=2, value=f"={noi_y1}/{A['price']}").number_format = PCT1
r += 2

r = section(rt, r, "EXIT VALUATION — tax-adjusted", span=2)
exit_cap_base_row = r
rt.cell(row=r, column=1, value="Exit Cap Rate — base case (direct market input on Assumptions; NOT tied to this deal's entry cap)").font = BOLD
rt.cell(row=r, column=2, value=f"={A['exit_cap']}").font = BOLD
rt.cell(row=r, column=2).number_format = PCT
exit_cap_base_addr = f"'Returns'!$B${exit_cap_base_row}"
r += 1
rt.cell(row=r, column=1, value="  memo: exit cap minus in-place (Day-0) entry cap")
rt.cell(row=r, column=2, value=f"={exit_cap_base_addr}-{cap_inplace_addr}").number_format = PCT
r += 1
eff_tax_exit_row = r
rt.cell(row=r, column=1, value="Effective Tax Rate at Exit (same cost-of-sale factor as entry)")
rt.cell(row=r, column=2, value=f"={A['millage']}*{A['cos_factor']}").number_format = PCT1
eff_tax_exit_addr = f"'Returns'!$B${eff_tax_exit_row}"
r += 1
fwd_noi_row = r
rt.cell(row=r, column=1, value="Forward NOI Before Property Tax (Year 6, for exit)")
y6_col = get_column_letter(YEAR_COLS[5])
rt.cell(row=r, column=2, value=f"={OPS}${y6_col}${OP['noi_pretax_row']}").number_format = USDC
fwd_noi_addr = f"'Returns'!$B${fwd_noi_row}"
r += 1
exit_price_row = r
rt.cell(row=r, column=1, value="EXIT PRICE = Fwd NOI pretax / (Exit Cap + Eff. Tax Rate)").font = BOLD
rt.cell(row=r, column=2, value=f"={fwd_noi_addr}/({exit_cap_base_addr}+{eff_tax_exit_addr})").font = BOLD
rt.cell(row=r, column=2).number_format = USDC
exit_price_addr = f"'Returns'!$B${exit_price_row}"
r += 1
cos_exit_row = r
rt.cell(row=r, column=1, value="Less: Cost of Sale")
rt.cell(row=r, column=2, value=f"=-{exit_price_addr}*{A['cost_of_sale_exit']}").number_format = USDC
cos_exit_addr = f"'Returns'!$B${cos_exit_row}"
r += 1
payoff_row = r
rt.cell(row=r, column=1, value="Less: Loan Payoff (Scenario B Debt tab, End Balance Year 5)")
rt.cell(row=r, column=2, value=f"=-'Debt'!$F${DEBT['amort_end']}").number_format = USDC
payoff_addr = f"'Returns'!$B${payoff_row}"
r += 1
prepay_b_row = r
rt.cell(row=r, column=1, value="Less: Prepayment Premium (Scenario B, declining schedule, loan year 5)")
rt.cell(row=r, column=2, value=f"={payoff_addr}*{DEBT['prepay_b_addr']}").number_format = USDC
r += 1
net_proceeds_row = r
rt.cell(row=r, column=1, value="NET SALE PROCEEDS TO EQUITY — SCENARIO B").font = BOLD
rt.cell(row=r, column=2, value=f"={exit_price_addr}+{cos_exit_addr}+{payoff_addr}+B{prepay_b_row}").font = BOLD
rt.cell(row=r, column=2).number_format = USDC
net_proceeds_addr = f"'Returns'!$B${net_proceeds_row}"
r += 1
net_proceeds_unlev_row = r
rt.cell(row=r, column=1, value="Net Sale Proceeds, UNLEVERED (no loan payoff)")
rt.cell(row=r, column=2, value=f"={exit_price_addr}+{cos_exit_addr}").number_format = USDC
net_proceeds_unlev_addr = f"'Returns'!$B${net_proceeds_unlev_row}"
r += 2

r = section(rt, r, "CASH FLOWS ($) — Year 0 = closing, Years 1-5 = operations + exit in Year 5", span=2 + HOLD)
hdr = r
rt.cell(row=hdr, column=1, value="").font = BOLD
rt.cell(row=hdr, column=2, value="Year 0").font = BOLD
for i, col in enumerate(RCOLS, start=1):
    rt.cell(row=hdr, column=col, value=f"Year {i}").font = BOLD
r += 1

ucf_row_rt = r
rt.cell(row=r, column=1, value="Unlevered CF (NOI + reserves + roof/recert capex)")
for i, col in enumerate(RCOLS):
    opcol = get_column_letter(YEAR_COLS[i])
    rt.cell(row=r, column=col, value=f"={OPS}${opcol}${OP['ucf_row']}").number_format = USDC
r += 1
unlev_total_row = r
rt.cell(row=r, column=1, value="+ Net Sale Proceeds (Year 5 only, unlevered)")
for i, col in enumerate(RCOLS):
    if i == HOLD - 1:
        rt.cell(row=r, column=col, value=f"={net_proceeds_unlev_addr}").number_format = USDC
    else:
        rt.cell(row=r, column=col, value=0).number_format = USDC
r += 1
unlev_cf_total_row = r
rt.cell(row=r, column=1, value="TOTAL UNLEVERED CASH FLOW TO EQUITY").font = BOLD
for col in RCOLS:
    cl = get_column_letter(col)
    rt.cell(row=r, column=col, value=f"={cl}{ucf_row_rt}+{cl}{unlev_total_row}").font = BOLD
    rt.cell(row=r, column=col).number_format = USDC
r += 1

debt_svc_row = r
rt.cell(row=r, column=1, value="Less: Debt Service (Scenario B)")
for i, col in enumerate(RCOLS):
    dbrow = DEBT['amort_start'] + i
    rt.cell(row=r, column=col, value=f"=-'Debt'!$E${dbrow}").number_format = USDC
r += 1
lev_before_exit_row = r
rt.cell(row=r, column=1, value="Levered CF from Operations (Scenario B)")
for col in RCOLS:
    cl = get_column_letter(col)
    rt.cell(row=r, column=col, value=f"={cl}{ucf_row_rt}+{cl}{debt_svc_row}").number_format = USDC
r += 1
lev_exit_row = r
rt.cell(row=r, column=1, value="+ Net Sale Proceeds (Year 5 only, levered, Scenario B)")
for i, col in enumerate(RCOLS):
    if i == HOLD - 1:
        rt.cell(row=r, column=col, value=f"={net_proceeds_addr}").number_format = USDC
    else:
        rt.cell(row=r, column=col, value=0).number_format = USDC
r += 1
lev_cf_total_row = r
rt.cell(row=r, column=1, value="TOTAL LEVERED CASH FLOW TO EQUITY — SCENARIO B").font = BOLD
for col in RCOLS:
    cl = get_column_letter(col)
    rt.cell(row=r, column=col, value=f"={cl}{lev_before_exit_row}+{cl}{lev_exit_row}").font = BOLD
    rt.cell(row=r, column=col).number_format = USDC
r += 2

r = section(rt, r, "RETURNS SUMMARY", span=2)
inv_row = r
rt.cell(row=r, column=1, value="Total Equity Invested (Year 0, Scenario B)")
rt.cell(row=r, column=2, value=f"={CAP['equity_addr']}").number_format = USDC
r += 1
uses_row = r
rt.cell(row=r, column=1, value="Total Uses, All-Cash (Year 0, unlevered basis)")
rt.cell(row=r, column=2, value=f"={CAP['uses_total_addr']}").number_format = USDC
r += 1

# Backfill Year-0 outflows into column B of the two TOTAL cash-flow rows so each
# row B:G is one contiguous IRR-ready range (Year0..Year5). No HSTACK needed.
rt.cell(row=unlev_cf_total_row, column=2, value=f"=-B{uses_row}").font = BOLD
rt.cell(row=unlev_cf_total_row, column=2).number_format = USDC
rt.cell(row=lev_cf_total_row, column=2, value=f"=-B{inv_row}").font = BOLD
rt.cell(row=lev_cf_total_row, column=2).number_format = USDC

unlev_range = f"B{unlev_cf_total_row}:{get_column_letter(RCOLS[-1])}{unlev_cf_total_row}"
lev_range = f"B{lev_cf_total_row}:{get_column_letter(RCOLS[-1])}{lev_cf_total_row}"
unlev_irr_row = r
rt.cell(row=r, column=1, value="Unlevered IRR (debt-agnostic)")
rt.cell(row=r, column=2, value=f'=IFERROR(IRR({unlev_range}),"N/A - no sign change / undefined")').number_format = PCT1
r += 1
lev_irr_row = r
rt.cell(row=r, column=1, value="Levered IRR — SCENARIO B (alternative, new debt)")
rt.cell(row=r, column=2, value=f'=IFERROR(IRR({lev_range}),"N/A - no sign change / undefined")').number_format = PCT1
r += 1
unlev_em_row = r
rt.cell(row=r, column=1, value="Unlevered Equity Multiple (debt-agnostic)")
rt.cell(row=r, column=2,
        value=f"=SUM(C{unlev_cf_total_row}:{get_column_letter(RCOLS[-1])}{unlev_cf_total_row})/B{uses_row}").number_format = "0.00\"x\""
r += 1
lev_em_row = r
rt.cell(row=r, column=1, value="Levered Equity Multiple — SCENARIO B (alternative, new debt)")
rt.cell(row=r, column=2,
        value=f"=SUM(C{lev_cf_total_row}:{get_column_letter(RCOLS[-1])}{lev_cf_total_row})/B{inv_row}").number_format = "0.00\"x\""
r += 1
peak_eq_row = r
rt.cell(row=r, column=1, value="Peak Equity, Scenario B (single close, no follow-on calls)")
rt.cell(row=r, column=2, value=f"=B{inv_row}").number_format = USDC
r += 2

r = section(rt, r, "CASH-ON-CASH BY YEAR (levered, Scenario B)", span=1 + HOLD)
coc_row = r
for i, col in enumerate(RCOLS, start=1):
    cl = get_column_letter(col)
    rt.cell(row=r, column=col, value=f"={cl}{lev_before_exit_row}/B{inv_row}").number_format = PCT1
r += 2

RET = dict(exit_cap_base_addr=exit_cap_base_addr, exit_price_addr=exit_price_addr,
           net_proceeds_addr=net_proceeds_addr, net_proceeds_unlev_addr=net_proceeds_unlev_addr,
           unlev_cf_total_row=unlev_cf_total_row, lev_before_exit_row=lev_before_exit_row,
           lev_cf_total_row=lev_cf_total_row, lev_exit_row=lev_exit_row,
           inv_row=inv_row, uses_row=uses_row, unlev_irr_row=unlev_irr_row, lev_irr_row=lev_irr_row,
           unlev_em_row=unlev_em_row, lev_em_row=lev_em_row, RCOLS=RCOLS,
           fwd_noi_addr=fwd_noi_addr, eff_tax_exit_addr=eff_tax_exit_addr,
           day0_noi_addr=day0_noi_addr, cap_inplace_addr=cap_inplace_addr,
           cap_broker_row=cap_broker_row, cap_inplace_row=cap_inplace_row, cap_y1fwd_row=cap_y1fwd_row,
           b_day0_row=b_day0_row, b_burnoff_row=b_burnoff_row, b_capture_row=b_capture_row, b_y1_row=b_y1_row)
print("Returns built through row", r)
wb.save("model_wip.xlsx")

# =====================================================================
# 6b. DEBT (ASSUMED) — Scenario A: assume the existing loan, refinance
#     at its maturity if that falls inside the hold. Fully dynamic on
#     the maturity-year assumption cell (IF-based), not hardcoded to
#     today's default of Year 3.
# =====================================================================
da = sheet("Debt (Assumed)")
DACOLS = list(range(2, 2 + HOLD))  # B..F = Year1..Year5
colwidths(da, [36] + [14] * HOLD)
r = 1
r = title(da, r, "DEBT (ASSUMED) — SCENARIO A (BASE CASE): broker-disclosed existing loan + refinance at maturity")
da.cell(row=r, column=1, value=(
    "First mortgage and supplemental loan sourced from LoopNet/Crexi (see Assumptions). Amortization/IO "
    "status is NOT disclosed for either -- Assumptions!assum_io is a labeled judgment toggle. If the first "
    "mortgage's maturity (Assumptions!assum_first_maturity_yr) falls inside the 5-year hold, the combined "
    "balance is refinanced at that point into an agency fixed-rate loan on the same terms as Scenario B "
    "(LTV on value at refinance, or DSCR on amortizing debt service, whichever binds). At closing, the lender's "
    "assumption test can force a principal paydown (Assumptions: max LTV on purchase price).")).font = NOTE
r += 2

r = section(da, r, "ASSUMPTION APPROVAL — LENDER PAYDOWN TEST AT CLOSING", span=2)
max_assum_row = r
da.cell(row=r, column=1, value="Max Assumable Balance = Purchase Price x Max LTV")
da.cell(row=r, column=2, value=f"={A['price']}*{A['assum_max_ltv']}").number_format = USDC
r += 1
assume_pd_row = r
da.cell(row=r, column=1, value="Required Paydown at Closing = MAX(0, First + Supplemental - Max)").font = BOLD
da.cell(row=r, column=2, value=f"=MAX(0,{A['assum_first_bal']}+{A['assum_supp_bal']}-B{max_assum_row})").font = BOLD
da.cell(row=r, column=2).number_format = USDC
assume_pd_addr = f"'Debt (Assumed)'!$B${r}"
r += 1
pd_supp_row = r
da.cell(row=r, column=1, value="  applied to Supplemental (6.2%) first")
da.cell(row=r, column=2, value=f"=MIN({assume_pd_addr},{A['assum_supp_bal']})").number_format = USDC
r += 1
pd_first_row = r
da.cell(row=r, column=1, value="  remainder applied to First Mortgage")
da.cell(row=r, column=2, value=f"={assume_pd_addr}-B{pd_supp_row}").number_format = USDC
r += 1
first0_row = r
da.cell(row=r, column=1, value="First Mortgage Balance Assumed")
da.cell(row=r, column=2, value=f"={A['assum_first_bal']}-B{pd_first_row}").number_format = USDC
first0 = f"'Debt (Assumed)'!$B${r}"
r += 1
da.cell(row=r, column=1, value="Supplemental Balance Assumed")
da.cell(row=r, column=2, value=f"={A['assum_supp_bal']}-B{pd_supp_row}").number_format = USDC
supp0 = f"'Debt (Assumed)'!$B${r}"
r += 2

hdr = r
da.cell(row=hdr, column=1, value="").font = BOLD
for i, col in enumerate(DACOLS, start=1):
    da.cell(row=hdr, column=col, value=f"Year {i}").font = BOLD
r += 1

mat = A['assum_first_maturity_yr']
io_flag = A['assum_io']

r = section(da, r, "FIRST MORTGAGE (pre-maturity)", span=1 + HOLD)
f_beg_row = r
da.cell(row=r, column=1, value="Beginning Balance")
for i, col in enumerate(DACOLS):
    cl = get_column_letter(col)
    if i == 0:
        f = f"={first0}"
    else:
        prev = get_column_letter(col - 1)
        f = f"=IF({OPS}${cl}${yr_row}<={mat},{prev}{f_beg_row}-{prev}{r+1},0)"  # placeholder, fixed below
    da.cell(row=r, column=col, value=f).number_format = USDC
r += 1
f_int_row = r
da.cell(row=r, column=1, value="Interest")
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"=IF({OPS}${cl}${yr_row}<={mat},{cl}{f_beg_row}*{A['assum_first_rate']},0)").number_format = USDC
r += 1
f_prin_row = r
da.cell(row=r, column=1, value="Principal (0 if IO)")
for col in DACOLS:
    cl = get_column_letter(col)
    pmt_amort = f"(-PMT({A['assum_first_rate']},{A['amort_years']},{first0})-{cl}{f_int_row})"
    da.cell(row=r, column=col, value=f"=IF({OPS}${cl}${yr_row}<={mat},IF({io_flag}=1,0,{pmt_amort}),0)").number_format = USDC
r += 1
f_end_row = r
da.cell(row=r, column=1, value="Ending Balance")
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"=IF({OPS}${cl}${yr_row}<={mat},{cl}{f_beg_row}-{cl}{f_prin_row},0)").number_format = USDC
r += 2
# fix beginning-balance formula now that f_end_row is known (row = f_beg_row+3)
for i, col in enumerate(DACOLS):
    if i == 0:
        continue
    cl = get_column_letter(col)
    prev = get_column_letter(col - 1)
    da.cell(row=f_beg_row, column=col,
            value=f"=IF({OPS}${cl}${yr_row}<={mat},IF({OPS}${prev}${yr_row}<={mat},{prev}{f_end_row},{first0}),0)")

r = section(da, r, "SUPPLEMENTAL LOAN (pre-maturity)", span=1 + HOLD)
s_beg_row = r
da.cell(row=r, column=1, value="Beginning Balance")
for i, col in enumerate(DACOLS):
    cl = get_column_letter(col)
    if i == 0:
        f = f"={supp0}"
        da.cell(row=r, column=col, value=f).number_format = USDC
r += 1
s_int_row = r
da.cell(row=r, column=1, value="Interest")
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"=IF({OPS}${cl}${yr_row}<={mat},{cl}{s_beg_row}*{A['assum_supp_rate']},0)").number_format = USDC
r += 1
s_prin_row = r
da.cell(row=r, column=1, value="Principal (0 if IO)")
for col in DACOLS:
    cl = get_column_letter(col)
    pmt_amort = f"(-PMT({A['assum_supp_rate']},{A['amort_years']},{supp0})-{cl}{s_int_row})"
    da.cell(row=r, column=col, value=f"=IF({OPS}${cl}${yr_row}<={mat},IF({io_flag}=1,0,{pmt_amort}),0)").number_format = USDC
r += 1
s_end_row = r
da.cell(row=r, column=1, value="Ending Balance")
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"=IF({OPS}${cl}${yr_row}<={mat},{cl}{s_beg_row}-{cl}{s_prin_row},0)").number_format = USDC
r += 2
for i, col in enumerate(DACOLS):
    if i == 0:
        continue
    cl = get_column_letter(col)
    prev = get_column_letter(col - 1)
    da.cell(row=s_beg_row, column=col,
            value=f"=IF({OPS}${cl}${yr_row}<={mat},IF({OPS}${prev}${yr_row}<={mat},{prev}{s_end_row},{supp0}),0)")
    da.cell(row=s_beg_row, column=col).number_format = USDC

LASTC = get_column_letter(DACOLS[-1])
HOLD_C = A['hold_years']
r = section(da, r, "ASSUMED LOANS COMBINED (through maturity)", span=1 + HOLD)
pre_ds_row = r
da.cell(row=r, column=1, value="Assumed Loans Debt Service (First + Supplemental)")
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"={cl}{f_int_row}+{cl}{f_prin_row}+{cl}{s_int_row}+{cl}{s_prin_row}").number_format = USDC
r += 1
combined_payoff_row = r
da.cell(row=r, column=1, value="Payoff Balance at Maturity (First + Supplemental)")
da.cell(row=r, column=2, value=f"=INDEX(B{f_end_row}:{LASTC}{f_end_row},{mat})+INDEX(B{s_end_row}:{LASTC}{s_end_row},{mat})").number_format = USDC
payoff_mat_addr = f"'Debt (Assumed)'!$B${r}"
r += 1
refi_noi_row = r
da.cell(row=r, column=1, value="NOI in the first post-maturity year (Operating Model, indexed on maturity year)")
da.cell(row=r, column=2, value=f"=INDEX({OPS}${get_column_letter(YEAR_COLS[0])}${OP['noi_row']}:{OPS}${get_column_letter(YEAR_COLS[-1])}${OP['noi_row']},{mat}+1)").number_format = USDC
refi_noi_addr = f"'Debt (Assumed)'!$B${r}"
r += 1
refi_value_row = r
da.cell(row=r, column=1, value="Value at Refinance = that NOI / exit cap (lender appraisal proxy; no reassessment on a refi)")
da.cell(row=r, column=2, value=f"={refi_noi_addr}/{RET['exit_cap_base_addr']}").number_format = USDC
refi_value_addr = f"'Debt (Assumed)'!$B${r}"
r += 2

VARIANTS = [
    ("float", "REFI OPTION 2a — FLOATING: 30-day Avg SOFR + spread, purchased 2-year rate cap, interest-only, open at sale",
     A['float_rate'], A['float_sizing_rate'], f"IF({A['float_io']}=1,{HOLD_C},0)", A['cap_cost_pct'], f"{A['float_prepay']}"),
    ("fixed5", "REFI OPTION 2b — 5-YEAR AGENCY FIXED: 5-yr UST + spread, 5-4-3-2-1 declining prepayment premium",
     A['rate5'], A['rate5'], A['io_years'], "0", f"IF({HOLD_C}>{mat},INDEX({A['prepay5_range']},{HOLD_C}-{mat}),0)"),
    ("fixed10", "COMPARISON ONLY — 10-YEAR AGENCY FIXED (prior structure): 10-yr UST + spread, 10-yr declining premium",
     A['rate'], A['rate'], A['io_years'], "0", f"IF({HOLD_C}>{mat},INDEX({A['prepay_range']},{HOLD_C}-{mat}),0)"),
]
V = {}
for key, title_, rate_x, size_x, io_x, up_x, pp_x in VARIANTS:
    r = section(da, r, title_, span=1 + HOLD)
    d = {'title': title_}
    def sc(label, formula, fmt=USDC, bold=False):
        global r
        c1 = da.cell(row=r, column=1, value=label)
        c = da.cell(row=r, column=2, value=formula)
        if fmt:
            c.number_format = fmt
        if bold:
            c1.font = BOLD; c.font = BOLD
        addr = f"'Debt (Assumed)'!$B${r}"
        r += 1
        return addr
    d['rate'] = sc("All-in rate", f"={rate_x}", PCT)
    d['size'] = sc("Sizing rate for the DSCR test", f"={size_x}", PCT)
    d['io'] = sc("Interest-only years after refinance", f"={io_x}", "0")
    d['ltv_leg'] = sc("Loan — LTV constraint (on value at refinance)", f"={refi_value_addr}*{A['ltv']}")
    d['dscr_leg'] = sc("Loan — DSCR constraint (amortizing payment at the sizing rate)", f"={refi_noi_addr}/({A['min_dscr']}*-PMT({d['size']},{A['amort_years']},1))")
    d['loan'] = sc("REFI LOAN AMOUNT (binding = minimum)", f"=MIN({d['ltv_leg']},{d['dscr_leg']})", bold=True)
    d['binding'] = sc("Binding constraint", f'=IF({d["loan"]}={d["ltv_leg"]},"LTV","DSCR")', None)
    d['pmt'] = sc("Annual P&I payment (after any IO period)", f"=-PMT({d['rate']},{A['amort_years']},{d['loan']})")
    d['upfront'] = sc("Upfront cost at refinance (rate cap premium)", f"={d['loan']}*{up_x}")
    d['cash_req'] = sc("Cash Required at Refinance = payoff - new loan + upfront cost", f"={payoff_mat_addr}-{d['loan']}+{d['upfront']}", bold=True)
    beg_row = r
    da.cell(row=r, column=1, value="Refi Loan Beginning Balance")
    int_row, prin_row, end_row = r + 1, r + 2, r + 3
    for i, col in enumerate(DACOLS):
        cl = get_column_letter(col)
        prev = get_column_letter(col - 1)
        f = (f"=IF({OPS}${cl}${yr_row}={mat}+1,{d['loan']},IF({OPS}${cl}${yr_row}>{mat}+1,{prev}{end_row},0))" if i > 0
             else f"=IF({OPS}${cl}${yr_row}={mat}+1,{d['loan']},0)")
        da.cell(row=beg_row, column=col, value=f).number_format = USDC
        da.cell(row=int_row, column=col, value=f"=IF({OPS}${cl}${yr_row}>{mat},{cl}{beg_row}*{d['rate']},0)").number_format = USDC
        da.cell(row=prin_row, column=col, value=(f"=IF({OPS}${cl}${yr_row}>{mat},IF(({OPS}${cl}${yr_row}-{mat})<={d['io']},0,"
                                                 f"{d['pmt']}-{cl}{int_row}),0)")).number_format = USDC
        da.cell(row=end_row, column=col, value=f"=IF({OPS}${cl}${yr_row}>{mat},{cl}{beg_row}-{cl}{prin_row},0)").number_format = USDC
    da.cell(row=int_row, column=1, value="Refi Loan Interest")
    da.cell(row=prin_row, column=1, value="Refi Loan Principal")
    da.cell(row=end_row, column=1, value="Refi Loan Ending Balance")
    r = end_row + 1
    ds_row = r
    da.cell(row=r, column=1, value="TOTAL DEBT SERVICE (assumed loans to maturity, then this refi)").font = BOLD
    for col in DACOLS:
        cl = get_column_letter(col)
        da.cell(row=r, column=col, value=f"={cl}{pre_ds_row}+{cl}{int_row}+{cl}{prin_row}").number_format = USDC
    r += 1
    d['prepay_pct'] = sc("Prepayment premium % at the Year-5 sale", f"={pp_x}", PCT1)
    d['prepay'] = sc("Prepayment premium $ at sale", f"={LASTC}{end_row}*{d['prepay_pct']}")
    d['fin_cost'] = sc("Financing cost over the refi (interest + cap premium + prepayment premium)", f"=SUM(B{int_row}:{LASTC}{int_row})+{d['upfront']}+{d['prepay']}")
    d['fin_pct'] = sc("Financing cost, % of loan per year", f"={d['fin_cost']}/{d['loan']}/({HOLD_C}-{mat})", PCT, bold=True)
    d.update(beg_row=beg_row, int_row=int_row, prin_row=prin_row, end_row=end_row, ds_row=ds_row)
    V[key] = d
    r += 1

r = section(da, r, "SELECTED REFINANCE (feeds Returns (Assumed) and the Sensitivity tab)", span=1 + HOLD)
short_choice_row = r
da.cell(row=r, column=1, value="Short-refi choice (1 = floating + cap, 2 = 5-yr fixed): lower financing cost % per year")
da.cell(row=r, column=2, value=f"=IF({V['float']['fin_pct']}<={V['fixed5']['fin_pct']},1,2)").number_format = "0"
short_choice_addr = f"'Debt (Assumed)'!$B${r}"
r += 1
sel_var_row = r
da.cell(row=r, column=1, value="Selected refi (1 = floating, 2 = 5-yr fixed, 3 = 10-yr fixed); not used when the plan is 1 (sale at maturity)")
da.cell(row=r, column=2, value=f"=IF({A['a_plan']}=3,3,{short_choice_addr})").number_format = "0"
sel_var_addr = f"'Debt (Assumed)'!$B${r}"
r += 1
SEL = {}
for k, lab, fmt in [('rate', "Selected: all-in rate", PCT), ('size', "Selected: sizing rate", PCT), ('io', "Selected: interest-only years", "0"),
                    ('upfront_pct', "Selected: upfront cost % of loan", PCT), ('prepay_pct', "Selected: prepayment premium % at sale", PCT1)]:
    src = {'rate': 'rate', 'size': 'size', 'io': 'io', 'prepay_pct': 'prepay_pct'}
    if k == 'upfront_pct':
        items = [f"{V[v]['upfront']}/{V[v]['loan']}" for v in ("float", "fixed5", "fixed10")]
    else:
        items = [V[v][src[k]] for v in ("float", "fixed5", "fixed10")]
    da.cell(row=r, column=1, value=lab)
    da.cell(row=r, column=2, value=f"=CHOOSE({sel_var_addr},{','.join(items)})").number_format = fmt
    SEL[k] = f"'Debt (Assumed)'!$B${r}"
    r += 1
r += 1

DA = dict(f_beg_row=f_beg_row, f_end_row=f_end_row, s_beg_row=s_beg_row, s_end_row=s_end_row,
          combined_payoff_row=combined_payoff_row, payoff_mat_addr=payoff_mat_addr, pre_ds_row=pre_ds_row,
          DACOLS=DACOLS, assume_pd_addr=assume_pd_addr, first0=first0, supp0=supp0,
          V=V, SEL=SEL, short_choice_addr=short_choice_addr, sel_var_addr=sel_var_addr,
          refi_noi_addr=refi_noi_addr, refi_value_addr=refi_value_addr)
print("Debt (Assumed) built through row", r)
wb.save("model_wip.xlsx")

# =====================================================================
# 6c. RETURNS (ASSUMED) — Scenario A returns, same NOI trajectory as
#     Scenario B, different debt (assumed loan + Year-3 refi).
# =====================================================================
ra = sheet("Returns (Assumed)")
colwidths(ra, [38, 13] + [13] * HOLD)
r = 1
r = title(ra, r, "RETURNS (ASSUMED DEBT) — SCENARIO A (BASE CASE): exit plans compared; base case = selected plan")
ra.cell(row=r, column=1, value=(
    "Same property, same NOI trajectory as the Scenario B (new-debt) Returns tab -- the only thing that "
    "changes here is the debt.")).font = NOTE
r += 2

r = section(ra, r, "SOURCES & USES — SCENARIO A", span=2)
a_fee_row = r
ra.cell(row=r, column=1, value="Loan Assumption Fee (on balance assumed after any required paydown)")
ra.cell(row=r, column=2, value=f"=({DA['first0']}+{DA['supp0']})*{A['assum_fee_pct']}").number_format = USDC
a_fee_addr = f"'Returns (Assumed)'!$B${a_fee_row}"
r += 1
a_uses_row = r
ra.cell(row=r, column=1, value="Total Uses (Scenario B uses + assumption fee)")
ra.cell(row=r, column=2, value=f"={CAP['uses_total_addr']}+{a_fee_addr}").number_format = USDC
a_uses_addr = f"'Returns (Assumed)'!$B${a_uses_row}"
r += 1
a_loan_row = r
ra.cell(row=r, column=1, value="Assumed Debt (First + Supplemental, after any lender-required paydown)")
ra.cell(row=r, column=2, value=f"={DA['first0']}+{DA['supp0']}").number_format = USDC
a_loan_addr = f"'Returns (Assumed)'!$B${a_loan_row}"
r += 1
a_equity_row = r
ra.cell(row=r, column=1, value="Sponsor Equity").font = BOLD
ra.cell(row=r, column=2, value=f"={a_uses_addr}-{a_loan_addr}").font = BOLD
ra.cell(row=r, column=2).number_format = USDC
a_equity_addr = f"'Returns (Assumed)'!$B${a_equity_row}"
r += 1
a_lp_eq_row = r
ra.cell(row=r, column=1, value="  LP Equity (90%)")
ra.cell(row=r, column=2, value=f"={a_equity_addr}*(1-{A['gp_coinvest']})").number_format = USDC
a_lp_eq_addr = f"'Returns (Assumed)'!$B${a_lp_eq_row}"
r += 1
a_gp_eq_row = r
ra.cell(row=r, column=1, value="  GP Equity (10%, co-invest)")
ra.cell(row=r, column=2, value=f"={a_equity_addr}*{A['gp_coinvest']}").number_format = USDC
a_gp_eq_addr = f"'Returns (Assumed)'!$B${a_gp_eq_row}"
r += 1
ra.cell(row=r, column=1, value="  memo: vs. Scenario B equity")
ra.cell(row=r, column=2, value=f"={CAP['equity_addr']}").number_format = USDC
r += 1
ra.cell(row=r, column=1, value="  memo: required paydown at assumption (included in Sponsor Equity above)")
ra.cell(row=r, column=2, value=f"={DA['assume_pd_addr']}").number_format = USDC
r += 2

LASTR = get_column_letter(RCOLS[-1])
YRC = lambda i: f"{OPS}${get_column_letter(YEAR_COLS[i])}${yr_row}"  # year number of Returns column i
r = section(ra, r, "EXIT PLANS — cash flows for each plan (Year 0 = closing). The selected plan is the base case below.", span=2 + HOLD)
hdr = r
ra.cell(row=hdr, column=2, value="Year 0").font = BOLD
for i, col in enumerate(RCOLS, start=1):
    ra.cell(row=hdr, column=col, value=f"Year {i}").font = BOLD
r += 1
a_ucf_row = r
ra.cell(row=r, column=1, value="Unlevered CF (same as Scenario B -- identical NOI/reserves/capex)")
for i, col in enumerate(RCOLS):
    opcol = get_column_letter(YEAR_COLS[i])
    ra.cell(row=r, column=col, value=f"={OPS}${opcol}${OP['ucf_row']}").number_format = USDC
r += 2

PL = {}
def plan_tail(key, ops_row, net_addr, sale_year_expr):
    """Total levered CF, IRR, multiple, capital call, peak equity for one plan."""
    global r
    tot = r
    ra.cell(row=r, column=1, value="Total levered cash flow to equity").font = BOLD
    ra.cell(row=r, column=2, value=f"=-{a_equity_addr}").number_format = USDC
    for i, col in enumerate(RCOLS):
        cl = get_column_letter(col)
        ra.cell(row=r, column=col, value=f"={cl}{ops_row}+IF({YRC(i)}={sale_year_expr},{net_addr},0)").number_format = USDC
    r += 1
    rng = f"B{tot}:{LASTR}{tot}"
    irr = r; ra.cell(row=r, column=1, value="Levered IRR"); ra.cell(row=r, column=2, value=f'=IFERROR(IRR({rng}),"N/A")').number_format = PCT; r += 1
    em = r; ra.cell(row=r, column=1, value="Levered equity multiple"); ra.cell(row=r, column=2, value=f"=SUM(C{tot}:{LASTR}{tot})/{a_equity_addr}").number_format = '0.00"x"'; r += 1
    call = r; ra.cell(row=r, column=1, value="Capital call (largest negative year from operations before the sale)")
    ra.cell(row=r, column=2, value=f"=MAX(0,-MIN(C{ops_row}:{LASTR}{ops_row}))").number_format = USDC; r += 1
    peak = r; ra.cell(row=r, column=1, value="Peak equity"); ra.cell(row=r, column=2, value=f"={a_equity_addr}+B{call}").number_format = USDC; r += 2
    PL[key] = dict(ops_row=ops_row, tot_row=tot, irr_row=irr, em_row=em, call_row=call, peak_row=peak)

# Plan 1: sell at maturity
r = section(ra, r, "PLAN 1 — SELL AT MATURITY (end of Year 3, Dec 2029, when the 3.0% loan matures)", span=2 + HOLD)
s_exit_row = r
ra.cell(row=r, column=1, value="Exit price = Year-4 NOI before tax / (exit cap + effective tax rate)")
noi_pre_mat1 = (f"INDEX({OPS}${get_column_letter(YEAR_COLS[0])}${OP['noi_pretax_row']}:"
                f"{OPS}${get_column_letter(YEAR_COLS[-1])}${OP['noi_pretax_row']},{mat}+1)")
ra.cell(row=r, column=2, value=f"={noi_pre_mat1}/({RET['exit_cap_base_addr']}+{RET['eff_tax_exit_addr']})").number_format = USDC
r += 1
ra.cell(row=r, column=1, value="Less: cost of sale")
ra.cell(row=r, column=2, value=f"=-B{s_exit_row}*{A['cost_of_sale_exit']}").number_format = USDC
r += 1
ra.cell(row=r, column=1, value="Less: payoff of the assumed loans at maturity (no prepayment premium)")
ra.cell(row=r, column=2, value=f"=-{DA['payoff_mat_addr']}").number_format = USDC
r += 1
s_net_row = r
ra.cell(row=r, column=1, value="Net sale proceeds at maturity").font = BOLD
ra.cell(row=r, column=2, value=f"=SUM(B{s_exit_row}:B{r-1})").number_format = USDC
r += 1
s_ops_row = r
ra.cell(row=r, column=1, value="Levered CF from operations (zero after the sale)")
for i, col in enumerate(RCOLS):
    dacol = get_column_letter(DA['DACOLS'][i])
    ra.cell(row=r, column=col, value=f"=IF({YRC(i)}<={mat},{get_column_letter(col)}{a_ucf_row}-'Debt (Assumed)'!{dacol}${DA['pre_ds_row']},0)").number_format = USDC
r += 1
plan_tail("sale", s_ops_row, f"$B${s_net_row}", mat)

for key, title_ in [("float", "PLAN 2a — SHORT REFI: FLOATING + 2-YEAR CAP, sell end of Year 5"),
                    ("fixed5", "PLAN 2b — SHORT REFI: 5-YEAR AGENCY FIXED, sell end of Year 5"),
                    ("fixed10", "PLAN 3 — 10-YEAR AGENCY FIXED REFI, sell end of Year 5 (COMPARISON ONLY)")]:
    v = DA['V'][key]
    r = section(ra, r, title_, span=2 + HOLD)
    lastda = get_column_letter(DA['DACOLS'][-1])
    ra.cell(row=r, column=1, value="Exit price (Year-6 NOI before tax / (exit cap + effective tax rate))")
    ra.cell(row=r, column=2, value=f"={RET['exit_price_addr']}").number_format = USDC
    ex_row = r; r += 1
    ra.cell(row=r, column=1, value="Less: cost of sale"); ra.cell(row=r, column=2, value=f"=-B{ex_row}*{A['cost_of_sale_exit']}").number_format = USDC; r += 1
    ra.cell(row=r, column=1, value="Less: refi loan payoff (Year-5 balance)")
    ra.cell(row=r, column=2, value=f"=-'Debt (Assumed)'!{lastda}${v['end_row']}").number_format = USDC; r += 1
    ra.cell(row=r, column=1, value="Less: prepayment premium"); ra.cell(row=r, column=2, value=f"=-{v['prepay']}").number_format = USDC; r += 1
    net_row = r
    ra.cell(row=r, column=1, value="Net sale proceeds (Year 5)").font = BOLD
    ra.cell(row=r, column=2, value=f"=SUM(B{ex_row}:B{r-1})").number_format = USDC
    r += 1
    ops_row = r
    ra.cell(row=r, column=1, value="Levered CF from operations (incl. cash required at refinance in the maturity year)")
    for i, col in enumerate(RCOLS):
        dacol = get_column_letter(DA['DACOLS'][i])
        ra.cell(row=r, column=col, value=(f"={get_column_letter(col)}{a_ucf_row}-'Debt (Assumed)'!{dacol}${v['ds_row']}"
                                          f"-IF({YRC(i)}={mat},{v['cash_req']},0)")).number_format = USDC
    r += 1
    plan_tail(key, ops_row, f"$B${net_row}", HOLD_C)

r = section(ra, r, "EXIT PLAN COMPARISON (Scenario A, same price, same property)", span=8)
cmp_hdr = r
for i, h in enumerate(["Plan", "Levered IRR", "Equity multiple", "Capital call", "Peak equity", "Refi all-in rate",
                       "Refi financing cost %/yr", "Sale year"], start=1):
    ra.cell(row=r, column=i, value=h).font = BOLD
r += 1
for key, lab in [("sale", "1. Sell at maturity"), ("float", "2a. Short refi: floating + cap"),
                 ("fixed5", "2b. Short refi: 5-yr fixed"), ("fixed10", "3. 10-yr fixed refi (comparison)")]:
    p = PL[key]
    ra.cell(row=r, column=1, value=lab)
    ra.cell(row=r, column=2, value=f"=B{p['irr_row']}").number_format = PCT
    ra.cell(row=r, column=3, value=f"=B{p['em_row']}").number_format = '0.00"x"'
    ra.cell(row=r, column=4, value=f"=B{p['call_row']}").number_format = USDC
    ra.cell(row=r, column=5, value=f"=B{p['peak_row']}").number_format = USDC
    if key == "sale":
        ra.cell(row=r, column=6, value="n/a"); ra.cell(row=r, column=7, value="n/a")
        ra.cell(row=r, column=8, value=f"={mat}").number_format = "0"
    else:
        ra.cell(row=r, column=6, value=f"={DA['V'][key]['rate']}").number_format = PCT
        ra.cell(row=r, column=7, value=f"={DA['V'][key]['fin_pct']}").number_format = PCT
        ra.cell(row=r, column=8, value=f"={HOLD_C}").number_format = "0"
    PL[key]['cmp_row'] = r
    r += 1
r += 1

r = section(ra, r, "SELECTED BASE CASE — SCENARIO A (plan chosen on Assumptions)", span=2 + HOLD)
sel_lab_row = r
ra.cell(row=r, column=1, value="Exit plan in the base case")
ra.cell(row=r, column=2, value=(f'=IF({A["a_plan"]}=1,"1. Sell at maturity",IF({A["a_plan"]}=3,"3. 10-yr fixed refi (comparison)",'
                                f'IF({DA["short_choice_addr"]}=1,"2a. Short refi: floating + cap","2b. Short refi: 5-yr fixed")))'))
r += 1
def pick(rowkey, colL):
    s_, f_, f5_, f10_ = (f"{colL}{PL[k][rowkey]}" for k in ("sale", "float", "fixed5", "fixed10"))
    return f"=IF({A['a_plan']}=1,{s_},CHOOSE({DA['sel_var_addr']},{f_},{f5_},{f10_}))"
a_levops_row = r
ra.cell(row=r, column=1, value="Levered CF from Operations")
for col in RCOLS:
    ra.cell(row=r, column=col, value=pick('ops_row', get_column_letter(col))).number_format = USDC
r += 1
a_levtotal_row = r
ra.cell(row=r, column=1, value="TOTAL LEVERED CASH FLOW TO EQUITY — SCENARIO A").font = BOLD
for col in [2] + RCOLS:
    c = ra.cell(row=r, column=col, value=pick('tot_row', get_column_letter(col))); c.number_format = USDC; c.font = BOLD
r += 2

r = section(ra, r, "RETURNS SUMMARY — SCENARIO A (assumed debt)", span=2)
a_irr_row = r
ra.cell(row=r, column=1, value="Levered IRR — SCENARIO A (BASE CASE)")
a_lev_range = f"B{a_levtotal_row}:{LASTR}{a_levtotal_row}"
ra.cell(row=r, column=2, value=f'=IFERROR(IRR({a_lev_range}),"N/A - no sign change / undefined")').number_format = PCT
r += 1
a_em_row = r
ra.cell(row=r, column=1, value="Levered Equity Multiple — SCENARIO A (BASE CASE)")
ra.cell(row=r, column=2, value=f"=SUM(C{a_levtotal_row}:{LASTR}{a_levtotal_row})/{a_equity_addr}").number_format = "0.00\"x\""
r += 1
a_coc1_row = r
ra.cell(row=r, column=1, value="Year-1 Cash-on-Cash — SCENARIO A (BASE CASE)")
ra.cell(row=r, column=2, value=f"=C{a_levops_row}/{a_equity_addr}").number_format = PCT
r += 1
a_call_row = r
ra.cell(row=r, column=1, value="Capital Call Required (largest single-year negative levered CF from operations, e.g. refinance shortfall)")
ra.cell(row=r, column=2, value=f"=MAX(0,-MIN(C{a_levops_row}:{LASTR}{a_levops_row}))").number_format = USDC
r += 1
a_peak_row = r
ra.cell(row=r, column=1, value="PEAK EQUITY — SCENARIO A (Year-0 equity + capital call)").font = BOLD
ra.cell(row=r, column=2, value=f"={a_equity_addr}+B{a_call_row}").font = BOLD
ra.cell(row=r, column=2).number_format = USDC
r += 2

RA = dict(a_equity_addr=a_equity_addr, a_uses_addr=a_uses_addr, a_loan_addr=a_loan_addr,
          a_levtotal_row=a_levtotal_row, a_irr_row=a_irr_row, a_em_row=a_em_row,
          a_coc1_row=a_coc1_row, a_fee_addr=a_fee_addr,
          a_lp_eq_addr=a_lp_eq_addr, a_gp_eq_addr=a_gp_eq_addr, a_ucf_row=a_ucf_row,
          a_call_row=a_call_row, a_peak_row=a_peak_row, PL=PL, sel_lab_row=sel_lab_row)
print("Returns (Assumed) built through row", r)
wb.save("model_wip.xlsx")

# =====================================================================
# 7. WATERFALL — pari passu investor capital (LP + GP co-invest), GP promote
#    on top. Hurdle-balance method (exact, no iterative solving).
# =====================================================================
wf = sheet("Waterfall")
WCOLS = list(range(3, 3 + HOLD))  # C..G = Year1..Year5, B = Year0
colwidths(wf, [52, 13] + [13] * HOLD)
r = 1
r = title(wf, r, "WATERFALL — BASE CASE: Scenario A (assumed debt). Pref -> ROC -> Tier 2 -> Tier 3, GP co-invest pari passu")
wf.cell(row=r, column=1, value=(
    "Structure: all equity (LP 90% + GP co-invest 10%) is ONE investor class, pari passu. Every tier's 'investor' share is "
    "split LP/GP pro rata to capital; the GP additionally earns the promote in Tiers 2-3. No fees are modeled. "
    "Hurdles are measured on total investor capital with a compounding hurdle balance debited by every investor dollar, "
    "which is mathematically the same as the investors reaching exactly that IRR. Tier rates and splits live on Assumptions. "
    "A negative year (e.g. the Year-3 refinance capital call) flows through Tier 1 as a pro-rata investor contribution that accrues pref.")).font = NOTE
r += 2

hdr = r
wf.cell(row=hdr, column=2, value="Year 0").font = BOLD
for i, col in enumerate(WCOLS, start=1):
    wf.cell(row=hdr, column=col, value=f"Year {i}").font = BOLD
r += 1

avail_row = r
wf.cell(row=r, column=1, value="Available Cash for Distribution (Scenario A)")
wf.cell(row=r, column=2, value=0).number_format = USDC
for i, col in enumerate(WCOLS):
    cl = get_column_letter(RET['RCOLS'][i])
    wf.cell(row=r, column=col, value=f"='Returns (Assumed)'!{cl}${RA['a_levtotal_row']}").number_format = USDC
r += 1
inv_eq_row = r
wf.cell(row=r, column=1, value="Investor Capital, Year 0 (LP + GP co-invest)")
wf.cell(row=r, column=2, value=f"={RA['a_equity_addr']}").number_format = USDC
inv_eq = f"$B${inv_eq_row}"
r += 1
wf.cell(row=r, column=1, value="  of which LP")
wf.cell(row=r, column=2, value=f"={RA['a_lp_eq_addr']}").number_format = USDC
r += 1
wf.cell(row=r, column=1, value="  of which GP co-invest")
wf.cell(row=r, column=2, value=f"={RA['a_gp_eq_addr']}").number_format = USDC
r += 2

r = section(wf, r, "TIER 1 — Return of Capital + Preferred Return (100% to investors, pro rata)", span=1 + HOLD)
t1_bal_row = r
wf.cell(row=r, column=1, value="Investor Pref Hurdle Balance, End of Year (compounding at pref rate)")
wf.cell(row=r, column=2, value=f"={inv_eq}").number_format = USDC
r += 1
t1_dist_row = r
wf.cell(row=r, column=1, value="Tier 1 Distribution to Investors")
for col in WCOLS:
    cl, prevcl = get_column_letter(col), get_column_letter(col - 1)
    wf.cell(row=r, column=col, value=f"=MIN({cl}{avail_row},{prevcl}{t1_bal_row}*(1+{A['pref']}))").number_format = USDC
    wf.cell(row=t1_bal_row, column=col, value=f"={prevcl}{t1_bal_row}*(1+{A['pref']})-{cl}{t1_dist_row}").number_format = USDC
r += 1
rem_t1_row = r
wf.cell(row=r, column=1, value="Remaining Cash After Tier 1")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{avail_row}-{cl}{t1_dist_row}").number_format = USDC
r += 2

r = section(wf, r, "TIER 2 — investors / GP promote, until investors reach the Tier 2 IRR hurdle", span=1 + HOLD)
t2_bal_row = r
wf.cell(row=r, column=1, value="Investor Tier-2 Hurdle Balance, End of Year (net of ALL investor $)")
wf.cell(row=r, column=2, value=f"={inv_eq}").number_format = USDC
r += 1
t2_after_t1_row = r
wf.cell(row=r, column=1, value="Tier-2 Hurdle Balance After Tier-1 Cash Applied")
for col in WCOLS:
    cl, prevcl = get_column_letter(col), get_column_letter(col - 1)
    wf.cell(row=r, column=col, value=f"={prevcl}{t2_bal_row}*(1+{A['tier2_hurdle']})-{cl}{t1_dist_row}").number_format = USDC
r += 1
t2_dist_row = r
wf.cell(row=r, column=1, value="Tier 2 Total Distribution")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col,
            value=f"=MIN({cl}{rem_t1_row},MAX(0,{cl}{t2_after_t1_row})/{A['tier2_lp']})").number_format = USDC
r += 1
inv_t2_row = r
wf.cell(row=r, column=1, value="  Tier 2 to investors")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{t2_dist_row}*{A['tier2_lp']}").number_format = USDC
r += 1
promo_t2_row = r
wf.cell(row=r, column=1, value="  Tier 2 GP promote")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{t2_dist_row}*{A['tier2_gp']}").number_format = USDC
r += 1
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=t2_bal_row, column=col, value=f"={cl}{t2_after_t1_row}-{cl}{inv_t2_row}").number_format = USDC
rem_t2_row = r
wf.cell(row=r, column=1, value="Remaining Cash After Tier 2")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{rem_t1_row}-{cl}{t2_dist_row}").number_format = USDC
r += 2

r = section(wf, r, "TIER 3 — investors / GP promote thereafter", span=1 + HOLD)
t3_dist_row = r
wf.cell(row=r, column=1, value="Tier 3 Total Distribution")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{rem_t2_row}").number_format = USDC
r += 1
inv_t3_row = r
wf.cell(row=r, column=1, value="  Tier 3 to investors")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{t3_dist_row}*{A['tier3_lp']}").number_format = USDC
r += 1
promo_t3_row = r
wf.cell(row=r, column=1, value="  Tier 3 GP promote")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{t3_dist_row}*{A['tier3_gp']}").number_format = USDC
r += 2

r = section(wf, r, "SPLIT BY PARTY (investor distributions split pro rata to capital; promote to GP)", span=1 + HOLD)
inv_total_row = r
wf.cell(row=r, column=1, value="Total to Investors (Tier 1 + investor share of Tiers 2-3)")
wf.cell(row=r, column=2, value=0).number_format = USDC
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{t1_dist_row}+{cl}{inv_t2_row}+{cl}{inv_t3_row}").number_format = USDC
r += 1
lp_total_row = r
wf.cell(row=r, column=1, value="LP Total Distribution").font = BOLD
wf.cell(row=r, column=2, value=f"=-{RA['a_lp_eq_addr']}").number_format = USDC
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{inv_total_row}*(1-{A['gp_coinvest']})").number_format = USDC
    wf.cell(row=r, column=col).font = BOLD
r += 1
gp_coinv_row = r
wf.cell(row=r, column=1, value="GP Co-Invest Distribution (pro rata, same terms as LP)")
wf.cell(row=r, column=2, value=f"=-{RA['a_gp_eq_addr']}").number_format = USDC
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{inv_total_row}*{A['gp_coinvest']}").number_format = USDC
r += 1
promote_row = r
wf.cell(row=r, column=1, value="GP Promote (Tier 2 + Tier 3)")
wf.cell(row=r, column=2, value=0).number_format = USDC
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{promo_t2_row}+{cl}{promo_t3_row}").number_format = USDC
r += 1
gp_total_row = r
wf.cell(row=r, column=1, value="GP Total Distribution (co-invest + promote)").font = BOLD
wf.cell(row=r, column=2, value=f"=-{RA['a_gp_eq_addr']}").number_format = USDC
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{gp_coinv_row}+{cl}{promote_row}").number_format = USDC
    wf.cell(row=r, column=col).font = BOLD
r += 2

r = section(wf, r, "CHECK — LP + GP distributions must equal Available Cash each year", span=1 + HOLD)
wf_check_row = r
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{lp_total_row}+{cl}{gp_total_row}-{cl}{avail_row}").number_format = USDC
r += 2

last = get_column_letter(WCOLS[-1])
r = section(wf, r, "LP / GP RETURNS (Scenario A)", span=2)
lp_irr_row = r
wf.cell(row=r, column=1, value="LP IRR")
wf.cell(row=r, column=2, value=f'=IFERROR(IRR(B{lp_total_row}:{last}{lp_total_row}),"N/A - no sign change / undefined")').number_format = PCT1
r += 1
gp_irr_row = r
wf.cell(row=r, column=1, value="GP IRR (co-invest + promote)")
wf.cell(row=r, column=2, value=f'=IFERROR(IRR(B{gp_total_row}:{last}{gp_total_row}),"N/A - no sign change / undefined")').number_format = PCT1
r += 1
lp_mult_row = r
wf.cell(row=r, column=1, value="LP Equity Multiple")
wf.cell(row=r, column=2, value=f"=SUM(C{lp_total_row}:{last}{lp_total_row})/{RA['a_lp_eq_addr']}").number_format = '0.00"x"'
r += 1
gp_mult_row = r
wf.cell(row=r, column=1, value="GP Equity Multiple (co-invest + promote)")
wf.cell(row=r, column=2, value=f"=SUM(C{gp_total_row}:{last}{gp_total_row})/{RA['a_gp_eq_addr']}").number_format = '0.00"x"'
r += 1
promote_total_row = r
wf.cell(row=r, column=1, value="Total GP Promote over the hold ($)")
wf.cell(row=r, column=2, value=f"=SUM(C{promote_row}:{last}{promote_row})").number_format = USDC
r += 1
wf.cell(row=r, column=1, value="memo: Deal-level Levered IRR (Scenario A) -- LP = GP = this when no promote is earned")
wf.cell(row=r, column=2, value=f"='Returns (Assumed)'!B{RA['a_irr_row']}").number_format = PCT1
r += 1

WF = dict(avail_row=avail_row, lp_total_row=lp_total_row, gp_total_row=gp_total_row,
          wf_check_row=wf_check_row, lp_irr_row=lp_irr_row, gp_irr_row=gp_irr_row,
          lp_mult_row=lp_mult_row, gp_mult_row=gp_mult_row, WCOLS=WCOLS,
          promote_total_row=promote_total_row)
print("Waterfall built through row", r)
wb.save("model_wip.xlsx")

# =====================================================================
# =====================================================================
# 8. SENSITIVITY — live formulas. Each grid cell reads the IRR/EM of its own 4-row calculation
#    block at the bottom of the tab (NOI by year, debt scalars, debt service by year, levered CF).
#    Blocks start from the Operating Model's actual rows and apply only what the two axes change:
#      - purchase price: reassessed tax (scales with price), closing costs, equity, the assumption
#        paydown test (Scenario A) or the LTV leg (Scenario B)
#      - exit cap: exit value AND the refinance appraisal (refi value = refi-year NOI / exit cap)
#      - renovation premium / cost: classic-unit rent (Year-1 capture, full from Year 2), capex
#      - rent growth (Table 2): the rent tracks are rebuilt per cell at the shifted growth path,
#        and tax growth (tied to terminal rent growth) shifts with it.
#    The assumed loans, refinance (sizing, capital call, prepayment premium) and exit are rebuilt
#    per scenario with the same rules as the Debt (Assumed) / Returns (Assumed) tabs. CHECKS
#    confirms each grid's base cell equals the model's own IRR. verify_model.py re-runs every
#    exact cell through its full engine.
# =====================================================================
sn = sheet("Sensitivity")
colwidths(sn, [30] + [14] * 11)
r = 1
r = title(sn, r, "SENSITIVITY — Tables 1-3 on SCENARIO A (BASE CASE: assumed debt, selected exit plan); Table 4 = Scenario B (new debt), secondary")
sn.cell(row=r, column=1, value=(
    "Deal-level levered IRR (top) and equity multiple (bottom). Pre-promote: with pari passu capital, LP IRR = deal IRR "
    "whenever the deal is below the 8% pref. Exit cap runs base +/- 100 bps. Axis steps live on Assumptions. "
    "Each cell is computed in its own calculation block at the bottom of this tab (not a shortcut): assumed loans after "
    "any required paydown, then the selected exit plan (sale at maturity, or a refinance sized on the scenario's refi-year NOI "
    "and exit cap with its cap cost and prepayment premium), tax-adjusted exit. Every cell is exact (verify_model.py re-runs each one through its full engine).")).font = NOTE
sn.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
sn.row_dimensions[r].height = 60
r += 2

YC = [get_column_letter(c) for c in YEAR_COLS[:6]]          # Operating Model columns, Years 1..6
YR = [f"{OPS}{c}${OP['yr_row']}" for c in YC]              # year-number cells (no typed year indices)
LOSS = f"({A['vacancy']}+{A['credit_loss']}+{A['concessions']})"
HOLD_C, MAT_C, IO_C = A['hold_years'], A['assum_first_maturity_yr'], A['io_years']
RATE, AM, CONST = A['rate'], A['amort_years'], DEBT['const_addr']
SENS_BASE = {}


def sens_block(row, label, scen, pk, ec, dg, prem, ck, growth_rows=False):
    """Writes one scenario block starting at `row` (4 rows, or 4 + 2*types + 1 when growth_rows). Returns
    (irr_addr, em_addr, next_row). pk = price factor, ec = exit cap, dg = market rent growth shift,
    prem = premium $/mo, ck = reno cost factor (Excel expressions, normally grid header cells).
    growth_rows=True re-runs the unit-by-unit rent engine (market, prior-renovated and classic tracks)
    at the shifted growth path, so rent-growth cells are exact rather than a scaling shortcut."""
    gpr_s = None
    if growth_rows:
        k = f"{A['turnover_rate']}*{A['burnoff_pct']}"
        terms = {i: [] for i in range(6)}
        for tb in type_blocks:
            ri = tb['row_i']
            mrow, prow = row, row + 1
            sn.cell(row=mrow, column=1, value=f"{label} | {tb['name']} market rent/mo").font = NOTE
            sn.cell(row=prow, column=1, value=f"{label} | {tb['name']} prior-renovated rent/mo").font = NOTE
            for i, c in enumerate(YC):
                col, prev = get_column_letter(3 + i), get_column_letter(2 + i)
                g = f"({OPS}{c}${OP['grow_row']}+{dg})"
                m_f = f"='Unit Mix'!$H${ri}*(1+{g})" if i == 0 else f"={prev}{mrow}*(1+{g})"
                base = f"'Unit Mix'!$G${ri}" if i == 0 else f"{prev}{prow}"
                sn.cell(row=mrow, column=3 + i, value=m_f).number_format = USD
                sn.cell(row=prow, column=3 + i, value=f"={base}+{k}*({col}{mrow}-{base})").number_format = USD
                classic = (f"('Unit Mix'!$F${ri}*(1-{A['reno_y1_capture']})+({col}{mrow}+{prem})*{A['reno_y1_capture']})"
                           if i == 0 else f"({col}{mrow}+{prem})")
                terms[i].append(f"'Unit Mix'!$C${ri}*{classic}+'Unit Mix'!$D${ri}*{col}{prow}")
            row += 2
        sn.cell(row=row, column=1, value=f"{label} | scheduled rent (GPR) at shifted growth").font = NOTE
        for i in range(6):
            sn.cell(row=row, column=3 + i, value="=(" + "+".join(terms[i]) + ")*12").number_format = USD
        gpr_s = row
        row += 1
    q0, q1, q2, q3 = row, row + 1, row + 2, row + 3
    sn.cell(row=q0, column=1, value=f"{label} | NOI Y1..Y6, pretax Y6").font = NOTE
    tax_s = lambda i: f"{OPS}$B${OP['tax_row']}*{pk}*(1+{A['tax_growth']}+{dg})^({YR[i]}-1)"  # tax grows with just value
    for i, c in enumerate(YC):
        col = get_column_letter(3 + i)
        prem_rev = (f"{UM['classic_total_addr']}*({prem}-{A['reno_premium_mo']})*12*IF({YR[i]}=1,{A['reno_y1_capture']},1)"
                    if gpr_s is None else "0")  # growth blocks already carry the premium inside the classic track
        rent_rev = f"({col}{gpr_s}-{OPS}{c}{OP['gpr_row']})" if gpr_s is not None else "0"
        f = (f"={OPS}{c}{OP['noi_row']}-{OPS}{c}{OP['tax_row']}+{tax_s(i)}"
             f"+({rent_rev}+{prem_rev})*(1-{LOSS})*(1-{A['mgmt_fee_pct']})")
        sn.cell(row=q0, column=3 + i, value=f).number_format = USD
    sn.cell(row=q0, column=9, value=f"=H{q0}-{tax_s(5)}").number_format = USD  # Y6 NOI before tax
    exit_net = f"I{q0}/({ec}+{RET['eff_tax_exit_addr']})*(1-{A['cost_of_sale_exit']})"
    uses = f"B{q1}*(1+{A['closing_pct']})+{UM['reno_total_addr']}*{ck}"
    sn.cell(row=q1, column=1, value=f"{label} | debt scalars").font = NOTE
    sn.cell(row=q1, column=2, value=f"={A['price']}*{pk}").number_format = USD  # price
    if scen == "A":
        L0 = f"({A['assum_first_bal']}+{A['assum_supp_bal']})"
        sn.cell(row=q1, column=3, value=f"=MAX(0,{L0}-{A['assum_max_ltv']}*B{q1})").number_format = USD      # paydown
        sn.cell(row=q1, column=4, value=f"={A['assum_first_bal']}-MAX(0,C{q1}-{A['assum_supp_bal']})").number_format = USD
        sn.cell(row=q1, column=5, value=f"={A['assum_supp_bal']}-MIN(C{q1},{A['assum_supp_bal']})").number_format = USD
        sn.cell(row=q1, column=6, value=f"={uses}+(D{q1}+E{q1})*{A['assum_fee_pct']}-(D{q1}+E{q1})").number_format = USD  # equity
        r1, r2 = A['assum_first_rate'], A['assum_supp_rate']
        sn.cell(row=q1, column=7, value=(f"=IF({A['assum_io']}=1,D{q1}+E{q1},"
                                         f"-FV({r1},{MAT_C},PMT({r1},{AM},D{q1}),D{q1})-FV({r2},{MAT_C},PMT({r2},{AM},E{q1}),E{q1}))")).number_format = USD  # payoff at maturity
        SEL, PLAN = DA['SEL'], A['a_plan']
        refi_noi = f"INDEX(C{q0}:H{q0},{MAT_C}+1)"
        sn.cell(row=q1, column=8, value=f"=MIN({refi_noi}/{ec}*{A['ltv']},{refi_noi}/({A['min_dscr']}*-PMT({SEL['size']},{AM},1)))").number_format = USD  # refi loan
        n_am = f"MAX(0,{HOLD_C}-{MAT_C}-{SEL['io']})"
        sn.cell(row=q1, column=9, value=f"=IF({n_am}=0,H{q1},-FV({SEL['rate']},{n_am},PMT({SEL['rate']},{AM},H{q1}),H{q1}))").number_format = USD  # refi bal at sale
        sn.cell(row=q1, column=10, value=f"=I{q1}*{SEL['prepay_pct']}").number_format = USD  # prepayment premium
        sn.cell(row=q1, column=11, value=f"={exit_net}-I{q1}-J{q1}").number_format = USD  # net sale proceeds, Year-5 sale
        sn.cell(row=q1, column=12, value=f"=H{q1}*{SEL['upfront_pct']}").number_format = USD  # cap premium at refi
        noi_pre_m1 = f"({refi_noi}-{OPS}$B${OP['tax_row']}*{pk}*(1+{A['tax_growth']}+{dg})^{MAT_C})"
        sn.cell(row=q1, column=13, value=f"={noi_pre_m1}/({ec}+{RET['eff_tax_exit_addr']})*(1-{A['cost_of_sale_exit']})-G{q1}").number_format = USD  # net proceeds, sale at maturity
        eq, proceeds = f"F{q1}", f"K{q1}"
        sn.cell(row=q2, column=1, value=f"{label} | debt service Y1..Y5").font = NOTE
        for i in range(HOLD):
            t = YR[i]
            f = (f"=IF({t}<={MAT_C},IF({A['assum_io']}=1,D{q1}*{r1}+E{q1}*{r2},-PMT({r1},{AM},D{q1})-PMT({r2},{AM},E{q1})),"
                 f"IF({PLAN}=1,0,IF({t}-{MAT_C}<={SEL['io']},H{q1}*{SEL['rate']},-PMT({SEL['rate']},{AM},H{q1}))))")
            sn.cell(row=q2, column=3 + i, value=f).number_format = USD
        cf_a = True
    else:
        sn.cell(row=q1, column=3, value=f"=MIN(B{q1}*{A['ltv']},C{q0}/({A['min_dscr']}*{CONST}))").number_format = USD  # loan
        sn.cell(row=q1, column=4, value=f"={uses}-C{q1}").number_format = USD  # equity
        n_am = f"MAX(0,{HOLD_C}-{IO_C})"
        sn.cell(row=q1, column=5, value=f"=IF({n_am}=0,C{q1},-FV({RATE},{n_am},PMT({RATE},{AM},C{q1}),C{q1}))").number_format = USD
        sn.cell(row=q1, column=6, value=f"=E{q1}*INDEX({A['prepay_range']},{HOLD_C})").number_format = USD
        sn.cell(row=q1, column=7, value=f"={exit_net}-E{q1}-F{q1}").number_format = USD
        eq, proceeds = f"D{q1}", f"G{q1}"
        sn.cell(row=q2, column=1, value=f"{label} | debt service Y1..Y5").font = NOTE
        for i in range(HOLD):
            sn.cell(row=q2, column=3 + i, value=f"=IF({YR[i]}<={IO_C},C{q1}*{RATE},-PMT({RATE},{AM},C{q1}))").number_format = USD
        cf_a = False
    sn.cell(row=q3, column=1, value=f"{label} | levered CF Y0..Y5, IRR, EM").font = NOTE
    sn.cell(row=q3, column=2, value=f"=-{eq}").number_format = USD
    for i in range(HOLD):
        col = get_column_letter(3 + i)
        c = YC[i]
        ucf_s = f"{OPS}{c}{OP['ucf_row']}+({col}{q0}-{OPS}{c}{OP['noi_row']})-{col}{q2}"
        if cf_a:  # plan 1 sells at maturity (net proceeds in M); otherwise refi at maturity (cash in G-H+L), sell in Year 5
            P_ = A['a_plan']
            f = (f"=IF(AND({P_}=1,{YR[i]}>{MAT_C}),0,{ucf_s}-IF({YR[i]}={MAT_C},IF({P_}=1,-M{q1},G{q1}-H{q1}+L{q1}),0)"
                 f"+IF(AND({P_}<>1,{YR[i]}={HOLD_C}),{proceeds},0))")
        else:
            f = f"={ucf_s}+IF({YR[i]}={HOLD_C},{proceeds},0)"
        sn.cell(row=q3, column=3 + i, value=f).number_format = USD
    sn.cell(row=q3, column=8, value=f'=IFERROR(IRR(B{q3}:G{q3}),"N/A")').number_format = PCT1
    sn.cell(row=q3, column=9, value=f"=SUM(C{q3}:G{q3})/{eq}").number_format = '0.00"x"'
    return f"'Sensitivity'!$H${q3}", f"'Sensitivity'!$I${q3}", q3 + 2


KS = [-2, -1, 0, 1, 2]
TABLES = [
    dict(key="T1", scen="A", title="TABLE 1 (Scenario A, BASE CASE) — Exit Cap (rows) x Purchase Price (cols)",
         rows=[(f"={A['exit_cap']}+({k})*{A['sens_exit_step']}", PCT) for k in KS],
         cols=[(f"={A['price']}*(1+({k})*{A['sens_price_step']})", USDC) for k in KS],
         args=lambda rh, ch: dict(pk=f"({ch}/{A['price']})", ec=rh, dg="0", prem=A['reno_premium_mo'], ck="1"),
         base=(2, 2), note=None),
    dict(key="T2", scen="A", title="TABLE 2 (Scenario A, BASE CASE) — Exit Cap (rows) x Market Rent Growth, change vs. base schedule (cols)",
         rows=[(f"={A['exit_cap']}+({k})*{A['sens_exit_step']}", PCT) for k in KS],
         cols=[(f"=({k})*{A['sens_growth_step']}", '+0.00%;-0.00%;0.00%') for k in KS],
         args=lambda rh, ch: dict(pk="1", ec=rh, dg=ch, prem=A['reno_premium_mo'], ck="1"),
         base=(2, 2), note=("Growth change is added to every year's market rent growth. Each cell re-runs the unit-by-unit rent "
                            "engine (market, prior-renovated burn-off, classic tracks) and property-tax growth, which is tied to "
                            "terminal rent growth, at the shifted path. Exact.")),
    dict(key="T3", scen="A", title="TABLE 3 (Scenario A, BASE CASE) — Renovation Premium over Market, $/mo (rows) x Renovation Cost per Unit (cols)",
         rows=[(f"={A['reno_premium_mo']}+({k})*{A['sens_prem_step']}", USDC) for k in [0, 1, 2, 3, 4]],
         cols=[(f"={A['reno_per_unit']}*(1+({k})*{A['sens_cost_step']})", USDC) for k in KS],
         args=lambda rh, ch: dict(pk="1", ec=A['exit_cap'], dg="0", prem=rh, ck=f"({ch}/{A['reno_per_unit']})"),
         base=(0, 2), note="Base premium is $0 (renovated units reach market). Rows show what a premium above market would add."),
    dict(key="T4", scen="B", title="TABLE 4 (SECONDARY: Scenario B, new agency debt) — Exit Cap (rows) x Purchase Price (cols)",
         rows=[(f"={A['exit_cap']}+({k})*{A['sens_exit_step']}", PCT) for k in KS],
         cols=[(f"={A['price']}*(1+({k})*{A['sens_price_step']})", USDC) for k in KS],
         args=lambda rh, ch: dict(pk=f"({ch}/{A['price']})", ec=rh, dg="0", prem=A['reno_premium_mo'], ck="1"),
         base=(2, 2), note="New loan re-sized at each price (LTV or DSCR, whichever binds)."),
]

grid_pos = {}
for T in TABLES:
    r = section(sn, r, T['title'] + " | Levered IRR (top) / Equity Multiple (bottom)", span=6)
    if T['note']:
        sn.cell(row=r, column=1, value=T['note']).font = NOTE
        r += 1
    hdr = r
    sn.cell(row=hdr, column=1, value="rows \\ cols").font = BOLD
    for j, (f, fmt) in enumerate(T['cols']):
        c = sn.cell(row=hdr, column=2 + j, value=f); c.font = BOLD; c.number_format = fmt
    r += 1
    irr_top = r
    for i, (f, fmt) in enumerate(T['rows']):
        c = sn.cell(row=irr_top + i, column=1, value=f); c.number_format = fmt
    em_top = irr_top + len(T['rows']) + 1
    sn.cell(row=em_top - 1, column=1, value="(same grid, Equity Multiple)").font = NOTE
    for i, (f, fmt) in enumerate(T['rows']):
        c = sn.cell(row=em_top + i, column=1, value=f"=A{irr_top + i}"); c.number_format = fmt
    grid_pos[T['key']] = (hdr, irr_top, em_top)
    r = em_top + len(T['rows']) + 1

r += 1
r = section(sn, r, "CALCULATION DETAIL (one 4-row block per grid cell; feeds the grids above)", span=11)
sn.cell(row=r, column=1, value=(
    "Block rows: (1) NOI Years 1-6 in C:H, Year-6 NOI before property tax in I; (2) scalars -- Scenario A: B price, C required "
    "assumption paydown, D/E first/supplemental assumed, F equity, G payoff at maturity, H refi loan, I refi balance at sale, "
    "J prepayment premium, K net sale proceeds at the Year-5 sale, L rate-cap premium at refinance, M net proceeds if sold at "
    "maturity. Scenario A blocks follow the exit plan selected on Assumptions and the refi terms selected on Debt (Assumed); "
    "Scenario B: B price, C loan, D equity, E balance at sale, F prepayment premium, "
    "G net sale proceeds; (3) debt service Years 1-5; (4) levered cash flow Years 0-5, IRR (H), equity multiple (I). Table 2 "
    "blocks first carry 9 extra rows: market and prior-renovated rent by unit type, and scheduled rent, at the shifted growth path.")).font = NOTE
r += 2
for T in TABLES:
    hdr, irr_top, em_top = grid_pos[T['key']]
    for i in range(len(T['rows'])):
        for j in range(len(T['cols'])):
            rh = f"$A${irr_top + i}"
            ch = f"{get_column_letter(2 + j)}${hdr}"
            label = f"{T['key']} r{i+1} c{j+1}"
            irr_addr, em_addr, r_next = sens_block(r, label, T['scen'], growth_rows=(T['key'] == "T2"), **T['args'](rh, ch))
            ci = sn.cell(row=irr_top + i, column=2 + j, value=f"={irr_addr}")
            ce = sn.cell(row=em_top + i, column=2 + j, value=f"={em_addr}")
            ci.number_format, ce.number_format = PCT1, '0.00"x"'
            if (i, j) == T['base']:
                ci.font = ce.font = BOLD
                SENS_BASE[T['key']] = f"'Sensitivity'!${get_column_letter(2 + j)}${irr_top + i}"
            r = r_next

print("Sensitivity built through row", r)
wb.save("model_wip.xlsx")



# =====================================================================
# 9. CHECKS
# =====================================================================
ck = sheet("Checks")
colwidths(ck, [50, 15, 40])
r = 1
r = title(ck, r, "CHECKS")
r += 1

def check_row(label, formula, expect_zero=True):
    global r
    ck.cell(row=r, column=1, value=label)
    ck.cell(row=r, column=2, value=formula).number_format = USD2
    if expect_zero:
        ck.cell(row=r, column=3, value=f'=IF(ABS(B{r})<0.01,"OK","FAIL")')
    r += 1

r = section(ck, r, "1. SOURCES = USES", span=3)
check_row("Sources - Uses (Capital tab)", f"={CAP['cap_check_addr']}")
r += 1

r = section(ck, r, "2. SCENARIO B: LEVERED CF REBUILT FROM OPERATING + DEBT TABS (each year)", span=3)
for i, (opcol, dbrow, rcol) in enumerate(zip(YEAR_COLS[:5],
                                              range(DEBT['amort_start'], DEBT['amort_start'] + 5),
                                              RET['RCOLS']), start=1):
    ocl = get_column_letter(opcol)
    rcl = get_column_letter(rcol)
    fresh = f"({OPS}{ocl}${OP['ucf_row']}-'Debt'!$E${dbrow})"
    check_row(f"Year {i}: (Operating UCF - Debt Svc) - Returns Levered-from-Ops", f"={fresh}-'Returns'!{rcl}{lev_before_exit_row}")
r += 1

r = section(ck, r, "3. NOI RECOMPUTATION (EGI + Opex - NOI, each year)", span=3)
for i, col in enumerate(YEAR_COLS[:5], start=1):
    cl = get_column_letter(col)
    check_row(f"Year {i}: EGI+OpexTotal-NOI", f"={OPS}{cl}{egi_row}+{OPS}{cl}{opex_total_row}-{OPS}{cl}{noi_row}")
r += 1

r = section(ck, r, "4. SCENARIO A (BASE CASE) WATERFALL DISTRIBUTIONS = AVAILABLE CASH (each year)", span=3)
for i, col in enumerate(WF['WCOLS'], start=1):
    cl = get_column_letter(col)
    check_row(f"Year {i}: LP+GP-Available", f"='Waterfall'!{cl}{WF['wf_check_row']}")
r += 1

r = section(ck, r, "5. SCENARIO A (BASE CASE) WATERFALL HURDLE BALANCES NEVER GO NEGATIVE", span=3)
t1_range = f"'Waterfall'!C{t1_bal_row}:{get_column_letter(WF['WCOLS'][-1])}{t1_bal_row}"
t2_range = f"'Waterfall'!C{t2_bal_row}:{get_column_letter(WF['WCOLS'][-1])}{t2_bal_row}"
ck.cell(row=r, column=1, value="MIN Tier-1 hurdle balance (should be >= 0)")
ck.cell(row=r, column=2, value=f"=MIN({t1_range})").number_format = USD2
ck.cell(row=r, column=3, value=f'=IF(B{r}>=-0.01,"OK","FAIL")')
r += 1
ck.cell(row=r, column=1, value="MIN Tier-2 hurdle balance (should be >= 0)")
ck.cell(row=r, column=2, value=f"=MIN({t2_range})").number_format = USD2
ck.cell(row=r, column=3, value=f'=IF(B{r}>=-0.01,"OK","FAIL")')
r += 2

r = section(ck, r, "6. LP EQUITY + GP EQUITY = TOTAL EQUITY", span=3)
check_row("Scenario B (Capital tab): LP+GP Equity - Total Equity", f"={CAP['lp_eq_addr']}+{CAP['gp_eq_addr']}-{CAP['equity_addr']}")
check_row("Scenario A (base case, Returns (Assumed) tab): LP+GP Equity - Total Equity", f"={RA['a_lp_eq_addr']}+{RA['a_gp_eq_addr']}-{RA['a_equity_addr']}")
r += 1

r = section(ck, r, "7. SCENARIO B DEBT SCHEDULE INTERNAL CONSISTENCY", span=3)
check_row("Loan - Cumulative Principal Paid - Year5 End Balance",
          f"={DEBT['loan_addr']}-SUM('Debt'!D{DEBT['amort_start']}:D{DEBT['amort_end']})-'Debt'!F{DEBT['amort_end']}")
r += 1

r = section(ck, r, "8. NOI BRIDGE TIES OUT (Day-0 + burn-off + capture = Year-1 Forward)", span=3)
check_row("Bridge sum - Operating Model Year-1 NOI",
          f"='Returns'!B{RET['b_y1_row']}-{noi_y1}")
r += 1

r = section(ck, r, "9. SCENARIO A REFINANCE SCHEDULES ROLL FORWARD (loan - principal paid - Year-5 balance), each option", span=3)
_lc = get_column_letter(DA['DACOLS'][-1])
for _k, _lab in [("float", "Floating + cap"), ("fixed5", "5-yr fixed"), ("fixed10", "10-yr fixed")]:
    _v = DA['V'][_k]
    check_row(f"{_lab}: refi loan - principal - Year-5 balance",
              f"={_v['loan']}-SUM('Debt (Assumed)'!B{_v['prin_row']}:{_lc}{_v['prin_row']})-'Debt (Assumed)'!{_lc}{_v['end_row']}")
check_row("Selected base-case cash flow = the chosen plan's cash flow (Year 5)",
          f"='Returns (Assumed)'!{get_column_letter(RCOLS[-1])}{RA['a_levtotal_row']}-IF({A['a_plan']}=1,'Returns (Assumed)'!{get_column_letter(RCOLS[-1])}{RA['PL']['sale']['tot_row']},"
          f"CHOOSE({DA['sel_var_addr']},'Returns (Assumed)'!{get_column_letter(RCOLS[-1])}{RA['PL']['float']['tot_row']},"
          f"'Returns (Assumed)'!{get_column_letter(RCOLS[-1])}{RA['PL']['fixed5']['tot_row']},'Returns (Assumed)'!{get_column_letter(RCOLS[-1])}{RA['PL']['fixed10']['tot_row']}))")
r += 1

r = section(ck, r, "10. SENSITIVITY GRIDS: BASE CELL = MODEL IRR (catches any drift between the grid blocks and the model tabs)", span=3)
for key, target, lab in [("T1", f"'Returns (Assumed)'!B{RA['a_irr_row']}", "Table 1 base cell - Scenario A levered IRR"),
                         ("T2", f"'Returns (Assumed)'!B{RA['a_irr_row']}", "Table 2 base cell - Scenario A levered IRR"),
                         ("T3", f"'Returns (Assumed)'!B{RA['a_irr_row']}", "Table 3 base cell - Scenario A levered IRR"),
                         ("T4", f"'Returns'!B{RET['lev_irr_row']}", "Table 4 base cell - Scenario B levered IRR")]:
    ck.cell(row=r, column=1, value=lab)
    ck.cell(row=r, column=2, value=f"={SENS_BASE[key]}-{target}").number_format = "0.000000%"
    ck.cell(row=r, column=3, value=f'=IF(ABS(B{r})<0.000001,"OK","FAIL")')
    r += 1
r += 1

r = section(ck, r, "11. FORMULA ERROR SCAN", span=3)
ck.cell(row=r, column=1, value="See Phase 3 verification report for a full-workbook #REF!/#DIV/0!/#VALUE!/#NAME? scan (done via LibreOffice headless recalculation + openpyxl re-read, not a formula on this tab).").font = NOTE
r += 2

CK = dict()
print("Checks built through row", r)
wb.save("model_wip.xlsx")

# =====================================================================
# 10. SUMMARY
# =====================================================================
sm = sheet("Summary")
colwidths(sm, [40, 20, 40])
r = 1
r = title(sm, r, "SUMMARY — Parkview Crossing")
sm.cell(row=r, column=1, value=(
    "97-unit garden apartment community (unit count per Broward Property Appraiser), Pompano Beach, FL, built 1958. Light value-add / core-plus: "
    "75% of units already renovated by the prior owner; this plan finishes the remaining ~24 classic "
    "units, burns off loss-to-lease on the rest, and underwrites Florida's post-sale property-tax "
    "reassessment (and a tax-adjusted exit) explicitly rather than ignoring them.")).font = NOTE
sm.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
sm.row_dimensions[r].height = 45
r += 3

r = section(sm, r, "SOURCES & USES — BASE CASE: Scenario A, assumed debt", span=2)
sm.cell(row=r, column=1, value="Purchase Price"); sm.cell(row=r, column=2, value=f"={A['price']}").number_format = USDC; r += 1
sm.cell(row=r, column=1, value="Total Uses (incl. loan assumption fee)"); sm.cell(row=r, column=2, value=f"={RA['a_uses_addr']}").number_format = USDC; r += 1
sm.cell(row=r, column=1, value="Assumed Debt (First + Supplemental, Year-0)"); sm.cell(row=r, column=2, value=f"={RA['a_loan_addr']}").number_format = USDC; r += 1
sm.cell(row=r, column=1, value="Sponsor Equity").font = BOLD
sm.cell(row=r, column=2, value=f"={RA['a_equity_addr']}").font = BOLD
sm.cell(row=r, column=2).number_format = USDC; r += 1
sm.cell(row=r, column=1, value="  LP Equity (90%)"); sm.cell(row=r, column=2, value=f"={RA['a_lp_eq_addr']}").number_format = USDC; r += 1
sm.cell(row=r, column=1, value="  GP Equity (10%)"); sm.cell(row=r, column=2, value=f"={RA['a_gp_eq_addr']}").number_format = USDC; r += 1
sm.cell(row=r, column=1, value="Exit plan (Scenario A base case)"); sm.cell(row=r, column=2, value=f"='Returns (Assumed)'!B{RA['sel_lab_row']}"); r += 1
sm.cell(row=r, column=1, value="Capital Call at the Year-3 Refinance (Scenario A, selected plan)"); sm.cell(row=r, column=2, value=f"='Returns (Assumed)'!B{RA['a_call_row']}").number_format = USDC; r += 1
sm.cell(row=r, column=1, value="PEAK EQUITY (Scenario A)").font = BOLD; sm.cell(row=r, column=2, value=f"='Returns (Assumed)'!B{RA['a_peak_row']}").number_format = USDC; r += 2

r = section(sm, r, "KEY METRICS (property-level, same under both debt scenarios unless labeled)", span=2)
sm.cell(row=r, column=1, value="1. Broker-Stated Cap Rate (seller's current tax basis)"); sm.cell(row=r, column=2, value=f"={A['broker_cap']}").number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="2. In-Place Cap Rate, Day-0, reassessed tax (TRUE going-in)").font = BOLD
sm.cell(row=r, column=2, value=f"={RET['cap_inplace_addr']}").font = BOLD
sm.cell(row=r, column=2).number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="3. Year-1 Forward Cap Rate (includes partial-yr business plan)")
sm.cell(row=r, column=2, value=f"='Returns'!B{RET['cap_y1fwd_row']}").number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="Exit Cap Rate (base case: Fort Lauderdale market 5.60% + 100 bps Class C / vintage spread)"); sm.cell(row=r, column=2, value=f"={RET['exit_cap_base_addr']}").number_format = PCT; r += 1
sm.cell(row=r, column=1, value="Assumed-Debt LTV at Close (after any lender-required paydown)"); sm.cell(row=r, column=2, value=f"={RA['a_loan_addr']}/{A['price']}").number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="Agency 10-yr Fixed Rate (Scenario B new debt; Scenario A plan 3 comparison)"); sm.cell(row=r, column=2, value=f"={A['rate']}").number_format = PCT; r += 1
sm.cell(row=r, column=1, value="Scenario A Refinance Rate, selected plan (floating: 30-day SOFR + spread, capped)"); sm.cell(row=r, column=2, value=f"={DA['SEL']['rate']}").number_format = PCT; r += 1
sm.cell(row=r, column=1, value="Hold Period (structural)"); sm.cell(row=r, column=2, value=f"={A['hold_years']}").number_format = "0 \"years\""; r += 2

r = section(sm, r, "RETURNS — BASE CASE: Scenario A, assumed debt", span=2)
sm.cell(row=r, column=1, value="Unlevered IRR (debt-agnostic)"); sm.cell(row=r, column=2, value=f"='Returns'!B{RET['unlev_irr_row']}").number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="Levered IRR (deal-level, Scenario A)").font = BOLD
sm.cell(row=r, column=2, value=f"='Returns (Assumed)'!B{RA['a_irr_row']}").font = BOLD
sm.cell(row=r, column=2).number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="Unlevered Equity Multiple (debt-agnostic)"); sm.cell(row=r, column=2, value=f"='Returns'!B{RET['unlev_em_row']}").number_format = "0.00\"x\""; r += 1
sm.cell(row=r, column=1, value="Levered Equity Multiple (deal-level, Scenario A)").font = BOLD
sm.cell(row=r, column=2, value=f"='Returns (Assumed)'!B{RA['a_em_row']}").font = BOLD
sm.cell(row=r, column=2).number_format = "0.00\"x\""; r += 1
sm.cell(row=r, column=1, value="LP IRR (Scenario A)"); sm.cell(row=r, column=2, value=f"='Waterfall'!B{WF['lp_irr_row']}").number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="LP Equity Multiple (Scenario A)"); sm.cell(row=r, column=2, value=f"='Waterfall'!B{WF['lp_mult_row']}").number_format = "0.00\"x\""; r += 1
sm.cell(row=r, column=1, value="GP IRR (Scenario A)"); sm.cell(row=r, column=2, value=f"='Waterfall'!B{WF['gp_irr_row']}").number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="GP Equity Multiple (Scenario A)"); sm.cell(row=r, column=2, value=f"='Waterfall'!B{WF['gp_mult_row']}").number_format = "0.00\"x\""; r += 1
sm.cell(row=r, column=1, value="GP Promote earned over hold ($, Scenario A)"); sm.cell(row=r, column=2, value=f"='Waterfall'!B{WF['promote_total_row']}").number_format = USDC; r += 2

r = section(sm, r, "SCENARIO A EXIT PLANS — what to do when the 3.0% loan matures (Dec 2029)", span=8)
_hdr = r
for _i, _h in enumerate(["Plan", "Levered IRR", "Equity multiple", "Capital call", "Peak equity", "Refi all-in rate",
                         "Refi financing cost %/yr", "Sale year"], start=1):
    sm.cell(row=r, column=_i, value=_h).font = BOLD
r += 1
for _k in ("sale", "float", "fixed5", "fixed10"):
    _cr = RA['PL'][_k]['cmp_row']
    for _c in range(1, 9):
        _src = sm.cell(row=r, column=_c, value=f"='Returns (Assumed)'!{get_column_letter(_c)}{_cr}")
    for _c, _f in zip(range(2, 9), [PCT, '0.00"x"', USDC, USDC, PCT, PCT, "0"]):
        sm.cell(row=r, column=_c).number_format = _f
    r += 1
sm.cell(row=r, column=1, value=(
    "Base case = 2a. A 3.0% loan through 2029 is the reason to buy with assumed debt; selling at maturity (1) gives up "
    "two years of the renovated, burned-off NOI and pays acquisition and sale costs over a 3-year hold. Of the two refinances "
    "that can be prepaid cheaply at the 2031 sale, the floating loan with a 2-year cap costs less than the 5-year fixed, "
    "whose 4% prepayment premium in loan year 2 outweighs its fixed rate. The cap limits the rate risk to the strike.")).font = NOTE
r += 2

r = section(sm, r, "DEBT SCENARIO COMPARISON — deal-level (pre-promote) returns", span=3)
sm.cell(row=r, column=2, value="A: Assumed Debt (BASE CASE)").font = BOLD
sm.cell(row=r, column=3, value="B: New Debt (alternative)").font = BOLD
r += 1
sm.cell(row=r, column=1, value="Year-0 Loan Amount")
sm.cell(row=r, column=2, value=f"={RA['a_loan_addr']}").number_format = USDC
sm.cell(row=r, column=3, value=f"={DEBT['loan_addr']}").number_format = USDC
r += 1
sm.cell(row=r, column=1, value="Rate (A: blended assumed rate to Year 3, then the selected refi; B: agency fixed)")
sm.cell(row=r, column=2, value=f"={A['assum_blended_rate']}").number_format = PCT
sm.cell(row=r, column=3, value=f"={A['rate']}").number_format = PCT
r += 1
sm.cell(row=r, column=1, value="Sponsor Equity Required")
sm.cell(row=r, column=2, value=f"={RA['a_equity_addr']}").number_format = USDC
sm.cell(row=r, column=3, value=f"={CAP['equity_addr']}").number_format = USDC
r += 1
sm.cell(row=r, column=1, value="Levered IRR (deal-level)")
sm.cell(row=r, column=2, value=f"='Returns (Assumed)'!B{RA['a_irr_row']}").number_format = PCT1
sm.cell(row=r, column=3, value=f"='Returns'!B{RET['lev_irr_row']}").number_format = PCT1
r += 1
sm.cell(row=r, column=1, value="Levered Equity Multiple (deal-level)")
sm.cell(row=r, column=2, value=f"='Returns (Assumed)'!B{RA['a_em_row']}").number_format = "0.00\"x\""
sm.cell(row=r, column=3, value=f"='Returns'!B{RET['lev_em_row']}").number_format = "0.00\"x\""
r += 1
sm.cell(row=r, column=1, value="Year-1 Cash-on-Cash")
sm.cell(row=r, column=2, value=f"='Returns (Assumed)'!B{RA['a_coc1_row']}").number_format = PCT1
sm.cell(row=r, column=3, value=f"='Returns'!C{RET['lev_before_exit_row']}/'Returns'!B{RET['inv_row']}").number_format = PCT1
r += 2

r = section(sm, r, "BID PRICE — max price by target return, BOTH debt scenarios (solver output, not live formulas)", span=8)
sm.cell(row=r, column=1, value=(
    "From price_solve.py (repo root), which runs the same engine verify_model.py checks line by line against this workbook, "
    "and writes bid_prices.json, which this builder reads. Goal-seek is not expressible as static Excel formulas: re-run "
    "price_solve.py, then build_model.py, after any assumption change (price_solve.py flags stale rows). Held fixed: exit cap "
    "(a market input), assumed loan balances, rents, other opex, reno capex. Moves with price: reassessed tax, closing costs, "
    "Scenario B loan (LTV/DSCR), the assumption paydown test (Scenario A), equity.")).font = NOTE
r += 1
hdr = r
for i, h in enumerate(["Scenario / Target", "Max Price", "$/Unit", "vs $13.8M ask", "Going-In (In-Place) Cap",
                       "Deal IRR", "LP IRR", "A: required paydown / B: loan"], start=1):
    sm.cell(row=hdr, column=i, value=h).font = BOLD
r += 1
import json, os
BID_ROWS = json.load(open("bid_prices.json"))["rows"] if os.path.exists("bid_prices.json") else []
for row_ in BID_ROWS:
    sm.cell(row=r, column=1, value=row_["label"])
    if row_.get("unreachable"):
        sm.cell(row=r, column=2, value=row_["note"])
    else:
        vals = [(row_["price"], USDC), (row_["ppu"], USDC), (row_["vs_ask"], PCT1), (row_["cap_inplace"], PCT),
                (row_["deal_irr"], PCT), (row_["lp_irr"], PCT), (row_["debt_memo"], USDC)]
        for c, (v, fmt) in enumerate(vals, start=2):
            sm.cell(row=r, column=c, value=v).number_format = fmt
    r += 1
sm.cell(row=r, column=1, value=(
    "With pari passu capital, LP IRR = deal IRR until the 8% pref is met, so target (a) is the same price as an 8% deal IRR. "
    "Scenario A: below ~$12.6M the assumption test (75% max LTV on price, a judgment) forces a principal paydown at closing, "
    "which adds equity and removes 6.2% supplemental debt.")).font = NOTE
r += 2

r = section(sm, r, "DEAL THESIS", span=2)
sm.cell(row=r, column=1, value=(
    "Light value-add / core-plus acquisition of a 1958-vintage, 97-unit Broward County garden apartment "
    "community that is 75% already renovated. Return drivers: (1) finishing the ~24 remaining classic "
    "units on a bottom-up $20,460/unit scope, (2) loss-to-lease burn-off on units still priced below the "
    "broker-disclosed 20.76% market gap, (3) modest, Broward-Class-C-sourced market rent growth capped "
    "at 3.0% terminal, and (4) expense discipline given real insurance and property-tax exposure on a "
    "68-year-old building. Property tax is modeled on Florida's actual post-sale reassessment mechanic "
    "(Fla. Stat. 193.011(8) cost-of-sale method), and exit value uses a tax-adjusted formula so the "
    "exit buyer's own reassessment isn't ignored. Roof condition and the building's 40/50-Year "
    "recertification status are undisclosed and treated as flagged diligence items, not assumptions.")).font = NOTE
sm.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
sm.row_dimensions[r].height = 110

SM = dict()
print("Summary built through row", r)
wb.save("model_wip.xlsx")
print("ALL TABS BUILT. Saved model_wip.xlsx")

with open("_cellmap_all.json", "w") as f:
    import json
    def strval(d):
        return {k: v for k, v in d.items() if isinstance(v, (str, int, float))}
    json.dump(dict(A=strval(A), OP=strval(OP), DEBT=strval(DEBT), CAP=strval(CAP),
                    RET={k: v for k, v in RET.items() if isinstance(v, (str, int))},
                    WF={k: v for k, v in WF.items() if isinstance(v, (str, int))}),
              f, indent=2, default=str)

