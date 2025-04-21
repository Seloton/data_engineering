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
    return text


def clear_text(text: List[str]) -> List[str]:
    # Удаляем все тире и соединяем слова
    new_text = list()
    counter = 0
    # Делаем через while чтобы слова не повторялись тк мы объединяя слова забираем два слова из исходного текста
    while counter < len(text):
        if text[counter].endswith('-'):
            new_text.append(text[counter][:-1] + text[counter + 1])
            counter += 2
        else:
            new_text.append(text[counter])
            counter += 1
    # Выводим текст без лишних точек
    return list(map(lambda x: x.replace('.', ''), new_text))


def get_longest_diverse_words(text: list, pattern: str) -> List[str]:
    # Находим 10 самых длинных слов с уникальными символами.
    # Находим и убираем все числа и переводим символы в нижний регистр.
    # Очищаем текст от тире и убираем точки
    text = list(map(lambda x: x.lower(), filter(lambda x: not x[0].isdigit(), clear_text(text))))
    # Выводим 10 значений развернутого отсортированного по количеству уникальных символов списка.
    # Каждый символ unicode (который состоит из 6 символов) мы находим с помощью регулярных выражений.
    # И каждый этот символ проверяем его на уникальность и считаем за 1 символ.
    return sorted(text,
                  key=lambda x: len(set(re.findall(pattern, x))) + len(set(re.sub(pattern, '', x))),
                  reverse=True)[:10]


def get_rarest_char(text: str, pattern: str) -> str:
    # Находим самый редкий символ в тексте.
    # Ищем все символы unicode и считаем их количество.
    unicode_symbols = re.findall(pattern, text)
    unicode_counter = dict()
    for i in set(unicode_symbols):
        unicode_counter[i] = unicode_symbols.count(i)
    # Убираем все символы unicode из текста тк их уже посчитали.
    text = re.sub(pattern, '', text)
    # Считаем количество каждого символа в тексте
    symbol_counter = dict()
    for i in set(text):
        symbol_counter[i] = text.count(i)
    # Объединяем два словаря с символами и их количеством
    symbol_counter.update(unicode_counter)
    # Ищем символ, который встречается меньше всего раз
    minimum = min(symbol_counter, key=symbol_counter.get)
    return f'Самый редкий символ: "{minimum}", он встречается {symbol_counter[minimum]} раз'


def count_punctuation_chars(text: str, pattern: str) -> str:
    # Убираем unicode символы.
    text = re.sub(pattern, '', text)
    # С помощью регулярных выражений ищем все символы которые не являются: буквами, цифрами и пробелами.
    return f'Количество знаков препинания: {len(re.findall(r"\W", text))}'


def count_non_ascii_chars(text: str, pattern: str) -> str:
    return f'Количество не ASCII-символ: {len(re.findall(pattern, text))}'


def get_most_common_non_ascii_char(text: str, pattern: str) -> str:
    # Оставляем только unicode символы
    unicode_symbols = re.findall(pattern, text)
    # Ищем символ с максимальным числом повторений
    maximum = max(unicode_symbols, key=lambda x: unicode_symbols.count(x))
    return f'Самый популярный не ASCII-символ: {maximum}, он встречается {unicode_symbols.count(maximum)} раз'


if __name__ == '__main__':
    # Путь до файла
    file_path = "data.txt"
    # Текст, где слова разделены друг от друга
    normal_text = get_text(file_path)
    # Переводим все слова в один сплошной текст и в один регистр.
    text = ''.join(normal_text).lower()
    # Паттерн по поиску unicode символов для регулярных выражений
    unicode_pattern = r"\\u...."

    # 1) Find 10 longest words consisting from largest amount of unique symbols
    print(get_longest_diverse_words(normal_text, unicode_pattern))
    # 2) Find rarest symbol for document
    print(get_rarest_char(text, unicode_pattern))
    # 3) Count every punctuation char
    print(count_punctuation_chars(text, unicode_pattern))
    # 4) Count every non ascii char
    print(count_non_ascii_chars(text, unicode_pattern))
    # 5) Find most common non ascii char for document
    print(get_most_common_non_ascii_char(text, unicode_pattern))
