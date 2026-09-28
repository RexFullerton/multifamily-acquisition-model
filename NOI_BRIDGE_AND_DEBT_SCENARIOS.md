# NOI Bridge, Assumable Debt Scenario, and a Correction

Prepared 2026-09-28. Stop point per instruction — report before any further work.

**Read this first: while building item 2, I found and fixed a real bug that materially changes the headline numbers from the Phase 3 report.** Section 0 covers that. Sections 1–3 answer your three numbered items.

---

## 0. A correction — Scenario B's debt service was understated by one year

Building the assumable-debt comparison required tracing the Debt tab's amortization schedule row-by-row, which surfaced a bug: the `amort_start` row pointer was set **before** the "Annual P&I Payment" label row was written, one row too early. Every downstream reference that computed `amort_start + i` to walk Years 1–5 was therefore off by one — it read the P&I-payment label row (blank in the debt-service column) as "Year 1," and Year 1's real data as "Year 2," and so on through the schedule.

**Practical effect: Scenario B's Year-1 debt service was computed as $0 instead of $636,870.** Because the loan is interest-only in Years 1–2 (same payment both years) and the amortizing years all carry an identical level payment by construction, the shift was invisible everywhere except Year 1 — which is exactly why it survived the Phase 3 checks. The wiring-consistency checks (e.g., "Levered CF independently rebuilt from Operating + Debt tabs") passed because the check's own reconstruction used the *same* mis-pointed `amort_start`, so it agreed with the equally-wrong Returns tab value. Two paths sharing one root bug will always agree with each other — that's a real blind spot in that style of check, and I want to be direct about it rather than let "checks passed" imply more than it does.

Fixed by moving the `amort_start` assignment to after the P&I-payment row is written. Rebuilt, recalculated, re-verified — see Section 4.

| Metric (Scenario B, new debt) | Phase 3 report (buggy) | Corrected |
|---|---|---|
| Levered IRR | 4.50% | **1.48%** |
| Levered Equity Multiple | 1.20x | **1.07x** |
| LP IRR | 7.22% | **3.85%** |
| LP Equity Multiple | 1.34x | **1.19x** |
| Unlevered IRR / EM | 5.03% / 1.24x | unchanged (no debt involved) |

Unlevered figures, the NOI build, the tax mechanics, and Scenario A's build (added fresh this round, never had the bug) are all unaffected. This makes the deal's negative-leverage story even more pronounced than I reported last time, not less — the corrected numbers strengthen, not undercut, the "weak returns" finding from Phase 3.

---

## 1. NOI reconciliation — the bridge

You were right that something didn't add up. Here's why, worked through with the live model rather than guessed at.

### The mechanical answer

**"Year 1" in the Operating Model was never a true in-place figure — it already includes a partial year of the business plan's own value creation.** Specifically:

- The "market rent" ceiling used inside Year 1's formulas is grown by 1.0% before anything else happens (`Base Market Rent × (1 + Year-1 growth)`).
- The **loss-to-lease burn-off** mechanic (55% turnover × 50% burn-off) fires for a full year on the 73 already-renovated units, moving them toward that grown market rent.
- The **renovation-premium capture** mechanic credits the 24 classic units with 50% of a full year's renovated rent (market + $175/mo premium), reflecting the 6-month renovation program.

None of this is wrong as a *forward* projection — it's what the Operating Model is supposed to do. The error was in Phase 3's language: I called the result the "going-in cap rate," which conventionally means Day-1 in-place, not "Year 1 after we've already started executing."

I verified this by building the true Day-0 calculation live in the workbook (Returns tab, new "NOI Bridge" section) directly from Unit Mix's raw in-place rents — no growth, no burn-off, no renovation credit — and then isolating each effect with its own counterfactual formula (also live, not hand math):

| Step | NOI | Cap rate | What changed |
|---|---|---|---|
| **Day-0 In-Place** (reassessed tax) | $905,244 | **6.56%** | Raw in-place rents, Unit Mix F/G columns, zero growth/burn-off/capture |
| + Loss-to-lease burn-off effect | +$27,853 | → 6.76% | 73 prior-renovated units, 1 year of 55%×50% burn-off toward Year-1 market rent |
| + Renovation-premium capture effect | +$64,587 | → 7.23% | 24 classic units, 50% Year-1 capture of (market + $175/mo) |
| = **Year-1 Forward NOI** | $997,684 | 7.23% | Ties out exactly to the Operating Model's own Year-1 column |

