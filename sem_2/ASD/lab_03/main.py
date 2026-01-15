def fsm(text, pattern):
    text = text.lower()
    pattern = pattern.lower()

    table = [[0 for _ in range(26)] for _ in range(len(pattern))]

    for i in range(len(pattern)):
        for j in range(26):
            prefix = pattern[:i] + chr(j + 97)
            for k in range(len(prefix)):
                if prefix[k:] == pattern[:len(prefix[k:])]:
                    table[i][j] = len(prefix[k:])
                    break
    
    table.append([len(pattern) for _ in range(26)])

    s = 0
    for el in text:
        s = table[s][ord(el) - 97]
        if s == len(pattern):
            return True
        
    return False
        

print(fsm("abcd", "abcd"))  # True
print(fsm("zzabcdzz", "abcd"))  # True
print(fsm("abxabc", "abcd"))  # False