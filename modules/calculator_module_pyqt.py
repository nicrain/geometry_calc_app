import sys
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# 导入PyQt6模块
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QLineEdit, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 导入自定义组件
from modules.ui_components_pyqt import BaseModule, MetroButton, COLOR_MAP

class CalculatorModule(BaseModule):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建标题
        title_label = QLabel("Calculatrice")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # 创建计算器UI
        self.create_calculator_ui()
    
    def create_calculator_ui(self):
        # 创建内容区域的水平布局
        content_layout = QHBoxLayout()
        self.main_layout.addLayout(content_layout)
        
        # 创建计算器主区域
        calc_frame = QWidget()
        calc_layout = QVBoxLayout(calc_frame)
        calc_layout.setContentsMargins(10, 10, 10, 10)
        calc_frame.setMinimumWidth(510)  # 设置最小宽度
        content_layout.addWidget(calc_frame)
        
        # 创建显示结果的文本框
        self.result_display = QLineEdit("0")
        self.result_display.setFont(QFont("Arial", 32))
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.result_display.setReadOnly(True)  # 设置为只读
        self.result_display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
        """)
        calc_layout.addWidget(self.result_display)
        
        # 创建数字按钮容器
        buttons_frame = QWidget()
        buttons_layout = QGridLayout(buttons_frame)
        buttons_layout.setContentsMargins(20, 10, 20, 10)
        buttons_layout.setSpacing(10)  # 增加按钮之间的间距
        calc_layout.addWidget(buttons_frame)
        
        # 使用更高对比度的颜色方案
        buttons = [
            ('7', '#1A237E'), ('8', '#1A237E'), ('9', '#1A237E'), ('/', '#311B92'),
            ('4', '#1A237E'), ('5', '#1A237E'), ('6', '#1A237E'), ('*', '#311B92'),
            ('1', '#1A237E'), ('2', '#1A237E'), ('3', '#1A237E'), ('-', '#311B92'),
            ('0', '#1A237E'), ('.', '#1A237E'), ('=', '#1B5E20'), ('+', '#311B92')
        ]

        # 创建按钮
        for i, (button_text, color) in enumerate(buttons):
            row = i // 4
            col = i % 4
            btn = MetroButton(button_text, color, 'white')
            btn.setFixedSize(80, 60)  # 设置固定大小
            btn.setFont(QFont("Arial", 16, weight=QFont.Weight.Bold))
            btn.clicked.connect(lambda checked, text=button_text: self.click_button(text))
            buttons_layout.addWidget(btn, row, col)
        
        # 创建工具栏
        tools_frame = QWidget()
        tools_layout = QVBoxLayout(tools_frame)
        tools_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.addWidget(tools_frame)

        # 添加返回主界面按钮
        return_button = MetroButton("Retour", "#757575", "#FFFFFF")
        return_button.setMinimumSize(110, 110)
        return_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        return_button.clicked.connect(self.back_to_home)
        tools_layout.addWidget(return_button)

        # 添加弹性空间
        content_layout.addStretch(1)
    
    def click_button(self, value):
        """实现计算器按钮点击功能"""
        if value == '=':
            self._calculate_result()
        elif value == 'C':
            self.result_display.setText("0")
        elif value == '←':
            self._handle_backspace()
        else:
            self._append_to_display(value)
    
    def _calculate_result(self):
        """计算表达式结果"""
        try:
            # 安全地计算表达式
            expression = self.result_display.text()
            # 替换乘除符号为Python可识别的符号
            expression = expression.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            
            # 格式化结果，避免过长的小数
            if isinstance(result, float):
                # 如果是整数值的浮点数，转换为整数
                if result.is_integer():
                    result = int(result)
                else:
                    # 限制小数位数为6位
                    result = round(result, 6)
            
            self.result_display.setText(str(result))
        except Exception as e:
            self.result_display.setText("Erreur")
            print(f"Erreur de calcul: {e}")
            
    def _handle_backspace(self):
        """处理退格功能"""
        current_text = self.result_display.text()
        if current_text != "0" and current_text != "Erreur":
            if len(current_text) == 1:
                self.result_display.setText("0")
            else:
                self.result_display.setText(current_text[:-1])
                
    def _append_to_display(self, value):
        """向显示屏添加字符"""
        current_text = self.result_display.text()
        if current_text == "0" or current_text == "Erreur":
            self.result_display.setText(value)
        else:
            self.result_display.setText(current_text + value)
                
    def back_to_home(self):
        # 获取主应用程序实例并调用返回主页面方法
        parent = self.parent()
        while parent:
            if hasattr(parent, 'back_to_home'):
                parent.back_to_home()
                break
            parent = parent.parent()