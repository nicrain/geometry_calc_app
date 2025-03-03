import tkinter as tk

class BaseModule:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack_forget()  # 初始时隐藏
        
    def show(self):
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        self.frame.pack_forget()
