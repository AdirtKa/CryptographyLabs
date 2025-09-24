import math

def bytes_to_bits(data: bytes) -> str:
    return ''.join(f"{byte:08b}" for byte in data)

def encrypt(plaintext: bytes, key: bytes) -> bytes:
    key: bytes = key * math.ceil(len(plaintext) // len(key))
    key: bytes = key[:len(plaintext)]
    cipher_bytes: bytearray = bytearray()
    for idx, byte in enumerate(plaintext):
        cipher_bytes.append(byte ^ key[idx])
    return bytes(cipher_bytes)


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    key: bytes = key * math.ceil(len(ciphertext) // len(key))
    key: bytes = key[:len(ciphertext)]
    plain_bytes: bytearray = bytearray()
    for idx, byte in enumerate(ciphertext):
        plain_bytes.append(byte ^ key[idx])
    return bytes(plain_bytes)



def main() -> None:
    key: bytes  = "Даня".encode()
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
            print(f"{key.decode()=}")

        elif choice == "2":
            try:
                key: bytes = input("Введите новый ключ: ").encode()
                
                print("✅ Ключ изменён.")
            except Exception as e:
                print("Ошибка при вводе ключа:", e)

        elif choice == "3":
            text = input("Введите текст для шифрования: ")
            if not text:
                print("Пустой ввод.")
                continue

            ciphertext = encrypt(text.encode(), key)

            print("Шифротекст:", ciphertext.decode())
            print("🔒 Шифротекст (hex):", ciphertext.hex())
            print("🔒 Шифротекст (bin):", bytes_to_bits(ciphertext))

        elif choice == "4":
            hex_str = input("Введите шифротекст в hex: ").strip()
            try:
                ciphertext = bytes.fromhex(hex_str)
            except ValueError:
                print("Ошибка: некорректный hex.")
                continue

            text = decrypt(ciphertext, key)
            print("📜 Расшифровка:", text.decode())

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()