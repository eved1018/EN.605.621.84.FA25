def min_cost_bf(S, r, c):
    n = len(S)
    sched = []

    if n == 0:
        return 0, []

    if n == 1:
        # sched.append("A")
        return S[0] * r, ["A"]

    if n < 4:
        # sched.append("A")
        ca, sa = min_cost_bf(S[1:], r, c)
        cost = (S[0] * r) + ca
        sched = sa
        sched.append("A")

    else:
        ca, sa = min_cost_bf(S[1:], r, c)
        costA = (S[0] * r) + ca

        cb, sb = min_cost_bf(S[4:], r, c)
        costB = (4 * c) + cb

        if costA < costB:
            cost = costA
            sched = sa
            sched.append("A")

        else:
            cost = costB
            sched = sb
            sched.extend("BBBB")

    return cost, sched


def min_cost_dp(S, r, c):
    n = len(S)

    DP = [0] * (n)
    choice = [0] * (n)
    i = 1
    DP[0] = S[0] * r
    choice[0] = "cA"
    while i < n:
        if i < 3:
            DP[i] = DP[i - 1] + S[i] * r
            choice[i] = "cA"
        else:
            cA = DP[i - 1] + S[i] * r
            cB = DP[i - 4] + 4 * c
            if cA < cB:
                choice[i] = "cA"
            else:
                choice[i] = "cB"

            DP[i] = min(cA, cB)
        i += 1

    # i = n
    # schedule = [None] * n
    #
    # while i > 0:
    #     if choice[i] == 'cA':
    #         schedule[i - 1] = 'A'   # Convert to 0-indexed
    #         i -= 1
    #     elif choice[i] == 'cB':
    #         # Mark 4 weeks as Company B
    #         for j in range(i - 4, i):
    #             schedule[j] = 'B'
    #         i -= 4
    # print(schedule)

    return DP[n - 1], DP, choice


S = [11, 9, 9, 12, 11, 12, 12, 9, 9, 11]
r = 1
c = 10

print("DP")
cost, dp, choice = min_cost_dp(S, r, c)
print(cost)
print(dp)
print(choice)


print("\nBF")
cost, sched = min_cost_bf(S, r, c)
print(cost)
print(sched)
