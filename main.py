#!/usr/bin/env python3

import os
import sys
import tty
import termios
import random
import time

alphabet = ['ა', 'ბ', 'გ', 'დ', 'ე', 'ვ', 'ზ', 'თ', 'ი', 'კ', 'ლ', 'მ', 'ნ', 'ო', 'პ', 'ჟ', 'რ', 'ს', 'ტ', 'უ', 'ფ',
            'ქ', 'ღ', 'ყ', 'შ', 'ჩ', 'ც', 'ძ', 'წ', 'ჭ', 'ხ', 'ჯ', 'ჰ']


black = '39;49'
green = '30;42'
yellow = '30;103'
gray = '30;47'
red = '37;101'

file_path = os.path.realpath(__file__)
dir_path = os.path.dirname(file_path)


def draw_row(row):
    for cell in row:
        print('┌───┐', end='')
    print()
    for cell in row:
        print(f'│\033[{cell["color"]}m {cell["char"]} \033[0m│', end='')
    print()
    for cell in row:
        print('└───┘', end='')
    print()


def draw_used_letters(used_letters):
    for i, char in enumerate(alphabet):
        if i % 11 == 0:
            print('  ', end='')
        print(f'\033[{used_letters[char]}m{char}\033[0m', end=' ')
        if i % 11 == 10:
            print()


def draw(matrix, used_letters):
    for row in matrix:
        draw_row(row)
    draw_used_letters(used_letters)


def clear(lines=24):
    print(f'\x1b[{lines}A', end='')


def read_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())

    ch = sys.stdin.read(1)

    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def check_for_win(y, matrix, length):
    green_count = 0
    for x in range(length):
        if matrix[y][x]['color'] == green:
            green_count += 1

    if green_count == length:
        win()


def lose(word):
    print(f'სიტყვა იყო \033[{green}m{word}\033[0m')
    exit()


def win():
    print('გ ი ლ ო ც ა ვ ! ! !')
    exit()


def escape(x, y, matrix, used_letters, char, word, length, words):
    confirm = input('Are you sure you want to quit? ["\033[4my\033[0m", "n"]')
    if confirm == 'n' or confirm == 'ნ':
        clear(1)
        return x, y
    lose(word)


def backspace(x, y, matrix, used_letters, char, word, length, words):
    if x > 0:
        x -= 1
        matrix[y][x] = {'char': ' ', 'color': black}
    return x, y


def determine_matches(y, matrix, used_letters, word, length, words):
    entry = ''.join([cell['char'] for cell in matrix[y]])

    # check word in dictionary
    if entry not in words:
        return False

    not_green_word = [char for char in word]

    # Check for green letters
    for x in range(length):
        char = matrix[y][x]['char']
        if char == word[x]:
            matrix[y][x]['color'] = green
            used_letters[char] = green
            not_green_word[x] = ''

    not_green_word = [char for char in not_green_word if char != '']

    # Check for yellow letters
    for x in range(length):
        char = matrix[y][x]['char']
        if matrix[y][x]['color'] != green and char in not_green_word:
            matrix[y][x]['color'] = yellow
            if used_letters[char] != green:
                used_letters[char] = yellow
            not_green_word[not_green_word.index(char)] = ''

    # Check for gray letters
    for x in range(length):
        char = matrix[y][x]['char']
        if used_letters[char] not in {yellow, green}:
            used_letters[char] = gray
    return True


def twinkle(y, matrix, used_letters, length):
    for x in range(length):
        matrix[y][x]['color'] = red
    clear()
    draw(matrix, used_letters)
    time.sleep(0.5)
    for x in range(length):
        matrix[y][x]['color'] = black
    clear()
    draw(matrix, used_letters)
    time.sleep(0.25)
    for x in range(length):
        matrix[y][x]['color'] = red
    clear()
    draw(matrix, used_letters)
    time.sleep(0.25)
    for x in range(length):
        matrix[y][x]['char'] = ' '
        matrix[y][x]['color'] = black


def enter(x, y, matrix, used_letters, char, word, length, words):
    if x == length:
        if determine_matches(y, matrix, used_letters, word, length, words):
            y += 1
        else:
            twinkle(y, matrix, used_letters, length)
        x = 0
    return x, y


def insert(x, y, matrix, used_letters, char, word, length, words):
    if x < length:
        matrix[y][x] = {'char': char, 'color': black}
        x += 1
    return x, y


def invalid_character(x, y, matrix, used_letters, char, word, length, words):
    # matrix[y][x] = {'char': char, 'color': '37;41'}
    return x, y


def determine_action(char):
    if char == '\x03' or char == '\x1b':
        return escape
    if char == '\x7f':
        return backspace
    if char == '\r' or char == '\n':
        return enter
    if char in alphabet:
        return insert
    return invalid_character


def read_words(length):
    with open(f'{dir_path}/words_{length}.txt', 'r') as f:
        words = []
        for i in range(15000):
            words.append(f.readline().strip())
    return words


def main(args):
    tries = 7
    length = 5 if len(args) == 0 else int(args[0])
    words = read_words(length)
    word = random.choice(words[:1000])

    matrix = [[{'char': ' ', 'color': black} for _ in range(length)] for _ in range(tries)]
    used_letters = {char: black for char in alphabet}

    draw(matrix, used_letters)

    x, y = 0, 0
    while True:
        if y == tries:
            lose(word)
        char = read_char()
        action = determine_action(char)
        x, y = action(x, y, matrix, used_letters, char, word, length, words)

        clear()
        draw(matrix, used_letters)
        check_for_win(y - 1, matrix, length)


if __name__ == '__main__':
    main(sys.argv[1:])
