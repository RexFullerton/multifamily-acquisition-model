#!/usr/bin/env python3
"""
price_solve.py -- maximum purchase price that achieves each target return, under both debt
scenarios, using the SAME engine verify_model.py checks against the workbook line by line.

Targets
  (a) LP IRR = 8%            (LP clears the preferred return)
  (b) Levered IRR = 12%      (deal level)
  (c) Levered IRR = 15%      (deal level)

What moves with price (everything else held at the Assumptions-tab values):
  - Property tax: reassessed at price x 85% cost-of-sale factor x millage (then grows with just value).
  - Closing costs: 1.5% of price.
  - Scenario B loan: MIN(75% LTV x price, DSCR leg); the DSCR leg moves only through NOI (tax).
  - Scenario A: the lender's assumption test -- if assumed balances exceed 75% of price, the buyer
    pays down principal at closing (supplemental first). Below ~$12.6M this adds equity.
  - Equity: the plug. Going-in (in-place) cap: Day-0 NOI at that price / price.
What does NOT move:
  - Exit cap: a direct market input (6.60%), independent of what this buyer pays.
  - Rents, other opex, renovation capex, the refinance terms.

Writes bid_prices.json (read by build_model.py for the Summary tab's Bid Price rows) and checks the
workbook's Summary rows against a fresh solve.

Usage: python3 price_solve.py [workbook.xlsx]
"""
import json
import sys
from scipy.optimize import brentq
import verify_model as V

PATH = sys.argv[1] if len(sys.argv) > 1 else "Parkview_Crossing_Acquisition_Model.xlsx"
I = V.load_inputs(PATH)
BASE = V.run_model(I)
UNITS = I["units"]
LO, HI = 6_000_000, 20_000_000

TARGETS = [("lp", 0.08, "LP IRR = 8%"), ("deal", 0.12, "Levered IRR = 12%"), ("deal", 0.15, "Levered IRR = 15%")]
SCENS = [("A", "A (base)", "Scenario A — assumed loan (BASE CASE)"), ("B", "B (alt)", "Scenario B — new agency debt (alternative)")]


def metric(price, scen, target):
    m = V.run_model(I, price=price)
    S = m[scen]
    W = S["W"] if scen == "B" else m["W"]
    return (W["lp_irr"] if target == "lp" else S["irr"]), m


def solve(scen, target, rate):
    g = lambda p: metric(p, scen, target)[0] - rate
    glo, ghi = g(LO), g(HI)
    if glo != glo or ghi != ghi or glo * ghi > 0:  # nan or no sign change
        return dict(unreachable=True)
    p = brentq(g, LO, HI, xtol=1.0)
    _, m = metric(p, scen, target)
    S = m[scen]
    W = S["W"] if scen == "B" else m["W"]
    return dict(unreachable=False, price=p, ppu=p / UNITS, vs_ask=p / BASE["price"] - 1, cap_inplace=m["cap_inplace"],
                deal_irr=S["irr"], lp_irr=W["lp_irr"], gp_irr=W["gp_irr"], equity=S["equity"],
                debt_memo=(m["A"]["assume_paydown"] if scen == "A" else m["B"]["loan"]),
                binding=(None if scen == "A" else m["B"]["binding"]))


def run():
    out = []
    print(f"Base case at ${BASE['price']:,.0f} (${BASE['price']/UNITS:,.0f}/unit): in-place cap {BASE['cap_inplace']:.2%}, "
          f"exit cap {BASE['exit_cap']:.2%}, A levered {BASE['A']['irr']:.2%} (LP {BASE['W']['lp_irr']:.2%}), "
          f"B levered {BASE['B']['irr']:.2%}\n")
    for scen, short, slab in SCENS:
        print(slab)
        print(f"  {'Target':20s}{'Max price':>14s}{'$/unit':>10s}{'vs ask':>8s}{'In-place cap':>13s}{'Deal IRR':>10s}"
              f"{'LP IRR':>8s}{'GP IRR':>8s}{'Equity':>13s}{'A paydown / B loan':>20s}")
        for key, rate, tlab in TARGETS:
            r = solve(scen, key, rate)
            label = f"{short}: {tlab}"
            if r["unreachable"]:
                print(f"  {tlab:20s}  UNREACHABLE between ${LO:,.0f} and ${HI:,.0f}")
                out.append(dict(label=label, unreachable=True, note=f"not reachable between ${LO/1e6:.0f}M and ${HI/1e6:.0f}M"))
                continue
            memo = f"{r['debt_memo']:,.0f}" + (f" ({r['binding']})" if r["binding"] else "")
            print(f"  {tlab:20s}{r['price']:>14,.0f}{r['ppu']:>10,.0f}{r['vs_ask']:>8.1%}{r['cap_inplace']:>13.2%}"
                  f"{r['deal_irr']:>10.2%}{r['lp_irr']:>8.2%}{r['gp_irr']:>8.2%}{r['equity']:>13,.0f}{memo:>20s}")
            out.append(dict(label=label, **{k: v for k, v in r.items() if k != "binding"}))
        print()
    return out


def check_summary(rows, path):
    """Staleness guard: the Summary tab's Bid Price rows are solver output -- flag drift vs. a fresh solve."""
    import openpyxl
    ws = openpyxl.load_workbook(path, data_only=True)["Summary"]
    fresh = {r["label"]: r for r in rows}
    seen, stale = 0, 0
    for rr in range(1, ws.max_row + 1):
        lab = ws.cell(row=rr, column=1).value
        if lab in fresh:
            seen += 1
            f, typed = fresh[lab], ws.cell(row=rr, column=2).value
            if f.get("unreachable") != (not isinstance(typed, (int, float))) or \
               (not f.get("unreachable") and abs(f["price"] - typed) > 1000):
                stale += 1
                print(f"  STALE Summary row '{lab}': workbook {typed}, fresh {f.get('price')}")
    if seen != len(rows):
        stale += 1
        print(f"  Summary has {seen} of {len(rows)} Bid Price rows")
    print("Summary Bid Price rows:", "STALE -- run build_model.py (it reads bid_prices.json) and recalc" if stale
          else "match the fresh solve (within $1,000).")


if __name__ == "__main__":
    rows = run()
    json.dump(dict(source=PATH, rows=rows), open("bid_prices.json", "w"), indent=1)
    print("wrote bid_prices.json")
    check_summary(rows, PATH)
