from LFSR import LFSR


def text_to_bits(s: str) -> list[int]:
    """Кодирует каждый символ строки как последовательность битов."""
    return [int(b) for ch in s.encode("utf-8") for b in f"{ch:08b}"]


def bits_to_text(bits: list[int]) -> str:
    """Кодирует каждые восемь битов как одну букву."""
    b = bytes(int("".join(str(x) for x in bits[i:i+8]), 2)
              for i in range(0, len(bits), 8))
    return b.decode("utf-8")


def xor_bits(a: list[int], b: list[int]) -> list[int]:
    """Производит взаимоисключающее или для соответственных битов каждого массива."""
    return [x ^ y for x, y in zip(a, b)]


def main():
    # значения по умолчанию
    length = 4
    seed = 0b1011
    taps = [0, 1]

    while True:
        print("\n=== LFSR Cipher ===")
        print("1. Показать ключ")
        print("2. Сменить ключ")
        print("3. Зашифровать текст")
        print("4. Расшифровать текст")
        print("0. Выход")

        choice = input("> ").strip()

        if choice == "0":
            print("Выход.")
            break

        elif choice == "1":
            print(f"length = {length}")
            print(f"seed   = {bin(seed)} ({seed})")
            print(f"taps   = {taps}")

        elif choice == "2":
            try:
                length = int(input("Длина регистра: "))
                seed_str = input("Начальное состояние (в двоичном формате, напр. 1011): ").strip()
                seed = int(seed_str, 2)
                taps_str = input("Taps (через запятую, индексы 0=LSB): ").strip()
                taps = [int(x) for x in taps_str.split(",") if x.strip()]

                if length <= 0:
                    print("Ошибка: длина должна быть > 0")
                    continue
                if not (0 < seed < (1 << length)):
                    print("Ошибка: seed должен быть в диапазоне 1..2^length-1")
                    continue
                if any(t < 0 or t >= length for t in taps):
                    print(f"Ошибка: taps должны быть в диапазоне [0,{length - 1}]")
                    continue

                print("✅ Ключ изменён.")
            except Exception as e:
                print("Ошибка при вводе ключа:", e)

        elif choice == "3":
            text = input("Введите текст для шифрования: ")
            if not text:
                print("Пустой ввод.")
                continue

            lfsr = LFSR(length, seed, taps)
            bits = text_to_bits(text)
            ks = lfsr.keystream(len(bits))
            cipher_bits = xor_bits(bits, ks)
            print("🔒 Шифротекст (биты):")
            print("".join(map(str, cipher_bits)))

        elif choice == "4":
            cipher_str = input("Введите битовую строку (только 0 и 1): ").strip()
            if not cipher_str or any(ch not in "01" for ch in cipher_str):
                print("Ошибка: введите строку только из 0 и 1.")
                continue

            bits = [int(b) for b in cipher_str]
            lfsr = LFSR(length, seed, taps)
            ks = lfsr.keystream(len(bits))
            plain_bits = xor_bits(bits, ks)

            try:
                text = bits_to_text(plain_bits)
                print("📜 Расшифровка:", text)
            except Exception:
                print("Не удалось декодировать в текст.")

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()

if __name__ == '__main__':
    main()