One clean, incidental finding from isolating these: **market rent growth has zero effect on Year-1 GPR by itself.** With burn-off and capture both switched off, changing the growth assumption from 0% to 1% didn't move Day-0 NOI at all — growth only enters Year 1 *through* the burn-off and capture mechanisms (it changes the target those two chase), never directly. So to directly answer your question: **yes, loss-to-lease burn-off and renovation-premium capture both leak into what I'd been calling "Year 1" — about $92,440 combined, ~10% of true in-place NOI. Growth doesn't leak in on its own; it only matters as an input to those two.**

### The three-way cap rate

| # | Basis | Cap Rate | Notes |
|---|---|---|---|
| 1 | **Broker-stated** | 7.00% | LoopNet-advertised, seller's current (lower) tax basis |
| 2 | **In-place, Day-0, reassessed tax** | **6.56%** | The true going-in number — my own bottom-up rent roll, buyer's reassessed property tax |
| 3 | **Year-1 forward** | 7.23% | Includes ~10 months average of business-plan execution — not a going-in number |

Cap rate #2 (6.56%) is now **below** the broker's 7.00%, which is what you'd expect once you reassess taxes upward — consistent with Phase 1's original manual estimate (6.80%, using the broker's own NOI as the starting point rather than my independently-built rent roll). The two don't match exactly because they start from different revenue bases — see below — but they now point the same direction, which they hadn't before.

### Where the broker gap actually comes from — and what I can't fully verify

I built a second check: take my Day-0 NOI ($905,244, my tax) and swap in the *seller's* tax basis instead (undoing my reassessment) to compare like-for-like against the broker's $966,000. That gives **$933,243** — about **$32,757 (3.4%) below** the broker's number.

I can't decompose that $32,757 further, and I want to be honest about why: it's the gap between my own bottom-up rent-roll-and-expense build and whatever's inside the broker's unseen T-12. I don't have their P&L, only their headline cap rate and NOI. What I can tell you:

- **It's a small, plausible gap**, not a red flag — could be marketing rounding, a slightly different other-income assumption, minor differences in one or two opex lines. It is *not* evidence that my model is inflating revenue; if anything my own build comes in slightly more conservative than the broker's marketed figure on a same-tax-basis comparison.
- **On the expense side specifically**, nothing in my build is obviously under-market: insurance ($2,400/unit) is already set above the general $2,000/unit South Florida average, and repairs & maintenance was deliberately nudged up for the 1958 vintage. If anything my opex assumptions skew conservative (higher), not low — so a too-low-opex explanation for the broker gap seems unlikely, though I can't rule it out without their actual T-12.

This is now a live, auditable section of the workbook (Returns tab), not just prose — click into it and every step is a formula, cross-checked with a new CHECKS-tab row confirming the bridge sums to exactly the Operating Model's own Year-1 NOI.

---

## 2. Assumable debt

### What's actually disclosed, with sources

| Term | First Mortgage | Supplemental Loan |
|---|---|---|
| Balance | $5,887,000 (Crexi) / $5,908,933.50 (LoopNet) | $3,563,000 (both) |
| Rate | 3.00% fixed | 6.20% |
| Maturity | December 2029 | Not disclosed |
| Blended rate | **4.2%** (broker-stated; the math checks: (5.887M×3.0% + 3.563M×6.2%)/9.45M = 4.205%) | |
| Amortization / IO status | **Not disclosed for either loan** | |
| Assumption fee / conditions | **Not disclosed** | |
| Type | "Non-Agency" (Crexi) — a balance-sheet or private loan, not Fannie/Freddie | |

