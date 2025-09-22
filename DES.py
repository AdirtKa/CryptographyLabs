pc1: list[int] =  [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

pc2: list[int] = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

ip: list[int] = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

pc1 = list(map(lambda x: x - 1, pc1))
pc2 = list(map(lambda x: x - 1, pc2))
ip = list(map(lambda x: x - 1, ip))

# pc2_left: list[int] = pc2[:len(pc2) // 2]
# pc2_right: list[int] = pc2[len(pc2) // 2:]


def word_to_bits(word: str) -> list[int]:
    """Преобразует строку в список битов (UTF-8)."""
    return [int(b) for byte in word.encode("utf-8") for b in f"{byte:08b}"]

def bits_to_word(bits: list[int]) -> str:
    """Обратно: список битов → строка (UTF-8)."""
    # группируем по 8 бит
    bytes_list = [int("".join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)]
    return bytes(bytes_list).decode("utf-8", errors="ignore")

def shift_bits(bits: list[int], n: int) -> list[int]:
    """Сдвиг списка битов на n позиций (циклический)."""
    n = n % len(bits)
    return bits[n:] + bits[:n]

def permute_bits(bits: list[int], order: list[int]) -> list[int]:
    """Перестановка битов по заданному порядку."""
    return [bits[i] for i in order]



plaintext: str = "botanica"
key: str = "ecliptic"

K: list[int] = word_to_bits(key)
new_K: list[int] = permute_bits(K, pc1)

C_0, D_0 = new_K[:28], new_K[28:]

shifts: list[int] = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
round_keys: list[list[int]] = []
for shift in shifts:
    C_0 = shift_bits(C_0, shift)
    D_0 = shift_bits(D_0, shift)
    round_keys.append(permute_bits(C_0 + D_0, pc2))
    

T: list[int] = word_to_bits(plaintext)
new_T: list[int] = permute_bits(T, ip)
l0: list[int] = new_T[:32]
r0: list[int] = new_T[32:]