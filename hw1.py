"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""
from typing import List
import re


def get_text(file_path: str) -> List[str]:
    # Читаем текст из файла
    text = list()
    with open(file_path, "r") as file:
        # Читаем заголовок
        for _ in range(2):
            text += [word.replace(' ', '').strip() for word in file.readline().split('    ')]
        # Читаем основной текст
        text += file.read().split()
    return dash_remover(text)


def dash_remover(text: List[str]) -> List[str]:
    # Удаляем все тире и соединяем слова
    new_text = list()
    counter = 0
    while counter < len(text):
        if text[counter].endswith('-'):
            new_text.append(text[counter][:-1] + text[counter + 1])
            counter += 2
        else:
            new_text.append(text[counter])
            counter += 1
    return new_text


def get_longest_diverse_words(file_path: str) -> List[str]:
    ...


def get_rarest_char(file_path: str) -> str:
    ...


def count_punctuation_chars(file_path: str) -> int:
    ...


def count_non_ascii_chars(file_path: str) -> int:
    ...


def get_most_common_non_ascii_char(file_path: str) -> str:
    ...


if __name__ == '__main__':
    file_path = "data.txt"
    q1 = get_text(file_path)
    print(q1)