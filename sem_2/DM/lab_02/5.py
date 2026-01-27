m = 17
n = 19

# 1st case
dp = [[0] * (n + 1) for _ in range(m + 1)]

dp[1][1] = 2

for i in range(2, n + 1):
    dp[1][i] = dp[1][i - 1] + 1

for i in range(2, m + 1):
    dp[i][1] = dp[i - 1][1] + 1

for i in range(2, m + 1):
    for j in range(2, n + 1):
        dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

print(dp[-1][-1])

#2nd case
dp = [[0] * (n + 1) for _ in range(m + 1)]

dp[1][1] = 2

for i in range(2, n + 1):
    dp[1][i] = dp[1][i - 1] + 1

dp[2][1] = 1

for i in range(2, m + 1):
    for j in range(2, n + 1):
        dp[i][j] = dp[i - 1][j - 1] + dp[i][j - 1]

print(dp[-1][-1])