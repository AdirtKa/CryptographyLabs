"""
Графический интерфейс для LSB и видимой стеганографии.

Предоставляет простой интерфейс для встраивания и извлечения
водяных знаков из изображений (скрытых и видимых).
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from lsb_steganography import LSBSteganography
from visible_watermark import VisibleWatermark
import os


class WatermarkGUI:
    """Класс GUI для приложения водяных знаков."""

    def __init__(self, root: tk.Tk):
        """
        Инициализирует графический интерфейс.

        Args:
            root: Корневое окно Tkinter
        """
        self.root = root
        self.root.title("Водяные знаки - LSB & Видимые")
        self.root.geometry("650x600")
        self.root.resizable(False, False)

        self.lsb_steganography = LSBSteganography()
        self.visible_watermark = VisibleWatermark()

        self._create_widgets()

    def _create_widgets(self):
        """Создает все виджеты интерфейса."""
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="Водяные знаки на изображениях",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()

        # Создаем вкладки
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Вкладка видимых водяных знаков
        visible_frame = ttk.Frame(notebook)
        notebook.add(visible_frame, text="Видимый водяной знак")
        self._create_visible_tab(visible_frame)

        # Вкладка LSB кодирования
        encode_frame = ttk.Frame(notebook)
        notebook.add(encode_frame, text="Скрытый - Встроить (LSB)")
        self._create_encode_tab(encode_frame)

        # Вкладка LSB декодирования
        decode_frame = ttk.Frame(notebook)
        notebook.add(decode_frame, text="Скрытый - Извлечь (LSB)")
        self._create_decode_tab(decode_frame)

    def _create_visible_tab(self, parent: ttk.Frame):
        """Создает вкладку для видимых водяных знаков."""
        # Фрейм для выбора файла
        file_frame = ttk.LabelFrame(parent, text="Выбор изображения", padding=10)
        file_frame.pack(fill='x', padx=10, pady=10)

        self.visible_file_label = tk.Label(file_frame, text="Файл не выбран", fg="gray")
        self.visible_file_label.pack(side='left', expand=True)

        select_btn = ttk.Button(
            file_frame,
            text="Выбрать изображение",
            command=self._select_visible_image
        )
        select_btn.pack(side='right')

        # Фрейм для текста
        text_frame = ttk.LabelFrame(parent, text="Текст водяного знака", padding=10)
        text_frame.pack(fill='x', padx=10, pady=10)

        self.visible_text_entry = tk.Entry(text_frame, font=("Arial", 11))
        self.visible_text_entry.pack(fill='x')
        self.visible_text_entry.insert(0, "© Мой водяной знак")

        # Фрейм настроек
        settings_frame = ttk.LabelFrame(parent, text="Настройки", padding=10)
        settings_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Позиция
        pos_frame = tk.Frame(settings_frame)
        pos_frame.pack(fill='x', pady=5)

        tk.Label(pos_frame, text="Позиция:", width=12, anchor='w').pack(side='left')
        self.position_var = tk.StringVar(value='bottom-right')
        position_combo = ttk.Combobox(
            pos_frame,
            textvariable=self.position_var,
            values=['bottom-right', 'bottom-left', 'top-right', 'top-left', 'center', 'diagonal', 'grid'],
            state='readonly',
            width=20
        )
        position_combo.pack(side='left', padx=5)

        # Прозрачность
        opacity_frame = tk.Frame(settings_frame)
        opacity_frame.pack(fill='x', pady=5)

        tk.Label(opacity_frame, text="Прозрачность:", width=12, anchor='w').pack(side='left')
        self.opacity_var = tk.IntVar(value=128)
        opacity_scale = tk.Scale(
            opacity_frame,
            from_=0,
            to=255,
            orient='horizontal',
            variable=self.opacity_var,
            length=200
        )
        opacity_scale.pack(side='left', padx=5)
        tk.Label(opacity_frame, textvariable=self.opacity_var, width=5).pack(side='left')

        # Размер шрифта
        size_frame = tk.Frame(settings_frame)
        size_frame.pack(fill='x', pady=5)

        tk.Label(size_frame, text="Размер:", width=12, anchor='w').pack(side='left')
        self.font_size_var = tk.IntVar(value=36)
        size_scale = tk.Scale(
            size_frame,
            from_=12,
            to=100,
            orient='horizontal',
            variable=self.font_size_var,
            length=200
        )
        size_scale.pack(side='left', padx=5)
        tk.Label(size_frame, textvariable=self.font_size_var, width=5).pack(side='left')

        # Цвет
        color_frame = tk.Frame(settings_frame)
        color_frame.pack(fill='x', pady=5)

        tk.Label(color_frame, text="Цвет:", width=12, anchor='w').pack(side='left')
        self.color_var = tk.StringVar(value='white')
        color_combo = ttk.Combobox(
            color_frame,
            textvariable=self.color_var,
            values=['white', 'black', 'red', 'blue', 'green', 'yellow'],
            state='readonly',
            width=20
        )
        color_combo.pack(side='left', padx=5)

        # Кнопка применения
        apply_btn = ttk.Button(
            parent,
            text="Применить водяной знак",
            command=self._apply_visible_watermark,
            style='Accent.TButton'
        )
        apply_btn.pack(pady=10)

    def _create_encode_tab(self, parent: ttk.Frame):
        """Создает вкладку для встраивания скрытого водяного знака."""
        # Фрейм для выбора файла
        file_frame = ttk.LabelFrame(parent, text="Выбор изображения", padding=10)
        file_frame.pack(fill='x', padx=10, pady=10)

        self.encode_file_label = tk.Label(file_frame, text="Файл не выбран", fg="gray")
        self.encode_file_label.pack(side='left', expand=True)

        select_btn = ttk.Button(
            file_frame,
            text="Выбрать изображение",
            command=self._select_encode_image
        )
        select_btn.pack(side='right')

        # Фрейм для ввода сообщения
        message_frame = ttk.LabelFrame(parent, text="Скрытый водяной знак (текст)", padding=10)
        message_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.message_text = scrolledtext.ScrolledText(
            message_frame,
            height=10,
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.message_text.pack(fill='both', expand=True)

        # Кнопка встраивания
        encode_btn = ttk.Button(
            parent,
            text="Встроить и сохранить",
            command=self._encode_message,
            style='Accent.TButton'
        )
        encode_btn.pack(pady=10)

    def _create_decode_tab(self, parent: ttk.Frame):
        """Создает вкладку для извлечения скрытого водяного знака."""
        # Фрейм для выбора файла
        file_frame = ttk.LabelFrame(parent, text="Выбор изображения", padding=10)
        file_frame.pack(fill='x', padx=10, pady=10)

        self.decode_file_label = tk.Label(file_frame, text="Файл не выбран", fg="gray")
        self.decode_file_label.pack(side='left', expand=True)

        select_btn = ttk.Button(
            file_frame,
            text="Выбрать изображение",
            command=self._select_decode_image
        )
        select_btn.pack(side='right')

        # Кнопка извлечения
        decode_btn = ttk.Button(
            parent,
            text="Извлечь водяной знак",
            command=self._decode_message,
            style='Accent.TButton'
        )
        decode_btn.pack(pady=10)

        # Фрейм для результата
        result_frame = ttk.LabelFrame(parent, text="Извлеченный водяной знак", padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=10,
            wrap=tk.WORD,
            font=("Arial", 10),
            state='disabled'
        )
        self.result_text.pack(fill='both', expand=True)

    def _select_visible_image(self):
        """Открывает диалог выбора изображения для видимого водяного знака."""
        filepath = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.bmp"),
                ("Все файлы", "*.*")
            ]
        )
        if filepath:
            self.visible_image_path = filepath
            filename = os.path.basename(filepath)
            self.visible_file_label.config(text=filename, fg="black")

    def _select_encode_image(self):
        """Открывает диалог выбора изображения для кодирования."""
        filepath = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.bmp"),
                ("Все файлы", "*.*")
            ]
        )
        if filepath:
            self.encode_image_path = filepath
            filename = os.path.basename(filepath)
            self.encode_file_label.config(text=filename, fg="black")

    def _select_decode_image(self):
        """Открывает диалог выбора изображения для декодирования."""
        filepath = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.bmp"),
                ("Все файлы", "*.*")
            ]
        )
        if filepath:
            self.decode_image_path = filepath
            filename = os.path.basename(filepath)
            self.decode_file_label.config(text=filename, fg="black")

    def _apply_visible_watermark(self):
        """Применяет видимый водяной знак к изображению."""
        # Проверяем выбрано ли изображение
        if not hasattr(self, 'visible_image_path'):
            messagebox.showerror("Ошибка", "Пожалуйста, выберите изображение")
            return

        # Получаем текст
        text = self.visible_text_entry.get().strip()
        if not text:
            messagebox.showerror("Ошибка", "Пожалуйста, введите текст водяного знака")
            return

        # Выбираем путь для сохранения
        output_path = filedialog.asksaveasfilename(
            title="Сохранить изображение как",
            defaultextension=".png",
            filetypes=[
                ("PNG изображение", "*.png"),
                ("JPEG изображение", "*.jpg"),
                ("Все файлы", "*.*")
            ]
        )

        if not output_path:
            return

        # Конвертируем цвет
        color_map = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 255, 0),
            'yellow': (255, 255, 0)
        }
        color = color_map.get(self.color_var.get(), (255, 255, 255))

        # Применяем водяной знак
        success, message = self.visible_watermark.add_watermark(
            self.visible_image_path,
            text,
            output_path,
            position=self.position_var.get(),
            opacity=self.opacity_var.get(),
            font_size=self.font_size_var.get(),
            color=color
        )

        if success:
            messagebox.showinfo("Успех", message)
        else:
            messagebox.showerror("Ошибка", message)

    def _encode_message(self):
        """Встраивает сообщение в выбранное изображение."""
        # Проверяем выбрано ли изображение
        if not hasattr(self, 'encode_image_path'):
            messagebox.showerror("Ошибка", "Пожалуйста, выберите изображение")
            return

        # Получаем текст сообщения
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Ошибка", "Пожалуйста, введите текст водяного знака")
            return

        # Выбираем путь для сохранения
        output_path = filedialog.asksaveasfilename(
            title="Сохранить изображение как",
            defaultextension=".png",
            filetypes=[
                ("PNG изображение", "*.png"),
                ("Все файлы", "*.*")
            ]
        )

        if not output_path:
            return

        # Кодируем сообщение
        success, result_message = self.lsb_steganography.encode(
            self.encode_image_path,
            message,
            output_path
        )

        if success:
            messagebox.showinfo("Успех", result_message)
            self.message_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Ошибка", result_message)

    def _decode_message(self):
        """Извлекает сообщение из выбранного изображения."""
        # Проверяем выбрано ли изображение
        if not hasattr(self, 'decode_image_path'):
            messagebox.showerror("Ошибка", "Пожалуйста, выберите изображение")
            return

        # Декодируем сообщение
        success, message = self.lsb_steganography.decode(self.decode_image_path)

        # Отображаем результат
        self.result_text.config(state='normal')
        self.result_text.delete("1.0", tk.END)

        if success:
            self.result_text.insert("1.0", message)
        else:
            self.result_text.insert("1.0", f"Ошибка: {message}")

        self.result_text.config(state='disabled')
