def kpm(text, pattern):
    pi = [0 for _ in range(len(pattern))]
    k = 0

    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k

    s = 0
    for el in text:
        while s > 0 and pattern[s] != el:
            s = pi[s - 1]
        if pattern[s] == el:
            s += 1
        if s == len(pattern):
            return True

    return False

print(kpm("abcd", "abcd"))  # True
print(kpm("zzabcdzz", "abcd"))  # True
print(kpm("abxabc", "abcd"))  # False