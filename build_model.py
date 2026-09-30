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
A['units'] = frm(ws, r, "Units (formula = Unit Mix total, not an input)", 0, "0", "Single source of truth: sums the Unit Mix tab. Listing is internally inconsistent -- LoopNet headline says 97, but the unit-type breakdown in both LoopNet and Crexi marketing text (19 studios + 52 1BR/1BA + 17 2BR/1BA + 10 2BR/2BA) sums to 98. Model uses 98 because the rent roll is built on that breakdown. DILIGENCE ITEM: confirm against the actual rent roll."); r += 1
A['price'] = inp(ws, r, "Purchase Price ($)", 13800000, USDC, "Broker-stated asking price (LoopNet)"); r += 1
A['broker_cap'] = inp(ws, r, "Broker-Stated Cap Rate", 0.07, PCT1, "LoopNet advertised cap rate"); r += 1
A['broker_noi'] = frm(ws, r, "Broker-Implied NOI ($)", f"={A['price']}*{A['broker_cap']}", USDC, "i.e. Price x Broker Cap (not used downstream)"); r += 1
A['closing_pct'] = inp(ws, r, "Closing Costs (% of Price)", 0.015, PCT1, "Broward doc stamps $0.70/$100 + title/legal/reports"); r += 1
A['closing_cost'] = frm(ws, r, "Closing Costs ($)", f"={A['price']}*{A['closing_pct']}", USDC); r += 1
r += 1

r = section(ws, r, "PROPERTY TAX REASSESSMENT")
A['millage'] = inp(ws, r, "Combined Millage Rate", 0.0198394, "0.000000", "PLACEHOLDER (Broward county-wide avg) — REPLACE with BCPA-confirmed parcel millage code rate", bold=True); r += 1
A['seller_taxable'] = inp(ws, r, "Seller's Current TAXABLE Value ($)", 10318700, USDC, "PLACEHOLDER (LoopNet-disclosed 'assessed value', treated as taxable value since no exemptions apply to non-homestead rental) — REPLACE with BCPA-confirmed taxable value", bold=True); r += 1
A['cos_factor'] = inp(ws, r, "Cost-of-Sale Factor (DOR customary)", 0.85, PCT1, "Fla. Stat. 193.011(8): DOR sales-ratio studies customarily net sale price by 15% cost-of-sale allowance. Set to 100% to run the conservative (full-price) case instead."); r += 1
A['nonhs_cap'] = inp(ws, r, "Non-Homestead Annual Assessment Cap", 0.10, PCT1, "Fla. Const. Art VII — 10% cap today; Amendment 3 (Nov 2026 ballot) would cut to 5% starting 2027 if passed — NOT modeled"); r += 1
A['just_value_entry'] = frm(ws, r, "Reassessed Just Value at Purchase ($)", f"={A['price']}*{A['cos_factor']}", USDC, "i.e. Purchase Price x Cost-of-Sale Factor"); r += 1
A['seller_tax'] = frm(ws, r, "Seller's Current Annual Tax ($)", f"={A['seller_taxable']}*{A['millage']}", USDC); r += 1
A['buyer_tax_y1'] = frm(ws, r, "Buyer's Year-1 Tax ($)", f"={A['just_value_entry']}*{A['millage']}", USDC); r += 1
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
A['reno_premium_mo'] = inp(ws, r, "Renovated-Unit Rent Premium ($/month)", 175, USDC, "Southeast Class B/C industry commentary, $100-250/mo range"); r += 1
A['reno_premium_yr'] = frm(ws, r, "Renovated-Unit Rent Premium ($/year)", f"={A['reno_premium_mo']}*12", USDC); r += 1
A['reno_y1_capture'] = inp(ws, r, "Year-1 Premium Capture % (mid-program convention)", 0.5, PCT1, "6-month program starting month 1 of the hold -> average unit captures ~half a year of uplift in Year 1"); r += 1
r += 1

r = section(ws, r, "OPERATING ASSUMPTIONS")
A['vacancy'] = inp(ws, r, "Physical Vacancy %", 0.065, PCT1, "vs. 92% disclosed occupancy; nudged for renovation downtime"); r += 1
A['credit_loss'] = inp(ws, r, "Credit Loss % (of GPR)", 0.01, PCT1); r += 1
A['concessions'] = inp(ws, r, "Concessions % (of GPR)", 0.005, PCT1); r += 1
A['other_income_mo'] = inp(ws, r, "Other Income ($/unit/month)", 35, USDC, "RUBS, pet, parking, admin fees"); r += 1
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

r = section(ws, r, "EXPENSE GROWTH")
A['exp_growth'] = inp(ws, r, "General Expense Growth % (ex-insurance, ex-tax)", 0.035, PCT1); r += 1
A['ins_growth'] = inp(ws, r, "Insurance Growth %", 0.07, PCT1, "above general expense growth given the recent ~37% two-year South Florida trend"); r += 1
r += 1

r = section(ws, r, "OPERATING EXPENSES (Year 1, $/unit/year unless noted)")
A['payroll'] = inp(ws, r, "Payroll (on-site mgmt + maintenance)", 1400, USDC); r += 1
A['repairs'] = inp(ws, r, "Repairs & Maintenance", 1100, USDC, "nudged up for 1958 vintage / undisclosed roof"); r += 1
A['turnover_cost'] = inp(ws, r, "Turnover / Make-Ready", 350, USDC); r += 1
A['contract_svc'] = inp(ws, r, "Contract Services (landscaping, pest, trash)", 450, USDC); r += 1
A['utilities'] = inp(ws, r, "Utilities (owner-paid common area/vacant)", 500, USDC); r += 1
A['insurance_base'] = inp(ws, r, "Insurance — Base Case ($/unit)", 2400, USDC, "vintage-risk-adjusted above the general $2,000/unit South Florida average"); r += 1
A['insurance_roof'] = inp(ws, r, "Insurance — If Roof Replaced ($/unit)", 1900, USDC, "scenario only — see Roof section below"); r += 1
A['mgmt_fee_pct'] = inp(ws, r, "Management Fee (% of EGI)", 0.035, PCT1); r += 1
A['ga'] = inp(ws, r, "G&A / Admin", 250, USDC); r += 1
A['marketing'] = inp(ws, r, "Marketing", 150, USDC); r += 1
A['reserves'] = inp(ws, r, "Replacement Reserves (below NOI)", 300, USDC); r += 1
r += 1

r = section(ws, r, "ROOF & RECERTIFICATION — diligence items, not confident estimates")
A['roof_toggle'] = inp(ws, r, "Roof Replacement Scenario Toggle (1=on, 0=off)", 0, "0"); r += 1
A['roof_cost'] = inp(ws, r, "Roof Replacement Cost ($, one-time, Year 1 if toggled)", 235000, USDC, "~23,480 SF est. roof area x $8-12/SF hurricane-code TPO/mod-bit; midpoint of $188k-282k range"); r += 1
A['recert_year'] = inp(ws, r, "Recertification Year (model Year #)", 2, "0", "next 40/50-Year Program cycle due ~2028; Year 2 of the hold if closing is late 2026/early 2027"); r += 1
A['recert_inspect'] = inp(ws, r, "Recertification Inspection Cost ($, one-time)", 10000, USDC, "placeholder — no sourced fee"); r += 1
A['recert_remediation'] = inp(ws, r, "Recertification Remediation Contingency ($, one-time)", 150000, USDC, "placeholder — genuinely unknowable without an engineer's report"); r += 1
r += 1

