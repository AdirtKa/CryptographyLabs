from typing import Optional
from watermarkLab.eliptic_curve import EllipticCurve


class Point:
    """Класс для представления точки на эллиптической кривой или точки бесконечности"""

    def __init__(self, x: Optional[int] = None, y: Optional[int] = None,
                 curve: Optional[EllipticCurve] = None):
        """
        Инициализация точки

        Args:
            x: X-координата (None для точки в бесконечности)
            y: Y-координата (None для точки в бесконечности)
            curve: Ссылка на эллиптическую кривую
        """
        self.x = x
        self.y = y
        self.curve = curve
        self.is_infinity = (x is None and y is None)

    def __eq__(self, other: 'Point') -> bool:
        """Сравнение двух точек"""
        if self.is_infinity and other.is_infinity:
            return True
        if self.is_infinity or other.is_infinity:
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other: 'Point') -> 'Point':
        """
        Сложение двух точек на эллиптической кривой (закон группы)

        Args:
            other: Вторая точка

        Returns:
            Сумма двух точек
        """
        if self.is_infinity:
            return Point(other.x, other.y, self.curve)
        if other.is_infinity:
            return Point(self.x, self.y, self.curve)

        if self.x == other.x:
            if self.y == other.y:
                return self._double()
            else:
                # Точки противоположны
                return Point(curve=self.curve)

        # Вычисление углового коэффициента
        slope = ((other.y - self.y) *
                 pow(other.x - self.x, -1, self.curve.p)) % self.curve.p

        x_result = (slope ** 2 - self.x - other.x) % self.curve.p
        y_result = (slope * (self.x - x_result) - self.y) % self.curve.p

        return Point(x_result, y_result, self.curve)

    def _double(self) -> 'Point':
        """
        Удвоение точки (сложение точки с самой собой)

        Returns:
            2P (точка, полученная при удвоении)
        """
        if self.is_infinity:
            return Point(curve=self.curve)

        # slope = (3x² + a) / (2y)
        numerator = (3 * self.x ** 2 + self.curve.a) % self.curve.p
        denominator = (2 * self.y) % self.curve.p

        slope = (numerator * pow(denominator, -1, self.curve.p)) % self.curve.p

        x_result = (slope ** 2 - 2 * self.x) % self.curve.p
        y_result = (slope * (self.x - x_result) - self.y) % self.curve.p

        return Point(x_result, y_result, self.curve)

    def __mul__(self, scalar: int) -> 'Point':
        """
        Скалярное умножение (бинарный метод - двоичное представление)

        Args:
            scalar: Целое число для умножения

        Returns:
            scalar * P
        """
        if scalar == 0:
            return Point(curve=self.curve)

        if scalar < 0:
            return Point(self.x, (-self.y) % self.curve.p, self.curve) * (-scalar)

        result = Point(curve=self.curve)  # O (точка в бесконечности)
        addend = Point(self.x, self.y, self.curve)

        while scalar:
            if scalar & 1:
                result = result + addend
            addend = addend + addend
            scalar >>= 1

        return result

    def __rmul__(self, scalar: int) -> 'Point':
        """Поддержка умножения справа: scalar * point"""
        return self * scalar

    def __repr__(self) -> str:
        """Строковое представление"""
        if self.is_infinity:
            return "Point(∞)"
        return f"Point({hex(self.x)}, {hex(self.y)})"