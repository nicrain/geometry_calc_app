import sys
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# 导入PyQt6模块
from PyQt6.QtWidgets import (QWidget, QPushButton, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

# 颜色映射表 - 集中管理应用的颜色方案
COLOR_MAP = {
    # 基础颜色
    "#1B5E20": {"lighter": "#2E7D32", "darker": "#0F4C12", "name": "深墨绿色"},  
    "#1A237E": {"lighter": "#283593", "darker": "#0D1642", "name": "深靛蓝色"},  
    "#311B92": {"lighter": "#4527A0", "darker": "#1A0F4C", "name": "深紫色"},  
    "#B71C1C": {"lighter": "#D32F2F", "darker": "#7F1414", "name": "深红色"},  
    "#757575": {"lighter": "#9E9E9E", "darker": "#424242", "name": "灰色"},  
    "#FF5722": {"lighter": "#FF7043", "darker": "#E64A19", "name": "橙色"},
    "#E65100": {"lighter": "#EF6C00", "darker": "#BF360C", "name": "深橙色"},
    "#0277BD": {"lighter": "#0288D1", "darker": "#01579B", "name": "蓝色"}
}

def generate_button_style(bg_color, fg_color, is_active=False):
    """生成按钮样式表，避免重复代码
    
    Args:
        bg_color: 背景颜色
        fg_color: 前景(文字)颜色
        is_active: 是否处于活动状态
    
    Returns:
        生成的样式表字符串
    """
    # 确定要使用的背景颜色
    if is_active:
        bg = COLOR_MAP.get(bg_color, {}).get("lighter", bg_color)
    else:
        bg = bg_color
        
    hover_bg = COLOR_MAP.get(bg_color, {}).get("lighter", bg_color)
    pressed_bg = COLOR_MAP.get(bg_color, {}).get("darker", bg_color)
    
    return f"""
        QPushButton {{
            background-color: {bg};
            color: {fg_color};
            border: none;
            border-radius: 6px;
            padding: 10px;
            text-align: center;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {hover_bg};
        }}
        QPushButton:pressed {{
            background-color: {pressed_bg};
        }}
    """

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
        self.setStyleSheet(generate_button_style(bg_color, fg_color))
        
        # 设置阴影效果
        self.setGraphicsEffect(None)  # 先清除任何现有效果
        
        # 设置最小尺寸
        self.setMinimumSize(120, 36)
        
    def _lighten_color(self, color):
        """使颜色变亮"""
        return COLOR_MAP.get(color, {}).get("lighter", color)
    
    def _darken_color(self, color):
        """使颜色变暗"""
        return COLOR_MAP.get(color, {}).get("darker", color)
    
    def set_active(self, is_active=True):
        """设置按钮的活动状态"""
        self.setStyleSheet(generate_button_style(self.bg_color, self.fg_color, is_active))

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
        
    def back_to_home(self):
        """返回主页面的通用方法"""
        parent = self.parent()
        while parent:
            if hasattr(parent, 'back_to_home'):
                parent.back_to_home()
                break
            parent = parent.parent()