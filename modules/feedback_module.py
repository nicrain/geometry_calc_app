## ✅ **交互反馈模块**
from tkinter import messagebox
def show_feedback(message, success=True):
    if success:
        messagebox.showinfo("Succès", message)
    else:
        messagebox.showerror("Erreur", message)