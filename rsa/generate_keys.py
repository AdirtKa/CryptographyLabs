from typing import Optional

from Crypto.Util import number
from math import gcd


def get_coprime(phi: int) -> int:
    """
    Выбирает подходящий открытый экспонент для RSA.
    Обычно возвращает 65537, если он взаимно прост с phi.
    Если нет, пробует другие варианты.

    :param phi: Значение функции Эйлера для n
    :return: подходящее число e
    """
    candidates = [65537, 257, 17, 3]
    for e in candidates:
        if gcd(phi, e) == 1:
            return e

    e = 3
    while e < phi:
        if gcd(phi, e) == 1:
            return e
        e += 2

    raise ValueError("Не удалось найти взаимно простое число для e")



def is_prime(n: int) -> bool:
    """
    Проверяет, является ли число n простым.

    Args:
        n (int): Число для проверки.

    Returns:
        bool: True, если число простое, иначе False.
    """
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False

    r = int(n ** 0.5)
    f = 5
    while f <= r:
        if n % f == 0:
            return False
        if n % (f + 2) == 0:
            return False
        f += 6
    return True


def generate_keys(*, init_state: Optional[tuple[int, int]] = None, bits_len: int = 10) -> tuple[int, int, int]:
    """
    Generate keys for rsa algorithm.
    return in format n, e, d
    where n and e are public keys and d is a private key.
    to cipher M use C = (M ** e) % n
    to decipher C use M = (C ** d) % n

    :param bits_len: how many bits will be in initial numbers to generate keys
    :param init_state: initial state with p and q. Must be prime numbers

    :return: tuple[int, int, int]
    """
    if init_state is not None:
        p, q = init_state
        if not is_prime(p) or not is_prime(q):
            raise ValueError("init_state must be prime numbers")
    else:
        p: int = number.getPrime(bits_len)
        q: int = number.getPrime(bits_len)

    n: int = p * q

    phi: int = (p - 1) * (q - 1)
    e: int = get_coprime(phi)
    d: int = pow(e, -1, phi)

    return n, e, d


def main() -> None:
    """Entry point."""
    n, e, d = generate_keys(init_state=(1231, 13))

    test_num: int = 42
    cipher: int = (test_num ** e) % n
    decipher: int = (cipher ** d) % n
    print(decipher)


if __name__ == '__main__':
    main()
