"""
Модуль генераторов псевдослучайных чисел.

Содержит реализации различных алгоритмов генерации псевдослучайных чисел:
- Алгоритм среднего квадрата (Mid-Square)
- Алгоритм Фибоначчи с задержкой
- Правило 30 клеточного автомата

Автор: AdirtKa
Дата: 2025-11-18
"""

import random
import time
from typing import Generator, Union
from collections import deque


class RandomGeneratorError(Exception):
    """Базовый класс исключений для генераторов случайных чисел."""
    pass


class InvalidInitStateError(RandomGeneratorError):
    """Исключение для невалидного начального состояния."""
    pass


def mid_square(init_state: int) -> Generator[int, None, None]:
    """
    Генератор псевдослучайных чисел на основе алгоритма среднего квадрата.
    
    Алгоритм возводит текущее число в квадрат, дополняет результат нулями
    до 8 цифр и извлекает средние 4 цифры как следующее значение.
    
    Args:
        init_state: Начальное состояние (от 1000 до 9999 включительно).
        
    Yields:
        int: Следующее псевдослучайное число в последовательности.
        
    Raises:
        InvalidInitStateError: Если init_state не в диапазоне [1000, 9999].
        
    Example:
        >>> gen = mid_square(1234)
        >>> next(gen)
        5227
        >>> next(gen)
        3215
    """
    if init_state < 1000 or init_state > 9999:
        raise InvalidInitStateError(
            f'init_state должен быть между 1000 и 9999, получено: {init_state}'
        )

    current: int = init_state
    
    while True:
        square: int = current ** 2
        filled: str = str(square).zfill(8)
        current = int(filled[2:6])
        yield current


def fibonacci_delay(
    init_state: list[int], 
    num_count: int
) -> Generator[int, None, None]:
    """
    Генератор псевдослучайных чисел на основе алгоритма Фибоначчи с задержкой.
    
    Использует параметры a=17 и b=5 для генерации последовательности
    на основе разности элементов: |state[a-1] - state[b-1]|.
    
    Args:
        init_state: Начальное состояние (список минимум из 17 элементов).
        num_count: Количество чисел для генерации.
        
    Yields:
        int: Следующее псевдослучайное число в последовательности.
        
    Raises:
        InvalidInitStateError: Если init_state содержит менее 17 элементов.
        
    Example:
        >>> init = [random.randint(1, 100) for _ in range(17)]
        >>> gen = fibonacci_delay(init, 10)
        >>> list(gen)
        [23, 45, 12, ...]
    """
    a: int = 17
    b: int = 5
    start_position: int = max(a, b)

    if len(init_state) < start_position:
        raise InvalidInitStateError(
            f'init_state должен содержать минимум {start_position} элементов, '
            f'получено: {len(init_state)}'
        )

    state: deque[int] = deque(init_state.copy())

    for _ in range(num_count):
        output: int = abs(state[a - 1] - state[b - 1])
        state.popleft()
        state.append(output)
        yield output


def rule30_iter(state: list[int]) -> list[int]:
    """
    Выполняет одну итерацию правила 30 клеточного автомата.
    
    Правило 30: новое состояние ячейки зависит от её текущего состояния
    и состояния двух соседних ячеек по формуле XOR.
    
    Args:
        state: Текущее состояние клеточного автомата.
        
    Returns:
        list[int]: Новое состояние после применения правила 30.
        
    Example:
        >>> rule30_iter([0, 1, 0])
        [1, 1, 1]
    """
    padded_state: list[int] = [0] + state + [0]
    current: list[int] = [0] * len(state)
    
    for i in range(len(current)):
        left: int = padded_state[i]
        center: int = padded_state[i + 1]
        right: int = padded_state[i + 2]
        current[i] = left ^ (center | right)
        
    return current


def pprint_rule30_row(row: list[int]) -> None:
    """
    Красиво печатает строку клеточного автомата.
    
    Использует символы ▓ для 1 и ░ для 0.
    
    Args:
        row: Строка клеточного автомата для вывода.
        
    Example:
        >>> pprint_rule30_row([0, 1, 1, 0, 1])
        ░▓▓░▓
    """
    symbols: dict[int, str] = {1: '▓', 0: '░'}
    print(''.join(symbols[val] for val in row))


