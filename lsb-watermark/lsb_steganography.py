"""
Модуль для реализации LSB (Least Significant Bit) стеганографии.

LSB метод скрывает данные в наименее значимых битах пикселей изображения,
что делает изменения практически незаметными для человеческого глаза.
"""

from PIL import Image
import numpy as np
from typing import Tuple


class LSBSteganography:
    """Класс для встраивания и извлечения текстовых водяных знаков в изображениях."""

    DELIMITER = "$END$"  # Разделитель для обозначения конца сообщения

    @staticmethod
    def _message_to_binary(message: str) -> str:
        """
        Конвертирует текстовое сообщение в бинарную строку.

        Args:
            message: Текстовое сообщение для конвертации

        Returns:
            Бинарное представление сообщения
        """
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        return binary_message

    @staticmethod
    def _binary_to_message(binary: str) -> str:
        """
        Конвертирует бинарную строку обратно в текст.

        Args:
            binary: Бинарная строка для конвертации

        Returns:
            Текстовое сообщение
        """
        message = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i + 8]
            if len(byte) == 8:
                message += chr(int(byte, 2))
        return message

    def encode(self, image_path: str, message: str, output_path: str) -> Tuple[bool, str]:
        """
        Встраивает сообщение в изображение используя LSB метод.

        Args:
            image_path: Путь к исходному изображению
            message: Сообщение для встраивания
            output_path: Путь для сохранения изображения с водяным знаком

        Returns:
            Tuple (успех, сообщение об ошибке или успехе)
        """
        try:
            # Загружаем изображение
            img = Image.open(image_path)

            # Конвертируем в RGB если необходимо
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Получаем массив пикселей
            pixels = np.array(img)
            height, width, channels = pixels.shape
            total_pixels = height * width * channels

            # Добавляем разделитель к сообщению
            message_with_delimiter = message + self.DELIMITER
            binary_message = self._message_to_binary(message_with_delimiter)
            message_length = len(binary_message)

            # Проверяем, достаточно ли места в изображении
            if message_length > total_pixels:
                return False, f"Сообщение слишком длинное! Максимум {total_pixels // 8} символов, получено {len(message)}"

            # Встраиваем сообщение в LSB пикселей
            flat_pixels = pixels.flatten()
            for i in range(message_length):
                # Изменяем последний бит пикселя
                flat_pixels[i] = (flat_pixels[i] & 0xFE) | int(binary_message[i])

            # Восстанавливаем форму массива
            encoded_pixels = flat_pixels.reshape(height, width, channels)

            # Создаем и сохраняем изображение
            encoded_image = Image.fromarray(encoded_pixels.astype('uint8'), 'RGB')
            encoded_image.save(output_path)

            return True, f"Сообщение успешно встроено! Сохранено в {output_path}"

        except Exception as e:
            return False, f"Ошибка при кодировании: {str(e)}"

    def decode(self, image_path: str) -> Tuple[bool, str]:
        """
        Извлекает скрытое сообщение из изображения.

        Args:
            image_path: Путь к изображению с водяным знаком

        Returns:
            Tuple (успех, извлеченное сообщение или ошибка)
        """
        try:
            # Загружаем изображение
            img = Image.open(image_path)

            # Конвертируем в RGB если необходимо
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Получаем массив пикселей
            pixels = np.array(img)
            flat_pixels = pixels.flatten()

            # Извлекаем биты
            binary_message = ''
            for pixel_value in flat_pixels:
                binary_message += str(pixel_value & 1)

            # Конвертируем биты в текст
            decoded_message = self._binary_to_message(binary_message)

            # Ищем разделитель
            if self.DELIMITER in decoded_message:
                decoded_message = decoded_message[:decoded_message.index(self.DELIMITER)]
                return True, decoded_message
            else:
                return False, "Водяной знак не найден в изображении"

        except Exception as e:
            return False, f"Ошибка при декодировании: {str(e)}"
