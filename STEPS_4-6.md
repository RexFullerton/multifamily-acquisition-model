# Steps 4–6: Decisions Applied, Bid Price, BCPA Record, Assumption Review

Prepared 2026-09-29. Stops after Step 6, as instructed. Steps 7–9 have not been started.

Every figure below comes from `verify_model.py`. That engine ties to the recalculated workbook on 163 lines and 702 individual figures, within $1 or 1 bp. Figures for scenarios that are not in the workbook, such as bid prices and assumption tests, come from the same engine run with one input changed.

## Current base case

These figures use 97 units, Scenario A (assumed loan), and an asking price of $13.8M.

| Metric | Value |
|---|---|
| Year-1 NOI (reassessed tax) | $916,855 |
| In-place cap (Day-0) / Year-1 forward cap / broker-stated cap | 6.14% / 6.64% / 7.0% |
| Exit cap (in-place + 50 bps) | 6.64% |
| Unlevered IRR / EM | 5.28% / 1.26x |
| **Scenario A levered IRR / EM** | **5.20% / 1.27x** |
| LP IRR / GP IRR / GP promote | 5.20% / 5.20% / $0 |
| Scenario B (new debt) levered IRR / EM | 2.31% / 1.11x |
| Scenario A Year-1 cash-on-cash | 9.62% |
| Scenario A equity at close / Year-3 capital call / peak equity | $5,095,290 / $540,895 / $5,636,185 |

**Finding: at $13.8M the deal does not clear the 8% preferred return under either debt structure, so no promote is earned.** The broker's roughly 10% Day-1 cash-on-cash is real under the assumed loan (9.62% here). It comes from the 3.0% first mortgage, and it ends at the Year-3 maturity.

---

## Decisions applied before Step 4

### 1. Renovation premium set to $0

Renovated units now reach market rent and nothing above it. The value of the renovation is closing the gap between in-place and market rent, which is 24 classic units at about $300/month each. The 73 units the prior owner already renovated were only ever trended *to* market. Charging a $175 premium on our units on top of that would have double-counted. The input is now labeled "Renovated-Unit Rent Premium over Market ($/month)" and set to 0. The reasoning is in the cell note, and it will go in the README in Step 8. Sensitivity Table 3 keeps $0, $50, $100, $175 (the old base), and $250 so the effect stays visible.

### 2. Unit count is 97, and BCPA confirms it

Unit Mix now shows 51 1BR/1BA, down from 52. The unit was removed from the most common type, as instructed, and flagged in the note. BCPA's record then confirmed 97 across three folios (Step 5), so the flag now reads "confirmed" rather than "provisional." The unit-type split *within* the 97 is still the listing's, and is still a rent-roll item.

| | 97 units (base) | 98 units |
|---|---|---|
| Year-1 NOI | $916,855 | $928,477 |
| In-place cap / exit cap | 6.14% / 6.64% | 6.22% / 6.72% |
| Unlevered IRR | 5.28% | 5.36% |
| Scenario A levered IRR / EM | 5.20% / 1.27x | 5.43% / 1.28x |
| LP IRR | 5.20% | 5.43% |
| Scenario B levered IRR | 2.31% | 2.53% |
| Year-1 cash-on-cash (A) | 9.62% | 9.84% |

The 98th unit is modeled as a renovated 1BR at $1,673/month. It adds about 23 bps of levered IRR. Part of that is offset by the exit-cap rule, because more NOI at the same price raises the in-place cap and therefore the exit cap.

### 3. Waterfall: how GP capital was treated, and the fix

**What the model did before (the Step-3 version).** The GP co-invest was 10% of equity. Tier 1 paid 100% of cash to the LP until the LP had its 8% pref *and* its capital back, with the pref measured on LP capital only. The GP's co-invest received nothing until then. After that, cash split 70/30 and then 50/50, with the GP co-invest counted inside the GP's 30% or 50%. No acquisition, asset-management, or disposition fees were modeled. In effect the GP's capital was **subordinated** to the LP's. That is why the LP (9.82%) out-earned the deal (7.89%) while the GP's own capital lost money (−15.88%). Nothing in the spec asked for subordinated co-invest. It was a construction error, not an intended structure.

