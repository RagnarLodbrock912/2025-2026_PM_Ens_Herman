def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def next_prime(n):
    if n <= 2:
        return 2
    prime = n
    if prime % 2 == 0:
        prime += 1
    while not is_prime(prime):
        prime += 2
    return prime

def fnv1a_hash(key, table_size):
    fnv_prime = 16777619
    hash_value = 2166136261

    key = str(key)
    
    for char in key:
        hash_value ^= ord(char)
        hash_value *= fnv_prime
        hash_value &= 0xFFFFFFFF

    return hash_value % table_size

words = list()

with open("input.txt", 'r', encoding="utf-8") as f:
    words = [word for line in f for word in line.split()]

table_size = next_prime(int(len(words) * 0.7))
hash_table = [[] for _ in range(table_size)]

for word in words:
    ind = fnv1a_hash(word, table_size)

    if word not in hash_table[ind]:
        hash_table[ind].append(word)

with open("output.txt", "w", encoding="utf-8") as f:
    for chain in hash_table:
        f.write(", ".join(chain) + "\n")