# Multifamily Acquisition Model

**Status: stub.** The full README (model structure, assumption sources, deal thesis, limitations) will be written in Phase 4, once the model is built and verified. This file exists now to hold the two sections below, both written during Phase 1 at explicit request.

## Deal thesis: light value-add / core-plus, not heavy value-add

The subject property, Parkview Crossing (97 units, Pompano Beach, FL), has already had 75% of its units renovated by the current owner — kitchens, mini-split AC, vinyl slider windows, and lighting — alongside $1M+ in building-wide capital work (electrical, fencing, parking, security, common-area lighting). That changes what kind of deal this is. A buyer here isn't taking on a full repositioning; they're finishing a program someone else mostly completed. The return drivers are:

1. **Finishing the remaining ~24 unrenovated units** with a small, low-risk capital program.
2. **Loss-to-lease burn-off** on units — including some already-renovated ones — still priced below what the broker's own materials describe as achievable market rent.
3. **Market rent growth** over the hold period.
4. **Expense management**, which carries more weight than usual here given a 68-year-old building's insurance exposure and an unresolved building-recertification timeline.

Which of these four actually contributes the most to total return is a question the built model needs to answer, not something to assert in advance — that decomposition will be reported once the Phase 2 model is running.

## Alternative strategy considered: Florida's Live Local Act

During Phase 1 due diligence, I researched Florida's Live Local Act (currently in its "4.0" iteration under House Bill 1389, effective July 1, 2026) as a possible alternative structure for this deal. The Act grants a property-tax exemption to qualifying multifamily developments — 75% of assessed value exempted on affordable units if less than the whole project is affordable, or 100% if the entire project is — provided the property has at least 71 units and reserves at least 40% of units as affordable (at or below 100% AMI) for a minimum 30-year term. Parkview Crossing's 97 units clear the size threshold. I did not model this option, and don't recommend pursuing it here: even under the corrected light-value-add/core-plus thesis above, the return still depends on pushing rents on the remaining classic units and burning off loss-to-lease on the rest toward market — while Live Local requires permanently capping at least 40% of units below market for three decades in exchange for the tax break. The two strategies pull in opposite directions on the same units, regardless of how "heavy" the underlying renovation program is. It's worth understanding as a live option in the Florida market generally, but it conflicts with, rather than complements, the underwriting approach used here.

## Exit valuation: the tax-adjusted exit cap

Every buyer of Florida investment real estate gets reassessed to (roughly) what they paid, the year after they buy. That's true of us going in, and it'll be true of whoever buys this property from us at exit, five years out. Most simple models ignore this at exit — they just capitalize forward NOI (which already has some property-tax number baked in) at an assumed exit cap rate. That's fine as an approximation, but it quietly assumes the exit buyer's tax bill doesn't change with the price they pay, which isn't how Florida property tax actually works.

The correct version has a circularity problem: the exit buyer's post-tax NOI depends on their tax bill, which depends on the price they pay, which is exactly the number we're trying to solve for. Here's the algebra that breaks the circularity:

Let `P` = exit price, `T` = the effective combined millage rate (as a percentage of assessed value), and `NOI_pretax` = forward NOI calculated *before* subtracting property tax expense (i.e., every other operating line is already netted out).

The exit buyer's post-tax NOI, once reassessed, is `NOI_pretax − (T × P)`. We want to find the price at which that post-tax NOI, divided by the price, equals our assumed exit cap rate `C` (an ordinary post-tax cap rate — the same kind of number as every other cap rate in this model):

```
C = (NOI_pretax − T×P) / P
C×P = NOI_pretax − T×P
P×(C + T) = NOI_pretax
P = NOI_pretax / (C + T)
```

So instead of capitalizing NOI at the exit cap rate alone, we capitalize **pre-tax NOI** at **(exit cap rate + effective tax rate)**. The effect is intuitive once you see it: a higher property tax rate acts exactly like a higher cap rate from the exit buyer's perspective, because it's another claim on the income stream that scales with price. Leaving this out overstates exit value in any market — like Florida — where non-homestead reassessment on sale is real and material.

This model uses that formula for exit valuation. See `PHASE1_ASSET_AND_ASSUMPTIONS.md` for the specific effective tax rate used and a worked illustrative example (with placeholder NOI, pending the actual Phase 2 model output).