Old split, at the Step-3 state of the model:

| Year | Available cash | Tier 1 (100% to LP) | Tier 2 LP / GP | LP total | GP total |
|---|---|---|---|---|---|
| 0 | | | | −4,585,761 | −509,529 |
| 1 | 564,573 | 564,573 | | 564,573 | 0 |
| 2 | 385,838 | 385,838 | | 385,838 | 0 |
| 3 | 49,397 | 49,397 | | 49,397 | 0 |
| 4 | 276,229 | 276,229 | | 276,229 | 0 |
| 5 | 5,843,217 | 5,127,904 | 500,720 / 214,594 | 5,628,623 | 214,594 |
| IRR / EM | | | | 9.82% / 1.51x | −15.88% / 0.42x |

**What the model does now (standard pari passu).**
- **Investor capital** is LP 90% plus GP co-invest 10%. The two are treated identically.
- **Tier 1:** 100% to investors until they have an 8% compounded pref and their capital back, both measured on *total* investor capital. Investors split each dollar 90/10.
- **Tier 2:** 70% to investors and 30% GP promote, until investors reach a 12% IRR.
- **Tier 3:** 50/50.
- The GP receives its co-invest share of every investor dollar, plus the promote.
- **No fees are modeled.** Most real deals have them (an acquisition fee of about 1% and an asset-management fee of 1–2% of equity, for example). I have not added them because they are outside the spec. Say if you want them.
- A negative year, meaning the Year-3 capital call, flows through Tier 1 as a pro-rata contribution. It raises the pref balance and is split 90/10.

The same Step-3 cash flows under pari passu: LP 7.89% / 1.40x, GP 7.89% / 1.40x, promote $0. Both equal the deal IRR, as they must when the deal is below the pref.

Current base case, split year by year:

| Year | Available cash | Tier 1 | Tier 2 / 3 | LP (90%) | GP co-invest (10%) | GP promote | GP total |
|---|---|---|---|---|---|---|---|
| 0 | | | | −4,585,761 | −509,529 | | −509,529 |
| 1 | 490,239 | 490,239 | 0 | 441,216 | 49,024 | 0 | 49,024 |
| 2 | 309,405 | 309,405 | 0 | 278,465 | 30,941 | 0 | 30,941 |
| 3 | −540,895 | −540,895 | 0 | −486,805 | −54,089 | 0 | −54,089 |
| 4 | 231,094 | 231,094 | 0 | 207,985 | 23,109 | 0 | 23,109 |
| 5 | 5,959,619 | 5,959,619 | 0 | 5,363,657 | 595,962 | 0 | 595,962 |
| IRR / EM | | | | 5.20% / 1.27x | | | 5.20% / 1.27x |

The promote tiers are tested at other prices, where they actually pay out:
- **At $12.0M (Tier 2 reached):** Year-5 cash is $5,248,640. Tier 1 takes $4,970,968. Tier 2 takes $277,672, split $194,370 to investors and $83,301 to the GP promote. Result: deal 9.28%, LP 8.90%, GP 12.48%.
- **At $10.0M (Tier 3 reached):** LP 16.29%, GP 50.00%, promote $637,637.

Both variants tie to a recalculated workbook.

**How `verify_model.py` checks this without mirroring the model.** The workbook rolls two hurdle balances forward year by year. The script uses no balances. For each year it computes the investors' shortfall at each hurdle in closed form, as the future value of the original equity minus the future value of everything investors have received so far. Tier 1 and Tier 2 are then read off those shortfalls. It also asserts two facts that must hold in any correct pari passu waterfall:
- LP plus GP equals available cash in every year.
- With zero promote, LP IRR = GP IRR = deal IRR.

The old subordinated structure fails the second check, so the script cannot pass that bug again.

---

## Change bridge: Step-3 state to current base case

Each row adds one change on top of the row above, run in the verified engine.

