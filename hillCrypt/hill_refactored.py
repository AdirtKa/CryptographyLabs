from math import gcd
from typing import List, Tuple
import numpy as np

# В Хилле работаем по модулю размера алфавита.
# Здесь используем всю таблицу Unicode (0..0x10FFFF).
MODULUS: int = 1_114_111  # 0x110000 - 1


# ===== Базовые числа и линейная алгебра над Z_m =====

def _egcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Расширенный алгоритм Евклида.
    Возвращает (g, x, y) такие, что a*x + b*y = g = gcd(a, b).
    """
    if b == 0:
        return a, 1, 0
    g, x1, y1 = _egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def _modinv(a: int, m: int) -> int:
    """
    Мультипликативно обратное к a по модулю m.
    Бросает ValueError, если обратного не существует.
    """
    a %= m
    g, x, _ = _egcd(a, m)
    if g != 1:
        raise ValueError(f"no inverse for {a} mod {m}")
    return x % m


def _det_mod(A: np.ndarray, m: int) -> int:
    """
    Детерминант матрицы A по модулю m.
    Небольшая рекурсивная реализация (достаточно для 2x2, 3x3).
    """
    n = A.shape[0]
    if n == 1:
        return int(A[0, 0] % m)
    if n == 2:
        return int((A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]) % m)
    s = 0
    for j in range(n):
        minor = np.delete(np.delete(A, 0, axis=0), j, axis=1)
        cofactor = ((-1) ** j) * int(A[0, j]) * _det_mod(minor, m)
        s = (s + cofactor) % m
    return s % m


def _adjugate_mod(A: np.ndarray, m: int) -> np.ndarray:
    """
    Присоединённая матрица adj(A) по модулю m:
    adj(A) = C^T, где C — матрица алгебраических дополнений.
    """
    n = A.shape[0]
    C = np.zeros_like(A, dtype=int)
    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(A, i, axis=0), j, axis=1)
            C[i, j] = ((-1) ** (i + j)) * _det_mod(minor, m)
    return (C.T % m)


def has_inv_mod_matrix(key_matrix: np.ndarray, m: int) -> bool:
    """
    Проверяет существование обратной матрицы key_matrix по модулю m.
    Условие обратимости: gcd(det(key_matrix), m) == 1.
    """
    if key_matrix.ndim != 2 or key_matrix.shape[0] != key_matrix.shape[1]:
        raise ValueError("key_matrix must be a square matrix")
    detA = _det_mod(key_matrix % m, m)
    return gcd(detA, m) == 1


def inv_mod_matrix(key_matrix: np.ndarray, m: int) -> np.ndarray:
    """
    Обратная матрица K^{-1} по модулю m.
    Предполагается, что K обратима по модулю m (проверяй отдельно).
    Формула: K^{-1} ≡ (det K)^{-1} * adj(K) (mod m).
    """
    if key_matrix.ndim != 2 or key_matrix.shape[0] != key_matrix.shape[1]:
        raise ValueError("key_matrix must be a square matrix")
    K = (key_matrix % m).astype(int, copy=False)
    d = _det_mod(K, m)
    d_inv = _modinv(d, m)
    adj = _adjugate_mod(K, m)
    return (d_inv * adj) % m


# ===== Текстовые утилиты для шифра Хилла =====

def pad_plaintext(plaintext: str, block_size: int, pad_char: str = "а") -> Tuple[str, int]:
    """
    Дополняет открытый текст до кратности размеру блока.
    Возвращает (padded_text, pad_len), где pad_len — число добавленных символов.
    """
    if block_size <= 0:
        raise ValueError("block_size must be positive")
    remainder = len(plaintext) % block_size
    pad_len = (block_size - remainder) % block_size
    if pad_len:
        plaintext = plaintext + pad_char * pad_len
    return plaintext, pad_len


def split_blocks(text: str, block_size: int) -> List[str]:
    """
    Делит строку на блоки фиксированного размера.
    Последний блок предполагается уже дополенным.
    """
    return [text[i:i + block_size] for i in range(0, len(text), block_size)]


def text_block_to_vector(block: str) -> np.ndarray:
    """
    Преобразует блок текста в вектор кодов Unicode (dtype=int64).
    """
    return np.fromiter((ord(ch) for ch in block), dtype=np.int64, count=len(block))


def vector_to_text(vec: np.ndarray) -> str:
    """
    Преобразует вектор кодов Unicode обратно в строку (каждый элемент уже приведён по модулю).
    """
    return "".join(map(chr, map(int, vec)))


# ===== Шифр Хилла =====

def hill_encrypt_block(plain_vec: np.ndarray, key_matrix: np.ndarray, m: int = MODULUS) -> np.ndarray:
    """
    Шифрует один вектор блока: c = x · K (mod m).
    plain_vec — вектор формы (n,), key_matrix — матрица (n, n).
    """
    return (plain_vec @ (key_matrix % m)) % m


def hill_decrypt_block(cipher_vec: np.ndarray, inv_key_matrix: np.ndarray, m: int = MODULUS) -> np.ndarray:
    """
    Дешифрует один вектор блока: x = c · K^{-1} (mod m).
    cipher_vec — вектор формы (n,), inv_key_matrix — матрица (n, n).
    """
    return (cipher_vec @ (inv_key_matrix % m)) % m


def hill_encrypt(plaintext: str, key_matrix: np.ndarray, modulus: int = MODULUS) -> str:
    """
    Шифрование Хилла.
    Разбивает plaintext на блоки длины n=len(K), переводит в векторы, умножает на K по модулю modulus.
    Возвращает ciphertext.
    """
    n = key_matrix.shape[0]
    if key_matrix.ndim != 2 or key_matrix.shape[1] != n:
        raise ValueError("key_matrix must be square (n x n)")
    padded, _ = pad_plaintext(plaintext, n)
    blocks = split_blocks(padded, n)

    cipher_chunks: List[str] = []
    K = (key_matrix % modulus).astype(np.int64, copy=False)
    for b in blocks:
        x = text_block_to_vector(b)  # shape: (n,)
        c = hill_encrypt_block(x, K, modulus)  # shape: (n,)
        cipher_chunks.append(vector_to_text(c))
    return "".join(cipher_chunks)


def hill_decrypt(ciphertext: str, key_matrix: np.ndarray, modulus: int = MODULUS) -> str:
    """
    Дешифрование Хилла.
    Вычисляет K^{-1} по модулю и применяет к каждому блоку.
    Возвращает plaintext (без удаления паддинга — это лучше делать снаружи, если нужно).
    """
    n = key_matrix.shape[0]
    if key_matrix.ndim != 2 or key_matrix.shape[1] != n:
        raise ValueError("key_matrix must be square (n x n)")
    if len(ciphertext) % n != 0:
        raise ValueError("ciphertext length must be a multiple of block size")

    K_inv = inv_mod_matrix(key_matrix, modulus).astype(np.int64, copy=False)
    blocks = split_blocks(ciphertext, n)

    plain_chunks: List[str] = []
    for b in blocks:
        c = text_block_to_vector(b)  # shape: (n,)
        x = hill_decrypt_block(c, K_inv, modulus)  # shape: (n,)
        plain_chunks.append(vector_to_text(x))
    return "".join(plain_chunks)


# ===== Пример использования =====

def main() -> int:
    """
    Демонстрация: шифруем и расшифровываем строку.
    Для примера берём случайный 2x2 ключ над Z_MODULUS (его обратимость не гарантируем).
    """
    rng = np.random.default_rng()
    n = 2
    key_matrix = rng.integers(low=1, high=30, size=(n, n), dtype=np.int64)

    # Если хочешь, проверь обратимость перед шифрованием:

    while not has_inv_mod_matrix(key_matrix, MODULUS):
        raise ValueError("Key matrix is not invertible modulo MODULUS")

    plaintext = "Adirtka"
    ciphertext = hill_encrypt(plaintext, key_matrix, MODULUS)
    decrypted = hill_decrypt(ciphertext, key_matrix, MODULUS)

    print(f"plaintext = {plaintext!r}")
    print(f"ciphertext = {ciphertext!r}")
    print(f"decrypted  = {decrypted!r}")
    return 0


if __name__ == "__main__":
    main()
