from typing import Iterable

from generate_keys import generate_keys


def encrypt(plaintext: Iterable[int], publickey: tuple[int, int]) -> list[int]:
    """
    Encrypt plaintext with public key.

    :param plaintext: plaintext to encrypt
    :param publickey: public key pair e, n
    :return bytes: encrypted plaintext
    """

    e, n = publickey

    encrypted_text: list[int] = []
    for char in plaintext:
        encrypted_text.append((char ** e) % n)

    return encrypted_text


def decrypt(ciphertext: Iterable[int], private_key: tuple[int, int]) -> str:
    """
    Decrypt encrypted plaintext with private key.

    :param ciphertext: ciphertext to decrypt
    :param private_key: private key pair d, n
    :return: decrypted plaintext
    """

    d, n = private_key
    decrypted_ints = [(char ** d) % n for char in ciphertext]
    # Преобразуем каждое число в символ
    return ''.join(chr(i) for i in decrypted_ints)


def main() -> None:
    """Entry point."""
    message: bytes = b"AdirtKa"
    n, e, d = generate_keys()
    encrypted_message = encrypt(message, (e, n))
    decrypted_message = decrypt(encrypted_message, (d, n))

    print(f"{message=}")
    print(f"{encrypted_message=}")
    print(f"{decrypted_message=}")


if __name__ == '__main__':
    main()
