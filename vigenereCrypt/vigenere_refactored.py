from itertools import cycle
from typing import Tuple, Iterable

UNICODE_MODULUS: int = 1_114_111  # 0..0x10FFFF (вся плоскость Unicode)


def pad_text(text: str, block_len: int, pad_char: str = " ") -> Tuple[str, int]:
    """
    Дополняет text до кратности block_len символом pad_char.
    Возвращает (padded_text, pad_len).
    """
    if block_len <= 0:
        raise ValueError("block_len must be positive")
    r = len(text) % block_len
    pad_len = (block_len - r) % block_len
    if pad_len:
        text += pad_char * pad_len
    return text, pad_len


def key_stream(key: str) -> Iterable[int]:
    """
    Бесконечный поток кодов ключа (ord), key повторяется циклически.
    """
    return (ord(k) for k in cycle(key))


def vigenere_shift(text: str, key: str, decrypt: bool = False, modulus: int = UNICODE_MODULUS) -> str:
    """
    Универсальная функция шифрования/дешифрования 'Виженера' над Unicode-модулем.
    encrypt:  c_i = (ord(p_i) + ord(k_i)) mod M
    decrypt:  p_i = (ord(c_i) - ord(k_i)) mod M
    """
    if not key:
        raise ValueError("key must be non-empty")

    sign = -1 if decrypt else 1
    ks = key_stream(key)
    codes = ((ord(ch) + sign * next(ks)) % modulus for ch in text)
    return "".join(map(chr, codes))


def encrypt(plaintext: str, key: str) -> str:
    """
    Шифрование: повторяет ключ по длине текста, складывает коды по модулю Unicode.
    Текст не дополняется: шифруется как есть.
    """
    return vigenere_shift(plaintext, key, decrypt=False)


def decrypt(ciphertext: str, key: str) -> str:
    """
    Дешифрование: повторяет ключ по длине текста, вычитает коды по модулю Unicode.
    """
    return vigenere_shift(ciphertext, key, decrypt=True)


def main() -> int:
    key: str = "AdirtKa"
    plaintext: str = "Adirtka"

    # при желании можно паддить plaintext до кратности длине ключа:
    # plaintext, _ = pad_text(plaintext, len(key))

    ciphertext: str = encrypt(plaintext, key)
    decrypted: str = decrypt(ciphertext, key)

    print(f"{plaintext=}")
    print(f"{ciphertext=}")
    print(f"{decrypted=}")
    return 0


if __name__ == "__main__":
    main()
