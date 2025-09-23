BLOCK_SIZE: int = 16
SBOX_SIZE: int = 4
ROUNDS: int = 4


# --- S-блок ---
def s_box_permutation(bits: int, invert: bool = False) -> int:
    """
    Применение S-блока или обратного S-блока ко входному блоку.

    :param bits: Целое число, представляющее 16-битный блок данных.
    :param invert: Если True, используется обратный S-блок (для дешифрования).
    :return: Преобразованный блок (int).
    """
    s_box: dict[int, int] = {
        0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
        0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
        0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
        0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7,
    }
    if invert:
        s_box = {v: k for k, v in s_box.items()}

    out: int = 0
    for i in range(BLOCK_SIZE // SBOX_SIZE):
        nibble: int = (bits >> (SBOX_SIZE * i)) & 0xF
        out |= s_box[nibble] << (SBOX_SIZE * i)
    return out


# --- P-блок ---
def p_box_permutation(bits: int, invert: bool = False) -> int:
    """
    Применение P-блока или обратного P-блока к блоку данных.

    :param bits: Целое число, представляющее 16-битный блок данных.
    :param invert: Если True, используется обратная перестановка.
    :return: Преобразованный блок (int).
    """
    p_block: list[int] = [
        1, 5, 9, 13,
        2, 6, 10, 14,
        3, 7, 11, 15,
        4, 8, 12, 16
    ]
    p_block = [x - 1 for x in p_block]

    if invert:
        inv_p: list[int] = [0] * len(p_block)
        for i, p in enumerate(p_block):
            inv_p[p] = i
        p_block = inv_p

    out: int = 0
    for i, pos in enumerate(p_block):
        bit: int = (bits >> pos) & 1
        out |= bit << i
    return out


# --- Подключи ---
def get_round_keys(master_key: int) -> list[int]:
    """
    Генерация подключей из мастер-ключа.

    :param master_key: 32-битный мастер-ключ.
    :return: Список из 5 подключей по 16 бит.
    """
    round_keys: list[int] = []
    for r in range(ROUNDS + 1):
        shift: int = 32 - 16 - 4 * r
        rk: int = (master_key >> shift) & 0xFFFF
        round_keys.append(rk)
    return round_keys


# --- Шифрование ---
def encrypt_block(message: int, key: int) -> int:
    """
    Шифрование одного 16-битного блока.

    :param message: Исходный блок (16 бит).
    :param key: Мастер-ключ (32 бита).
    :return: Зашифрованный блок (16 бит).
    """
    round_keys = get_round_keys(key)
    w: int = message
    for i in range(ROUNDS - 1):
        w ^= round_keys[i]
        w = s_box_permutation(w)
        w = p_box_permutation(w)
    w ^= round_keys[ROUNDS - 1]
    w = s_box_permutation(w)
    w ^= round_keys[ROUNDS]
    return w


# --- Дешифрование ---
def decrypt_block(ciphertext: int, key: int) -> int:
    """
    Дешифрование одного 16-битного блока.

    :param ciphertext: Зашифрованный блок (16 бит).
    :param key: Мастер-ключ (32 бита).
    :return: Расшифрованный блок (16 бит).
    """
    round_keys = get_round_keys(key)
    w: int = ciphertext ^ round_keys[-1]
    w = s_box_permutation(w, invert=True)
    w ^= round_keys[-2]
    for i in range(ROUNDS - 2, -1, -1):
        w = p_box_permutation(w, invert=True)
        w = s_box_permutation(w, invert=True)
        w ^= round_keys[i]
    return w


# --- Работа с текстом ---
def encrypt_text(message: str, key: int) -> bytes:
    """
    Шифрование текстового сообщения.

    :param message: Строка (UTF-8).
    :param key: Мастер-ключ (32 бита).
    :return: Зашифрованное сообщение в виде bytes.
    """
    data: bytes = message.encode("utf-8")
    if len(data) % 2 == 1:  # паддинг до 2 байт
        data += b"\x00"

    ciphertext: bytes = b""
    for i in range(0, len(data), 2):
        block: int = (data[i] << 8) | data[i + 1]
        enc: int = encrypt_block(block, key)
        ciphertext += bytes([enc >> 8, enc & 0xFF])
    return ciphertext


def decrypt_text(ciphertext: bytes, key: int) -> str:
    """
    Дешифрование текстового сообщения.

    :param ciphertext: Зашифрованные данные в виде bytes.
    :param key: Мастер-ключ (32 бита).
    :return: Расшифрованная строка (UTF-8).
    """
    plaintext: bytes = b""
    for i in range(0, len(ciphertext), 2):
        block: int = (ciphertext[i] << 8) | ciphertext[i + 1]
        dec: int = decrypt_block(block, key)
        plaintext += bytes([dec >> 8, dec & 0xFF])
    return plaintext.rstrip(b"\x00").decode("utf-8")


# --- Демонстрация ---
if __name__ == "__main__":
    key: int = 0b00111010100101001101011000111111
    text: str = "Привет, мир!"

    enc: bytes = encrypt_text(text, key)
    dec: str = decrypt_text(enc, key)

    print("Оригинал :", text)
    print("Шифртекст:", enc.hex())
    print("Расшифр. :", dec)
