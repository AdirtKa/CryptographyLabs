import math
import os

# БЛОК С МАТРИЦАМИ ПЕРЕСТАНОВОК

pc1: list[int] = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

pc2: list[int] = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

ip: list[int] = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

s_boxes = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],

    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],

    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],

    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],

    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],

    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],

    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],

    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

p_box = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

ip_inverse = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

p_box = list(map(lambda x: x - 1, p_box))
pc1 = list(map(lambda x: x - 1, pc1))
pc2 = list(map(lambda x: x - 1, pc2))
ip = list(map(lambda x: x - 1, ip))
ip_inverse = list(map(lambda x: x - 1, ip_inverse))


# УТИЛИТИ ФУНКЦИИ

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def prompt_int(msg: str) -> int:
    """Безопасный ввод целого числа."""
    while True:
        s = input(msg).strip()
        try:
            return int(s)
        except ValueError:
            print("Ошибка: введите целое число.")


def get_decimal_from_first_last(bits_list):
    """
    Возвращает десятичное число, составленное из первого и последнего бита списка.
    """
    first_bit = bits_list[0]
    last_bit = bits_list[-1]
    binary_string = str(first_bit) + str(last_bit)
    return int(binary_string, 2)


def get_decimal_from_middle(bits_list):
    """
    Возвращает десятичное число, составленное из средних 4 битов списка.
    Предполагается, что список имеет длину 6 элементов.
    """
    middle_bits = bits_list[1:5]  # Индексы 1, 2, 3, 4
    binary_string = ''.join(str(bit) for bit in middle_bits)
    return int(binary_string, 2)


def word_to_bits(word: str, encoding: str = "latin-1") -> list[int]:
    """Преобразует строку в список битов (использует указанную кодировку)."""
    return [int(b) for byte in word.encode(encoding) for b in f"{byte:08b}"]


def bits_to_word(bits: list[int], encoding: str = "latin-1") -> str:
    """Обратно: список битов → строка (использует указанную кодировку)."""
    bytes_list = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
    return bytes(bytes_list).decode(encoding, errors="ignore")


def shift_bits(bits: list[int], n: int) -> list[int]:
    """Сдвиг списка битов на n позиций (циклический)."""
    n = n % len(bits)
    return bits[n:] + bits[:n]


def permute_bits(bits: list[int], order: list[int]) -> list[int]:
    """Перестановка битов по заданному порядку."""
    return [bits[i] for i in order]


def get_new_key() -> str:
    """Получает новый ключ от пользователя."""

    while True:
        key = input("Введите новый ключ: ")

        if len(key) != 8:
            print("Длина ключа должна равняться 8")
            continue

        return key

    return "secretAd"


# ФУНКЦИИ ШИФРОВАНИЯ

def get_round_keys(k: list[int]) -> list[list[int]]:
    """Функция получения раундовых ключей на основе переставленных битов начального ключа"""
    shifts: list[int] = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    c: list[int] = k[:28]
    d: list[int] = k[28:]

    round_keys: list[list[int]] = []
    for shift in shifts:
        c = shift_bits(c, shift)
        d = shift_bits(d, shift)
        round_keys.append(permute_bits(c + d, pc2))

    return round_keys


def extend(array: list[int]) -> list[int]:
    """Расширяет битовую последовательность до соответствия размерности раундовому ключу"""
    tetrads: list[list[int]] = [array[i: i + 4] for i in range(0, len(array), 4)]
    extended_tetrads: list[list[int]] = []

    for i in range(len(tetrads)):
        extended_tetrad: list[int] = tetrads[i].copy()
        extended_tetrad.insert(0, tetrads[i - 1][-1])
        extended_tetrad.append(tetrads[(i + 1) % len(tetrads)][0])
        extended_tetrads.append(extended_tetrad)

    extended_array: list[int] = []
    for tetrad in extended_tetrads:
        extended_array.extend(tetrad)

    return extended_array


