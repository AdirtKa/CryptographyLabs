"""
DES Encryption/Decryption with PCBC Mode
Реализация алгоритма DES с режимом PCBC (Plaintext Cipher Block Chaining)
"""

import os
from typing import List

# ═════════════════════════════════════════════════════════════════════════════
# БЛОК С МАТРИЦАМИ ПЕРЕСТАНОВОК
# ═════════════════════════════════════════════════════════════════════════════

PC1: List[int] = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2: List[int] = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

IP: List[int] = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

S_BOXES: List[List[List[int]]] = [
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

P_BOX: List[int] = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

IP_INVERSE: List[int] = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Преобразование матриц в индексы от 0
P_BOX = [x - 1 for x in P_BOX]
PC1 = [x - 1 for x in PC1]
PC2 = [x - 1 for x in PC2]
IP = [x - 1 for x in IP]
IP_INVERSE = [x - 1 for x in IP_INVERSE]


# ═════════════════════════════════════════════════════════════════════════════
# УТИЛИТИ ФУНКЦИИ
# ═════════════════════════════════════════════════════════════════════════════

def clear_screen() -> None:
    """Очищает экран консоли."""
    os.system("cls" if os.name == "nt" else "clear")


def prompt_int(msg: str) -> int:
    """Безопасный ввод целого числа."""
    while True:
        s = input(msg).strip()
        try:
            return int(s)
        except ValueError:
            print("Ошибка: введите целое число.")


def get_decimal_from_first_last(bits_list: List[int]) -> int:
    """Возвращает десятичное число из первого и последнего бита."""
    first_bit = bits_list[0]
    last_bit = bits_list[-1]
    return (first_bit << 1) | last_bit


def get_decimal_from_middle(bits_list: List[int]) -> int:
    """Возвращает десятичное число из средних 4 битов списка."""
    middle_bits = bits_list[1:5]
    result = 0
    for idx, bit in enumerate(middle_bits):
        result |= bit << (len(middle_bits) - idx - 1)
    return result


def word_to_bits(data: bytes) -> List[int]:
    """Преобразует байты в список битов."""
    return [int(b) for byte in data for b in f"{byte:08b}"]


def bits_to_word(bits: List[int]) -> bytes:
    """Преобразует список битов в байты."""
    bytes_list = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
    return bytes(bytes_list)


def bytes_to_bits(data: bytes) -> str:
    """Преобразует байты в бинарную строку."""
    return ''.join(f"{byte:08b}" for byte in data)


def shift_bits(bits: List[int], n: int) -> List[int]:
    """Циклический сдвиг списка битов на n позиций."""
    n = n % len(bits)
    return bits[n:] + bits[:n]


def permute_bits(bits: List[int], order: List[int]) -> List[int]:
    """Перестановка битов по заданному порядку."""
    return [bits[i] for i in order]


def xor_bits(bits1: List[int], bits2: List[int]) -> List[int]:
    """XOR двух битовых последовательностей."""
    return [(a + b) % 2 for a, b in zip(bits1, bits2)]


def get_new_key() -> bytes:
    """Получает новый ключ от пользователя (ровно 8 байт в UTF-8)."""
    while True:
        key_str = input("Введите новый ключ (ровно 8 байт в UTF-8): ")
        key_bytes = key_str.encode("utf-8")

        if len(key_bytes) != 8:
            print(f"Ошибка: ключ должен занимать ровно 8 байт в UTF-8 (сейчас {len(key_bytes)} байт).")
            continue

        return key_bytes


def get_iv() -> bytes:
    """Получает вектор инициализации (ровно 8 байт)."""
    while True:
        iv_str = input("Введите вектор инициализации - IV (ровно 8 байт в UTF-8): ")
        iv_bytes = iv_str.encode("utf-8")

        if len(iv_bytes) != 8:
            print(f"Ошибка: IV должен занимать ровно 8 байт в UTF-8 (сейчас {len(iv_bytes)} байт).")
            continue

        return iv_bytes


# ═════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ ШИФРОВАНИЯ DES
# ═════════════════════════════════════════════════════════════════════════════

def get_round_keys(k: List[int]) -> List[List[int]]:
    """Получает раундовые ключи на основе переставленных битов начального ключа."""
    shifts: List[int] = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    c: List[int] = k[:28]
    d: List[int] = k[28:]

    round_keys: List[List[int]] = []
    for shift in shifts:
        c = shift_bits(c, shift)
        d = shift_bits(d, shift)
        round_keys.append(permute_bits(c + d, PC2))

    return round_keys


def extend(array: List[int]) -> List[int]:
    """Расширяет битовую последовательность до размерности раундового ключа."""
    tetrads: List[List[int]] = [array[i: i + 4] for i in range(0, len(array), 4)]
    extended_tetrads: List[List[int]] = []

    for i in range(len(tetrads)):
        extended_tetrad: List[int] = tetrads[i].copy()
        extended_tetrad.insert(0, tetrads[i - 1][-1])
        extended_tetrad.append(tetrads[(i + 1) % len(tetrads)][0])
        extended_tetrads.append(extended_tetrad)

    extended_array: List[int] = []
    for tetrad in extended_tetrads:
        extended_array.extend(tetrad)

    return extended_array


def make_round(left: List[int], right: List[int], round_key: List[int]) -> List[int]:
    """Проводит один раунд шифрования DES."""
    extended_right = extend(right)

    y: List[int] = xor_bits(round_key, extended_right)

    blocks: List[List[int]] = [y[i:i + 6] for i in range(0, len(y), 6)]
    bits: List[int] = []

    for i in range(len(blocks)):
        block: List[int] = blocks[i]
        b1: int = get_decimal_from_first_last(block)
        b2: int = get_decimal_from_middle(block)
        s_value: str = bin(S_BOXES[i][b1][b2])
        bits.extend([int(b) for b in s_value[2:].zfill(4)])

    permuted_bits: List[int] = permute_bits(bits, P_BOX)

    return xor_bits(left, permuted_bits)


def encrypt_block(block: bytes, key: bytes) -> bytes:
    """Шифрует ровно 8 байт (64 бита) в режиме ECB."""
    key_bits: List[int] = word_to_bits(key)
    permuted_key_bits: List[int] = permute_bits(key_bits, PC1)
    round_keys: List[List[int]] = get_round_keys(permuted_key_bits)

    word_bits: List[int] = word_to_bits(block)
    permuted_word_bits: List[int] = permute_bits(word_bits, IP)
    left: List[int] = permuted_word_bits[:32]
    right: List[int] = permuted_word_bits[32:]

    for round_key in round_keys:
        new_left: List[int] = make_round(left, right, round_key)
        left, right = right, new_left

    cipher_bits: List[int] = permute_bits(right + left, IP_INVERSE)
    return bits_to_word(cipher_bits)


def decrypt_block(block: bytes, key: bytes) -> bytes:
    """Дешифрует ровно 8 байт (64 бита) в режиме ECB."""
    key_bits: List[int] = word_to_bits(key)
    permuted_key_bits: List[int] = permute_bits(key_bits, PC1)
    round_keys: List[List[int]] = get_round_keys(permuted_key_bits)

    word_bits: List[int] = word_to_bits(block)
    permuted_word_bits: List[int] = permute_bits(word_bits, IP)
    left: List[int] = permuted_word_bits[:32]
    right: List[int] = permuted_word_bits[32:]

    for round_key in reversed(round_keys):
        new_left: List[int] = make_round(left, right, round_key)
        left, right = right, new_left

    plain_bits: List[int] = permute_bits(right + left, IP_INVERSE)
    return bits_to_word(plain_bits)


# ═════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ ШИФРОВАНИЯ PCBC (Plaintext Cipher Block Chaining)
# ═════════════════════════════════════════════════════════════════════════════

def encrypt_pcbc(data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Шифрует данные в режиме PCBC (Plaintext Cipher Block Chaining).
    
    Процесс PCBC (режим Kerberos):
    1. Разбиваем данные на блоки по 8 байт
    2. Для каждого блока:
       - XOR текущего блока с (предыдущий открытый блок XOR предыдущий зашифрованный блок)
       - Шифруем результат XOR
    3. Зашифрованный блок становится предыдущим для следующей итерации
    
    Формула шифрования:
    P[i] - открытый блок i
    C[i] - зашифрованный блок i
    IV - вектор инициализации
    
    C[i] = DES(P[i] ⊕ (P[i-1] ⊕ C[i-1]))
    
    Преимущества PCBC:
    - Детектирует ошибки/изменения в любом месте цепи
    - Зависит от открытого текста (хороший криптографический режим)
    - Изменение одного бита открытого текста меняет весь поток
    
    Args:
        data: Данные для шифрования
        key: Ключ шифрования (8 байт)
        iv: Вектор инициализации (8 байт)
    
    Returns:
        Зашифрованные данные
    """
    # Добавляем паддинг нулями
    while len(data) % 8 != 0:
        data = data + b"\x00"
    
    blocks = [data[i:i + 8] for i in range(0, len(data), 8)]
    encrypted_blocks: List[bytes] = []
    previous_plaintext = iv
    previous_ciphertext = iv

    for block in blocks:
        # XOR: current_plaintext XOR (previous_plaintext XOR previous_ciphertext)
        # Это создаёт зависимость как от открытого, так и от зашифрованного текста
        combined_xor = bytes(a ^ b for a, b in zip(previous_plaintext, previous_ciphertext))
        xored_block = bytes(a ^ b for a, b in zip(block, combined_xor))
        
        # Шифруем результат XOR
        encrypted_block = encrypt_block(xored_block, key)
        
        encrypted_blocks.append(encrypted_block)
        previous_plaintext = block
        previous_ciphertext = encrypted_block

    return b"".join(encrypted_blocks)


def decrypt_pcbc(data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Расшифровывает данные в режиме PCBC.
    
    Процесс дешифрования PCBC:
    1. Разбиваем зашифрованные данные на блоки по 8 байт
    2. Для каждого блока:
       - Расшифровываем блок
       - XOR результата с (предыдущий открытый блок XOR предыдущий зашифрованный блок)
    3. Получаем открытый текст и сохраняем для следующей итерации
    
    Формула расшифрования:
    P[i] = DES_decrypt(C[i]) ⊕ (P[i-1] ⊕ C[i-1])
    
    Args:
        data: Зашифрованные данные
        key: Ключ шифрования (8 байт)
        iv: Вектор инициализации (8 байт)
    
    Returns:
        Расшифрованные данные
    """
    blocks = [data[i:i + 8] for i in range(0, len(data), 8)]
    decrypted_blocks: List[bytes] = []
    previous_plaintext = iv
    previous_ciphertext = iv

    for block in blocks:
        # Расшифровываем блок
        decrypted_block = decrypt_block(block, key)
        
        # XOR с (предыдущий открытый XOR предыдущий зашифрованный)
        combined_xor = bytes(a ^ b for a, b in zip(previous_plaintext, previous_ciphertext))
        xored_block = bytes(a ^ b for a, b in zip(decrypted_block, combined_xor))
        
        decrypted_blocks.append(xored_block)
        previous_plaintext = xored_block
        previous_ciphertext = block

    return b"".join(decrypted_blocks)


# ═════════════════════════════════════════════════════════════════════════════
# ГЛАВНАЯ ФУНКЦИЯ И МЕНЮ
# ═════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Entry point приложения."""
    key: bytes = b"ecliptic"
    iv: bytes = b"initvect"

    while True:
        clear_screen()

        print("╔════════════════════════════════════════════════════════════════╗")
        print("║           Шифратор DES (Режим PCBC)                           ║")
        print("║    Plaintext Cipher Block Chaining (Режим Kerberos)           ║")
        print("╚════════════════════════════════════════════════════════════════╝\n")
        print("1. Посмотреть текущий ключ")
        print("2. Заменить ключ")
        print("3. Посмотреть вектор инициализации (IV)")
        print("4. Заменить IV")
        print("5. Зашифровать сообщение")
        print("6. Расшифровать сообщение")
        print("7. Выход\n")
        
        choice: str = input("Ваш выбор: ").strip()

        if choice == "1":
            print(f"\n✓ Текущий ключ: {key.decode('utf-8')}")

        elif choice == "2":
            key = get_new_key()
            print("✓ Ключ успешно заменён\n")

        elif choice == "3":
            print(f"\n✓ Текущий IV: {iv.decode('utf-8')}")

        elif choice == "4":
            iv = get_iv()
            print("✓ IV успешно заменён\n")

        elif choice == "5":
            message: str = input("\nВведите ваше сообщение: ")
            encrypted_message = encrypt_pcbc(message.encode('utf-8'), key, iv)
            print(f"\n✓ Зашифрованное сообщение (hex):\n{encrypted_message.hex()}")
            print(f"\n✓ Зашифрованное сообщение (bin):\n{bytes_to_bits(encrypted_message)}")

        elif choice == "6":
            ciphertext_hex: str = input("\nВведите зашифрованную строку (hex): ")
            try:
                ciphertext = bytes.fromhex(ciphertext_hex)
                decrypted_message = decrypt_pcbc(ciphertext, key, iv)
                print(f"\n✓ Расшифрованное сообщение:\n{decrypted_message.decode('utf-8').rstrip(chr(0))}")
            except ValueError:
                print("\n✗ Ошибка: неверный формат hex")
            except Exception as e:
                print(f"\n✗ Ошибка при расшифровке: {e}")

        elif choice == "7":
            print("\nВыход из шифратора. До свидания!")
            break

        else:
            print("\n✗ Неверный выбор")

        input("\nНажмите Enter для продолжения...")


if __name__ == '__main__':
    main()