| Change | Unlevered | A levered | A EM | B levered | Year-3 A cash flow |
|---|---|---|---|---|---|
| Step-3 state (98 units, $175 premium) | 6.25% | 7.89% | 1.40x | 4.90% | +49,397 |
| Premium to $0 | 5.74% | 6.45% | 1.32x | 3.53% | |
| 97 units | 5.65% | 6.20% | 1.31x | 3.30% | |
| Millage 20.2573 to 20.1710 (BCPA 2026 proposed) | 5.62% | 6.11% | 1.30x | 3.21% | |
| Non-ad valorem assessments $375/unit (new line, BCPA) | 5.28% | 5.13% | 1.25x | 2.31% | −29,415 |
| Refi LTV on value at refi, not on purchase price | 5.28% | 5.20% | 1.27x | 2.31% | −540,895 |

Two of these rows need explanation.

**Non-ad valorem assessments** are the largest single change. They cost $36,375 a year. The old model left them out entirely: BCPA shows them on the actual tax bills (Step 5).

**Refi sizing on value.** The refi had been sized at 65% of the *purchase price*, which is not how a lender sizes a loan. It is now sized on value at refinance, calculated as refi-year (Year 4) NOI of $863,913 divided by the 6.64% exit cap, which gives $13.01M. That value is lower than the purchase price because NOI falls over the hold (see Step 6, property tax). The refi is capped by LTV at $8.46M against a $9.45M payoff. The $991K shortfall, less Year-3 operating cash, is a **$540,895 capital call in Year 3**. The model now shows it as a separate line and includes it in peak equity.

---

## Step 4: Bid price solve

**What moves with price:**
- Reassessed property tax, at price × 85% × millage
- Closing costs, at 1.5%
- Equity
- The Scenario B loan, through its LTV leg
- The going-in cap

**What stays fixed:**
- Rents and all other opex
- Renovation capex
- The assumed loan balances ($9.45M) and the assumption fee
- **The exit cap, which is frozen at the base 6.64%.** Otherwise the model's rule (in-place + 50 bps) would raise the exit cap whenever the buyer pays less, as if the market repriced because of what this buyer paid. The floating version is shown for reference.

The Scenario A refi value moves only through NOI.

Solved with `brentq`. Tolerance is $1.

**Scenario A (assumed loan, base case)**

| Target | Max price | $/unit | vs ask | In-place cap | Deal IRR | LP IRR | GP IRR | Assumed-loan LTV | Price if exit cap floats |
|---|---|---|---|---|---|---|---|---|---|
| (a) LP IRR 8% | $13,273,194 | $136,837 | −3.8% | 6.45% | 8.00% | 8.00% | 8.00% | 71.2% | $12,446,851 |
| (b) Levered IRR 12% | $12,649,932 | $130,412 | −8.3% | 6.85% | 12.00% | 10.86% | 20.55% | 74.7% | $11,279,057 |
| (c) Levered IRR 15% | $12,261,655 | $126,409 | −11.1% | 7.12% | 15.00% | 12.78% | 29.67% | 77.1% | $10,722,578 |

**Scenario B (new debt, alternative)**

| Target | Max price | $/unit | vs ask | In-place cap | Price if exit cap floats |
|---|---|---|---|---|---|
| (a) LP IRR 8% | $12,642,396 | $130,334 | −8.4% | 6.86% | $10,742,611 |
| (b) Levered IRR 12% | $11,838,755 | $122,049 | −14.2% | 7.44% | $9,186,571 |
| (c) Levered IRR 15% | $11,247,732 | $115,956 | −18.5% | 7.92% | $8,245,244 |

**How to read these tables:**

- **Why the lines are steep.** Levered IRR is steep in price under Scenario A. The assumed loan does not shrink as price falls, so each dollar off the price is a dollar off equity. That is also why the assumed-loan LTV climbs to 77% at target (c).
- **LTV risk at lower prices.** Many assumption lenders cap LTV or require a paydown. That is not modeled, so treat (b) and (c) as upper bounds on what Scenario A can support.
- **The Scenario A floor.** Below about $8.78M, the $9.45M assumed loan exceeds total uses. Equity turns negative, and the structure stops making sense. All three targets sit well above that floor.
- **The frozen exit-cap choice matters.** It is worth $0.8–1.5M of bid price. With a floating exit cap, cutting the price also cuts the modeled exit value.
- **The Summary tab.** It carries these rows as typed values, labeled as solver output. `price_solve.py` rechecks them against a fresh solve on every run, and they currently match.

