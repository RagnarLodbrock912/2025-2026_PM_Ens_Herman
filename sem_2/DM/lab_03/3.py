s = "aaaaaaaaaaaaadghtttttttttttyiklooooooop"

ch = s[0]
c = 1
answ = []

for i in range(1, len(s)):
    if s[i] == ch:
        c += 1
    if s[i] != ch:
        answ.append(c)
        answ.append(ch)
        c = 1
        ch = s[i]

if s[-1] == s[-2]:
    answ.append(c + 1)
    answ.append(ch)
else:
    answ.append(1)
    answ.append(s[-1])
     
print(answ)

i = 0
res = []

while i < len(answ):
    if answ[i] != 1:
        res.append(answ[i])
        res.append(answ[i + 1])
        i += 2

    else:
        c = 0
        st = ""
        while answ[i] == 1:
            c += 1
            st += answ[i + 1]
            i += 2
            if i >= len(answ): break

        res.append(0)
        res.append(c)
        res.append(st)


print(res)

# 2 + 6 + 2 + 6 + 2 + 3 = 21 байт
# 13 + 4 + 11 + 4 + 7 + 1 = 40 символов = 40 байт
# k= 40 / 21 = 1,9
