"""
点属性面板的实现。
"""
from typing import Dict, Any
from PyQt6.QtWidgets import QLabel, QDoubleSpinBox, QGridLayout
from PyQt6.QtCore import Qt

from modules.property_panels import PropertyPanel

class PointPropertiesPanel(PropertyPanel):
    """点属性面板，提供X和Y坐标设置"""
    
    def __init__(self, parent=None):
        super().__init__(
            title="Propriétés du Point",
            bg_color="#FBE9E7",
            text_color="#E65100",
            parent=parent
        )
        
        # 创建控件
        self._create_controls()
        
        # 添加属性网格到主布局
        self.main_layout.addLayout(self.properties_layout)
        
        # 添加按钮布局
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addStretch()
    
    def _create_controls(self):
        """创建控件"""
        # X坐标
        self.properties_layout.addWidget(QLabel("X:"), 0, 0)
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(-50.0, 50.0)
        self.x_spin.setSingleStep(0.5)
        self.x_spin.setValue(0.0)
        self.properties_layout.addWidget(self.x_spin, 0, 1)
        
        # Y坐标
        self.properties_layout.addWidget(QLabel("Y:"), 1, 0)
        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(-50.0, 50.0)
        self.y_spin.setSingleStep(0.5)
        self.y_spin.setValue(0.0)
        self.properties_layout.addWidget(self.y_spin, 1, 1)
        
        # 连接值变化信号
        self.x_spin.valueChanged.connect(self._on_property_changed)
        self.y_spin.valueChanged.connect(self._on_property_changed)
    
    def get_properties(self) -> Dict[str, Any]:
        """获取当前设置的属性"""
        return {
            'x': self.x_spin.value(),
            'y': self.y_spin.value()
        }
    
    def set_properties(self, properties: Dict[str, Any]) -> None:
        """设置面板属性值"""
        if 'x' in properties:
            self.x_spin.setValue(properties['x'])
        if 'y' in properties:
            self.y_spin.setValue(properties['y'])
