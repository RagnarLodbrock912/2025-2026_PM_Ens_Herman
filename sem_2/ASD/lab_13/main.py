w = [2, 8 ,3, 4, 5, 3, 5]

def bf(w, m):
    b = [[]]
    b_r = [m]

    for j, el in enumerate(w):
        if el > m:
            return "Impossible"
        
        min_r = float("inf")
        min_r_ind = 0

        for i, r in enumerate(b_r):
            if r <= min_r and r >= el:
                min_r = r
                min_r_ind = i

        if min_r != float("inf"):
            b[min_r_ind].append(j)
            b_r[min_r_ind] -= el
        else:
            b.append([j])
            b_r.append(m - el)

    return b

print(bf(w, 10))