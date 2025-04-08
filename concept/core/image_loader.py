from tkinter import filedialog
import os

class ImageLoader:
    def __init__(self):
        self.images = []
        self.listbox = None
    
    def set_listbox(self, listbox):
        self.listbox = listbox
    
    def add_images(self):
        files = filedialog.askopenfilenames(
            title="Выберите изображения",
            filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        for f in files:
            if f not in self.images:
                self.images.append(f)
                self.listbox.insert("end", os.path.basename(f))
    
    def delete_image(self, index):
        if 0 <= index < len(self.images):
            self.images.pop(index)
            self.listbox.delete(index)