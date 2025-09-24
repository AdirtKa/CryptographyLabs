from typing import Iterable


class LFSR:
    """
    Правый сдвиг. На каждом шаге:
      out = state & 1
      fb  = parity(state & taps_mask)
      state = (state >> 1) | (fb << (width-1))
    """
    def __init__(self, seed: int, taps: Iterable[int]):
        """
        seed  — начальное состояние (1..2^n-1)
        taps  — индексы битов для XOR (0=LSB, n-1=MSB)
        """
        if seed <= 0:
            raise ValueError("seed must be > 0")

        self.width: int = seed.bit_length()
        self.state: int = seed
        self.taps_mask: int = 0
        for i in taps:
            if not (0 <= i < self.width):
                raise ValueError(f"tap index {i} out of range [0,{self.width-1}]")
            self.taps_mask |= (1 << i)

    @staticmethod
    def _parity(x: int) -> int:
        return x.bit_count() & 1

    def step(self) -> int:
        out = self.state & 1
        fb = self._parity(self.state & self.taps_mask)
        self.state = (self.state >> 1) | (fb << (self.width - 1))
        return out

    def bits(self, n: int):
        for _ in range(n):
            yield self.step()

    def bytes(self, n: int):
        for _ in range(n):
            b = 0
            for i in range(8):
                b |= (self.step() << i)
            yield b

    def keystream(self, n: int):
        return list(self.bits(n))
