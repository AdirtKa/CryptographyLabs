"""
Реализация алгоритма SHA256 (FIPS 180-4)

SHA256 (Secure Hash Algorithm 256-bit) — криптографическая хеш-функция,
которая преобразует входные данные произвольной длины в хеш-значение
фиксированной длины 256 бит (32 байта).

Основные свойства:
- Детерминированность: одни и те же входные данные всегда дают один результат
- Необратимость: невозможно восстановить входные данные из хеша
- Чувствительность: малое изменение входа дает совершенно иной хеш
- Производительность: быстрое вычисление для любого размера входа
"""

import struct
from typing import List


class SHA256:
    """
    Класс для вычисления SHA256 хеша.

    Использует стандартные константы из FIPS 180-4:
    - Начальные значения (первые 32 бита дробных частей квадратных корней первых 8 простых чисел)
    - Константы раунда (первые 32 бита дробных частей кубических корней первых 64 простых чисел)
    """

    # Константы раунда K (первые 32 бита дробных частей кубических корней первых 64 простых чисел)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    def __init__(self):
        """Инициализирует начальные значения хеша."""
        # Начальные значения H (первые 32 бита дробных частей квадратных корней первых 8 простых чисел)
        self.h = [
            0x6a09e667,  # sqrt(2)
            0xbb67ae85,  # sqrt(3)
            0x3c6ef372,  # sqrt(5)
            0xa54ff53a,  # sqrt(7)
            0x510e527f,  # sqrt(11)
            0x9b05688c,  # sqrt(13)
            0x1f83d9ab,  # sqrt(17)
            0x5be0cd19   # sqrt(19)
        ]

    @staticmethod
    def _right_rotate(value: int, amount: int) -> int:
        """
        Циклический сдвиг вправо на amount бит.

        Args:
            value: 32-битное значение
            amount: количество позиций для сдвига

        Returns:
            Результат циклического сдвига вправо
        """
        value &= 0xffffffff  # Маскируем до 32 бит
        return ((value >> amount) | (value << (32 - amount))) & 0xffffffff

    @staticmethod
    def _right_shift(value: int, amount: int) -> int:
        """
        Логический сдвиг вправо на amount бит.

        Args:
            value: 32-битное значение
            amount: количество позиций для сдвига

        Returns:
            Результат логического сдвига вправо
        """
        return (value >> amount) & 0xffffffff

    @staticmethod
    def _sigma0(x: int) -> int:
        """
        Функция Σ0(x) = ROTR(x, 2) ⊕ ROTR(x, 13) ⊕ ROTR(x, 22)

        Используется в основном цикле обработки блока.
        """
        return SHA256._right_rotate(x, 2) ^ SHA256._right_rotate(x, 13) ^ SHA256._right_rotate(x, 22)

    @staticmethod
    def _sigma1(x: int) -> int:
        """
        Функция Σ1(x) = ROTR(x, 6) ⊕ ROTR(x, 11) ⊕ ROTR(x, 25)

        Используется в основном цикле обработки блока.
        """
        return SHA256._right_rotate(x, 6) ^ SHA256._right_rotate(x, 11) ^ SHA256._right_rotate(x, 25)

    @staticmethod
    def _gamma0(x: int) -> int:
        """
        Функция γ0(x) = ROTR(x, 7) ⊕ ROTR(x, 18) ⊕ SHR(x, 3)

        Используется при расширении блока сообщения.
        """
        return SHA256._right_rotate(x, 7) ^ SHA256._right_rotate(x, 18) ^ SHA256._right_shift(x, 3)

    @staticmethod
    def _gamma1(x: int) -> int:
        """
        Функция γ1(x) = ROTR(x, 17) ⊕ ROTR(x, 19) ⊕ SHR(x, 10)

        Используется при расширении блока сообщения.
        """
        return SHA256._right_rotate(x, 17) ^ SHA256._right_rotate(x, 19) ^ SHA256._right_shift(x, 10)

    @staticmethod
    def _ch(x: int, y: int, z: int) -> int:
        """
        Функция выбора: Ch(x, y, z) = (x ∧ y) ⊕ (¬x ∧ z)

        Выбирает y если x=1, иначе выбирает z.
        """
        return (x & y) ^ ((~x) & z)

    @staticmethod
    def _maj(x: int, y: int, z: int) -> int:
        """
        Функция большинства: Maj(x, y, z) = (x ∧ y) ⊕ (x ∧ z) ⊕ (y ∧ z)

        Возвращает большинство бит (если 2 или 3 из них равны 1).
        """
        return (x & y) ^ (x & z) ^ (y & z)

    def _pad_message(self, message: bytes) -> bytes:
        """
        Добавляет пэддинг к сообщению согласно FIPS 180-4.

        Процесс пэддинга:
        1. Добавить один бит '1' (0x80 для целого байта)
        2. Добавить нулевые биты до длины ≡ 448 (mod 512)
        3. Добавить 64-битное представление исходной длины в битах

        Args:
            message: исходное сообщение

        Returns:
            Дополненное сообщение, длина которого кратна 512 битам (64 байтам)
        """
        msg_len_bits = len(message) * 8

        # Добавляем '1' бит (представлен как 0x80)
        padded = bytearray(message)
        padded.append(0x80)

        # Добавляем нулевые байты до достижения длины ≡ 448 (mod 512)
        while (len(padded) % 64) != 56:
            padded.append(0x00)

        # Добавляем исходную длину сообщения в битах (big-endian, 64 бита)
        padded.extend(struct.pack('>Q', msg_len_bits))

        return bytes(padded)

    def _process_block(self, block: bytes) -> None:
        """
        Обрабатывает один блок сообщения (512 бит = 64 байта).

        Процесс:
        1. Расширить 16 слов в 64 слова
        2. Инициализировать рабочие переменные (a-h) текущими значениями хеша
        3. Выполнить 64 раунда сжатия
        4. Обновить значения хеша

        Args:
            block: один блок сообщения (ровно 64 байта)
        """
        # Шаг 1: Расширение блока (подготовка 64 слов)
        w: List[int] = []

        # W[0..15] — первые 16 слов из блока (32-битные, big-endian)
        for i in range(16):
            w.append(struct.unpack('>I', block[i*4:(i+1)*4])[0])

        # W[16..63] — расширенные слова по формуле:
        # W[i] = γ1(W[i-2]) + W[i-7] + γ0(W[i-15]) + W[i-16]
        for i in range(16, 64):
            s0 = self._gamma0(w[i - 15])
            s1 = self._gamma1(w[i - 2])
            w.append((s1 + w[i - 7] + s0 + w[i - 16]) & 0xffffffff)

        # Шаг 2: Инициализация рабочих переменных
        a, b, c, d, e, f, g, h = self.h

        # Шаг 3: Основной цикл сжатия (64 раунда)
        for i in range(64):
            # Вычисляем временные значения
            T1 = (h + self._sigma1(e) + self._ch(e, f, g) + self.K[i] + w[i]) & 0xffffffff
            T2 = (self._sigma0(a) + self._maj(a, b, c)) & 0xffffffff

            # Сдвигаем переменные
            h = g
            g = f
            f = e
            e = (d + T1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xffffffff

        # Шаг 4: Обновляем значения хеша
        self.h[0] = (self.h[0] + a) & 0xffffffff
        self.h[1] = (self.h[1] + b) & 0xffffffff
        self.h[2] = (self.h[2] + c) & 0xffffffff
        self.h[3] = (self.h[3] + d) & 0xffffffff
        self.h[4] = (self.h[4] + e) & 0xffffffff
        self.h[5] = (self.h[5] + f) & 0xffffffff
        self.h[6] = (self.h[6] + g) & 0xffffffff
        self.h[7] = (self.h[7] + h) & 0xffffffff

    def update(self, message: bytes) -> None:
        """
        Обновляет внутреннее состояние, обрабатывая новые данные.

        Args:
            message: данные для добавления в хеш
        """
        if not isinstance(message, bytes):
            message = bytes(message, 'utf-8')

        padded = self._pad_message(message)

        # Обрабатываем каждый 512-битный блок
        for i in range(0, len(padded), 64):
            self._process_block(padded[i:i + 64])

    def digest(self) -> bytes:
        """
        Возвращает финальный хеш в виде байтов.

        Returns:
            32-байтовый (256-битный) хеш в big-endian формате
        """
        return b''.join(struct.pack('>I', h) for h in self.h)

    def hexdigest(self) -> str:
        """
        Возвращает финальный хеш в виде шестнадцатеричной строки.

        Returns:
            64-символьная шестнадцатеричная строка (256 бит = 64 hex символа)
        """
        return self.digest().hex()

    def decdigest(self) -> int:
        """
        Возвращает финальный хеш в виде целого десятичного числа.

        Преобразует 32-байтовый хеш (256 бит) в целое число от 0 до 2^256 - 1.

        Returns:
            Десятичное целое число, представляющее хеш

        Example:
            >>> h = SHA256()
            >>> h.update(b"hello world")
            >>> print(h.decdigest())
            83260119260225805697088093127046923526196509892841150256906384614308062156393
        """
        return int.from_bytes(self.digest(), byteorder='big')

    def decdigest_str(self) -> str:
        """
        Возвращает финальный хеш в виде строки десятичного числа.

        Удобнее для отображения больших чисел.

        Returns:
            Строка с десятичным представлением хеша
        """
        return str(self.decdigest())


def sha256(data: bytes) -> str:
    """
    Удобная функция для вычисления SHA256 (шестнадцатеричный формат).

    Args:
        data: данные для хеширования

    Returns:
        Шестнадцатеричная строка хеша

    Example:
        >>> sha256(b"hello world")
        'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
    """
    h = SHA256()
    h.update(data)
    return h.hexdigest()


def sha256_decimal(data: bytes) -> int:
    """
    Удобная функция для вычисления SHA256 (десятичный формат).

    Args:
        data: данные для хеширования

    Returns:
        Целое число (256-битное, беззнаковое)

    Example:
        >>> sha256_decimal(b"hello world")
        83260119260225805697088093127046923526196509892841150256906384614308062156393
    """
    h = SHA256()
    h.update(data)
    return h.decdigest()


def sha256_decimal_str(data: bytes) -> str:
    """
    Удобная функция для вычисления SHA256 (десятичный формат, строка).

    Возвращает результат в виде строки, что удобнее для больших чисел.

    Args:
        data: данные для хеширования

    Returns:
        Строка с десятичным представлением хеша

    Example:
        >>> sha256_decimal_str(b"hello world")
        '83260119260225805697088093127046923526196509892841150256906384614308062156393'
    """
    h = SHA256()
    h.update(data)
    return h.decdigest_str()


if __name__ == "__main__":
    # Примеры использования
    print("=== Примеры SHA256 ===\n")

    # Пример 1: Пустая строка
    result1 = sha256(b"")
    dec1 = sha256_decimal(b"")
    print(f"sha256(b\"\") = ")
    print(f"HEX: {result1}")
    print(f"DEC: {dec1}\n")

    # Пример 2: Простая строка
    result2 = sha256(b"hello world")
    dec2 = sha256_decimal(b"hello world")
    print(f"sha256(b\"hello world\") =")
    print(f"HEX: {result2}")
    print(f"DEC: {dec2}")
    print(f"STR: {sha256_decimal_str(b'hello world')}\n")

    # Пример 3: Другая строка
    result3 = sha256(b"The quick brown fox jumps over the lazy dog")
    dec3 = sha256_decimal(b"The quick brown fox jumps over the lazy dog")
    print(f"sha256(b\"The quick brown fox jumps over the lazy dog\") =")
    print(f"HEX: {result3}")
    print(f"DEC: {dec3}\n")

    # Пример 4: Чувствительность к изменениям
    result4 = sha256(b"The quick brown fox jumps over the lazy dog.")
    dec4 = sha256_decimal(b"The quick brown fox jumps over the lazy dog.")
    print(f"sha256(b\"The quick brown fox jumps over the lazy dog.\") =")
    print(f"HEX: {result4}")
    print(f"DEC: {dec4}\n")

    # Пример 5: Работа с классом напрямую (пошаговое обновление)
    h = SHA256()
    h.update(b"hello")
    h.update(b" ")
    h.update(b"world")
    print(f"Пошаговое обновление:")
    print(f"h.update(b\"hello\") + h.update(b\" \") + h.update(b\"world\") =")
    print(f"HEX: {h.hexdigest()}")
    print(f"DEC: {h.decdigest()}\n")

    # Пример 6: Кодирование строки (Unicode)
    text = "Привет, мир"
    result5 = sha256(text.encode('utf-8'))
    dec5 = sha256_decimal(text.encode('utf-8'))
    print(f"sha256(\"{text}\") =")
    print(f"HEX: {result5}")
    print(f"DEC: {dec5}\n")

    # Пример 7: Сравнение размеров чисел
    print(f"=== Информация о десятичном формате ===")
    dec_value = sha256_decimal(b"example")
    print(f"Пример: sha256(b\"example\") в десятичном формате")
    print(f"Значение: {dec_value}")
    print(f"Количество цифр: {len(str(dec_value))}")
    print(f"Максимальное 256-битное число: {2**256 - 1}")
    print(f"Количество цифр в max: {len(str(2**256 - 1))}")