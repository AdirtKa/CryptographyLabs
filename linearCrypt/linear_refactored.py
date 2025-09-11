from __future__ import annotations

import math
import os
import random
import string
from typing import Tuple


# ======================= Конфигурация =======================

ALPHABET: str = string.ascii_lowercase
ALPHABET_SIZE: int = len(ALPHABET)


# ======================= Базовые утилиты =======================

def is_coprime(a: int, m: int) -> bool:
    """Проверка взаимной простоты a и m."""
    return math.gcd(a, m) == 1


def find_coprime_starting_from(start: int, m: int) -> int:
    """
    Найти ближайшее число >= start, взаимно простое с m.
    (Используется для автоподбора корректного 'a'.)
    """
    a = max(1, start)
    while not is_coprime(a, m):
        a += 1
    return a


def validate_keys(a: int, b: int, m: int) -> None:
    """
    Валидация ключей аффинного шифра.
    :raises ValueError: Если ключи некорректны.
    """
    if not is_coprime(a, m):
        raise ValueError(f"'a'={a} не взаимно просто с модулем {m}. Выберите другое 'a'.")
    # if not (0 <= b < m):
    #     raise ValueError(f"'b'={b} должно быть в диапазоне [0, {m - 1}].")


def mod_inverse(a: int, m: int) -> int:
    """
    Обратный элемент к a по модулю m. Бросает ValueError, если не существует.
    (В Python 3.8+ можно коротко: pow(a, -1, m))
    """
    try:
        return pow(a, -1, m)
    except ValueError as e:
        # на случай старых интерпретаторов можно реализовать расширенный Евклид
        raise e


def _transform_char(ch: str, idx_transform) -> str:
    """
    Преобразовать символ через индексную трансформацию, сохранив регистр.
    Idx_transform: функция, принимающая индекс в алфавите и возвращающая новый индекс.
    """
    # нижний регистр
    if ch.islower() and ch in ALPHABET:
        i = ALPHABET.index(ch)
        return ALPHABET[idx_transform(i)]
    # верхний регистр
    if ch.isupper() and ch.lower() in ALPHABET:
        i = ALPHABET.index(ch.lower())
        return ALPHABET[idx_transform(i)].upper()
    # прочие символы не трогаем
    return ch


# ======================= Шифр =======================

def encrypt_affine(plaintext: str, a: int, b: int, alphabet: str = ALPHABET) -> str:
    """
    Зашифровать строку аффинным шифром.
    Шифруются символы латинского алфавита (a-z / A-Z); остальные сохраняются.

    :param plaintext: Исходный текст
    :param a: мультипликативный ключ (gcd(a, |alphabet|) == 1)
    :param b: аддитивный ключ (0 <= b < |alphabet|)
    :param alphabet: алфавит (по умолчанию a-z)
    :return: шифротекст
    """
    m = len(alphabet)
    validate_keys(a, b, m)

    def f(i: int) -> int:
        return (a * i + b) % m

    # используем глобальный ALPHABET в _transform_char; если нужен кастомный — можно расширить
    # или заменить _transform_char на вариант, который принимает alphabet явно
    return "".join(_transform_char(ch, f) for ch in plaintext)


def decrypt_affine(ciphertext: str, a: int, b: int, alphabet: str = ALPHABET) -> str:
    """
    Расшифровать строку, зашифрованную аффинным шифром.

    :param ciphertext: Шифротекст
    :param a: мультипликативный ключ
    :param b: аддитивный ключ
    :param alphabet: алфавит (по умолчанию a-z)
    :return: исходный текст
    """
    m = len(alphabet)
    validate_keys(a, b, m)
    a_inv = mod_inverse(a, m)

    def f_inv(i: int) -> int:
        return (a_inv * (i - b)) % m

    return "".join(_transform_char(ch, f_inv) for ch in ciphertext)


# ======================= CLI-утилиты =======================

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def prompt_int(msg: str) -> int:
    """Безопасный ввод целого числа."""
    while True:
        s = input(msg).strip()
        try:
            return int(s)
        except ValueError:
            print("Ошибка: введите целое число.")


