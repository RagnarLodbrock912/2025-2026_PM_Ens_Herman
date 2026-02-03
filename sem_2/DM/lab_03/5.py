def fraction_to_binary(x, bits=16):
    result = "0."
    for _ in range(bits):
        x *= 2
        if x >= 1:
            result += "1"
            x -= 1
        else:
            result += "0"
    return result


intervals = {
    "a": (0.00, 0.10),
    "b": (0.10, 0.20),
    "c": (0.20, 0.25),
    "d": (0.25, 0.80),
    "e": (0.80, 0.90),
    "f": (0.90, 1.00),
}

s = "aecdfb"

l = 0
r = 1

for el in s:
    d = r - l

    old_l = l
    l = l + intervals[el][0] * d
    r = old_l + intervals[el][1] * d

print(fraction_to_binary((r + l) / 2))

# Равномерное кодирование: 6 символов, ceil(log2(6))=3 бита → 6*3=18 бит
# Вероятность строки aecdfb: 0.1*0.8*0.05*0.55*0.1*0.1=0.00000275
# Арифметическое кодирование: -log2(0.00000275) ≈ 18.47 бит
# Степень сжатия: 18 / 18.47 ≈ 0.97