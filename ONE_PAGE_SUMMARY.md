# Parkview Crossing: Acquisition Summary

**The property.** 97 units, built 1958-59, at 901-951 NW 8th Ave, Pompano Beach, FL. Asking price $13.8M ($142,268/unit). The owner of record bought it in December 2021 for $11.76M, so the ask is 17.3% higher. About 75% of the units are already renovated.

**Recommendation: do not pay the ask.** The most I would pay is about $13.1M. That is the price at which the LP clears its 8% preferred return using the seller's assumable debt.

## The plan

- **Finish the renovation.** Renovate the last 24 classic units at $20,460 per unit. They reach market rent from Year 2.
- **Burn off loss-to-lease.** Let the 73 already-renovated units close toward market as they turn over.
- **Assume the seller's debt.** Take over the $5.887M first mortgage at 3.0% (to December 2029) and the $3.563M supplemental loan at 6.20%.
- **Refinance and sell.** Refinance in Year 4 with an agency fixed-rate loan at 7.24%, and sell at the end of Year 5.

## Base case at $13.8M (assumed debt)

| | |
|---|---|
| Total cost / equity | $14.55M / $5.10M (90% LP, 10% GP co-invest) |
| Cap rate: broker / in-place (reassessed tax) / Year 1 | 7.0% / 5.86% / 6.36% |
| Year-1 NOI; operating expenses | $878,230; $10,736 per unit (54% of revenue) |
| Exit (end of Year 5) | 6.60% cap, $14.54M ($149,920/unit) |
| Year-4 refinance | $8.92M loan against $9.45M payoff; $38,965 capital call |
| **Levered IRR / multiple** | **4.19% / 1.20x** (LP = GP, no promote) |
| Unlevered IRR | 5.53% |
| Year-1 cash-on-cash | 8.86% |
| With new agency debt instead | 2.45% levered IRR |

Leverage lowers the return. New debt at 7.24% costs more than the property's 6.36% Year-1 yield, and the refinance pays a 5% prepayment premium at sale.

## Maximum price by target

| Target | Assumed debt | New debt |
|---|---|---|
| LP IRR 8% | $13.11M ($135,113/unit, 5.0% below ask) | $12.57M |
| Levered IRR 12% | $12.51M (9.3% below ask) | $11.92M |
| Levered IRR 15% | $12.08M (12.5% below ask) | $11.46M |

## What moves the answer (levered IRR, assumed debt)

| Change | Effect on IRR |
|---|---|
| Exit cap 6.10% / 7.10% (±50 bps) | 7.37% / 0.97% |
| Rent growth ±0.5% every year | 6.34% / 1.97% |
| Price 10% below ask ($12.42M) | 12.62% |
| $100/month renovation premium over market | 5.66% |

## Method and verification

**Property tax.** Reassessed to 85% of the price (Fla. Stat. 193.011(8)), then grows 3% a year with market value. The 10% cap in 193.1555 is a ceiling, not a growth rate. The exit price accounts for the next buyer's reassessment.

**Verification.** `verify_model.py` rebuilds the model from the input cells alone and matches 945 figures to within $1 or 1 bp, including all 200 sensitivity cells.

## Open diligence items

- Rent roll and T-12
- Who pays water, sewer and trash; the lease form (RUBS clause)
- Roof condition and 40/50-year recertification status
- Insurance quote
- Loan documents: interest-only status, assumption test and fee