---

## Step 5: Broward County Property Appraiser record

Source: the BCPA parcel search and the parcel-information service, pulled 2026-09-29. The owner of record is Channel Grove LLC. The property is three folios under common ownership.

| Folio | Address | Units | Built | 2025 taxable | 2026 working just value | 2025 total bill |
|---|---|---|---|---|---|---|
| 4842-35-00-0460 | 951 NW 8 Ave | 20 | 1959 | $2,166,930 | $2,402,380 | $51,403 |
| 4842-35-00-0471 | 901 NW 8 Ave | 18 | 1959 | $2,063,740 | $2,162,450 | $48,577 |
| 4842-35-00-0480 | 930–980 NW 9 Ave | 59 | 1958 | $6,088,030 | $7,085,810 | $145,433 |
| **Total** | | **97** | | **$10,318,700** | **$11,650,640** | **$245,413** |

**Units.** The record shows 97, which settles the listing's 97-versus-98 conflict. Two of the three buildings are 1959, not 1958.

**Seller's taxable value.** $10,318,700 matches the listing figure the model already used. It is now marked BCPA-confirmed.

**Reassessment cross-check.** BCPA's 2026 working just value is $11.65M. The model's post-sale reassessment is $13.8M × 85% = $11.73M. These are 0.7% apart, which supports the cost-of-sale method.

**Millage, code 1512 (Pompano Beach).** The 2026 proposed rate is 20.1710 mills. It breaks down as follows:

| Levy | Mills |
|---|---|
| County operating | 5.6658 |
| School operating | 6.2940 |
| School debt | 0.1587 |
| Children's Services | 0.4500 |
| North Broward Hospital | 1.2391 |
| FIND | 0.0270 |
| SFWMD | 0.2301 |
| EMS/fire | 0.5000 |
| City operating | 5.1920 |
| City debt | 0.4143 |

The 2025 final rate was 20.2573. The model now uses 20.1710.

**Non-ad valorem charges.** The 2025 bills total $245,413. Ad valorem tax on $10,318,700 at 20.2573 mills is $209,026. The remaining $36,387, or $375/unit, consists of per-unit charges, mainly the city fire assessment ($331/unit in 2025, with a $20–30 increase proposed for FY2026). These charges do not reset on sale and were missing from the model. They are now a separate opex line at $375/unit, grown at 3.5%.

**Prior sale.** The three folios sold together on 12/23/2021 for $11,760,000, or $121,237/unit. The $13.8M ask is 17.3% above that price, about 3.4% a year over roughly 4.75 years.

---

## Step 6: Assumption review

**Scope.** This covers insurance, each opex line, reserves, and debt terms. I have **not changed any assumption.** Each recommended change is shown with its effect on the verified engine, one at a time.

**About the ranges.** "Reasonable range" means a range for a roughly 100-unit 1958 garden property in Broward. Unless a source is named, the range is my judgment. I could not find a free, citable 2026 opex benchmark for this product type. The seller's T-12 is the real test, and it should be the first diligence request.

**Two IRR columns.** Each impact shows two numbers:
- The *model rule*: exit cap = in-place + 50 bps, so it moves when Day-0 NOI moves.
- *Exit cap frozen* at 6.64%.

The gap between the two columns is itself a finding (flag C below).

### Year-1 operating expenses (97 units)

