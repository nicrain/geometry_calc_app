import sys
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QPushButton, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class MetroButton(QPushButton):
    """实现类似Communicator 5的Metro风格按钮"""
    def __init__(self, text="", bg_color="#ffffff", fg_color="#000000", parent=None):
        super().__init__(text, parent)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.normal_bg = bg_color
        self.hover_bg = self._lighten_color(bg_color)
        self.pressed_bg = self._darken_color(bg_color)
        
        # 设置样式
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.normal_bg};
                color: {fg_color};
                border: none;
                border-radius: 6px;
                padding: 10px;
                text-align: center;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.hover_bg};
            }}
            QPushButton:pressed {{
                background-color: {self.pressed_bg};
            }}
        """)
        
        # 设置阴影效果
        self.setGraphicsEffect(None)  # 先清除任何现有效果
        
        # 设置最小尺寸
        self.setMinimumSize(120, 36)
        
    def _lighten_color(self, color):
        """使颜色变亮"""
        color_map = {
            "#1B5E20": "#2E7D32",  # 深墨绿色 -> 浅一点的绿色
            "#1A237E": "#283593",  # 深靛蓝色 -> 浅一点的靛蓝
            "#311B92": "#4527A0",  # 深紫色 -> 浅一点的紫色
            "#B71C1C": "#D32F2F",   # 深红色 -> 浅一点的红色
            "#757575": "#9E9E9E",   # 灰色 -> 浅灰色
            "#FF5722": "#FF7043"    # 橙色 -> 浅橙色
        }
        return color_map.get(color, color)
    
    def _darken_color(self, color):
        """使颜色变暗"""
        color_map = {
            "#1B5E20": "#0F4C12",  # 深墨绿色 -> 更深的绿色
            "#1A237E": "#0D1642",  # 深靛蓝色 -> 更深的蓝色
            "#311B92": "#1A0F4C",  # 深紫色 -> 更深的紫色
            "#B71C1C": "#7F1414",   # 深红色 -> 更深的红色
            "#757575": "#424242",   # 灰色 -> 深灰色
            "#FF5722": "#E64A19"    # 橙色 -> 深橙色
        }
        return color_map.get(color, color)
    
    def set_active(self, is_active=True):
        """设置按钮的活动状态"""
        if is_active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.hover_bg};
                    color: {self.fg_color};
                    border: none;
                    border-radius: 6px;
                    padding: 10px;
                    text-align: center;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.hover_bg};
                }}
                QPushButton:pressed {{
                    background-color: {self.pressed_bg};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.normal_bg};
                    color: {self.fg_color};
                    border: none;
                    border-radius: 6px;
                    padding: 10px;
                    text-align: center;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.hover_bg};
                }}
                QPushButton:pressed {{
                    background-color: {self.pressed_bg};
                }}
            """)

class BaseModule(QWidget):
    """所有模块的基类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hide()  # 初始时隐藏
        
    def show_module(self):
        """显示模块"""
        self.show()
        
    def hide_module(self):
        """隐藏模块"""
        self.hide()