import math

x = int(input())

k = int(math.log(x, 3)) + 1 
l = int(math.log(x, 5)) + 1 
m = int(math.log(x, 7)) + 1 

answ = list()

for i in range(k):
    for j in range(l):
        for t in range(m):
            n = 3 ** i * 5 ** j * 7 ** t
            if n <= x:
                answ.append(n)

answ.sort()
print(answ)