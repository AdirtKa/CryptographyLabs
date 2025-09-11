from string import ascii_letters
from math import gcd
import numpy as np


ALPHABET_LENGTH: int = 1_114_111

m: int = 2
key: np.ndarray = np.random.randint(low=1, high=30, size=(m, m))

def _egcd(a: int, b: int):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = _egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def _modinv(a: int, m: int) -> int:
    a %= m
    g, x, _ = _egcd(a, m)
    if g != 1:
        raise ValueError(f"no inverse for {a} mod {m}")
    return x % m

def _det_mod(A: np.ndarray, m: int) -> int:
    n = A.shape[0]
    if n == 1:
        return int(A[0, 0] % m)
    if n == 2:
        return int((A[0,0]*A[1,1] - A[0,1]*A[1,0]) % m)
    s = 0
    for j in range(n):
        # минор без 0-й строки и j-го столбца
        minor = np.delete(np.delete(A, 0, axis=0), j, axis=1)
        cofactor = ((-1) ** j) * int(A[0, j]) * _det_mod(minor, m)
        s = (s + cofactor) % m
    return s % m

def _adjugate_mod(A: np.ndarray, m: int) -> np.ndarray:
    n = A.shape[0]
    C = np.zeros_like(A, dtype=int)  # матрица кофакторов
    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(A, i, axis=0), j, axis=1)
            C[i, j] = ((-1) ** (i + j)) * _det_mod(minor, m)
    # adj = C^T (и сразу приводим по модулю)
    return (C.T % m)

def has_inv_mod_matrix(A: np.ndarray, m: int) -> bool:
    """
    Проверяет, существует ли обратная матрица по модулю m.
    Возвращает True, если gcd(det(A), m) == 1.
    """
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be a square matrix")

    detA = _det_mod(A % m, m)
    return gcd(detA, m) == 1

def inv_mod_matrix(A: np.ndarray, m: int) -> np.ndarray:
    """
    Обратная матрица A^{-1} по модулю m.
    A — квадратная np.ndarray целых чисел, предполагается обратимость по модулю m.
    """
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be a square matrix")

    A = (A % m).astype(int, copy=False)
    d = _det_mod(A, m)                 # det(A) mod m
    d_inv = _modinv(d, m)              # обратный к det(A) по модулю m
    adj = _adjugate_mod(A, m)          # adj(A) mod m
    return (d_inv * adj) % m


def pad_text(text: str, key_len: int) -> tuple[str, int]:
    letters_to_add: int = key_len - (len(text) % key_len)
    if letters_to_add != key_len:
        text = text + " " * letters_to_add
    return text, letters_to_add % key_len


def break_apart(text: str, key_len: int) -> list[str]:
    parts: list[str] = [text[i: i + key_len] for i in range(0, len(text), key_len)]
    return parts


def encrypt_part(part: str, encrypt_key: np.ndarray) -> str:
    encrypted_part: str = ""
    ord_letters: list[int] = []
    for letter in part:
        ord_letters.append(ord(letter))
    
    encrypted_letters: np.ndarray = np.dot(ord_letters, encrypt_key) % ALPHABET_LENGTH
    encrypted_part = "".join(map(chr, encrypted_letters))
    return encrypted_part


def encrypt(plaintext: str, key: np.ndarray) -> str:
    plaintext, _ = pad_text(plaintext, len(key))
    plain_parts: list[str] = break_apart(plaintext, len(key))
    cipher_parts = list(map(lambda x: encrypt_part(x, key), plain_parts))
    return "".join(cipher_parts)


def decrypt(ciphertext: str, key: np.ndarray) -> str:
    inv_key: np.ndarray = inv_mod_matrix(key, ALPHABET_LENGTH)
    plaintext: str = encrypt(ciphertext, inv_key)
    return plaintext


def main() -> int:
    plaintext: str = "Adirtka"
    encrypted_text: str = encrypt(plaintext, key)
    decrypted_text: str = decrypt(encrypted_text, key)
    print(f"{plaintext=}")
    print(f"{encrypted_text=}")
    print(f"{decrypted_text=}")
    return 0


if __name__ == "__main__":
    main()
