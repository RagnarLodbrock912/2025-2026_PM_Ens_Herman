def select_sort(arr):
    usorted_ind = len(arr)

    while usorted_ind >= 2:
        n = max(arr[:usorted_ind])
        ind = arr.index(n)
        arr[ind], arr[usorted_ind - 1] = arr[usorted_ind - 1], arr[ind]
        usorted_ind -= 1

    return arr

with open("input.txt", "r", encoding="utf-8") as f:
    n = int(f.readline().strip())
    arr = list(map(int, f.readline().split()))

arr = select_sort(arr)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(" ".join(map(str, arr)))
