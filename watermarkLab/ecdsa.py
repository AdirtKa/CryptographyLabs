import random
from typing import Tuple
from hashlib import sha256
from point import Point
from watermarkLab.eliptic_curve import EllipticCurve


class ECDSA:
    """
    Реализация алгоритма ECDSA (Elliptic Curve Digital Signature Algorithm)
    с поддержкой встраивания водяного знака
    """

    def __init__(self, curve: EllipticCurve, G: Point, n: int):
        """
        Инициализация ECDSA

        Args:
            curve: Эллиптическая кривая
            G: Базовая (генерирующая) точка
            n: Порядок базовой точки (количество элементов в подгруппе)
        """
        self.curve = curve
        self.G = G
        self.n = n
        self.private_key = None
        self.public_key = None

    def generate_keys(self) -> Tuple[Point, int]:
        """
        Генерация пары ключей

        Returns:
            Кортеж (публичный_ключ, приватный_ключ)
        """
        self.private_key = random.randint(1, self.n - 1)
        self.public_key = self.private_key * self.G
        return self.public_key, self.private_key

    def sign(self, message: int, private_key: int) -> Tuple[int, int]:
        """
        ECDSA подпись сообщения

        Args:
            message: Хеш сообщения (целое число)
            private_key: Приватный ключ подписанта

        Returns:
            Кортеж (r, s) - компоненты подписи
        """
        while True:
            k = random.randint(1, self.n - 1)
            R = self.G * k
            r = R.x % self.n

            if r == 0:
                continue

            s = (pow(k, -1, self.n) * (message + r * private_key)) % self.n

            if s == 0:
                continue

            return r, s

    def verify(self, public_key: Point, message: int,
               signature: Tuple[int, int]) -> bool:
        """
        ECDSA верификация подписи

        Args:
            public_key: Публичный ключ подписанта
            message: Хеш сообщения
            signature: Кортеж (r, s)

        Returns:
            True если подпись валидна
        """
        r, s = signature

        if not (1 <= r < self.n and 1 <= s < self.n):
            return False

        w = pow(s, -1, self.n)
        u1 = (message * w) % self.n
        u2 = (r * w) % self.n

        C = u1 * self.G + u2 * public_key

        if C.is_infinity:
            return False

        return C.x % self.n == r