import random
import time
from typing import Generator, Deque
from collections import deque


def mid_square(init_state: int) -> Generator[int, None, None]:
    if init_state < 999 or init_state > 9999:
        raise ValueError('init_state must be between 1000 and 10_000')

    current: int = init_state
    while True:
        square: int = current ** 2
        filled: str = str(square).zfill(8)
        current = int(filled[2:6])
        yield current


def fibonacci_delay(init_state: list[int], num_count: int) -> Generator[int, None, None]:
    a, b = 17, 5

    state: Deque[int] = Deque(init_state.copy())

    start_position: int = max(a, b)

    if len(init_state) < start_position:
        raise IndexError(f'init_state must be at least {start_position}')

    for i in range(num_count):
        output: int = abs(state[a - 1] - state[b - 1])
        state.popleft()
        state.append(output)
        yield output


def demonstrate_mid_square(init_state: int) -> None:
    gen = mid_square(init_state)
    current: int = -1
    seen: set = set()
    counter: int = 0
    while current not in seen:
        seen.add(current)
        current = next(gen)
        counter += 1

    print("Алгоритм Среднего квадрата")
    print(f"Повторение случилось через {counter} шагов.\n"
          f"Повторилось число {current}\n"
          f"Список чисел {seen}")


def demonstrate_fibonacci(init_state: list[int], num_count: int) -> None:
    gen = fibonacci_delay(init_state, num_count)
    current: int = -1
    seen: list[int] = list()
    duplicates: list[int] = []
    duplicates_counter: list[int] = []
    for i in range(num_count):
        current = next(gen)
        if current in seen:
            duplicates.append(current)
            duplicates_counter.append(i)
        else:
            seen.append(current)

    print("Алгоритм Фибоначчи")
    print(f"Список чисел {seen}")
    if not duplicates_counter:
        print("Нет дубликатов")
        return

    print(f"Повторение случилось через {duplicates_counter} шагов.\n"
          f"Повторилось число {current}")


def rule30_iter(state: list[int]) -> list[int]:
    padded_state: list[int] = [0] + state + [0]
    current: list[int] = [0] * len(state)
    for i in range(len(current)):
        current[i] = padded_state[i] ^ (padded_state[i + 1] or padded_state[i + 2])
    return current


def pprint_rule30_row(row) -> None:
    symbols = {1: '▓', 0: '░'}
    print(''.join(symbols[val] for val in row))




def rule30(init_state: list[int] | int | str, n_rows: int, num_bits: int,
           verbose: bool, num_count: int) -> Generator[int, None, None]:
    if isinstance(init_state, int):
        state: list[int] = []
        for i in range(init_state.bit_length()):
            state.append(init_state >> i & 1)
    elif isinstance(init_state, list):
        state: list[int] = init_state.copy()
    elif isinstance(init_state, str):
        if init_state.count('1') + init_state.count('0') != len(init_state):
            raise ValueError(f'init_state must contain exactly 0 or 1')
        state: list[int] = list(map(int, init_state))
    else:
        raise ValueError(f'init_state must be int, str or list')

    if len(state) % 2 == 0:
        raise ValueError('init_state must be odd size')

    rule30_list: list[list[int]] = [state]
    for i in range(n_rows):
        state = rule30_iter(state)
        rule30_list.append(state)

    size: int = len(state)
    center: int = size // 2
    if verbose:
        for row in rule30_list:
            pprint_rule30_row(row)

    padding: int = int(time.time()) % n_rows

    for i in range(num_count):
        num: int = 0
        for j in range(num_bits):
            current_row: list[int] = rule30_list[(j + padding) % n_rows]
            num |= current_row[center] << j

        padding = (j + padding) % n_rows
        yield num


def generate_bitstring(length: int) -> str:
    return ''.join(str(random.randint(0, 1)) for _ in range(length))


def demonstrate(*args, num_count: int, name: str, algorithm: Generator[int, None, None]) -> None:
    gen = algorithm(*args, num_count=num_count)
    current: int = -1
    seen: list[int] = list()
    duplicates: list[int] = []
    duplicates_counter: list[int] = []
    for i in range(num_count):
        current = next(gen)
        if current in seen:
            duplicates.append(current)
            duplicates_counter.append(i)
        seen.append(current)

    print(f"Алгоритм {name}")
    print(f"Список чисел {seen}")
    if not duplicates_counter:
        print("Нет дубликатов")
        return

    print(f"Первое повторение случилось через {duplicates_counter[0]} шагов.\n"
          f"Повторилось число {duplicates[0]}")


def main() -> None:
    """Entry point."""
    demonstrate_mid_square(1234)
    print()
    demonstrate([random.randint(1, 10_000) for i in range(17)], num_count=1000, name="Фибоначчи", algorithm=fibonacci_delay)
    print()
    demonstrate(generate_bitstring(201), 100, 8, True, num_count=1000, name="rule30", algorithm=rule30)


if __name__ == '__main__':
    # '0' * 50 + '1' + '0' * 50
    # gen = rule30(generate_bitstring(101), 50, 8, True, num_count=5)
    # for num in gen:
    #     print(num)
    main()
