"""
属性面板基类模块
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QDoubleSpinBox, QPushButton, QSizePolicy,
                             QGraphicsDropShadowEffect)  # 从 QtWidgets 导入
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

# 解决元类冲突的方法是创建一个带有ABC元方法的QFrame子类
class AbstractQFrame(QFrame):
    """解决元类冲突的抽象QFrame基类"""
    pass

class PropertyPanel(AbstractQFrame):
    """属性面板的抽象基类"""
    
    # 定义信号
    property_changed = pyqtSignal(dict)  # 属性变化信号
    create_requested = pyqtSignal(dict)  # 创建请求信号
    
    def __init__(self, title: str, bg_color: str, text_color: str, parent=None):
        """初始化属性面板
        
        Args:
            title: 面板标题
            bg_color: 背景颜色
            text_color: 文本颜色
            parent: 父组件
        """
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)  # 修正：使用 QFrame.Shadow.Raised 而不是 QFrame.Shape.Raised
        self.bg_color = bg_color
        self.text_color = text_color
        
        # 设置基本样式
        self._update_style()
        
        # 设置阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor("#CCCCCC"))
        shadow.setOffset(2, 2)
        self.setGraphicsEffect(shadow)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)
        
        # 添加标题
        self.title_label = QLabel(title, self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {text_color};")
        self.main_layout.addWidget(self.title_label)
        
        # 创建属性网格布局
        self.properties_layout = QGridLayout()
        self.properties_layout.setVerticalSpacing(10)
        self.properties_layout.setHorizontalSpacing(8)
        
        # 创建按钮布局
        self.buttons_layout = QHBoxLayout()
        
        # 创建按钮
        self.create_button = QPushButton("Créer")
        self.create_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {text_color}; 
                color: white; 
                border-radius: 4px; 
                padding: 5px 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self._lighten_color(text_color)};
            }}
        """)
        self.create_button.clicked.connect(self._on_create_clicked)
        self.buttons_layout.addWidget(self.create_button)
        
        # 设置尺寸策略
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedWidth(220)
    
    def _update_style(self):
        """更新面板样式"""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.bg_color};
                border-radius: 8px;
                border: 1px solid {self._darken_color(self.bg_color)};
            }}
            QLabel {{
                color: {self.text_color};
                font-weight: bold;
            }}
        """)
    
    def _lighten_color(self, color: str) -> str:
        """使颜色变亮"""
        if color.startswith('#'):
            color_obj = QColor(color)
            h, s, v, a = color_obj.getHsvF()
            v = min(1.0, v * 1.2)  # 增加亮度
            color_obj.setHsvF(h, s, v, a)
            return color_obj.name()
        return color
    
    def _darken_color(self, color: str) -> str:
        """使颜色变暗"""
        if color.startswith('#'):
            color_obj = QColor(color)
            h, s, v, a = color_obj.getHsvF()
            v = max(0.0, v * 0.8)  # 减少亮度
            color_obj.setHsvF(h, s, v, a)
            return color_obj.name()
        return color
    
    def _on_create_clicked(self):
        """创建按钮点击事件处理"""
        properties = self.get_properties()
        self.create_requested.emit(properties)
    
    def _on_property_changed(self):
        """属性值变化事件处理"""
        properties = self.get_properties()
        self.property_changed.emit(properties)
    
    # 使用装饰器将方法标记为抽象方法
    @abstractmethod
    def get_properties(self) -> Dict[str, Any]:
        """获取当前设置的属性"""
        pass
    
    @abstractmethod
    def set_properties(self, properties: Dict[str, Any]) -> None:
        """设置面板属性值"""
        pass
    
    def set_enabled(self, enabled: bool = True) -> None:
        """设置面板输入控件的启用/禁用状态"""
        for i in range(self.properties_layout.count()):
            item = self.properties_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, (QDoubleSpinBox, QPushButton)):
                    widget.setEnabled(enabled)
        
        self.create_button.setEnabled(enabled)
        
        # 更新样式
        if not enabled:
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: #ECEFF1;
                    border-radius: 8px;
                    border: 1px solid #CFD8DC;
                }}
                QLabel {{
                    color: #607D8B;
                    font-weight: bold;
                }}
                QDoubleSpinBox, QPushButton {{
                    background-color: #ECEFF1;
                    color: #90A4AE;
                    border: 1px solid #CFD8DC;
                }}
            """)
        else:
            self._update_style()
