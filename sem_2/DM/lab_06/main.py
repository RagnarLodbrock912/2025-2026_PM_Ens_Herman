import itertools

g1 = [(0, 1), (0, 3), (0, 4), (0, 6), (1, 2), (1, 3), (1, 9), (2, 3), (2, 5), (2, 8), (3, 4), (3, 5), (3, 7), (4, 5), (4, 7), (4, 8), (5, 6), (5, 7), (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9)]
g2 = [(0, 1), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 2), (1, 3), (1, 6), (1, 7), (2, 3), (2, 5), (2, 8), (3, 7), (3, 8), (3, 9), (4, 5), (4, 6), (4, 8), (5, 6), (5, 7), (6, 9), (7, 9), (8, 9)]

g1 = {tuple(sorted(e)) for e in g1}
g2 = {tuple(sorted(e)) for e in g2}

vertices = list(range(10))

def is_isomorphism(mapping):
    mapped_edges = set()
    for u, v in g1:
        mu = mapping[u]
        mv = mapping[v]
        mapped_edges.add(tuple(sorted((mu, mv))))
    return mapped_edges == g2


count = 0

for perm in itertools.permutations(vertices):
    mapping = {i: perm[i] for i in vertices}
    if is_isomorphism(mapping):
        print("Found biection:")
        print(mapping)
        count += 1

print("Total count:", count)