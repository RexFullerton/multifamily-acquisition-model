# Phase 1 — Asset Selection and Assumption Set

Status: **DRAFT FOR REVIEW.** Nothing in this document has been approved. No model has been built.
Prepared: 2026-09-21

---

## 1. Candidate search — what I actually found

I searched LoopNet listings for every apartment building currently for sale in Miami-Dade (204 listings), Broward (128 listings), and Palm Beach (39 listings) counties, plus news/trade-press searches (Green Street News, The Real Deal, GlobeSt, Yardi Matrix) for South Florida value-add multifamily deal activity. Crexi's search results could not be reliably scraped (its listing grid did not apply county/type filters in the automated browser session — it kept serving an unfiltered national "recommended" feed), so it is not a complete source here; LoopNet's public listing pages were fully accessible.

**Finding: there is no property currently for sale in the three counties that is simultaneously (a) 80–200 units, (b) built 1970s–1990s, and (c) has publicly disclosed pricing.** The 80–200-unit band on LoopNet right now is thin — only three listings across all three counties fall in or near it, and none is the right vintage:

| Property | Units | Built | Status | Price | Cap Rate |
|---|---|---|---|---|---|
| [Parkview Crossing](https://www.loopnet.com/Listing/901-951-NW-8th-Ave-Pompano-Beach-FL/35917237/), Pompano Beach (Broward) | 97 | **1958** | Actively listed (listed 6/30/2026, broker Franklin Street) | $13,800,000 ($142,268/unit) | 7.0% |
| Havana Palms II, 910 SW 2nd St / 931 SW 3rd St, Miami (Little Havana) | 79 | **1946** | Actively listed | $18,500,000 ($234,177/unit) | Not disclosed |
| Il Villaggio, 1455 Ocean Dr, Miami Beach | 127 | Pre-war (historic) | Actively listed | Price upon request | Not disclosed |

Parkview Crossing is the strongest real candidate by data richness — it has a full public unit mix, an assumable-loan note, capex history, occupancy, and a broker flyer — but it's a 1958 concrete-block garden property, not 1970s–1990s. The other two either miss the vintage by even more or don't disclose price.

I also pulled two **recently closed** South Florida value-add trades as market evidence (not active listings, but real, disclosed transactions useful for calibrating price/unit and cap rate):

| Property | Units | Built | County | Sale Date | Price | $/Unit |
|---|---|---|---|---|---|---|
| [Cascades at the Hammocks](https://therealdeal.com/miami/2026/05/06/south-florida-top-real-estate-deals-may-5-2026/), Kendall | 264 | **1988** | Miami-Dade | May 2026 | $65.5M | $248,100 |
| [Savona Grand](https://therealdeal.com/miami/2026/08/10/south-florida-top-real-estate-deals-august-7-2026/), Lake Worth | 214 | 2003 | Palm Beach | Aug 2026 | $64.8M | $302,804 |

Cascades is actually the right vintage (1988) and county mix, but it's 264 units (above your 200-unit ceiling) and it's a closed sale, not something you could underwrite an acquisition of today — there's no rent roll or T-12 attached to a news article.

**Conclusion: per your fallback instruction, I'm proposing a constructed illustrative asset** rather than stretching one of the above into a false fit. Below it's labeled illustrative everywhere, and its pricing/rent/cap-rate assumptions are anchored to the real comps above, not invented in a vacuum.

### Proposed illustrative asset

**"Cove Pointe Apartments" (illustrative name, no real address)** — a hypothetical 120-unit garden-style community in the Pompano Beach / Margate / Tamarac corridor of Broward County, built 1985, Class C, 3-story walk-up construction, on ~6 acres. Positioned as a classic value-add deal: rents below market because units haven't been touched since original build-out, on-site management has been passive, and a straightforward interior-renovation program is the thesis.

I picked Broward specifically because it's where the real comp (Parkview Crossing) lives, so the pricing/rent benchmarks below aren't guessed from nothing — they're interpolated between a real 1958/Class C Broward comp and a real 1988/Miami-Dade comp.

**If you'd rather I keep pushing on a real listing** (e.g., accept the 1958 vintage of Parkview Crossing, or widen the unit-count band, or pull Crexi/CoStar data through a different path), tell me and I'll redo this section. Otherwise, Phase 2 will build off the illustrative asset below.

---

## 2. Full assumption set

Legend: **Source** = a live link or named report. **Judgment** = my estimate, with the one-sentence reasoning and a range so you can defend or challenge it.

### Acquisition

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Purchase price | $19,800,000 ($165,000/unit) | **Judgment.** Interpolated between Parkview Crossing ($142k/unit, 1958, Broward, Class C) and Cascades at the Hammocks ($248k/unit, 1988, Miami-Dade, better submarket) — a 1985 Broward asset should price above the 1958 comp (newer structure, better mechanical/electrical life) but below the Miami-Dade comp (weaker submarket, no waterfront/urban-infill premium). | $150k–$185k/unit ($18.0M–$22.2M) |
| Going-in cap rate (in-place NOI) | 6.75% | **Judgment**, bracketed by real South Florida trade data: Parkview Crossing trades at 7.0% (older, rougher asset, priced for the risk), general Broward/Palm Beach value-add trades cited in market commentary cluster 5.5–7.0%. 6.75% assumes a slightly better-positioned asset than Parkview Crossing. | 6.25%–7.25% |
| Closing costs | 1.75% of purchase price | **Judgment**, standard FL commercial convention: doc stamps on the deed at $0.60/$100 in Miami-Dade or $0.70/$100 elsewhere (Fla. Stat. §201.02) plus title insurance, legal, and third-party reports (PCA, Phase I ESA, appraisal). Not scoured for a live source — this is a well-established statutory/market convention. | 1.25%–2.25% |

### Unit mix and rents (120 units)

| Unit type | Count | Avg SF | In-place rent | Market (renovated) rent | Loss-to-lease |
|---|---|---|---|---|---|
| 1BR / 1BA | 60 (50%) | 650 | $1,550/mo | $1,750/mo | $200/mo |
| 2BR / 2BA | 48 (40%) | 850 | $1,850/mo | $2,050/mo | $200/mo |
| 3BR / 2BA | 12 (10%) | 1,050 | $2,150/mo | $2,400/mo | $250/mo |

**All judgment**, calibrated as follows: the Yardi Matrix Miami/South Florida market report (June 2026) puts the **overall metro asking rent average at $2,526/mo** — but that average is pulled up hard by new Class A lease-ups (like the Soleste portfolio at $3,082 average) and isn't representative of unrenovated 1980s Class C stock. Unrenovated Class C garden units in tertiary Broward submarkets typically trade 30–40% below the metro blended average; the figures above reflect that discount. **Reasonable range: in-place rents could be $100–150/mo higher or lower depending on the actual submarket** (Pompano Beach core vs. Margate/Tamarac interior) — this is the single assumption I'd most want you to pressure-test against an actual rent comp set (RentCafe/Apartments.com asking rents for nearby 1980s stock) before defending it.

### Renovation program

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Interior renovation scope | LVP flooring, stone/quartz counters, stainless appliances, fixtures, paint | **Judgment**, standard institutional Class B/C value-add scope per multiple 2026 industry renovation guides. | — |
| Renovation cost per unit | $12,000/unit ($1,440,000 total) | **Judgment — weakest-sourced number in this set.** Search results gave a very wide, inconsistent range ($3,000–5,000 "modest," up to $150–300/SF full gut) from secondary SEO content, not a primary contractor cost report. $12,000/unit is a mid-point guess for a classic (not full-gut) interior scope. **You should get an actual GC quote or RSMeans-type cost data before defending this number in an interview.** | $8,000–$18,000/unit |
| Renovated rent premium | $150/mo | **Judgment**, informed by industry commentary suggesting $100–250/mo premiums for full interior upgrades in Class B/C Southeast assets. | $100–$250/mo |
| Units renovated per month | 4/month (30-month program) | **Judgment** — a common pace for a 120-unit value-add plan that avoids over-concentrating vacancy loss; no source, just standard practice. | 3–6 units/month |
| Exterior/common-area capex | $500,000 (~$4,167/unit) | **Judgment** — paint, landscaping, signage, amenity refresh, roof/parking lot repairs as needed; no specific source. | $300k–$800k |

### Operating assumptions

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Physical vacancy | 6.0% | **Judgment.** Yardi Matrix reports Miami-metro stabilized occupancy at 95% (5% vacancy) as of March 2026, down 50bps YoY — I've nudged to 6% for a Class C asset mid-renovation, which typically runs a bit looser than stabilized Class A/B. | 5%–8% |
| Credit loss / bad debt | 1.0% of GPR | **Judgment**, standard underwriting convention. | 0.5%–1.5% |
| Concessions | 0.5% of GPR | **Judgment**, standard underwriting convention for a competitive but not distressed submarket. | 0%–1.5% |
| Other income (RUBS, pet, parking, admin fees) | $35/unit/month | **Judgment** — typical workforce-housing other-income range; no specific South Florida source found. | $25–$50/unit/mo |
| Rent growth (Years 1–10) | 3.0%/year | **Judgment.** Yardi Matrix's own trailing-3-month rent growth was only 0.2%, i.e., near-flat currently — but that's a snapshot of a soft moment in a market that's absorbed a lot of new Class A supply (2,649 units delivered through April 2026). 3.0% is a longer-run trend assumption, not a read of today's market — flag this gap explicitly if asked. | 2.0%–4.0% |
| Expense growth | 3.5%/year | **Judgment**, standard convention (expenses typically outpace rent growth slightly, driven by insurance/taxes — see below). | 3.0%–4.5% |

### Operating expenses (Year 1, $/unit/year unless noted)

| Line | Value | Source / Judgment |
|---|---|---|
| Payroll (on-site mgmt + maintenance) | $1,400/unit | **Judgment** — no specific South Florida payroll benchmark found; standard industry range for a self-managed Class C garden asset. |
| Repairs & maintenance | $900/unit | **Judgment**, standard range for older vintage requiring more upkeep. |
| Turnover / make-ready | $350/unit | **Judgment**. |
| Contract services (landscaping, pest, trash) | $450/unit | **Judgment**. |
| Utilities (owner-paid common area/vacant units) | $500/unit | **Judgment**. |
| Property insurance | $2,000/unit ($240,000 total) | **Sourced (directional).** Multiple 2026 industry sources cite Florida multifamily insurance averaging **~$2,000/unit/year currently, up from ~$800/unit two years prior** — a ~37% annualized increase driven by hurricane/litigation risk. Treated as its own flagged line below with its own growth rate. |
| Property taxes | See FL-specific section below | Modeled on reassessed basis, not a flat assumption. |
| Management fee | 3.5% of EGI | **Judgment**, standard third-party management convention. |
| G&A / admin | $250/unit | **Judgment**. |
| Marketing | $150/unit | **Judgment**. |
| Replacement reserves (below NOI) | $300/unit | **Judgment**, standard lender-required convention. |

### Debt

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Index | 1-month SOFR, currently ~3.85% | **Sourced** — [sofrrate.com](https://www.sofrrate.com/), reading as of 9/18/2026. | — |
| Spread | +325 bps | **Judgment**, within the 200–500bps range cited for 2026 multifamily bridge/value-add acquisition financing in industry lender surveys. | +200 to +400 bps |
| All-in floating rate | ~7.10% | Derived (SOFR + spread) | — |
| LTV | 65% | **Judgment**, mid-point of the 65–75% range typically cited for multifamily bridge loans in 2026 industry sources. | 60%–70% |
| Interest-only period | 24 months | **Judgment**, matched to the renovation/lease-up business plan. | 18–36 months |
| Amortization (post-IO) | 30 years | **Judgment**, standard convention. | 25–30 years |
| Renovation holdback | Available, drawn against capex schedule | **Judgment** — structural feature, not a number. | — |
| Min. DSCR / debt yield constraint | 1.25x DSCR / 8.0% debt yield | **Judgment**, standard lender minimums cited across bridge-lending sources; the model will show which of LTV/DSCR/debt yield actually binds. | DSCR 1.20–1.30x; debt yield 7.5–9.0% |
| Refinance | Toggle — refinance at stabilization (Month 30) into a fixed-rate agency-style permanent loan, or hold the bridge loan to exit | **Judgment** — a standard value-add structure; the model will let you toggle it. | — |

### Hold and exit

| Assumption | Value | Source / Judgment | Range |
|---|---|---|---|
| Hold period | 5 years | **Judgment**, standard value-add hold. | 3–7 years |
| Exit cap rate | 7.00% (going-in cap + 25 bps) | **Judgment.** Market commentary on core multifamily cites a ~20bps going-in-to-exit spread, widening to 50–75bps for value-add/secondary assets. I've used +25bps as a base case (below the cited value-add range) — **you may want to widen this to +50–75bps for a more conservative, defensible base case**, since a +25bps spread is on the aggressive end for a 5-year hold. | +25 to +75 bps over entry |
| Cost of sale | 2.0% of exit price | **Judgment**, standard broker commission + closing cost convention. | 1.5%–2.5% |

### Waterfall

| Assumption | Value | Source / Judgment |
|---|---|---|
| Preferred return | 8.0% | **Judgment**, standard LP preferred return convention. |
| Tier 1 (return of capital + pref) | 100% LP / 0% GP until pref + capital returned | Standard structure |
| Tier 2 | 70/30 LP/GP up to 12% IRR | **Judgment**, a common mid-tier promote split. |
| Tier 3 | 50/50 LP/GP above 12% IRR | **Judgment**, common back-end split. |
| GP co-invest | 10% of equity | **Judgment**, typical GP co-investment level. |

All waterfall parameters will be editable inputs in the ASSUMPTIONS tab — these are starting points, not fixed.

---

## 3. Florida-specific items

### Property tax reassessment on sale

**Researched, sourced.** Florida's non-homestead 10% annual assessment cap does **not** carry over to a new owner: on transfer of ownership, the property is reassessed to full market value (typically the purchase price, or the appraiser's independent market value determination) in the January 1 following the sale, then the 10% annual cap resumes for future years under the new owner. The model must tax on the **new (post-sale) basis**, not the seller's existing assessed value — this is a common modeling error and will be built correctly.

Live consideration: **Florida Amendment 3** is on the November 3, 2026 ballot and would cut the non-homestead cap from 10% to 5%, effective for the 2027 tax year if it passes with 60% voter approval. It doesn't change the reassessment-on-sale mechanic, only the annual growth cap afterward. I'll model the current 10% cap as the base case and can add the 5% cap as a toggle/sensitivity if you want — **flag for your decision, not yet modeled.**

I pulled Parkview Crossing's actual current county assessment as a real reference point: total assessed value $10,318,700 against a $13.8M asking price — illustrating the exact gap a buyer's reassessment would need to close (in that real case, roughly +34% to basis, generating a materially higher post-sale tax bill than the seller was paying).

### Property insurance

**Researched, sourced (directionally, not a single verifiable index).** Multiple 2026 industry sources converge on Florida multifamily insurance having risen from roughly **$800/unit/year two years ago to roughly $2,000/unit/year currently** (~37% increases cited), driven by hurricane exposure and litigation-related claims, with some sources citing older/coastal/frame stock running $900–$2,500+/unit. I could not find a single authoritative primary-source index (e.g., a specific MMI/CBRE/JLL insurance survey) — this is aggregated from several secondary industry commentary sources, so treat the $2,000/unit figure as directionally right but not laboratory-precise. I've modeled it as its own line with an elevated growth rate (I'd suggest 6–8%/year vs. 3.5% general expense growth, given the trend) — **flag for your input on the growth rate.**

### Live Local Act

**Researched — not modeled, per your instruction.** Findings:

- Florida's Live Local Act (now in its "4.0" iteration as of House Bill 1389, effective July 1, 2026) provides an **ad valorem property tax exemption** for qualifying affordable multifamily developments.
- To qualify: a property must have **at least 71 units**, and must reserve **at least 40% of units as affordable** (at ≤100% AMI, tightened down from 120% AMI in the 2026 update) for a minimum **30-year** compliance period.
- The exemption is **75% of assessed value** for the affordable units if less than 100% of the project is affordable, or **100% of assessed value** if the entire project is designated affordable.
- **Relevance to this asset:** Cove Pointe (120 units) would meet the unit-count threshold, but electing Live Local would require permanently restricting 48+ units to below-market, income-qualified rents for 30 years — directly conflicting with the value-add thesis of pushing rents to market through renovation. It's a real, live option worth understanding (and worth being able to discuss in an interview), but **not something I've built into the model** without your sign-off, since it would fundamentally change the deal from a rent-growth play to a tax-exemption/affordable-housing play.

---

## 4. What I need from you before Phase 2

1. **Approve, reject, or redirect the illustrative-asset approach.** If you'd rather I underwrite the real Parkview Crossing listing (1958 vintage, not 1970s–1990s) instead of a constructed asset, say so — it has genuinely better data (an actual T-12-adjacent flyer, assumable debt, real unit mix) even though it misses your vintage brief.
2. **Renovation cost per unit** is the weakest-sourced number here ($8k–$18k judgment range) — worth tightening if you can find a real contractor quote or cost report.
3. **Exit cap spread** (+25bps in my base case) is aggressive relative to the +50–75bps cited for value-add assets generally — I'd lean toward you widening this for defensibility.
4. **Rent growth** (3.0%/yr assumed) sits well above the ~flat trailing rent growth Yardi Matrix reported for the actual current Miami market — worth being ready to explain why you're underwriting above the current trend.
5. **Live Local Act** — confirm you want it left out of the model (my default assumption based on your instructions).

I have not built anything beyond this document. Nothing here is final.
