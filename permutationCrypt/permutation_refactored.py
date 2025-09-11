from __future__ import annotations

import os
from random import shuffle
from typing import List, Tuple


# ------------ Перестановочные утилиты ------------

def invert_permutation(key: List[int]) -> List[int]:
    """
    Построить обратный ключ перестановки.
    На позиции value будет стоять индекс исходной позиции.

    :param key: Перестановка длины n, элементы 0..n-1 без повторов
    :return: обратная перестановка
    """
    inv: List[int] = [0] * len(key)
    for i, v in enumerate(key):
        inv[v] = i
    return inv


def pad_message(message: str, block_size: int) -> Tuple[str, int]:
    """
    Дополнить сообщение пробелами до кратности длине блока.

    :param message: Исходный текст
    :param block_size: размер блока (длина ключа перестановки)
    :return: (дополненный текст, кол-во добавленных символов)
    """
    if block_size <= 0:
        raise ValueError("block_size должен быть положительным")
    rem = len(message) % block_size
    padding_len = (block_size - rem) if rem else 0
    if padding_len:
        message += " " * padding_len
    return message, padding_len


def split_into_blocks(message: str, block_size: int) -> List[str]:
    """
    Разбить текст на блоки фиксированного размера.

    :param message: Текст (обычно уже дополненный)
    :param block_size: размер блока
    :return: список блоков
    """
    return [message[i:i + block_size] for i in range(0, len(message), block_size)]


def permute_block(block: str, key: List[int]) -> str:
    """
    Применить перестановку символов в блоке.

    :param block: Строка длиной, равной длине key
    :param key: перестановка (список индексов)
    :return: переставленный блок
    """
    if len(block) != len(key):
        raise ValueError("Длина блока должна совпадать с длиной ключа")
    return "".join(block[key[i]] for i in range(len(block)))


def encrypt_message(plaintext: str, key: List[int]) -> Tuple[str, int]:
    """
    Зашифровать сообщение перестановочным шифром.

    :param plaintext: исходный текст
    :param key: ключ перестановки
    :return: (ciphertext, padding_len)
    """
    padded, padding_len = pad_message(plaintext, len(key))
    blocks = split_into_blocks(padded, len(key))
    cipher_blocks = [permute_block(b, key) for b in blocks]
    return "".join(cipher_blocks), padding_len


def decrypt_message(ciphertext: str, key: List[int]) -> str:
    """
    Расшифровать сообщение перестановочным шифром.
    (Возвращает строку как есть; если нужно убрать дополнение — отбросьте
    последние padding_len символов, полученных при шифровании.)

    :param ciphertext: зашифрованный текст
    :param key: исходный ключ перестановки
    :return: расшифрованный текст (с добавленными пробелами, если они были)
    """
    inv = invert_permutation(key)
    # используем тот же процесс, но с обратным ключом
    ciphertext, _ = pad_message(ciphertext, len(inv))
    blocks = split_into_blocks(ciphertext, len(inv))
    plain_blocks = [permute_block(b, inv) for b in blocks]
    return "".join(plain_blocks)


# ------------ Валидация/ввод ключа ------------

def is_valid_permutation(seq: List[int]) -> bool:
    """
    Проверить, что список — корректная перестановка 0..n-1.

    :param seq: Список целых
    :return: True, если это перестановка
    """
    n = len(seq)
    return sorted(seq) == list(range(n))


def read_new_key_from_stdin() -> List[int]:
    """
    Запросить у пользователя новый ключ-перестановку.
    Ожидается строка из цифр 0..n-1 (пример: 03124).

    :return: Список int — перестановка
    """
    print(
        "Введите новый ключ-перестановку одной строкой, без пробелов.\n"
        "Ключ должен содержать все числа от 0 до n-1 ровно по одному разу.\n"
        "Пример: 03124"
    )
    while True:
        s = input("> ").strip()
        if not s.isdigit():
            print("Ключ должен состоять только из цифр. Попробуйте ещё.")
            continue

        key = list(map(int, s))
        if not is_valid_permutation(key):
            print("Это не корректная перестановка 0..n-1. Проверьте повторы и пропуски.")
            continue

        return key


def print_keys(key: List[int]) -> None:
    """
    Красиво распечатать ключ (пары позиция→значение).
    """
    print("Перестановочный ключ:")
    print("позиция: ", *range(len(key)))
    print("значение:", *key)


# ------------ CLI ------------

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def main() -> int:
    key: List[int] = list(range(4))
    shuffle(key)  # случайный стартовый ключ

    last_padding: int | None = None  # можно хранить padding от последнего шифрования

    while True:
        clear_screen()
        print("Добро пожаловать в шифратор методом перестановки!")
        print("Выберите действие:")
        print("1. Посмотреть ключ")
        print("2. Изменить ключ")
        print("3. Зашифровать сообщение")
        print("4. Расшифровать сообщение")
        print("5. Выйти")

        try:
            choice = int(input("Введите номер действия: ").strip())
        except ValueError:
            print("Нужно ввести номер пункта меню. Нажмите Enter.")
            input()
            continue

        if choice == 1:
            print_keys(key)
            print("\nНажмите Enter для продолжения...")
            input()

        elif choice == 2:
            key = read_new_key_from_stdin()
            print("Ключ принят успешно. Нажмите Enter для продолжения...")
            input()

        elif choice == 3:
            msg = input("Введите сообщение для шифрования: ")
            ciphertext, padding_len = encrypt_message(msg, key)
            last_padding = padding_len
            print("Зашифрованное сообщение:")
            print(ciphertext)
            if padding_len:
                print(f"(добавлено пробелов при выравнивании: {padding_len})")
            print("\nНажмите Enter для продолжения...")
            input()

        elif choice == 4:
            ct = input("Введите зашифрованное сообщение: ")
            plaintext = decrypt_message(ct, key)
            print("Расшифрованное сообщение:")
            if last_padding:
                # Если шифровали в этом же сеансе — можем убрать точное дополнение
                print(plaintext[:-last_padding])
                print(f"(удалено добавленных пробелов: {last_padding})")
            else:
                print(plaintext)
                print("(подсказка: если при шифровании добавлялись пробелы, "
                      "их можно удалить вручную срезом)")
            print("\nНажмите Enter для продолжения...")
            input()

        elif choice == 5:
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Нажмите Enter.")
            input()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
