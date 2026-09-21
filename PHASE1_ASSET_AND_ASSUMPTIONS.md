# Phase 1 — Asset Selection and Assumption Set

Status: **DRAFT FOR REVIEW, REV. 2.** Nothing in this document has been approved. No model has been built.
Prepared: 2026-09-21 · Revised: 2026-09-21 (subject property switched to Parkview Crossing per review)

---

## 1. Subject property: Parkview Crossing

**901–951 NW 8th Ave, Pompano Beach, FL 33060 (Broward County)** — listed by Franklin Street (Dan Dratch, Ryan Wold, Alex Gerdak), active on both [LoopNet](https://www.loopnet.com/Listing/901-951-NW-8th-Ave-Pompano-Beach-FL/35917237/) and [Crexi](https://www.crexi.com/properties/1932017/florida-parkview-crossing). Listed 6/30/2026 (~490 days on market per Crexi, which appears to date from an earlier listing attempt), last updated 9/8/2026.

| Fact | Value | Source |
|---|---|---|
| Units | 97 (LoopNet) / 98 (Crexi, marketing text) — 7 buildings: 19 studios, 52 1BR/1BA, 17 2BR/1BA, 10 2BR/2BA | LoopNet, Crexi |
| Year built | 1958, reinforced concrete block, painted stucco | LoopNet, Crexi |
| Building size | 46,960–46,962 SF (7 buildings), 2.39 acres, 2 stories | LoopNet |
| Class / style | Class C, Garden | LoopNet |
| Occupancy | 92% average | LoopNet |
| Asking price | $13,800,000 ($142,268/unit per LoopNet; $140,816/unit per Crexi, using 98 units) | LoopNet, Crexi |
| Headline cap rate | 7.0% (LoopNet) | LoopNet |
| Existing debt | Assumable first: ~$5.89–5.91M at 3.0% fixed through Dec 2029 (LoopNet/Crexi differ slightly on balance, likely different as-of dates); plus a supplemental loan of $3,563,000 at 6.20%; broker states a blended 4.2% rate and "almost 10% cash-on-cash return Day 1" | LoopNet, Crexi |
| Capital improvements to date | $1M+ invested: electrical supply lines/panels/breakers (all units), gated 6-ft steel fencing, repaved parking, LED common-area lighting, security/surveillance system, landscaping | LoopNet, Crexi |
| Unit-level renovation status | **75% of units already renovated** (upgraded kitchens, new mini-split AC, vinyl slider windows, modern lighting) — implies **~24 classic (unrenovated) units remain** | LoopNet, Crexi |
| Disclosed upside | "Opportunity to increase rents by 20.76%" (Crexi investment highlights) | Crexi |
| Recertification | "Passed 40 & 50 Year Recertification" | LoopNet, Crexi — **see caveat in Section 3** |
| Opportunity Zone | Yes | LoopNet |
| Current tax assessment | Improvements $9,695,170 + Land $623,530 = **$10,318,700 total** | LoopNet |
| Zoning | RM-20 | LoopNet |

**A note on how I got the NOI, since neither portal displays it outright.** Crexi masks the "NOI," "Cap Rate," and "Occupancy" fields on the property-facts panel behind a login wall — but its own public, ungated "Valuation Calculator" widget on the same page **auto-populates with the listing's real data**. With no debt entered, it shows Annual Cash Flow (= NOI, since debt service is $0) of **$931,227** and a calculated cap rate of **6.75%** on the $13.8M price. That's inconsistent with LoopNet's headline "7.0%" — implying LoopNet is showing a rounded marketing number off a slightly different (~$966,000) NOI figure, while Crexi's calculator is pulling the more precise underlying figure. **I'm using $931,227 as the working broker NOI** because it's unrounded and appears to come directly from the listing data field rather than marketing copy, and I flag the $966k/7.0% figure as the rounded alternative. I could not access the actual T-12 or full OM (gated behind a "Request Info" / NDA flow) to verify this directly — treat both as broker-marketed numbers, not audited financials, until you request the OM.

### Broker cap rate vs. reassessed cap rate

The broker's NOI almost certainly reflects the **seller's current (lower) property tax bill**, not what a buyer would actually pay after Florida reassesses the property to the purchase price. This is standard industry practice — brokers underwrite off in-place/trailing actuals, not buyer-specific post-sale reassessment — but I can't confirm it directly since the tax line itself isn't broken out in what's public. Here's the reconstruction:

- Broward's 2025–26 combined millage (county + school board + city + special districts) averages **19.8394 mills = 1.98394%** of assessed value. [Source: JVM Lending's Broward County property tax guide, corroborating the commonly cited "~19.84 mills combined" figure and the separately-confirmed Broward countywide millage of 5.6658 mills as just the county-general-fund component of that total.]
- Seller's current assessed value: $10,318,700 (LoopNet, above) → current tax ≈ **$204,700/year**.
- Reassessed to the $13.8M purchase price: → new tax ≈ **$273,800/year**.
- **Incremental tax hit to a buyer: ≈ +$69,100/year.**

