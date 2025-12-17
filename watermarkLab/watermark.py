from typing import Tuple, Dict, Optional
from hashlib import sha256, md5
from datetime import datetime
import json


class Watermark:
    """
    Класс для встраивания и извлечения цифровых водяных знаков в ECDSA подписи
    """

    WATERMARK_SIZE = 16  # Размер водяного знака в битах
    WATERMARK_MASK = (1 << WATERMARK_SIZE) - 1

    def __init__(self, owner: str, document_id: str = ""):
        """
        Инициализация водяного знака

        Args:
            owner: Имя владельца/автора
            document_id: Идентификатор документа (опционально)
        """
        self.owner = owner
        self.document_id = document_id
        self.created_at = datetime.now()

    def encode(self) -> int:
        """
        Кодирование информации владельца в целое число

        Returns:
            Закодированное значение водяного знака (16 бит)
        """
        # Комбинируем информацию владельца
        data = f"{self.owner}:{self.document_id}:{self.created_at.timestamp()}"

        # Хешируем и берём младшие 16 бит
        hash_value = int(md5(data.encode()).hexdigest(), 16)
        return hash_value & self.WATERMARK_MASK

    def embed_in_signature(self, r: int, s: int) -> Tuple[int, int]:
        """
        Встраивание водяного знака в компоненты подписи

        Args:
            r: Первый компонент подписи
            s: Второй компонент подписи

        Returns:
            Модифицированная подпись (r', s')
        """
        watermark_value = self.encode()

        # Встраиваем в младшие биты s
        s_modified = (s & ~self.WATERMARK_MASK) | watermark_value

        return r, s_modified

    @staticmethod
    def extract_from_signature(s: int) -> int:
        """
        Извлечение водяного знака из подписи

        Args:
            s: Компонент подписи

        Returns:
            Извлечённый водяной знак
        """
        return s & Watermark.WATERMARK_MASK

    def metadata(self) -> Dict:
        """
        Метаданные водяного знака

        Returns:
            Словарь с информацией
        """
        return {
            "owner": self.owner,
            "document_id": self.document_id,
            "created_at": self.created_at.isoformat(),
            "watermark_value": self.encode()
        }

    def __repr__(self) -> str:
        return f"Watermark(owner='{self.owner}', id='{self.document_id}')"