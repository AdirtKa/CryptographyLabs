import math
import os
import random
import string

alphabet = string.ascii_lowercase
n = len(alphabet)


def gen_keys():
    a = random.randint(2, n - 1)
    while math.gcd(a, n) != 1:
        a += 1
    b = random.randint(0, n - 1)
    return a, b


def encrypt(msg, a, b):
    out = ""
    for ch in msg:
        if ch in alphabet:
            out += alphabet[(a * alphabet.index(ch) + b) % n]
        elif ch.lower() in alphabet:
            out += alphabet[(a * alphabet.index(ch.lower()) + b) % n].upper()
        else:
            out += ch
    return out


def decrypt(msg, a, b):
    out, a_inv = "", pow(a, -1, n)
    for ch in msg:
        if ch in alphabet:
            out += alphabet[(a_inv * (alphabet.index(ch) - b)) % n]
        elif ch.lower() in alphabet:
            out += alphabet[(a_inv * (alphabet.index(ch.lower()) - b)) % n].upper()
        else:
            out += ch
    return out


def main():
    a, b = gen_keys()
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Аффинный шифр (алфавит a-z). Текущие ключи: a={a}, b={b}")
        print("1. Зашифровать сообщение")
        print("2. Расшифровать сообщение")
        print("3. Сгенерировать новые ключи")
        print("4. Выйти")
        c = input("Ваш выбор: ")
        if c == "1":
            m = input("Введите текст: ")
            print("Шифротекст:", encrypt(m, a, b))
            input("Enter...")
        elif c == "2":
            m = input("Введите шифротекст: ")
            print("Расшифровка:", decrypt(m, a, b))
            input("Enter...")
        elif c == "3":
            a, b = gen_keys()
        elif c == "4":
            break


if __name__ == "__main__":
    main()
