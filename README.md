# Parkview Crossing Acquisition Model

An underwriting model for the purchase of Parkview Crossing, a 97-unit garden apartment property at 901-951 NW 8th Ave, Pompano Beach, Florida (Broward County), built in 1958-59 and listed at $13.8M. The workbook is live-formula Excel: inputs are blue cells on the Assumptions and Unit Mix tabs, and every other number is a formula. A separate Python script recomputes the model from the inputs alone and compares it line by line with the workbook.

**Finding: at the $13.8M asking price the deal does not work.** The base case assumes the seller's loans, refinances into a short floating-rate loan with a rate cap when the 3.0% loan matures in December 2029, and sells at the end of Year 5.
- Levered IRR 5.73% and a 1.29x multiple, below the 8% preferred return, so the GP earns no promote.
- The price at which the LP earns 8% is $13,369,967, 3.1% below the ask.

All figures in this README come from the current workbook. `verify_model.py` reproduces them (1,080 figures, within $1 or 1 bp).

## Contents

1. Deal and thesis
2. How the workbook is organized
3. Key assumptions and sources
4. Florida property tax: what the model does and why
5. Why the renovation premium is $0
6. The exit plan: what happens when the 3.0% loan matures
7. Five judgment calls, and why
8. Results
9. How the model is verified
10. Limitations
11. How to run it
12. Earlier working reports

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

