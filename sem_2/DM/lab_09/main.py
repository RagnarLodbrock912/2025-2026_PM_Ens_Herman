from collections import defaultdict, deque

g = [(4, 13), (3, 10), (10, 13), (8, 12), (10, 16), (9,13), (2, 13), (10, 15), (8, 14), (5, 6), (4, 6), (4, 12), (2,7),
    (7, 9), (10, 14), (10, 12), (8, 16), (4, 15), (9, 15), (3, 5), (4, 7), (5, 15), (3, 9), (10, 11), (5, 11), (2, 11),
    (7, 10), (2, 15), (2,14), (4, 14), (7, 8), (3, 8), (5, 16), (2, 12), (5, 7)]

    
adj = defaultdict(list)
capacity = defaultdict(lambda: defaultdict(int))

n = 17
source = 2

for el in g:
    a, b = el
    adj[a].append(b)
    adj[b].append(a)
    capacity[a][b] = 1

bad_edges = set()

q = deque()
q.append(source)

parent = {v: None for v in range(n)}
visited = {v: 0 for v in range(n)}

visited[source] = 1

while len(q) > 0:
    u = q.popleft()

    color = visited[u] if visited[u] != 0 else 1

    visited[u] = color

    for v in adj[u]:
        if visited[v] == 0:
            visited[v] = 2 if color == 1 else 1
            parent[v] = u
            q.append(v)
        if visited[v] == color:
            if u < v:
                bad_edges.add((u, v))
            else:
                bad_edges.add((v, u))

print(bad_edges)

Left = {v for v in visited if visited[v] == 1}
Right = {v for v in visited if visited[v] == 2}

print("Left:", Left)
print("Right:", Right)

S = 0
T = 17

edges = []

for u in Left:
    edges.append((S, u, 1))

for u, v in g:
    if u in Left and v in Right:
        edges.append((u, v, 1))
    elif v in Left and u in Right:
        edges.append((v, u, 1))

for v in Right:
    edges.append((v, T, 1))

def bfs(residual, source, sink, nodes):
    parent = {v: None for v in nodes}
    visited = {v: False for v in nodes}

    q = deque([source])
    visited[source] = True

    while q:
        u = q.popleft()
        for v in residual[u]:
            if not visited[v] and residual[u][v] > 0:
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

def build_residual(capacity, flow):
    residual = defaultdict(lambda: defaultdict(int))

    for u in capacity:
        for v in capacity[u]:
            residual[u][v] = capacity[u][v] - flow[u][v]
            residual[v][u] += flow[u][v]

    return residual

def bottleneck(path, residual):
    return min(residual[path[i]][path[i + 1]] for i in range(len(path) - 1))

def ford_fulkerson(edges, source, sink):
    capacity = defaultdict(lambda: defaultdict(int))
    flow = defaultdict(lambda: defaultdict(int))
    adj = defaultdict(list)

    for u, v, cap in edges:
        adj[u].append(v)
        adj[v].append(u)
        capacity[u][v] += cap
        flow[u][v] = 0

    nodes = set()
    for u, v, _ in edges:
        nodes.add(u)
        nodes.add(v)

    residual = build_residual(capacity, flow)
    path = bfs(residual, source, sink, nodes)

    while path:
        b = bottleneck(path, residual)

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            flow[u][v] += b
            flow[v][u] -= b

        residual = build_residual(capacity, flow)
        path = bfs(residual, source, sink, nodes)

    max_flow = sum(flow[source][v] for v in flow[source])

    return max_flow, flow

max_flow, flow = ford_fulkerson(edges, S, T)

print("Maximum matching size:", max_flow)


matching1 = []

for u in Left:
    for v in flow[u]:
        if v in Right and flow[u][v] > 0:
            matching1.append((u, v))

print("\nMatching edges (Ford-Fulkerson):")
print("Matching edges:", matching1)


match = {}

def dfs(u, used):
    for v in adj[u]:
        if v in used:
            continue
        used.add(v)

        if v not in match or dfs(match[v], used):
            match[v] = u
            return True

    return False

for u in Left:
    used = set()
    dfs(u, used)

matching2 = []
for v in match:
    matching2.append((match[v], v))

print("Matching size:", len(matching2))
print("\nMatching edges (Kuhn):")
print("Matching:", matching2)


"""
1) Какой граф называется двудольным?

Двудольным называется граф, вершины которого можно разбить на
два непересекающихся множества (доли) так, что каждое ребро
соединяет вершины из разных множеств.
Рёбер внутри одной доли нет.

------------------------------------------------------------

2) Дайте определение паросочетания.

Паросочетание — это множество рёбер графа, в котором никакие
два ребра не имеют общей вершины.
То есть каждая вершина используется не более одного раза.

------------------------------------------------------------

3) Алгоритмы поиска паросочетаний:

1. Алгоритм Куна
   - работает через поиск увеличивающих цепей (DFS)
   - применяется только для двудольных графов
   - сложность: O(V * E)

2. Алгоритм Хопкрофта–Карпа
   - также для двудольных графов
   - использует BFS + DFS
   - сложность: O(√V * E)

3. Алгоритм максимального потока (Ford–Fulkerson)
   - универсальный алгоритм
   - сводит задачу к поиску максимального потока
   - сложность зависит от реализации

Сравнение:
- Кун: простой, но медленнее
- Хопкрофт-Карп: быстрее
- Ford-Fulkerson: универсальный, но сложнее
"""

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edges_from(g)

node_colors = []
for v in G.nodes():
    if v in Left:
        node_colors.append("lightblue")
    else:
        node_colors.append("lightgreen")

pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(10, 8))

nx.draw_networkx_edges(G, pos, alpha=0.3)

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800)

nx.draw_networkx_labels(G, pos)

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=matching2,
    width=3,
    edge_color="red"
)

plt.title("Bipartite Graph + Maximum Matching")
plt.axis("off")
plt.show()