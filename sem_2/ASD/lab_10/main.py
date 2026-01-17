def eggs(n=100, e=2):
    dp = [[0] * (n + 1) for _ in range(e + 1)]

    for i in range(1, e + 1):
        dp[i][1] = 1

    for j in range(1, n + 1):
        dp[1][j] = j
    for i in range(2, e + 1):
        for j in range(2, n + 1):
            dp[i][j] = dp[i - 1][j - 1] + dp[i][j - 1] + 1

    for i, el in enumerate(dp[e]):
        if el >= n:
            return i

print(eggs())