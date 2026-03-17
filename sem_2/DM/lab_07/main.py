import copy
import heapq
import random
import math

n = [700, 2000, 6000, 15000, 30000]
INF = float("inf")

def build_graph(n):
    g = [[INF] * n for _ in range(n)]

    for i in range(n):
        g[i][i] = 0

    for i in range(6):
        for j in range(6):
            if i ==  j: continue
            g[i][j] = 1
            g[j][i] = 1

    for i in range(6, 10):
        for j in range(10, 15):
            g[i][j] = 1
            g[j][i] = 1

    g[5][6] = 1
    g[6][5] = 1

    for i in range(15, n):
        g[i - 1][i] = 1
        g[i][i - 1] = 1

        for j in range(i):
            if random.random() < 0.005:
                g[i][j] = 1
                g[j][i] = 1

    return g

def floyd_warshall(g, a, b):
    n = len(g)
    s = copy.deepcopy(g)

    p = [[None]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if g[i][j] < INF:
                p[i][j] = j

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if s[i][k] < INF and s[k][j] < INF:
                    if s[i][k] + s[k][j] < s[i][j]:
                        s[i][j] = s[i][k] + s[k][j]
                        p[i][j] = p[i][k]

    if p[a][b] is None:
        return []

    path = [a]
    while a != b:
        a = p[a][b]
        path.append(a)

    return path, s

def dijkstra(g, a, b):
    n = len(g)
    dist = [INF] * n
    p = [-1] * n

    dist[a] = 0
    pq = [(0, a)] 
    iterations = 0

    while pq:
        iterations += 1
        d, v = heapq.heappop(pq)

        if d > dist[v]:
            continue
        
        for u in range(n):
            if g[v][u] < INF:
                iterations += 1
                if dist[v] + g[v][u] < dist[u]:
                    dist[u] = dist[v] + g[v][u]
                    p[u] = v
                    heapq.heappush(pq, (dist[u], u))

    path = []

    while b != -1:
        path.append(b)
        b = p[b]

    return path[::-1], dist, iterations

def count_edges(g):
    n = len(g)
    edges = 0
    for i in range(n):
        for j in range(i + 1, n):
            if g[i][j] < float('inf'):
                edges += 1
    return edges

g = build_graph(20)
num_edges = count_edges(g)

p1, s = floyd_warshall(g, 0, 19)
p2, d, iterations = dijkstra(g, 0, 19)

for row in s: print(row)
print(p1)
print("-" * 50)
print(d)
print(p2)
print(iterations, (20 + num_edges)* math.log(20))