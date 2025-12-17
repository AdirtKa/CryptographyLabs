from hashlib import sha256
from typing import Union


class HashUtils:
    """Вспомогательные функции для хеширования"""

    @staticmethod
    def hash_message(message: str) -> int:
        """
        Хеширование сообщения с использованием SHA-256

        Args:
            message: Текстовое сообщение

        Returns:
            Целое число (хеш)
        """
        hash_bytes = sha256(message.encode()).digest()
        return int.from_bytes(hash_bytes, 'big')

    @staticmethod
    def hash_file(filepath: str) -> int:
        """
        Хеширование файла

        Args:
            filepath: Путь к файлу

        Returns:
            Целое число (хеш)
        """
        sha256_hash = sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return int.from_bytes(sha256_hash.digest(), 'big')


class FormatUtils:
    """Вспомогательные функции для форматирования"""

    @staticmethod
    def signature_to_hex(r: int, s: int) -> str:
        """Преобразование подписи в hex формат"""
        return f"r:{hex(r)}\ns:{hex(s)}"

    @staticmethod
    def signature_from_hex(hex_str: str) -> tuple:
        """Преобразование из hex формата в подпись"""
        lines = hex_str.strip().split('\n')
        r = int(lines[0].split(':')[1], 16)
        s = int(lines[1].split(':')[1], 16)
        return r, s