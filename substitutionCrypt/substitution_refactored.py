from string import ascii_letters, punctuation
from random import sample
from typing import Dict


def generate_substitution_key(alphabet: str) -> Dict[str, str]:
    """
    Генерирует случайный ключ (биекцию) для подстановочного шифра.
    """
    shuffled = ''.join(sample(alphabet, len(alphabet)))
    return dict(zip(alphabet, shuffled))


def invert_key(key: Dict[str, str]) -> Dict[str, str]:
    """
    Строит обратный ключ для расшифровки.
    """
    return {v: k for k, v in key.items()}


def encrypt(plaintext: str, substitution_key: Dict[str, str]) -> str:
    """
    Шифрование подстановкой.
    """
    return ''.join(substitution_key[ch] for ch in plaintext)


def decrypt(ciphertext: str, substitution_key: Dict[str, str]) -> str:
    """
    Дешифрование подстановкой (через обратный ключ).
    """
    inverse_key = invert_key(substitution_key)
    return ''.join(inverse_key[ch] for ch in ciphertext)


def main() -> int:
    alphabet: str = ascii_letters + punctuation + " "
    key = generate_substitution_key(alphabet)

    plaintext: str = "Adirt Ka"
    ciphertext: str = encrypt(plaintext, key)
    decrypted: str = decrypt(ciphertext, key)

    print(f"{plaintext=}")
    print(f"{ciphertext=}")
    print(f"{decrypted=}")

    return 0


if __name__ == "__main__":
    main()
