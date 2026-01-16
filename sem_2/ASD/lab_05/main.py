def bm(text, pattern):
    p = [0 for _ in range(26)]

    l = set()
    for el in pattern:
        l.add(ord(el) - 97)

    for i in range(26):
        if i not in l:
            p[i] = len(pattern)
        else:
            for j in range(len(pattern) - 1, -1, -1):
                if pattern[j] == chr(i + 97):
                    p[i] = j + 1
                    break

    l1 = [-1 for _ in range(len(pattern))]
    l2 = [0 for _ in range(len(pattern))]

    for i in range(1, len(pattern)):
        suffix = pattern[i + 1:]
        for j in range(len(pattern) - len(suffix) - 1):
            if pattern[j:j+len(suffix)] == suffix and pattern[j-1] != pattern[i]:
                l1[i] = j
                break

        if pattern[:len(suffix)] == suffix:
            l2[i] = len(suffix)

    l2[len(pattern) - 1] = len(pattern)

    k = 0
    flag = False

    while k <= (len(text) - len(pattern)) and not flag:
        flag = True
        for j in range(len(pattern) -1, -1, -1):
            if pattern[j] != text[k + j]:
                bc = p[ord(text[k + j]) - 97]

                if l1[j] != -1:
                    gs = len(pattern) - 1 - l1[j]
                else:
                    gs = len(pattern) - l2[j]

                k += max(bc, gs)
                
                flag = False
                break

    return flag

print(bm("abcd", "abcd"))  # True
print(bm("zzabcdzz", "abcd"))  # True
print(bm("abxabc", "abcd"))  # False
