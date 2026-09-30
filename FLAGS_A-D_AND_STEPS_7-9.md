# Flags A–D Applied; Steps 7–9

Prepared 2026-09-29. `verify_model.py` reproduces every figure here: 219 lines and 945 figures tie within $1 or 1 bp, including all 200 sensitivity cells. All 27 CHECKS pass, and the workbook has no formula errors.

## Headline

The new base case (Scenario A, assumed debt, $13.8M) has a levered IRR of **4.19%** and a multiple of **1.20x**, down from 5.20%. Other results:
- Unlevered IRR: 5.53%.
- Scenario B (new debt): 2.45%.
- LP and GP both earn 4.19%. No promote is paid.

The deal still does not reach the 8% pref at the ask. The maximum price for an 8% LP return is **$13,105,989**, 5.0% below the ask.

## Bridge: 5.20% to 4.19%

Changes are applied cumulatively, top to bottom. Row 0 turns every change off and reproduces the prior 5.20%. The last row equals the workbook. Reproduce with `python3 bridge.py`.

| Change | A levered IRR | Change | A multiple | B levered IRR | Unlevered IRR | Year-1 NOI | Exit cap | Year-3 call |
|---|---|---|---|---|---|---|---|---|
| Prior base case (commit efb3da1) | 5.20% | | 1.27x | 2.31% | 5.28% | 916,855 | 6.64% | 540,895 |
| A. Tax grows with just value (3.0%), not 10% | 5.83% | +63 bp | 1.29x | 2.97% | 5.52% | 916,855 | 6.64% | 0 |
| B. Owner-paid water/sewer/trash at city rates, 60% RUBS, other income re-split | 4.59% | −124 bp | 1.23x | 1.81% | 5.09% | 878,230 | 6.36% | 59,131 |
| C. Exit cap = direct market input 6.60% | 3.15% | −144 bp | 1.15x | 0.32% | 4.57% | 878,230 | 6.60% | 385,995 |
| D1. Agency fixed 7.24%, 75% LTV, 1.25x DSCR on amortizing payment, no IO | 3.12% | −4 bp | 1.15x | 0.80% | 4.57% | 878,230 | 6.60% | 522,525 |
| D2. Prepayment premium at sale (Fannie declining schedule) | 1.52% | −160 bp | 1.07x | −0.02% | 4.57% | 878,230 | 6.60% | 522,525 |
| D3. Assumption paydown test (75% max LTV on price) | 1.52% | 0 bp | 1.07x | −0.02% | 4.57% | 878,230 | 6.60% | 522,525 |
| **Bug fix:** renovated classic units reach market from Year 2 | **4.19%** | +267 bp | 1.20x | 2.45% | 5.53% | 878,230 | 6.60% | 38,965 |

How to read it:
- **C in isolation.** Under the old rule, the exit cap had fallen to 6.36% once B lowered the in-place cap. Row C moves it to the 6.60% market input. That is the "exit rule absorbs expense errors" effect from Step 6, now removed.
- **D3.** The paydown test does nothing at the ask. It only binds below about $12.6M.
- **The bug fix.** It is not one of A–D; see below. It is shown separately so its effect is visible.

## A. Property tax

**What changed.** Tax is still reassessed at purchase (price × 85% × millage). It now grows at the model's terminal market rent growth (3.0%), linked by formula, instead of the 10% cap.

**Citation.** Fla. Stat. 193.1555(3) limits annual increases in assessed value to 10% for non-school levies (193.1555(2)). Assessed value resets to just value after a change of ownership (193.1555(5)). The property is covered by 193.1555 rather than 193.1554 because 193.1554(1) is limited to residential property of nine or fewer units.

**Assumptions tab.** The cap input is kept, labeled "reference only, not used in formulas."

**README.** Section 4 explains the difference between the cap and the growth rate, and the timing simplification: reassessment actually takes effect the January 1 after closing.

## B. Utilities and other income

**The listing is silent.** Neither LoopNet nor Crexi says who pays water, sewer or trash. The LoopNet flyer could not be downloaded, and the OM is gated. As instructed, the model assumes **owner-paid with RUBS recovery**, flagged as a diligence item.

**Water and sewer: $630/unit/yr (sourced tariff, judgment on usage).**
- Rates: Pompano Beach Code 50.03 and 51.05, multifamily classification, effective 10/1/2026:
  - water $7.10/unit/month + $3.90/1,000 gal;
  - sewer $16.10/unit/month + $4.88/1,000 gal;
  - $40.64/month per 2-inch meter.
- Judgment: 3,000 gal/unit/month and 7 meters.
- Growth: 6%/yr, from the adopted schedule through FY2029.

**Trash: $170/unit/yr (sourced rate, judgment on container count).**
- Rate: the city's 2025-26 schedule for a 6-yd container picked up twice a week (the city's multifamily minimum) is $457.63/month.
- Judgment: 3 containers.
- Contract services drop from $450 to $280 because trash was previously inside that line. The total is unchanged.

**RUBS recovery: 60% of water, sewer and trash (judgment).** That is $46,532 in Year 1.

