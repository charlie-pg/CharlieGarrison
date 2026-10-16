
# Lab 13 — Portfolio Mandate Defense

## S1–S10: Statement Classification

S1 — Hard constraint: Sets a 7-year investment horizon and annual rebalancing schedule.

S2 — Objective: The foundation wants to earn 4% above inflation annually after costs over five-year periods.

S3 — Hard constraint: The foundation needs enough cash or government securities to cover a full year of payouts.

S4 — Preference: The foundation uses a 60% stock and 40% bond benchmark to compare how well the portfolio performs.

S5 — Hard constraint: The foundation can't borrow money, short stocks, or use derivatives.

S6 — Hard constraint: No single company can make up more than 8% of the portfolio.

S7 — Hard constraint: The foundation can't trade more than 25% of its portfolio each year unless the committee approves it.

S8 — Hard constraint: At least 90% of the portfolio needs to be accessible within five business days.

S9 — Unverifiable promise: The foundation wants to avoid losing more than 10% in a year, but there's no way to guarantee that.

S10 — Missing: The foundation hasn't decided what it wants the portfolio to focus on when optimizing.

## Python Checker Results

The minimum reserve requirement is 3% of the portfolio.

- Candidate A: Passes every checkable rule.
- Candidate B: Fails 3 rules.
- Candidate C: Fails 1 rule.
- Candidate D: Passes every checkable rule.

I also tested Candidate A with -2% cash and 64% global equities. The checker correctly failed the long-only rule while the reserve remained at 10%. I then restored the original inputs.

## Candidate D — Portfolio Challenge

Candidate D passes every rule because it's 100% cash, but I don't think it's a good investment choice for the foundation. It probably wouldn't earn enough to meet the CPI + 4% return goal in S2.

## Question for the CIO

Question: Should the portfolio focus more on maximizing returns or minimizing risk?

If returns are the priority, I would invest more in stocks. If minimizing risk is more important, I would focus more on bonds and cash.

## Investment Policy Statement (IPS)

An Investment Policy Statement is a document that sets out an investor's goals and the rules for managing their portfolio. It helps guide investment decisions and gives the manager a way to evaluate whether the portfolio is following the client's requirements.

For Meridian Foundation, S2 establishes the return objective. S1 and S3–S8 establish the investment horizon, liquidity needs, benchmark, and investment restrictions. S9 needs clarification because a maximum annual loss cannot be guaranteed. S10 identifies a missing decision about what the portfolio should optimize.

## Reflection

### 1. Why can a portfolio pass every check but still be wrong?

A portfolio can follow all the rules but still not make enough money to reach the client's goals.

### 2. Which S1–S10 statement was most confusing?

S9 was the most confusing to me because it sounds like a strict rule, but you can't guarantee that a portfolio won't lose more than 10% in a year.

## Project 2 — Initial Client Mandate

Client: A 25-year-old investor saving for retirement.

Objective: Grow investments over the next 30 years to build wealth for retirement.

Hard constraints:
- No borrowing or short selling.
- Keep at least 5% in cash.
- Don't invest more than 10% in one company.

Question for the client: How much risk are you comfortable taking to earn higher returns?