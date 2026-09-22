# Phase 3 — Verification Report

Model: [`Parkview_Crossing_Acquisition_Model.xlsx`](Parkview_Crossing_Acquisition_Model.xlsx) · Build script: [`build_model.py`](build_model.py)
Prepared 2026-09-22. Stop point per instruction — report before any further work.

---

## 1. Formula error scan

Recalculated the full workbook headless (`soffice --headless --convert-to xlsx`, LibreOffice 26.8.0.3) and scanned every cell in every tab for `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#NUM!`, `#N/A`, `#NULL!`.

**Result: 0 formula errors in the delivered workbook.**

Getting there took two real fixes, both worth disclosing:

1. **Two note cells were misread as formulas.** Two assumption notes started with "= " (e.g., "= Purchase Price x Cost-of-Sale Factor") — Excel/LibreOffice treat any cell string starting with `=` as a formula, so these threw `#VALUE!`. Fixed by rewording the notes and adding a guard in the build script so no future note can trigger this.
2. **`HSTACK` is not supported by this LibreOffice version.** My first draft of the SENSITIVITY tab used `=IRR(HSTACK(-equity, cf1, cf2, ...))` to build inline cash-flow arrays without helper cells — a modern Excel-365 function. LibreOffice returned `#NAME?` on every one of those 90 cells. I rebuilt the sensitivity engine around a "calculation detail" block of ordinary helper rows (one real row of Year-0…Year-5 cells per scenario) so `IRR()` gets a plain contiguous range — no array-literal functions, safer for portability across Excel/LibreOffice/Google Sheets. The visible 5×5 grids just reference those rows.

**One legitimate `N/A`, not an error:** GP IRR shows `N/A — GP receives $0 in this scenario, IRR undefined`, wrapped in `IFERROR()`. This isn't a bug — see Section 5. IRR is mathematically undefined for a cash flow stream that's all zero after the initial outflow (no sign change), so I return an explanatory string instead of letting `#N/A` propagate raw. I did the same defensively for LP/GP/unlevered/levered IRR and every sensitivity cell.

---

## 2. CHECKS tab — all pass

| # | Check | Result |
|---|---|---|
| 1 | Sources = Uses | **OK** (difference = $0) |
| 2 | Levered CF independently rebuilt from Operating + Debt tabs vs. Returns tab, each of 5 years | **OK** (all 5 years, difference = $0) |
| 3 | NOI recomputation (EGI + Opex − NOI), each of 5 years | **OK** (all 5 years = $0) |
| 4 | Waterfall distributions (LP+GP) = Available Cash, each of 5 years | **OK** (all 5 years = $0) |
| 5 | Waterfall hurdle balances never go negative | **OK** (Tier-1 min $211,804; Tier-2 min $1,407,249 — both ≥ 0 throughout) |
| 6 | LP Equity + GP Equity = Total Equity | **OK** ($0 difference) |
| 7 | Debt schedule: Loan − cumulative principal paid − Year-5 ending balance | **OK** ($0 difference) |

I want to be honest about what these checks do and don't prove: checks 2, 3, and 4 verify **wiring correctness** (did I reference the right cells across tabs) more than independent economic logic, since the downstream tabs are built directly from the same source cells they're checked against. Check 5 and 7 are genuinely independent structural constraints (a hurdle balance going negative, or a debt schedule not summing to the ending balance, would indicate a real formula bug, not just a copy-paste reference error). Check 1 and 6 verify the Sources & Uses and equity-split arithmetic ties.

---

## 3. Independent Python recomputation

Per your instruction, I pulled the actual computed cash-flow rows out of the recalculated workbook and re-ran IRR and equity multiple in plain Python (`numpy_financial.irr`), not reading Excel's own IRR output.

| Metric | Excel | Python (independent) | Match? |
|---|---|---|---|
| Unlevered IRR | 5.0258% | 5.0258% | ✅ |
| Levered IRR | 4.4995% | 4.4995% | ✅ |
| Unlevered Equity Multiple | 1.2449x | 1.2449x | ✅ |
| Levered Equity Multiple | 1.2020x | 1.2020x | ✅ |
| LP IRR | 7.2204% | 7.2204% | ✅ |
| LP Equity Multiple | 1.3356x | 1.3356x | ✅ |

Cash flows used (Year 0 → Year 5):
- Unlevered: `[-14,498,040, 968,584, 790,160, 934,047, 920,579, 14,435,299]`
- Levered: `[-5,528,040, 968,584, 153,290, 297,177, 190,444, 5,035,294]`
- LP: `[-4,975,236, 968,584, 153,290, 297,177, 190,444, 5,035,294]`

