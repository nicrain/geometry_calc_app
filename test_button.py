import tkinter as tk
from tkinter import ttk
from modules.ui_components import MetroButton

def main():
    root = tk.Tk()
    root.geometry("400x300")
    
    # 设置默认主题
    style = ttk.Style()
    style.theme_use('default')
    
    frame = ttk.Frame(root, padding="10")
    frame.pack(fill='both', expand=True)
    
    # 测试不同颜色的按钮
    colors = [
        ("#1B5E20", "深绿色按钮"),
        ("#1A237E", "深蓝色按钮"),
        ("#B71C1C", "深红色按钮")
    ]
    
    for color, text in colors:
        btn = MetroButton(
            frame,
            text=text,
            bg=color,
            fg='white'
        )
        btn.pack(pady=10, padx=20, fill='x')

    root.mainloop()

if __name__ == "__main__":
    main()
