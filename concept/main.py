import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Галерея изображений")
        self.images = []
        self.current_image = None

        # Получаем размеры экрана
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Устанавливаем размеры окна (60% ширины, 70% высоты)
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.7)
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(400, 300)  # Минимальный размер окна

        # Основной контейнер с прокруткой
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Кнопки управления
        self.btn_frame = tk.Frame(self.main_frame)
        self.btn_frame.pack(pady=10, fill=tk.X)

        self.add_btn = tk.Button(self.btn_frame, text="Добавить фото", command=self.add_image)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.del_btn = tk.Button(self.btn_frame, text="Удалить фото", command=self.delete_image)
        self.del_btn.pack(side=tk.LEFT, padx=5)

        # Список изображений (с прокруткой)
        self.list_frame = tk.Frame(self.main_frame)
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar_list = Scrollbar(self.list_frame)
        self.scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)

        self.image_list = Listbox(
            self.list_frame,
            width=50,
            height=10,
            yscrollcommand=self.scrollbar_list.set,
            selectmode=tk.SINGLE
        )
        self.image_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.image_list.bind("<<ListboxSelect>>", self.show_selected_image)

        self.scrollbar_list.config(command=self.image_list.yview)

        # Область для изображения (с прокруткой)
        self.image_canvas = tk.Canvas(self.main_frame, bg="white")
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

        # Скроллбары для изображения
        self.scrollbar_x = Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scrollbar_y = Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.image_canvas.configure(
            xscrollcommand=self.scrollbar_x.set,
            yscrollcommand=self.scrollbar_y.set
        )

        # Внутренний фрейм для изображения
        self.image_frame = tk.Frame(self.image_canvas)
        self.image_canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

        # Метка для изображения
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        # Привязка изменения размера
        self.image_frame.bind("<Configure>", lambda e: self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all")))
    
    def add_image(self):
        file_paths = filedialog.askopenfilenames(
            title="Выберите изображения",
            filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if not file_paths:
            return
        
        for path in file_paths:
            if path not in self.images:
                self.images.append(path)
                self.image_list.insert(tk.END, path.split("/")[-1])
    
    def delete_image(self):
        selected_index = self.image_list.curselection()
        if not selected_index:
            messagebox.showwarning("Ошибка", "Выберите изображение для удаления!")
            return
        
        del self.images[selected_index[0]]
        self.image_list.delete(selected_index)
        
        if len(self.images) == 0:
            self.image_label.config(image=None)
            self.image_label.image = None
        elif selected_index[0] == self.image_list.curselection():
            self.image_list.selection_set(0)
            self.show_selected_image()
    
    def show_selected_image(self, event=None):
        selected_index = self.image_list.curselection()
        if not selected_index:
            return
        
        img_path = self.images[selected_index[0]]
        try:
            img = Image.open(img_path)
            
            # Масштабируем изображение под размер Canvas (с сохранением пропорций)
            canvas_width = self.image_canvas.winfo_width() - 20  # Учитываем отступы
            canvas_height = self.image_canvas.winfo_height() - 20
            
            img.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
            
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
            
            # Обновляем скроллрегион
            self.image_frame.update_idletasks()
            self.image_canvas.config(scrollregion=self.image_canvas.bbox("all"))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()