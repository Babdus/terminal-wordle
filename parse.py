import re

with open('Frequency_Dictionary_GE_363_202.txt', 'r') as f:
    lines = f.readlines()

words_by_length = {}

pattern = re.compile("^([ა-ჰ]+)+$")

for line in lines:
    word = line.strip().split()[0]

    if not pattern.match(word):
        continue

    if len(word) in words_by_length:
        words_by_length[len(word)].append(word)
    else:
        words_by_length[len(word)] = [word]

for n in words_by_length:
    with open(f'words_{n}.txt', 'w') as f:
        for word in words_by_length[n]:
            f.write(f'{word}\n')
