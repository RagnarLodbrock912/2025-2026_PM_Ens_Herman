m = [
    [0, 2, 7, 1, 9],
    [2, 0, 3, 4, 6],
    [7, 3, 0, 2, 5],
    [1, 4, 2, 0, 8],
    [9, 6, 5, 8, 0]
]

q = {1, 3, 4}

def tcp(m, q, start=0):
    n = len(m)
    INF = 10**9

    dp = [[INF] * n for _ in range(1 << n)]
    dp[1 << start][start] = 0

    for S in range(1 << n):
        for j in range(n):
            if not (S & (1 << j)):
                continue

            S_without_j = S & ~(1 << j)

            for i in range(n):
                if S_without_j & (1 << i):
                    dp[S][j] = min(dp[S][j], dp[S_without_j][i] + m[i][j])

    S = 0
    for v in q:
        S |= (1 << v)
    S |= (1 << start)

    best_cost = float('inf')
    last = None

    for j in q:
        if j == start:
            continue
        cost = dp[S][j] + m[j][start]
        if cost < best_cost:
            best_cost = cost
            last = j

    route = [start, last]
    mask = S
    cur = last

    while cur != start:
        mask_without_cur = mask & ~(1 << cur)

        best_prev = None
        best_val = float('inf')

        for i in range(n):
            if (mask_without_cur & (1 << i)):
                val = dp[mask_without_cur][i] + m[i][cur]
                if val < best_val:
                    best_val = val
                    best_prev = i

        route.append(best_prev)
        cur = best_prev
        mask = mask_without_cur

    route.reverse()
    return route, best_cost

print(tcp(m, q))
