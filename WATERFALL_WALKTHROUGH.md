# Waterfall Walkthrough

This is how the Scenario A cash gets split between the LP and the GP, using the numbers in the workbook. Scenario A is the base case: assume the seller's debt, refinance into a floating loan with a rate cap at the December 2029 maturity, and sell at the end of Year 5. I walk through two prices. At the $13.8M ask only the first tier pays, which is the whole problem with the deal. At $12.0M all three tiers pay, which shows the structure actually working. The $12.0M case is the same model with only the purchase price changed, and I checked both line by line with `verify_model.py`.

## The structure

Equity at closing is split 90% LP and 10% GP co-invest. The two are one class of investor capital, treated identically (pari passu), so every dollar that goes to "investors" splits 90/10. I didn't model any fees: no acquisition, asset-management or disposition fee. The GP's economics are its 10% share plus the promote.

Each year's cash available for distribution is the Scenario A levered cash flow, and it runs through three tiers:

| Tier | Paid until | Split (investors / GP promote) |
|---|---|---|
| 1 | Investors have their capital back plus 8% compounded | 100 / 0 |
| 2 | Investors reach a 12% IRR | 70 / 30 |
| 3 | Everything after that | 50 / 50 |

I track each hurdle as a balance. It starts at the investors' capital, grows each year at the hurdle rate, and falls by whatever investors receive. When the 8% balance hits zero, investors have earned exactly 8%, and the same goes for 12%. A negative year, like a capital call, runs through Tier 1 as a contribution: investors fund it 90/10 and the 8% balance grows by it. The workbook uses rolling balances, and the verification script checks the same thing a different way, with a closed-form future value of the investors' whole cash-flow history.

## At the $13.8M ask

Investor capital is $5,095,290: LP $4,585,761 and GP co-invest $509,529.

| Year | Cash available | 8% hurdle balance, end of year | Tier 1 | Tier 2/3 | LP (90%) | GP co-invest (10%) | GP promote |
|---|---|---|---|---|---|---|---|
| 0 | | 5,095,290 | | | −4,585,761 | −509,529 | |
| 1 | 451,614 | 5,051,299 | 451,614 | 0 | 406,453 | 45,161 | 0 |
| 2 | 328,301 | 5,127,102 | 328,301 | 0 | 295,471 | 32,830 | 0 |
| 3 | −357,752 | 5,895,022 | −357,752 | 0 | −321,977 | −35,775 | 0 |
| 4 | 302,926 | 6,063,698 | 302,926 | 0 | 272,633 | 30,293 | 0 |
| 5 | 5,860,685 | 688,108 | 5,860,685 | 0 | 5,274,616 | 586,068 | 0 |

In Year 1 the 8% balance grows from $5,095,290 to $5,502,913 ($5,095,290 × 1.08), and the $451,614 Tier 1 payment brings it down to $5,051,299. Year 3 is the refinance. The $9,450,000 payoff is replaced with an $8,699,030 floating loan sized on the capped rate, and the cap costs $93,950, so $844,919 of cash is needed. Year-3 operations cover part of it, and investors put in the other $357,752, split 90/10, which pushes the 8% balance back up.

By Year 5 the sale proceeds aren't enough. All $5,860,685 goes to Tier 1 and $688,108 of the 8% hurdle is still unpaid, so Tiers 2 and 3 pay nothing. The LP, the GP and the deal all earn 5.73% with a 1.29x multiple, and the promote is $0.

That equality is also how I know pari passu is built correctly. My first version put the GP's co-invest behind the LP in Tier 1, so the LP took 100% of Tier 1 until it had its own capital back plus 8%. At a 7.89% deal IRR, that gave the LP 9.82% and the GP −15.88%. That isn't a structure anyone would sign.

## At a $12.0M purchase, where all three tiers pay

A few things change at the lower price. The lender's assumption test (75% of price, $9,000,000) requires a $450,000 paydown at closing, which I apply to the 6.2% supplemental loan. Reassessed property tax is lower. Higher NOI means the 2029 floating refinance comes in at $9,017,659 against a $9,000,000 payoff, so after the cap premium only $79,732 is needed, and Year-3 operations cover it with no capital call. Investor capital is $3,716,040: LP $3,344,436 and GP $371,604.

Tier 1, the 8% hurdle:

| Year | Cash available | 8% balance, start × 1.08 | Tier 1 paid | 8% balance, end |
|---|---|---|---|---|
| 1 | 510,376 | 4,013,323 | 510,376 | 3,502,947 |
| 2 | 387,989 | 3,783,183 | 387,989 | 3,395,194 |
| 3 | 468,076 | 3,666,810 | 468,076 | 3,198,734 |
| 4 | 315,203 | 3,454,633 | 315,203 | 3,139,429 |
| 5 | 5,555,345 | 3,390,583 | 3,390,583 | 0 |

In Year 5, Tier 1 takes the $3,390,583 needed to clear the 8% balance, leaving $2,164,762.

Tier 2 runs the same roll-forward at 12%. The 12% balance at the start of Year 5 is $3,804,078. It grows to $4,260,567, and the $3,390,583 investors just got in Tier 1 brings it down to $869,984. That's how much more investor cash it takes to reach 12%. Since investors get 70% of Tier 2, the tier has to total $869,984 / 0.70 = $1,242,834: $869,984 to investors and $372,850 of GP promote.

Tier 3 gets what's left, $2,164,762 − $1,242,834 = $921,928, split evenly: $460,964 to investors and $460,964 of promote.

| Year 5 | Amount |
|---|---|
| To investors | $3,390,583 + $869,984 + $460,964 = $4,721,531 |
| LP (90% of investor cash) | $4,249,378 |
| GP co-invest (10%) | $472,153 |
| GP promote | $372,850 + $460,964 = $833,814 |
| GP total | $1,305,967 |
| Check: LP + GP | $5,555,345, equal to cash available |

| | IRR | Equity multiple |
|---|---|---|
| Deal | 16.98% | 1.95x |
| LP | 13.89% | 1.72x |
| GP (co-invest + promote) | 35.61% | 3.97x |

The LP ends up between the 12% hurdle and the 16.98% deal IRR, because it gives up part of everything above 12% to the promote. The GP's 35.61% comes from the $833,814 promote on $371,604 of co-invest. Without the promote, the GP would earn the same 13.89% as the LP.

In the workbook, the Waterfall tab shows each tier's balance, distribution and split by year, the split by party, a check row (LP + GP − available cash = 0 every year), and the LP and GP IRRs and multiples. The tier rates and splits are inputs on the Assumptions tab under WATERFALL.
