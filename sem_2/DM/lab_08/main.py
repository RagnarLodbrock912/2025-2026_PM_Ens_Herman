from collections import defaultdict, deque
import random

nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

edges = [
    ("A", "B", 5),
    ("A", "C", 9),
    ("A", "I", 6),

    ("B", "C", 6),
    ("B", "I", 6),
    ("B", "G", 9),

    ("D", "C", 6),

    ("E", "D", 7),

    ("F", "E", 7),
    ("F", "C", 6),
    ("F", "D", 7),

    ("H", "C", 7),
    ("H", "G", 7),
    ("H", "F", 7),

    ("I", "H", 7),
    ("I", "C", 4),
    ("I", "G", 6),

    ("G", "D", 3),
    ("G", "F", 3),
    ("G", "E", 3)
]


def bfs(g, source, sink):
    q = deque()
    q.append(source)

    parent = {v: None for v in nodes}
    visited = {v: False for v in nodes}

    visited[source] = True

    while len(q) > 0:
        u = q.popleft()

        for v in g[u]:
            if visited[v] == False and g[u][v] > 0:
                visited[v] = True
                parent[v] = u
                q.append(v)
    
    if not visited[sink]:
        return None
    
    path = []
    cur = sink

    while cur != source:
        path.append(cur)
        cur = parent[cur]
    
    path.append(source)
    path.reverse()

    return path

def build_residual_graph(capacity, flow):
    residual = defaultdict(lambda: defaultdict(int))

    for u in capacity:
        for v in capacity[u]:
            residual[u][v] = capacity[u][v] - flow[u][v]
            residual[v][u] += flow[u][v]
    
    return residual

def bottleneck(p, residual):
    min_cap = float("inf")

    for i in range(1, len(p)):
        min_cap = min(min_cap, residual[p[i - 1]][p[i]])

    return min_cap

def ford_fulkerson(edges, source, sink):
    adj = defaultdict(list)
    capacity = defaultdict(lambda: defaultdict(int))
    flow = defaultdict(lambda: defaultdict(int))

    for u, v, cap in edges:
        adj[u].append(v)
        adj[v].append(u)
        capacity[u][v] += cap
        flow[u][v] = 0

    residual = build_residual_graph(capacity, flow)
    p = bfs(residual, source, sink)

    while p is not None:
        b = bottleneck(p, residual)

        for i in range(1, len(p)):
            flow[p[i - 1]][p[i]] += b
            flow[p[i]][p[i - 1]] -= b

        residual = build_residual_graph(capacity, flow)
        p = bfs(residual, source, sink)
    
    s = 0
    for v in flow[source]:
        s += flow[source][v]

    return s, capacity, flow

def min_cut(capacity, flow, source):
    residual = build_residual_graph(capacity, flow)

    visited = {v: False for v in nodes}
    q = deque()
    q.append(source)
    visited[source] = True

    while q:
        u = q.popleft()
        for v in residual[u]:
            if not visited[v] and residual[u][v] > 0:
                visited[v] = True
                q.append(v)

    S = [v for v in nodes if visited[v]]
    T = [v for v in nodes if not visited[v]]

    cut_edges = []
    for u in capacity:
        for v in capacity[u]:
            if visited[u] and not visited[v]:
                cut_edges.append((u, v, capacity[u][v]))

    return S, T, cut_edges

def randomize_edges(edges):
    return [(u, v, random.randint(100, 1000)) for (u, v, _) in edges]

source = "A"
sink = "C"

print(f"Sourse: {source}")
print(f"Sink: {sink}")

print("=== ORIGINAL GRAPH ===")
max_flow, capacity, flow = ford_fulkerson(edges, source, sink)

print("\nMax flow:", max_flow)

S, T, cut_edges = min_cut(capacity, flow, source)

print("S:", S)
print("T:", T)
print("Min-cut:", cut_edges)


print("\n=== RANDOM GRAPH ===")
edges_random = randomize_edges(edges)

max_flow2, capacity2, flow2 = ford_fulkerson(edges_random, source, sink)

print("Max flow:", max_flow2)

S2, T2, cut_edges2 = min_cut(capacity2, flow2, source)

print("S:", S2)
print("T:", T2)
print("Min-cut:", cut_edges2)