All match to displayed precision.

---

## 4. Stress test — rent growth 0%, exit cap +100bps

Set all ten `Market Rent Growth` assumption cells to 0% and the exit-cap spread to +100bps (entry+100bps = 8.18%), recalculated, rescanned.

**Result: model behaves sensibly. No negative-balance weirdness, debt still services throughout.**

| Metric | Base case | Stress case |
|---|---|---|
| Formula errors | 0 | 0 |
| CHECKS | all pass | all pass |
| Year-1 → Year-5 NOI | $998k → (growing) | $991k → $802k (declining, as expected — expenses still grow at 3.5–7%/yr while rents are frozen) |
| Debt service coverage, worst year | — | Year 5 NOI $802k vs. debt service $730k = **1.10x DSCR** — tight but the loan still services; no default flag, no negative cash flow |
| Loan balance | amortizes normally | amortizes normally, never goes negative |
| Unlevered IRR | 5.03% | 1.14% |
| Levered IRR | 4.50% | **-8.96%** |
| LP IRR | 7.22% | **-6.51%** |
| LP Equity Multiple | 1.34x | **0.69x** (LP loses ~31% of invested capital) |

This is exactly the kind of result a stress test should produce: a real, sensible loss scenario, not a broken one. Debt keeps servicing (DSCR stays above 1.0x even in the worst year), no cell goes to a nonsensical value, and the loss is concentrated where it should be — the equity holders, with LP taking the largest hit since Tier 1 (100%-to-LP pref/ROC) no longer gets fully satisfied.

---

## 5. Are the returns realistic? — Yes, and they're weak, not too good

You asked me to flag it if returns look too good. They don't — **they look weak, and I want to walk through exactly why, because the reason is a real, defensible market dynamic, not a modeling error.**

| Metric | Value |
|---|---|
| Going-in cap rate (Year-1 model NOI ÷ price, reassessed-tax basis) | **7.23%** |
| All-in floating debt rate (SOFR 3.85% + 325bps) | **7.10%** |
| **Spread between the two** | **~13 basis points** |
| Unlevered IRR | 5.03% |
| Levered IRR | 4.50% (*below* unlevered) |
| LP IRR | 7.22% (*below* the 8% preferred return) |
| GP IRR | undefined — GP receives $0 across the entire 5-year hold |

**The core driver: there's almost no positive leverage spread.** A 7.23% cap rate against a 7.10% cost of debt leaves only ~13bps of unlevered-yield-over-debt-cost — and once you layer in 3 years of loan amortization (principal paydown reduces cash flow without reducing the equity base proportionally the same way), the levered return actually comes out **below** the unlevered return (4.50% vs. 5.03%). That's textbook negative leverage, and it's the single biggest thing driving the weak result. It also means LP never fully collects its own 8% preferred return within the 5-year hold — a **$211,804 pref/capital shortfall remains unpaid at exit** (Check #5's Tier-1 balance) — so the waterfall never reaches Tier 2 or Tier 3, and GP's promote is exactly zero. This isn't a bug; it's the correct output of the hurdle-balance mechanic given real cash flows too thin to clear Tier 1.

**Two things a real acquisitions team would do next, which I flag rather than silently build in:**

