from ui.main_window import MainWindow
import tkinter as tk

def on_resize(event):
    if hasattr(event.widget, 'show_preview'):
        event.widget.show_preview()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    
    # Bind resize event
    root.bind('<Configure>', on_resize)
    
    root.mainloop()