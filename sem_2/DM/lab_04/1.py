from collections import Counter
filename = 'text.txt'
try:
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
except FileNotFoundError:
    print(f'файл не найден')
    
    
lower_text = text.lower()

if len(lower_text) % 2 != 0: 
    lower_text += '\0'

char_counts = Counter(lower_text)
total_chars = len(lower_text)

print(char_counts)

for char, count in sorted(char_counts.items(), key=lambda x: (-x[1], x[0])):
    print (f' Колическтво одного символа {char}: {count}')

pairs_letters = {}
for i in range(0, total_chars - 2):
    pair = lower_text[i] + lower_text[i + 1]
    if pair in pairs_letters:
        pairs_letters[pair] += 1
    else:
        pairs_letters[pair] = 1
for pair, count in pairs_letters.items():
    print(f"Пары'{pair}': {count}")