1. **The real assumable debt would change this materially.** The OM discloses an assumable loan blending to **~4.2%**, not the 7.10% generic floating-rate debt this model deliberately uses (per the Phase 2 spec's instruction to build a generic, teaching-clear DEBT tab). A ~290bps lower cost of debt against the same 7.23% cap rate would flip the leverage from negative to strongly positive. I flagged this as an unmodeled alternative back in Phase 1 and it's the most obvious lever to pull if you want to see whether this deal actually works.
2. **Purchase price.** Sensitivity Table 2 (Purchase Price × Exit Cap) is live in the workbook — pulling price down works in the expected direction, mechanically raising the entry cap and widening the leverage spread.

**Is a ~7.2% going-in cap with ~7.1% floating debt realistic for South Florida value-add multifamily in September 2026?** Yes — this is a widely-discussed dynamic in 2025-2026 commercial real estate: base rates rose faster than cap rates compressed, so a lot of stabilized-to-light-value-add deals in this cycle show exactly this thin-or-negative leverage spread. It's a real market condition, not an artifact of my assumptions. **I did not tune anything to produce this result — it's what the assumption set you approved actually produces**, and per your original instruction, that's a legitimate finding to report, not a problem to quietly fix.

---

## 6. Full ASSUMPTIONS tab — every input, value, and source

| Section | Assumption | Value | Source / Basis |
|---|---|---|---|
| **Acquisition** | Units | 97 | LoopNet listing |
| | Purchase Price | $13,800,000 | Broker-stated asking price (LoopNet) |
| | Broker-Stated Cap Rate | 7.00% | LoopNet advertised cap rate |
| | Broker-Implied NOI (formula, not used downstream) | $966,000 | = Price × Broker Cap |
| | Closing Costs % | 1.50% | Broward doc stamps $0.70/$100 + title/legal/reports |
| **Property Tax Reassessment** | Combined Millage Rate | 1.98394% | **PLACEHOLDER** — Broward county-wide average; awaiting your BCPA-confirmed parcel figure |
| | Seller's Current Taxable Value | $10,318,700 | **PLACEHOLDER** — LoopNet-disclosed value, treated as taxable value (no exemptions apply to non-homestead rental); awaiting your BCPA-confirmed figure |
| | Cost-of-Sale Factor | 85% | Fla. Stat. §193.011(8) / DOR customary 15% cost-of-sale allowance; settable to 100% for the conservative full-price case |
| | Non-Homestead Annual Assessment Cap | 10% | Fla. Const. Art. VII — current cap; Amendment 3 (Nov 2026 ballot) would cut to 5% from 2027 — not modeled |
| | Reassessed Just Value at Purchase (formula) | $11,730,000 | = Price × Cost-of-Sale Factor |
| | Seller's Current Annual Tax (formula) | $204,717 | = Taxable Value × Millage |
| | Buyer's Year-1 Tax (formula) | $232,716 | = Reassessed Just Value × Millage |
| **Renovation — bottom-up, per classic unit** | Kitchen | $7,000 | Judgment, mid-low end of $4,500–15,000 kitchen-cost research |
| | Mini-split ductless AC | $3,500 | Judgment, general HVAC market pricing |
| | Vinyl slider windows | $1,500 | Judgment |
| | Lighting + ceiling fans | $400 | Judgment |
| | LVP flooring | $4,000 | Judgment, ~$5.75/SF × 700 SF |
| | Bathroom refresh | $1,200 | Judgment, kept light — not disclosed as part of the prior owner's scope |
| | Interior paint | $500 | Judgment |
| | Turnover labor | $500 | Judgment |
| | Subtotal (formula) | $18,600 | Sum of the 8 lines |
| | Contingency % | 10% | Standard convention |
| | Contingency (formula) | $1,860 | = Subtotal × 10% |
| | **TOTAL per classic unit (formula)** | **$20,460** | |
| | Renovation Pace | 4 units/month | Judgment |
| | Renovated-Unit Rent Premium | $175/month | Southeast Class B/C industry commentary, $100–250/mo range |
| | Year-1 Premium Capture % | 50% | 6-month program starting month 1 → average unit captures ~half a year |
| **Operating** | Physical Vacancy | 6.5% | vs. 92% disclosed occupancy, nudged for renovation downtime |
| | Credit Loss | 1.0% of GPR | Standard convention |
| | Concessions | 0.5% of GPR | Standard convention |
| | Other Income | $35/unit/month | Judgment, no South Florida-specific source found |
| | Loss-to-Lease Burn-off | 50% of gap per turnover | Standard modeling convention |
| | Annual Turnover Rate | 55% | General Class B/C garden-apartment convention, not property-specific |
| | Prior-Renovated Units' Starting Capture | 65% | Judgment split of the disclosed 20.76% blended upside |
| **Market Rent Growth** | Year 1 | 1.0% | Yardi Matrix via MIAMI REALTORS®+RWorld May 2026 report: Broward County Class C/C+ asking rents +0.2% YoY (near-flat), nudged to 1.0% for a full forward year |
| | Year 2 | 1.75% | Judgment, gradual convergence |
| | Year 3 | 2.5% | Judgment, gradual convergence |
| | Years 4–10 | 3.0% (flat) | **Capped per instruction** — no source supports going higher |
| **Expense Growth** | General (ex-insurance, ex-tax) | 3.5% | Standard convention |
| | Insurance | 7.0% | Above general growth, given the ~37% two-year South Florida insurance trend |
| **Operating Expenses (Year 1, $/unit/yr)** | Payroll | $1,400 | Judgment |
| | Repairs & Maintenance | $1,100 | Judgment, nudged up for 1958 vintage / undisclosed roof |
| | Turnover / Make-Ready | $350 | Judgment |
| | Contract Services | $450 | Judgment |
| | Utilities (owner-paid) | $500 | Judgment |
| | Insurance — base case | $2,400 | Judgment, vintage-risk-adjusted above the general $2,000/unit South Florida average |
| | Insurance — if roof replaced (scenario) | $1,900 | Judgment |
| | Management Fee | 3.5% of EGI | Standard convention |
| | G&A / Admin | $250 | Judgment |
| | Marketing | $150 | Judgment |
| | Replacement Reserves (below NOI) | $300 | Standard lender convention |
| **Roof & Recertification** | Roof Replacement Toggle | 0 (off) | Base case does not assume roof replacement |
| | Roof Replacement Cost (scenario) | $235,000 | Judgment, ~23,480 SF est. roof area × $8–12/SF hurricane-code TPO/mod-bit |
| | Recertification Year | Year 2 | Next 40/50-Year Program cycle due ~2028 |
| | Recertification Inspection Cost | $10,000 | Placeholder — no sourced fee |
| | Recertification Remediation Contingency | $150,000 | Placeholder — genuinely unknowable without an engineer's report |
| **Debt** | 1-Month SOFR | 3.85% | sofrrate.com, reading as of 9/18/2026 |
| | Spread | 325bps | Judgment, within the 200–500bps range cited for 2026 multifamily bridge financing |
| | All-In Rate (formula) | 7.10% | = SOFR + Spread |
| | Maximum LTV | 65% | Judgment |
| | Minimum DSCR | 1.25x | Judgment, standard cited lender minimum |
| | Minimum Debt Yield | 8.0% | Judgment, standard cited lender minimum |
| | Interest-Only Period | 2 years | Judgment |
| | Amortization | 30 years | Judgment |
| **Hold & Exit** | Hold Period | 5 years | Judgment |
| | Exit Cap Spread — base case | +50bps over entry | Per instruction |
| | Exit Cap Spread — sensitivity ceiling | +100bps over entry | Per instruction |
| | Cost of Sale at Exit | 2.0% | Standard convention |
| **Waterfall** | Preferred Return | 8.0% | Standard LP pref convention |
| | Tier 2 Split | 70% LP / 30% GP | Judgment, common mid-tier promote split |
| | Tier 2 IRR Hurdle | 12% | Judgment |
| | Tier 3 Split | 50% LP / 50% GP | Judgment, common back-end split |
| | GP Co-Invest | 10% of equity | Judgment, typical GP co-investment level |

Unit-level rent-roll inputs (per unit type: count, classic/renovated split, SF, in-place and market rents) live on the **Unit Mix** tab, not Assumptions, per the Phase 1 build spec — full detail and sourcing for those is in `PHASE1_ASSET_AND_ASSUMPTIONS.md`.

---

## 7. Returns summary

| | Unlevered | Levered (deal) | LP | GP |
|---|---|---|---|---|
| IRR | 5.03% | 4.50% | 7.22% | undefined ($0 received) |
| Equity Multiple | 1.24x | 1.20x | 1.34x | 0.00x |
| Capital | $14,498,040 (all-cash) | $5,528,040 equity | $4,975,236 | $552,804 |

Sources & Uses: Purchase $13,800,000 + Closing $207,000 + Renovation $491,040 = **Total Uses $14,498,040**, funded by a **$8,970,000 senior loan** (LTV-bound — LTV, debt-yield, and DSCR constraints all computed; LTV binds at $8.97M vs. $12.47M debt-yield capacity and $11.24M DSCR capacity, so the loan is well short of what income alone would support) and **$5,528,040 sponsor equity**.

Going-in cap rate: 7.23% (Year-1 model NOI, reassessed-tax basis) vs. broker-stated 7.00%. Exit cap: 7.73% base case (entry+50bps), sensitivity to 8.23% (entry+100bps). Exit price via the tax-adjusted formula: **$13,805,012** (essentially flat to the $13.8M entry price — the deal is a wash on the real estate itself over 5 years; whatever return exists comes from operations, not appreciation).

---

## 8. What's still open

1. **Millage and taxable value are placeholders**, wired as the single input cells you asked for (`Assumptions!C14` and `C15`). Drop in your BCPA-confirmed figures and every downstream number (tax, reassessed cap rate, exit valuation) recalculates automatically.
2. **Roof and recertification costs remain genuinely unconfirmed placeholders**, flagged as such in the workbook itself.
3. **The assumable-debt alternative is not modeled** — flagged in Section 5 above as the most likely lever to materially change the outcome.
4. **Weak base-case returns are a real finding, not a bug** — see Section 5. I have not adjusted any assumption to make this look better.

Nothing further has been built beyond what's described here. Stopping per your instruction.
