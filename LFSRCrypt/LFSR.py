from typing import Iterable


class LFSR:
    """
    Правый сдвиг. На каждом шаге:
      out = state & 1
      fb  = parity(state & taps_mask)
      state = (state >> 1) | (fb << (width-1))
    """
    def __init__(self, width: int, seed: int, taps: Iterable[int]):
        """
        width — число бит (n)
        seed  — начальное состояние (1..2^n-1)
        taps  — индексы битов для XOR (0=LSB, n-1=MSB), НЕ включая n-й член многочлена
        Пример: для многочлена x^8 + x^6 + x^5 + x^4 + 1 — taps = [0,4,5,6]
        """
        if width <= 0:
            raise ValueError("width must be > 0")
        if not (0 < seed < (1 << width)):
            raise ValueError("seed must be in 1..(2^width-1)")
        self.width = width
        self.state = seed
        self.taps_mask = 0
        for i in taps:
            if not (0 <= i < width):
                raise ValueError(f"tap index {i} out of range [0,{width-1}]")
            self.taps_mask |= (1 << i)

    @staticmethod
    def _parity(x: int) -> int:
        return x.bit_count() & 1

    def step(self) -> int:
        """Сделать один шаг и вернуть выходной бит (LSB до сдвига)."""
        out = self.state & 1
        fb = self._parity(self.state & self.taps_mask)
        self.state = (self.state >> 1) | (fb << (self.width - 1))
        return out

    def bits(self, n: int):
        """Итератор из n бит."""
        for _ in range(n):
            yield self.step()

    def bytes(self, n: int):
        """Итератор из n байт (младший бит генерируется первым внутри байта)."""
        for _ in range(n):
            b = 0
            for i in range(8):
                b |= (self.step() << i)
            yield b

    def keystream(self, n: int):
        """Вернуть n битов, но в виде массива"""
        return list(self.bits(n))