r = section(ws, r, "DEBT — SCENARIO B: NEW ACQUISITION DEBT (generic)")
A['sofr'] = inp(ws, r, "1-Month SOFR", 0.0385, PCT1, "sofrrate.com, reading as of 9/18/2026"); r += 1
A['spread'] = inp(ws, r, "Spread (bps over SOFR)", 0.0325, PCT1); r += 1
A['rate'] = frm(ws, r, "All-In Floating Rate", f"={A['sofr']}+{A['spread']}", PCT1, bold=True); r += 1
A['ltv'] = inp(ws, r, "Maximum LTV %", 0.65, PCT1); r += 1
A['min_dscr'] = inp(ws, r, "Minimum DSCR", 1.25, "0.00x"); r += 1
A['min_debt_yield'] = inp(ws, r, "Minimum Debt Yield %", 0.08, PCT1); r += 1
A['io_years'] = inp(ws, r, "Interest-Only Period (years)", 2, "0"); r += 1
A['amort_years'] = inp(ws, r, "Amortization (years)", 30, "0"); r += 1
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
r += 1

r = section(ws, r, "HOLD & EXIT")
A['hold_years'] = frm(ws, r, "Hold Period (years) -- STRUCTURAL, not a live input", 5, "0", "The model is built for a 5-year hold (5 cash-flow columns, exit on Year-6 forward NOI). Changing this cell does NOT change the model -- shown black, not blue, for that reason."); r += 1
A['exit_spread_base'] = inp(ws, r, "Exit Cap Spread over Entry — Base Case (bps)", 0.005, PCT1, "per instruction: entry + 50bps"); r += 1
A['exit_spread_sens'] = inp(ws, r, "Exit Cap Spread over Entry — Sensitivity Ceiling (bps)", 0.010, PCT1, "per instruction: sensitivity extends to +100bps"); r += 1
A['cost_of_sale_exit'] = inp(ws, r, "Cost of Sale at Exit (%)", 0.02, PCT1); r += 1
r += 1

r = section(ws, r, "WATERFALL")
A['pref'] = inp(ws, r, "Preferred Return %", 0.08, PCT1); r += 1
A['tier2_lp'] = inp(ws, r, "Tier 2 LP Share", 0.70, PCT1); r += 1
A['tier2_gp'] = inp(ws, r, "Tier 2 GP Share", 0.30, PCT1); r += 1
A['tier2_hurdle'] = inp(ws, r, "Tier 2 IRR Hurdle", 0.12, PCT1); r += 1
A['tier3_lp'] = inp(ws, r, "Tier 3 LP Share", 0.50, PCT1); r += 1
A['tier3_gp'] = inp(ws, r, "Tier 3 GP Share", 0.50, PCT1); r += 1
A['gp_coinvest'] = inp(ws, r, "GP Co-Invest %", 0.10, PCT1); r += 1

print("Assumptions built through row", r)

# =====================================================================
# 2. UNIT MIX / RENT ROLL
# =====================================================================
um = sheet("Unit Mix")
colwidths(um, [16, 11, 11, 11, 9, 13, 15, 13])
r = 1
r = title(um, r, "UNIT MIX / RENT ROLL — 98 units (see Assumptions note on the listing's 97 vs. 98 discrepancy)")
um.cell(row=r, column=1, value="75% of units already renovated by prior owner (LoopNet/Crexi). Classic-unit counts below are a proportional allocation of that disclosed 75/25 split across unit types — judgment, not unit-type-level disclosed data.").font = NOTE
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
    ("1BR/1BA", 52, 13, 685, 1475, 1780),
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
            f = (f"='Unit Mix'!$F${row_i}*(1-{A['reno_y1_capture']})"
                 f"+({cl}{market_row}+{A['reno_premium_mo']})*{A['reno_y1_capture']}")
        else:
            prev = get_column_letter(col - 1)
            f = f"={prev}{classic_row}*(1+{cl}${grow_row})"
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
op.cell(row=r, column=1, value="Plus: Other Income")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"={A['units']}*{A['other_income_mo']}*12*(1+{A['exp_growth']})^({cl}${yr_row}-1)").number_format = USDC
r += 1
egi_row = r
op.cell(row=r, column=1, value="Effective Gross Income (EGI)").font = BOLD
for col in YEAR_COLS:
    cl = get_column_letter(col)
    op.cell(row=r, column=col, value=f"=SUM({cl}{gpr_row}:{cl}{oi_row})").number_format = USDC
    op.cell(row=r, column=col).font = BOLD
r += 1
OP.update(gpr_row=gpr_row, egi_row=egi_row, market_gpr_row=market_gpr_row, ltl_row=ltl_row,
          vac_row=vac_row, cl_row=cl_row, con_row=con_row, oi_row=oi_row)
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
util_row = opex_line("Utilities (owner-paid)", A['utilities'], A['exp_growth'], r); r += 1

ins_row = r
op.cell(row=r, column=1, value="Insurance")
for col in YEAR_COLS:
    cl = get_column_letter(col)
    base = f"IF({A['roof_toggle']}=1,{A['insurance_roof']},{A['insurance_base']})"
    f = f"=-{A['units']}*({base})*(1+{A['ins_growth']})^({cl}${yr_row}-1)"
    op.cell(row=r, column=col, value=f).number_format = USDC
r += 1

tax_row = r
op.cell(row=r, column=1, value="Property Tax (reassessed basis, capped growth)")
for i, col in enumerate(YEAR_COLS):
    cl = get_column_letter(col)
    if i == 0:
        f = f"=-{A['buyer_tax_y1']}"
    else:
        prev = get_column_letter(col - 1)
        f = f"={prev}{tax_row}*(1+{A['nonhs_cap']})"
    op.cell(row=r, column=col, value=f).number_format = USDC
r += 1

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

