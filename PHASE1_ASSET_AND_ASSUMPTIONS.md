# Phase 1 — Asset Selection and Assumption Set

Status: **DRAFT FOR REVIEW, REV. 3.** Nothing in this document has been approved. No model has been built.
Prepared: 2026-09-21 · Revised: 2026-09-21 (rev. 2: subject switched to Parkview Crossing) · Revised again: 2026-09-21 (rev. 3: thesis reframed, sourcing tightened, tax mechanics deepened, roof/recert scenario added)

---

## 0. Thesis correction (read this first)

**With 75% of units already renovated, this is a light value-add / core-plus deal, not a heavy value-add deal.** Rev. 1 and rev. 2 both used "value-add" language that implied a full repositioning — that's wrong for this asset, and I should have caught it sooner given I had the 75%-renovated fact in hand since rev. 2. The prior owner has already executed the heavy lift (electrical, mini-split AC, windows, kitchens on 73 of 97 units). What's left for a new buyer is:

1. **Finishing the remaining ~24 classic units** (a small, low-risk capital program — see Section 2).
2. **Loss-to-lease burn-off** on units already renovated but still priced below market (the disclosed 20.76% blended upside suggests this exists even among the renovated units).
3. **Market rent growth** over the hold.
4. **Expense management** — this is genuinely a lever here given the flagged insurance and tax exposure below, not just a filler category.

This reframing is now reflected in `README.md`. **Which of these four actually drives the most value is a Phase 2 question — it requires the built model to decompose, and I'll report it once Phase 2 runs.** I won't guess at it here.

---

## 1. Subject property: Parkview Crossing

