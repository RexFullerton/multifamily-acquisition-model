# Interview Q&A

These are fifteen questions a VP reviewing this model would likely ask, with the answers I would give. Every number is from the verified workbook (Scenario A base case at $13.8M unless stated).

---

**1. Give me the deal in a minute.**

The property:
- Parkview Crossing: 97 units, built 1958-59, Pompano Beach.
- Asking price $13.8M, or $142,268 per unit.
- The seller has renovated about 75% of the units. The plan is to finish the last 24 at about $20,500 each and let the rest of the rents drift up to market as units turn over.
- The seller's 3.0% first mortgage is assumable until December 2029.

The result:
- At the ask, the deal returns a 4.19% levered IRR and 1.20x over five years.
- The unlevered return is 5.53%.
- It does not reach the 8% pref.

My conclusion: the most I would pay for an 8% LP return is about $13.1M.

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

The spread is judgment. CBRE says expectations of rising cap rates are strongest for Class C, but its market tables are gated. The two named comps have no public NOI, so neither gives an implied cap rate:
- Cascades at the Hammocks sold for $65.5M, or $248,106 per unit.
- Savona Grand sold at an undisclosed price.

I used to set the exit cap at the entry cap plus 50 bps. I dropped that because it quietly offsets expense mistakes: raise an expense and the entry cap falls, and so does the exit cap. The market does not price a building off my expense estimate.

Each 50 bps of exit cap moves the IRR by about 3.2 points.

---

**5. Why is the levered IRR below the unlevered IRR?**

Leverage is working against the deal. Three things drive it:
- **Negative spread.** The property yields 6.36% in Year 1, and the refinance and any new loan cost 7.24%. Once the 3.0% loan matures in Year 3, the debt costs more than the property earns.
- **Prepayment premium.** The refinance is a 10-year fixed loan repaid in its second year, so it pays a 5% premium at sale: $436,819.
- **Transaction costs.** The assumption fee and the Year-3 capital call add small costs.

With new debt instead (Scenario B), the levered IRR is 2.45%.

---

**6. What is the assumable loan worth?**

At the same price, assuming the debt returns 4.19% levered, against 2.45% with new agency debt: about 174 bps. It also needs about $890,000 less equity.

But the benefit only lasts three years. After December 2029 the deal refinances at market rates.

---

**7. Walk me through the refinance.**

The first mortgage matures in Year 3, and the combined $9.45M balance has to be repaid.

The new agency loan is sized at the lower of two limits:
- 75% of value, where value is $920,697 of NOI divided by the 6.60% cap, or $13.95M;
- a 1.25x DSCR on the amortizing payment at 7.24%.

The DSCR limit binds at $8,923,868. That leaves $526,132 to fund. Year-3 operating cash covers most of it, and investors put in a $38,965 capital call. Peak equity is $5,134,255.

---

**8. How does the waterfall work, and why do the LP and GP get the same IRR?**

The GP's 10% co-invest is pari passu with the LP. The tiers are:
- Tier 1: 100% to investors until they have their capital back plus 8%.
- Tier 2: 70/30 until they reach a 12% IRR.
- Tier 3: 50/50 after that.

At the ask, investors never reach 8%, so everything is Tier 1. The LP and GP both earn exactly the deal's 4.19%.

At a $12.0M price, all three tiers pay:
- LP 13.11%
- GP 31.31%
- Promote $624,446

`WATERFALL_WALKTHROUGH.md` has the year-by-year figures.

---

**9. What is your bid?**

My maximum bid is $13.1M ($135,113 per unit), the price at which the LP earns exactly 8% with the assumed debt:

| Target | Assumed debt | New debt |
|---|---|---|
| 8% LP return | $13.1M | $12.6M |
| 12% levered IRR | $12.5M | $11.9M |
| 15% levered IRR | $12.1M | $11.5M |

At all three assumed-debt prices, I built the full workbook and confirmed it returns the target exactly.

Below about $12.6M, I assume the lender requires a paydown at assumption: $388,793 at the 15% price.

---

**10. The seller paid $11.76M in December 2021. Does the $13.8M ask make sense?**

The ask is 17.3% above that price, about 3.4% a year. Over the same period, the seller renovated roughly three quarters of the units and did over $1M of building work. The property is in better shape than the one they bought.

What has not improved is the income on a buyer's basis:
- The reassessed tax and the actual non-ad valorem charges hold the in-place cap at 5.86%.
- Rates are higher than in 2021. The 10-year Treasury was 5.24% on September 28, 2026.

My 8%-LP price of $13.1M is still 11.4% above the 2021 price. That seems to me a fair credit for the renovations. $13.8M does not.

---

**11. What are the biggest risks?**

In order of how much they move the answer:
1. **Exit cap.** About 3.2 points of IRR per 50 bps.
2. **Rent growth.** About 2.2 points per 0.5% a year.
3. **Insurance.** At $2,400 per unit, it is 12% of revenue. The roof and the 40/50-year recertification are unknown.
4. **Refinance rate in 2029.** That rate is set by the 10-year Treasury at the time, not today.
5. **Assumption approval and terms.** It is not disclosed whether the loans are interest-only or what test the lender will apply at assumption.

---

**12. What is the weakest assumption?**

The rents by unit type. I built them from the broker's disclosed 20.76% upside and zip-code averages, not from a rent roll.

After that:
- **Utilities.** The listing does not say who pays water, sewer and trash, so I assumed the owner pays, with 60% recovered through RUBS.
- **Water use.** I assumed 3,000 gallons per unit per month.
- **Exit cap spread.** The 100 bps Class C spread is judgment.

The rent roll, T-12, utility bills and lease form would answer most of these in a day.

---

**13. Why a $0 renovation premium?**

The 24 classic units are renovated to the same standard as the other 73, and those units define market rent. Charging a premium on top of market would count the same upgrade twice.

The renovation's value is closing a gap of about $300 per month per unit up to market. The sensitivity table shows what a premium would add: about 74 bps of IRR for each $50 per month.

---

**14. Would you really take out a 10-year fixed loan and pay 5% to prepay it two years later?**

Probably not. The instruction was to price off the 10-year Treasury, and I modeled Fannie Mae's actual declining-premium schedule (5-5-4-4-3-3-2-2-1-1), which costs about 160 bps of IRR.

In practice I would look at other structures:
- a 5-year fixed loan;
- a floating-rate agency loan;
- selling with the loan assumed by the buyer.

The first two would need another pricing source. The third depends on the buyer. I left the base case conservative and flagged it.

---

**15. How do you know the model is right?**

`verify_model.py` reads only the input cells, rebuilds everything with separate code, and compares 945 figures with the workbook to within $1 or 1 bp. That includes:
- every operating line for ten years;
- both debt schedules;
- the waterfall tier by tier;
- all 200 sensitivity cells, each re-run through the full engine.

It checks the waterfall a different way from the workbook (closed-form, not rolling balances). It also asserts that the LP IRR equals the GP IRR when no promote is paid.

What it does not prove is that the assumptions are right. The same person wrote both sides, and both missed two bugs until a review caught one and new work exposed the other:
- the GP's co-invest was paid behind the LP, when it should be pari passu;
- renovated units never reached full market rent, which cost 267 bps.
