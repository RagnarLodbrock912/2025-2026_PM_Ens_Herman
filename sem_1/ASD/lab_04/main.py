def comb_sort(arr, k = 1.25):
    is_swapped = False
    gap = len(arr)

    while gap > 1 or is_swapped:
        is_swapped = False

        if gap > 1:
            gap = max(1, int(gap / k))

        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                is_swapped = True

    return arr

with open("input.txt", "r", encoding="utf-8") as f:
    n = int(f.readline().strip())
    arr = list(map(int, f.readline().split()))

arr = comb_sort(arr)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(" ".join(map(str, arr)))
