"""
Реализация алгоритма SHA-1 с нуля.

SHA-1 (Secure Hash Algorithm 1) - криптографическая хеш-функция,
которая преобразует входные данные в 160-битный (20-байтный) хеш.

Структура реализации:
- Инициализирующие константы
- Вспомогательные функции
- Основной класс SHA1
"""

from struct import pack, unpack
from typing import Union

# ============================================================================
# КОНСТАНТЫ
# ============================================================================

# Начальные значения хеш-переменных (первые 32 бита дробной части корней)
INITIAL_HASH_VALUES = [
    0x67452301,
    0xEFCDAB89,
    0x98BADCFE,
    0x10325476,
    0xC3D2E1F0,
]

# Константы раундов (первые 32 бита дробной части корней кубических чисел)
ROUND_CONSTANTS = [
    0x5A827999,  # Раунды 0-19
    0x6ED9EBA1,  # Раунды 20-39
    0x8F1BBCDC,  # Раунды 40-59
    0xCA62C1D6,  # Раунды 60-79
]


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================

def left_rotate(value: int, shift: int) -> int:
    """
    Циклический сдвиг влево на 32-битном целом числе.

    Args:
        value: 32-битное целое число
        shift: Количество позиций для сдвига

    Returns:
        Результат циклического сдвига влево
    """
    value &= 0xFFFFFFFF
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF


def sha1_f(x: int, y: int, z: int, round_num: int) -> int:
    """
    Нелинейная функция SHA-1 в зависимости от номера раунда.

    Args:
        x, y, z: 32-битные входные значения
        round_num: Номер раунда (0-79)

    Returns:
        Результат функции f
    """
    if round_num < 20:
        return (x & y) | ((~x) & z)
    elif round_num < 40:
        return x ^ y ^ z
    elif round_num < 60:
        return (x & y) | (x & z) | (y & z)
    else:
        return x ^ y ^ z


def sha1_k(round_num: int) -> int:
    """
    Константа для раунда SHA-1.

    Args:
        round_num: Номер раунда (0-79)

    Returns:
        Соответствующая константа раунда
    """
    if round_num < 20:
        return ROUND_CONSTANTS[0]
    elif round_num < 40:
        return ROUND_CONSTANTS[1]
    elif round_num < 60:
        return ROUND_CONSTANTS[2]
    else:
        return ROUND_CONSTANTS[3]


# ============================================================================
# ОСНОВНОЙ КЛАСС SHA1
# ============================================================================

class SHA1:
    """
    Реализация алгоритма SHA-1.

    Использование:
        sha1 = SHA1()
        sha1.update(b"Hello, World!")
        hash_hex = sha1.hexdigest()
    """

    def __init__(self):
        """Инициализация SHA-1."""
        # Копируем начальные значения
        self.h = INITIAL_HASH_VALUES.copy()

        # Счетчик обработанных бит
        self.bit_count = 0

        # Буфер для неполного блока
        self.buffer = b""

    def update(self, data: Union[bytes, str]) -> None:
        """
        Обновить хеш-значение новыми данными.

        Args:
            data: Данные для хеширования (bytes или str)
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        self.bit_count += len(data) * 8
        self.buffer += data

        # Обработить полные блоки по 64 байта
        while len(self.buffer) >= 64:
            self._process_block(self.buffer[:64])
            self.buffer = self.buffer[64:]

    def digest(self) -> bytes:
        """
        Получить хеш-значение в виде байтов.

        Returns:
            20 байт хеш-значения
        """
        # Работаем с копией для неизменяемости
        h = self.h.copy()
        bit_count = self.bit_count
        buffer = self.buffer

        # Добавляем бит 1 после сообщения
        buffer += b'\x80'

        # Добавляем нулевые биты до 56 байт mod 64
        while (len(buffer) % 64) != 56:
            buffer += b'\x00'

        # Добавляем длину сообщения в битах (64-битное, big-endian)
        buffer += pack('>Q', bit_count)

        # Обработить оставшиеся блоки
        for i in range(0, len(buffer), 64):
            h = self._process_block_static(buffer[i:i + 64], h)

        # Упаковать хеш-значение в байты
        return b''.join(pack('>I', x) for x in h)

    def hexdigest(self) -> str:
        """
        Получить хеш-значение в шестнадцатеричном формате.

        Returns:
            Строка из 40 шестнадцатеричных символов
        """
        return self.digest().hex()

    def _process_block(self, block: bytes) -> None:
        """
        Обработить один 64-байтный блок.

        Args:
            block: 64-байтный блок данных
        """
        self.h = self._process_block_static(block, self.h)



    @staticmethod
    def _process_block_static(block: bytes, h: list) -> list:
        """
        Статический метод для обработки блока.

        Args:
            block: 64-байтный блок данных
            h: Копия хеш-значения

        Returns:
            Обновленное хеш-значение
        """
        # Разбить блок на 16 32-битных слов (big-endian)
        w = list(unpack('>16I', block))

        # Расширить на 80 слов
        for i in range(16, 80):
            w.append(left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1))

        # Инициализировать рабочие переменные
        a, b, c, d, e = h

        # Основной цикл (80 раундов)
        for i in range(80):
            f = sha1_f(b, c, d, i)
            k = sha1_k(i)

            temp = (left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp

        # Добавить результаты к исходным хеш-значениям
        h[0] = (h[0] + a) & 0xFFFFFFFF
        h[1] = (h[1] + b) & 0xFFFFFFFF
        h[2] = (h[2] + c) & 0xFFFFFFFF
        h[3] = (h[3] + d) & 0xFFFFFFFF
        h[4] = (h[4] + e) & 0xFFFFFFFF

        return h


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    # Пример 1: Простая строка
    print("Пример 1: Хеширование простой строки")
    sha1 = SHA1()
    sha1.update("помогите")
    print(f"SHA-1('Даня Морозов A.K.A AdirtKa') = {sha1.hexdigest()}")
    print()

    # Пример 2: Пустая строка
    print("Пример 2: Хеширование пустой строки")
    sha1 = SHA1()
    sha1.update("")
    print(f"SHA-1('') = {sha1.hexdigest()}")
    print()

    # Пример 3: Метод update с несколькими вызовами
    print("Пример 3: Несколько вызовов update")
    sha1 = SHA1()
    sha1.update("The quick brown ")
    sha1.update("fox jumps over ")
    sha1.update("the lazy dog")
    print(f"SHA-1('The quick brown fox jumps over the lazy dog') = {sha1.hexdigest()}")
    print()

    # Пример 4: Байтовые данные
    print("Пример 4: Хеширование байтовых данных")
    sha1 = SHA1()
    sha1.update(b"\x00\x01\x02\x03\x04\x05")
    print(f"SHA-1(b'\\x00\\x01\\x02\\x03\\x04\\x05') = {sha1.hexdigest()}")
    print()

    # Пример 5: Большие данные
    print("Пример 5: Хеширование больших данных")
    sha1 = SHA1()
    sha1.update("a" * 1000000)
    print(f"SHA-1('a' * 1000000) = {sha1.hexdigest()}")
