import random
from typing import Optional, Tuple
from hashlib import sha256


class Point:
    """Класс для представления точки на эллиптической кривой или точки бесконечности"""

    def __init__(self, x: Optional[int] = None, y: Optional[int] = None,
                 curve: 'EllipticCurve' = None):
        """
        Инициализация точки на эллиптической кривой

        Args:
            x: X-координата точки
            y: Y-координата точки
            curve: Эллиптическая кривая
        """
        self.x: int = x
        self.y: int = y
        self.curve: EllipticCurve = curve
        self.is_infinity: bool = (x is None and y is None)

    def __eq__(self, other: 'Point') -> bool:
        """Проверка равенства двух точек"""
        if self.is_infinity and other.is_infinity:
            return True
        if self.is_infinity or other.is_infinity:
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other: 'Point') -> 'Point':
        """Сложение двух точек на эллиптической кривой"""
        if self.is_infinity:
            return Point(other.x, other.y, self.curve)
        if other.is_infinity:
            return Point(self.x, self.y, self.curve)

        if self.x == other.x:
            if self.y == other.y:
                # Удвоение точки
                return self._double()
            else:
                # Точки противоположны, результат - точка в бесконечности
                return Point(curve=self.curve)

        # Вычисление углового коэффициента
        slope = ((other.y - self.y) *
                 pow(other.x - self.x, -1, self.curve.p)) % self.curve.p

        # Вычисление координат новой точки
        x_result = (slope * slope - self.x - other.x) % self.curve.p
        y_result = (slope * (self.x - x_result) - self.y) % self.curve.p

        return Point(x_result, y_result, self.curve)

    def _double(self) -> 'Point':
        """Удвоение точки на эллиптической кривой"""
        if self.is_infinity:
            return Point(curve=self.curve)

        # Для кривой y^2 = x^3 + ax + b
        # slope = (3x^2 + a) / (2y)
        numerator = (3 * self.x * self.x + self.curve.a) % self.curve.p
        denominator = (2 * self.y) % self.curve.p

        slope = (numerator * pow(denominator, -1, self.curve.p)) % self.curve.p

        x_result = (slope * slope - 2 * self.x) % self.curve.p
        y_result = (slope * (self.x - x_result) - self.y) % self.curve.p

        return Point(x_result, y_result, self.curve)

    def __mul__(self, scalar: int) -> 'Point':
        """Скалярное умножение точки (двоичный метод)"""
        if scalar == 0:
            return Point(curve=self.curve)

        if scalar < 0:
            # Для отрицательных скаляров используем противоположную точку
            return Point(self.x, (-self.y) % self.curve.p, self.curve) * (-scalar)

        result = Point(curve=self.curve)  # Точка в бесконечности
        addend = Point(self.x, self.y, self.curve)

        while scalar:
            if scalar & 1:
                result = result + addend
            addend = addend + addend
            scalar >>= 1

        return result

    def __rmul__(self, scalar: int) -> 'Point':
        """Поддержка умножения справа"""
        return self * scalar

    def __repr__(self) -> str:
        """Строковое представление точки"""
        if self.is_infinity:
            return "Point(Infinity)"
        return f"Point({self.x}, {self.y})"


class EllipticCurve:
    """Класс для представления эллиптической кривой вида y^2 = x^3 + ax + b (mod p)"""

    def __init__(self, a: int, b: int, p: int):
        """
        Инициализация эллиптической кривой

        Args:
            a: Коэффициент a кривой y^2 = x^3 + ax + b
            b: Коэффициент b кривой y^2 = x^3 + ax + b
            p: Простое число (модуль)
        """
        self.a = a % p
        self.b = b % p
        self.p = p

        # Проверка, что кривая невырожденная: 4a^3 + 27b^2 ≠ 0 (mod p)
        discriminant = (4 * a ** 3 + 27 * b ** 2) % p
        if discriminant == 0:
            raise ValueError("Невырожденная кривая не поддерживается")

    def is_point_on_curve(self, x: int, y: int) -> bool:
        """Проверка, принадлежит ли точка кривой"""
        left = (y * y) % self.p
        right = (x * x * x + self.a * x + self.b) % self.p
        return left == right

    def __repr__(self) -> str:
        """Строковое представление кривой"""
        return f"EllipticCurve(y^2 = x^3 + {self.a}x + {self.b} mod {self.p})"


