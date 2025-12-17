import random
from typing import Optional, Tuple
from hashlib import sha256


class EllipticCurve:
    """Класс для представления эллиптической кривой вида y^2 = x^3 + ax + b (mod p)"""

    def __init__(self, a: int, b: int, p: int):
        """
        Инициализация эллиптической кривой

        Args:
            a: Коэффициент a кривой y^2 = x^3 + ax + b
            b: Коэффициент b кривой y^2 = x^3 + ax + b
            p: Простое число (модуль)

        Raises:
            ValueError: Если кривая вырожденная (4a³ + 27b² ≡ 0 mod p)
        """
        self.a = a % p
        self.b = b % p
        self.p = p

        # Проверка невырожденности: 4a^3 + 27b^2 ≠ 0 (mod p)
        discriminant = (4 * a ** 3 + 27 * b ** 2) % p
        if discriminant == 0:
            raise ValueError("Кривая вырожденная: 4a³ + 27b² ≡ 0 (mod p)")

    def is_point_on_curve(self, x: int, y: int) -> bool:
        """
        Проверка принадлежности точки кривой

        Args:
            x: X-координата
            y: Y-координата

        Returns:
            True если точка на кривой, иначе False
        """
        left = (y * y) % self.p
        right = (x * x * x + self.a * x + self.b) % self.p
        return left == right

    def __repr__(self) -> str:
        """Строковое представление кривой"""
        return f"EllipticCurve(y² = x³ + {self.a}x + {self.b} mod {self.p})"
