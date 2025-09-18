START_RUN_SIZE = 2

def nearest_fib(n):
    fib = [1, 1]
    while fib[-1] < n:
        fib.append(fib[-1] + fib[-2])

    return fib[-2]

def external_merge_sort(filename):
    with open(filename, "r", encoding="utf-8") as f:
        n = int(f.readline().strip())
        k = nearest_fib(n)

        for i in range(k):
            arr = list(map(int, f.readline().split()))
            arr.sort()

            with open("f1.txt", "a", encoding="utf-8") as file_1:
                file_1.write(" ".join(map(str, arr)) + " ")

        for i in range(n - k):
            arr = list(map(int, f.readline().split()))
            arr.sort()

            with open("f2.txt", "a", encoding="utf-8") as file_2:
                file_2.write(" ".join(map(str, arr)) + " ")

        files = ["f1.txt", "f2.txt", "f3.txt"]
        am_of_runs = [k, n - k, 0]
        size_of_runs = [START_RUN_SIZE, START_RUN_SIZE, 0]

        while sum(am_of_runs) != 1:
            files, am_of_runs, size_of_runs = zip(
                *sorted(zip(files, am_of_runs, size_of_runs), key=lambda x: x[1])
            )

            files = list(files)
            am_of_runs = list(am_of_runs)
            size_of_runs = list(size_of_runs)

            with open(files[2], "r", encoding="utf-8") as in1:
                with open(files[1], "r", encoding="utf-8") as in2:
                    i



arr = external_merge_sort("input.txt")

# with open("output.txt", "w", encoding="utf-8") as f:
#     f.write(" ".join(map(str, arr)))
