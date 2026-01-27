word = "АБРАКАДАБРА"
n = len(word)

words = set()

for i in range(n):
    for j in range(n):
        if i == j: continue
        for k in range(n):
            if k == i or k == j: continue
            for l in range(n):
                if l == k or l == j or l == i: continue
                words.add(f'{word[i]}{word[j]}{word[k]}{word[l]}')\

print(len(words))