**Other income excluding utilities: $15/unit/month (judgment).** It was $35 including RUBS.

**Net effect.** Year-1 NOI falls $38,625, to $878,230.

## C. Exit cap

The exit cap is now **6.60% = 5.60% market anchor + 100 bps Class C / vintage spread**. It is a direct input, not tied to the deal.

**Market anchor.** Matthews, Fort Lauderdale Multifamily Q3 2025: average 5.6%, $283K/unit. Cross-check: Colliers, South Florida Multifamily Q1 2026 (4/24/2026), cap rates "near 5.0%" across all classes.

**Class C / vintage spread (judgment).** The CBRE H1 2026 Cap Rate Survey (8/12/2026) says expectations of rising cap rates are strongest for Class C. Its market-level tables are behind a registration form, which I did not fill in.

**Named comps: no implied cap rate available.**
- Cascades at the Hammocks: Miami-Dade, 264 units, built 1988. Bought by Bowery in May 2026 for $65.5M ($248,106/unit), assuming about $58M of Freddie Mac loans. No NOI published.
- Savona Grand: Palm Beach County, 214 units. Bought by American Landmark in July 2026 at an undisclosed price; the prior sale was $47.8M in 2019.

**Sensitivity.** All tables run the exit cap ±100 bps (5.60%–7.60%). The −100 bps row is the building trading at the Fort Lauderdale average.

**Refinance.** The Year-4 refinance appraisal uses the same exit cap.

## D. Debt

**Rate.** 10-year Treasury **5.24%** (FRED DGS10, 9/28/2026) + **200 bps** agency spread = **7.24% fixed**. The floating 7.10% is removed.
- The spread is judgment within the sourced ranges.
- multifamily.loans says spreads are "generally 200-250 bps." Its August small-loan quotes imply 140-350 bps.
- apartmentloanstore's Fannie quotes on 9/29/2026 (6.28-6.87%) imply about 105-165 bps for larger, better assets.

**Terms.** Fannie Mae Small Mortgage Loan program: up to $9M, 80% max LTV, 1.25x minimum DSCR.
- The model uses 75% LTV (judgment for a 1958 Class C asset).
- DSCR is sized on the **amortizing** payment, 30-year amortization, no interest-only period (judgment).
- The debt-yield test is removed; agencies don't size on it.
- DSCR binds in both places: the Scenario B loan is $8,512,260 (61.7% LTV) and the refinance loan is $8,923,868.

**Prepayment.** The Fannie 10-year declining premium is 5-5-4-4-3-3-2-2-1-1.
- Scenario B sells in loan year 5: 3%, or $240,408.
- The Scenario A refinance sells in loan year 2: 5%, or $436,819.
- This is the D2 row, −160 bp. I would not choose this structure in practice. A 5-year fixed loan, a floating-rate agency loan, or a sale with loan assumption would avoid most of it. I kept it because the instruction specifies 10-year Treasury pricing. See INTERVIEW_QA Q14.

**Assumption paydown risk: modeled, not excluded.**
- If the assumed balances exceed 75% of the purchase price, the buyer pays the difference down at closing, supplemental first. The 75% is judgment; the lender's actual test is not disclosed.
- Zero at $13.8M. It binds below $12.6M: $67,189 at the 12% bid price and $388,793 at the 15% bid price.

## Bug found and fixed

The Operating Model's classic-unit rent track had a bug in how renovated units reached market rent:
- **Year 1 was right.** Rent was blended 50% in-place and 50% renovated while renovations were underway.
- **Year 2 on was wrong.** The model compounded that blend forward with market growth, so the 24 renovated units stayed about $150/month below market for the whole hold.
- **Why it wasn't caught.** `verify_model.py` had the same logic, so it passed.
- **How it surfaced.** I found it while writing the renovation-premium sensitivity.
- **The fix.** Units are at market (+ premium, $0) from Year 2.

It is worth +267 bp. It is shown as its own bridge row so you can see it separately from A–D.

## Step 4 (re-run): bid prices

The exit cap is now a market input, so it no longer moves with price. The frozen-versus-floating distinction from last round is gone.

**Scenario A (base case).** Each of the three prices was also built as a full workbook and verified; each returns its target exactly.

| Target | Max price | $/unit | vs. ask | In-place cap | Deal IRR | LP IRR | GP IRR | Assumption paydown |
|---|---|---|---|---|---|---|---|---|
| LP IRR 8% | $13,105,989 | $135,113 | −5.0% | 6.26% | 8.00% | 8.00% | 8.00% | $0 |
| Levered IRR 12% | $12,510,415 | $128,973 | −9.3% | 6.64% | 12.00% | 10.86% | 20.50% | $67,189 |
| Levered IRR 15% | $12,081,610 | $124,553 | −12.5% | 6.94% | 15.00% | 12.79% | 29.46% | $388,793 |

**Scenario B (new agency debt).**