| | Broker's NOI basis | Reassessed-tax NOI |
|---|---|---|
| Using Crexi's precise $931,227 NOI | $931,227 → **6.75% cap** | $862,159 → **6.25% cap** |
| Using LoopNet's rounded $966,000 NOI | $966,000 → **7.00% cap** | $896,932 → **6.50% cap** |

**Bottom line: the real, tax-adjusted going-in cap rate on this deal is roughly 6.25–6.50%, not the 7.0% headline number.** This is exactly the kind of adjustment I'd expect an interviewer to probe — the broker's number isn't wrong, it's just not what you'd actually earn as the buyer in year one.

### 1958 vintage: roof, insurance, and Broward recertification

You asked for roof condition, insurance implications, and Broward recertification requirements — here's what's real vs. what I'm flagging as unknown.

**Roof.** Not disclosed anywhere in the public listing data (LoopNet, Crexi, or the visible marketing bullets). The $1M+ capital-improvements list is specific and detailed (electrical, fencing, parking, mini-split AC, windows) and **conspicuously does not mention the roof**, which is the kind of omission worth noting rather than assuming away. **Judgment: treat roof age/condition as unknown and a live diligence item**, not as "recently replaced." I've added a placeholder roof-reserve line to the capex plan below rather than ignoring it.

**Insurance.** Two separate mechanisms are relevant, and I want to be precise about which one actually governs a commercial multifamily policy:
- **Sourced, but for homeowners' (personal-lines) policies specifically:** Florida SB 2-D (2022) says an insurer cannot refuse to write or renew a policy solely because a roof is 15+ years old, provided an inspection shows ≥5 years of remaining useful life; most insurers require a 4-point inspection (roof, electrical, plumbing, HVAC) for properties 15–20+ years old, and Citizens requires one for properties over 20 years old.
- **Judgment/extrapolation:** SB 2-D's text targets homeowners' insurance, not commercial blanket multifamily policies — I could not find a source confirming it binds commercial carriers the same way. In practice, commercial underwriters apply very similar logic (4-point-style inspections, roof-age scrutiny, wind mitigation credit questionnaires) when pricing older CBS-construction buildings, but this is my inference from how the personal-lines market works, not a confirmed commercial-market rule.
- **Practical implication:** because roof age is undisclosed and the building is 68 years old, I've priced insurance for this asset **above** the general South Florida $2,000/unit average cited in Phase 1 rev. 1 — see the updated operating-expense table below.

