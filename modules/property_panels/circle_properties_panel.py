"""
圆形属性面板的实现。
"""
import math
from typing import Dict, Any
from PyQt6.QtWidgets import QLabel, QDoubleSpinBox, QGridLayout
from PyQt6.QtCore import Qt

from modules.property_panels import PropertyPanel

class CirclePropertiesPanel(PropertyPanel):
    """圆形属性面板，提供半径和位置设置"""
    
    def __init__(self, parent=None):
        super().__init__(
            title="Propriétés du Cercle",
            bg_color="#E8F5E9",
            text_color="#1B5E20",
            parent=parent
        )
        
        # 创建属性设置控件
        self._create_controls()
        
        # 添加属性网格到主布局
        self.main_layout.addLayout(self.properties_layout)
        
        # 添加按钮布局
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addStretch()
    
    def _create_controls(self):
        """创建控件"""
        # 半径设置
        self.properties_layout.addWidget(QLabel("Rayon:"), 0, 0)
        self.radius_spin = QDoubleSpinBox()
        self.radius_spin.setRange(0.1, 50.0)
        self.radius_spin.setSingleStep(0.5)
        self.radius_spin.setValue(3.0)
        self.radius_spin.setSuffix(" cm")
        self.properties_layout.addWidget(self.radius_spin, 0, 1)
        
        # X坐标 (圆心)
        self.properties_layout.addWidget(QLabel("X:"), 1, 0)
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(-50.0, 50.0)
        self.x_spin.setSingleStep(1.0)
        self.x_spin.setValue(0.0)
        self.properties_layout.addWidget(self.x_spin, 1, 1)
        
        # Y坐标 (圆心)
        self.properties_layout.addWidget(QLabel("Y:"), 2, 0)
        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(-50.0, 50.0)
        self.y_spin.setSingleStep(1.0)
        self.y_spin.setValue(0.0)
        self.properties_layout.addWidget(self.y_spin, 2, 1)
        
        # 周长显示（只读）
        self.properties_layout.addWidget(QLabel("Circonférence:"), 3, 0)
        self.circumference_label = QLabel("18.85 cm")
        self.circumference_label.setStyleSheet("color: #01579B; background-color: #E1F5FE; padding: 2px 5px; border-radius: 2px;")
        self.properties_layout.addWidget(self.circumference_label, 3, 1)
        
        # 面积显示（只读）
        self.properties_layout.addWidget(QLabel("Surface:"), 4, 0)
        self.area_label = QLabel("28.27 cm²")
        self.area_label.setStyleSheet("color: #01579B; background-color: #E1F5FE; padding: 2px 5px; border-radius: 2px;")
        self.properties_layout.addWidget(self.area_label, 4, 1)
        
        # 连接值变化信号
        self.radius_spin.valueChanged.connect(self._update_derived_values)
        self.x_spin.valueChanged.connect(self._on_property_changed)
        self.y_spin.valueChanged.connect(self._on_property_changed)
        
        # 初始化计算派生值
        self._update_derived_values()
    
    def _update_derived_values(self):
        """更新派生值（周长和面积）"""
        # 获取半径
        radius = self.radius_spin.value()
        
        # 计算周长
        circumference = 2 * math.pi * radius
        self.circumference_label.setText(f"{circumference:.2f} cm")
        
        # 计算面积
        area = math.pi * (radius ** 2)
        self.area_label.setText(f"{area:.2f} cm²")
        
        # 发送属性变化信号
        self._on_property_changed()
    
    def get_properties(self) -> Dict[str, Any]:
        """获取当前设置的属性"""
        return {
            'radius': self.radius_spin.value(),
            'x': self.x_spin.value(),
            'y': self.y_spin.value()
        }
    
    def set_properties(self, properties: Dict[str, Any]) -> None:
        """设置面板属性值"""
        if 'radius' in properties:
            self.radius_spin.setValue(properties['radius'])
        if 'x' in properties:
            self.x_spin.setValue(properties['x'])
        if 'y' in properties:
            self.y_spin.setValue(properties['y'])
        
        # 更新派生值
        self._update_derived_values()
