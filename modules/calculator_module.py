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
        result_display = tk.Entry(
            self.frame,
            textvariable=self.result_var,
            font=("Arial", 32),  # 更大的字体
            justify="right",
            bd=2,
            relief="solid"
        )
        result_display.pack(fill="x", padx=20, pady=20)
        
        # 创建数字按钮容器
        buttons_frame = tk.Frame(self.frame, bg='white')
        buttons_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        # 更新按钮基础配置
        button_configs = {
            'width': 60,     # 减小宽度
            'height': 40,    # 减小高度
            'font': ('Arial', 16, 'bold')  # 调整字体大小
        }
        
        # 使用更高对比度的颜色方案
        buttons = [
            ('7', '#1A237E'), ('8', '#1A237E'), ('9', '#1A237E'), ('/', '#311B92'),
            ('4', '#1A237E'), ('5', '#1A237E'), ('6', '#1A237E'), ('*', '#311B92'),
            ('1', '#1A237E'), ('2', '#1A237E'), ('3', '#1A237E'), ('-', '#311B92'),
            ('0', '#1A237E'), ('.', '#1A237E'), ('=', '#1B5E20'), ('+', '#311B92')
        ]
        
        # 设置网格布局的间距
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1, pad=5)  # 减小间距
            buttons_frame.grid_rowconfigure(i, weight=1, pad=5)     # 减小间距
            
        # 创建按钮
        for i, (button_text, color) in enumerate(buttons):
            row = i // 4
            col = i % 4
            cmd = lambda x=button_text: self.click_button(x)
            btn = MetroButton(
                buttons_frame,
                text=button_text,
                bg=color,
                fg='white',
                command=cmd,
                **button_configs
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')  # 减小边距
    
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