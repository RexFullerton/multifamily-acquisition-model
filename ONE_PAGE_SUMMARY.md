# Parkview Crossing: Acquisition Summary

**The property.** 97 units, built 1958-59, at 901-951 NW 8th Ave, Pompano Beach, FL. Asking price $13.8M ($142,268/unit). The owner of record bought it in December 2021 for $11.76M, so the ask is 17.3% higher. About 75% of the units are already renovated.

**Recommendation: do not pay the ask.** The most I would pay is about $13.37M. That is the price at which the LP clears its 8% preferred return using the seller's assumable debt.

## The plan

- **Finish the renovation.** Renovate the last 24 classic units at $20,460 per unit. They reach market rent from Year 2.
- **Burn off loss-to-lease.** Let the 73 already-renovated units close toward market as they turn over.
- **Assume the seller's debt.** Take over the $5.887M first mortgage at 3.0% (to December 2029) and the $3.563M supplemental loan at 6.20%.
- **Refinance and sell.** At maturity, refinance into a floating loan: SOFR + 300 bps (6.73%), interest-only, with a 2-year cap at a 4.50% strike. Sell at the end of 2031 with no prepayment premium.

## Base case at $13.8M

| | |
|---|---|
| Total cost / equity | $14.55M / $5.10M (90% LP, 10% GP co-invest) |
| Cap rate: broker / in-place (reassessed tax) / Year 1 | 7.0% / 5.86% / 6.36% |
| Year-1 NOI; operating expenses | $878,230; $10,736 per unit (54% of revenue) |
| 2029 refinance | $8.70M loan against $9.45M payoff; $93,950 cap; $357,752 capital call |
| Exit (end of Year 5) | 6.60% cap, $14.54M ($149,920/unit) |
| **Levered IRR / multiple** | **5.73% / 1.29x** (LP = GP, no promote) |
| Unlevered IRR | 5.53% |
| Year-1 cash-on-cash | 8.86% |

## Exit plan when the 3.0% loan matures (levered IRR)

| Plan | IRR |
|---|---|
| Sell at maturity (3-year hold) | 4.23% |
| **Floating + cap refinance (base case)** | **5.73%** |
| 5-year fixed refinance (4% prepayment premium at sale) | 4.58% |
| 10-year fixed refinance (5% premium, comparison only) | 4.19% |
| New 5-year agency fixed debt at closing, matched to the hold (Scenario B) | 3.36% |

## Maximum price by target

| Target | Assumed debt | New debt |
|---|---|---|
| LP IRR 8% | $13.37M ($137,835/unit, 3.1% below ask) | $12.79M |
| Levered IRR 12% | $12.73M | $12.12M |
| Levered IRR 15% | $12.29M | $11.65M |

## What moves the answer

| Change | Levered IRR |
|---|---|
| Exit cap 6.10% / 7.10% (±50 bps) | 8.70% / 2.79% |
| Rent growth ±0.5% every year | 7.79% / 3.63% |
| SOFR at the 4.50% cap strike for both refinance years | 5.26% |
| Price 10% below ask ($12.42M) | 14.11% |

**Method.** Property tax is reassessed to 85% of the price (Fla. Stat. 193.011(8)) and grows 3% a year with market value; the 10% cap in 193.1555 is a ceiling, not a growth rate. `verify_model.py` rebuilds the model from the input cells alone and matches 1,080 figures within $1 or 1 bp. Rates are FRED observations for 9/28/2026 (SOFR30DAYAVG, DGS5, DGS10).

**Diligence:** rent roll and T-12; who pays utilities and whether leases have a RUBS clause; roof and 40/50-year recertification; insurance quote; assumed-loan documents; 2029 floating-debt terms.