OP.update(payroll_row=payroll_row, repairs_row=repairs_row, turnover_row=turnover_row,
          contract_row=contract_row, util_row=util_row, ins_row=ins_row, tax_row=tax_row,
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
r = title(db, r, "DEBT — SCENARIO B (ALTERNATIVE): new acquisition debt, sized on the binding constraint (no circularity)")
r += 1

r = section(db, r, "SIZING", span=3)
db.cell(row=r, column=1, value="Year 1 NOI (from Operating Model)")
db.cell(row=r, column=3, value=f"={noi_y1}").number_format = USDC
noi_y1_ref = f"'Debt'!$C${r}"
r += 1
loan_ltv_row = r
db.cell(row=r, column=1, value="Loan Amount — LTV Constraint")
db.cell(row=r, column=3, value=f"={A['price']}*{A['ltv']}").number_format = USDC
r += 1
loan_dy_row = r
db.cell(row=r, column=1, value="Loan Amount — Debt Yield Constraint")
db.cell(row=r, column=3, value=f"={noi_y1_ref}/{A['min_debt_yield']}").number_format = USDC
r += 1
loan_dscr_row = r
db.cell(row=r, column=1, value="Loan Amount — DSCR Constraint (IO-period debt service)")
db.cell(row=r, column=3, value=f"={noi_y1_ref}/({A['min_dscr']}*{A['rate']})").number_format = USDC
r += 1
loan_row = r
db.cell(row=r, column=1, value="SIZED LOAN AMOUNT (binding = minimum)").font = BOLD
db.cell(row=r, column=3, value=f"=MIN(C{loan_ltv_row},C{loan_dy_row},C{loan_dscr_row})").number_format = USDC
db.cell(row=r, column=3).font = BOLD
loan_addr = f"'Debt'!$C${loan_row}"
r += 1
bind_row = r
db.cell(row=r, column=1, value="Binding Constraint")
db.cell(row=r, column=3,
        value=(f'=IF(C{loan_row}=C{loan_ltv_row},"LTV",'
               f'IF(C{loan_row}=C{loan_dy_row},"Debt Yield","DSCR"))'))
r += 1
db.cell(row=r, column=1, value="Resulting LTV")
db.cell(row=r, column=3, value=f"={loan_addr}/{A['price']}").number_format = PCT1
r += 1
db.cell(row=r, column=1, value="Resulting Debt Yield")
db.cell(row=r, column=3, value=f"={noi_y1_ref}/{loan_addr}").number_format = PCT1
r += 1
db.cell(row=r, column=1, value="Resulting DSCR (Year 1, IO)")
db.cell(row=r, column=3, value=f"={noi_y1_ref}/({loan_addr}*{A['rate']})").number_format = "0.00\"x\""
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
DEBT = dict(loan_addr=loan_addr, amort_start=amort_start, amort_end=amort_end,
            bind_row=bind_row, loan_ltv_row=loan_ltv_row, loan_dy_row=loan_dy_row,
            loan_dscr_row=loan_dscr_row, loan_row=loan_row, noi_y1_ref=noi_y1_ref)

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
rt.cell(row=r, column=1, value="Plus: Other Income")
rt.cell(row=r, column=2, value=f"={A['units']}*{A['other_income_mo']}*12").number_format = USDC
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
                               "util_row", "ins_row", "tax_row", "ga_row", "mktg_row"]])
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
    "Counterfactual S2 = burn-off ON (55% turnover x 50% burn-off, on the 74 prior-renovated units, toward "
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
        value=f"={s2_gpr_addr}*(1-{A['vacancy']}-{A['credit_loss']}-{A['concessions']})+{A['units']}*{A['other_income_mo']}*12").number_format = USDC
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
entry_cap_row = r
rt.cell(row=r, column=1, value="Entry Cap Rate ANCHOR for exit-spread convention = #2 above: In-Place, Day-0, reassessed tax (primary/cost-of-sale method)")
rt.cell(row=r, column=2, value=f"={cap_inplace_addr}").font = BOLD
rt.cell(row=r, column=2).number_format = PCT1
entry_cap_addr = f"'Returns'!$B${entry_cap_row}"
r += 1
exit_cap_base_row = r
rt.cell(row=r, column=1, value="Exit Cap Rate — base case (in-place entry + 50bps)")
rt.cell(row=r, column=2, value=f"={entry_cap_addr}+{A['exit_spread_base']}").number_format = PCT1
exit_cap_base_addr = f"'Returns'!$B${exit_cap_base_row}"
r += 1
exit_cap_sens_row = r
rt.cell(row=r, column=1, value="Exit Cap Rate — sensitivity ceiling (in-place entry + 100bps)")
rt.cell(row=r, column=2, value=f"={entry_cap_addr}+{A['exit_spread_sens']}").number_format = PCT1
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
net_proceeds_row = r
rt.cell(row=r, column=1, value="NET SALE PROCEEDS TO EQUITY — SCENARIO B").font = BOLD
rt.cell(row=r, column=2, value=f"={exit_price_addr}+{cos_exit_addr}+{payoff_addr}").font = BOLD
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

RET = dict(entry_cap_addr=entry_cap_addr, exit_cap_base_addr=exit_cap_base_addr,
           exit_cap_sens_row=exit_cap_sens_row, exit_price_addr=exit_price_addr,
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
    "balance is refinanced at that point into new debt sized on Scenario B's generic terms (LTV/DSCR/Debt "
    "Yield, whichever binds).")).font = NOTE
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
        f = f"={A['assum_first_bal']}"
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
    pmt_amort = f"(-PMT({A['assum_first_rate']},{A['amort_years']},{A['assum_first_bal']})-{cl}{f_int_row})"
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
            value=f"=IF({OPS}${cl}${yr_row}<={mat},IF({OPS}${prev}${yr_row}<={mat},{prev}{f_end_row},{A['assum_first_bal']}),0)")

r = section(da, r, "SUPPLEMENTAL LOAN (pre-maturity)", span=1 + HOLD)
s_beg_row = r
da.cell(row=r, column=1, value="Beginning Balance")
for i, col in enumerate(DACOLS):
    cl = get_column_letter(col)
    if i == 0:
        f = f"={A['assum_supp_bal']}"
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
    pmt_amort = f"(-PMT({A['assum_supp_rate']},{A['amort_years']},{A['assum_supp_bal']})-{cl}{s_int_row})"
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
            value=f"=IF({OPS}${cl}${yr_row}<={mat},IF({OPS}${prev}${yr_row}<={mat},{prev}{s_end_row},{A['assum_supp_bal']}),0)")
    da.cell(row=s_beg_row, column=col).number_format = USDC

r = section(da, r, "REFINANCE AT MATURITY (fires the year after Assumptions!assum_first_maturity_yr)", span=1 + HOLD)
combined_payoff_row = r
da.cell(row=r, column=1, value="Payoff Balance (First + Supplemental, at maturity)")
da.cell(row=r, column=2, value=f"=INDEX(B{f_end_row}:{get_column_letter(DACOLS[-1])}{f_end_row},{mat})+INDEX(B{s_end_row}:{get_column_letter(DACOLS[-1])}{s_end_row},{mat})").number_format = USDC
r += 1
refi_noi_row = r
da.cell(row=r, column=1, value="NOI in the refinance year (Operating Model, dynamically indexed)")
da.cell(row=r, column=2, value=f"=INDEX({OPS}${get_column_letter(YEAR_COLS[0])}${OP['noi_row']}:{OPS}${get_column_letter(YEAR_COLS[-1])}${OP['noi_row']},{mat}+1)").number_format = USDC
refi_noi_addr = f"'Debt (Assumed)'!$B${r}"
r += 1
refi_ltv_row = r
da.cell(row=r, column=1, value="New Loan — LTV constraint")
da.cell(row=r, column=2, value=f"={A['price']}*{A['ltv']}").number_format = USDC
r += 1
refi_dy_row = r
da.cell(row=r, column=1, value="New Loan — Debt Yield constraint")
da.cell(row=r, column=2, value=f"={refi_noi_addr}/{A['min_debt_yield']}").number_format = USDC
r += 1
refi_dscr_row = r
da.cell(row=r, column=1, value="New Loan — DSCR constraint (IO-equivalent)")
da.cell(row=r, column=2, value=f"={refi_noi_addr}/({A['min_dscr']}*{A['rate']})").number_format = USDC
r += 1
refi_loan_row = r
da.cell(row=r, column=1, value="NEW REFI LOAN AMOUNT (binding = minimum)").font = BOLD
da.cell(row=r, column=2, value=f"=MIN(B{refi_ltv_row}:B{refi_dscr_row})").font = BOLD
da.cell(row=r, column=2).number_format = USDC
refi_loan_addr = f"'Debt (Assumed)'!$B${r}"
r += 1
refi_paydown_row = r
da.cell(row=r, column=1, value="Cash Required / (Released) at Refinance = Payoff - New Loan")
da.cell(row=r, column=2, value=f"=B{combined_payoff_row}-{refi_loan_addr}").number_format = USDC
refi_paydown_addr = f"'Debt (Assumed)'!$B${r}"
r += 2

r = section(da, r, "POST-REFINANCE LOAN", span=1 + HOLD)
pmt_refi_row = r
da.cell(row=r, column=1, value="Annual P&I Payment (post-refi IO period)")
da.cell(row=r, column=2, value=f"=-PMT({A['rate']},{A['amort_years']},{refi_loan_addr})").number_format = USDC
pmt_refi_addr = f"'Debt (Assumed)'!$B${r}"
r += 1
rf_beg_row = r
da.cell(row=r, column=1, value="Beginning Balance")
for i, col in enumerate(DACOLS):
    cl = get_column_letter(col)
    prev = get_column_letter(col - 1) if i > 0 else None
    f = (f"=IF({OPS}${cl}${yr_row}={mat}+1,{refi_loan_addr},"
         f"IF({OPS}${cl}${yr_row}>{mat}+1,{prev}{r+3},0))")
    da.cell(row=r, column=col, value=f).number_format = USDC
