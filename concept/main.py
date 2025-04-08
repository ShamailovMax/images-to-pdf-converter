import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, simpledialog
from PIL import Image, ImageTk
from fpdf import FPDF
import os
import uuid

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Галерея изображений → PDF")
        self.images = []
        
        # Настройка размеров окна (60% ширины, 70% высоты экрана)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.7)
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Основные элементы интерфейса
        self.setup_ui()
    
    def setup_ui(self):
        # Фрейм для кнопок
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10, fill=tk.X)
        
        # Кнопки управления
        tk.Button(btn_frame, text="Добавить фото", command=self.add_image).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить фото", command=self.delete_image).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Создать PDF", command=self.create_pdf, bg="#4CAF50", fg="white").pack(side=tk.RIGHT, padx=5)
        
        # Список изображений с прокруткой
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.image_list = Listbox(
            list_frame, 
            width=50, 
            height=15,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.image_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.image_list.yview)
        
        # Область предпросмотра изображения
        self.preview_label = tk.Label(self.root)
        self.preview_label.pack(pady=10)
        
        # Привязка событий
        self.image_list.bind("<<ListboxSelect>>", self.show_preview)
    
    def add_image(self):
        files = filedialog.askopenfilenames(
            title="Выберите изображения",
            filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp")]
        )
        for f in files:
            if f not in self.images:
                self.images.append(f)
                self.image_list.insert(tk.END, os.path.basename(f))
    
    def delete_image(self):
        selected = self.image_list.curselection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите изображение для удаления!")
            return
        
        self.images.pop(selected[0])
        self.image_list.delete(selected)
        
        # Очищаем превью, если удалили текущее изображение
        if not self.images:
            self.preview_label.config(image=None)
            self.preview_label.image = None
    
    def show_preview(self, event=None):
        selected = self.image_list.curselection()
        if not selected or not self.images:
            return
        
        try:
            img = Image.open(self.images[selected[0]])
            img.thumbnail((400, 400))
            
            img_tk = ImageTk.PhotoImage(img)
            self.preview_label.config(image=img_tk)
            self.preview_label.image = img_tk
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{e}")
    
    def create_pdf(self):
        if not self.images:
            messagebox.showwarning("Ошибка", "Нет изображений для создания PDF!")
            return
        
        pdf_name = simpledialog.askstring("Имя файла", "Введите название PDF (без .pdf):")
        if not pdf_name:
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF файлы", "*.pdf")],
            initialfile=f"{pdf_name}.pdf"
        )
        if not save_path:
            return
        
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            temp_files = []  # Будем хранить временные файлы для последующего удаления
            
            for img_path in self.images:
                img = Image.open(img_path)
                
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Генерируем уникальное имя для временного файла
                temp_path = f"temp_pdf_img_{uuid.uuid4().hex}.jpg"
                img.save(temp_path)
                temp_files.append(temp_path)
                
                pdf.add_page()
                pdf.image(temp_path, x=10, y=10, w=190)
            
            pdf.output(save_path)
            
            # Удаляем все временные файлы
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            messagebox.showinfo("Готово!", f"PDF успешно сохранён:\n{save_path}")
        except Exception as e:
            # Удаляем временные файлы даже в случае ошибки
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            messagebox.showerror("Ошибка", f"Не удалось создать PDF:\n{e}")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()