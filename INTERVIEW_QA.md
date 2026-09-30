# Interview Q&A

These are questions a VP reviewing this model would likely ask, with the answers I would give. Every number is from the verified workbook: the Scenario A base case at $13.8M, assuming the seller's debt, refinancing into a capped floating loan in December 2029, and selling at the end of Year 5, unless stated otherwise.

---

**1. Give me the deal in a minute.**

The property:
- Parkview Crossing: 97 units, built 1958-59, Pompano Beach.
- Asking price $13.8M, or $142,268 per unit.
- The seller has renovated about 75% of the units. The plan is to finish the last 24 at about $20,500 each and let the rest of the rents drift up to market as units turn over.
- The seller's 3.0% first mortgage is assumable until December 2029. At that point I refinance into a short floating loan with a rate cap, then sell in 2031.

The result:
- At the ask, the deal returns a 5.73% levered IRR and 1.29x.
- That does not reach the 8% pref.

My conclusion: the most I would pay for an 8% LP return is about $13.37M.

---

**2. The broker says 7.0% cap. You say 5.86%. Why?**

The broker's cap rate uses the seller's property tax. After a sale, Florida reassesses the property to about 85% of the price. That takes Year-1 tax from about $208,000 to $236,606.

I also include expenses the listing does not show:
- $375 per unit of non-ad valorem charges, mainly the fire assessment, taken from the actual tax bills;
- owner-paid water, sewer and trash, net of what RUBS recovers;
- my own operating-expense estimates.

On in-place rents with the buyer's tax, NOI is $808,528, which is 5.86% of $13.8M. Year-1 NOI, which includes the first renovations and some burn-off, is $878,230, a 6.36% cap. Neither number reaches 7%.

---

**3. How do you grow property tax, and why not at the 10% cap?**

The 10% cap in Fla. Stat. 193.1555 limits how fast assessed value can rise. It is a ceiling, not a growth rate. It exists so owners whose market value rose faster catch up slowly.

After a sale, assessed value resets to just value, so there is nothing to catch up. Tax grows with market value. I tie it to the model's 3.0% terminal rent growth.

My first version grew tax at 10% a year, which made NOI fall every year. Correcting it was worth 63 bps of IRR on its own.

---

**4. Where does the 6.60% exit cap come from?**

It has two parts:
- **Market level, 5.60%.** Matthews reports a 5.6% Fort Lauderdale multifamily average. Colliers reports South Florida "near 5.0%" across all classes.
- **Class C spread, 100 bps.** This is for a Class C building that will be about 73 years old at sale.

The spread is judgment. CBRE says expectations of rising cap rates are strongest for Class C, but its market tables are gated. The two named comps have no public NOI, so neither gives an implied cap rate.

I used to set the exit cap at the entry cap plus 50 bps. I dropped that because it quietly offsets expense mistakes: raise an expense and the entry cap falls, and so does the exit cap.

Each 50 bps of exit cap moves the IRR by about 3.0 points.

---

**5. Why does the assumed loan's maturity drive the hold period?**

The only reason to take over this debt is the 3.0% first mortgage, and that rate ends in December 2029. At that point the whole $9.45M has to be repaid, so the maturity forces a decision:
- sell;
- refinance at today's rates;
- or refinance and sell soon after.

I compared all three at the same price:

| Plan | Levered IRR | Multiple |
|---|---|---|
| Sell at maturity (3-year hold) | 4.23% | 1.12x |
| Refinance into a capped floating loan, sell in 2031 (base case) | 5.73% | 1.29x |
| Refinance into a 5-year fixed loan, sell in 2031 | 4.58% | 1.22x |
| Refinance into a 10-year fixed loan, sell in 2031 | 4.19% | 1.20x |

Selling at maturity avoids refinancing risk. But it pays acquisition and sale costs over three years and sells before the renovation and burn-off show up in two full years of NOI.

A longer hold only works if the refinance can be repaid cheaply at the sale, which is why fixed-rate debt with a prepayment premium performs poorly here. The loan maturity sets the decision date. The prepayment terms of the replacement debt then decide whether a longer hold pays.

---

**6. Why is levered IRR only slightly above unlevered?**

The levered IRR is 5.73% and the unlevered 5.53%, so leverage adds about 20 bps.
- **Years 1-3.** The assumed debt costs about 4.2% blended against a 6.36% Year-1 yield, which is positive leverage.
- **After the refinance.** The loan costs 6.74% against about a 6.6% property yield, roughly neutral.
- **The costs.** The cap premium and the Year-3 equity contribution take back most of the early gain.

With new debt at closing (Scenario B, 7.24%), levered IRR is only 2.45%.

---

**7. What is the assumable loan worth?**

At the same price, assuming the debt returns 5.73% against 2.45% with new agency debt: about 328 bps. It also needs about $890,000 less equity at closing.

But the benefit lasts only three years, which is why the exit plan matters as much as it does.

---

**8. Walk me through the refinance.**

In December 2029 the $9.45M of assumed debt has to be repaid.

The new loan:
- **Pricing.** 30-day average SOFR (3.74%) + 300 bps = 6.74%, interest-only.
- **Rate cap.** A 2-year cap at a 4.50% strike, costing 1.08% of the loan ($93,950).
- **Sizing.** 1.25x DSCR at the capped rate (7.50%), which gives $8,699,030.