r += 1
rf_int_row = r
da.cell(row=r, column=1, value="Interest")
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"=IF({OPS}${cl}${yr_row}>{mat},{cl}{rf_beg_row}*{A['rate']},0)").number_format = USDC
r += 1
rf_prin_row = r
da.cell(row=r, column=1, value="Principal (0 during post-refi IO window)")
for col in DACOLS:
    cl = get_column_letter(col)
    io_check = f"({OPS}${cl}${yr_row}-{mat})<={A['io_years']}"
    da.cell(row=r, column=col,
            value=f"=IF({OPS}${cl}${yr_row}>{mat},IF({io_check},0,{pmt_refi_addr}-{cl}{rf_int_row}),0)").number_format = USDC
r += 1
rf_end_row = r
da.cell(row=r, column=1, value="Ending Balance")
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"=IF({OPS}${cl}${yr_row}>{mat},{cl}{rf_beg_row}-{cl}{rf_prin_row},0)").number_format = USDC
r += 2

r = section(da, r, "COMBINED DEBT SERVICE BY YEAR (feeds Returns (Assumed))", span=1 + HOLD)
tot_int_row = r
da.cell(row=r, column=1, value="Total Interest")
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"={cl}{f_int_row}+{cl}{s_int_row}+{cl}{rf_int_row}").number_format = USDC
r += 1
tot_prin_row = r
da.cell(row=r, column=1, value="Total Principal")
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"={cl}{f_prin_row}+{cl}{s_prin_row}+{cl}{rf_prin_row}").number_format = USDC
r += 1
tot_ds_row = r
da.cell(row=r, column=1, value="TOTAL DEBT SERVICE").font = BOLD
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"={cl}{tot_int_row}+{cl}{tot_prin_row}").font = BOLD
    da.cell(row=r, column=col).number_format = USDC
r += 1
tot_end_row = r
da.cell(row=r, column=1, value="TOTAL ENDING BALANCE").font = BOLD
for col in DACOLS:
    cl = get_column_letter(col)
    da.cell(row=r, column=col, value=f"={cl}{f_end_row}+{cl}{s_end_row}+{cl}{rf_end_row}").font = BOLD
    da.cell(row=r, column=col).number_format = USDC
r += 2

DA = dict(f_beg_row=f_beg_row, f_end_row=f_end_row, s_beg_row=s_beg_row, s_end_row=s_end_row,
          combined_payoff_row=combined_payoff_row, refi_loan_addr=refi_loan_addr,
          refi_paydown_addr=refi_paydown_addr, tot_ds_row=tot_ds_row, tot_end_row=tot_end_row,
          DACOLS=DACOLS)
print("Debt (Assumed) built through row", r)
wb.save("model_wip.xlsx")

# =====================================================================
# 6c. RETURNS (ASSUMED) — Scenario A returns, same NOI trajectory as
#     Scenario B, different debt (assumed loan + Year-3 refi).
# =====================================================================
ra = sheet("Returns (Assumed)")
colwidths(ra, [38, 13] + [13] * HOLD)
r = 1
r = title(ra, r, "RETURNS (ASSUMED DEBT) — SCENARIO A (BASE CASE), 5-Year Hold")
ra.cell(row=r, column=1, value=(
    "Same property, same NOI trajectory as the Scenario B (new-debt) Returns tab -- the only thing that "
    "changes here is the debt.")).font = NOTE
r += 2

r = section(ra, r, "SOURCES & USES — SCENARIO A", span=2)
a_fee_row = r
ra.cell(row=r, column=1, value="Loan Assumption Fee")
ra.cell(row=r, column=2, value=f"=({A['assum_first_bal']}+{A['assum_supp_bal']})*{A['assum_fee_pct']}").number_format = USDC
a_fee_addr = f"'Returns (Assumed)'!$B${a_fee_row}"
r += 1
a_uses_row = r
ra.cell(row=r, column=1, value="Total Uses (Scenario B uses + assumption fee)")
ra.cell(row=r, column=2, value=f"={CAP['uses_total_addr']}+{a_fee_addr}").number_format = USDC
a_uses_addr = f"'Returns (Assumed)'!$B${a_uses_row}"
r += 1
a_loan_row = r
ra.cell(row=r, column=1, value="Assumed Debt (First + Supplemental, Year-0 balance)")
ra.cell(row=r, column=2, value=f"={A['assum_first_bal']}+{A['assum_supp_bal']}").number_format = USDC
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
r += 2

r = section(ra, r, "EXIT (same NOI/exit-cap mechanics as Scenario B -- only the loan payoff differs)", span=2)
a_exitprice_row = r
ra.cell(row=r, column=1, value="Exit Price (same tax-adjusted formula as Scenario B)")
ra.cell(row=r, column=2, value=f"={RET['exit_price_addr']}").number_format = USDC
r += 1
a_cos_row = r
ra.cell(row=r, column=1, value="Less: Cost of Sale")
ra.cell(row=r, column=2, value=f"=-B{a_exitprice_row}*{A['cost_of_sale_exit']}").number_format = USDC
r += 1
a_payoff_row = r
ra.cell(row=r, column=1, value="Less: Loan Payoff (Debt (Assumed), Year-5 Total Ending Balance)")
ra.cell(row=r, column=2, value=f"=-'Debt (Assumed)'!{get_column_letter(DA['DACOLS'][-1])}${DA['tot_end_row']}").number_format = USDC
r += 1
a_netproceeds_row = r
ra.cell(row=r, column=1, value="NET SALE PROCEEDS TO EQUITY — SCENARIO A").font = BOLD
ra.cell(row=r, column=2, value=f"=B{a_exitprice_row}+B{a_cos_row}+B{a_payoff_row}").font = BOLD
ra.cell(row=r, column=2).number_format = USDC
a_netproceeds_addr = f"'Returns (Assumed)'!$B${r}"
r += 2

r = section(ra, r, "CASH FLOWS ($) — Year 0 = closing, Years 1-5 = operations + exit in Year 5", span=2 + HOLD)
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
r += 1
a_ds_row = r
ra.cell(row=r, column=1, value="Less: Debt Service (Debt (Assumed))")
for i, col in enumerate(RCOLS):
    dacol = get_column_letter(DA['DACOLS'][i])
    ra.cell(row=r, column=col, value=f"=-'Debt (Assumed)'!{dacol}${DA['tot_ds_row']}").number_format = USDC
r += 1
a_refishort_row = r
ra.cell(row=r, column=1, value="Less: Cash Required at Refinance (new loan < payoff balance; fires in the maturity year only)")
for i, col in enumerate(RCOLS):
    cl = get_column_letter(col)
    yr_i = i + 1
    ra.cell(row=r, column=col, value=f"=-IF({yr_i}={mat},{DA['refi_paydown_addr']},0)").number_format = USDC
r += 1
a_levops_row = r
ra.cell(row=r, column=1, value="Levered CF from Operations")
for col in RCOLS:
    cl = get_column_letter(col)
    ra.cell(row=r, column=col, value=f"={cl}{a_ucf_row}+{cl}{a_ds_row}+{cl}{a_refishort_row}").number_format = USDC
