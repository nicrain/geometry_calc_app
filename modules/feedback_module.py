from tkinter import messagebox

def show_feedback(message, type="info"):
    if type == "error":
        messagebox.showerror("Erreur", message)
    else:
        messagebox.showinfo("Information", message)