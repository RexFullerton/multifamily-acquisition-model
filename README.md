# Parkview Crossing: 97-Unit Acquisition Model

I built this model to underwrite a real listing from start to finish: take the numbers the broker gives you, rebuild the ones they leave out, and decide what I would actually pay. The property is Parkview Crossing, a 97-unit garden apartment complex at 901-951 NW 8th Ave in Pompano Beach (Broward County), built in 1958-59 and listed at $13.8M. What I learned is that a lot of the broker's 7.0% cap rate goes away the day a buyer closes. Florida reassesses the property tax at the sale price, the listing leaves out real expenses, and the cheap assumable loan has an expiration date that ends up setting the whole business plan.

At the asking price, the deal doesn't work. In my base case I assume the seller's loans, refinance into a short floating-rate loan with a rate cap when the 3.0% loan matures in December 2029, and sell at the end of Year 5. That returns a 5.73% levered IRR and a 1.29x multiple. It never reaches the 8% preferred return, so the GP earns no promote. The most I would pay for the LP to earn 8% is $13,369,967, 3.1% below the ask.

The workbook is live-formula Excel. Blue cells on the Assumptions and Unit Mix tabs are inputs, and every other number is a formula. I didn't want to rely on a spreadsheet I had only checked by eye, so I also wrote a Python script that rebuilds the model from the inputs alone and compares the two. All 1,080 figures it checks tie within $1 or 1 bp.

## The property and the plan

The property is seven two-story concrete-block buildings on 2.39 acres: 19 studios, 51 one-bed/one-bath, 17 two-bed/one-bath and 10 two-bed/two-bath units. The listing's unit breakdown adds up to 98, but the Broward County Property Appraiser (BCPA) records 97 across three folios, so I followed BCPA and dropped one 1BR/1BA.

| Folio | Address | Units |
|---|---|---|
| 4842-35-00-0460 | 951 NW 8 Ave | 20 |
| 4842-35-00-0471 | 901 NW 8 Ave | 18 |
| 4842-35-00-0480 | 930-980 NW 9 Ave | 59 |

The owner of record, Channel Grove LLC, bought all three folios on 12/23/2021 for $11,760,000 ($121,237/unit). The $13.8M ask is 17.3% above that, roughly 3.4% a year. According to the listing, the owner has already renovated about 75% of the units (kitchens, mini-split AC, vinyl windows, lighting) and put over $1M into the buildings: electrical supply lines and panels, fencing and gates, parking, and security.

So this is a light value-add deal, not a repositioning. A buyer would finish a program someone else mostly completed. The returns come from renovating the last 24 classic units at $20,460 each to bring them up to market rent, letting the already-renovated units drift from in-place rent up to market as they turn over, market rent growth (1.0% in Year 1, rising to 3.0% by Year 4), and keeping insurance and property tax under control. I model the renovated units at 65% of the way from in-place to market, and each turnover closes half of the remaining gap.

The listing offers an assumable $5,887,000 first mortgage at 3.0% fixed until December 2029, plus a $3,563,000 supplemental loan at 6.20%. Scenario A, the base case, assumes that debt. Scenario B is the alternative: new 5-year agency fixed debt at closing, matched to a 5-year hold.

I also looked at Florida's Live Local Act (HB 1389, effective July 1, 2026), which exempts qualifying properties from property tax if at least 40% of units are set aside as affordable for 30 years. Parkview Crossing has more than the 71 units required, but I didn't model it. This plan makes its money by moving rents up toward market on the same units the Act would cap below market, so the two strategies work against each other.

## How a 7.0% cap becomes 5.86%

The broker's 7.0% cap rate is calculated on the seller's property tax. After a sale, Florida reassesses non-homestead property to just value on the next January 1. I estimate that just value as 85% of the price, the cost-of-sale allowance under Fla. Stat. 193.011(8). At $13.8M, that gives a reassessed value of $11.73M and Year-1 tax of $236,606, against the seller's current $208,138. BCPA's own 2026 working just value is $11.65M, within 1% of my figure, which gave me some confidence in the method.