r += 1
a_levexit_row = r
ra.cell(row=r, column=1, value="+ Net Sale Proceeds (Year 5 only)")
for i, col in enumerate(RCOLS):
    if i == HOLD - 1:
        ra.cell(row=r, column=col, value=f"={a_netproceeds_addr}").number_format = USDC
    else:
        ra.cell(row=r, column=col, value=0).number_format = USDC
r += 1
a_levtotal_row = r
ra.cell(row=r, column=1, value="TOTAL LEVERED CASH FLOW TO EQUITY — SCENARIO A").font = BOLD
ra.cell(row=r, column=2, value=f"=-{a_equity_addr}").font = BOLD
ra.cell(row=r, column=2).number_format = USDC
for col in RCOLS:
    cl = get_column_letter(col)
    ra.cell(row=r, column=col, value=f"={cl}{a_levops_row}+{cl}{a_levexit_row}").font = BOLD
    ra.cell(row=r, column=col).number_format = USDC
r += 2

r = section(ra, r, "RETURNS SUMMARY — SCENARIO A (assumed debt)", span=2)
a_irr_row = r
ra.cell(row=r, column=1, value="Levered IRR — SCENARIO A (BASE CASE)")
a_lev_range = f"B{a_levtotal_row}:{get_column_letter(RCOLS[-1])}{a_levtotal_row}"
ra.cell(row=r, column=2, value=f'=IFERROR(IRR({a_lev_range}),"N/A - no sign change / undefined")').number_format = PCT1
r += 1
a_em_row = r
ra.cell(row=r, column=1, value="Levered Equity Multiple — SCENARIO A (BASE CASE)")
ra.cell(row=r, column=2,
        value=f"=SUM(C{a_levtotal_row}:{get_column_letter(RCOLS[-1])}{a_levtotal_row})/{a_equity_addr}").number_format = "0.00\"x\""
r += 1
a_coc1_row = r
ra.cell(row=r, column=1, value="Year-1 Cash-on-Cash — SCENARIO A (BASE CASE)")
ra.cell(row=r, column=2, value=f"=C{a_levops_row}/{a_equity_addr}").number_format = PCT1
r += 2

RA = dict(a_equity_addr=a_equity_addr, a_uses_addr=a_uses_addr, a_loan_addr=a_loan_addr,
          a_levtotal_row=a_levtotal_row, a_irr_row=a_irr_row, a_em_row=a_em_row,
          a_coc1_row=a_coc1_row, a_fee_addr=a_fee_addr, a_netproceeds_addr=a_netproceeds_addr,
          a_lp_eq_addr=a_lp_eq_addr, a_gp_eq_addr=a_gp_eq_addr, a_ucf_row=a_ucf_row,
          a_ds_row=a_ds_row)
print("Returns (Assumed) built through row", r)
wb.save("model_wip.xlsx")

# =====================================================================
# 7. WATERFALL — hurdle-balance method (exact, no iterative solving)
# =====================================================================
wf = sheet("Waterfall")
WCOLS = list(range(3, 3 + HOLD))  # C..G = Year1..Year5, B = Year0
colwidths(wf, [40, 13] + [13] * HOLD)
r = 1
r = title(wf, r, "WATERFALL — 8% Pref -> ROC -> 70/30 to 12% IRR -> 50/50 (BASE CASE: Scenario A, assumed debt)")
wf.cell(row=r, column=1,
        value=("Method: each tier tracks a compounding 'hurdle balance' (what LP is owed at that "
               "tier's rate) that is debited by every LP dollar received. The balance hitting zero is "
               "mathematically equivalent to LP achieving exactly that IRR — no iterative solver needed. "
               "Runs on Scenario A (assumed debt, the base case) -- for the Scenario B (new debt) waterfall, "
               "swap the 'Available Cash' and equity references below to the 'Returns' / 'Capital' tabs.")).font = NOTE
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

lp_inv_row = r
wf.cell(row=r, column=1, value="LP Investment / GP Investment (Year 0)")
wf.cell(row=r, column=2, value=f"=-{RA['a_lp_eq_addr']}").number_format = USDC
r += 1
gp_inv_row = r
wf.cell(row=r, column=2, value=f"=-{RA['a_gp_eq_addr']}").number_format = USDC
r += 1
r += 1

r = section(wf, r, "TIER 1 — Return of Capital + 8% Preferred Return (100% LP)", span=1 + HOLD)
t1_bal_row = r
wf.cell(row=r, column=1, value="Hurdle Balance, End of Year (8% compounding)")
wf.cell(row=r, column=2, value=f"={RA['a_lp_eq_addr']}").number_format = USDC
r += 1
t1_dist_row = r
wf.cell(row=r, column=1, value="Tier 1 Distribution to LP")
for i, col in enumerate(WCOLS):
    cl = get_column_letter(col)
    prevcl = get_column_letter(col - 1)
    boy = f"{prevcl}{t1_bal_row}*(1+{A['pref']})"
    wf.cell(row=r, column=col, value=f"=MIN({cl}{avail_row},{boy})").number_format = USDC
r += 1
# backfill t1_bal_row for years 1-5 (needs t1_dist_row, defined above -> ok, same pass since formulas)
for i, col in enumerate(WCOLS):
    cl = get_column_letter(col)
    prevcl = get_column_letter(col - 1)
    boy = f"{prevcl}{t1_bal_row}*(1+{A['pref']})"
    wf.cell(row=t1_bal_row, column=col, value=f"={boy}-{cl}{t1_dist_row}").number_format = USDC
rem_t1_row = r + 1
wf.cell(row=rem_t1_row, column=1, value="Remaining Cash After Tier 1")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=rem_t1_row, column=col, value=f"={cl}{avail_row}-{cl}{t1_dist_row}").number_format = USDC
r = rem_t1_row + 2

r = section(wf, r, "TIER 2 — 70/30 LP/GP up to a 12% LP IRR", span=1 + HOLD)
t2_bal_row = r
wf.cell(row=r, column=1, value="12% Hurdle Balance, End of Year (compounding, net of ALL LP $ incl. Tier 1)")
wf.cell(row=r, column=2, value=f"={RA['a_lp_eq_addr']}").number_format = USDC
r += 1
t2_after_t1_row = r
wf.cell(row=r, column=1, value="12% Hurdle Balance After Tier-1 Cash Applied")
for col in WCOLS:
    cl = get_column_letter(col)
    prevcl = get_column_letter(col - 1)
    boy = f"{prevcl}{t2_bal_row}*(1+{A['tier2_hurdle']})"
    wf.cell(row=r, column=col, value=f"={boy}-{cl}{t1_dist_row}").number_format = USDC
r += 1
t2_dist_row = r
wf.cell(row=r, column=1, value="Tier 2 Total Distribution (LP+GP)")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col,
            value=f"=MIN({cl}{rem_t1_row},MAX(0,{cl}{t2_after_t1_row})/{A['tier2_lp']})").number_format = USDC
r += 1
lp_t2_row = r
wf.cell(row=r, column=1, value="  LP share (70%)")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{t2_dist_row}*{A['tier2_lp']}").number_format = USDC
r += 1
gp_t2_row = r
wf.cell(row=r, column=1, value="  GP share (30%)")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{t2_dist_row}*{A['tier2_gp']}").number_format = USDC
r += 1
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=t2_bal_row, column=col, value=f"={cl}{t2_after_t1_row}-{cl}{lp_t2_row}").number_format = USDC
rem_t2_row = r
wf.cell(row=r, column=1, value="Remaining Cash After Tier 2")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{rem_t1_row}-{cl}{t2_dist_row}").number_format = USDC
r += 2

