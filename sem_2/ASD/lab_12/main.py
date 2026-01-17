c = [1, 2, 5]
v = [4, 5, 6]

def bp(c, v, w_m):
    dp = [[0] * (w_m + 1) for _ in range(len(c))]

    for w in range(v[0], w_m + 1):
        dp[0][w] = c[0]

    for i in range(1, len(c)):
        for w in range(w_m + 1):
            if w >= v[i]:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-v[i]] + c[i])
            else:
                dp[i][w] = dp[i-1][w]

    return dp[-1][-1]

print(bp(c, v, 8))