**Broward 40/50-Year Building Safety Inspection Program.** Sourced: Broward's program (in place since 2006, tightened post-Surfside) requires a structural and electrical inspection at 40 years of a building's life, then **every 10 years thereafter** — so 40, 50, 60, 70, etc. Some Broward municipalities (Fort Lauderdale, Hollywood, Pembroke Pines, Davie) run their own overlapping programs; **Pompano Beach isn't listed among those**, which suggests it likely follows the county baseline, but I haven't independently confirmed that with the Pompano Beach Building Department. A building built in 1958 turns 68 this year — on the standard 40/50/60/70 cycle, it would have already passed 40 (1998), 50 (2008), and 60 (2018), with the **next inspection due around 2028**. The listing's claim of "passed 40 & 50 year recertification" reads to me as shorthand for "compliant with the county's 40/50-Year Recertification Program" (a common way brokers refer to the program by its original name) rather than a literal claim that only the 1998 and 2008 exams have happened — but **I can't rule out the more concerning reading, that the 60-year (2018) inspection is the most recent one on file and nothing since.** This is a genuine, material diligence item: **confirm the actual date of the most recent recertification and the exact date the next one (likely ~2028) is due directly with Broward County / Pompano Beach Building Services** before relying on the broker's language. Your 5-year hold (if starting 2026) would run through the 2028 recertification cycle regardless of which reading is correct.

**Modeling response:** I've added a "recertification/roof contingency" reserve to the capital plan (see Section 2) rather than assuming this away.

### Market and exit-cap comps (kept from rev. 1, per your instruction)

