from LFSR import LFSR


def bytes_to_bits(data: bytes) -> str:
    return ''.join(f"{byte:08b}" for byte in data)


def encrypt(plaintext: str, lfsr: LFSR) -> bytes:
    """Шифрует строку с помощью LFSR и XOR."""
    string_bytes = plaintext.encode("utf-8")
    bits_in_byte: int = 8
    keystream = lfsr.bits(len(string_bytes) * bits_in_byte)
    encrypted: bytearray = bytearray()
    for byte in string_bytes:
        new_byte: int = 0
        for i in range(bits_in_byte):
            cipher_bit = ((byte >> i) & 1) ^ next(keystream)
            new_byte |= cipher_bit << i
        encrypted.append(new_byte)

    return bytes(encrypted)


def decrypt(ciphertext: bytes, lfsr: LFSR) -> str:
    """Расшифровка: повторяем XOR с тем же LFSR."""
    bits_in_byte: int = 8
    keystream = lfsr.bits(len(ciphertext) * bits_in_byte)
    decrypted: bytearray = bytearray()
    for byte in ciphertext:
        new_byte: int = 0
        for i in range(bits_in_byte):
            plain_bit = ((byte >> i) & 1) ^ next(keystream)
            new_byte |= plain_bit << i
        decrypted.append(new_byte)

    return decrypted.decode("utf-8")


def main():
    # значения по умолчанию
    seed = 0b1011
    taps = [0, 1]

    while True:
        print("\n=== LFSR Cipher ===")
        print("1. Показать ключ")
        print("2. Сменить ключ")
        print("3. Зашифровать текст")
        print("4. Расшифровать текст (hex)")
        print("0. Выход")

        choice = input("> ").strip()

        if choice == "0":
            print("Выход.")
            break

        elif choice == "1":
            print(f"состояние = {bin(seed)} ({seed})")
            print(f"биты обратной связи = {taps}")

        elif choice == "2":
            try:
                seed_str = input("Начальное состояние (в двоичном формате, напр. 1011): ").strip()
                seed = int(seed_str, 2)
                length = len(seed_str)
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

            lfsr = LFSR(seed, taps)
            ciphertext = encrypt(text, lfsr)

            print("🔒 Шифротекст (hex):", ciphertext.hex())
            print("🔒 Шифротекст (bin):", bytes_to_bits(ciphertext))

        elif choice == "4":
            hex_str = input("Введите шифротекст в hex: ").strip()
            try:
                ciphertext = bytes.fromhex(hex_str)
            except ValueError:
                print("Ошибка: некорректный hex.")
                continue

            lfsr = LFSR(seed, taps)
            text = decrypt(ciphertext, lfsr)
            print("📜 Расшифровка:", text)

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
