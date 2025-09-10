from random import shuffle
import os


def get_decrypt_key(encrypt_key: list[int]) -> list[int]:

    decrypt_key: list[int] = [0] * len(encrypt_key)
    for idx, val in enumerate(encrypt_key):
        decrypt_key[val] = idx

    return decrypt_key


def add_letters(text: str, block_len: int) -> tuple[str, int]:
    letters_to_add: int = block_len - (len(text) % block_len)
    if letters_to_add != block_len:
        text = text + " " * letters_to_add
    return text, letters_to_add % block_len


def break_apart(text: str, block_len: int) -> list[str]:
    parts: list[str] = [text[i: i+block_len] for i in range(0, len(text), block_len)]
    return parts


def encrypt_part(part: str, encrypt_key: list[int]) -> str:
    encrypted_part: str = ""
    for idx in range(len(part)):
        encrypted_part += part[encrypt_key[idx]]
    return encrypted_part



def encrypt(text: str, encrypt_key: list[int]) -> tuple[str, int]:
    text, added_letters = add_letters(text, len(encrypt_key))
    parts: list[str] = break_apart(text, len(encrypt_key))
    encrypted_parts= list(map(lambda x: encrypt_part(x, encrypt_key), parts))
    return "".join(encrypted_parts), added_letters


def decrypt(text: str, encrypt_key: list[int]) -> str:
    decrypt_key: list[int] = get_decrypt_key(encrypt_key)
    decrypted_text = encrypt(text, decrypt_key)
    return decrypted_text

def get_new_key():
    print("Введите новый ключ, он должен состоять из последовательных чисел\n" \
    "От 0 до n - 1 в произвольном порядке (например 03124)")
    while True:
        new_key: str = input()
        if not new_key.isdigit():
            print("Вы ввели что-то помимо числа, попробуйте еще")
            continue

        new_key_list: list[int] = list(map(int, new_key))
        for num in new_key_list:
            if num < 0 or num > len(new_key_list) - 1:
                print("Вы пропустили какое-то из чисел, попробуйте еще")
                break
        else:
            break

    return new_key_list

def main() -> int:
    encrypt_key: list[int] = list(range(0, 4))
    shuffle(encrypt_key)

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print("Добро пожаловать в шифратор методом перестановки!")
        print("Выберите действие:")
        print("1. Посмотреть ключи")
        print("2. Изменить ключи")
        print("3. Зашифровать сообщение")
        print("4. Расшифровать сообщение")
        print("5. Выйти")

        choice: int = int(input("Введите номер действия: "))
        if choice == 1:
            print("Ключи шифрования:")
            print("Перестановочный ключ")
            print(*range(0, len(encrypt_key)))
            print(*encrypt_key)
            print("Нажмите Enter для продолжения")
            input()
        elif choice == 2:
            encrypt_key = get_new_key()
            print("Ключ принят успешно, нажмите Enter для продолжения")
            input()
        elif choice == 3:
            message = input("Введите сообщение для шифрования: ")
            encrypted_text, added_letters = encrypt(message, encrypt_key)
            print("Зашифрованное сообщение:", encrypted_text)
            print("Нажмите Enter для продолжения")
            input()
        elif choice == 4:
            encrypted_text = input("Введите зашифрованное сообщение: ")
            decrypted_text, _ = decrypt(encrypted_text, encrypt_key)
            print("Расшифрованное сообщение:", decrypted_text)
            print("Нажмите Enter для продолжения")
            input()
        elif choice == 5:
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор.")

    return 0


if __name__ == "__main__":
    main()