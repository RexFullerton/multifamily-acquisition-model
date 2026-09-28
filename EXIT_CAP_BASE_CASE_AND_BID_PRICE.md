# Exit Cap Fix, Base Case Switch, Independent Verification, and Bid Price

Prepared 2026-09-28. Stop point per instruction — report before any further work.

---

## 1. Exit cap anchor — was wrong, now fixed

You were right to check. The exit cap was anchored to the 7.23% Year-1 forward figure, not the 6.56% true in-place cap. Fixed at the source (Returns tab): the "entry cap" cell that everything downstream reads now points to **Cap Rate #2 — In-Place, Day-0, reassessed tax, primary (cost-of-sale) method — 6.56%**, not Cap Rate #3.

| | Before (wrong) | After (fixed) |
|---|---|---|
| Entry cap anchor | 7.23% (Year-1 forward) | **6.56%** (Day-0 in-place, reassessed tax) |
| Exit cap (entry + 50bps) | 7.73% | **7.06%** |

A **lower** exit cap means a **higher** exit price (same forward NOI, capitalized at a smaller rate), so this fix is return-*positive*, on top of the base-case switch below. The fix also automatically propagated to Sensitivity Table 1 (Exit Cap × Rent Growth, which reads the same anchor cell) and Table 2's own internal entry-cap calculation (which I updated to use the Day-0 basis too, keeping its cash-flow projections on the Year-1-forward basis where they belong — those shouldn't change, only the cap-rate label feeding the exit formula).

---

## 2. Base case = Scenario A (assumed debt)

Waterfall, and the Summary tab's headline "Sources & Uses," "Key Metrics," and "Returns" sections now run on Scenario A. Scenario B is preserved as the labeled alternative in the "Debt Scenario Comparison" section (columns swapped so A is first).

This required adding an LP/GP equity split to the Returns (Assumed) tab (wasn't needed before, since only Scenario B fed the Waterfall) and repointing every Waterfall formula — available cash, both hurdle-balance starting values, both IRR/multiple denominators — from `Returns`/`Capital` to `Returns (Assumed)`.

**Combined effect of the exit-cap fix + base-case switch** on the headline numbers:

| | Old report (Scenario B, wrong exit cap) | Now (Scenario A, base case, fixed exit cap) |
|---|---|---|
| Levered IRR (deal) | 1.48% | **8.07%** |
| Levered EM (deal) | 1.07x | **1.41x** |
| LP IRR | 3.85% | **9.96%** — clears the 8% pref |
| LP EM | 1.19x | **1.51x** |
| GP IRR | undefined ($0) | **-14.62%** (GP gets some promote, still recovers only 45% of its capital) |

The deal looks a lot better once (a) you fix the debt-service bug from last round, (b) you anchor the exit cap correctly, and (c) you underwrite the cheaper assumed debt instead of generic new debt. It's also a good, concrete illustration of how much those two modeling errors were distorting the picture — worth remembering as a general lesson, not just a one-off fix. GP's negative IRR despite the deal-level numbers looking solid is a real, structural finding: Tier 1 (100% to LP) eats most of the early cash flow paying down LP's pref, and there isn't enough left in Tiers 2–3 to fully return GP's own $509,529 co-invest within 5 years — worth knowing before you use this waterfall structure as a template elsewhere.

---

## 3. Independent verification — genuinely from scratch this time

[`verify_from_assumptions.py`](verify_from_assumptions.py) (new, in the repo) shares **no code path** with `build_model.py`. It reads only Assumptions/Unit Mix input values (by scanning for label text, never a hardcoded row number), and rebuilds the entire mechanic independently: 10-year rent-track engine, NOI, Debt (Assumed) including the maturity-triggered refinance, the tax-adjusted exit, cash flows, and the hurdle-balance waterfall for both LP and GP.

This is the right design specifically because it can't share the Section-0 bug from last round — that bug lived in *how the Excel formulas were wired* (a row-pointer error), and a script that never reads the model's own formulas, only its input values, can't inherit a wiring mistake. It found two real bugs of its own on the first two runs (a unit-mix double-counting issue from accidentally reading the Renovation Capex table's rows too, and a couple of column-offset mistakes in its own comparison logic) — both are in the script's own scaffolding, not the model, and both are fixed and disclosed in the script's comments.

