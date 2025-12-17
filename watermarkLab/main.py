from watermarkLab.eliptic_curve import EllipticCurve
from watermarkLab.point import Point
from watermarkLab.ecdsa import ECDSA
from watermarkLab.watermark import Watermark
from watermarkLab.utils import HashUtils, FormatUtils


def main():
    """Демонстрация ECDSA с водяным знаком"""

    print("=" * 60)
    print("ECDSA с цифровым водяным знаком - Демонстрация")
    print("=" * 60)

    # 1. Инициализация кривой secp256k1
    print("\n[1] Инициализация кривой secp256k1...")
    curve = EllipticCurve(
        a=0,
        b=7,
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    )
    print(f"✓ Кривая инициализирована: {curve}")

    # 2. Базовая точка (из secp256k1)
    print("\n[2] Установка базовой точки G...")
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    G = Point(Gx, Gy, curve)
    print(f"✓ Базовая точка установлена")

    # 3. Порядок группы
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    # 4. Инициализация ECDSA
    print("\n[3] Инициализация ECDSA...")
    ecdsa = ECDSA(curve, G, n)
    print("✓ ECDSA инициализирована")

    # 5. Генерация ключей
    print("\n[4] Генерация пары ключей...")
    public_key, private_key = ecdsa.generate_keys()
    print(f"✓ Приватный ключ: {hex(private_key)[:16]}...")
    print(f"✓ Публичный ключ сгенерирован")

    # 6. Создание водяного знака
    print("\n[5] Создание водяного знака...")
    watermark = Watermark(owner="Alice", document_id="DOC-2025-001")
    print(f"✓ {watermark}")
    print(f"  Метаданные: {watermark.metadata()}")

    # 7. Подписание сообщения
    print("\n[6] Подписание сообщения...")
    message = "Это важный криптографический документ"
    message_hash = HashUtils.hash_message(message)
    r, s = ecdsa.sign(message_hash, private_key)

    print(f"  Сообщение: '{message}'")
    print(f"  Хеш: {hex(message_hash)[:32]}...")

    # 8. Встраивание водяного знака
    print("\n[7] Встраивание водяного знака в подпись...")
    r_marked, s_marked = watermark.embed_in_signature(r, s)
    print(f"  Оригинальная s: {hex(s)[-16:]}")
    print(f"  Модифицированная s: {hex(s_marked)[-16:]}")

    # 9. Верификация подписи
    print("\n[8] Верификация подписи...")
    is_valid = ecdsa.verify(public_key, message_hash, (r_marked, s_marked))
    status = "✓ ВАЛИДНА" if is_valid else "✗ НЕВАЛИДНА"
    print(f"  Статус подписи: {status}")

    # 10. Извлечение водяного знака
    print("\n[9] Извлечение водяного знака...")
    extracted_watermark = Watermark.extract_from_signature(s_marked)
    embedded_watermark = watermark.encode()

    print(f"  Встроенный водяной знак: {hex(embedded_watermark)}")
    print(f"  Извлечённый водяной знак: {hex(extracted_watermark)}")

    is_watermark_valid = extracted_watermark == embedded_watermark
    print(f"  Проверка: {'✓ Совпадает' if is_watermark_valid else '✗ Не совпадает'}")

    # 11. Форматирование результатов
    print("\n[10] Результаты в hex формате:")
    signature_hex = FormatUtils.signature_to_hex(r_marked, s_marked)
    print(signature_hex)

    print("\n" + "=" * 60)
    print("Демонстрация завершена успешно!")
    print("=" * 60)


if __name__ == "__main__":
    main()