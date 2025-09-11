ALPHABET_LENGTH: int = 128  # используем первые 128 символов ASCII


def _shift_text(text: str, shift: int, modulus: int = ALPHABET_LENGTH) -> str:
    """
    Сдвигает все символы строки text на shift по модулю modulus.
    Положительный shift = шифрование, отрицательный = расшифрование.
    """
    codes = [(ord(ch) + shift) % modulus for ch in text]
    return "".join(map(chr, codes))


def encrypt(plaintext: str, shift: int) -> str:
    """
    Шифрование Цезаря.
    plaintext -> ciphertext
    """
    return _shift_text(plaintext, shift)


def decrypt(ciphertext: str, shift: int) -> str:
    """
    Дешифрование Цезаря.
    ciphertext -> plaintext
    """
    return _shift_text(ciphertext, -shift)


def main() -> int:
    shift: int = 3
    plaintext: str = "Adirtka"

    ciphertext: str = encrypt(plaintext, shift)
    decrypted: str = decrypt(ciphertext, shift)

    print(f"{plaintext=}")
    print(f"{ciphertext=}")
    print(f"{decrypted=}")
    return 0


if __name__ == "__main__":
    main()
