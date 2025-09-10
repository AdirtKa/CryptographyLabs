from pydoc import text
import string
from random import randint
import math


alphabet: str = string.ascii_lowercase
alphabet_length: int = len(alphabet)

b: int = randint(1, 42)

a = 4
while math.gcd(a, alphabet_length) != 1:
    a += 1

print(f"{a=}, {alphabet_length=}")


def encrypt(plaintext: str, a: int, b: int) -> str:
    ciphertext: str = ""
    for char in plaintext:
        if char in alphabet:
            # Apply the linear encryption formula
            new_index: int = (a * alphabet.index(char) + b) % alphabet_length
            ciphertext += alphabet[new_index]
        else:
            ciphertext += char
    return ciphertext


def decrypt(ciphertext: str, a: int, b: int) -> str:
    plaintext: str = ""
    a_inv: int = pow(a, -1, alphabet_length)  # Modular multiplicative inverse of a
    for char in ciphertext:
        if char in alphabet:
            # Apply the linear decryption formula
            old_index: int = (a_inv * (alphabet.index(char) - b)) % alphabet_length
            plaintext += alphabet[old_index]
        else:
            plaintext += char
    return plaintext


text = "heаыllo  Даня world"
encrypted = encrypt(text, a, b)
decrypted = decrypt(encrypted, a, b)
print("Original:", text)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)

print(pow(5, -1, 26))