Sources: [LoopNet listing](https://www.loopnet.com/Listing/901-951-NW-8th-Ave-Pompano-Beach-FL/35917237/), [Crexi listing](https://www.crexi.com/properties/1932017/florida-parkview-crossing). The broker also claims "almost 10% cash-on-cash return Day 1" from this structure — I didn't try to reverse-engineer their underlying NOI to verify that figure exactly, but Scenario A's modeled Year-1 cash-on-cash (11.2%, see below) lands in the same neighborhood, which is a reasonable sanity check.

The small balance discrepancy between LoopNet ($5,908,933.50) and Crexi ($5,887,000) is most likely two different as-of dates on the same amortizing loan. I used Crexi's figure since it's presented alongside the explicit blended-rate confirmation.

**Where I had to propose judgment values, clearly labeled in the workbook (Assumptions tab):**

- **IO status**: assumed both loans are interest-only through the first mortgage's December 2029 maturity. Not disclosed for either loan — this is a judgment call, chosen because IO is a common structure for non-agency assumable loans marketed on a cash-flow basis, and it's roughly consistent with the broker's "almost 10%" cash-on-cash claim (amortizing debt would pull that down). A toggle cell (`Assumptions!assum_io`) lets you flip it off.
- **Assumption fee**: 0.5% of the assumed balance ($47,250). Not disclosed. 0.5–1.0% is a commonly cited range for CMBS/balance-sheet loan assumption fees; I used the low end. Lender consent/underwriting timing (typically 30–60 days) isn't separately costed.
- **Supplemental loan maturity**: not disclosed; I treated it as coterminous with the first mortgage (Dec 2029) since that's the more common structure for a second lien layered onto an assumable first.

### How the scenario is built

Both loans run interest-only for Years 1–3 (Dec 2029 maturity falls in model Year 3, assuming a 2027 close). At the end of Year 3, the combined $9,450,000 balance is paid off and refinanced into new debt sized on Scenario B's own terms (MIN of LTV/DSCR/debt-yield — LTV binds again, at $8,970,000). **Because the new loan is smaller than the payoff, refinancing requires an extra $480,000 of cash at that point** — I added this explicitly as a Year-3 cash outflow in Scenario A's returns (it wasn't there in my first draft; caught it while reviewing the numbers, fixed before this report). The refi loan then runs interest-only for its own 2-year window, which happens to cover both remaining hold years (4 and 5), so it never starts amortizing within the hold.

Everything here is dynamic on `Assumptions!assum_first_maturity_yr` — change that cell and the whole schedule (which years are pre/post-refi) recalculates, it's not hardcoded to Year 3.

### Returns, side by side (both corrected for the Section 0 bug)

| | B: New Debt (generic) | A: Assumed Debt |
|---|---|---|
| Year-0 loan amount | $8,970,000 | $9,450,000 |
| Rate | 7.10% floating | 4.21% blended (fixed, Years 1–3) |
| Sponsor equity required | $5,528,040 | $5,095,290 |
| Levered IRR | **1.48%** | **4.37%** |
| Levered Equity Multiple | 1.07x | 1.20x |
| Year-1 Cash-on-Cash | 6.0% | 11.2% |

**Scenario A (assumed debt) clearly outperforms** — which is exactly what you'd expect once Scenario B's debt-service bug is fixed and both are compared fairly. The gap isn't as large as the 4.2%-vs-7.1% rate spread alone would suggest, because Scenario A pays for its cheap early-year financing with a $480,000 cash call at refinance and gets no amortization credit on the post-refi loan (it stays in IO through the rest of the hold). But it's still the better of the two as modeled. Neither is set as the base case, per your instruction — that's your call.

---

## 3. Verification

Recalculated the full workbook (LibreOffice headless), full re-scan, full re-check, per your instruction.

- **Formula errors: 0** (full workbook, both existing and new tabs).
- **CHECKS tab: all pass**, including two new checks added this round — the NOI bridge ties out exactly to the Operating Model's Year-1 NOI, and Debt (Assumed)'s post-refi sub-loan schedule reconciles independently.
- **Independent Python (numpy_financial) IRR/EM recomputation**, both scenarios:

| | Excel | Python | Match? |
|---|---|---|---|
| Scenario B Unlevered IRR | 5.0258% | 5.0258% | ✅ |
| Scenario B Levered IRR | 1.4842% | 1.4842% | ✅ |
| Scenario B Levered EM | 1.0699x | 1.0699x | ✅ |
| Scenario B LP IRR | 3.8534% | 3.8534% | ✅ |
| Scenario A Levered IRR | 4.3695% | 4.3695% | ✅ |
| Scenario A Levered EM | 1.2035x | 1.2035x | ✅ |

All match to displayed precision.

Updated workbook and this report are committed and pushed. I have not re-run the Phase 3 stress test (0% growth / +100bps exit cap) under the corrected debt-service formulas — that wasn't asked for this round, but flagging that the stress-test numbers in `PHASE3_VERIFICATION.md` are now stale (they inherited the same bug) if you want them redone.

Stopping here per your instruction.