def make_round(left, right, round_key):
    """Проводит один раунд шифрования"""
    extended_right = extend(right)

    y: list[int] = [(a + b) % 2 for a, b in zip(round_key, extended_right)]

    blocks: list[list[int]] = [y[i:i + 6] for i in range(0, len(y), 6)]
    bits: list[int] = []

    for i in range(len(blocks)):
        block: list[int] = blocks[i]
        b1: int = get_decimal_from_first_last(block)
        b2: int = get_decimal_from_middle(block)
        s: str = bin(s_boxes[i][b1][b2])
        bits.extend(list(map(int, s[2:].zfill(4))))

    permuted_bits: list[int] = permute_bits(bits, p_box)

    return [(a + b) % 2 for a, b in zip(left, permuted_bits)]


def encrypt(plaintext: str, key: str) -> str:
    """Основная функция зашифровки"""
    key_bits: list[int] = word_to_bits(key)
    permuted_key_bits: list[int] = permute_bits(key_bits, pc1)

    round_keys: list[list[int]] = get_round_keys(permuted_key_bits)

    word_bits: list[int] = word_to_bits(plaintext)
    permuted_word_bits: list[int] = permute_bits(word_bits, ip)
    left = permuted_word_bits[:32]
    right = permuted_word_bits[32:]
    for round_key in round_keys:
        new_left: list[int] = make_round(left, right, round_key)
        left: list[int] = right.copy()
        right: list[int] = new_left.copy()

    cipher_bits: list[int] = permute_bits(right + left, ip_inverse)

    return bits_to_word(cipher_bits)


def decrypt(ciphertext: str, key: str) -> str:
    """Основная функция расшифровки"""
    key_bits: list[int] = word_to_bits(key)
    permuted_key_bits: list[int] = permute_bits(key_bits, pc1)

    round_keys: list[list[int]] = get_round_keys(permuted_key_bits)
    word_bits: list[int] = word_to_bits(ciphertext, encoding="latin-1")
    permuted_word_bits: list[int] = permute_bits(word_bits, ip)
    left = permuted_word_bits[:32]
    right = permuted_word_bits[32:]
    for round_key in round_keys[::-1]:
        new_left: list[int] = make_round(left, right, round_key)
        left: list[int] = right.copy()
        right: list[int] = new_left.copy()

    plain_bits: list[int] = permute_bits(right + left, ip_inverse)

    return bits_to_word(plain_bits)


# ФУНКЦИИ ДЛЯ ИСПОЛЬЗОВАНИЯ

def encrypt_message(plaintext: str, key: str) -> str:
    """Шифрует сообщения любой размерности добавляя нули в начало сообщения"""
    plaintext: str = plaintext.zfill(math.ceil(len(plaintext) / 8) * 8)
    splitted_plaintext: list[str] = [plaintext[i:i + 8] for i in range(0, len(plaintext), 8)]
    return "".join(encrypt(part, key) for part in splitted_plaintext)


def decrypt_message(ciphertext: str, key: str) -> str:
    """Расшифровывает сообщения любой размерности добавляя нули в начало сообщения"""
    ciphertext: str = ciphertext.zfill(math.ceil(len(ciphertext) / 8) * 8)
    splitted_ciphertext: list[str] = [ciphertext[i:i + 8] for i in range(0, len(ciphertext), 8)]
    return "".join(decrypt(part, key) for part in splitted_ciphertext)


def main() -> None:
    """Entry point."""
    key: str = "ecliptic"

    while True:
        clear_screen()

        print("Добро пожаловать в шифратор методом DES\n"
              "Выберите ваше действие\n"
              "1. Посмотреть текущий ключ\n"
              "2. Заменить ключ\n"
              "3. Зашифровать\n"
              "4. Расшифровать")
        choice: str = input("Ваш выбор: ")
        if choice == "1":
            print(f"Текущий ключ для шифрования: {key}")
        elif choice == "2":
            key: str = get_new_key()
        elif choice == "3":
            message: str = input("Введите ваше сообщение: ")
            print(f"Зашифрованное сообщение {encrypt_message(message, key)}")
        elif choice == "4":
            ciphertext: str = input("Введите зашифрованную строку: ")
            print(f"Расшифрованное сообщение {decrypt_message(ciphertext, key)}")
        elif choice == "5":
            print("Выход из шифратора")
            break
        else:
            print("Неверный выбор")

        input("Нажмите Enter для продолжения...")


if __name__ == '__main__':
    main()
