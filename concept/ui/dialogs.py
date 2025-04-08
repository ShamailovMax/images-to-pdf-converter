from tkinter import messagebox

def show_error(message):
    messagebox.showerror("Ошибка", message)

def show_info(message):
    messagebox.showinfo("Информация", message)