def _parse_init_state(init_state: Union[int, list[int], str]) -> list[int]:
    """
    Преобразует различные форматы начального состояния в список битов.
    
    Args:
        init_state: Начальное состояние (int, list[int] или str).
        
    Returns:
        list[int]: Список битов (0 и 1).
        
    Raises:
        InvalidInitStateError: Если формат init_state некорректен.
    """
    if isinstance(init_state, int):
        state: list[int] = []
        for i in range(init_state.bit_length()):
            state.append((init_state >> i) & 1)
        return state
        
    elif isinstance(init_state, list):
        return init_state.copy()
        
    elif isinstance(init_state, str):
        if not all(c in '01' for c in init_state):
            raise InvalidInitStateError(
                'init_state в виде строки должен содержать только 0 и 1'
            )
        return list(map(int, init_state))
        
    else:
        raise InvalidInitStateError(
            f'init_state должен быть int, str или list[int], '
            f'получен: {type(init_state).__name__}'
        )


def rule30(
    init_state: Union[int, list[int], str],
    n_rows: int,
    num_bits: int,
    verbose: bool,
    num_count: int
) -> Generator[int, None, None]:
    """
    Генератор псевдослучайных чисел на основе правила 30 клеточного автомата.
    
    Правило 30 - это одномерный клеточный автомат, который генерирует
    хаотическое поведение из простых правил. Используется центральный столбец
    эволюции автомата для извлечения псевдослучайных бит.
    
    Args:
        init_state: Начальное состояние автомата (int, list[int] или str).
                   Должно быть нечётной длины.
        n_rows: Количество строк эволюции автомата для генерации.
        num_bits: Количество бит в каждом выходном числе.
        verbose: Если True, печатает визуализацию автомата.
        num_count: Количество чисел для генерации.
        
    Yields:
        int: Следующее псевдослучайное число.
        
    Raises:
        InvalidInitStateError: Если init_state имеет чётную длину или
                              некорректный формат.
                              
    Example:
        >>> init = '0' * 50 + '1' + '0' * 50
        >>> gen = rule30(init, 100, 8, False, 10)
        >>> next(gen)
        127
    """
    state: list[int] = _parse_init_state(init_state)

    if len(state) % 2 == 0:
        raise InvalidInitStateError(
            f'init_state должен иметь нечётную длину, получено: {len(state)}'
        )

    # Генерация эволюции клеточного автомата
    rule30_list: list[list[int]] = [state]
    for _ in range(n_rows):
        state = rule30_iter(state)
        rule30_list.append(state)

    size: int = len(state)
    center: int = size // 2
    
    # Визуализация автомата
    if verbose:
        print("\nЭволюция клеточного автомата (Правило 30):")
        print("=" * size)
        for row in rule30_list:
            pprint_rule30_row(row)
        print("=" * size)
        print()

    # Генерация псевдослучайных чисел
    padding: int = int(time.time()) % n_rows

    for i in range(num_count):
        num: int = 0
        for j in range(num_bits):
            current_row: list[int] = rule30_list[(j + padding) % n_rows]
            num |= current_row[center] << j

        padding = (j + padding) % n_rows
        yield num


def generate_bitstring(length: int) -> str:
    """
    Генерирует случайную битовую строку заданной длины.
    
    Args:
        length: Длина битовой строки.
        
    Returns:
        str: Строка из случайных 0 и 1.
        
    Example:
        >>> bitstring = generate_bitstring(10)
        >>> len(bitstring)
        10
        >>> all(c in '01' for c in bitstring)
        True
    """
    return ''.join(str(random.randint(0, 1)) for _ in range(length))


def demonstrate_mid_square(init_state: int) -> None:
    """
    Демонстрирует работу алгоритма среднего квадрата.
    
    Генерирует числа до первого повторения и выводит статистику.
    
    Args:
        init_state: Начальное состояние для алгоритма.
    """
    print("=" * 60)
    print("АЛГОРИТМ СРЕДНЕГО КВАДРАТА (Mid-Square)")
    print("=" * 60)
    
    gen = mid_square(init_state)
    current: int = -1
    seen: set[int] = set()
    counter: int = 0
    
    while current not in seen:
        seen.add(current)
        current = next(gen)
        counter += 1

    print(f"Начальное значение: {init_state}")
    print(f"Повторение случилось через {counter} шагов")
    print(f"Повторилось число: {current}")
    print(f"Уникальных чисел сгенерировано: {len(seen)}")
    print(f"Первые 10 чисел: {list(seen)[:10]}")
    print()