r = section(wf, r, "TIER 3 — 50/50 LP/GP thereafter", span=1 + HOLD)
t3_dist_row = r
wf.cell(row=r, column=1, value="Tier 3 Total Distribution (LP+GP)")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{rem_t2_row}").number_format = USDC
r += 1
lp_t3_row = r
wf.cell(row=r, column=1, value="  LP share (50%)")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{t3_dist_row}*{A['tier3_lp']}").number_format = USDC
r += 1
gp_t3_row = r
wf.cell(row=r, column=1, value="  GP share (50%)")
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{t3_dist_row}*{A['tier3_gp']}").number_format = USDC
r += 2

r = section(wf, r, "TOTALS BY PARTY", span=1 + HOLD)
lp_total_row = r
wf.cell(row=r, column=1, value="LP Total Distribution").font = BOLD
wf.cell(row=r, column=2, value=0).number_format = USDC
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{t1_dist_row}+{cl}{lp_t2_row}+{cl}{lp_t3_row}").font = BOLD
    wf.cell(row=r, column=col).number_format = USDC
r += 1
gp_total_row = r
wf.cell(row=r, column=1, value="GP Total Distribution").font = BOLD
wf.cell(row=r, column=2, value=0).number_format = USDC
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col, value=f"={cl}{gp_t2_row}+{cl}{gp_t3_row}").font = BOLD
    wf.cell(row=r, column=col).number_format = USDC
r += 2

r = section(wf, r, "CHECK — LP + GP distributions must equal Available Cash each year", span=1 + HOLD)
wf_check_row = r
for col in WCOLS:
    cl = get_column_letter(col)
    wf.cell(row=r, column=col,
            value=f"={cl}{lp_total_row}+{cl}{gp_total_row}-{cl}{avail_row}").number_format = USDC
r += 2

r = section(wf, r, "LP / GP RETURNS", span=2)
lp_irr_row = r
wf.cell(row=r, column=1, value="LP IRR")
lp_range = f"B{lp_inv_row}:{get_column_letter(WCOLS[-1])}{lp_total_row}"
# Build a single contiguous row for IRR: reuse lp_total_row col B as -investment
wf.cell(row=lp_total_row, column=2, value=f"=-{RA['a_lp_eq_addr']}").number_format = USDC
wf.cell(row=r, column=2, value=f'=IFERROR(IRR(B{lp_total_row}:{get_column_letter(WCOLS[-1])}{lp_total_row}),"N/A - no sign change / undefined")').number_format = PCT1
r += 1
gp_irr_row = r
wf.cell(row=gp_total_row, column=2, value=f"=-{RA['a_gp_eq_addr']}").number_format = USDC
wf.cell(row=r, column=1, value="GP IRR")
wf.cell(row=r, column=2, value=f'=IFERROR(IRR(B{gp_total_row}:{get_column_letter(WCOLS[-1])}{gp_total_row}),"N/A - GP receives $0 in this scenario, IRR undefined")').number_format = PCT1
r += 1
lp_mult_row = r
wf.cell(row=r, column=1, value="LP Equity Multiple")
wf.cell(row=r, column=2,
        value=f"=SUM(C{lp_total_row}:{get_column_letter(WCOLS[-1])}{lp_total_row})/{RA['a_lp_eq_addr']}").number_format = "0.00\"x\""
r += 1
gp_mult_row = r
wf.cell(row=r, column=1, value="GP Equity Multiple")
wf.cell(row=r, column=2,
        value=f"=SUM(C{gp_total_row}:{get_column_letter(WCOLS[-1])}{gp_total_row})/{RA['a_gp_eq_addr']}").number_format = "0.00\"x\""
r += 1

WF = dict(avail_row=avail_row, lp_total_row=lp_total_row, gp_total_row=gp_total_row,
          wf_check_row=wf_check_row, lp_irr_row=lp_irr_row, gp_irr_row=gp_irr_row,
          lp_mult_row=lp_mult_row, gp_mult_row=gp_mult_row, WCOLS=WCOLS)
print("Waterfall built through row", r)
wb.save("model_wip.xlsx")

# =====================================================================
# =====================================================================
# 8. SENSITIVITY — explicit formulas (openpyxl can't make native Excel
#    Data Tables). Each grid cell's IRR/EM references a dedicated helper
#    row (below, in a clearly marked "calculation detail" area) holding
#    a real 6-point cash flow (Year0..Year5) so IRR() gets a plain
#    contiguous range -- no array-literal functions (HSTACK is not
#    supported by all spreadsheet engines, confirmed via LibreOffice
#    testing, so it is deliberately avoided here for portability).
#    Each scenario is a compact, self-contained proxy: Year-1 NOI starts
#    from the Operating Model's base case and is adjusted only for what
#    that table's two axes actually change (tax, debt sizing, renovation
#    NOI/capex, or a flat rent-growth override) -- it does not re-run
#    the full unit-by-unit burn-off engine 25 times per table. Debt is
#    re-sized where price or capex changes; held at the base-case loan
#    where it doesn't. For full-fidelity what-if testing, edit
#    Assumptions directly and read Returns/Waterfall.
# =====================================================================
sn = sheet("Sensitivity")
colwidths(sn, [22] + [13] * 5)
r = 1
r = title(sn, r, "SENSITIVITY — built on SCENARIO B (ALTERNATIVE: new-debt) debt structure; see note")
sn.cell(row=r, column=1, value=(
    "Each grid is a self-contained proxy calc: Year-1 NOI starts from the Operating Model's base case "
    "and is adjusted only for what that table's two axes change (tax, debt sizing, renovation NOI/capex, "
    "or a flat rent-growth override); it does not re-run the full unit-by-unit burn-off engine 25 times. "
    "Debt is re-sized where price or capex changes; held at the base-case loan where it doesn't. "
    "IRR/EM values are pulled from the 'calculation detail' rows near the bottom of this tab. "
    "DEBT STRUCTURE IN THESE GRIDS IS SCENARIO B (new debt, 7.10% floating) -- NOT the Scenario A base case. "
    "Read them as directional, not as base-case returns.")).font = NOTE
r += 2

def cumprinc_end_balance(loan_expr, n_years):
    return f"({loan_expr}+CUMPRINC({A['rate']},{A['amort_years']},{loan_expr},1,{n_years},0))"

noi1 = noi_y1
loan1 = DEBT['loan_addr']
equity1 = CAP['equity_addr']
uses1 = CAP['uses_total_addr']

# ---- helper-row builders: each writes Year0..Year5 into one row, returns (irr_addr, em_addr) ----
HELPER = {'row': None}

def write_helper_row(ws, row, label, equity_expr, cf_list):
    ws.cell(row=row, column=1, value=label).font = NOTE
    ws.cell(row=row, column=2, value=f"=-({equity_expr})").number_format = USDC
    for i, cf in enumerate(cf_list):
        ws.cell(row=row, column=3 + i, value=f"={cf}").number_format = USDC
    irr_c = 3 + len(cf_list)
    em_c = irr_c + 1
    ws.cell(row=row, column=irr_c, value=f'=IFERROR(IRR(B{row}:{get_column_letter(2+len(cf_list))}{row}),"N/A")').number_format = PCT1
    ws.cell(row=row, column=em_c,
            value=f"=SUM(C{row}:{get_column_letter(2+len(cf_list))}{row})/({equity_expr})").number_format = '0.00"x"'
    return f"'Sensitivity'!${get_column_letter(irr_c)}${row}", f"'Sensitivity'!${get_column_letter(em_c)}${row}"

