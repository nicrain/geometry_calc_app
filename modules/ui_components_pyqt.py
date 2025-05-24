"""
UI组件模块 - 提供通用界面组件
"""
from PyQt6.QtWidgets import (QWidget, QPushButton, QFrame, QVBoxLayout, 
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

# 颜色映射 - 用于组件样式
COLOR_MAP = {
    'primary': '#1976D2',
    'secondary': '#424242',
    'success': '#4CAF50',
    'danger': '#F44336',
    'warning': '#FFC107',
    'info': '#2196F3',
    'light': '#F5F5F5',
    'dark': '#212121',
}

class BaseModule(QWidget):
    """基础模块类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_base_ui()
    
    def _setup_base_ui(self):
        """设置基础UI"""
        self.setContentsMargins(0, 0, 0, 0)
    
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
        self.active = False
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI样式"""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.bg_color};
                color: {self.text_color};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {self._lighten_color(self.bg_color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(self.bg_color)};
            }}
        """)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(3, 3)
        self.setGraphicsEffect(shadow)
    
    def _lighten_color(self, color, factor=0.2):
        """使颜色变亮"""
        if color.startswith('#'):
            # 解析十六进制颜色
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # 使颜色变亮
            r = min(255, int(r * (1 + factor)))
            g = min(255, int(g * (1 + factor)))
            b = min(255, int(b * (1 + factor)))
            
            # 返回十六进制颜色
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def _darken_color(self, color, factor=0.2):
        """使颜色变暗"""
        if color.startswith('#'):
            # 解析十六进制颜色
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # 使颜色变暗
            r = max(0, int(r * (1 - factor)))
            g = max(0, int(g * (1 - factor)))
            b = max(0, int(b * (1 - factor)))
            
            # 返回十六进制颜色
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def set_active(self, active):
        """设置按钮的激活状态"""
        self.active = active
        if active:
            # 激活状态：使用更深的颜色
            active_bg = self._darken_color(self.bg_color, 0.3)
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {active_bg};
                    color: {self.text_color};
                    border: 2px solid {self.bg_color};
                    border-radius: 4px;
                    padding: 8px 16px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    background-color: {self._lighten_color(active_bg)};
                }}
                QPushButton:pressed {{
                    background-color: {self._darken_color(active_bg)};
                }}
            """)
        else:
            # 非激活状态：恢复原样式
            self._setup_ui()