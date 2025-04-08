import tkinter as tk
from tkinter import Listbox, Scrollbar
from core.image_loader import ImageLoader
from core.pdf_creator import PDFCreator

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        
        # Инициализация компонентов
        self.image_loader = ImageLoader()
        self.pdf_creator = PDFCreator()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Фрейм для кнопок
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10, fill=tk.X)
        
        # Кнопки управления
        tk.Button(btn_frame, text="Добавить фото", 
                 command=self.image_loader.add_images).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Удалить фото",
                 command=self.delete_image).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Создать PDF",
                 command=self.create_pdf,
                 bg="#4CAF50", fg="white").pack(side=tk.RIGHT, padx=5)
        
        # Список изображений
        self.listbox = Listbox(self.root, width=60, height=15)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        
        # Привязка событий
        self.image_loader.set_listbox(self.listbox)
    
    def delete_image(self):
        selected = self.listbox.curselection()
        if selected:
            self.image_loader.delete_image(selected[0])
    
    def create_pdf(self):
        if not self.image_loader.images:
            tk.messagebox.showwarning("Ошибка", "Нет изображений для создания PDF!")
            return
        
        self.pdf_creator.create_from_images(self.image_loader.images)