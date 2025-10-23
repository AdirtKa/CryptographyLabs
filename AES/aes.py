from typing import List

# AES S-box
s_box = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# Константы раундов для расширения ключа
r_con = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
]

def inv_sub_bytes(state: List[List[int]]) -> None:
    """
    Обратная замена байтов с помощью обратного S-box.

    Args:
        state: Матрица состояния 4x4 (модифицируется на месте)
    """
    inv_s_box = [0] * 256
    for i in range(256):
        inv_s_box[s_box[i]] = i
    for r in range(4):
        for c in range(4):
            state[r][c] = inv_s_box[state[r][c]]


def inv_shift_rows(state: List[List[int]]) -> None:
    """
    Обратный циклический сдвиг строк вправо.

    Args:
        state: Матрица состояния 4x4 (модифицируется на месте)
    """
    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]


def inv_mix_columns(state: List[List[int]]) -> None:
    """
    Обратное линейное преобразование столбцов состояния.

    Args:
        state: Матрица состояния 4x4 (модифицируется на месте)
    """
    for c in range(4):
        a = [state[r][c] for r in range(4)]
        state[0][c] = gmul(0x0e, a[0]) ^ gmul(0x0b, a[1]) ^ gmul(0x0d, a[2]) ^ gmul(0x09, a[3])
        state[1][c] = gmul(0x09, a[0]) ^ gmul(0x0e, a[1]) ^ gmul(0x0b, a[2]) ^ gmul(0x0d, a[3])
        state[2][c] = gmul(0x0d, a[0]) ^ gmul(0x09, a[1]) ^ gmul(0x0e, a[2]) ^ gmul(0x0b, a[3])
        state[3][c] = gmul(0x0b, a[0]) ^ gmul(0x0d, a[1]) ^ gmul(0x09, a[2]) ^ gmul(0x0e, a[3])


def aes_decrypt_block(ciphertext: bytes, key: bytes) -> bytes:
    """
    Расшифровывает один блок 16 байт с помощью AES-128.

    Args:
        ciphertext: Зашифрованный блок 16 байт.
        key: Ключ шифрования 16 байт.

    Returns:
        Расшифрованный блок 16 байт.
    """
    if len(ciphertext) != 16:
        raise ValueError("Длина зашифрованного текста должна быть 16 байт.")
    if len(key) != 16:
        raise ValueError("Длина ключа должна быть 16 байт.")

    state = bytes_to_state(ciphertext)
    expanded_key = key_expansion(key)

    add_round_key(state, expanded_key[40:44])  # Начальный раунд (последний ключ)

    for round_num in range(9, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, expanded_key[round_num * 4:(round_num + 1) * 4])
        inv_mix_columns(state)

    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, expanded_key[:4])  # Финальный раунд

    return state_to_bytes(state)


def gmul(a: int, b: int) -> int:
    """
    Выполняет умножение двух чисел в поле Галуа GF(2^8).
    
    Умножение выполняется по модулю неприводимого полинома 0x11b (x^8 + x^4 + x^3 + x + 1).
    Это основная операция для преобразования MixColumns в AES.
    
    Args:
        a: Первый операнд (0-255)
        b: Второй операнд (0-255)
    
    Returns:
        Результат умножения в GF(2^8)
    
    Example:
        >>> gmul(0x02, 0x87)
        0x15
    """
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set:
            a ^= 0x1b  # Редукция по модулю полинома
        a &= 0xFF
        b >>= 1
    return p


