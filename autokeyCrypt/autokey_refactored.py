from __future__ import annotations

import os
from typing import List

# Базовый алфавит: русские строчные буквы
ALPHABET: str = "".join(chr(i) for i in range(ord("а"), ord("я") + 1))
ALPHABET_SIZE: int = len(ALPHABET)

# Быстрые отображения для O(1) доступа
CHAR2IDX: dict[str, int] = {ch: i for i, ch in enumerate(ALPHABET)}
IDX2CHAR: List[str] = list(ALPHABET)


def _normalize(text: str) -> str:
    """Приводит текст к нижнему регистру (остальная логика не меняется)."""
    return text.lower()


def _to_positions(text: str) -> List[int]:
    """
    Преобразует строку в список индексов по ALPHABET.
    Символы вне алфавита маппятся в 0 (как в исходной версии).
    """
    return [CHAR2IDX.get(ch, 0) for ch in text]


def _from_positions(positions: List[int]) -> str:
    """Собирает строку из индексов по ALPHABET (mod ALPHABET_SIZE)."""
    return "".join(IDX2CHAR[p % ALPHABET_SIZE] for p in positions)


def encrypt(plaintext: str, key: int) -> str:
    """
    Шифрует текст.
    Первая позиция сдвигается на key, далее к каждой позиции прибавляется предыдущая зашифрованная.
    """
    pt = _normalize(plaintext)
    pos = _to_positions(pt)
    if not pos:
        return ""

    new_pos = [0] * len(pos)
    new_pos[0] = (pos[0] + key) % ALPHABET_SIZE
    for i in range(1, len(pos)):
        new_pos[i] = (pos[i] + pos[i - 1]) % ALPHABET_SIZE

    return _from_positions(new_pos)


def decrypt(ciphertext: str, key: int) -> str:
    """
    Расшифровывает текст, инвертируя рекуррентную формулу из encrypt.
    """
    ct = _normalize(ciphertext)
    pos = _to_positions(ct)
    if not pos:
        return ""

    new_pos = [0] * len(pos)
    new_pos[0] = (pos[0] - key) % ALPHABET_SIZE
    for i in range(1, len(pos)):
        new_pos[i] = (pos[i] - new_pos[i - 1]) % ALPHABET_SIZE

    return _from_positions(new_pos)


def _input_int(prompt: str) -> int:
    """Безопасный ввод целого числа."""
    while True:
        raw = input(prompt).strip()
        if raw.lstrip("-").isdigit():
            return int(raw)
        print("Ошибка: введите целое число.")


def get_new_key() -> int:
    """Запрашивает у пользователя новый целочисленный ключ."""
    return _input_int("Введите новый ключ: ")


def _clear_screen() -> None:
    """Очищает консоль (по возможности)."""
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass


def main() -> int:
    """Точка входа CLI."""
    encrypt_key: int = 16

    while True:
        _clear_screen()
        print("Добро пожаловать в шифратор (рекуррентный мод по русскому алфавиту)!")
        print("1. Посмотреть ключ")
        print("2. Изменить ключ")
        print("3. Зашифровать сообщение")
        print("4. Расшифровать сообщение")
        print("5. Выйти")

        choice = _input_int("Введите номер действия: ")

        if choice == 1:
            print(f"Текущий ключ: {encrypt_key}")
            input("Enter для продолжения...")
        elif choice == 2:
            encrypt_key = get_new_key()
            print("Ключ обновлён.")
            input("Enter для продолжения...")
        elif choice == 3:
            message = input("Введите сообщение для шифрования: ")
            print("Зашифрованное сообщение:", encrypt(message, encrypt_key))
            input("Enter для продолжения...")
        elif choice == 4:
            cipher = input("Введите зашифрованное сообщение: ")
            print("Расшифрованное сообщение:", decrypt(cipher, encrypt_key))
            input("Enter для продолжения...")
        elif choice == 5:
            print("Выход.")
            return 0
        else:
            print("Неверный выбор.")
            input("Enter для продолжения...")

    # Теоретически недостижимо
    # return 0


if __name__ == "__main__":
    raise SystemExit(main())