# ---- Table 1: Exit Cap x Rent Growth ----
r = section(sn, r, "TABLE 1 — Exit Cap Rate (rows) x Flat Rent Growth Override (cols) | Levered IRR (top) / Equity Multiple (bottom)", span=6)
exitcap_labels = ["Entry+0bps", "Entry+25bps", "Entry+50bps (base)", "Entry+75bps", "Entry+100bps"]
exitcap_spreads = [0.0, 0.0025, 0.0050, 0.0075, 0.0100]
growth_vals5 = [0.015, 0.020, 0.025, 0.030, 0.035]
hdr = r
sn.cell(row=hdr, column=1, value="Exit Cap \\ Rent Gr.").font = BOLD
for j, g in enumerate(growth_vals5):
    c = sn.cell(row=hdr, column=2 + j, value=g); c.font = BOLD; c.number_format = PCT1
r += 1
irr_cells_t1 = [[None]*5 for _ in range(5)]
em_cells_t1 = [[None]*5 for _ in range(5)]
for i, spread in enumerate(exitcap_spreads):
    for j, g in enumerate(growth_vals5):
        ec = f"({RET['entry_cap_addr']}+{spread})"
        ds_io = f"({loan1}*{A['rate']})"
        ds_amort = f"(-PMT({A['rate']},{A['amort_years']},{loan1}))"
        end_bal5 = cumprinc_end_balance(loan1, 3)
        cf_years = [f"({noi1}*(1+{g})^{n})" for n in range(1, 6)]
        y6noi = f"({noi1}*(1+{g})^6)"
        exitprice = f"({y6noi}/({ec}+{RET['eff_tax_exit_addr']}))"
        proceeds = f"({exitprice}*(1-{A['cost_of_sale_exit']})-{end_bal5})"
        cf = [f"({cf_years[0]}-{ds_io})", f"({cf_years[1]}-{ds_io})",
              f"({cf_years[2]}-{ds_amort})", f"({cf_years[3]}-{ds_amort})",
              f"({cf_years[4]}-{ds_amort}+{proceeds})"]
        irr_cells_t1[i][j] = (equity1, cf)
r_grid1_irr = r
for i in range(5):
    sn.cell(row=r + i, column=1, value=exitcap_labels[i])
r_grid1_em = r + 6
for i in range(5):
    sn.cell(row=r_grid1_em + i, column=1, value=exitcap_labels[i])
sn.cell(row=r_grid1_em - 1, column=1, value="(same grid, Equity Multiple)").font = NOTE
r = r_grid1_em + 6
r += 1

# ---- Table 2: Purchase Price x Exit Cap ----
r = section(sn, r, "TABLE 2 — Purchase Price (rows) x Exit Cap Spread over Entry (cols) | Levered IRR (top) / Equity Multiple (bottom)", span=6)
price_deltas = [-0.10, -0.05, 0.0, 0.05, 0.10]
price_labels = ["-10%", "-5%", "Base ($13.8M)", "+5%", "+10%"]
spread_labels2 = exitcap_labels
hdr = r
sn.cell(row=hdr, column=1, value="Price \\ Exit Spread").font = BOLD
for j, lbl in enumerate(spread_labels2):
    c = sn.cell(row=hdr, column=2 + j, value=lbl); c.font = BOLD
r += 1

def price_scenario_cf(pdelta, spread):
    price_s = f"({A['price']}*(1+{pdelta}))"
    just_val_s = f"({price_s}*{A['cos_factor']})"
    tax_y1_s = f"({just_val_s}*{A['millage']})"
    # noi1_s (Year-1 forward basis) drives the actual projected cash flows -- that's
    # genuinely what the property is expected to collect, business-plan-inclusive.
    noi1_s = f"({noi1}+{A['buyer_tax_y1']}-{tax_y1_s})"
    # day0_noi_s (Day-0 in-place basis) drives ONLY the entry-cap-rate figure used to
    # anchor the exit cap, per the same correction applied on the Returns tab.
    day0_noi_s = f"({day0_noi_addr}+{A['buyer_tax_y1']}-{tax_y1_s})"
    loan_s = f"({price_s}*{A['ltv']})"
    uses_s = f"({price_s}*(1+{A['closing_pct']})+({uses1}-{A['price']}*(1+{A['closing_pct']})))"
    equity_s = f"({uses_s}-{loan_s})"
    entry_cap_s = f"({day0_noi_s}/{price_s})"
    ec = f"({entry_cap_s}+{spread})"
    ds_io = f"({loan_s}*{A['rate']})"
    ds_amort = f"(-PMT({A['rate']},{A['amort_years']},{loan_s}))"
    end_bal5 = cumprinc_end_balance(loan_s, 3)
    base_g = A['growth'][3]
    cf_years = [f"({noi1_s}*(1+{base_g})^{n})" for n in range(0, 5)]
    y6noi = f"({noi1_s}*(1+{base_g})^5)"
    exitprice = f"({y6noi}/({ec}+{RET['eff_tax_exit_addr']}))"
    proceeds = f"({exitprice}*(1-{A['cost_of_sale_exit']})-{end_bal5})"
    cf = [f"({cf_years[0]}-{ds_io})", f"({cf_years[1]}-{ds_io})",
          f"({cf_years[2]}-{ds_amort})", f"({cf_years[3]}-{ds_amort})",
          f"({cf_years[4]}-{ds_amort}+{proceeds})"]
    return equity_s, cf

r_grid2_irr = r
for i in range(5):
    sn.cell(row=r + i, column=1, value=price_labels[i])
r_grid2_em = r + 6
sn.cell(row=r_grid2_em - 1, column=1, value="(same grid, Equity Multiple)").font = NOTE
for i in range(5):
    sn.cell(row=r_grid2_em + i, column=1, value=price_labels[i])
r = r_grid2_em + 6
r += 1

# ---- Table 3: Renovation Premium x Renovation Cost ----
r = section(sn, r, "TABLE 3 — Renovation Premium/mo (rows) x Renovation Cost/unit (cols) | Levered IRR (top) / Equity Multiple (bottom)", span=6)
prem_vals = [100, 137.5, 175, 212.5, 250]
prem_labels = ["$100/mo", "$137.50/mo", "$175/mo (base)", "$212.50/mo", "$250/mo"]
cost_deltas = [-0.20, -0.10, 0.0, 0.10, 0.20]
cost_labels = ["-20%", "-10%", "Base ($20,460)", "+10%", "+20%"]
hdr = r
sn.cell(row=hdr, column=1, value="Premium \\ Cost").font = BOLD
for j, lbl in enumerate(cost_labels):
    c = sn.cell(row=hdr, column=2 + j, value=lbl); c.font = BOLD
r += 1

def reno_scenario_cf(prem_mo, cdelta):
    cost_s = f"({A['reno_per_unit']}*(1+{cdelta}))"
    capex_s = f"({UM['classic_total_addr']}*{cost_s})"
    capex_delta = f"({capex_s}-{UM['reno_total_addr']})"
    equity_s = f"({equity1}+{capex_delta})"
    prem_delta_annual = f"(({prem_mo}-{A['reno_premium_mo']})*12*{UM['classic_total_addr']})"
    noi1_s = f"({noi1}+{prem_delta_annual}*{A['reno_y1_capture']})"
    noi_y_s = [f"({noi1_s}+{prem_delta_annual})" for _ in range(2, 6)]
    base_g = A['growth'][3]
    ds_io = f"({loan1}*{A['rate']})"
    ds_amort = f"(-PMT({A['rate']},{A['amort_years']},{loan1}))"
    end_bal5 = cumprinc_end_balance(loan1, 3)
    y6_s = f"({noi_y_s[3]}*(1+{base_g}))"
    exitprice = f"({y6_s}/({RET['exit_cap_base_addr']}+{RET['eff_tax_exit_addr']}))"
    proceeds = f"({exitprice}*(1-{A['cost_of_sale_exit']})-{end_bal5})"
    cf = [f"({noi1_s}-{ds_io})", f"({noi_y_s[0]}-{ds_io})",
          f"({noi_y_s[1]}-{ds_amort})", f"({noi_y_s[2]}-{ds_amort})",
          f"({noi_y_s[3]}-{ds_amort}+{proceeds})"]
    return equity_s, cf

