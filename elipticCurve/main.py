import hashlib
from typing import Tuple
from elipticCurve.ECELGamal import EllipticCurve, Point, ECElGamal, PointEncoder
from hash.sha256 import SHA256


class MessageHasher:
    """Класс для хеширования сообщений с помощью SHA-256"""

    @staticmethod
    def hash_message(message: str) -> int:
        """
        Хеширование строкового сообщения в целое число

        Args:
            message: Строка сообщения

        Returns:
            Целое число (256-битный хеш)
        """
        message_bytes = message.encode('utf-8')
        sha256 = SHA256()
        sha256.update(message_bytes)
        return sha256.decdigest()
        # hash_object = hashlib.sha256(message_bytes)
        # return int.from_bytes(hash_object.digest(), byteorder='big')

    @staticmethod
    def hash_message_hex(message: str) -> str:
        """
        Хеширование сообщения с возвращением в формате hex

        Args:
            message: Строка сообщения

        Returns:
            Хеш в формате hex строки
        """
        message_bytes = message.encode('utf-8')
        hash_object = hashlib.sha256(message_bytes)
        return hash_object.hexdigest()


class ECElGamalInterface:
    """Интерфейс командной строки для работы с криптосистемой Эль-Гамаля на эллиптической кривой"""

    def __init__(self):
        """Инициализация интерфейса и криптосистемы"""
        # Инициализируем кривую с параметрами secp256k1
        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        a = 0
        b = 7

        self.curve = EllipticCurve(a, b, p)

        # Базовая точка (координаты из secp256k1)
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        self.G = Point(Gx, Gy, self.curve)

        # Порядок группы
        self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

        # Криптосистема
        self.elgamal = ECElGamal(self.curve, self.G, self.n)

        # Данные для хранения зашифрованных сообщений
        self.encrypted_messages = []

        # Данные для хранения подписанных сообщений
        self.signed_messages = []

    def print_separator(self, char: str = "=", length: int = 70):
        """Печать разделителя"""
        print(char * length)

    def print_menu(self):
        """Вывод главного меню"""
        print()
        self.print_separator()
        print("Криптосистема Эль-Гамаля на эллиптической кривой")
        self.print_separator()
        print("1. Сгенерировать новую пару ключей")
        print("2. Посмотреть текущие ключи")
        print("3. Зашифровать сообщение (EC-ElGamal)")
        print("4. Расшифровать сообщение (EC-ElGamal)")
        print("5. Подписать сообщение (ECDSA)")
        print("6. Верифицировать подпись (ECDSA)")
        print("7. Выход")
        print("-" * 70)

    def generate_keys(self):
        """Генерация новой пары ключей"""
        print("\n[INFO] Генерирую новую пару ключей...")
        public_key, private_key = self.elgamal.generate_keys()
        print("✓ Новая пара ключей успешно сгенерирована!")

    def view_keys(self):
        """Просмотр текущих ключей"""
        if self.elgamal.private_key is None:
            print("\n[ОШИБКА] Ключи еще не сгенерированы. Пожалуйста, сгенерируйте их первым.")
            return

        print("\n" + "-" * 70)
        print("ИНФОРМАЦИЯ О КЛЮЧАХ")
        print("-" * 70)

        print(f"\nЗакрытый ключ (d):")
        print(f"  {hex(self.elgamal.private_key)}")

        print(f"\nОткрытый ключ (Q = d*G):")
        print(f"  X: {hex(self.elgamal.public_key.x)}")
        print(f"  Y: {hex(self.elgamal.public_key.y)}")

        print(f"\nПараметры эллиптической кривой:")
        print(f"  Уравнение: y² = x³ + {self.curve.a}x + {self.curve.b} mod p")
        print(f"  p = {hex(self.curve.p)}")
        print(f"  n = {hex(self.n)}")

        print("-" * 70)

    def encrypt_message(self):
        """Шифрование сообщения"""
        if self.elgamal.public_key is None:
            print("\n[ОШИБКА] Ключи еще не сгенерированы. Пожалуйста, сгенерируйте их первым.")
            return

        print("\n" + "-" * 70)
        print("ШИФРОВАНИЕ СООБЩЕНИЯ (EC-ElGamal)")
        print("-" * 70)

        message = input("\nВведите сообщение для шифрования: ")

        if not message:
            print("[ОШИБКА] Сообщение не может быть пустым.")
            return

        print("\n[INFO] Кодирую сообщение в точку эллиптической кривой...")
        message_point = PointEncoder.encode_message(message, self.curve)

        if message_point is None:
            print("[ОШИБКА] Не удалось закодировать сообщение.")
            return

        print(f"✓ Сообщение закодировано в точку:")
        print(f"  X: {hex(message_point.x)}")
        print(f"  Y: {hex(message_point.y)}")

        print("\n[INFO] Шифрую сообщение...")
        C1, C2 = self.elgamal.encrypt(message_point, self.elgamal.public_key)

        print("✓ Сообщение успешно зашифровано!")
        print(f"\nШифротекст (C1, C2):")
        print(f"\nC1 (k*G):")
        print(f"  X: {hex(C1.x)}")
        print(f"  Y: {hex(C1.y)}")
        print(f"\nC2 (M + k*Q):")
        print(f"  X: {hex(C2.x)}")
        print(f"  Y: {hex(C2.y)}")

        # Сохраняем зашифрованное сообщение
        self.encrypted_messages.append({
            'original': message,
            'message_point': message_point,
            'C1': C1,
            'C2': C2
        })

        print(f"\n[INFO] Сообщение сохранено (ID: {len(self.encrypted_messages) - 1})")
        print("-" * 70)

    def decrypt_message(self):
        """Расшифрование сообщения"""
        if self.elgamal.private_key is None:
            print("\n[ОШИБКА] Ключи еще не сгенерированы. Пожалуйста, сгенерируйте их первым.")
            return

        if not self.encrypted_messages:
            print("\n[ОШИБКА] Нет зашифрованных сообщений. Сначала зашифруйте что-то.")
            return

        print("\n" + "-" * 70)
        print("РАСШИФРОВАНИЕ СООБЩЕНИЯ (EC-ElGamal)")
        print("-" * 70)

        print("\nДоступные зашифрованные сообщения:")
        for idx, msg in enumerate(self.encrypted_messages):
            print(f"  {idx}. '{msg['original']}'")

        try:
            msg_id = int(input("\nВыберите ID сообщения для расшифрования: "))
            if msg_id < 0 or msg_id >= len(self.encrypted_messages):
                print("[ОШИБКА] Неверный ID сообщения.")
                return
        except ValueError:
            print("[ОШИБКА] Введите корректный номер.")
            return

        encrypted_msg = self.encrypted_messages[msg_id]
        C1 = encrypted_msg['C1']
        C2 = encrypted_msg['C2']
        original_point = encrypted_msg['message_point']

        print(f"\n[INFO] Расшифровываю сообщение...")
        decrypted_point = self.elgamal.decrypt(C1, C2)

        print("✓ Сообщение успешно расшифровано!")

        print(f"\nРасшифрованная точка:")
        print(f"  X: {hex(decrypted_point.x)}")
        print(f"  Y: {hex(decrypted_point.y)}")

        # Проверяем корректность
        if decrypted_point == original_point:
            print("\n✓ ВЕРИФИКАЦИЯ ПРОЙДЕНА!")
            print(f"  Расшифрованная точка совпадает с исходной.")
            print(f"  Исходное сообщение: '{encrypted_msg['original']}'")
        else:
            print("\n✗ ОШИБКА ВЕРИФИКАЦИИ!")
            print(f"  Расшифрованная точка НЕ совпадает с исходной.")

        print("-" * 70)

    def sign_message(self):
        """Подписание сообщения с помощью ECDSA"""
        if self.elgamal.private_key is None:
            print("\n[ОШИБКА] Ключи еще не сгенерированы. Пожалуйста, сгенерируйте их первым.")
            return

        print("\n" + "-" * 70)
        print("ПОДПИСАНИЕ СООБЩЕНИЯ (ECDSA)")
        print("-" * 70)

        message = input("\nВведите сообщение для подписания: ")

        if not message:
            print("[ОШИБКА] Сообщение не может быть пустым.")
            return

        print("\n[INFO] Вычисляю SHA-256 хеш сообщения...")
        message_hash_hex = MessageHasher.hash_message(message) % self.n
        print(f"✓ SHA-256 хеш (hex): {message_hash_hex}")

        print("\n[INFO] Подписываю сообщение с помощью ECDSA...")
        signature = self.elgamal.sign(message_hash_hex, self.elgamal.private_key)
        r, s = signature

        print("✓ Сообщение успешно подписано!")
        print(f"\nПодпись ECDSA (r, s):")
        print(f"  r = {r}")
        print(f"  s = {s}")

        # Сохраняем подписанное сообщение
        self.signed_messages.append({
            'message': message,
            'message_hash': message_hash_hex,
            'signature': signature,
            'public_key': self.elgamal.public_key
        })

        print(f"\n[INFO] Подпись сохранена (ID: {len(self.signed_messages) - 1})")
        print("-" * 70)

    def verify_signature(self):
        """Верификация подписи сообщения"""
        if not self.signed_messages:
            print("\n[ОШИБКА] Нет подписанных сообщений. Сначала подпишите что-то.")
            return

        print("\n" + "-" * 70)
        print("ВЕРИФИКАЦИЯ ПОДПИСИ (ECDSA)")
        print("-" * 70)

        print("\nДоступные подписанные сообщения:")
        for idx, msg in enumerate(self.signed_messages):
            print(f"  {idx}. '{msg['message']}'")

        try:
            msg_id = int(input("\nВыберите ID сообщения для верификации: "))
            if msg_id < 0 or msg_id >= len(self.signed_messages):
                print("[ОШИБКА] Неверный ID сообщения.")
                return
        except ValueError:
            print("[ОШИБКА] Введите корректный номер.")
            return

        signed_msg = self.signed_messages[msg_id]
        message = signed_msg['message']
        message_hash = signed_msg['message_hash']
        signature = signed_msg['signature']
        public_key = signed_msg['public_key']

        print(f"\n[INFO] Верифицирую подпись для сообщения: '{message}'")

        # Верифицируем подпись
        is_valid = self.elgamal.verify(public_key, message_hash, signature)

        print("-" * 70)

        if is_valid:
            print("\n✓ ПОДПИСЬ ВАЛИДНА!")
            print("  Сообщение не было изменено и подписано правильным ключом.")
        else:
            print("\n✗ ПОДПИСЬ НЕВАЛИДНА!")
            print("  Сообщение было изменено или подпись некорректна.")

        # Попытаемся верифицировать с измененным сообщением
        print("\n[INFO] Проверяю, что подпись отвергает измененное сообщение...")
        fake_message = message + " (подделано)"
        fake_message_hash = MessageHasher.hash_message(fake_message) % self.n
        is_fake_valid = self.elgamal.verify(public_key, fake_message_hash, signature)

        if not is_fake_valid:
            print("✓ Измененное сообщение корректно отвергнуто!")
        else:
            print("✗ ОШИБКА: Измененное сообщение прошло верификацию!")

        print("-" * 70)

    def run(self):
        """Главный цикл интерфейса"""
        print("\n")
        self.print_separator("*")
        print("Добро пожаловать в криптосистему Эль-Гамаля на эллиптической кривой!")
        print("Система инициализирована с параметрами кривой secp256k1")
        print("Поддерживает шифрование, расшифрование и цифровые подписи (ECDSA)")
        self.print_separator("*")

        while True:
            self.print_menu()
            choice = input("Выберите действие (1-7): ").strip()

            if choice == "1":
                self.generate_keys()
            elif choice == "2":
                self.view_keys()
            elif choice == "3":
                self.encrypt_message()
            elif choice == "4":
                self.decrypt_message()
            elif choice == "5":
                self.sign_message()
            elif choice == "6":
                self.verify_signature()
            elif choice == "7":
                print("\n" + "=" * 70)
                print("Спасибо за использование криптосистемы. До свидания!")
                print("=" * 70 + "\n")
                break
            else:
                print("\n[ОШИБКА] Неверный выбор. Пожалуйста, выберите опцию от 1 до 7.")


if __name__ == "__main__":
    app = ECElGamalInterface()
    app.run()