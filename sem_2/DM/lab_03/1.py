s = "location"

def encode(b, control_bits = [1, 2, 4, 8, 16, 32]):
    b = list(b)

    for c in control_bits:
        b = b[:c - 1] + ["0"] + b[c - 1:]

    for c in control_bits:
        i = c - 1 
        count = 0

        while i < len(b):
            for j in range(i, min(i + c, len(b))):
                if b[j] == "1": count += 1

            i += c + 1

        if count % 2 != 0: b[c - 1] = "1"

    return b


def decode(b, control_bits = [1, 2, 4, 8, 16, 32]):
    m = []
    for c in control_bits:
        i = c - 1 
        count = 0

        while i < len(b):
            for j in range(i, min(i + c, len(b))):
                if b[j] == "1": count += 1

            i += c + 1

        if count % 2 != 0 and  b[c - 1] != "1": m.append(c)

    mistake = sum(m)

    b[mistake - 1] = "0" if b[mistake - 1] == "1" else "0"

    for i in range(len(control_bits) - 1, -1, -1):
        b.pop(control_bits[i] - 1)

    answ = ""

    for i in range(0, len(b), 8):
        byte_str = b[i:i + 8]

        if len(byte_str) == 8:
            num = int("".join(byte_str), 2)
            answ += chr(num)

    return answ

b1 = ""
b2 = ""

b1 += format(ord(s[0]), '08b')
b1 += format(ord(s[1]), '08b')
b1 += format(ord(s[2]), '08b')
b1 += format(ord(s[3]), '08b')

b2 += format(ord(s[4]), '08b')
b2 += format(ord(s[5]), '08b')
b2 += format(ord(s[6]), '08b')
b2 += format(ord(s[7]), '08b')


print(b1)
b1 = encode(b1)
b2 = encode(b2)

print("".join(b1))

b1[6] = "0" if b1[6] == "1" else "0"
b1[16] = "0" if b1[16] == "1" else "0"

b1 = decode(b1)
b2 = decode(b2)

print(b1 + b2)