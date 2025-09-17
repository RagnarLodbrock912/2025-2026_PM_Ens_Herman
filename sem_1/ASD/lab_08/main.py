def radix_sort(arr):
    length = len(str(max(arr)))
    rang = 10

    for i in range(length):
        new_arr = [[] for k in range(rang)]
        for el in arr:
            new_arr[el // 10**i % 10].append(el)

        arr = []
        for el in new_arr:
            arr += el

    return arr

with open("input.txt", "r", encoding="utf-8") as f:
    n = int(f.readline().strip())
    arr = list(map(int, f.readline().split()))

arr = radix_sort(arr)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(" ".join(map(str, arr)))
