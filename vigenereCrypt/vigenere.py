ALPHABET_LENGTH: int = 1_114_111


def pad_text(text: str, key_len: int) -> tuple[str, int]:
    letters_to_add: int = key_len - (len(text) % key_len)
    if letters_to_add != key_len:
        text = text + " " * letters_to_add
    return text, letters_to_add % key_len


def break_apart(text: str, key_len: int) -> list[str]:
    parts: list[str] = [text[i: i + key_len] for i in range(0, len(text), key_len)]
    return parts


def crypt_core_part(part: str, crypt_key: str, is_decrypt: bool = False) -> str:
    encrypted_part: str = ""
    for idx, letter in enumerate(part):
        encrypted_part += chr((ord(letter) + (-1) ** is_decrypt * ord(crypt_key[idx])) % ALPHABET_LENGTH)

    return encrypted_part

def encrypt(plaintext: str, encrypt_key: str) -> str:
    plaintext, _ = pad_text(plaintext, len(encrypt_key))
    plain_parts: list[str] = break_apart(plaintext, len(encrypt_key))
    ciphertext: str = "".join(map(lambda x: crypt_core_part(x, encrypt_key), plain_parts))

    return ciphertext


def decrypt(ciphertext: str, encrypt_key: str) -> str:
    ciphertext, _ = pad_text(ciphertext, len(encrypt_key))
    cipher_parts: list[str] = break_apart(ciphertext, len(encrypt_key))
    plaintext: str = "".join(map(lambda x: crypt_core_part(x, encrypt_key, True), cipher_parts))
    return plaintext


def main() -> int:
    key: str = "AdirtKa"
    plaintext: str = "Adirtka"
    encrypted_text: str = encrypt(plaintext, key)
    decrypted_text: str = decrypt(encrypted_text, key)
    print(f"{plaintext=}")
    print(f"{encrypted_text=}")
    print(f"{decrypted_text=}")
    return 0


if __name__ == "__main__":
    main()