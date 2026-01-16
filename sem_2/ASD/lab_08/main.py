nominals = [1, 2, 5]
sum = 6

dp = [0] * (sum + 1)
dp[0] = 1

for n in nominals:
    for x in range(n, sum + 1):
        dp[x] += dp[x - n]
    
print(dp[sum])