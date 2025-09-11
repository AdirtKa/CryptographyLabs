from ast import main
from string import ascii_letters, punctuation
from random import sample


def inv_key(key: dict[str, str]) -> dict[str, str]:
    return dict([(v, k) for k, v in key.items()])


def encrypt(plaintext: str, key: dict[str, str]) -> str:
    ciphertext: str = ""
    for letter in plaintext:
        ciphertext += key[letter]

    return ciphertext


def decrypt(ciphertext: str, key: dict[str, str]) -> str:
    inverted_key: dict[str, str] = inv_key(key)
    plaintext: str = ""
    for letter in ciphertext:
        plaintext += inverted_key[letter]

    return plaintext


def main() -> int:
    alphabet: str = ascii_letters + punctuation + " "
    shuffled_alphabet: str = ''.join(sample(alphabet,len(alphabet)))
    key: dict[str, str] = dict(zip(alphabet, shuffled_alphabet))
    
    plaintext: str = "Adirt Ka"

    encrypted_text: str = encrypt(plaintext, key)
    decrypted_text: str = decrypt(encrypted_text, key)
    print(f"{plaintext=}")
    print(f"{encrypted_text=}")
    print(f"{decrypted_text=}")

    return 0


if __name__ == "__main__":
    main()