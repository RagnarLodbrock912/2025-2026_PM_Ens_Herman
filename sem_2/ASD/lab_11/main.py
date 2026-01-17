g = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}

g = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0],
    3: [1],
    4: [1]
}

c = [0]
color = {}

for el in g:
    forbidden_c = []
    for e in g[el]:
        v = color.get(e)

        if v is not None:
            forbidden_c.append(v)

    for e in c:
        if e not in forbidden_c:
            color[el] = e
            break

    if  color.get(el) is None:
        color[el] = max(c) + 1
        c.append(max(c) + 1)

print(color)