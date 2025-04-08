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
            pdf.set_auto_page_break(auto=False)
            temp_files = []
            
            for img_path in images:
                img = Image.open(img_path)
                
                # Конвертируем PNG с прозрачностью
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                
                # Сохраняем временный файл
                temp_path = f"temp_{uuid.uuid4().hex}.jpg"
                img.save(temp_path, quality=95)
                temp_files.append(temp_path)
                
                # Получаем размеры изображения в мм (1px ≈ 0.264583mm при 96dpi)
                img_width = img.width * 0.264583
                img_height = img.height * 0.264583
                
                # Размеры области PDF (A4: 210x297mm с полями 10mm)
                pdf_width = 190  # 210 - 10*2
                pdf_height = 277  # 297 - 10*2
                
                # Рассчитываем масштаб
                width_ratio = pdf_width / img_width
                height_ratio = pdf_height / img_height
                scale = min(width_ratio, height_ratio)
                
                # Новые размеры с сохранением пропорций
                new_width = img_width * scale
                new_height = img_height * scale
                
                # Центрируем изображение
                x_pos = (210 - new_width) / 2
                y_pos = (297 - new_height) / 2
                
                # Добавляем страницу
                pdf.add_page()
                pdf.image(temp_path, 
                        x=x_pos, 
                        y=y_pos, 
                        w=new_width,
                        h=new_height)
            
            pdf.output(save_path)

            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            messagebox.showinfo("Готово!", f"PDF успешно сохранён:\n{save_path}")
        except Exception as e:
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            messagebox.showerror("Ошибка", f"Не удалось создать PDF:\n{e}")