| Target | Max price | $/unit | vs. ask | In-place cap | Loan (binding) |
|---|---|---|---|---|---|
| LP IRR 8% | $12,572,261 | $129,611 | −8.9% | 6.60% | $8,716,288 (DSCR) |
| Levered IRR 12% | $11,921,109 | $122,898 | −13.6% | 7.05% | $8,824,497 (DSCR) |
| Levered IRR 15% | $11,458,598 | $118,130 | −17.0% | 7.41% | $8,593,948 (LTV) |

## Step 7: sensitivities

Tables 1–3 are on Scenario A. Table 4 is secondary, on Scenario B. The exit cap runs ±100 bps in each table.

**How each cell is computed.** Every cell has its own calculation block on the tab: NOI by year, the assumed loans after any paydown, the refinance sized on that cell's NOI and exit cap, the capital call, the prepayment premium, and the exit.
- Table 2 rebuilds the rent engine unit by unit at each growth path.
- My first version of Table 2 used a shortcut (scaling rent by the growth change). A full re-run showed it was off by 90–210 bp per cell, so I replaced it.
- CHECKS confirms each grid's base cell equals the model IRR.

**Table 1: Scenario A levered IRR, exit cap × price.**

| Exit cap | $12.42M | $13.11M | $13.80M | $14.49M | $15.18M |
|---|---|---|---|---|---|
| 5.60% | 19.30% | 14.57% | 10.58% | 7.29% | 4.52% |
| 6.10% | 15.95% | 11.27% | 7.37% | 4.18% | 1.49% |
| **6.60%** | 12.62% | 7.98% | **4.19%** | 1.09% | −1.51% |
| 7.10% | 9.26% | 4.65% | 0.97% | −2.03% | −4.53% |
| 7.60% | 5.82% | 1.26% | −2.31% | −5.20% | −7.60% |

**Table 2: Scenario A levered IRR, exit cap × rent growth change (added to every year).**

| Exit cap | −1.0% | −0.5% | 0 | +0.5% | +1.0% |
|---|---|---|---|---|---|
| 5.60% | 6.45% | 8.54% | 10.58% | 12.57% | 14.51% |
| 6.10% | 3.07% | 5.25% | 7.37% | 9.44% | 11.46% |
| **6.60%** | −0.32% | 1.97% | **4.19%** | 6.34% | 8.44% |
| 7.10% | −3.77% | −1.36% | 0.97% | 3.23% | 5.42% |
| 7.60% | −7.35% | −4.78% | −2.31% | 0.07% | 2.38% |

**Table 3: Scenario A levered IRR, renovation premium × renovation cost per unit.**

| Premium | $16,368 | $18,414 | $20,460 | $22,506 | $24,552 |
|---|---|---|---|---|---|
| **$0** | 4.64% | 4.41% | **4.19%** | 3.96% | 3.74% |
| $50 | 5.39% | 5.16% | 4.93% | 4.70% | 4.47% |
| $100 | 6.14% | 5.90% | 5.66% | 5.43% | 5.20% |
| $150 | 6.88% | 6.64% | 6.40% | 6.16% | 5.93% |
| $200 | 7.62% | 7.38% | 7.13% | 6.89% | 6.65% |

**Table 4 (secondary): Scenario B levered IRR, exit cap × price.**

| Exit cap | $12.42M | $13.11M | $13.80M | $14.49M | $15.18M |
|---|---|---|---|---|---|
| 5.60% | 14.84% | 11.04% | 7.96% | 5.38% | 3.17% |
| 6.10% | 11.82% | 8.15% | 5.18% | 2.69% | 0.57% |
| **6.60%** | 8.85% | 5.32% | **2.45%** | 0.06% | −1.97% |
| 7.10% | 5.91% | 2.51% | −0.24% | −2.52% | −4.47% |
| 7.60% | 2.98% | −0.29% | −2.92% | −5.10% | −6.95% |

The equity-multiple grids are in the workbook.

## Steps 8–9: deliverables

**Step 8 (documents):**
- `README.md`: thesis, structure, sourced assumptions, results and limitations. It covers the $0 premium reasoning, the 193.1555 cap vs. growth explanation, and the 2021 sale at $11.76M with the 17.3% markup.
- `WATERFALL_WALKTHROUGH.md`: the base case and a $12.0M case where all three tiers pay. That variant workbook was verified: 945 figures tie.
- `INTERVIEW_QA.md`: fifteen questions, including the 2021 sale.

**Step 9:** `ONE_PAGE_SUMMARY.md` and `.pdf` (one page), and `RESUME_BULLETS.md` (two bullets, 18 and 20 words, verified numbers only).

## Judgment calls made this round

These are the calls to review first:
- **Water and sewer.** 3,000 gal/unit/month usage and 7 meters.
- **Trash.** 3 containers.
- **RUBS recovery.** 60%.
- **Other income.** $15/unit/month excluding utilities.
- **Exit cap.** The 5.60% anchor (not Colliers' 5.0%) and the +100 bps vintage spread.
- **Agency terms.** 200 bps spread, 75% LTV, no interest-only period.
- **Prepayment.** The 10-year prepayment structure on the refinance.
- **Assumption test.** 75% max LTV.
- **Tax growth.** Tied to *terminal* rent growth (3.0%) rather than each year's growth.