| Line | Year 1 | $/unit | % of EGI |
|---|---|---|---|
| Payroll | $135,800 | $1,400 | 7.2% |
| Repairs & maintenance | $106,700 | $1,100 | 5.6% |
| Turnover / make-ready | $33,950 | $350 | 1.8% |
| Contract services | $43,650 | $450 | 2.3% |
| Utilities | $48,500 | $500 | 2.6% |
| Insurance | $232,800 | $2,400 | 12.3% |
| Property tax (reassessed) | $236,606 | $2,439 | 12.5% |
| Non-ad valorem | $36,375 | $375 | 1.9% |
| Management (3.5% of EGI) | $66,374 | $684 | 3.5% |
| G&A | $24,250 | $250 | 1.3% |
| Marketing | $14,550 | $150 | 0.8% |
| **Total** | **$979,555** | **$10,099** | **51.7%** |

Reserves of $300/unit ($29,100) sit below NOI.

### Line-by-line review

Base case Scenario A levered IRR is 5.20%. The "Test" column shows the value I ran, and the last two columns give Scenario A levered IRR for that test.

| Line | Model value | Source | Reasonable range | Verdict | Test | A IRR, model rule | A IRR, exit frozen |
|---|---|---|---|---|---|---|---|
| Insurance level | $2,400/unit | Judgment: $2,000 South Florida average from Phase 1 sources, marked up for the undisclosed roof | $1,800–3,000 | Defensible, upper half. One broker source puts *coastal Miami-Dade* at $2,200–2,800/unit and inland at about half that ([Serhant](https://serhantfloridacommercialgroup.com/blog/reading-miamis-2026-multifamily-numbers-against-themselves), weak source). The property is about 2 miles inland. A quote is needed. | $2,000 / $3,000 | 6.57% / 3.05% | 8.18% / 0.63% |
| Insurance growth | 7%/yr | Judgment, based on the 2023–25 trend | 0–5% | **Conservative and dated.** Guy Carpenter reported Florida property-cat reinsurance down about 15–20% at the June 2026 renewals ([Insurance Journal](https://www.insurancejournal.com/news/southeast/2026/06/30/875651.htm)). Compounding 7% for five years assumes that reverses. | 3.5% | 7.48% | 7.48% |
| **Property tax growth** | **10%/yr** | The statutory *cap* | 3–5% (tracks just value) | **Indefensible as a base case.** 10% is the ceiling on annual assessed-value growth for non-school levies, not a growth rate, and the school levy (6.45 mills) is not capped at all. After a sale, assessed value resets to just value, so there is no gap left to catch up. Tax then grows with just value plus any millage changes. At 10% a year, tax rises from $237K to $346K by Year 5, and NOI *falls* every year ($917K to $848K). This error runs in the conservative direction. | 3.5% | 5.79% | 5.79% |
| Non-ad valorem | $375/unit | **Sourced:** BCPA 2025 bills | $350–400 | Defensible. The FY2026 fire increase is about 6–9% against 3.5% modeled growth, which is immaterial (about $2–3K). | none | | |
| Payroll | $1,400/unit | Judgment | $1,200–1,800 | Defensible. It implies about two FTEs (manager and maintenance tech) with burden, and no leasing or porter staff. | $1,600 | 4.69% | 3.89% |
| Repairs & maintenance | $1,100/unit | Judgment, marked up for vintage | $900–1,500 | Defensible, middle of range. A 1958 building likely has original cast-iron drain lines. A plumbing scope in the PCA would move this. | $1,300 | 4.69% | 3.89% |
| Turnover / make-ready | $350/unit/yr | Judgment | $450–650/unit/yr | **Low.** At the modeled 55% turnover this is $636 per turn, which buys paint and cleaning but little flooring or appliance work. | $500 | 4.82% | 4.21% |
| Contract services | $450/unit | Judgment | $350–600 | Defensible | none | | |
| **Utilities** | **$500/unit** | Judgment: "common area / vacant units" | $400–600 if tenants pay water; $900–1,300 if the owner pays water, sewer, and trash | **Internally inconsistent.** Other income ($35/unit/month) includes RUBS, which only exists if the owner pays water and sewer and bills it back. If the owner pays, $500 is too low. If tenants pay directly, RUBS should come out of other income. Buildings of this vintage are usually master-metered for water. This is an aggressive-direction error until the T-12 or rent roll resolves it. | $900 | 4.18% | 2.57% |
| Management fee | 3.5% of EGI | Judgment | 3.0–5.0% | **Low end.** At about $66K a year, 3.5% is achievable only through a large-portfolio manager or an owner-operator platform. Third-party managers usually price about 4–5% for roughly 100 units. | 4.5% | 4.73% | 3.97% |
| G&A | $250/unit | Judgment | $200–400 | Defensible | none | | |
| Marketing | $150/unit | Judgment | $100–200 | Defensible | none | | |
| General expense growth | 3.5%/yr | Judgment | 3.0–4.5% | Defensible | none | | |
| Replacement reserves | $300/unit | Judgment: lender convention | $350–500 for this vintage | **Low for a 68-year-old building.** Agency lenders set the reserve from a property condition assessment ([Fannie Mae MF Guide](https://mfguide.fanniemae.com/node/3416)), and a 1958 asset with an unknown roof is unlikely to come in at the floor. The dated recert line ($160K in Year 2) is separate. | $400 | 5.00% | 5.00% |

### Debt terms

| Term | Model value | Source | Reasonable range | Verdict | Test | A IRR | B IRR |
|---|---|---|---|---|---|---|---|
| SOFR | 3.85%, held flat | Sourced (sofrrate.com, 9/18/2026). Holding it flat is judgment. | | Defensible as a simplification. No forward curve is modeled. | +50 bps | 4.90% | 1.49% |
| Spread / all-in rate | +325 bps, 7.10% floating | Judgment, within the 200–500 bps bridge range | | **Mismatched to the asset.** 73 of 97 units are already renovated, so an agency fixed-rate loan is the natural execution for both new debt and the Year-4 takeout. One broker site quoted a Freddie Mac 5-year fixed at 6.20% on 9/11/2026 ([apartmentloanstore](https://apartmentloanstore.com/loan-product/apartment-multifamily-loan-interest-rates); indicative, not a term sheet). Separately, **floating debt without a rate-cap cost is incomplete.** Bridge lenders require a cap, and its cost is not modeled. | 6.20% fixed | 5.74% | 3.78% |
| LTV / DSCR / debt yield | 65% / 1.25x / 8.0% | Judgment | Agency roughly 70–80% / 1.25x | Defensible and conservative. LTV binds: B loan $8.97M, with the DSCR leg at $10.33M and the DY leg at $11.46M. | none | | |
| IO / amortization (B and refi) | 2 years IO, then 30-year amortization | Judgment | | Defensible | none | | |
| Assumed first mortgage | $5,887,000 at 3.0% fixed, matures Dec 2029 (Year 3) | **Sourced:** Crexi / LoopNet | | Balance differs from LoopNet by $21,934, probably a different as-of date. Year 3 assumes a close around January 2027. | none | | |
| Supplemental loan | $3,563,000 at 6.2% | **Sourced:** Crexi / LoopNet | | The loan terms are sourced. Treating it as coterminous with the first is judgment. | none | | |
| Both assumed loans IO | Yes | **Judgment**, not disclosed | | Plausible. It is consistent with the broker's roughly 10% Day-1 cash-on-cash. | Amortizing | 5.17% (Year-3 call falls to $186,896) | |
| Assumption fee | 0.5% | Judgment | 0.5–1.0% | **Low end.** 1% is the more common figure. | 1.0% | 4.99% | |
| Refi sizing | 65% of refi-year NOI / exit cap | Judgment | | Defensible. It produces the $540,895 Year-3 capital call. | | | |
| Assumed-loan LTV at ask | 68.5% | Calculated | | Year-1 DSCR is 2.31x and debt yield 9.7% | | | |

### Flags

**Indefensible or internally inconsistent. Recommend changing, with your approval:**

- **A. Property tax grows at 10% a year.** This is a misreading of the non-homestead cap. It should grow with just value, which needs a new input, and judgment would put it around 3–4%. Correcting it raises Scenario A to 5.79% and eliminates the Year-3 capital call. This single input is also why NOI declines over the hold.
- **B. Utilities of $500/unit alongside RUBS income.** Either the owner pays water and sewer, in which case this line should be about $900–1,300, or tenants do, in which case RUBS should come out of other income. The T-12 or rent roll decides which.
- **C. The exit-cap rule absorbs opex errors.** Because exit cap = in-place cap + 50 bps, any opex increase lowers the in-place cap and therefore the exit cap. Part of every opex mistake gets repaid at sale. The IRR columns above show the size of this effect: the utilities fix costs 102 bps under the rule and 263 bps with the exit cap frozen. The market cap rate at exit does not depend on our opex estimate. I recommend making the exit cap a direct input, currently 6.64%, supported by sale comps. The in-place + 50 bps figure would then be reported only as a cross-check. This reverses a rule you chose last round, so it is your call.
- **D. Floating-rate debt with no rate-cap cost** (Scenario B and the Year-4 refi). Either add the cap cost or switch to fixed agency terms.

**Low but defensible only with support:** management fee 3.5%, turnover $350/unit, reserves $300/unit, assumption fee 0.5%.

**Conservative:** insurance growth 7%, insurance level $2,400/unit (pending a quote), all-in debt rate 7.10%.

### The flags together

These runs are not applied to the model. Group 1 is the aggressive-side corrections: utilities $900, management 4.5%, turnover $500, reserves $400, assumption fee 1%. Group 2 is the conservative-side corrections: tax growth 3.5%, insurance growth 3.5%.

| Case | Year-1 NOI | A IRR, model rule | A IRR, exit frozen at 6.64% | B IRR, exit frozen | Year-3 capital call, exit frozen |
|---|---|---|---|---|---|
| Base | $916,855 | 5.20% | 5.20% | 2.31% | $540,895 |
| Group 1 only | $844,541 | 2.93% | −0.05% | −3.17% | $1,405,799 |
| Group 2 only | $916,855 | 8.12% | 8.12% | 5.16% | $0 |
| Groups 1 + 2 | $844,541 | 5.94% | 2.83% | 0.20% | $575,731 |
| Groups 1 + 2, plus 6.20% fixed refi and new debt | $844,541 | 6.52% | 3.40% | 1.70% | $575,731 |

The aggressive-side and conservative-side errors roughly cancel under the current exit rule. With the exit cap set by the market, the opex corrections dominate. **No combination tested reaches the 8% pref at $13.8M unless the opex corrections are left out.** That leaves Step 4's conclusion intact: the deal needs a lower price, or a T-12 materially better than these assumptions.

---

## Verification status

- `verify_model.py` covers 163 lines and 702 figures. All tie to the recalculated workbook within $1 or 1 bp. It reads only literal input cells, and it confirms that none of them is a formula.
- Price variants at $12.0M (Tier 2) and $10.0M (Tier 3), and the 98-unit variant, were each rebuilt, recalculated, and verified. All tie.
- `price_solve.py` confirms that the Summary Bid Price rows match a fresh solve within $1,000.
- CHECKS tab: all pass. There are no formula errors.

## Files changed in this commit

- **`build_model.py`:**
  - Premium set to $0, 97-unit mix, millage 20.1710, non-ad valorem line
  - Refi sized on value, capital call and peak equity rows
  - Pari passu waterfall
  - Two-scenario Bid Price section
  - Sensitivity Table 3 values
- **`verify_model.py`:** matching inputs, an independent closed-form pari passu waterfall with structural assertions, refi on value, and capital-call rows.
- **`price_solve.py`:** both scenarios, frozen and floating exit cap, closed-form Scenario A floor, and the Summary staleness check.
- **`Parkview_Crossing_Acquisition_Model.xlsx`:** rebuilt and recalculated.

## Next (not started): Steps 7–9

- **Step 7:** Rebuild the sensitivities on Scenario A, with exit cap to +100 bps and a secondary new-debt table.
- **Step 8:** README, waterfall walkthrough, and interview Q&A.
- **Step 9:** One-page summary and resume bullets.

If you approve any of flags A–D, they should go in before Step 7, so the sensitivities and docs are built on the corrected base.
