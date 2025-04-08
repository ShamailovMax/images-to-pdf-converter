import tkinter as tk
from tkinter import Listbox, Scrollbar, Label
from core.image_loader import ImageLoader
from core.pdf_creator import PDFCreator
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        
        self.image_loader = ImageLoader()
        self.pdf_creator = PDFCreator()
        self.current_preview = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel (listbox)
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Right panel (preview)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Buttons
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame, text="Добавить фото", 
                 command=self.image_loader.add_images).pack(side=tk.LEFT, padx=2)
        
        tk.Button(btn_frame, text="Удалить фото",
                 command=self.delete_image).pack(side=tk.LEFT, padx=2)
        
        # Listbox with scroll
        scrollbar = Scrollbar(left_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = Listbox(left_frame, width=30, height=20,
                             yscrollcommand=scrollbar.set)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Preview area
        self.preview_label = Label(right_frame, bg='white', 
                                 relief=tk.SUNKEN, borderwidth=2)
        self.preview_label.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # PDF button
        tk.Button(right_frame, text="Создать PDF",
                 command=self.create_pdf,
                 bg="#4CAF50", fg="white").pack(side=tk.BOTTOM, pady=5)
        
        # Bind events
        self.image_loader.set_listbox(self.listbox)
        self.listbox.bind('<<ListboxSelect>>', self.show_preview)
    
    def show_preview(self, event=None):
        selected = self.listbox.curselection()
        if not selected or not self.image_loader.images:
            return
        
        try:
            img_path = self.image_loader.images[selected[0]]
            img = Image.open(img_path)
            
            # Calculate aspect ratio
            preview_width = self.preview_label.winfo_width() - 20
            preview_height = self.preview_label.winfo_height() - 20
            img.thumbnail((preview_width, preview_height))
            
            img_tk = ImageTk.PhotoImage(img)
            self.preview_label.config(image=img_tk)
            self.preview_label.image = img_tk  # Keep reference
            
        except Exception as e:
            print(f"Error loading preview: {e}")
    
    def delete_image(self):
        selected = self.listbox.curselection()
        if selected:
            self.image_loader.delete_image(selected[0])
            self.preview_label.config(image=None)
            self.preview_label.image = None
    
    def create_pdf(self):
        if not self.image_loader.images:
            tk.messagebox.showwarning("Ошибка", "Нет изображений для создания PDF!")
            return
        
        self.pdf_creator.create_from_images(self.image_loader.images)