**Financing.** The listing offers an assumable first mortgage of $5,887,000 at 3.0% fixed until December 2029, plus a $3,563,000 supplemental loan at 6.20%.
- **Scenario A (base case).** Assume that debt. Section 6 covers what happens when it matures.
- **Scenario B (alternative).** New 5-year agency fixed financing at closing, with the term matched to the 5-year hold.

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
| Debt (Assumed) | Scenario A: the lender's paydown test at assumption, both assumed loans, and three refinance options at maturity (floating + cap, 5-year fixed, 10-year fixed), each with sizing, schedule, cap cost, prepayment premium and financing cost. |
| Returns (Assumed) | Scenario A sources and uses; cash flows, IRR, multiple and capital call for each exit plan; a comparison table; and the selected base case. |
| Waterfall | LP/GP distribution of the Scenario A cash flows, tier by tier and year by year. |
| Sensitivity | Tables 1-3 on Scenario A: exit cap x price, exit cap x rent growth, and renovation premium x renovation cost. Table 4 is exit cap x price on Scenario B. Each grid cell has its own calculation block. |
| Checks | 30 internal checks: sources = uses, each Scenario B levered cash flow rebuilt from the operating and debt tabs, NOI recomputation, waterfall distributions = available cash, hurdle balances never negative, LP + GP equity = total equity, every debt schedule rolls forward, the base case equals the chosen plan, and each sensitivity base cell = the model IRR. |
| Summary | Headline sources and uses, cap rates, returns, the exit-plan comparison, a comparison of the two debt scenarios, and bid prices. |

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
| 10-year Treasury | 5.24% | [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), observation 9/28/2026 (the latest FRED print as of 9/30/2026) |
| Agency spread | 200 bps (5-yr fixed 7.06% for Scenario B and plan 2b; 10-yr fixed 7.24% for the plan-3 comparison) | JUDGMENT within broker ranges. [multifamily.loans](https://www.multifamily.loans/multifamily-mortgage-rates/) cites 200-250 bps typical. [apartmentloanstore](https://apartmentloanstore.com/loan-product/apartment-multifamily-loan-interest-rates) Fannie quotes on 9/29/2026 imply about 105-165 bps for larger, better assets. |
| Agency terms | 75% max LTV, 1.25x DSCR on amortizing payment, 30-yr amortization, no IO | [Fannie Mae Small Loan term sheet](https://multifamily.fanniemae.com/financing-options/small-loans/small-mortgage-loan-program-term-sheet): up to $9M, 80% LTV, 1.25x. 75% and no IO are JUDGMENT. |
| Prepayment premium | 10-yr schedule 5-5-4-4-3-3-2-2-1-1; 5-yr schedule 5-4-3-2-1 | [Fannie Mae declining prepayment premium](https://multifamily.fanniemae.com/financing-options/rate-lock-and-prepay-options/declining-prepayment-premium-term-sheet) |
| Base-case refinance (Dec 2029) | 30-day average SOFR 3.7307% + 300 bps = 6.73%, interest-only, open at sale | SOFR: [FRED SOFR30DAYAVG](https://fred.stlouisfed.org/series/SOFR30DAYAVG), observation 9/28/2026, the same date as the Treasury inputs. Spread: [multifamily-usa.com](https://multifamily-usa.com/rates/) (Sept 2026), "SOFR + ~275-325 bps before cap" for 12-month floating plus extensions on light value-add; midpoint. Interest-only and no prepayment premium after month 12 are JUDGMENT. |
| Rate cap | 2 years, 4.50% SOFR strike, 1.08% of the loan | [BlueGamma cap calculator](https://www.bluegamma.io/calculators/interest-rate-cap-calculator), priced 9/29/2026: $108,000 on $10M, indicative mid-market, excluding bank charges. The strike is JUDGMENT. The loan is sized at 1.25x DSCR on the capped rate (7.50%). |
| 5-year agency fixed (Scenario B; plan 2b) | 5-yr Treasury 5.06% + 200 bps = 7.06% | [FRED DGS5](https://fred.stlouisfed.org/series/DGS5), observation 9/28/2026 (the latest FRED print as of 9/30/2026) |
| Scenario B loan term | 5 years, matched to the hold; repaid at maturity with no prepayment premium | Fannie Small Loan terms allow 5-30 years |
| Exit cap | 6.60% = 5.60% market + 100 bps | See below. |
| Cost of sale at exit | 2.0% | JUDGMENT |
| Waterfall | 8% pref; 70/30 to a 12% IRR; 50/50 above | Standard structure. GP co-invests 10% pari passu. No fees. |

**Exit cap evidence.**
- **Market anchor.** [Matthews, Fort Lauderdale Q3 2025](https://www.matthews.com/insights/fort-lauderdale) puts the Fort Lauderdale multifamily average at 5.6%. [Colliers, South Florida Q1 2026](https://www.colliers.com/en/research/miami/sfl-multifamily-report-26q1) says cap rates are holding "near 5.0%" across all three counties.
- **Class C / vintage spread.** The 100 bps added for a Class C building that will be about 73 years old at exit is JUDGMENT. [CBRE's H1 2026 survey](https://www.cbre.com/insights/reports/us-cap-rate-survey-h1-2026) says expectations of rising cap rates are strongest for Class C assets, but its market-level tables are gated.
- **Named comps.** I checked the two comps named in the instructions. [Cascades at the Hammocks](https://crenews.com/2026/05/06/bowery-properties-buys-264-unit-apartment-complex-in-miami-for-65-5mln/) sold for $65.5M, or $248,106/unit (264 units, built 1988, May 2026). [Savona Grand](https://hoodline.com/2026/07/tampa-landlord-nabs-savona-grand-between-boynton-and-lake-worth-6942770/) sold in July 2026 at an undisclosed price. Neither has a public price-and-NOI pair, so no implied cap rate is available.
- **Not used as "market."** The exit cap is deliberately not tied to this deal's own entry cap. It is also used as the lender's cap rate when the refinance is sized, and for the sale-at-maturity price.

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
- An earlier version used a $175/month premium. Sensitivity Table 3 shows what a premium would be worth: each $50/month adds about 73 bps of levered IRR.
- Year 1 captures half of that gap, because renovations run through the first six months. From Year 2 on, renovated units are at full market rent.
- Fixing a bug in that logic was worth 267 bps. Earlier versions compounded the half-captured Year-1 rent forward, so those 24 units never reached market.

## 6. The exit plan: what happens when the 3.0% loan matures

The first mortgage is fixed at 3.0% only until December 2029, the end of Year 3. The whole $9.45M has to be repaid then. The model compares three plans at the same price.

**The plans.**
1. **Sell at maturity.** Sell at the end of 2029, pricing the sale on Year-4 NOI at the same 6.60% exit cap. The hold is about 3 years.
2. **Short refinance.** Refinance at maturity into a loan that can be prepaid cheaply at the 2031 sale. There are two versions, and the model uses whichever has the lower financing cost:
   - **(a) Floating.** SOFR + 300 bps (6.73%) with a purchased 2-year rate cap, interest-only, open at sale.
   - **(b) 5-year agency fixed.** 7.06%, with the 5-4-3-2-1 prepayment premium (4% at a sale in loan year 2).
3. **10-year agency fixed refinance.** The prior structure, 7.24%, with a 5% premium at sale. Kept only as a comparison row.

| Plan | Levered IRR | Multiple | Capital call | Refi financing cost (% of loan per year) |
|---|---|---|---|---|
| 1. Sell at maturity (3-year hold) | 4.23% | 1.12x | $0 | n/a |
| **2a. Short refi: floating + cap (base case)** | **5.73%** | **1.29x** | $357,752 | 7.27% |
| 2b. Short refi: 5-year fixed | 4.58% | 1.22x | $0 | 8.98% |
| 3. 10-year fixed refi (comparison) | 4.19% | 1.20x | $38,965 | 9.65% |

**Cost of the two short refinances.** The costs are over the two years each loan is outstanding.
- **Floating.** Loan $8,699,030. Interest $1,171,015 + cap $93,950 + no prepayment premium = **$1,264,964**, or 7.27% of the loan per year.
- **5-year fixed.** Loan $9,085,154. Interest $1,276,106 + prepayment premium $355,526 = **$1,631,632**, or 8.98% per year.

**Why the base case is 2a.** A sponsor who buys to take over a 3.0% loan plans around its maturity, and the three plans are what that date forces.
- **Selling at maturity costs return.** It avoids refinancing risk, but it pays acquisition and sale costs over a 3-year hold, and it sells before the renovated units and burn-off have shown two full years of higher NOI. It returns 4.23%.
- **Refinancing is the better route, but only into debt that can be repaid cheaply in 2031.** A 10-year or 5-year fixed loan repaid in its second year pays a 5% or 4% premium, which is where most of its cost comes from.
- **The floating loan with a cap is cheapest.** It costs 7.27% a year against 8.98% for the 5-year fixed. The 4.50% SOFR strike limits the rate risk: with SOFR at the strike for both years (an all-in 7.50%), the plan still returns 5.26%, above both alternatives.
- **The costs.** It needs a larger Year-3 equity contribution ($357,752), because a loan sized on the capped rate is smaller. It also depends on a floating loan being available in 2029: agency floating programs start at $10M (Freddie Mac) or $25M (Fannie Mae SARM), so this would be a bank or bridge loan.

## 7. Five judgment calls, and why

These were reviewed and kept as they are.

**1. RUBS recovery of 60% of the owner's water, sewer and trash cost.** The listing does not say who pays utilities or whether leases carry a bill-back clause.
- Fully implemented RUBS programs recover more than 60%. But recovery here depends on the lease form, vacancy (6.5%), any caps, and phasing in as leases turn over (55% a year).
- 60% is a middle case below full recovery.
- Each 10 points of recovery is about $7,800 a year of NOI (Year-1 cost is $77,553). At 50% the IRR is 5.19%; at 70% it is 6.28%.

**2. Water use of 3,000 gallons per unit per month.** About 72% of the units are studios or one-bedrooms.
- 3,000 gallons a month is roughly 1.5 occupants at about 65 gallons per person per day. That is a judgment, not a measured figure.
- At 2,000 gallons the IRR is 6.05%; at 4,000 it is 5.41%.
- The owner's water bills would replace this.

**3. A 100 bps Class C / vintage spread on the exit cap (6.60% = 5.60% + 1.00%).**
- The market averages (Matthews 5.6%, Colliers about 5.0%) are dominated by newer buildings. At sale this will be a Class C building about 73 years old.
- CBRE reports that cap-rate expansion expectations are strongest for Class C.
- The 6.60% exit is 74 bps above today's 5.86% in-place cap.
- At a 50 bps spread (6.10%) the IRR is 8.70%. The sensitivity tables run ±100 bps.

**4. A 200 bps agency spread over Treasuries.**
- Broker sources give 200-250 bps as typical. August small-loan quotes imply 140-350 bps. Current Fannie quotes for larger, better assets imply about 105-165 bps.
- A sub-$9M loan on a 1958 Class C asset in Florida belongs toward the upper part of the range.
- It sets the Scenario B loan and the plan-2b refinance (both 7.06%) and the plan-3 comparison (7.24%). It does not affect the base case, which refinances with floating debt. Scenario B moves from 3.36% to 3.87% at 150 bps and to 2.95% at 250 bps.

**5. The 10-year fixed loan with Fannie's declining prepayment schedule.**
- It now applies only to the plan-3 comparison row in Scenario A.
- Scenario B used it until this revision: a 10-year loan held five years paid 3% at sale ($240,408). Scenario B now uses a 5-year fixed loan matched to the hold, repaid at maturity with no premium. `bridge.py` row F shows the effect: +90 bp on Scenario B, 2.45% to 3.36%.
- The declining schedule was chosen over yield maintenance. With the note rate about 200 bps above Treasuries, yield maintenance on a loan repaid halfway through its term would cost more than the scheduled premium.
- The Scenario A refinance no longer uses this structure (section 6).

## 8. Results

**Base case: Scenario A, assumed debt, short floating refinance, $13.8M, sale at the end of Year 5.**

| | |
|---|---|
| Total uses | $14,545,290 (price, $207,000 closing, $491,040 renovation, $47,250 assumption fee) |
| Assumed debt / equity | $9,450,000 / $5,095,290 (LP $4,585,761, GP $509,529) |
| Cap rates | Broker 7.0%; Day-0 in-place with reassessed tax 5.86%; Year-1 forward 6.36% |
| Year-1 NOI | $878,230. Expenses are $10,736/unit, 54.3% of EGI. |
| Refinance (Dec 2029) | Year-4 NOI $920,697; value $13,949,955. The loan is sized at 1.25x DSCR on the capped 7.50% rate, giving $8,699,030. It pays 6.73% interest-only. The cap costs $93,950. Against the $9,450,000 payoff, $844,919 of cash is needed. Year-3 operations cover part of it, leaving a $357,752 capital call. Peak equity is $5,453,042. |
| Exit (end of Year 5) | 6.60% cap, $14,542,213 ($149,920/unit). No prepayment premium. Net proceeds $5,552,339. |
| Levered cash flows | −5,095,290 / 451,614 / 328,301 / −357,752 / 302,926 / 5,860,685 |
| **Levered IRR / multiple** | **5.73% / 1.29x**. LP and GP both 5.73%, promote $0. |
| Unlevered IRR / multiple | 5.53% / 1.28x |
| Year-1 cash-on-cash | 8.86% |

**Scenario B, new 5-year agency fixed debt.** The DSCR limit binds, giving an $8,666,106 loan (62.8% LTV) at 7.06%, repaid at maturity when the property sells, with no prepayment premium. Equity is $5,831,934. Levered IRR is 3.36%, the multiple 1.17x, and Year-1 cash-on-cash 2.51%.
- Assuming the 3.0% debt is worth about 237 bps of IRR against new debt.

**Maximum bid price.** Each row is solved on the verified engine. The three Scenario A prices were also built as full workbooks and verified, and each returns its target exactly.

| Target | Scenario A (assumed, base case) | Scenario B (new debt) |
|---|---|---|
| LP IRR 8% | $13,369,967 ($137,835/unit, −3.1%, 6.10% in-place cap) | $12,786,705 ($131,822/unit, −7.3%) |
| Levered IRR 12% | $12,729,444 ($131,231/unit, −7.8%); LP 10.86%, GP 20.54% | $12,123,380 ($124,983/unit, −12.1%) |
| Levered IRR 15% | $12,287,510 ($126,675/unit, −11.0%); LP 12.78%, GP 29.59% | $11,652,085 ($120,125/unit, −15.6%) |

Below about $12.6M, the assumption test (75% of price) forces a paydown at closing: $234,367 at the 15% price. The 8% price is 13.7% above the 2021 sale.

**Sensitivity (Scenario A levered IRR, base-case exit plan).**
- **Exit cap.** At the ask, each 50 bps of exit cap moves IRR by about 3.0 points. The range runs from 11.70% at 5.60% to −0.17% at 7.60%.
- **Rent growth.** Adding or subtracting 0.5% to every year's rent growth moves IRR by about +2.0 or −2.1 points.
- **Price.** Buying 10% below the ask ($12.42M) gives 14.11%.
- **Renovation.** Renovation cost ±20% moves IRR by about ±0.45 points.

## 9. How the model is verified

`verify_model.py` reads only the literal input cells on Assumptions and Unit Mix. It finds each by its label and fails if any of them is a formula. It then rebuilds the model with its own code, which shares nothing with `build_model.py`, and compares its results with the recalculated workbook.

**What it compares.**
- Every Operating Model line for ten years.
- The NOI bridge and cap rates.
- The exit.
- Both debt schedules, including the assumption paydown and all three refinance options.
- Each exit plan's cash flows, IRR, multiple and capital call, and which plan the base case selects.
- Both scenarios' sources and uses, cash flows, IRRs and multiples.
- The waterfall, tier by tier.
- The Summary headline cells.
- All 200 sensitivity cells. Each is recomputed by a full re-run of the engine with the axis inputs changed, not by copying the workbook's per-cell calculation.

**How the waterfall is checked.** The workbook rolls hurdle balances forward year by year. The script instead solves each year in closed form from the future value of the whole investor cash-flow history. It also asserts two things: LP + GP equals available cash each year, and with no promote, LP IRR = GP IRR = deal IRR.

**Current result.** 294 lines, 1,080 figures, all within $1 or 1 bp. The same holds for the variant workbooks at $12.0M (all three waterfall tiers pay out) and at each Scenario A bid price.

**What verification does not prove.** It shows the formulas do what the author intended. It does not validate the assumptions, and the same author wrote both implementations. Two bugs were missed by both until a reviewer or a new test caught them:
- the subordinated GP co-invest (found in review);
- the classic-unit rent track (found while rebuilding the renovation sensitivity table).

## 10. Limitations

- **No T-12 or rent roll.** Rents by unit type, the classic/renovated split, and every expense line are estimates. Water use, meter count, RUBS recovery, trash containers and the utility-payer assumption are the least certain inputs added in this round.
- **Roof and recertification are unknown.** A roof-replacement case is in the model as a toggle (off). The Year-2 recertification cost is a placeholder.
- **Assumed-loan terms are partly undisclosed.** Whether the loans are interest-only, the assumption fee, and the lender's approval test are all judgment. The first mortgage balance differs by $21,934 between the two listings.
- **Rates are held flat.** SOFR (FRED SOFR30DAYAVG), the 5-year (DGS5) and the 10-year Treasury (DGS10) are all FRED observations for 9/28/2026, the latest date all three had published as of 9/30/2026. They are held flat through the December 2029 refinance, with no forward curve.
- **The cap is priced today.** The 2-year cap is priced at today's mid-market for a purchase in 2029, with no bank charges. Doubling its cost lowers the base case to 5.37%.
- **The refinance terms are judgment.** The floating spread is a broker range midpoint for bridge debt. The interest-only period and a prepayment-free sale in loan year 2 are also judgment. A floating loan of about $8.7M would come from a bank or bridge lender, since agency floating programs start at $10M or more.
- **The agency spread is an estimate, not a quote.** Loan fees and third-party reports, including refinance fees, are assumed to be inside the 1.5% closing costs.
- **Scenario B assumes the sale happens at loan maturity.** Its 5-year loan matures at the end of Year 5. A later sale would need an extension or a new loan; an earlier one would pay the 5-4-3-2-1 premium.
- **The exit cap spread is judgment.** No implied cap rate was available for the named comps, and the Class C spread is not sourced.
- **Insurance growth of 7% is likely conservative.** It was left unchanged.
- **The management fee, turnover cost and reserves are at the low end.** Moving them to mid-range would lower returns further (see `STEPS_4-6.md`, Step 6).
- **The waterfall has no fees, no GP catch-up and no clawback.** The hold is fixed at five years.
- **The Summary bid prices are solver output, not live formulas.** Re-run `price_solve.py`, then `build_model.py`, after any input change.

## 11. How to run it

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

## 12. Earlier working reports

These files record how the model got here. The numbers in them are from earlier versions and are superseded by this README.
- `PHASE1_ASSET_AND_ASSUMPTIONS.md`
- `PHASE3_VERIFICATION.md`
- `NOI_BRIDGE_AND_DEBT_SCENARIOS.md`
- `EXIT_CAP_BASE_CASE_AND_BID_PRICE.md`
- `VERIFICATION_STEPS_1-3.md`
- `STEPS_4-6.md`
- `FLAGS_A-D_AND_STEPS_7-9.md`. Its base case (4.19%) was replaced when the 10-year refinance was swapped for the exit-plan comparison in section 6. `bridge.py` shows the step (+154 bp).

Also in the repo:
- `WATERFALL_WALKTHROUGH.md` walks through the LP/GP split with real numbers.
- `INTERVIEW_QA.md` has the questions a reviewer is likely to ask.
- `ONE_PAGE_SUMMARY.md` / `.pdf` is the one-page summary.