class ECElGamal:
    """
    Криптосистема Эль-Гамаля на эллиптической кривой
    """

    def __init__(self, curve: EllipticCurve, G: Point, n: int):
        """
        Инициализация криптосистемы

        Args:
            curve: Эллиптическая кривая
            G: Базовая точка
            n: Порядок базовой точки
        """
        self.curve = curve
        self.G = G
        self.n = n
        self.public_key = None
        self.private_key = None

    def generate_keys(self) -> Tuple[Point, int]:
        """
        Генерация пары ключей

        Returns:
            (открытый ключ Q, закрытый ключ d)
        """
        self.private_key = random.randint(1, self.n - 1)
        self.public_key = self.private_key * self.G

        return self.public_key, self.private_key

    def encrypt(self, message_point: Point, public_key: Point) -> Tuple[Point, Point]:
        """
        Шифрование сообщения

        Args:
            message_point: Точка на эллиптической кривой (сообщение)
            public_key: Открытый ключ получателя (Q)

        Returns:
            Кортеж (C1, C2) - зашифрованное сообщение
        """
        k = random.randint(1, self.n - 1)

        C1 = k * self.G
        S = k * public_key
        C2 = message_point + S

        return C1, C2

    def sign(self, message: int, private_key: int) -> Tuple[int, int]:
        """
        ECDSA подпись сообщения

        Args:
            message: Хеш сообщения (целое число)
            private_key: Приватный ключ подписанта

        Returns:
            (r, s) - компоненты подписи
        """
        while True:
            # Генерируем случайное число k
            k: int = random.randint(1, self.n - 1)

            # Вычисляем R = k * G (случайную точку)
            R: Point = self.G * k

            # r - это x-координата точки R
            r: int = R.x % self.n

            if r == 0:
                continue

            # Вычисляем s = k^(-1) * (message + r * private_key) mod n
            s: int = (pow(k, -1, self.n) * (message + r * private_key)) % self.n

            if s == 0:
                continue

            return r, s

    def verify(self, public_key: Point, message: int, signature: Tuple[int, int]) -> bool:
        """
        ECDSA верификация подписи

        Args:
            public_key: Публичный ключ подписанта
            message: Хеш сообщения
            signature: Кортеж (r, s)

        Returns:
            True если подпись валидна, False иначе
        """
        r, s = signature

        # Проверка границ
        if not (1 <= r < self.n and 1 <= s < self.n):
            return False

        # Вычисляем w = s^(-1) mod n
        w: int = pow(s, -1, self.n)

        # Вычисляем u1 = message * w mod n
        u1: int = (message * w) % self.n

        # Вычисляем u2 = r * w mod n
        u2: int = (r * w) % self.n

        # Вычисляем точку C = u1 * G + u2 * PublicKey
        C: Point = u1 * self.G + u2 * public_key

        # Проверяем точку на бесконечность
        if C.is_infinity:
            return False

        # Проверяем: C.x mod n == r
        return C.x % self.n == r

    def decrypt(self, C1: Point, C2: Point) -> Point:
        """
        Расшифрование сообщения

        Args:
            C1: Первая часть шифротекста
            C2: Вторая часть шифротекста

        Returns:
            Точка сообщения
        """
        if self.private_key is None:
            raise ValueError("Закрытый ключ не установлен")

        S = self.private_key * C1
        S_neg = Point(S.x, (-S.y) % self.curve.p, self.curve)
        P = C2 + S_neg

        return P


class PointEncoder:
    """Вспомогательный класс для кодирования и декодирования сообщений в точки"""

    @staticmethod
    def encode_message(message: str, curve: EllipticCurve, x_range: int = 1000) -> Optional[Point]:
        """
        Кодирование сообщения в точку эллиптической кривой

        Args:
            message: Сообщение для кодирования
            curve: Эллиптическая кривая
            x_range: Диапазон для поиска координаты x

        Returns:
            Точка на кривой или None если не найдена
        """
        message_hash = int.from_bytes(message.encode(), 'big') % (curve.p // 1000)

        for i in range(x_range):
            x = (message_hash * x_range + i) % curve.p
            y_squared = (pow(x, 3, curve.p) + curve.a * x + curve.b) % curve.p
            y = PointEncoder._tonelli_shanks(y_squared, curve.p)

            if y is not None:
                return Point(x, y, curve)

        return None

    @staticmethod
    def _tonelli_shanks(n: int, p: int) -> Optional[int]:
        """
        Алгоритм Тонелли-Шэнкса для вычисления квадратного корня по модулю p
        """
        if pow(n, (p - 1) // 2, p) != 1:
            return None

        if p % 4 == 3:
            return pow(n, (p + 1) // 4, p)

        s = 0
        q = p - 1
        while q % 2 == 0:
            s += 1
            q //= 2

        z = 2
        while pow(z, (p - 1) // 2, p) != p - 1:
            z += 1

        M = s
        c = pow(z, q, p)
        t = pow(n, q, p)
        R = pow(n, (q + 1) // 2, p)

        while t != 1:
            i = 1
            temp = (t * t) % p
            while temp != 1 and i < M:
                temp = (temp * temp) % p
                i += 1

            b = pow(c, 1 << (M - i - 1), p)
            M = i
            c = (b * b) % p
            t = (t * c) % p
            R = (R * b) % p

        return R


def main() -> None:
    """Entry point."""

    message: int = 12345
    curve: EllipticCurve = EllipticCurve(0, 7, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)

    # Базовая точка (координаты из secp256k1)
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    G = Point(Gx, Gy, curve)

    # Порядок группы
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    # Криптосистема
    elgamal = ECElGamal(curve, G, n)
    public_key, private_key = elgamal.generate_keys()

    signature: Tuple[int, int] = elgamal.sign(message, private_key)
    print(f"{message=}\n{signature=}")

    verified: bool = elgamal.verify(public_key, message, signature)
    print(f"{verified=}")


if __name__ == '__main__':
    main()
