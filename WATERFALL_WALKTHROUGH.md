# Waterfall Walkthrough

This walks through how Scenario A cash is split between the LP and the GP, using numbers from the workbook. There are two cases:
- the base case at the $13.8M ask, where only the first tier pays;
- a $12.0M purchase, where all three tiers pay.

Both were checked line by line with `verify_model.py`. The $12.0M case is the same model with only the purchase price changed.

## The structure

**Investor capital.** The equity at closing is split 90% LP and 10% GP co-invest. Both are one class of investor capital, treated identically, or pari passu. Every dollar that goes to "investors" is split 90/10.

**Fees.** None are modeled: no acquisition fee, asset-management fee or disposition fee. The GP's economics are its 10% share plus the promote.

**Tiers.** Each year's cash available for distribution is the Scenario A levered cash flow.

| Tier | Paid until | Split (investors / GP promote) |
|---|---|---|
| 1 | Investors have their capital back plus 8% compounded | 100 / 0 |
| 2 | Investors reach a 12% IRR | 70 / 30 |
| 3 | Everything after that | 50 / 50 |

**How the hurdles are tracked.**
- Each hurdle is a balance. It starts at the investors' capital, grows each year at the hurdle rate, and falls by what investors receive.
- When the 8% balance reaches zero, investors have earned exactly 8%. The same goes for the 12% balance.
- The workbook does this with rolling balances. `verify_model.py` checks it a different way, with a closed-form future value of the investors' full cash-flow history.

**A negative year** runs through Tier 1 as a contribution. The investors fund it 90/10, and the 8% balance grows by it.

## Case 1: base case, $13.8M ask

Investor capital is $5,095,290: LP $4,585,761, GP co-invest $509,529.

| Year | Cash available | 8% hurdle balance, end of year | Tier 1 | Tier 2/3 | LP (90%) | GP co-invest (10%) | GP promote |
|---|---|---|---|---|---|---|---|
| 0 | | 5,095,290 | | | −4,585,761 | −509,529 | |
| 1 | 451,614 | 5,051,299 | 451,614 | 0 | 406,453 | 45,161 | 0 |
| 2 | 328,301 | 5,127,102 | 328,301 | 0 | 295,471 | 32,830 | 0 |
| 3 | −38,965 | 5,576,234 | −38,965 | 0 | −35,068 | −3,896 | 0 |
| 4 | 151,876 | 5,870,457 | 151,876 | 0 | 136,688 | 15,188 | 0 |
| 5 | 5,235,467 | 1,104,627 | 5,235,467 | 0 | 4,711,920 | 523,547 | 0 |

**How to read it.**
- **Year 1.** The 8% balance grows from $5,095,290 to $5,502,913 ($5,095,290 × 1.08). Tier 1 pays out $451,614, leaving $5,051,299.
- **Year 3.** The −$38,965 is the refinance capital call. The new loan is $526,132 short of the $9,450,000 payoff, and Year-3 operating cash covers all but $38,965 of that. Investors fund the rest 90/10, and it raises the 8% balance.
- **Year 5.** All $5,235,467 goes to Tier 1, and $1,104,627 of the 8% hurdle is still unpaid. Investors never reach 8%, so Tiers 2 and 3 pay nothing.
- **Result.** LP IRR = GP IRR = deal IRR = 4.19%. Equity multiple = 1.20x for both. Promote = $0.

That equality is the test that pari passu is implemented correctly. An earlier version put the GP's co-invest behind the LP in Tier 1: the LP got 100% of Tier 1 until it had its own 8% and capital back. At a 7.89% deal IRR that produced an LP IRR of 9.82% and a GP IRR of −15.88%, which is not a standard structure.

## Case 2: $12.0M purchase (all three tiers pay)

**What changes at the lower price.**
- **Paydown at closing.** The lender's assumption test (75% of price, $9,000,000) requires a $450,000 paydown, applied to the 6.2% supplemental loan.
- **Tax.** Reassessed property tax is lower.
- **Refinance.** The lower tax means higher NOI, so the Year-4 refinance is sized at $9,250,732 against a $9,000,000 payoff. Year 3 releases cash instead of calling it.
- **Equity.** Investor capital is $3,716,040: LP $3,344,436, GP $371,604.

**Tier 1: 8% hurdle.**

| Year | Cash available | 8% balance, start × 1.08 | Tier 1 paid | 8% balance, end |
|---|---|---|---|---|
| 1 | 510,376 | 4,013,323 | 510,376 | 3,502,947 |
| 2 | 387,989 | 3,783,183 | 387,989 | 3,395,194 |
| 3 | 798,540 | 3,666,810 | 798,540 | 2,868,270 |
| 4 | 158,620 | 3,097,732 | 158,620 | 2,939,111 |
| 5 | 4,907,227 | 3,174,240 | 3,174,240 | 0 |

In Year 5, Tier 1 takes the $3,174,240 needed to bring the 8% balance to zero. That leaves $1,732,987.

**Tier 2: up to a 12% investor IRR.**
1. The 12% balance at the start of Year 5 is $3,590,541, the result of the same roll-forward at 12%.
2. It grows to $4,021,406 and is reduced by the $3,174,240 investors just received in Tier 1. That leaves $847,166 of investor cash still needed to reach 12%.
3. Investors get 70% of Tier 2, so Tier 2 must total $847,166 / 0.70 = $1,210,237.
4. That splits into $847,166 to investors and $363,071 of GP promote.

**Tier 3: 50/50.** The remaining $1,732,987 − $1,210,237 = $522,750 splits $261,375 to investors and $261,375 of GP promote.

**Year 5 by party.**

| | Amount |
|---|---|
| To investors | $3,174,240 + $847,166 + $261,375 = $4,282,781 |
| LP (90% of investor cash) | $3,854,503 |
| GP co-invest (10%) | $428,278 |
| GP promote | $363,071 + $261,375 = $624,446 |
| GP total | $1,052,724 |
| Check: LP + GP | $4,907,227, equal to cash available |

**Returns.**

| | IRR | Equity multiple |
|---|---|---|
| Deal | 15.59% | 1.82x |
| LP | 13.11% | 1.65x |
| GP (co-invest + promote) | 31.31% | 3.33x |

**What the numbers show.**
- **Why the LP lands where it does.** The LP gives up part of the return above 12% to the promote. It lands between 12% and the 15.59% deal IRR.
- **Where the GP's return comes from.** The GP's high return comes from the $624,446 promote on $371,604 of co-invest. Without the promote, the GP would earn the same 13.11% as the LP.

## Where to find it in the workbook

**Waterfall tab.** It shows each tier's balance, distribution and split by year, then the split by party, a check row (LP + GP − available cash = 0 each year), and the LP/GP IRRs and multiples.

**Assumptions tab.** The tier rates and splits are inputs there, under WATERFALL.