Tax isn't the only gap. The listing doesn't show $375 per unit of non-ad valorem charges (mostly the city fire assessment, taken from the actual 2025 tax bills), it doesn't say who pays water, sewer and trash, and it doesn't give a full expense breakdown. Once I put in the buyer's tax, those charges, owner-paid utilities net of what a bill-back (RUBS) program recovers, and my own operating-expense estimates, in-place NOI is $808,528. That's a 5.86% cap on $13.8M. Year-1 NOI is $878,230 (a 6.36% cap), because the first renovations add $42,214 and loss-to-lease burn-off adds $27,488. Neither number gets close to 7%.

I got property tax growth wrong in my first version. Fla. Stat. 193.1555(3) caps increases in the *assessed* value of non-homestead property with 10 or more units at 10% a year, and I grew the tax at 10% every year. That made NOI fall every year of the hold. The cap is a ceiling, not a growth rate. It exists so owners whose market value rose faster than 10% catch up gradually, and after a sale resets assessed value to just value there is nothing to catch up. The model now grows tax at 3.0%, tied by formula to terminal rent growth, and the cap only binds if value grows faster than 10%. (The cap applies to non-school levies only. Amendment 3, a proposed 5% cap on the November 2026 ballot, isn't modeled.) One simplification: strictly, part of Year 1 would still be taxed on the seller's assessment, but I tax the reassessed value from day one. Since BCPA's 2026 working value is already within 1% of mine, the difference is small.

The same reassessment hits the next buyer, so the exit price has to account for it. That's circular, because the buyer's NOI after tax depends on the price you're solving for. I handled it by capitalizing NOI *before* property tax at the exit cap plus the effective tax rate (millage × 85% = 1.71%). Year-6 NOI before tax is $1,209,117, so the exit price is $1,209,117 / (6.60% + 1.71%) = $14,542,213.

## The loan matures in 2029, and that sets the plan

The only reason to take over this debt is the 3.0% first mortgage, and that rate ends in December 2029, the end of Year 3. At that point the whole $9.45M has to be repaid. I compared three responses at the same $13.8M price: sell at maturity, refinance into a loan that can be repaid cheaply at a 2031 sale, or refinance into 10-year fixed debt. For the short refinance I priced two versions, a floating loan with a purchased rate cap and a 5-year agency fixed loan, and the model uses whichever costs less.

| Plan | Levered IRR | Multiple | Capital call | Refi financing cost (% of loan per year) |
|---|---|---|---|---|
| 1. Sell at maturity (3-year hold) | 4.23% | 1.12x | $0 | n/a |
| 2a. Short refi: floating + cap (base case) | 5.73% | 1.29x | $357,752 | 7.27% |
| 2b. Short refi: 5-year fixed | 4.58% | 1.22x | $0 | 8.98% |
| 3. 10-year fixed refi (comparison) | 4.19% | 1.20x | $38,965 | 9.65% |

Selling at maturity avoids refinancing risk, but it pays acquisition and sale costs over three years and sells before the renovations and burn-off show up in two full years of NOI. Refinancing is better, but only into debt you can get out of cheaply in 2031. The fixed loans lose because they'd be repaid in their second year: the 5-year loan pays a 4% prepayment premium and the 10-year pays 5%, which is where most of their cost comes from.

The floating loan is SOFR plus 300 bps (6.73%), interest-only, open at sale, with a 2-year cap at a 4.50% SOFR strike. Over its two years it costs $1,264,964 ($1,171,015 of interest plus the $93,950 cap), or 7.27% of the $8,699,030 loan per year. The 5-year fixed alternative costs $1,631,632 ($1,276,106 of interest plus a $355,526 premium) on a $9,085,154 loan, or 8.98% a year. Even with SOFR at the strike for both years (7.50% all-in), the floating plan still returns 5.26%, above both alternatives. It has two costs. Because a loan sized on the capped rate is smaller, investors have to put in $357,752 in Year 3. And it depends on a floating loan being available in 2029. Agency floating programs start at $10M (Freddie Mac) or $25M (Fannie Mae SARM), so a loan this size would come from a bank or bridge lender.

## Results

Base case: Scenario A, assumed debt, short floating refinance, $13.8M, sale at the end of Year 5.

| | |
|---|---|
| Total uses | $14,545,290 (price, $207,000 closing, $491,040 renovation, $47,250 assumption fee) |
| Assumed debt / equity | $9,450,000 / $5,095,290 (LP $4,585,761, GP $509,529) |
| Cap rates | Broker 7.0%; Day-0 in-place with reassessed tax 5.86%; Year-1 forward 6.36% |
| Year-1 NOI | $878,230. Expenses are $10,736/unit, 54.3% of EGI. |
| Refinance (Dec 2029) | Year-4 NOI $920,697; value $13,949,955. The $8,699,030 loan is sized at 1.25x DSCR on the capped 7.50% rate. Against the $9,450,000 payoff and the $93,950 cap, $844,919 of cash is needed. Year-3 operations cover part of it, leaving a $357,752 capital call. Peak equity is $5,453,042. |
| Exit (end of Year 5) | 6.60% cap, $14,542,213 ($149,920/unit). No prepayment premium. Net proceeds $5,552,339. |
| Levered cash flows | −5,095,290 / 451,614 / 328,301 / −357,752 / 302,926 / 5,860,685 |
| Levered IRR / multiple | 5.73% / 1.29x. LP and GP both 5.73%, promote $0. |
| Unlevered IRR / multiple | 5.53% / 1.28x |
| Year-1 cash-on-cash | 8.86% |

Scenario B, with new 5-year agency fixed debt, does worse. The DSCR test binds at an $8,666,106 loan (62.8% LTV) at 7.06%, repaid at maturity when the property sells. Equity is $5,831,934, and the deal returns 3.36% with a 1.17x multiple and 2.51% Year-1 cash-on-cash. So taking over the 3.0% debt is worth about 237 bps of IRR, but only for three years, which is why the exit plan matters so much.

Here is what I would pay for each target return. I solved each price on the verified engine, and for the three Scenario A prices I also built full workbooks and confirmed each returns its target exactly.

| Target | Scenario A (assumed debt, base case) | Scenario B (new debt) |
|---|---|---|
| LP IRR 8% | $13,369,967 ($137,835/unit, −3.1%, 6.10% in-place cap) | $12,786,705 ($131,822/unit, −7.3%) |
| Levered IRR 12% | $12,729,444 ($131,231/unit, −7.8%); LP 10.86%, GP 20.54% | $12,123,380 ($124,983/unit, −12.1%) |
| Levered IRR 15% | $12,287,510 ($126,675/unit, −11.0%); LP 12.78%, GP 29.59% | $11,652,085 ($120,125/unit, −15.6%) |

Below about $12.6M, the lender's assumption test (75% of price) forces a paydown at closing, $234,367 at the 15% price. My 8% price is 13.7% above the 2021 sale, which seems to me a fair credit for the seller's renovations.

The exit cap moves the answer more than anything else. At the ask, each 50 bps changes the IRR by about 3.0 points, from 11.70% at a 5.60% exit cap down to −0.17% at 7.60%. Adding or subtracting 0.5% to every year's rent growth moves it about +2.0 or −2.1 points. Buying 10% below the ask ($12.42M) gives 14.11%, and renovation cost ±20% moves it only about ±0.45 points. `WATERFALL_WALKTHROUGH.md` walks through the LP/GP split with real numbers.

## Assumptions and sources

"JUDGMENT" means I couldn't find a source and the number is my estimate. Those are the first things to test in diligence.

| Assumption | Value | Source |
|---|---|---|
| Price | $13,800,000 ($142,268/unit) | [LoopNet listing](https://www.loopnet.com/Listing/901-951-NW-8th-Ave-Pompano-Beach-FL/41107583/) |
| Units | 97 | BCPA parcel records (3 folios) |
| Seller's 2025 taxable value | $10,318,700 | BCPA, sum of three folios; matches the listing |
| Millage | 20.1710 mills | BCPA 2026 proposed millage, code 1512. 2025 final was 20.2573. |
| Reassessed value | Price × 85% | Fla. Stat. 193.011(8). BCPA's 2026 working just value, $11.65M, is within 1% of $11.73M. |
| Property tax growth | 3.0%/yr | Tied to terminal market rent growth |
| Non-ad valorem charges | $375/unit | BCPA 2025 bills: total $245,413, minus $209,026 ad valorem, divided by 97 units. Mainly the city fire assessment. |
| Market and in-place rents | By unit type | Broker's disclosed 20.76% blended upside plus apartments.com Pompano 33060 averages. JUDGMENT on the split by unit type. Weakest-sourced input. |
| Rent growth | 1.0%, 1.75%, 2.5%, then 3.0% | Year 1: Yardi Matrix Broward Class C/C+ asking rents +0.2% YoY (via MIAMI REALTORS, May 2026). Later years: JUDGMENT, capped at 3.0%. |
| Vacancy / credit loss / concessions | 6.5% / 1.0% / 0.5% | JUDGMENT. The listing reports 92% occupancy. |
| Other income, excluding utility recovery | $15/unit/month | JUDGMENT (laundry, fees, pet) |
| Water and sewer | $630/unit/yr, growing 6%/yr | [Pompano Beach Code 50.03](https://codelibrary.amlegal.com/codes/pompanobeach/latest/pompanobeach_fl/0-0-0-93003) and [51.05](https://codelibrary.amlegal.com/codes/pompanobeach/latest/pompanobeach_fl/0-0-0-80354), FY2027 multifamily rates. Usage of 3,000 gal/unit/month and 7 meters are JUDGMENT. |
| Trash | $170/unit/yr | [Pompano Beach 2025-26 solid waste rates](https://cdn.pompanobeachfl.gov/city/pages/solid_waste/2025-2026-DISPOSAL-RATES-New.pdf): 6-yd container, 2x/week, $457.63/month. Container count (3) is JUDGMENT. |
| Who pays water, sewer, trash | Owner, with 60% RUBS recovery | Listing is silent (the OM is gated). JUDGMENT. Diligence item. |
| Insurance | $2,400/unit, growing 7%/yr | JUDGMENT. Marked up from about $2,000/unit for an undisclosed roof. The growth rate is conservative: [Insurance Journal](https://www.insurancejournal.com/news/southeast/2026/06/30/875651.htm) reports Florida property-cat reinsurance down 15-20% at June 2026 renewals. |
| Payroll / R&M / turnover / contract / common utilities / G&A / marketing | $1,400 / $1,100 / $350 / $280 / $500 / $250 / $150 per unit | JUDGMENT. Turnover is at the low end. |
| Management fee | 3.5% of EGI | JUDGMENT; low end for 97 units |
| Replacement reserves | $300/unit | JUDGMENT; low end for this vintage |
| Renovation scope | $20,460/unit × 24 classic units | Bottom-up, eight line items + 10% contingency |
| Recertification | $160,000 in Year 2 | Broward 40/50-year program; cost is a placeholder |
| Assumed first mortgage | $5,887,000 at 3.0%, matures Dec 2029 (Year 3) | Crexi / LoopNet |
| Supplemental loan | $3,563,000 at 6.20% | Crexi / LoopNet |
| Interest-only status of assumed loans | Interest-only | JUDGMENT, not disclosed |
| Assumption fee / paydown test | 0.5% / 75% max LTV on price | JUDGMENT |
| 10-year Treasury | 5.24% | [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), 9/28/2026 (latest print as of 9/30/2026) |
| 5-year Treasury | 5.06% | [FRED DGS5](https://fred.stlouisfed.org/series/DGS5), 9/28/2026 |
| Agency spread | 200 bps (5-yr fixed 7.06%; 10-yr fixed 7.24%) | JUDGMENT within broker ranges. [multifamily.loans](https://www.multifamily.loans/multifamily-mortgage-rates/) cites 200-250 bps typical. [apartmentloanstore](https://apartmentloanstore.com/loan-product/apartment-multifamily-loan-interest-rates) Fannie quotes on 9/29/2026 imply about 105-165 bps for larger, better assets. |
| Agency terms | 75% max LTV, 1.25x DSCR, 30-yr amortization, no IO | [Fannie Mae Small Loan term sheet](https://multifamily.fanniemae.com/financing-options/small-loans/small-mortgage-loan-program-term-sheet): up to $9M, 80% LTV, 1.25x. 75% and no IO are JUDGMENT. |
| Prepayment premium | 10-yr: 5-5-4-4-3-3-2-2-1-1; 5-yr: 5-4-3-2-1 | [Fannie Mae declining prepayment premium](https://multifamily.fanniemae.com/financing-options/rate-lock-and-prepay-options/declining-prepayment-premium-term-sheet) |
| Base-case refinance (Dec 2029) | 30-day avg SOFR 3.7307% + 300 bps = 6.73%, interest-only, open at sale | [FRED SOFR30DAYAVG](https://fred.stlouisfed.org/series/SOFR30DAYAVG), 9/28/2026. Spread: midpoint of "SOFR + ~275-325 bps before cap" from [multifamily-usa.com](https://multifamily-usa.com/rates/) (Sept 2026). IO and no premium after month 12 are JUDGMENT. |
| Rate cap | 2 years, 4.50% SOFR strike, 1.08% of the loan | [BlueGamma cap calculator](https://www.bluegamma.io/calculators/interest-rate-cap-calculator), 9/29/2026: $108,000 on $10M, indicative mid-market. The strike is JUDGMENT. |
| Scenario B loan term | 5 years, repaid at maturity | Fannie Small Loan terms allow 5-30 years |
| Exit cap | 6.60% = 5.60% market + 100 bps | See below |
| Cost of sale at exit | 2.0% | JUDGMENT |
| Waterfall | 8% pref; 70/30 to a 12% IRR; 50/50 above | Standard structure. GP co-invests 10% pari passu. No fees. |

For the exit cap, I anchored on the market level and added a spread for age and class. [Matthews](https://www.matthews.com/insights/fort-lauderdale) puts the Fort Lauderdale multifamily average at 5.6% (Q3 2025), and [Colliers](https://www.colliers.com/en/research/miami/sfl-multifamily-report-26q1) says South Florida cap rates are holding "near 5.0%" (Q1 2026). Those averages are dominated by newer buildings, and this one will be about 73 years old at sale, so I added 100 bps. That spread is my judgment. [CBRE's H1 2026 survey](https://www.cbre.com/insights/reports/us-cap-rate-survey-h1-2026) says expectations of rising cap rates are strongest for Class C, but its market tables are gated. I checked two named comps: [Cascades at the Hammocks](https://crenews.com/2026/05/06/bowery-properties-buys-264-unit-apartment-complex-in-miami-for-65-5mln/) sold for $65.5M ($248,106/unit, 264 units, built 1988) in May 2026, and [Savona Grand](https://hoodline.com/2026/07/tampa-landlord-nabs-savona-grand-between-boynton-and-lake-worth-6942770/) sold in July 2026 at an undisclosed price. Neither has a public NOI, so neither gives an implied cap rate. I deliberately didn't tie the exit cap to this deal's own entry cap. An earlier version did, and it quietly offset expense mistakes: raise an expense and the entry cap falls, and the exit cap falls with it.

## Judgment calls I'd test first

These five inputs aren't sourced, and each one moves the answer.

RUBS recovery is set at 60% of the owner's water, sewer and trash cost. The listing doesn't say who pays utilities or whether leases have a bill-back clause. A fully implemented program recovers more, but recovery here depends on the lease form, 6.5% vacancy, any caps, and phasing in as leases turn over (55% a year). Each 10 points of recovery is worth about $7,800 a year of NOI on a Year-1 cost of $77,553. At 50% the IRR is 5.19%; at 70% it's 6.28%.

Water use is 3,000 gallons per unit per month, roughly 1.5 occupants at about 65 gallons per person per day, with 72% of units being studios or one-bedrooms. At 2,000 gallons the IRR is 6.05%; at 4,000 it's 5.41%. The owner's actual water bills would settle it.

The 100 bps Class C spread puts the exit cap at 6.60%, 74 bps above today's 5.86% in-place cap. At a 50 bps spread (6.10%), the IRR is 8.70%, which shows how much of the conclusion rides on this one number.

The 200 bps agency spread sits toward the upper part of what I found: broker sources say 200-250 bps is typical, August small-loan quotes imply 140-350 bps, and current Fannie quotes for larger, better assets imply 105-165 bps. A sub-$9M loan on a 1958 Class C building in Florida belongs toward the top. It doesn't touch the base case, which refinances with floating debt. Scenario B moves from 3.36% to 3.87% at 150 bps and to 2.95% at 250 bps.

For the fixed loans I used Fannie's declining prepayment schedule rather than yield maintenance. With the note rate about 200 bps above Treasuries, yield maintenance on a loan repaid halfway through its term would cost more than the scheduled premium.

## Mistakes I made along the way

Besides the 10% tax growth, four errors changed the answer. The first version grew the classic units' half-captured Year-1 rent forward, so the 24 units I renovated never reached market rent. Fixing that was worth 267 bps. I had also added a $175/month renovation premium on top of market rent, which counted the same upgrade twice, since market rent already is what renovated units command. The premium is now $0, and Sensitivity Table 3 shows each $50/month would add about 73 bps.

The waterfall first put the GP's 10% co-invest behind the LP in Tier 1. At a 7.89% deal IRR, that gave the LP 9.82% and the GP −15.88%, which isn't a real structure. Pari passu, both now earn the deal IRR when no promote is paid, and the verification script checks that.

Finally, I first priced the 2029 refinance as a 10-year fixed loan. It would have been repaid in its second year with a 5% premium. No sponsor planning a 2031 sale would take that debt. Switching to the exit-plan comparison moved the base case from 4.19% to 5.73% (+154 bp, shown step by step in `bridge.py`). Scenario B had the same problem, a 10-year loan paying 3% ($240,408) at the Year-5 sale. It now uses a 5-year loan matched to the hold, which moved it from 2.45% to 3.36% (+90 bp).

## How I checked it

`verify_model.py` reads only the literal input cells on Assumptions and Unit Mix, finds each by its label, and fails if any of them is a formula. It rebuilds the model with its own code, which shares nothing with `build_model.py`, then compares its results with the recalculated workbook. That covers every operating line for ten years, the NOI bridge, the exit, both debt schedules and all three refinance options, every exit plan, both scenarios' sources and uses and returns, the waterfall tier by tier, the Summary headline cells, and all 200 sensitivity cells, each re-run through the full engine. It checks the waterfall differently from the workbook (closed-form future values instead of rolling balances) and asserts that LP + GP equals available cash every year. The current result is 294 lines and 1,080 figures, all within $1 or 1 bp. The same holds for the $12.0M variant, where all three waterfall tiers pay, and at each Scenario A bid price.

This proves the formulas do what I meant them to do. It doesn't prove the assumptions are right, and I wrote both sides. Both missed the GP co-invest bug (a reviewer caught it) and the classic-unit rent bug (I found it while rebuilding the renovation sensitivity table).

## Limitations

- There's no T-12 or rent roll. Rents by unit type, the classic/renovated split and every expense line are estimates, and the utility inputs (water use, meters, RUBS recovery, trash containers, who pays) are the least certain.
- The roof and the 40/50-year recertification are unknown. A roof-replacement case is in the model as a toggle (off), and the $160,000 recertification cost is a placeholder.
- The assumed loans' terms are partly undisclosed: interest-only status, the assumption fee and the lender's approval test are judgment. The first mortgage balance differs by $21,934 between the two listings.
- Rates are held flat. SOFR and the 5- and 10-year Treasuries are FRED observations for 9/28/2026, held through the December 2029 refinance with no forward curve.
- The rate cap is priced at today's mid-market for a 2029 purchase, with no bank charges. Doubling its cost lowers the base case to 5.37%.
- The floating spread is a broker-range midpoint for bridge debt, and the interest-only period and prepayment-free sale in loan year 2 are judgment.
- Loan fees and third-party reports, including on the refinance, are assumed to fit inside the 1.5% closing costs.
- Scenario B assumes the sale happens exactly at loan maturity.
- Insurance growth of 7% is probably conservative. The management fee, turnover cost and reserves are at the low end, and moving them to mid-range would lower returns further (see `STEPS_4-6.md`, Step 6).
- The waterfall has no fees, GP catch-up or clawback, and the hold is fixed at five years.
- The Summary bid prices are solver output, not live formulas. After any input change, re-run `price_solve.py` and then `build_model.py`.

## Files and how to run it

`Parkview_Crossing_Acquisition_Model.xlsx` has twelve tabs, and each tab title says which debt scenario it shows.

| Tab | What it holds |
|---|---|
| Assumptions | Every input (blue) with its source or JUDGMENT, plus derived values (reassessed tax, utility cost per unit, agency rate, exit cap) |
| Unit Mix | Unit counts, in-place and market rent, and renovation capex by unit type |
| Operating Model | Ten years of rent, income, every expense line, NOI, reserves, capex and unlevered cash flow. Debt-agnostic. |
| Debt / Capital | Scenario B loan sizing, amortization, sources and uses, and the LP/GP equity split |
| Returns | NOI bridge from the broker's cap rate to Day-0, cap rates three ways, the tax-adjusted exit, unlevered and Scenario B returns |
| Debt (Assumed) | Scenario A: the assumption paydown test, both assumed loans, and the three refinance options |
| Returns (Assumed) | Scenario A sources and uses, each exit plan's returns, and the selected base case |
| Waterfall | LP/GP distributions tier by tier and year by year |
| Sensitivity | Exit cap × price, exit cap × rent growth and renovation premium × cost on Scenario A; exit cap × price on Scenario B |
| Checks | 30 internal checks (sources = uses, cash flows rebuild, schedules roll forward, waterfall ties, and so on) |
| Summary | Headline figures, the exit-plan and debt-scenario comparisons, and bid prices |

`build_model.py` writes the workbook, `verify_model.py` does the independent check, `price_solve.py` solves the bid prices (into `bid_prices.json`, which the builder reads), and `bridge.py` walks the earlier 5.20% base case to the current one, one change at a time. It needs Python 3 with `openpyxl`, `numpy_financial` and `scipy`, plus LibreOffice to recalculate (Excel recalculates on open).

```bash
python3 build_model.py
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --norestore --convert-to xlsx --outdir _recalc model_wip.xlsx
cp _recalc/model_wip.xlsx Parkview_Crossing_Acquisition_Model.xlsx
python3 verify_model.py
python3 price_solve.py
python3 bridge.py
```

`ONE_PAGE_SUMMARY.md` and `.pdf` are the one-page version. The other markdown files (`PHASE1_ASSET_AND_ASSUMPTIONS.md`, `PHASE3_VERIFICATION.md`, `NOI_BRIDGE_AND_DEBT_SCENARIOS.md`, `EXIT_CAP_BASE_CASE_AND_BID_PRICE.md`, `VERIFICATION_STEPS_1-3.md`, `STEPS_4-6.md`, `FLAGS_A-D_AND_STEPS_7-9.md`) are my working notes from earlier versions. Their numbers are superseded by this README.