| Property | Units | Built | County | Status | Price | $/Unit |
|---|---|---|---|---|---|---|
| [Cascades at the Hammocks](https://therealdeal.com/miami/2026/05/06/south-florida-top-real-estate-deals-may-5-2026/), Kendall | 264 | 1988 | Miami-Dade | Sold May 2026 | $65.5M | $248,100 |
| [Savona Grand](https://therealdeal.com/miami/2026/08/10/south-florida-top-real-estate-deals-august-7-2026/), Lake Worth | 214 | 2003 | Palm Beach | Sold Aug 2026 | $64.8M | $302,804 |

These stay in as market evidence for pricing/rent-growth context and as an exit-cap sanity check (better vintage/location assets trading meaningfully above Parkview Crossing's $142k/unit confirms the vintage/quality discount embedded in the subject deal), even though neither is a live listing.

The illustrative "Cove Pointe" asset from rev. 1 is **dropped** per your instruction.

---

## 2. Full assumption set (revised)

Legend: **Source** = a live link or named report. **Judgment** = my estimate, with the one-sentence reasoning and a range so you can defend or challenge it.

### Acquisition

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Purchase price | $13,800,000 ($142,268/unit) | **Sourced** — LoopNet/Crexi asking price. | — |
| Going-in cap rate — broker basis | 6.75% (Crexi calculator, precise) / 7.00% (LoopNet, rounded) | **Sourced**, see reconstruction above. | — |
| Going-in cap rate — reassessed-tax basis | **6.25%** (off the 6.75% broker basis) | **Derived**, see reconstruction above. This is the cap rate I'd use as the true "going-in" number. | 6.25%–6.50% depending on which broker NOI you start from |
| Closing costs | 1.5% of purchase price | **Judgment**, Broward-specific: doc stamps on the deed at $0.70/$100 (0.70%, Fla. Stat. §201.02 — Broward is NOT Miami-Dade's discounted $0.60/$100 rate) plus title insurance, legal, and third-party reports (PCA, Phase I ESA, appraisal, roof inspection given the vintage flag above). | 1.25%–2.0% |

### Unit mix and rents (97 units, per LoopNet's unit count)

| Unit type | Count | Renovated? | Avg SF | Est. in-place rent | Est. market (stabilized) rent |
|---|---|---|---|---|---|
| Studio | 19 | ~75% renovated proportionally (≈14 reno / 5 classic) | 540–750 | $1,275/mo | $1,550/mo |
| 1BR/1BA | 52 | ~75% (≈39 reno / 13 classic) | 600–770 | $1,475/mo | $1,780/mo |
| 2BR/1BA | 17 | ~75% (≈13 reno / 4 classic) | 700–780 | $1,700/mo | $2,050/mo |
| 2BR/2BA | 10 | ~75% (≈7 reno / 3 classic — note: this is my proportional split of "75% renovated," not a unit-by-unit disclosure) | 700–780 | $1,825/mo | $2,200/mo |

**How I built these:** The OM discloses a blended **20.76% rent upside** (Crexi investment highlights) — that's the one real, sourced anchor. I solved for a set of "market" rents such that the GPR-weighted average gap versus "in-place" rents comes out to ~20.76%, using apartments.com's own Pompano Beach 33060 submarket averages ($1,771 for 1BR, $2,319 for 2BR, as of the current listing pull) as the **upper-bound reference** for market rent — then discounted below that ceiling because 33060's blended average includes newer/better stock than this Class C asset can realistically achieve. Studio and 2BR/1BA figures are extrapolated proportionally (no direct submarket data for those configurations at this address) — **judgment, and the weakest-sourced row in this table.**

**Important — the 75/25 renovated split is disclosed at the property level, not unit-type level.** I don't have data on which unit types make up the ~24 remaining "classic" units. The per-type reno counts above are my own proportional allocation, not a disclosed fact — flag this if asked.

### Renovation program — bottom-up scope (proposed for your approval)

**Scope logic:** the OM states the 75% already-renovated units received "upgraded kitchens, new mini-split AC systems, vinyl slider windows, and modern lighting fixtures." To rent at the same market level, the remaining ~24 classic units need the **same bundle**, not a lighter or heavier one — so I've built the budget to match that disclosed standard, plus the ancillary items (flooring, bath, paint) that are standard for this scope of work even though not explicitly named in the OM.

| Line item | Cost/unit | Basis |
|---|---|---|
| Kitchen (cabinet refacing + hardware, laminate/quartz counter, sink/faucet, 4-piece stainless appliance package) | $7,000 | **Judgment**, mid-range of $4,500–15,000 kitchen-cabinet-and-counter cost guides found in 2026 renovation cost research; picked the lower-mid end because the OM's "upgraded kitchens" reads as a refresh, not a full gut, at this Class C price point. |
| Mini-split ductless AC system (1–2 zone) | $3,500 | **Judgment** — no single South Florida-specific mini-split install cost source found; general HVAC-mini-split market pricing. |
| Vinyl slider window replacement (~3 openings/unit) | $1,500 | **Judgment**, no specific source. |
| Modern lighting fixtures + ceiling fans | $400 | **Judgment**. |
| LVP flooring (~700 SF avg unit) | $4,000 | **Judgment**, using $5.50–$11.50/SF installed LVP cost range from 2026 flooring-cost research; picked the low-mid end (~$5.75/SF). |
| Bathroom refresh (vanity, fixtures, re-caulk, spot tile repair) | $1,200 | **Judgment**, below the $5,000–12,000 full-bath-remodel range since this is a refresh, not a gut — no bathroom upgrade is explicitly mentioned in the OM, so I've kept this line light. |
| Interior paint | $500 | **Judgment**. |
| Turnover labor / punch / make-ready cleaning | $500 | **Judgment**. |
| **Subtotal** | **$18,600** | |
| Contingency (10%) | $1,860 | **Judgment**, standard renovation-budget convention. |
| **Total per classic unit** | **$20,460 ≈ $20,500** | |

**Total renovation program: ~24 units × $20,500 ≈ $492,000** (not $1.44M — materially smaller than rev. 1's illustrative number, because 75% of the work is already done).

**Please confirm or edit this scope before Phase 2** — specifically: (a) whether you want to match the existing renovated standard exactly (my assumption) or upgrade further, and (b) whether a bathroom line this light is realistic, since I've deliberately kept it below full-remodel cost because the OM doesn't mention baths.

**Renovation return on cost:**
- Renovated rent premium: $150–200/mo judgment (Southeast Class B/C industry commentary), base case **$175/mo = $2,100/year**.
- Renovation ROI = $2,100 / $20,500 = **10.2%** (≈9.8-year simple payback on the renovation capital alone).
- **Flag: this falls below the ~15–20% yield-on-cost (5–7 year payback) threshold commonly cited as the bar for a renovation program to clearly pencil on a standalone cash-yield basis.** It's not a red flag on the deal — the exit-value uplift from capitalizing the extra NOI at the exit cap materially improves the full-cycle return, and I'll show that math explicitly in the Phase 2 sensitivity tables — but on a pure "does the renovation dollar earn its keep in cash flow" basis, 10.2% is average-to-soft, not compelling. Worth deciding whether to lean into a cheaper/lighter scope, or accept a longer payback because the exit math still works.
- Units renovated per month: 4/unit (≈6-month program, given the small remaining scope) — **judgment**.

### Operating assumptions

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Physical vacancy | 6.5% (vs. 92% disclosed occupancy) | **Sourced starting point** (92% occupancy, LoopNet), nudged down slightly for renovation-related downtime on the ~24 classic units. | 6%–9% during renovation, stabilizing lower after |
| Credit loss / bad debt | 1.0% of GPR | **Judgment**, standard underwriting convention. | 0.5%–1.5% |
| Concessions | 0.5% of GPR | **Judgment**, standard convention. | 0%–1.5% |
| Other income (RUBS, pet, parking, admin fees) | $35/unit/month | **Judgment** — no South Florida-specific source found. | $25–$50/unit/mo |
| Expense growth | 3.5%/year (ex-insurance, ex-taxes — those have their own lines) | **Judgment**, standard convention. | 3.0%–4.5% |

### Rent growth — ramped, not flat (revised per your instruction)

Three **separate, non-double-counted** mechanics:

**(1) Market rent growth** — a macro trend line applied to the "market rent" ceiling for all units, ramping from a near-flat current read up to a longer-run trend:

| Year | Market rent growth | Basis |
|---|---|---|
| 1 (2027) | 1.5% | **Sourced** — Miami-Dade County median asking rent was up 1.5% YoY as of May 2026 (MIAMI REALTORS®/RWorld South Florida Rental Market Report). Note Yardi Matrix separately clocked Miami-metro trailing-3-month rent growth at just 0.2% through April 2026 — the market is soft right now; 1.5% is the more representative annual figure, not the weakest monthly read. |
| 2 (2028) | 2.25% | **Judgment**, interpolated — Marcus & Millichap projects 2026–2028 completions (~10,000 units/yr) running above absorption (~8,000 units/yr) in the Miami market area, which should keep growth muted through this window before easing. |
| 3 (2029) | 2.75% | **Judgment**, continued normalization as M&M's cited "slowest inventory growth in a decade" (post-2026) takes hold. |
| 4 (2030) | 3.0% | **Judgment**, approaching long-run trend. |
| 5 (2031) | 3.25% | **Judgment**, long-run Sun Belt multifamily trend rate. |
| 6–10 | 3.25% (flat) | **Judgment**, terminal/stabilized assumption — no source for years this far out; treat as a standard long-run planning rate. |

**(2) Loss-to-lease burn-off** — applies only to **not-yet-renovated units** (both the ~24 classic units before their turn, and any already-renovated units still priced below that year's market rent per the disclosed 20.76% blended gap). Mechanic: at each lease turnover event, the unit's rent resets to `prior rent + 50% × (that year's market rent − prior rent)`, capped at market rent. **Judgment**: 50%-of-gap-per-turnover is a standard conservative convention (full one-shot mark-to-market at renewal is unrealistic); annual turnover assumed at ~55%, a general Class B/C garden-apartment industry convention **not specifically sourced for this property** — flag if pressed.

**(3) Renovation premium** — a one-time event when a classic unit gets renovated: `new rent = that month's market rent + $175/mo`, then grows with market rent growth thereafter. This only fires once per unit, at renovation.

**No double-counting check:** market rent grows on its own schedule regardless of any given unit's status; burn-off only moves a specific unit's rent toward that already-grown market rent; the renovation premium is a one-time add-on layered on top of market rent at the moment of renovation, not stacked with burn-off. Once a unit is renovated, burn-off no longer applies to it (there's no more gap to close).

### Operating expenses (Year 1, $/unit/year unless noted)

| Line | Value | Source / Judgment |
|---|---|---|
| Payroll (on-site mgmt + maintenance) | $1,400/unit | **Judgment**, no specific source. |
| Repairs & maintenance | $1,100/unit | **Judgment**, nudged up from rev. 1's $900 given the 1958 vintage and undisclosed roof status. |
| Turnover / make-ready | $350/unit | **Judgment**. |
| Contract services (landscaping, pest, trash) | $450/unit | **Judgment**. |
| Utilities (owner-paid common area/vacant units) | $500/unit | **Judgment**. |
| **Property insurance** | **$2,400/unit ($232,800 total)** | **Judgment, adjusted upward from the general $2,000/unit South Florida average** (multiple 2026 industry sources citing Florida multifamily insurance ~$800/unit two years ago → ~$2,000/unit currently) specifically because this is a 68-year-old CBS building with an undisclosed roof condition — older/frame/undocumented-roof stock is cited in the same sources as running $900–$2,500+/unit. Get an actual quote before defending this number; it is a placeholder for real underwriting. |
| Insurance growth rate | 7%/year | **Judgment**, above general 3.5% expense growth, reflecting the cited ~37% two-year (≈17%/yr compounded) recent trend moderating somewhat going forward — this is a guess at moderation, not a sourced forecast. |
| Property taxes | Modeled on reassessed basis (Section 1 math), grown at 10%/year cap (Florida non-homestead cap) or actual millage growth, whichever is lower | See Section 1 and Section 3. |
| Management fee | 3.5% of EGI | **Judgment**, standard convention. |
| G&A / admin | $250/unit | **Judgment**. |
| Marketing | $150/unit | **Judgment**. |
| Replacement reserves (below NOI) | $300/unit | **Judgment**, standard lender convention. |
| **Roof / recertification contingency reserve** | **$750/unit/year, funded for the first 3 years then reassessed** (~$72,750/yr) | **Judgment — new line, direct response to the undisclosed roof and ambiguous recertification status.** This is a placeholder until you get an actual roof inspection and confirm the next recertification date with Broward/Pompano Beach; if the roof turns out to be recently replaced and the 70-year recertification is comfortably scheduled, this reserve should come down. |

### Debt

Largely unchanged from rev. 1 — the model will size fresh acquisition debt generically (index + spread, LTV/DSCR/debt-yield binding-constraint logic), not simply assume the seller's existing loan.

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Index | 1-month SOFR, ~3.85% | **Sourced** — [sofrrate.com](https://www.sofrrate.com/), reading as of 9/18/2026. | — |
| Spread | +325 bps | **Judgment**, within the 200–500bps range cited for 2026 multifamily bridge/value-add financing. | +200 to +400 bps |
| LTV | 65% | **Judgment**, mid-point of the 65–75% range cited for 2026 multifamily bridge loans. | 60%–70% |
| Interest-only period | 24 months | **Judgment**. | 18–36 months |
| Amortization (post-IO) | 30 years | **Judgment**. | 25–30 years |
| Min. DSCR / debt yield constraint | 1.25x DSCR / 8.0% debt yield | **Judgment**, standard cited lender minimums; model shows which of LTV/DSCR/debt yield binds. | DSCR 1.20–1.30x; debt yield 7.5–9.0% |
| Refinance | Toggle — refi at stabilization or hold to exit | **Judgment**, structural feature. | — |

**Noted but not modeled by default:** the real assumable loan (~$5.9M @ 3.0% fixed to Dec 2029, plus a $3.563M supplemental piece at 6.20%, blended ~4.2%) is a genuinely attractive, real financing alternative disclosed in the OM. I'm keeping the model's DEBT tab generic per the Phase 2 spec (so it works as a teaching example of how to size acquisition debt from scratch), but flagging that the assumable structure would materially change the levered return math — worth adding as an alternative-financing toggle in Phase 2 if you want to show both.

### Hold and exit

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Hold period | 5 years | **Judgment**, standard value-add hold. | 3–7 years |
| Exit cap rate | **Entry + 50bps (base case)** | **Per your instruction.** Entry cap (reassessed basis) 6.25% → exit 6.75%. | Sensitivity extends to **+100bps** (exit 7.25%) |
| Cost of sale | 2.0% of exit price | **Judgment**, standard convention. | 1.5%–2.5% |

### Waterfall — unchanged from rev. 1

| Assumption | Value | Source / Judgment |
|---|---|---|
| Preferred return | 8.0% | **Judgment**, standard LP preferred return convention. |
| Tier 1 | 100% LP / 0% GP until pref + capital returned | Standard structure |
| Tier 2 | 70/30 LP/GP up to 12% IRR | **Judgment**. |
| Tier 3 | 50/50 LP/GP above 12% IRR | **Judgment**. |
| GP co-invest | 10% of equity | **Judgment**. |

All editable inputs in Phase 2's ASSUMPTIONS tab.

---

## 3. Florida-specific items (revised)

### Property tax reassessment on sale

Unchanged mechanic from rev. 1 (non-homestead 10% cap doesn't carry to a new owner; reassessed to market value the January following sale), now applied to **real numbers**: see the broker-cap-vs-reassessed-cap reconstruction in Section 1. **Florida Amendment 3** (Nov 3, 2026 ballot, would cut the non-homestead cap 10%→5% starting 2027 if passed) remains unmodeled by default — flag for your decision.

### Property insurance

Revised upward for this specific asset (see operating expense table) given the 1958 vintage and undisclosed roof — see the roof/insurance/recertification writeup in Section 1 for full sourcing and the honest distinction between what's sourced (the SB 2-D homeowners'-insurance rule, the general Florida multifamily insurance cost trend) and what's my extrapolation to the commercial context.

### Broward 40/50-Year Recertification

New section, not in rev. 1 (which used a generic illustrative asset with no real building-safety history) — see full writeup in Section 1.

### Live Local Act — excluded from the model, per your instruction

Findings unchanged from rev. 1 (71-unit minimum, 40%+ affordable at ≤100% AMI for 30 years, 75–100% ad valorem exemption depending on affordable share). Parkview Crossing's 97 units would meet the unit-count threshold. **A one-paragraph version of this has been added to `README.md`** (stub created now, full README to follow in Phase 4) as the "alternative strategy considered" writeup you asked for.

---

## 4. What I need from you before Phase 2

1. **Renovation scope approval** — confirm or edit the 8-line bottom-up budget above ($20,500/unit, ~24 units, ~$492,000 total). In particular: is matching the existing renovated standard the right call, and is the light bathroom line ($1,200) realistic?
2. **Renovation ROI is soft (10.2%, below the ~15–20% typical threshold)** — decide whether you want to see a cheaper/lighter alternative scope modeled alongside this one, or proceed and let the exit-value math carry it.
3. **Roof and recertification are genuinely unknown** — the $750/unit/year contingency reserve is a placeholder, not a real number. If you can get an actual roof inspection or confirm the Broward recertification timeline, this should be replaced with real data before Phase 2 locks.
4. **Insurance at $2,400/unit** is my upward adjustment for vintage/roof risk — confirm you want that adjustment (vs. the generic $2,000/unit market average) or want me to get a real quote-based number instead.
5. **Exit cap** — set at entry+50bps base case per your instruction, sensitivity to +100bps. Confirmed, no action needed unless you want to change it.
6. **Assumable debt** — confirm whether you want the real ~4.2%-blended assumable loan modeled as an alternative financing toggle in Phase 2, in addition to the generic freshly-sized debt.

I have not built anything beyond this document. Nothing here is final.