def prompt_keys(current_a: int, current_b: int, m: int) -> Tuple[int, int]:
    """
    Запросить у пользователя новые ключи a, b с валидацией.
    Можно ввести 0 для 'a', чтобы автоподобрать взаимнопростое значение.
    """
    print(f"\nТекущие ключи: a={current_a}, b={current_b}, модуль={m}")
    print("Правила: gcd(a, m) == 1,  0 <= b < m.")
    print("Подсказка: введите a=0 для авто-подбора (найдём ближайшее корректное).")

    while True:
        a = prompt_int("Введите a: ")
        b = prompt_int("Введите b: ")

        if a == 0:
            a = find_coprime_starting_from(2, m)
            print(f"Автоподбор: a → {a}")

        try:
            validate_keys(a, b, m)
            return a, b
        except ValueError as e:
            print(f"Ключи некорректны: {e}\nПопробуйте ещё.\n")


def random_keys(m: int) -> Tuple[int, int]:
    """Сгенерировать случайные валидные ключи (a, b)."""
    # случайный 'a' до тех пор, пока взаимно прост
    while True:
        a = random.randint(1, m - 1)
        if is_coprime(a, m):
            break
    b = random.randint(0, m - 1)
    return a, b


def print_keys(a: int, b: int, m: int) -> None:
    print("\nТекущие параметры шифра:")
    print(f"  Алфавит: a-z (|Σ| = {m})")
    print(f"  Ключи: a = {a}, b = {b}")
    try:
        inv = mod_inverse(a, m)
        print(f"  a^(-1) mod {m} = {inv}")
    except ValueError:
        print("  (a не имеет обратного — проверка не пройдена)")


# ======================= Основной CLI =======================

def main() -> int:
    m = ALPHABET_SIZE

    # стартовые ключи (как в твоём коде): a берём с 4 и двигаемся до взаимнопростого; b случайный
    a = find_coprime_starting_from(4, m)
    b = random.randint(1, 42) % m  # приведём в допустимый диапазон

    while True:
        clear_screen()
        print("Аффинный шифр (a-z). Шифруются только латинские буквы; регистр сохраняется.\n")
        print("Меню:")
        print("1. Показать текущие ключи")
        print("2. Изменить ключи вручную")
        print("3. Сгенерировать случайные ключи")
        print("4. Зашифровать сообщение")
        print("5. Расшифровать сообщение")
        print("6. Показать пример обратного по модулю")
        print("7. Выход")

        choice = input("\nВыберите пункт: ").strip()

        if choice == "1":
            print_keys(a, b, m)
            input("\nEnter для продолжения...")

        elif choice == "2":
            a, b = prompt_keys(a, b, m)
            print("\nКлючи обновлены.")
            input("\nEnter для продолжения...")

        elif choice == "3":
            a, b = random_keys(m)
            print_keys(a, b, m)
            input("\nEnter для продолжения...")

        elif choice == "4":
            msg = input("\nВведите сообщение для шифрования: ")
            try:
                ct = encrypt_affine(msg, a, b)
                print("\nЗашифрованный текст:")
                print(ct)
            except ValueError as e:
                print(f"\nОшибка: {e}")
            input("\nEnter для продолжения...")

        elif choice == "5":
            ct = input("\nВведите шифротекст для расшифрования: ")
            try:
                pt = decrypt_affine(ct, a, b)
                print("\nРасшифрованный текст:")
                print(pt)
            except ValueError as e:
                print(f"\nОшибка: {e}")
            input("\nEnter для продолжения...")

        elif choice == "6":
            k = prompt_int("\nВведите число k (покажем k^(-1) mod 26, если он существует): ")
            try:
                inv = mod_inverse(k, m)
                print(f"\nОбратное к {k} по модулю {m}: {inv}")
            except ValueError:
                print(f"\nУ {k} нет обратного по модулю {m} (gcd({k}, {m}) != 1).")
            input("\nEnter для продолжения...")

        elif choice == "7":
            print("\nВыход.")
            break

        else:
            print("\nНеверный выбор.")
            input("\nEnter для продолжения...")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