**Result: every one of 19 compared figures matches the workbook exactly** — Years 1–5 NOI, all 5 years of Scenario A's levered cash flow, Day-0 in-place NOI, exit price, Scenario A's levered IRR and equity multiple, and LP/GP IRR and equity multiples. Full output:

```
Year 1-5 NOI: all OK
Year 1-5 Waterfall Available Cash (Scenario A levered CF): all OK
Day-0 In-Place NOI: OK
Exit Price: OK
Scenario A Levered IRR: OK  |  Scenario A Levered EM: OK
LP IRR: OK  |  LP Equity Multiple: OK
GP IRR: OK  |  GP Equity Multiple: OK

RESULT: ALL CHECKS MATCH. Independent from-assumptions rebuild ties to the workbook.
```

Run it yourself: `python3 verify_from_assumptions.py Parkview_Crossing_Acquisition_Model.xlsx`

---

## 4. Bid price — maximum purchase price by target return

[`price_solve.py`](price_solve.py) (new, in the repo) reuses the same verified engine, parameterized on price, and solves each target with `scipy.optimize.brentq`. **This is not a live Excel formula** — true goal-seek isn't expressible as static formulas without a circular/iterative solver, and I didn't want to fake that with a misleading "live-looking" cell. The Summary tab's new "Bid Price" section reports the solved values with a clear note that they come from this script, not a formula chain — re-run it whenever you change an assumption.

One structural point worth understanding before the numbers: **the assumed debt balance ($9,450,000) is fixed** — it doesn't resize with price, because you're assuming an *existing* loan, not sizing new debt against a new price. Only the Year-3 refinance loan is price-sensitive. That means as price drops, equity shrinks roughly 1:1 (minus the closing-cost scaling), which is *why* returns are so price-sensitive here — there's no offsetting debt paydown effect the way there would be with freshly-sized LTV-based debt.

| Target | Max Price | vs. $13.8M Asking | Implied In-Place Cap | Deal IRR / LP IRR |
|---|---|---|---|---|
| **LP clears 8% pref** (LP IRR ≥ 8%) | **$15,471,922** | **+12.1%** | 5.67% | 5.34% / 8.00% |
| **Levered IRR (deal) ≥ 12%** | **$12,294,971** | **-10.9%** | 7.57% | 12.00% / 12.63% |
| **Levered IRR (deal) ≥ 15%** | **$11,552,192** | **-16.3%** | 8.16% | 15.00% / 14.31% |

**All three targets are reachable** — none hits the structural floor (~$8.78M, below which the assumed $9.45M loan would exceed Total Uses and the "assume the existing loan" framing stops making sense).

The LP-pref target coming in **above** the asking price is the headline finding here: at $13.8M, Scenario A already clears the 8% pref comfortably (9.96% LP IRR from Section 2), so the price could rise ~12% before LP stops clearing pref. The 12%/15% deal-IRR targets, by contrast, both require **discounts** to asking (11% and 16% respectively) — meaning the current $13.8M price already sits between "generates a promote-worthy return for a value-add buyer" (would need ~$12.3M or lower for a clean 12% deal IRR) and "merely clears the LP's minimum" (up to $15.5M). Where you'd actually want to bid depends on what return you're underwriting to, which isn't something I'm deciding for you.

---

## 5. Verification

- **Formula errors: 0** (full workbook).
- **CHECKS tab: all pass**, including the Section-0 fix carried forward and unaffected.
- **Independent from-assumptions script: all 19 compared figures match** (Section 3 above).
- **Price-solve sanity check**: `compute(base_price)` reproduces the workbook's actual base-case deal IRR (8.0727%) and LP IRR (9.9554%) exactly before any solving happens — confirms the price-solve engine is wired to the same mechanics, not a simplified stand-in.

Committed and pushed. Stopping here per your instruction.