r_grid3_irr = r
for i in range(5):
    sn.cell(row=r + i, column=1, value=prem_labels[i])
r_grid3_em = r + 6
sn.cell(row=r_grid3_em - 1, column=1, value="(same grid, Equity Multiple)").font = NOTE
for i in range(5):
    sn.cell(row=r_grid3_em + i, column=1, value=prem_labels[i])
r = r_grid3_em + 6
r += 2

# ---- calculation detail area: one helper row per scenario, all 3 tables ----
r = section(sn, r, "CALCULATION DETAIL (per-scenario cash flows -- not for review, feeds the grids above)", span=9)
hdr = r
for i, h in enumerate(["Scenario", "Year 0", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "IRR", "EM"], start=1):
    sn.cell(row=hdr, column=i, value=h).font = BOLD
r += 1

for i, spread in enumerate(exitcap_spreads):
    for j, g in enumerate(growth_vals5):
        equity_s, cf = irr_cells_t1[i][j]
        label = f"T1 {exitcap_labels[i]} / {g:.1%}"
        irr_addr, em_addr = write_helper_row(sn, r, label, equity_s, cf)
        sn.cell(row=r_grid1_irr + i, column=2 + j, value=f"={irr_addr}").number_format = PCT1
        sn.cell(row=r_grid1_em + i, column=2 + j, value=f"={em_addr}").number_format = '0.00"x"'
        r += 1

for i, pd in enumerate(price_deltas):
    for j, sp in enumerate(exitcap_spreads):
        equity_s, cf = price_scenario_cf(pd, sp)
        label = f"T2 {price_labels[i]} / {spread_labels2[j]}"
        irr_addr, em_addr = write_helper_row(sn, r, label, equity_s, cf)
        sn.cell(row=r_grid2_irr + i, column=2 + j, value=f"={irr_addr}").number_format = PCT1
        sn.cell(row=r_grid2_em + i, column=2 + j, value=f"={em_addr}").number_format = '0.00"x"'
        r += 1

for i, pv in enumerate(prem_vals):
    for j, cd in enumerate(cost_deltas):
        equity_s, cf = reno_scenario_cf(pv, cd)
        label = f"T3 {prem_labels[i]} / {cost_labels[j]}"
        irr_addr, em_addr = write_helper_row(sn, r, label, equity_s, cf)
        sn.cell(row=r_grid3_irr + i, column=2 + j, value=f"={irr_addr}").number_format = PCT1
        sn.cell(row=r_grid3_em + i, column=2 + j, value=f"={em_addr}").number_format = '0.00"x"'
        r += 1

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

r = section(ck, r, "9. SCENARIO A DEBT (ASSUMED) SCHEDULE INTERNAL CONSISTENCY (post-refi sub-loan)", span=3)
check_row("Refi Loan - Cumulative Post-Refi Principal - Year5 Refi End Balance",
          f"={DA['refi_loan_addr']}-SUM('Debt (Assumed)'!C{rf_prin_row}:{get_column_letter(DA['DACOLS'][-1])}{rf_prin_row})-'Debt (Assumed)'!{get_column_letter(DA['DACOLS'][-1])}{rf_end_row}")
r += 1

r = section(ck, r, "10. FORMULA ERROR SCAN", span=3)
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
    "98-unit garden apartment community (listing says 97 in one place, 98 in another -- see Assumptions), Pompano Beach, FL, built 1958. Light value-add / core-plus: "
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
sm.cell(row=r, column=1, value="  GP Equity (10%)"); sm.cell(row=r, column=2, value=f"={RA['a_gp_eq_addr']}").number_format = USDC; r += 2

r = section(sm, r, "KEY METRICS (property-level, same under both debt scenarios unless labeled)", span=2)
sm.cell(row=r, column=1, value="1. Broker-Stated Cap Rate (seller's current tax basis)"); sm.cell(row=r, column=2, value=f"={A['broker_cap']}").number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="2. In-Place Cap Rate, Day-0, reassessed tax (TRUE going-in -- anchors the exit cap below)").font = BOLD
sm.cell(row=r, column=2, value=f"={RET['cap_inplace_addr']}").font = BOLD
sm.cell(row=r, column=2).number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="3. Year-1 Forward Cap Rate (includes partial-yr business plan -- NOT used for exit-spread convention)")
sm.cell(row=r, column=2, value=f"='Returns'!B{RET['cap_y1fwd_row']}").number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="Exit Cap Rate (base case, In-Place entry + 50bps -- see NOI Bridge on Returns tab)"); sm.cell(row=r, column=2, value=f"={RET['exit_cap_base_addr']}").number_format = PCT1; r += 1
sm.cell(row=r, column=1, value="Assumed-Debt LTV at Close (fixed balance, not sized)"); sm.cell(row=r, column=2, value=f"={RA['a_loan_addr']}/{A['price']}").number_format = PCT1; r += 1
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
sm.cell(row=r, column=1, value="GP Equity Multiple (Scenario A)"); sm.cell(row=r, column=2, value=f"='Waterfall'!B{WF['gp_mult_row']}").number_format = "0.00\"x\""; r += 2

r = section(sm, r, "DEBT SCENARIO COMPARISON — deal-level (pre-promote) returns", span=3)
sm.cell(row=r, column=2, value="A: Assumed Debt (BASE CASE)").font = BOLD
sm.cell(row=r, column=3, value="B: New Debt (alternative)").font = BOLD
r += 1
sm.cell(row=r, column=1, value="Year-0 Loan Amount")
sm.cell(row=r, column=2, value=f"={RA['a_loan_addr']}").number_format = USDC
sm.cell(row=r, column=3, value=f"={DEBT['loan_addr']}").number_format = USDC
r += 1
sm.cell(row=r, column=1, value="Rate")
sm.cell(row=r, column=2, value=f"={A['assum_blended_rate']}").number_format = PCT1
sm.cell(row=r, column=3, value=f"={A['rate']}").number_format = PCT1
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

r = section(sm, r, "BID PRICE — max price by target return (Scenario A, assumed debt)", span=5)
sm.cell(row=r, column=1, value=(
    "Solved with scipy root-finding in price_solve.py (repo root), not a live in-sheet formula -- "
    "true goal-seek isn't expressible as static Excel formulas without an iterative/circular solver. "
    "Re-run that script any time Assumptions change; these are reported results, not linked cells.")).font = NOTE
r += 1
hdr = r
for i, h in enumerate(["Target", "Max Price", "vs. $13.8M Asking", "Implied In-Place Cap", "Deal IRR / LP IRR"], start=1):
    sm.cell(row=hdr, column=i, value=h).font = BOLD
r += 1
sm.cell(row=r, column=1, value="PENDING RE-SOLVE (Step 4): the prior solved prices assumed 97 units; the model now uses 98 "
        "(see Assumptions 'Units' note). Blanked rather than left stale. Step 4 re-solves under BOTH debt scenarios.").font = BOLD
r += 1
r += 2

r = section(sm, r, "DEAL THESIS", span=2)
sm.cell(row=r, column=1, value=(
    "Light value-add / core-plus acquisition of a 1958-vintage, 98-unit Broward County garden apartment "
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
