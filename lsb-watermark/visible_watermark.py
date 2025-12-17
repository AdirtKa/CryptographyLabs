"""
Модуль для создания видимых водяных знаков на изображениях.

Поддерживает различные стили размещения: одиночный, диагональный,
сетка по всему изображению.
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
import math


class VisibleWatermark:
    """Класс для добавления видимых водяных знаков на изображения."""

    @staticmethod
    def _get_font(size: int = 36) -> ImageFont.FreeTypeFont:
        """
        Получает шрифт для водяного знака.

        Args:
            size: Размер шрифта

        Returns:
            Объект шрифта
        """
        try:
            # Попытка использовать системные шрифты
            font = ImageFont.truetype("arial.ttf", size)
        except OSError:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
            except OSError:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
                except OSError:
                    # Используем шрифт по умолчанию если не найден
                    font = ImageFont.load_default()
        return font

    def add_watermark(
            self,
            image_path: str,
            text: str,
            output_path: str,
            position: str = "bottom-right",
            opacity: int = 128,
            font_size: int = 36,
            color: Tuple[int, int, int] = (255, 255, 255)
    ) -> Tuple[bool, str]:
        """
        Добавляет видимый водяной знак на изображение.

        Args:
            image_path: Путь к исходному изображению
            text: Текст водяного знака
            output_path: Путь для сохранения
            position: Позиция ('bottom-right', 'bottom-left', 'top-right',
                     'top-left', 'center', 'diagonal', 'grid')
            opacity: Прозрачность (0-255, где 0 - полностью прозрачный)
            font_size: Размер шрифта
            color: Цвет текста (R, G, B)

        Returns:
            Tuple (успех, сообщение)
        """
        try:
            # Открываем изображение
            img = Image.open(image_path).convert('RGBA')

            if position == 'grid':
                # Водяной знак сеткой
                result = self._add_grid_watermark(img, text, opacity, font_size, color)
            elif position == 'diagonal':
                # Диагональный водяной знак
                result = self._add_diagonal_watermark(img, text, opacity, font_size, color)
            else:
                # Одиночный водяной знак
                result = self._add_single_watermark(img, text, position, opacity, font_size, color)

            # Конвертируем обратно в RGB и сохраняем
            if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
                result = result.convert('RGB')

            result.save(output_path)
            return True, f"Водяной знак успешно добавлен! Сохранено в {output_path}"

        except Exception as e:
            return False, f"Ошибка при добавлении водяного знака: {str(e)}"

    def _add_single_watermark(
            self,
            img: Image.Image,
            text: str,
            position: str,
            opacity: int,
            font_size: int,
            color: Tuple[int, int, int]
    ) -> Image.Image:
        """Добавляет одиночный водяной знак в указанную позицию."""
        # Создаем прозрачный слой
        txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # Получаем шрифт
        font = self._get_font(font_size)

        # Получаем размер текста
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Вычисляем позицию
        margin = 10
        width, height = img.size

        positions = {
            'bottom-right': (width - text_width - margin, height - text_height - margin),
            'bottom-left': (margin, height - text_height - margin),
            'top-right': (width - text_width - margin, margin),
            'top-left': (margin, margin),
            'center': ((width - text_width) // 2, (height - text_height) // 2)
        }

        x, y = positions.get(position, positions['bottom-right'])

        # Рисуем текст с прозрачностью
        draw.text((x, y), text, font=font, fill=(*color, opacity))

        # Комбинируем слои
        return Image.alpha_composite(img, txt_layer)

    def _add_diagonal_watermark(
            self,
            img: Image.Image,
            text: str,
            opacity: int,
            font_size: int,
            color: Tuple[int, int, int]
    ) -> Image.Image:
        """Добавляет диагональный водяной знак через все изображение."""
        # Создаем прозрачный слой
        txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # Получаем шрифт
        font = self._get_font(font_size)

        # Получаем размер текста
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Позиция в центре
        width, height = img.size
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Рисуем текст
        draw.text((x, y), text, font=font, fill=(*color, opacity))

        # Поворачиваем слой на 45 градусов
        angle = 45
        txt_layer = txt_layer.rotate(angle, expand=False)

        # Комбинируем слои
        return Image.alpha_composite(img, txt_layer)

    def _add_grid_watermark(
            self,
            img: Image.Image,
            text: str,
            opacity: int,
            font_size: int,
            color: Tuple[int, int, int]
    ) -> Image.Image:
        """Добавляет водяной знак сеткой по всему изображению."""
        # Создаем прозрачный слой
        txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # Получаем шрифт (меньший размер для сетки)
        font = self._get_font(font_size // 2)

        # Получаем размер текста
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Расстояние между водяными знаками
        h_spacing = text_width + 100
        v_spacing = text_height + 100

        width, height = img.size

        # Рисуем сетку водяных знаков
        for y in range(-v_spacing, height + v_spacing, v_spacing):
            for x in range(-h_spacing, width + h_spacing, h_spacing):
                draw.text((x, y), text, font=font, fill=(*color, opacity // 2))

        # Поворачиваем на 30 градусов для лучшего эффекта
        txt_layer = txt_layer.rotate(30, expand=False)

        # Комбинируем слои
        return Image.alpha_composite(img, txt_layer)
