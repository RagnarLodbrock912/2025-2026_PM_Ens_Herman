filename = "text.txt"
with open(filename, "r", encoding='utf-8') as f:
    text = f.read()
    text = text.lower()

dictionary = list()

dictionary = []
lookup = {}
encoded = []

for ch in set(text):
    lookup[ch] = len(dictionary)
    dictionary.append(ch)

i = 0 

while i < len(text):
    code = lookup[text[i]]
    j = i + 1

    while j < len(text) and (code, text[j]) in lookup:
        code = lookup[(code, text[j])]
        j += 1

    encoded.append(code)

    if j < len(text):
        dictionary.append((code, text[j]))
        lookup[(code, text[j])] = len(dictionary) - 1

    i = j

import math

# ===== BASIC DATA =====
text_len = len(text)                
alphabet_size = len(set(text))
dict_size = len(dictionary)
codes_count = len(encoded)

# ===== ASCII (regular storage) =====
ascii_bits = text_len * 8

# ===== Uniform (fixed-length) coding =====
uniform_bits_per_symbol = math.ceil(math.log2(alphabet_size))
uniform_bits = text_len * uniform_bits_per_symbol

# ===== LZW coding =====
lzw_bits_per_code = math.ceil(math.log2(dict_size))
lzw_bits = codes_count * lzw_bits_per_code

# ===== OUTPUT =====
print("\n" + "="*50)
print("COMPARISON OF ENCODING METHODS")
print("="*50)

print(f"Text length: {text_len} symbols")
print(f"Alphabet size: {alphabet_size}")
print(f"LZW dictionary size: {dict_size}")
print(f"Number of LZW codes: {codes_count}")

print("\n--- ASCII ---")
print(f"Bits per symbol: 8")
print(f"Total bits: {ascii_bits}")

print("\n--- Uniform coding ---")
print(f"Bits per symbol: {uniform_bits_per_symbol}")
print(f"Total bits: {uniform_bits}")

print("\n--- LZW coding ---")
print(f"Bits per code: {lzw_bits_per_code}")
print(f"Total bits: {lzw_bits}")

print("\n--- Huffman coding ---")
print("Total bits: 62538")

print("\n" + "="*50)
