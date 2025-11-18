from typing import Generator


def mid_square(init_state: int) -> Generator[int, None, None]:
    if init_state < 999 or init_state > 9999:
        raise ValueError('init_state must be between 1000 and 10_000')

    current: int = init_state
    while True:
        square: int = current ** 2
        filled: str = str(square).zfill(8)
        current = int(filled[2:6])
        yield current

def demonstrate_mid_square(init_state: int) -> None:
    gen = mid_square(init_state)
    current: int = -1
    seen: set = set()
    counter: int = 0
    while current not in seen:
        seen.add(current)
        current = next(gen)
        counter += 1

    print(f"Повторение случилось через {counter} шагов.\n"
          f"Повторилось число {current}\n"
          f"Список чисел {seen}")


def main() -> None:
    """Entry point."""
    demonstrate_mid_square(1234)


if __name__ == '__main__':
    main()
