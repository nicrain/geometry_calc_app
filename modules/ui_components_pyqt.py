"""
PyQt6 UI组件模块
"""
from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 颜色映射
COLOR_MAP = {
    'geometry': '#1B5E20',
    'calculator': '#1A237E', 
    'back': '#757575',
    'undo': '#FF5722'
}

class BaseModule(QWidget):
    """模块基类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def show_module(self):
        """显示模块"""
        self.show()
        
    def hide_module(self):
        """隐藏模块"""
        self.hide()

class MetroButton(QPushButton):
    """Metro风格按钮"""
    def __init__(self, text, bg_color, text_color, parent=None):
        super().__init__(text, parent)
        self.bg_color = bg_color
        self.text_color = text_color
        self.is_active = False
        self._update_style()
        
    def _update_style(self):
        """更新按钮样式"""
        if self.is_active:
            style = f"""
                QPushButton {{
                    background-color: {self.text_color};
                    color: {self.bg_color};
                    border: 2px solid {self.bg_color};
                    border-radius: 8px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self._lighten_color(self.text_color)};
                }}
            """
        else:
            style = f"""
                QPushButton {{
                    background-color: {self.bg_color};
                    color: {self.text_color};
                    border: 2px solid {self.bg_color};
                    border-radius: 8px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self._lighten_color(self.bg_color)};
                }}
            """
        self.setStyleSheet(style)
    
    def _lighten_color(self, color):
        """使颜色变亮"""
        return color  # 简化实现
        
    def set_active(self, active):
        """设置按钮激活状态"""
        self.is_active = active
        self._update_style()