**901–951 NW 8th Ave, Pompano Beach, FL 33060 (Broward County)** — listed by Franklin Street (Dan Dratch, Ryan Wold, Alex Gerdak), active on both [LoopNet](https://www.loopnet.com/Listing/901-951-NW-8th-Ave-Pompano-Beach-FL/35917237/) and [Crexi](https://www.crexi.com/properties/1932017/florida-parkview-crossing). Listed 6/30/2026, last updated 9/8/2026.

| Fact | Value | Source |
|---|---|---|
| Units | 97 (LoopNet) / 98 (Crexi marketing text) — 7 buildings: 19 studios, 52 1BR/1BA, 17 2BR/1BA, 10 2BR/2BA | LoopNet, Crexi |
| Year built | 1958, reinforced concrete block, painted stucco | LoopNet, Crexi |
| Building size | 46,960–46,962 SF (7 buildings), 2.39 acres, 2 stories | LoopNet |
| Class / style | Class C, Garden | LoopNet |
| Occupancy | 92% average | LoopNet |
| **Asking price (broker-stated)** | **$13,800,000** ($142,268/unit per LoopNet; $140,816/unit per Crexi, using 98 units) | LoopNet, Crexi |
| **Cap rate (broker-stated)** | **7.0%** | [LoopNet](https://www.loopnet.com/Listing/901-951-NW-8th-Ave-Pompano-Beach-FL/35917237/) |
| Existing debt | Assumable first: ~$5.89–5.91M at 3.0% fixed through Dec 2029 (LoopNet/Crexi differ slightly on balance); plus a supplemental loan of $3,563,000 at 6.20%; broker states a blended 4.2% rate and "almost 10% cash-on-cash return Day 1" | LoopNet, Crexi |
| Capital improvements to date | $1M+ invested: electrical supply lines/panels/breakers (all units), gated 6-ft steel fencing, repaved parking, LED common-area lighting, security/surveillance system, landscaping | LoopNet, Crexi |
| Unit-level renovation status | **75% of units already renovated** (upgraded kitchens, new mini-split AC, vinyl slider windows, modern lighting) — implies **~24 classic (unrenovated) units remain** | LoopNet, Crexi |
| Disclosed upside | "Opportunity to increase rents by 20.76%" | [Crexi](https://www.crexi.com/properties/1932017/florida-parkview-crossing), investment highlights |
| Recertification | "Passed 40 & 50 Year Recertification" | LoopNet, Crexi — **caveated in Section 3**, treat as unverified |
| Opportunity Zone | Yes | LoopNet |
| Current tax assessment | Improvements $9,695,170 + Land $623,530 = **$10,318,700 total** | LoopNet |
| Zoning | RM-20 | LoopNet |

### Sourcing correction from rev. 2

**I previously used a figure I pulled from Crexi's ungated "Valuation Calculator" widget (which auto-populated a $931,227 NOI / 6.75% cap) as if it were a more precise, more reliable number than the broker's advertised 7.0%.** Per your instruction, I've dropped that. It's a calculator's computed output, not a disclosed fact, and I have no way to confirm what fed it. **The only broker-stated figures I'm using going forward are LoopNet's advertised $13,800,000 price and 7.0% cap rate, both directly linked above.** Everything downstream (the reassessed cap rate work in particular) now starts from that single broker-stated number: **implied broker NOI = $13,800,000 × 7.0% = $966,000.**

I have not seen the actual T-12 or OM — that's gated behind Franklin Street's "Request Info" / NDA flow. If you request it and sign an NDA, per your note the repo stays private, so there's no conflict with putting real figures from it into this file later.

### Going-in cap rate: broker-stated vs. reassessed-tax basis

The broker's $966,000 NOI almost certainly reflects the **seller's current (lower) property tax bill**, not what a buyer actually pays after Florida reassesses the parcel on sale. I can't confirm this directly (it's inside the gated T-12), but it's standard industry practice to underwrite off in-place actuals. Here's the reconstruction, redone properly per your instruction on the reassessment method (see Section 3 for the full statutory research):

| | Reassessed Just Value | Incremental tax vs. seller's current $204,717/yr | Reassessed NOI | Reassessed cap rate |
|---|---|---|---|---|
| **Broker-stated (no reassessment)** | — | — | $966,000 | **7.00%** |
| **Statutory/DOR method** (full purchase price less the DOR's customary 15% cost-of-sale allowance under Fla. Stat. §193.011(8)) — **primary case** | $13,800,000 × 0.85 = $11,730,000 | +$27,999 | $938,001 | **6.80%** |
| **Full-purchase-price reassessment — conservative case** | $13,800,000 | +$69,067 | $896,933 | **6.50%** |

(Millage and current-tax figures sourced and explained in Section 3.)

**I'm using 6.80% (the statutory/DOR method) as the primary going-in cap rate for the rest of this document**, since Fla. Stat. §193.011(8) case law and Florida Department of Revenue sales-ratio-study practice specifically contemplate deducting usual costs of sale from a transaction price when using it as evidence of just value — this isn't a made-up haircut, it's grounded in how assessors are actually instructed to treat sale prices. The full-price 6.50% stays in as the conservative sensitivity case, per your instruction.

### 1958 vintage: roof, insurance, and Broward recertification

**Roof.** Still not disclosed anywhere in the public listing data. The detailed $1M+ capital-improvements list conspicuously omits the roof. **Treated as an unresolved diligence item — see the roof-replacement scenario in Section 2, not assumed away.**

**Insurance.** Same two-part sourcing as rev. 2: Florida SB 2-D's roof-age protections are a homeowners'-insurance (personal-lines) statute, not something I can confirm binds commercial multifamily blanket policies the same way — but 4-point-inspection practice and roof-age underwriting scrutiny are commonly extrapolated into the commercial market. **This is judgment/extrapolation, not a confirmed commercial-market rule**, flagged the same as rev. 2.

**Broward 40/50-Year Recertification.** Same sourced mechanic as rev. 2: initial inspection at 40 years, then every 10 years. Building age 68 in 2026 → cycle would be 40 (1998), 50 (2008), 60 (2018), **next due ~2028**. The listing's "passed 40 & 50 year recertification" language remains ambiguous — it may mean "compliant with the county's 40/50-Year Program" generically, or it may literally mean only the 1998/2008 exams are on file. **Still unresolved from public data — confirm directly with Broward County / Pompano Beach Building Services before relying on it.** Given your instruction this round, I've now built a specific capital-plan response instead of a vague annual reserve — see Section 2.

### Market and exit-cap comps (unchanged)

| Property | Units | Built | County | Status | Price | $/Unit |
|---|---|---|---|---|---|---|
| [Cascades at the Hammocks](https://therealdeal.com/miami/2026/05/06/south-florida-top-real-estate-deals-may-5-2026/), Kendall | 264 | 1988 | Miami-Dade | Sold May 2026 | $65.5M | $248,100 |
| [Savona Grand](https://therealdeal.com/miami/2026/08/10/south-florida-top-real-estate-deals-august-7-2026/), Lake Worth | 214 | 2003 | Palm Beach | Sold Aug 2026 | $64.8M | $302,804 |

---

## 2. Full assumption set (revised)

Legend: **Source** = a live link or named report, cited as broker-stated/third-party-stated where relevant. **Judgment** = my estimate, with reasoning and a range.

### Acquisition

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Purchase price | $13,800,000 ($142,268/unit) | **Broker-stated** — [LoopNet](https://www.loopnet.com/Listing/901-951-NW-8th-Ave-Pompano-Beach-FL/35917237/) asking price. | — |
| Going-in cap rate — broker-stated | 7.00% | **Broker-stated**, LoopNet. | — |
| Going-in cap rate — reassessed (primary, statutory method) | **6.80%** | **Derived**, see Section 1 and Section 3. | 6.50%–6.80% |
| Closing costs | 1.5% of purchase price | **Judgment**, Broward-specific: doc stamps at $0.70/$100 (0.70%, Fla. Stat. §201.02 — Broward, not Miami-Dade's discounted rate) plus title, legal, third-party reports (PCA, Phase I ESA, appraisal, and now a roof inspection given the flagged vintage issue). | 1.25%–2.0% |

### Unit mix and rents (97 units)

| Unit type | Count | Renovated? (proportional est.) | Avg SF | Est. in-place rent | Est. market (stabilized) rent |
|---|---|---|---|---|---|
| Studio | 19 | ≈14 reno / 5 classic | 540–750 | $1,275/mo | $1,550/mo |
| 1BR/1BA | 52 | ≈39 reno / 13 classic | 600–770 | $1,475/mo | $1,780/mo |
| 2BR/1BA | 17 | ≈13 reno / 4 classic | 700–780 | $1,700/mo | $2,050/mo |
| 2BR/2BA | 10 | ≈7 reno / 3 classic | 700–780 | $1,825/mo | $2,200/mo |

Unchanged methodology from rev. 2: solved to match the disclosed **20.76% blended upside** (Crexi investment highlights — this is a broker-stated marketing claim, not audited, but it's the one real anchor available), using apartments.com's Pompano Beach 33060 submarket averages ($1,771 for 1BR, $2,319 for 2BR) as an upper-bound reference, discounted down because that submarket average includes newer/better stock. Studio and 2BR/1BA rows are proportionally extrapolated — **still the weakest-sourced row in this document.** The 75/25 reno split by unit type is my own proportional allocation, not disclosed at the unit-type level.

### Renovation program — bottom-up scope, full 8 lines (per your request)

**Scope logic unchanged:** matches the disclosed standard already applied to 75% of units (kitchen, mini-split AC, vinyl slider windows, modern lighting), plus standard ancillary items.

| # | Line item | Cost/unit | Basis |
|---|---|---|---|
| 1 | Kitchen (cabinet refacing + hardware, laminate/quartz counter, sink/faucet, 4-piece stainless appliance package) | $7,000 | **Judgment**, mid-low end of $4,500–15,000 kitchen cost research; picked lower-mid given "upgraded kitchens" reads as a refresh, not a gut, at this Class C price point. |
| 2 | Mini-split ductless AC system (1–2 zone) | $3,500 | **Judgment**, general HVAC mini-split market pricing, no South Florida-specific source. |
| 3 | Vinyl slider window replacement (~3 openings/unit) | $1,500 | **Judgment**, no specific source. |
| 4 | Modern lighting fixtures + ceiling fans | $400 | **Judgment**. |
| 5 | LVP flooring (~700 SF avg unit) | $4,000 | **Judgment**, $5.50–$11.50/SF installed LVP range; used ~$5.75/SF. |
| 6 | Bathroom refresh (vanity, fixtures, re-caulk, spot tile repair) | $1,200 | **Judgment**, kept light vs. the $5,000–12,000 full-remodel range since baths aren't mentioned in the OM's disclosed scope. |
| 7 | Interior paint | $500 | **Judgment**. |
| 8 | Turnover labor / punch / make-ready cleaning | $500 | **Judgment**. |
| | **Subtotal** | **$18,600** | |
| | Contingency (10%) | $1,860 | **Judgment**, standard convention. |
| | **Total per classic unit** | **$20,460** | |

**Total renovation program: ~24 units × $20,460 ≈ $491,000.** Units renovated per month: 4/unit (≈6-month program) — **judgment**.

**Please confirm or edit before Phase 2** — same two open questions as rev. 2: (a) is matching the existing standard the right call, and (b) is the light bathroom line ($1,200) realistic.

### Renovation return — both metrics you asked for

Renovated rent premium: $175/mo judgment (base case within a $100–250/mo range from Southeast Class B/C industry commentary) = **$2,100/year per unit**.

| Metric | Formula | Result |
|---|---|---|
| **Yield-on-cost** (cash-flow basis) | Annual premium ÷ cost per unit | $2,100 ÷ $20,460 = **10.3%** |
| **Value created at exit** (capitalized basis) | Annual premium ÷ exit cap rate | Primary case (7.30% exit, see Section on exit below): $2,100 ÷ 0.073 = **$28,767/unit** |
| **Value-created-to-cost multiple** | Value created ÷ cost per unit | $28,767 ÷ $20,460 = **1.41x** (renovation creates ~41% more value than it costs, on a capitalized basis) |

**Reframed conclusion given the thesis correction (Section 0):** 10.3% yield-on-cost is soft against the ~15–20% threshold typically cited for a *heavy* value-add program — but that threshold is calibrated for deals where renovation carries the whole thesis. Here, renovation is a small, low-risk sliver (24 of 97 units) inside a light value-add/core-plus deal, and the capitalized value-creation math (1.41x cost) is genuinely attractive. I'd frame this as: the renovation isn't the reason to do this deal, but it isn't value-destructive either — it pencils on a capitalized basis even though the standalone cash yield is unremarkable. At the +100bps exit-cap sensitivity ceiling (7.80%), value created falls to $2,100 ÷ 0.078 = $26,923/unit, a 1.32x multiple — still above cost.

### Roof replacement scenario (new, per your instruction)

| Item | Value | Basis |
|---|---|---|
| Estimated roof area | ~23,480 SF | **Judgment/derived** — half of the disclosed 46,960 SF total building area, assuming uniform 2-story floor plates across the 7 buildings (a reasonable but unconfirmed assumption for flat/low-slope garden-apartment roofs). |
| Replacement cost (TPO/modified bitumen, hurricane-code fastening) | $8–$12/SF installed → **$188,000–$282,000 total** (~$1,940–$2,900/unit) | **Judgment**, 2026 commercial flat-roof cost research; South Florida hurricane-code roof-deck attachment requirements likely push toward the higher end of the general national range, which I've reflected by leaning toward the top of the cited $4–15/SF national range rather than the middle. |
| Insurance impact if replaced | Insurance could fall from the vintage-risk-adjusted $2,400/unit (below) to **~$1,900/unit** — potentially *below* even the generic $2,000/unit South Florida average | **Judgment.** A new roof would plausibly qualify for wind-mitigation credits (roof covering, deck attachment, roof-to-wall connection) regardless of the building's 1958 origin — wind-mit credits are tied to roof/structural characteristics, not just year built, per the general FL wind-mitigation research cited in rev. 2. This is a real, sourced *mechanism*, but the specific $1,900/unit outcome is my own estimate, not a quote. |

**This is a scenario, not a base-case assumption** — I have not added the $188k–$282k roof cost to the base capital plan, since roof condition is unconfirmed. If diligence reveals the roof needs replacement, swap this line in; if it reveals a recently-replaced roof, the vintage-risk insurance markup below should probably come back down toward the generic $2,000/unit average instead.

### Recertification: specific year, not a flat reserve (revised per your instruction)

Replacing rev. 2's flat $750/unit/year ongoing reserve with a dated, specific capital event:

| Item | Year | Value | Basis |
|---|---|---|---|
| Next recertification inspection (structural + electrical engineering report) | **2028** | ~$10,000 (one-time) | **Judgment** — no sourced fee found for a report of this size; a placeholder pending an actual engineering quote. |
| Remediation contingency | **2028** | $150,000 (one-time placeholder) | **Judgment — genuinely unknowable without the engineer's findings.** Range could run from near-zero (if the building passes cleanly) to well into six figures if structural or electrical remediation is required. |

**Both explicitly labeled diligence items**, per your instruction — not confident estimates. 2026 + a 5-year hold runs through 2031, so this recertification cycle falls inside Year 2–3 of the hold regardless of exact closing date.

### Operating assumptions

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Physical vacancy | 6.5% (vs. 92% disclosed occupancy) | **Sourced starting point** (92% occupancy, LoopNet), nudged for renovation downtime on the ~24 classic units. | 6%–9% during renovation |
| Credit loss / bad debt | 1.0% of GPR | **Judgment**, standard convention. | 0.5%–1.5% |
| Concessions | 0.5% of GPR | **Judgment**, standard convention. | 0%–1.5% |
| Other income (RUBS, pet, parking, admin fees) | $35/unit/month | **Judgment**, no South Florida-specific source found. | $25–$50/unit/mo |
| Expense growth (ex-insurance, ex-taxes) | 3.5%/year | **Judgment**, standard convention. | 3.0%–4.5% |

### Rent growth — Broward/Fort Lauderdale sourced, capped at 3.0% terminal (revised per your instruction)

**Replaced the Miami-Dade anchor from rev. 2 with Broward-specific data.** Three separate, non-double-counted mechanics, unchanged in structure from rev. 2:

**(1) Market rent growth:**

| Year | Market rent growth | Basis |
|---|---|---|
| 1 (2027) | 2.5% | **Sourced, with a deliberate haircut.** Broward County's own submarket data (MIAMI REALTORS®/RWorld South Florida Rental Market Report, May 2026 edition) shows **Pompano Beach-South rents up 8.3% YoY** — the single most directly relevant number available, since that's the subject's own submarket. But only 50% of Broward's 24 tracked submarkets rose at all that month (the other half fell), and an 8.3% single-submarket spike likely partly reflects *other* owners' own renovation-driven repositioning (the same dynamic we're underwriting here), not pure organic market growth. I've used 2.5% — well above a generic Broward-wide flat read, well below the submarket's own headline number — as a defensible middle path. Fort Lauderdale metro-wide context (Marcus & Millichap's 2026 forecast, cited via search summary — I could not load the primary report page directly, so treat this as secondary-sourced) put effective rent near $2,530/month and vacancy near 4.9–5.1%, consistent with a market that's positive but not booming. |
| 2 (2028) | 2.75% | **Judgment**, gradual convergence toward the capped terminal rate. |
| 3 (2029) | 3.0% | **Judgment**, reaches the terminal rate. |
| 4–10 | 3.0% (flat) | **Capped per your instruction** — I don't have a source strong enough to justify going higher for a multi-year terminal assumption; 3.0% is the ceiling. |

**(2) Loss-to-lease burn-off** — unchanged mechanic from rev. 2: applies only to not-yet-renovated units (both classic units before their turn, and any renovated units still below that year's market rent per the disclosed 20.76% gap). At each lease turnover, rent resets to `prior rent + 50% × (market rent − prior rent)`, capped at market rent. Turnover assumed ~55%/year — **general industry convention, not specifically sourced for this property.**

**(3) Renovation premium** — unchanged: one-time event, `new rent = that month's market rent + $175/mo`, grows with market rent thereafter, fires once per unit.

**No double-counting** — same check as rev. 2: market rent grows independently; burn-off moves a specific unit toward that grown market rent; renovation premium is a one-time add-on at the moment of renovation. Once renovated, burn-off no longer applies.

### Operating expenses (Year 1, $/unit/year unless noted)

| Line | Value | Source / Judgment |
|---|---|---|
| Payroll (on-site mgmt + maintenance) | $1,400/unit | **Judgment**. |
| Repairs & maintenance | $1,100/unit | **Judgment**, nudged up for 1958 vintage / undisclosed roof. |
| Turnover / make-ready | $350/unit | **Judgment**. |
| Contract services (landscaping, pest, trash) | $450/unit | **Judgment**. |
| Utilities (owner-paid common area/vacant units) | $500/unit | **Judgment**. |
| **Property insurance** | **$2,400/unit ($232,800 total)** | **Judgment**, adjusted upward from the general $2,000/unit South Florida average (multiple 2026 industry sources: ~$800/unit two years ago → ~$2,000/unit currently) given the undisclosed roof on a 68-year-old building. See the roof-replacement scenario above for how this could improve. |
| Insurance growth rate | 7%/year | **Judgment**, above the general 3.5% expense growth, reflecting the cited recent trend moderating somewhat going forward. |
| Property taxes | Modeled on the reassessed basis (Section 1/3), grown per Florida's non-homestead cap | See Sections 1 and 3. |
| Management fee | 3.5% of EGI | **Judgment**, standard convention. |
| G&A / admin | $250/unit | **Judgment**. |
| Marketing | $150/unit | **Judgment**. |
| Replacement reserves (below NOI) | $300/unit | **Judgment**, standard lender convention. |

(The generic $750/unit/year recertification reserve from rev. 2 is **removed** — replaced by the dated 2028 line items above, per your instruction.)

### Debt (unchanged from rev. 2)

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Index | 1-month SOFR, ~3.85% | **Sourced** — [sofrrate.com](https://www.sofrrate.com/), reading as of 9/18/2026. | — |
| Spread | +325 bps | **Judgment**, within the 200–500bps range cited for 2026 multifamily bridge/value-add financing. | +200 to +400 bps |
| LTV | 65% | **Judgment**, mid-point of the 65–75% range cited. | 60%–70% |
| Interest-only period | 24 months | **Judgment**. | 18–36 months |
| Amortization (post-IO) | 30 years | **Judgment**. | 25–30 years |
| Min. DSCR / debt yield constraint | 1.25x DSCR / 8.0% debt yield | **Judgment**, standard cited lender minimums; model shows which of LTV/DSCR/debt yield binds. | DSCR 1.20–1.30x; debt yield 7.5–9.0% |
| Refinance | Toggle — refi at stabilization or hold to exit | **Judgment**. | — |

**Noted, not modeled by default:** the real assumable loan (~$5.9M @ 3.0% fixed to Dec 2029, plus $3.563M supplemental at 6.20%, blended ~4.2%) is broker-stated and real. Kept out of the base case for genericity; flag if you want it as an alternative-financing toggle in Phase 2.

### Hold and exit — now with the tax-adjusted exit mechanic you asked for

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Hold period | 5 years | **Judgment**. | 3–7 years |
| Exit cap rate (statutory-basis entry 6.80% + 50bps) | **7.30%** (base case) | **Per your instruction** (entry+50bps), applied to the primary (statutory-method) entry cap. | Sensitivity to **+100bps = 7.80%** |
| Exit cap rate (conservative-basis entry 6.50% + 50bps) | 7.00% (alternative base case) | Same convention, applied to the conservative entry cap. | Sensitivity to +100bps = 7.50% |
| Cost of sale | 2.0% of exit price | **Judgment**, standard convention. | 1.5%–2.5% |

**Tax-adjusted exit valuation — new mechanic, per your instruction.** See `README.md` for the full plain-language explanation; the short version:

A future buyer at exit will *also* get reassessed to whatever price they pay, so their post-tax NOI depends on the price itself — a circular reference if solved naively. The closed-form solution:

```
Exit Price = Forward NOI (before property tax) / (Exit Cap Rate + Effective Tax Rate)
```

This works because if "Exit Cap Rate" is a normal post-tax cap rate (consistent with every other cap rate in this document), then the exit buyer's post-tax NOI is `NOI_pretax − (Effective Tax Rate × Price)`, and setting that over Price equal to the target Exit Cap Rate and solving for Price algebraically eliminates the circularity.

**Illustrative worked example (placeholder numbers — the real Year 5 figure comes from the Phase 2 model, not from this document):** if Year 5 forward NOI before property tax comes out to approximately $1,150,000, and effective tax rate is 1.98394% (Section 3), then at a 7.30% exit cap: Exit Price = $1,150,000 / (0.0730 + 0.0198394) = $1,150,000 / 0.0928 ≈ **$12,392,000**. I want to be explicit that $1,150,000 is a placeholder I picked to demonstrate the mechanic, not a modeled number — Phase 2 will replace it with the actual Year 5 output.

### Waterfall (unchanged from rev. 2)

| Assumption | Value | Source / Judgment |
|---|---|---|
| Preferred return | 8.0% | **Judgment**, standard convention. |
| Tier 1 | 100% LP / 0% GP until pref + capital returned | Standard structure |
| Tier 2 | 70/30 LP/GP up to 12% IRR | **Judgment**. |
| Tier 3 | 50/50 LP/GP above 12% IRR | **Judgment**. |
| GP co-invest | 10% of equity | **Judgment**. |

---

## 3. Florida-specific items (deepened this round)

### How Broward actually sets "just value" after a sale — researched per your instruction

Florida Statute **§193.011** lists eight factors a property appraiser must consider in deriving just value. The **eighth criterion, §193.011(8)**, specifically addresses sale price as evidence of value: it directs the appraiser to consider **"the net proceeds of the sale... after deduction of all of the usual and reasonable fees and costs of the sale"** — the Florida Supreme Court has construed "reasonable fees and costs of sale" to include attorney's fees, broker's commissions, appraisal fees, documentary stamp costs, survey costs, and title insurance costs. [Source: Fla. Stat. §193.011; case-law summary via propertytaxinflorida.com.]

**In practice:** the Florida Department of Revenue's own sales-ratio studies "generally assume a 15% adjustment for costs of sale" when using transaction prices as evidence of market value — though this is **discretionary, not mandatory**, and appraisers can use a different percentage if the facts support it. This means a straight "just value = purchase price" assumption is actually the more aggressive (higher-tax) case, not the standard one — **the statutory/customary approach nets the price down first.** I've used this 15% DOR-customary adjustment as the **primary** reassessment method in Section 1, per your instruction, with full-price reassessment kept as the labeled **conservative case**.

### Combined millage for this parcel's tax district

**I attempted a direct parcel lookup on the Broward County Property Appraiser's site (web.bcpa.net) to confirm this specific parcel's millage code and taxing-district assignment, and could not get a usable result** — the site's search returned an empty "Parcel Result" panel in my automated session (likely an SPA interaction I couldn't reproduce correctly, not a data-availability problem). I was not able to verify anything address-specific beyond what LoopNet already discloses (the $10,318,700 current assessment). **Falling back to Broward's countywide combined average of 19.8394 mills (1.98394%)** — sourced to JVM Lending's Broward County property tax guide, which describes this as the "average combined millage rate... includes county, school board, city, and special district levies," consistent with the separately-confirmed Broward countywide general-fund millage of 5.6658 mills as just one component of that total. **This is a county-average proxy, not a confirmed parcel-specific rate** — Pompano Beach could carry a CRA (Community Redevelopment Agency) district assessment or other special-district add-on I haven't ruled out. If you or the broker can get the actual TRIM notice or tax bill for this parcel, that should replace this proxy.

### Property tax reassessment — mechanic and Amendment 3 (unchanged)

Non-homestead 10% annual cap doesn't carry to a new owner; reassessed to market value the January following sale, then the cap (10% today, possibly 5% from 2027 if **Florida Amendment 3** passes on the Nov 3, 2026 ballot) resumes for the new owner. Amendment 3 status unchanged from rev. 2 — not modeled by default, flagged for your decision.

### Property insurance (unchanged sourcing from rev. 2)

Same sourcing and same honest caveat about SB 2-D being a homeowners'-insurance statute, not confirmed to bind commercial multifamily blanket policies the same way.

### Broward 40/50-Year Recertification (deepened — see Section 1 and Section 2)

Now includes a specific dated capital event (2028 inspection + remediation contingency) rather than a flat reserve, per your instruction.

### Live Local Act — excluded from the model, reframed for the corrected thesis

Findings unchanged (71-unit minimum, 40%+ affordable at ≤100% AMI for 30 years, 75–100% ad valorem exemption). **README.md updated** to frame the conflict correctly given the thesis correction in Section 0: Live Local would still conflict with this deal, but the conflict is now framed against a light value-add/core-plus rent-growth thesis, not a heavy repositioning thesis.

---

## 4. What I need from you before Phase 2

1. **Renovation scope approval** — same two open questions as rev. 2 (matching-standard assumption, light bathroom line).
2. **Roof replacement scenario** — this is a scenario, not baked into the base case. Decide whether to run Phase 2 with the base case ($2,400/unit insurance, no roof capex) or the roof-replacement scenario ($188k–282k capex, ~$1,900/unit insurance thereafter) as an alternate case.
3. **2028 recertification contingency** ($10k inspection + $150k remediation placeholder) — both are genuinely unconfirmed guesses. Real diligence (an actual conversation with Broward/Pompano Beach Building Services, or an engineer's assessment) should replace these before you'd want to defend them in an interview.
4. **Which entry/exit cap basis to carry as the headline** — I've defaulted to the statutory/DOR method (6.80% entry → 7.30% exit) as primary, full-price reassessment (6.50% → 7.00%) as the conservative case. Confirm that's the right emphasis.
5. **BCPA parcel lookup** — I could not get a parcel-specific millage/tax-district confirmation from Broward's own site. If you're able to pull the actual TRIM notice or tax bill (or have the broker provide it), that would meaningfully tighten Section 3.
6. **Assumable debt** — still an open question from rev. 2 on whether to model it as an alternative-financing toggle.

I have not built anything beyond this document. Nothing here is final.
