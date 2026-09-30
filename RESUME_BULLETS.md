# Resume Bullets

- Showed a 97-unit Florida listing's 7.0% broker cap rate was 5.86% in-place after post-sale property-tax reassessment and full expense underwriting. (20 words)
- Underwrote assumable 3.0% debt and refinance options: $13.8M ask yields 5.7% levered IRR; maximum bid for an 8% LP IRR is $13.37M. (22 words)

## Where each number comes from

All cells are in `Parkview_Crossing_Acquisition_Model.xlsx`, as committed. `verify_model.py` independently reproduces every computed cell below (1,078 figures tie within $1 or 1 bp).

| Number in bullet | Workbook cell | Cell value | Type |
|---|---|---|---|
| 97 units | Assumptions!C6 | 97 | Formula: Unit Mix total. Matches the BCPA record. |
| 7.0% broker cap rate | Assumptions!C8 (shown at Summary!B18) | 0.07 | Input (broker-stated) |
| 5.86% in-place cap | Returns!B29 (shown at Summary!B19) | 0.058589 | Formula: Day-0 NOI with reassessed tax / price. Verified. |
| 3.0% assumable debt | Assumptions!C125 | 0.03 | Input (listing) |
| $13.8M ask | Assumptions!C7 | 13,800,000 | Input (listing) |
| 5.7% levered IRR | 'Returns (Assumed)'!B83 (shown at Summary!B29) | 0.057284 (5.73%) | Formula. Verified. |
| 8% LP IRR | Assumptions!C168 | 0.08 | Input (preferred return) |
| $13.37M maximum bid | Summary!B58 | 13,368,909 | Solver output from `price_solve.py`, not a formula. |

**How the $13.37M bid was checked.** A copy of the workbook with Assumptions!C7 set to 13,368,909 recalculates to Waterfall!B40 (LP IRR) = 0.0800 (8.00%), and `verify_model.py` ties that copy out in full.