Funding the gap:
- The payoff, less the new loan, plus the cap, needs $844,919 of cash.
- Year-3 operations cover part of it. Investors put in $357,752.

At the 2031 sale there is no prepayment premium.

Why floating rather than fixed:
- The 5-year fixed alternative (7.06%) would cost a 4% premium at a sale in loan year 2. Its financing cost is 8.98% of the loan a year, against 7.28% for floating.
- Even with SOFR at the cap strike for both years, the floating plan returns 5.26%.

---

**9. How does the waterfall work, and why do the LP and GP get the same IRR?**

The GP's 10% co-invest is pari passu with the LP. The tiers are:
- Tier 1: 100% to investors until they have their capital back plus 8%.
- Tier 2: 70/30 until they reach a 12% IRR.
- Tier 3: 50/50 after that.

At the ask, investors never reach 8%, so everything is Tier 1. The LP and GP both earn exactly the deal's 5.73%.

At a $12.0M price, all three tiers pay:
- LP 13.88%
- GP 35.59%
- Promote $832,934

`WATERFALL_WALKTHROUGH.md` has the year-by-year figures.

---

**10. What is your bid?**

My maximum bid is $13,368,909 ($137,824 per unit), the price at which the LP earns exactly 8% on the base case:

| Target | Assumed debt | New debt |
|---|---|---|
| 8% LP return | $13.37M | $12.57M |
| 12% levered IRR | $12.73M | $11.92M |
| 15% levered IRR | $12.29M | $11.46M |

At all three assumed-debt prices, I built the full workbook and confirmed it returns the target exactly.

Below about $12.6M, I assume the lender requires a paydown at assumption: $235,075 at the 15% price.

---

**11. The seller paid $11.76M in December 2021. Does the $13.8M ask make sense?**

The ask is 17.3% above that price, about 3.4% a year. Over the same period, the seller renovated roughly three quarters of the units and did over $1M of building work.

What has not improved is the income on a buyer's basis:
- The reassessed tax and the actual non-ad valorem charges hold the in-place cap at 5.86%.
- Rates are higher than in 2021. The 10-year Treasury was 5.24% on September 28, 2026.

My 8%-LP price of $13.37M is 13.7% above the 2021 price. That seems to me a fair credit for the renovations. $13.8M does not.

---

**12. What are the biggest risks?**

In order of how much they move the answer:
1. **Exit cap.** About 3.0 points of IRR per 50 bps.
2. **Rent growth.** About 2 points per 0.5% a year.
3. **Refinance market in 2029.** Floating spreads, cap prices and availability for a loan of about $8.7M. Doubling the cap cost alone takes the IRR to 5.37%.
4. **Insurance.** At $2,400 per unit, it is 12% of revenue. The roof and the 40/50-year recertification are unknown.
5. **Assumption approval.** It is not disclosed whether the loans are interest-only or what test the lender will apply.

---

**13. What is the weakest assumption?**

The rents by unit type. I built them from the broker's disclosed 20.76% upside and zip-code averages, not from a rent roll.

After that:
- **Utilities.** The listing does not say who pays water, sewer and trash. I assumed the owner pays, with 60% recovered through RUBS; 50% or 70% moves IRR to 5.18% or 6.27%.
- **Water use.** I assumed 3,000 gallons per unit per month.
- **Refinance terms.** The floating spread and the interest-only assumption are judgment.

---

**14. Why a $0 renovation premium?**

The 24 classic units are renovated to the same standard as the other 73, and those units define market rent. Charging a premium on top of market would count the same upgrade twice.

The renovation's value is closing a gap of about $300 per month per unit up to market. The sensitivity table shows what a premium would add: about 72 bps of IRR for each $50 per month.

---

**15. You first priced the refinance as a 10-year fixed loan. What changed?**

That loan would have been repaid in its second year at a 5% premium, $436,819, which cost about 160 bps of IRR. No sponsor planning a 2031 sale would take that debt. Pricing it that way was a structural mistake.

The model now compares the three exit plans in Q5 and uses the cheapest refinance that can be repaid at the sale, which moved the base case from 4.19% to 5.73%.

Scenario B still uses a 10-year fixed loan with a 3% premium at the year-5 sale. A 5-year loan matched to the hold would avoid it. I flagged that change rather than making it.

---

**16. How do you know the model is right?**

`verify_model.py` reads only the input cells, rebuilds everything with separate code, and compares 1,078 figures with the workbook to within $1 or 1 bp. That includes:
- every operating line for ten years;
- all three refinance options and all four exit plans;
- the waterfall tier by tier;
- all 200 sensitivity cells, each re-run through the full engine.

It checks the waterfall a different way from the workbook (closed-form, not rolling balances). It also asserts that the LP IRR equals the GP IRR when no promote is paid.

What it does not prove is that the assumptions are right. The same person wrote both sides, and both missed two bugs until a review caught one and new work exposed the other:
- the GP's co-invest was paid behind the LP, when it should be pari passu;
- renovated units never reached full market rent, which cost 267 bps.
