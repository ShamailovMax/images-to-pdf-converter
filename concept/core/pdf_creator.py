from fpdf import FPDF
from tkinter import filedialog, simpledialog, messagebox
import os
import uuid
from PIL import Image

class PDFCreator:
    def create_from_images(self, images):
        pdf_name = simpledialog.askstring("Имя файла", "Введите название PDF:")
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
            temp_files = []
            
            for img_path in images:
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                temp_path = f"temp_{uuid.uuid4().hex}.jpg"
                img.save(temp_path)
                temp_files.append(temp_path)
                
                pdf.add_page()
                pdf.image(temp_path, x=10, y=10, w=190)
            
            pdf.output(save_path)
            
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            messagebox.showinfo("Успех", f"PDF создан:\n{save_path}")
        except Exception as e:
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            messagebox.showerror("Ошибка", f"Ошибка при создании PDF:\n{e}")