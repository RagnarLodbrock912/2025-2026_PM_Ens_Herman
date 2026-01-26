import math

n = int(input())
dots = list()

for _ in range(n):
    x, y = map(int, input().split())
    dots.append((x,y))


def orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def dist(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def jarvis_alg(dots):
    n = len(dots)

    if n < 3:
        print("No")
        return
    
    if len(dots) == 3 and orientation(dots[0], dots[1], dots[2]) == 0:
        print("No")
        return
    
    l = min(range(n), key=lambda i: (dots[i][0], dots[i][1]))
    hull = []
    p = l
    
    while True:
        hull.append(dots[p])
        q = (p + 1) % n
        
        for i in range(n):
            o = orientation(dots[p], dots[i], dots[q])
            if o > 0 or (o == 0 and dist(dots[p], dots[i]) > dist(dots[p], dots[q])):
                q = i
        
        p = q
        
        if p == l:
            break
    
    print(hull)

jarvis_alg(dots)