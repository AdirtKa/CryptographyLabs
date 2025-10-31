import os
import requests
from time import sleep

from generate_keys import generate_keys
from rsa import encrypt, decrypt

API_URL: str = "http://localhost:8080"


def clear_screen() -> None:
    os.system("clear")


def get_server_key() -> tuple[int, int]:
    response = requests.get(f"{API_URL}/public_key")
    data = response.json()
    return data["e"], data["n"]


def send_message(message: list[int]) -> list[int]:
    response = requests.post(f"{API_URL}/decrypt_message", json={"message": message})
    data = response.json()
    return data["message"]


def receive_message(public_key: tuple[int, int]) -> list[int]:
    response = requests.post(f"{API_URL}/encrypt_message", json={"public_key": public_key})
    return response.json()["message"]


def is_english(message: str):
    return all(32 <= ord(char) <= 126 for char in message)


def get_user_message() -> bytes:
    while True:
        clear_screen()
        user_input: str = input("Введите ваше сообщение: ")

        if is_english(user_input):
            return user_input.encode()
        print("Ваше сообщение не должно содержать русских символов")
        sleep(1)


def main() -> None:
    """Entry point."""
    user_input: str = ""
    server_key: tuple[int, int] | None = None
    n, e, d = generate_keys(bits_len=5)
    while True:
        clear_screen()
        print("1 - посмотреть текущие ключи")
        print("2 - сгенерировать новый ключ")
        print("3 - запросить публичный ключ сервера")
        print("4 - отправить зашифрованное сообщение на сервер")
        print("5 - получить шифрованное сообщение с сервера")
        print("6 - выйти")
        user_input = input("Выберите ваше действие: ")
        match user_input:
            case "1":
                print(f"{n=}\n{e=}\n{d=}")
            case "2":
                n, e, d = generate_keys(bits_len=5)
                print("Новые ключи")
                print(f"{n=}\n{e=}\n{d=}")
            case "3":
                server_key: tuple[int, int] = get_server_key()
                print(f"Публичный ключ сервера {server_key}")
            case "4":
                if not server_key:
                    print("Сначала получите ключ от сервера")
                    sleep(1)
                    continue

                message: bytes = get_user_message()
                encrypted_message = encrypt(message, server_key)
                print(f"Зашифрованное сообщение: {encrypted_message}")
                response_message: list[int] = send_message(encrypted_message)
                print(f"Сервер расшифровал: {bytes(response_message)}")
            case "5":
                response_message = receive_message((e, n))
                print(f"Сервер прислал сообщение: {response_message}")
                decrypted_message = decrypt(response_message, (d, n))
                print(f"После расшифровки: {bytes(decrypted_message)}")
            case "6":
                exit(0)

        sleep(1)


if __name__ == '__main__':
    main()
