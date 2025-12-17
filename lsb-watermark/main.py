"""
Точка входа приложения LSB Водяной знак.

Запускает графический интерфейс для встраивания и извлечения
водяных знаков из изображений методом LSB стеганографии.
"""

import tkinter as tk
from gui import WatermarkGUI


def main():
    """Главная функция приложения."""
    root = tk.Tk()
    app = WatermarkGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