def key_expansion(key: bytes) -> List[List[int]]:
    """
    Расширяет 128-битный ключ в набор раундовых ключей.
    
    Для AES-128 исходный ключ 16 байт расширяется до 44 слов (176 байт = 11 * 16 байт),
    что обеспечивает по одному раундовому ключу для каждого из 10 раундов
    плюс начальный ключ.
    
    Args:
        key: Исходный ключ шифрования длиной 16 байт
    
    Returns:
        Список из 44 слов (каждое слово — список из 4 байт)
    
    Raises:
        ValueError: Если длина ключа не равна 16 байтам
    
    Example:
        >>> key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
        >>> expanded = key_expansion(key)
        >>> len(expanded)
        44
    """
    key_symbols = list(key)
    if len(key_symbols) != 16:
        raise ValueError("Длина ключа должна быть 16 байт для AES-128.")
    
    expanded_key = []
    
    # Первые 4 слова — это сам ключ
    for i in range(4):
        expanded_key.append(key_symbols[4 * i: 4 * (i + 1)])

    # Генерируем оставшиеся 40 слов
    for i in range(4, 44):
        temp = expanded_key[i - 1][:]
        if i % 4 == 0:
            # RotWord: циклический сдвиг байтов влево
            temp = temp[1:] + temp[:1]
            # SubWord: замена байтов через S-box
            temp = [s_box[b] for b in temp]
            # XOR с константой раунда
            temp[0] ^= r_con[(i // 4) - 1]
        # XOR текущего слова с предыдущим
        result_word = [expanded_key[i - 4][j] ^ temp[j] for j in range(4)]
        expanded_key.append(result_word)
    
    return expanded_key


def add_round_key(state: List[List[int]], round_key: List[List[int]]) -> None:
    """
    Добавляет (XOR) раундовый ключ к состоянию.
    
    Это единственная операция в AES, которая зависит от ключа.
    Выполняется XOR каждого байта состояния с соответствующим байтом раундового ключа.
    
    Args:
        state: Текущее состояние (матрица 4x4, модифицируется на месте)
        round_key: Раундовый ключ (4 слова по 4 байта)
    
    Note:
        Функция изменяет состояние напрямую, ничего не возвращая
    """
    for r in range(4):
        for c in range(4):
            state[r][c] ^= round_key[c][r]


def sub_bytes(state: List[List[int]]) -> None:
    """
    Выполняет нелинейную замену байтов через S-box.
    
    Каждый байт состояния заменяется на соответствующее значение из
    таблицы подстановки (S-box). Это обеспечивает нелинейность шифра.
    
    Args:
        state: Текущее состояние (матрица 4x4, модифицируется на месте)
    
    Note:
        S-box основан на взятии мультипликативного обратного в GF(2^8)
        с последующим аффинным преобразованием
    """
    for r in range(4):
        for c in range(4):
            state[r][c] = s_box[state[r][c]]


def shift_rows(state: List[List[int]]) -> None:
    """
    Выполняет циклический сдвиг строк состояния влево.
    
    Строка 0: не сдвигается
    Строка 1: сдвигается на 1 байт влево
    Строка 2: сдвигается на 2 байта влево
    Строка 3: сдвигается на 3 байта влево
    
    Это обеспечивает диффузию между столбцами.
    
    Args:
        state: Текущее состояние (матрица 4x4, модифицируется на месте)
    """
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]


def mix_columns(state: List[List[int]]) -> None:
    """
    Выполняет линейное преобразование столбцов состояния.
    
    Каждый столбец рассматривается как полином над GF(2^8) и умножается
    по модулю x^4 + 1 на фиксированный полином a(x) = 0x03*x^3 + x^2 + x + 0x02.
    Это обеспечивает диффузию внутри столбца.
    
    Args:
        state: Текущее состояние (матрица 4x4, модифицируется на месте)
    
    Note:
        Эта операция не выполняется в финальном раунде шифрования
    """
    for c in range(4):
        a = [state[r][c] for r in range(4)]
        state[0][c] = gmul(0x02, a[0]) ^ gmul(0x03, a[1]) ^ a[2] ^ a[3]
        state[1][c] = a[0] ^ gmul(0x02, a[1]) ^ gmul(0x03, a[2]) ^ a[3]
        state[2][c] = a[0] ^ a[1] ^ gmul(0x02, a[2]) ^ gmul(0x03, a[3])
        state[3][c] = gmul(0x03, a[0]) ^ a[1] ^ a[2] ^ gmul(0x02, a[3])


def bytes_to_state(block: bytes) -> List[List[int]]:
    """
    Преобразует 16-байтовый блок в матрицу состояния 4x4.
    
    Байты располагаются в матрице по столбцам (column-major order):
    block[0]  block[4]  block[8]  block[12]
    block[1]  block[5]  block[9]  block[13]
    block[2]  block[6]  block[10] block[14]
    block[3]  block[7]  block[11] block[15]
    
    Args:
        block: Входной блок данных длиной 16 байт
    
    Returns:
        Матрица состояния 4x4 (список из 4 списков по 4 элемента)
    """
    return [list(block[i:i + 4]) for i in range(0, 16, 4)]


def state_to_bytes(state: List[List[int]]) -> bytes:
    """
    Преобразует матрицу состояния 4x4 обратно в 16-байтовый блок.
    
    Обратная операция для bytes_to_state. Байты извлекаются из матрицы
    по столбцам.
    
    Args:
        state: Матрица состояния 4x4
    
    Returns:
        Блок данных длиной 16 байт
    """
    return bytes(sum(state, []))


def aes_encrypt_block(plaintext: bytes, key: bytes) -> bytes:
    """
    Шифрует один 16-байтовый блок данных алгоритмом AES-128.
    
    Выполняет полный цикл шифрования AES-128:
    1. Начальное добавление раундового ключа
    2. 9 основных раундов (SubBytes → ShiftRows → MixColumns → AddRoundKey)
    3. Финальный раунд без MixColumns (SubBytes → ShiftRows → AddRoundKey)
    
    Args:
        plaintext: Открытый текст длиной ровно 16 байт
        key: Ключ шифрования длиной ровно 16 байт
    
    Returns:
        Зашифрованный блок данных длиной 16 байт
    
    Raises:
        ValueError: Если длина plaintext или key не равна 16 байтам
    
    Example:
        >>> key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
        >>> plaintext = bytes.fromhex('3243f6a8885a308d313198a2e0370734')
        >>> ciphertext = aes_encrypt_block(plaintext, key)
        >>> ciphertext.hex()
        '3925841d02dc09fbdc118597196a0b32'
    """
    if len(plaintext) != 16:
        raise ValueError("Длина открытого текста должна быть 16 байт.")
    if len(key) != 16:
        raise ValueError("Длина ключа должна быть 16 байт.")
    
    # Преобразуем входные данные в матрицу состояния
    state = bytes_to_state(plaintext)
    
    # Расширяем ключ для всех раундов
    expanded_key = key_expansion(key)

    # Начальный раунд: только добавление ключа
    add_round_key(state, expanded_key[:4])

    # 9 основных раундов
    for round_num in range(1, 10):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, expanded_key[round_num * 4: (round_num + 1) * 4])

    # Финальный (10-й) раунд без MixColumns
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, expanded_key[40:44])

    # Преобразуем состояние обратно в байты
    return state_to_bytes(state)


# Пример использования
if __name__ == '__main__':
    # Тестовый вектор из спецификации FIPS-197
    example_key = bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
    example_plaintext = bytes.fromhex('3243f6a8885a308d313198a2e0370734')
    example_plaintext = b'ccDanyaMorozovcc'
    
    # Шифрование блока
    encrypted = aes_encrypt_block(example_plaintext, example_key)
    decrypted = aes_decrypt_block(encrypted, example_key)

    print(f'Открытый текст: {example_plaintext.hex()}')
    print(f'Ключ:           {example_key.hex()}')
    print(f'Шифртекст:      {encrypted.hex()}')
    print(f'Расшифровка      {decrypted.hex()}')
