#!/usr/bin/env python3
"""
bridge.py -- change bridge from the prior base case (Scenario A levered IRR 5.20%, commit efb3da1)
to the current base case, one row per change, applied cumulatively in the order listed.

Runs on verify_model.py's engine (the one that ties to the workbook line by line). Row 0 switches
every change OFF via run_model(legacy=...) and must reproduce the prior 5.20%; the last row has
every change ON and must equal the current workbook.

Usage: python3 bridge.py [workbook.xlsx]
"""
import sys
import verify_model as V

PATH = sys.argv[1] if len(sys.argv) > 1 else "Parkview_Crossing_Acquisition_Model.xlsx"
I = V.load_inputs(PATH)

STEPS = [
    (None, "Prior base case (commit efb3da1)"),
    ("tax10", "A. Property tax grows with just value (3.0%), not the 10% cap"),
    ("util_old", "B. Owner-paid water/sewer/trash at city rates, 60% RUBS recovery, other income re-split"),
    ("exit_old", "C. Exit cap = direct market input 6.60% (was in-place + 50 bps)"),
    ("debt_old", "D1. Agency fixed 7.24% (10-yr UST + 200 bps), 75% LTV / 1.25x amortizing DSCR, no IO"),
    ("no_prepay", "D2. Prepayment premium at sale (Fannie declining schedule)"),
    ("no_paydown", "D3. Assumption paydown test (75% max LTV on price)"),
    ("classic_bug", "Bug fix: renovated classic units reach market rent from Year 2"),
    ("plan10", "E. Exit plan: short floating refi + 2-yr cap (was 10-yr fixed repaid in loan yr 2)"),
    ("b10", "F. Scenario B: 5-yr agency fixed matched to hold (was 10-yr, 3% premium at sale)"),
    ("sofr_old", "G. SOFR input aligned to the 9/28/2026 FRED print: 3.7307% (was 3.74%)"),
]


def run():
    legacy = set(V.LEGACY_FLAGS)
    rows, prev = [], None
    for flag, label in STEPS:
        if flag:
            legacy.discard(flag)
        m = V.run_model(I, legacy=tuple(legacy))
        A, B = m["A"], m["B"]
        row = dict(label=label, a_irr=A["irr"], a_em=A["em"], b_irr=B["irr"], unlev=m["unlev_irr"],
                   noi1=m["noi"][0], exit_cap=m["exit_cap"], call=A["capital_call"],
                   refi=A["plans"][A["plan_key"]].get("loan", 0.0),
                   delta=None if prev is None else A["irr"] - prev)
        rows.append(row)
        prev = A["irr"]
    assert not legacy
    return rows


if __name__ == "__main__":
    rows = run()
    print(f"{'Change (cumulative)':88s}{'A lev IRR':>10s}{'chg bp':>8s}{'A EM':>7s}{'B lev':>8s}{'Unlev':>8s}"
          f"{'Y1 NOI':>11s}{'Exit cap':>9s}{'Y3 call':>11s}{'Refi loan':>12s}")
    for r in rows:
        d = "" if r["delta"] is None else f"{r['delta'] * 1e4:+.0f}"
        print(f"{r['label']:88s}{r['a_irr']:>10.2%}{d:>8s}{r['a_em']:>6.2f}x{r['b_irr']:>8.2%}{r['unlev']:>8.2%}"
              f"{r['noi1']:>11,.0f}{r['exit_cap']:>9.2%}{r['call']:>11,.0f}{r['refi']:>12,.0f}")
    print(f"\nTotal change: {(rows[-1]['a_irr'] - rows[0]['a_irr']) * 1e4:+.0f} bp")
