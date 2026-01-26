def rk(text, pattern):
    k = 0
    flag = False

    h = text[0:0 + len(pattern)]

    while k < len(text) - len(pattern) + 1 and not flag:
        a = text[k:k + len(pattern)]
        if hash(pattern) != hash(text[k:k + len(pattern)]):
            k += 1
            continue

        flag = True

        for i in range(len(pattern)):
            if pattern[i] != text[k + i]:
                flag = False
                break
    
    return flag

print(rk("abcd", "abcd"))  # True
print(rk("zzabcdzz", "abcd"))  # True
print(rk("abxabc", "abcd"))  # False

        