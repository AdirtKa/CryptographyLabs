import os
# from string import ascii_lowercase

# ALPHABET: str = ascii_lowercase + "".join([chr(i) for i in range(ord('а'), ord('я') + 1)]) + " "
ALPHABET: str = "".join([chr(i) for i in range(ord('а'), ord('я') + 1)])
ALPHABET_SIZE: int = len(ALPHABET)


def encrypt(plaintext: str, key: int) -> str:
    plaintext = plaintext.lower()
    positions: list[int] = [ALPHABET.index(letter) if letter in ALPHABET else 0 for letter in plaintext]
    new_positions: list[int] = ([(positions[0] + key) % ALPHABET_SIZE] +
                                [(positions[i] + positions[i - 1]) % ALPHABET_SIZE for i in range(1, len(positions))])

    return "".join(map(lambda x: ALPHABET[x], new_positions))


def decrypt(ciphertext: str, key: int) -> str:
    ciphertext = ciphertext.lower()
    positions: list[int] = [ALPHABET.index(letter) if letter in ALPHABET else 0 for letter in ciphertext]
    new_positions: list[int] = [(positions[0] - key) % ALPHABET_SIZE]
    for i in range(1, len(positions)):
        new_positions.append((positions[i] - new_positions[i - 1]) % ALPHABET_SIZE)
    return "".join(map(lambda x: ALPHABET[x], new_positions))


def get_new_key() -> int:
    while True:
        key: str = input("Введите новый ключ: ")
        if not key.isdigit():
            print("Ключ должен быть целочисленным")
            continue

        return int(key)

    return 0


def main() -> int:
    """Entry point."""
    # plaintext: str = "встречавпонедельник"
    encrypt_key: int = 16

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print("Добро пожаловать в шифратор методом автоматического ключа!")
        print("Выберите действие:")
        print("1. Посмотреть ключи")
        print("2. Изменить ключи")
        print("3. Зашифровать сообщение")
        print("4. Расшифровать сообщение")
        print("5. Выйти")

        choice: str = input("Введите номер действия: ")
        if choice == '1':
            print("Ключи шифрования:")
            print("ключ:", encrypt_key)
            print("Нажмите Enter для продолжения")
            input()
        elif choice == '2':
            encrypt_key = get_new_key()
            print("Ключ принят успешно, нажмите Enter для продолжения")
            input()
        elif choice == '3':
            message = input("Введите сообщение для шифрования: ")
            encrypted_text = encrypt(message, encrypt_key)
            print("Зашифрованное сообщение:", encrypted_text)
            print("Нажмите Enter для продолжения")
            input()
        elif choice == '4':
            encrypted_text = input("Введите зашифрованное сообщение: ")
            decrypted_text = decrypt(encrypted_text, encrypt_key)
            print("Расшифрованное сообщение:", decrypted_text)
            print("Нажмите Enter для продолжения")
            input()
        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор.")

    return 0


if __name__ == '__main__':
    main()
