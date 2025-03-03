import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from modules.base_module import BaseModule
from modules.ui_components import MetroButton

class CalculatorModule(BaseModule):
    def __init__(self, parent):
        BaseModule.__init__(self, parent)  # 使用显式的父类初始化
        
        # 在self.frame中创建计算器模块的内容
        self.title = tk.Label(self.frame, text="Calculatrice", font=("Arial", 16))
        self.title.pack(pady=10)
        
        self.create_calculator_ui()
    
    def create_calculator_ui(self):
        # 创建显示结果的文本框
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        result_display = tk.Entry(self.frame, textvariable=self.result_var, font=("Arial", 20), justify="right")
        result_display.pack(fill="x", padx=20, pady=10)
        
        # 创建数字按钮
        buttons_frame = tk.Frame(self.frame)
        buttons_frame.pack(padx=20, pady=10)
        
        # 使用Metro风格按钮创建计算器界面
        buttons = [
            ('7', '#2D89EF'), ('8', '#2D89EF'), ('9', '#2D89EF'), ('/', '#2D89EF'),
            ('4', '#2D89EF'), ('5', '#2D89EF'), ('6', '#2D89EF'), ('*', '#2D89EF'),
            ('1', '#2D89EF'), ('2', '#2D89EF'), ('3', '#2D89EF'), ('-', '#2D89EF'),
            ('0', '#2D89EF'), ('.', '#2D89EF'), ('=', '#00A300'), ('+', '#2D89EF')
        ]
        
        row = 0
        col = 0
        for button_text, color in buttons:
            cmd = lambda x=button_text: self.click_button(x)
            MetroButton(
                buttons_frame,
                text=button_text,
                bg=color,
                fg='white',
                width=8,
                height=3,
                command=cmd
            ).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1
                
        # 配置网格布局权重
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
            buttons_frame.grid_rowconfigure(i, weight=1)
    
    def click_button(self, value):
        # 实现计算器按钮点击功能
        if value == '=':
            try:
                result = eval(self.result_var.get())
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        else:
            if self.result_var.get() == "0" or self.result_var.get() == "Error":
                self.result_var.set(value)
            else:
                self.result_var.set(self.result_var.get() + value)