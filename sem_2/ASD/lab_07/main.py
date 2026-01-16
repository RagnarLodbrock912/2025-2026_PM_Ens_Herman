arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
n = len(arr)

dp = [0] * n
dp[0] = arr[0]

for i in range(1, n):
    dp[i] = max(arr[i], arr[i] + dp[i - 1])

s = max(dp)
ind = dp.index(s)

s2 = 0

while s2 < s:
    s2 += arr[ind]
    ind -= 1

print(f"Max submassive: [{ind + 1} : {dp.index(s)}]")