"""
Реализация MD5 (Message Digest 5) без использования сторонних библиотек.

MD5 — популярная криптографическая хеш-функция, формирует 128-битный (16 байт) хеш.
"""

from struct import pack, unpack
from typing import Union

# ----------------------------------------
# Константы MD5
# ----------------------------------------

# инициализирующие значения (A, B, C, D)
MD5_INIT = [
    0x67452301,
    0xefcdab89,
    0x98badcfe,
    0x10325476
]

# Сдвиги для каждого раунда
MD5_SHIFTS = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]

# Таблица констант для каждого шага (sin(i+1)*2^32)
MD5_TABLE = [int(abs(__import__('math').sin(i + 1)) * (2 ** 32)) & 0xFFFFFFFF for i in range(64)]


# ----------------------------------------
# Вспомогательные функции
# ----------------------------------------

def F(x, y, z): return (x & y) | (~x & z)


def G(x, y, z): return (x & z) | (y & ~z)


def H(x, y, z): return x ^ y ^ z


def I(x, y, z): return y ^ (x | ~z)


def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


# Каждая четверть MD5 использует свою функцию и индексацию
MD5_FUNCS = [F, G, H, I]


# ----------------------------------------
# Класс реализации MD5
# ----------------------------------------

class MD5:
    def __init__(self):
        self._a, self._b, self._c, self._d = MD5_INIT[:]
        self.count = 0
        self.buffer = b""

    def update(self, data: Union[bytes, str]) -> None:
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.count += len(data) * 8
        self.buffer += data
        while len(self.buffer) >= 64:
            self._process_block(self.buffer[:64])
            self.buffer = self.buffer[64:]

    def _process_block(self, block: bytes) -> None:
        a, b, c, d = self._a, self._b, self._c, self._d
        X = list(unpack('<16I', block))
        for i in range(64):
            if 0 <= i <= 15:
                f, g = F(b, c, d), i
            elif 16 <= i <= 31:
                f, g = G(b, c, d), (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f, g = H(b, c, d), (3 * i + 5) % 16
            else:
                f, g = I(b, c, d), (7 * i) % 16

            temp = (a + f + MD5_TABLE[i] + X[g]) & 0xFFFFFFFF
            temp = left_rotate(temp, MD5_SHIFTS[i])
            a, d, c, b = d, c, b, (b + temp) & 0xFFFFFFFF

        self._a = (self._a + a) & 0xFFFFFFFF
        self._b = (self._b + b) & 0xFFFFFFFF
        self._c = (self._c + c) & 0xFFFFFFFF
        self._d = (self._d + d) & 0xFFFFFFFF

    def digest(self) -> bytes:
        buffer = self.buffer
        count = self.count

        buffer += b'\x80'
        while (len(buffer) % 64) != 56:
            buffer += b'\x00'
        buffer += pack('<Q', count)

        # сохранение текущих переменных
        a, b, c, d = self._a, self._b, self._c, self._d
        for i in range(0, len(buffer), 64):
            self._process_block(buffer[i:i + 64])

        result = pack('<4I', self._a, self._b, self._c, self._d)

        # вернуть хеш и восстановить переменные
        self._a, self._b, self._c, self._d = a, b, c, d
        return result

    def hexdigest(self) -> str:
        return self.digest().hex()


# ----------------------------------------
# Пример использования
# ----------------------------------------
if __name__ == "__main__":
    m = MD5()
    m.update("The quick brown fox jumps over the lazy dog")
    print(m.hexdigest(), end="\n\n")  # 9e107d9d372bb6826bd81d3542a419d6

    m = MD5()
    m.update("")
    print(m.hexdigest(), end="\n\n")  # d41d8cd98f00b204e9800998ecf8427e

    m = MD5()
    m.update("Даня Морозов A.K.A AdirtKa")
    print(f"MD5('Даня Морозов A.K.A AdirtKa') = {m.hexdigest()}")

    m = MD5()
    m.update("помогите")
    print(f"MD5('Даня Морозов A.K.A AdirtKa') = {m.hexdigest()}")