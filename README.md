# Parkview Crossing Acquisition Model

An underwriting model for the purchase of Parkview Crossing, a 97-unit garden apartment property at 901-951 NW 8th Ave, Pompano Beach, Florida (Broward County), built in 1958-59 and listed at $13.8M. The workbook is live-formula Excel: inputs are blue cells on the Assumptions and Unit Mix tabs, and every other number is a formula. A separate Python script recomputes the model from the inputs alone and compares it line by line with the workbook.

**Finding: at the $13.8M asking price the deal does not work.** The base case (assuming the seller's loans) produces a 4.19% levered IRR and a 1.20x equity multiple over five years, below the 8% preferred return, so the GP earns no promote. The price at which the LP earns 8% is about $13.1M, 5% below the ask. At the ask, leverage lowers returns: the unlevered IRR is 5.53%.

All figures in this README come from the current workbook. `verify_model.py` reproduces them (945 figures, within $1 or 1 bp).

## Contents

1. Deal and thesis
2. How the workbook is organized
3. Key assumptions and sources
4. Florida property tax: what the model does and why
5. Why the renovation premium is $0
6. Results
7. How the model is verified
8. Limitations
9. How to run it
10. Earlier working reports

## 1. Deal and thesis

**The property.** 97 units in seven two-story concrete-block buildings on 2.39 acres. The unit mix is 19 studios, 51 one-bed/one-bath, 17 two-bed/one-bath and 10 two-bed/two-bath. The unit count is the Broward County Property Appraiser's (BCPA) record across three folios:

| Folio | Address | Units |
|---|---|---|
| 4842-35-00-0460 | 951 NW 8 Ave | 20 |
| 4842-35-00-0471 | 901 NW 8 Ave | 18 |
| 4842-35-00-0480 | 930-980 NW 9 Ave | 59 |

The listing's unit-type breakdown sums to 98. The model follows BCPA and removes one 1BR/1BA unit.

**Ownership history.** The owner of record is Channel Grove LLC, which bought the three folios together on 12/23/2021 for $11,760,000 ($121,237/unit). The $13.8M ask is 17.3% above that price, roughly 3.4% a year.

**Condition.** Per the listing, the current owner has already renovated about 75% of the units: kitchens, mini-split AC, vinyl windows and lighting. The owner also reports over $1M of building-wide work, including electrical supply lines and panels, fencing and gates, parking, and security.

**Thesis: light value-add, not a repositioning.** The buyer finishes a program someone else mostly completed. The return drivers are:
1. **The last 24 classic units.** Renovating them at $20,460 per unit brings them from in-place rent up to market.
2. **Loss-to-lease burn-off.** The already-renovated units are modeled at 65% of the way from in-place rent to market. Each time a unit turns over, half of the remaining gap closes.
3. **Market rent growth.** 1.0% in Year 1, rising to 3.0% by Year 4, and 3.0% thereafter.
4. **Holding expenses down.** This matters most for insurance and property tax.

**Financing.** The listing offers an assumable first mortgage of $5,887,000 at 3.0% fixed until December 2029, plus a $3,563,000 supplemental loan at 6.20%. Assuming that debt is the base case (Scenario A). New agency financing is the alternative (Scenario B).

**Alternative considered: Florida's Live Local Act.** The Live Local Act (HB 1389, effective July 1, 2026) exempts qualifying properties from property tax. It requires at least 71 units, with 40% set aside as affordable for 30 years. Parkview Crossing meets the size test, but the strategy was not modeled. This plan's returns depend on moving rents toward market on the same units the Act would cap below market, so the two strategies conflict.

## 2. How the workbook is organized

`Parkview_Crossing_Acquisition_Model.xlsx` has ten tabs. Every tab title says which debt scenario it shows.

| Tab | What it holds |
|---|---|
| Assumptions | Every input (blue) with its source or the word JUDGMENT. Also derived values: reassessed tax, water/sewer and trash cost per unit, agency rate, exit cap. |
| Unit Mix | Unit counts, in-place and market rent by unit type, renovation capex by type. |
| Operating Model | Ten years of rent tracks by unit type, income, every expense line, NOI, reserves, one-time capex and unlevered cash flow. Debt-agnostic. |
| Debt | Scenario B sizing (LTV vs. DSCR) and amortization. |
| Capital | Scenario B sources and uses, and the LP/GP equity split. |
| Returns | NOI bridge from the broker's cap rate to the Day-0 in-place cap rate, cap rates three ways, the tax-adjusted exit, unlevered returns, and Scenario B levered returns. |
| Debt (Assumed) | Scenario A: the lender's paydown test at assumption, both assumed loans, the Year-4 refinance, and the prepayment premium. |
| Returns (Assumed) | Scenario A sources and uses, cash flows, IRR, multiple, capital call and peak equity. |
| Waterfall | LP/GP distribution of the Scenario A cash flows, tier by tier and year by year. |
| Sensitivity | Tables 1-3 on Scenario A: exit cap x price, exit cap x rent growth, and renovation premium x renovation cost. Table 4 is exit cap x price on Scenario B. Each grid cell has its own calculation block. |
| Checks | 27 internal checks: sources = uses, each Scenario B levered cash flow rebuilt from the operating and debt tabs, NOI recomputation, waterfall distributions = available cash, hurdle balances never negative, LP + GP equity = total equity, debt schedules roll forward, and each sensitivity base cell = the model IRR. |
| Summary | Headline sources and uses, cap rates, returns, a comparison of the two debt scenarios, and bid prices. |

**Scripts.**

| Script | What it does |
|---|---|
| `build_model.py` | Writes the workbook. |
| `verify_model.py` | Independent recomputation and line-by-line comparison. See section 7. |
| `price_solve.py` | Maximum price for each target return, under both debt scenarios. Writes `bid_prices.json`, which the builder reads into the Summary tab. |
| `bridge.py` | Reproduces the prior 5.20% base case and walks it to the current one, one change at a time. |

## 3. Key assumptions and sources

"JUDGMENT" means no source was found and the number is my estimate. Those are the ones to test first in diligence.

| Assumption | Value | Source |
|---|---|---|
| Price | $13,800,000 ($142,268/unit) | [LoopNet listing](https://www.loopnet.com/Listing/901-951-NW-8th-Ave-Pompano-Beach-FL/41107583/) |
| Units | 97 | BCPA parcel records (3 folios) |
| Seller's 2025 taxable value | $10,318,700 | BCPA, sum of three folios; matches the listing |
| Millage | 20.1710 mills | BCPA 2026 proposed millage, code 1512. 2025 final was 20.2573. |
| Reassessed value | Price x 85% | Fla. Stat. 193.011(8) cost-of-sale factor. BCPA's 2026 working just value, $11.65M, is within 1% of $11.73M. |
| Property tax growth | 3.0%/yr | Tied to terminal market rent growth. See section 4. |
| Non-ad valorem charges | $375/unit | BCPA 2025 bills: total $245,413, minus $209,026 ad valorem, divided by 97 units. Mainly the city fire assessment. |
| Market rents, in-place rents | By unit type | Broker's disclosed 20.76% blended upside plus apartments.com Pompano 33060 averages. JUDGMENT on the split by unit type. Weakest-sourced input. |
| Rent growth | 1.0%, 1.75%, 2.5%, then 3.0% | Year 1: Yardi Matrix Broward Class C/C+ asking rents +0.2% YoY (via MIAMI REALTORS, May 2026). Later years: JUDGMENT, capped at 3.0%. |
| Vacancy / credit loss / concessions | 6.5% / 1.0% / 0.5% | JUDGMENT. The listing reports 92% occupancy. |
| Other income, excluding utility recovery | $15/unit/month | JUDGMENT (laundry, fees, pet) |
| Water and sewer | $630/unit/yr, growing 6%/yr | [Pompano Beach Code 50.03](https://codelibrary.amlegal.com/codes/pompanobeach/latest/pompanobeach_fl/0-0-0-93003) and [51.05](https://codelibrary.amlegal.com/codes/pompanobeach/latest/pompanobeach_fl/0-0-0-80354), FY2027 multifamily rates. Usage of 3,000 gal/unit/month and 7 meters are JUDGMENT. |
| Trash | $170/unit/yr | [Pompano Beach 2025-26 solid waste rates](https://cdn.pompanobeachfl.gov/city/pages/solid_waste/2025-2026-DISPOSAL-RATES-New.pdf): 6-yd container, 2x/week, $457.63/month. Container count (3) is JUDGMENT. |
| Who pays water, sewer, trash | Owner, with 60% RUBS recovery | Listing is silent (the OM is gated). Owner-paid is assumed; 60% recovery is JUDGMENT. Diligence item. |
| Insurance | $2,400/unit, growing 7%/yr | JUDGMENT. Marked up from about $2,000/unit for an undisclosed roof. The growth rate is conservative given 2026 reinsurance pricing: [Insurance Journal](https://www.insurancejournal.com/news/southeast/2026/06/30/875651.htm) reports Florida property-cat reinsurance down 15-20% at June renewals. |
| Payroll / R&M / turnover / contract / common utilities / G&A / marketing | $1,400 / $1,100 / $350 / $280 / $500 / $250 / $150 per unit | JUDGMENT. Turnover is at the low end. |
| Management fee | 3.5% of EGI | JUDGMENT; low end for 97 units |
| Replacement reserves | $300/unit | JUDGMENT; low end for this vintage |
| Renovation scope | $20,460/unit x 24 classic units | Bottom-up, eight line items + 10% contingency |
| Recertification | $160,000 in Year 2 | Broward 40/50-year program; cost is a placeholder |
| Assumed first mortgage | $5,887,000 at 3.0%, matures Dec 2029 (Year 3) | Crexi / LoopNet |
| Supplemental loan | $3,563,000 at 6.20% | Crexi / LoopNet |
| Interest-only status of assumed loans | Interest-only | JUDGMENT, not disclosed |
| Assumption fee / paydown test | 0.5% / 75% max LTV on price | JUDGMENT |
| 10-year Treasury | 5.24% | [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), 9/28/2026 |
| Agency spread | 200 bps (all-in 7.24% fixed) | JUDGMENT within broker ranges. [multifamily.loans](https://www.multifamily.loans/multifamily-mortgage-rates/) cites 200-250 bps typical. [apartmentloanstore](https://apartmentloanstore.com/loan-product/apartment-multifamily-loan-interest-rates) Fannie quotes on 9/29/2026 imply about 105-165 bps for larger, better assets. |
| Agency terms | 75% max LTV, 1.25x DSCR on amortizing payment, 30-yr amortization, no IO | [Fannie Mae Small Loan term sheet](https://multifamily.fanniemae.com/financing-options/small-loans/small-mortgage-loan-program-term-sheet): up to $9M, 80% LTV, 1.25x. 75% and no IO are JUDGMENT. |
| Prepayment premium | 10-yr schedule 5-5-4-4-3-3-2-2-1-1 | [Fannie Mae declining prepayment premium](https://multifamily.fanniemae.com/financing-options/rate-lock-and-prepay-options/declining-prepayment-premium-term-sheet) |
| Exit cap | 6.60% = 5.60% market + 100 bps | See below. |
| Cost of sale at exit | 2.0% | JUDGMENT |
| Waterfall | 8% pref; 70/30 to a 12% IRR; 50/50 above | Standard structure. GP co-invests 10% pari passu. No fees. |

**Exit cap evidence.**
- **Market anchor.** [Matthews, Fort Lauderdale Q3 2025](https://www.matthews.com/insights/fort-lauderdale) puts the Fort Lauderdale multifamily average at 5.6%. [Colliers, South Florida Q1 2026](https://www.colliers.com/en/research/miami/sfl-multifamily-report-26q1) says cap rates are holding "near 5.0%" across all three counties.
- **Class C / vintage spread.** The 100 bps added for a Class C building that will be about 73 years old at exit is JUDGMENT. [CBRE's H1 2026 survey](https://www.cbre.com/insights/reports/us-cap-rate-survey-h1-2026) says expectations of rising cap rates are strongest for Class C assets, but its market-level tables are gated.
- **Named comps.** I checked the two comps named in the instructions. [Cascades at the Hammocks](https://crenews.com/2026/05/06/bowery-properties-buys-264-unit-apartment-complex-in-miami-for-65-5mln/) sold for $65.5M, or $248,106/unit (264 units, built 1988, May 2026). [Savona Grand](https://hoodline.com/2026/07/tampa-landlord-nabs-savona-grand-between-boynton-and-lake-worth-6942770/) sold in July 2026 at an undisclosed price. Neither has a public price-and-NOI pair, so no implied cap rate is available.
- **Not used as "market."** The exit cap is deliberately not tied to this deal's own entry cap. It is also used as the lender's cap rate when the Year-4 refinance is sized.

## 4. Florida property tax: what the model does and why

**At purchase.** Florida reassesses non-homestead property to just value on the January 1 after a sale. The model estimates that just value as the price times 85%. The 85% is the cost-of-sale allowance under Fla. Stat. 193.011(8), which directs the appraiser to consider the net proceeds of a sale after the usual costs of sale.
- At $13.8M, reassessed value is $11.73M and Year-1 tax is $236,606, against the seller's current $208,139.
- BCPA's own 2026 working just value is $11.65M, which supports the method.

**The 10% cap is a ceiling, not a growth rate.** Fla. Stat. 193.1555(3) limits increases in the *assessed* value of non-homestead property with 10 or more units to 10% a year. Section 193.1554(1) covers residential property of nine or fewer units, which is why a 97-unit property falls under 193.1555. The cap applies to non-school levies only (193.1555(2)). It exists so that an owner whose market value rose faster than 10% catches up gradually.
- After a sale resets assessed value to just value, there is no gap to catch up. Assessed value then follows just value, and tax grows with market value.
- An earlier version of this model grew tax at 10% every year. That was a misreading, and it made NOI fall every year of the hold.
- The model now grows tax at 3.0%, tied by formula to the model's terminal market rent growth. The cap only binds if just value grows faster than 10%.
- Amendment 3 (November 2026 ballot, a 5% cap) is not modeled.

**Timing simplification.** Strictly, reassessment takes effect the January 1 after closing, so part of Year 1 would still be taxed on the seller's assessment. The model taxes the reassessed value from Year 1. Because BCPA's 2026 working value is already within 1% of the reassessed figure, the difference is small.

**At exit.** The next buyer is reassessed too, so the exit value in the model accounts for the buyer's tax.
- The problem is circular: the buyer's NOI after tax depends on the price, which is what we are solving for.
- The fix is to capitalize NOI *before* property tax at the exit cap plus the effective tax rate (millage x 85% = 1.71%): `Price = NOI before tax / (exit cap + effective tax rate)`.
- This follows from `exit cap = (NOI before tax - tax rate x Price) / Price`.
- Year-6 NOI before tax is $1,209,117, so exit price = $1,209,117 / (6.60% + 1.71%) = $14,542,213.

## 5. Why the renovation premium is $0

The 24 classic units are renovated to the same standard the owner used on the other 73. The market rents in the Unit Mix tab are what renovated units command. Treating our renovated units as earning market rent *plus* a premium would count the same upgrade twice.
- The renovation's value is closing the gap between in-place and market rent, about $300/month per unit.
- An earlier version used a $175/month premium. Sensitivity Table 3 shows what a premium would be worth: each $50/month adds about 74 bps of levered IRR.
- Year 1 captures half of that gap, because renovations run through the first six months. From Year 2 on, renovated units are at full market rent.
- Fixing a bug in that logic was worth 267 bps. Earlier versions compounded the half-captured Year-1 rent forward, so those 24 units never reached market.

## 6. Results

**Base case: Scenario A, assumed debt, $13.8M, 5-year hold.**

| | |
|---|---|
| Total uses | $14,545,290 (price, $207,000 closing, $491,040 renovation, $47,250 assumption fee) |
| Assumed debt / equity | $9,450,000 / $5,095,290 (LP $4,585,761, GP $509,529) |
| Cap rates | Broker 7.0%; Day-0 in-place with reassessed tax 5.86%; Year-1 forward 6.36% |
| Year-1 NOI | $878,230. Expenses are $10,736/unit, 54.3% of EGI. |
| Exit | 6.60% cap, $14,542,213 ($149,920/unit) |
| Refinance (Year 4) | Refi-year NOI is $920,697 and value at refi is $13,949,955. The DSCR limit binds at $8,923,868 against a $9,450,000 payoff. That requires $526,132 of cash, of which $38,965 is a Year-3 capital call. |
| Prepayment premium at sale | $436,819 (5% of the refi loan, in its second loan year) |
| Levered cash flows | −5,095,290 / 451,614 / 328,301 / −38,965 / 151,876 / 5,235,467 |
| **Levered IRR / multiple** | **4.19% / 1.20x**. LP and GP both 4.19%, promote $0. |
| Unlevered IRR / multiple | 5.53% / 1.28x |
| Year-1 cash-on-cash | 8.86% |

**Scenario B, new agency debt.** The DSCR limit binds, giving an $8,512,260 loan (61.7% LTV) at 7.24%. Equity is $5,985,780. Levered IRR is 2.45%, the multiple 1.12x, and Year-1 cash-on-cash 2.45%.
- The 3.0% assumed loan is worth about 174 bps of IRR against new debt.
- Both scenarios return less than the unlevered 5.53%. Debt at 7.24% costs more than the property yields (6.36% in Year 1), and there is a prepayment premium at sale.

**Maximum bid price.** Each row is solved on the verified engine. The three Scenario A prices were also built as full workbooks and verified, and each returns its target exactly.

| Target | Scenario A (assumed) | Scenario B (new debt) |
|---|---|---|
| LP IRR 8% | $13,105,989 ($135,113/unit, −5.0%, 6.26% in-place cap) | $12,572,261 ($129,611/unit, −8.9%) |
| Levered IRR 12% | $12,510,415 ($128,973/unit, −9.3%); LP 10.86%, GP 20.50% | $11,921,109 ($122,898/unit, −13.6%) |
| Levered IRR 15% | $12,081,610 ($124,553/unit, −12.5%); LP 12.79%, GP 29.46% | $11,458,598 ($118,130/unit, −17.0%) |

Below about $12.6M, the assumption test (75% of price) forces a paydown at closing: $67,189 at the 12% price and $388,793 at the 15% price. The 8% price is still 11.4% above the 2021 sale.

**Sensitivity (Scenario A levered IRR).**
- **Exit cap.** At the ask, each 50 bps of exit cap moves IRR by about 3.2 points. The range runs from 10.58% at 5.60% to −2.31% at 7.60%.
- **Rent growth.** Adding or subtracting 0.5% to every year's rent growth moves IRR by about +2.2 or −2.2 points.
- **Price.** Buying 10% below the ask ($12.42M) gives 12.62%.
- **Renovation.** Renovation cost ±20% moves IRR by about ±0.45 points.

## 7. How the model is verified

`verify_model.py` reads only the literal input cells on Assumptions and Unit Mix. It finds each by its label and fails if any of them is a formula. It then rebuilds the model with its own code, which shares nothing with `build_model.py`, and compares its results with the recalculated workbook.

**What it compares.**
- Every Operating Model line for ten years.
- The NOI bridge and cap rates.
- The exit.
- Both debt schedules, including the assumption paydown and the refinance.
- Both scenarios' sources and uses, cash flows, IRRs and multiples.
- The waterfall, tier by tier.
- The Summary headline cells.
- All 200 sensitivity cells. Each is recomputed by a full re-run of the engine with the axis inputs changed, not by copying the workbook's per-cell calculation.

**How the waterfall is checked.** The workbook rolls hurdle balances forward year by year. The script instead solves each year in closed form from the future value of the whole investor cash-flow history. It also asserts two things: LP + GP equals available cash each year, and with no promote, LP IRR = GP IRR = deal IRR.

**Current result.** 219 lines, 945 figures, all within $1 or 1 bp. The same holds for the variant workbooks at $12.0M (all three waterfall tiers pay out) and at each Scenario A bid price.

**What verification does not prove.** It shows the formulas do what the author intended. It does not validate the assumptions, and the same author wrote both implementations. Two bugs were missed by both until a reviewer or a new test caught them:
- the subordinated GP co-invest (found in review);
- the classic-unit rent track (found while rebuilding the renovation sensitivity table).

## 8. Limitations

- **No T-12 or rent roll.** Rents by unit type, the classic/renovated split, and every expense line are estimates. Water use, meter count, RUBS recovery, trash containers and the utility-payer assumption are the least certain inputs added in this round.
- **Roof and recertification are unknown.** A roof-replacement case is in the model as a toggle (off). The Year-2 recertification cost is a placeholder.
- **Assumed-loan terms are partly undisclosed.** Whether the loans are interest-only, the assumption fee, and the lender's approval test are all judgment. The first mortgage balance differs by $21,934 between the two listings.
- **Rates are held flat.** There is no forward curve for the 10-year Treasury.
- **The agency spread is an estimate, not a quote.** Loan fees and third-party reports are assumed to be inside the 1.5% closing costs.
- **The refinance uses a 10-year fixed loan and is prepaid in its second year.** The 5% premium costs about 160 bps of IRR. A real sponsor would likely choose a shorter term, a floating-rate agency loan, or a sale with loan assumption. The model follows the instruction to price off the 10-year Treasury.
- **The exit cap spread is judgment.** No implied cap rate was available for the named comps, and the Class C spread is not sourced.
- **Insurance growth of 7% is likely conservative.** It was left unchanged.
- **The management fee, turnover cost and reserves are at the low end.** Moving them to mid-range would lower returns further (see `STEPS_4-6.md`, Step 6).
- **The waterfall has no fees, no GP catch-up and no clawback.** The hold is fixed at five years.
- **The Summary bid prices are solver output, not live formulas.** Re-run `price_solve.py`, then `build_model.py`, after any input change.

## 9. How to run it

```bash
python3 build_model.py
```

```bash
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --norestore --convert-to xlsx --outdir _recalc model_wip.xlsx
```

```bash
cp _recalc/model_wip.xlsx Parkview_Crossing_Acquisition_Model.xlsx
```

```bash
python3 verify_model.py
```

```bash
python3 price_solve.py
```

```bash
python3 bridge.py
```

Requires Python 3 with `openpyxl`, `numpy_financial` and `scipy`, plus LibreOffice for recalculation. Excel recalculates the workbook on open.

## 10. Earlier working reports

These files record how the model got here. The numbers in them are from earlier versions and are superseded by this README.
- `PHASE1_ASSET_AND_ASSUMPTIONS.md`
- `PHASE3_VERIFICATION.md`
- `NOI_BRIDGE_AND_DEBT_SCENARIOS.md`
- `EXIT_CAP_BASE_CASE_AND_BID_PRICE.md`
- `VERIFICATION_STEPS_1-3.md`
- `STEPS_4-6.md`
- `FLAGS_A-D_AND_STEPS_7-9.md`

Also in the repo:
- `WATERFALL_WALKTHROUGH.md` walks through the LP/GP split with real numbers.
- `INTERVIEW_QA.md` has the questions a reviewer is likely to ask.
- `ONE_PAGE_SUMMARY.md` / `.pdf` is the one-page summary.