def demonstrate_fibonacci(init_state: list[int], num_count: int) -> None:
    """
    Демонстрирует работу алгоритма Фибоначчи с задержкой.
    
    Args:
        init_state: Начальное состояние (минимум 17 элементов).
        num_count: Количество чисел для генерации.
    """
    print("=" * 60)
    print("АЛГОРИТМ ФИБОНАЧЧИ С ЗАДЕРЖКОЙ")
    print("=" * 60)
    
    gen = fibonacci_delay(init_state, num_count)
    seen: list[int] = []
    duplicates: list[int] = []
    duplicates_counter: list[int] = []
    
    for i in range(num_count):
        current: int = next(gen)
        if current in seen:
            duplicates.append(current)
            duplicates_counter.append(i)
        seen.append(current)

    unique_count: int = len(set(seen))
    print(f"Сгенерировано чисел: {num_count}")
    print(f"Уникальных чисел: {unique_count}")
    print(f"Первые 20 чисел: {seen[:20]}")
    
    if duplicates_counter:
        print(f"\nПервое повторение на шаге: {duplicates_counter[0]}")
        print(f"Повторилось число: {duplicates[0]}")
        print(f"Всего повторений: {len(duplicates)}")
    else:
        print("\nПовторений не обнаружено")
    print()


def demonstrate_generic(
    *args,
    num_count: int,
    name: str,
    algorithm: callable
) -> None:
    """
    Универсальная функция для демонстрации работы алгоритма.
    
    Args:
        *args: Аргументы для передачи в алгоритм.
        num_count: Количество чисел для генерации.
        name: Название алгоритма для вывода.
        algorithm: Функция-генератор алгоритма.
    """
    print("=" * 60)
    print(f"АЛГОРИТМ {name.upper()}")
    print("=" * 60)
    
    gen = algorithm(*args, num_count=num_count)
    seen: list[int] = []
    duplicates: list[int] = []
    duplicates_counter: list[int] = []
    
    for i in range(num_count):
        current: int = next(gen)
        if current in seen:
            duplicates.append(current)
            duplicates_counter.append(i)
        seen.append(current)

    unique_count: int = len(set(seen))
    print(f"Сгенерировано чисел: {num_count}")
    print(f"Уникальных чисел: {unique_count}")
    print(f"Первые 20 чисел: {seen[:20]}")
    
    if duplicates_counter:
        print(f"\nПервое повторение на шаге: {duplicates_counter[0]}")
        print(f"Повторилось число: {duplicates[0]}")
        print(f"Всего повторений: {len(duplicates)}")
    else:
        print("\nПовторений не обнаружено")
    print()


def main() -> None:
    """
    Точка входа программы.
    
    Демонстрирует работу всех реализованных алгоритмов генерации
    псевдослучайных чисел с различными параметрами.
    """
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "ДЕМОНСТРАЦИЯ ГЕНЕРАТОРОВ ПСЧ" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Демонстрация алгоритма среднего квадрата
    demonstrate_mid_square(1234)
    
    # Демонстрация алгоритма Фибоначчи
    fibonacci_init: list[int] = [random.randint(1, 10_000) for _ in range(17)]
    demonstrate_generic(
        fibonacci_init,
        num_count=1000,
        name="Фибоначчи с задержкой",
        algorithm=fibonacci_delay
    )
    
    # Демонстрация правила 30
    rule30_init: str = '0' * 50 + '1' + '0' * 50
    rule30_init: str = generate_bitstring(201)
    demonstrate_generic(
        rule30_init,
        100,    # n_rows
        8,      # num_bits
        False,   # verbose
        num_count=1000,
        name="Правило 30 (Rule 30)",
        algorithm=rule30
    )
    
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except RandomGeneratorError as e:
        print(f"Ошибка генератора: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        raise
