import itertools

n = 21
m = 15
r = n - m

p = [1, 0, 1, 0, 1, 1, 1]

def division(a, b):
    a = a[:]
    
    for i in range(len(a) - len(b), -1, -1):
        if a[i + len(b) - 1] == 1:
            for j in range(len(b)):
                a[i + j] ^= b[j]
    
    return a[:r]

def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))

matrix = [[0]*n for _ in range(m)]

for i in range(m):
    matrix[i][i] = 1

for i in range(m):
    poly = [0]*n
    poly[r + i] = 1
    remainder = division(poly, p)
    for j in range(r):
        matrix[i][m + j] = remainder[j]

for row in matrix: print(row)

def encode(info):
    word = [0]*n
    for i in range(m):
        if info[i]:
            for j in range(n):
                word[j] ^= matrix[i][j]
    return word

codewords = []

for bits in itertools.product([0,1], repeat=m):
    word = encode(bits)
    codewords.append(word)

d_min = min(sum(c) for c in codewords if sum(c) > 0)

print("First 16 codewords:")
for i, w in enumerate(codewords[:16]):
    print(f"{i:2}: {w}")

print("\nMinimum Hamming distance d_min =", d_min)


print("Fragment of code distance table:")
for i in range(5):
    for j in range(i+1, 5):
        print(f"d(codeword {i}, codeword {j}) =", hamming_distance(codewords[i], codewords[j]))

t = (d_min - 1) // 2
s = d_min - 1

print("Guaranteed correctable errors t =", t)
print("Guaranteed detectable errors s =", s)

cw = codewords[20]

err1 = [0]*21
err1[3] = 1
received1 = [(cw[i] ^ err1[i]) for i in range(21)]

err2 = [0]*21
err2[0] = 1
err2[5] = 1
received2 = [(cw[i] ^ err2[i]) for i in range(21)]

print("Original codeword        :", cw)
print("Received with 1-bit error:", received1)
print("Received with 2-bit error:", received2)

