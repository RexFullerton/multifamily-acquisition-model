# Steps 1–3: Exit Cap Check, Base Case Labels, Independent Verification

Prepared 2026-09-29. Stop point after Step 3, per instruction.

## Step 1 — Exit cap

Confirmed correct: `Returns!B33` (entry-cap anchor) points to the in-place, Day-0, reassessed-tax cap rate (primary cost-of-sale method), and the exit cap is that anchor + 50 bps, applied to Year-6 forward NOI before property tax in the tax-adjusted formula, net of 2% cost of sale. It was fixed in the previous round. The isolated before/after below comes from repointing only that one cell in a scratch copy and recalculating. The figures are from that point in time, on 97 units. Step 3's unit fix moved them slightly (see below).

| | Before (7.23% anchor) | After (6.56% anchor) |
|---|---|---|
| Exit cap | 7.73% | 7.06% |
| Unlevered IRR / EM | 5.03% / 1.245x | 6.32% / 1.316x |
| Scen A levered IRR / EM | 4.37% / 1.204x | 8.07% / 1.407x |
| Scen B levered IRR / EM | 1.48% / 1.070x | 5.07% / 1.257x |
| LP IRR (Scen A) | 6.98% | 9.96% |

## Step 2 — Base case and labels

Scenario A (assumed debt) is the base case. Every tab title now names its scenario. Tabs that don't depend on debt are labeled debt-agnostic. So are the headline rows on both Returns tabs, the Summary rows, and the scenario-specific CHECKS sections. The Sensitivity grids are built on Scenario B's debt structure, and the tab now says so explicitly. Step 7 is the place to decide whether to rebuild them on Scenario A.

## Step 3 — verify_model.py

The script reads only literal input cells: Assumptions and the Unit Mix inputs. It finds each one by label and asserts that none is a formula. It recomputes everything with its own engine, then compares against the recalculated workbook line by line.

**Result: 146 lines, 661 figures, all within $1 / 1 bp.**

### Model fixes made in this step
1. **Unit count inconsistency (97 vs. 98).** Unit Mix summed to 98 (19+52+17+10), but Assumptions said 97. Rent was earned on 98 units while opex, other income and reserves were charged on 97. The listing itself is inconsistent: LoopNet's headline says 97, while the unit-type breakdown in both listings sums to 98. Assumptions "Units" is now a formula pointing to the Unit Mix total, so there's one source of truth. It's flagged as a rent-roll diligence item.
2. **Hardcoded IO period in Scenario B.** The Debt tab used a typed `2` instead of the Assumptions IO-period cell. That's fixed. Values didn't change, since the input is also 2.
3. **Hold period presented as an input.** The model is structurally a 5-year build, so that cell is now black and labeled "structural, not a live input."
4. **Added explicit Market GPR and Loss-to-Lease lines** to the Operating Model, as requested for verification.
5. **Summary Bid Price values blanked.** They were solved on 97 units and will be re-solved in Step 4.

No problems were found in the script this time. `verify_from_assumptions.py` is retired because `verify_model.py` supersedes it.

### Current headline (98 units, verified)
Unlevered IRR 6.25% · Scen A levered 7.89% / 1.40x · Scen B levered 4.90% / 1.25x · LP IRR 9.82% / 1.51x · GP IRR −15.88%

### Open design question (not changed — your call)
Classic units renovated by us earn **market + $175/mo**. The 74 units the prior owner already renovated only trend **to** market. If "market" means a unit renovated to the existing standard, and our scope was defined to match that standard, then the $175 premium is double-counted. Setting the premium to $0 gives: Scen A levered 7.89% → 6.45%, LP 9.82% → 8.75%, unlevered 6.25% → 5.74%.

### What the verification does not prove
It shows the formulas implement the intended logic exactly. It does not validate the assumptions or the design choices themselves, since the same author wrote both implementations. That's what Step 6 is for.
