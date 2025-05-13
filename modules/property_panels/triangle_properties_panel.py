"""
三角形属性面板的实现。
"""
import math
from typing import Dict, Any
from PyQt6.QtWidgets import QLabel, QDoubleSpinBox, QGridLayout
from PyQt6.QtCore import Qt

from modules.property_panels import PropertyPanel

class TrianglePropertiesPanel(PropertyPanel):
    """三角形属性面板，提供三个顶点坐标设置"""
    
    def __init__(self, parent=None):
        super().__init__(
            title="Propriétés du Triangle",
            bg_color="#EDE7F6",
            text_color="#311B92",
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
        # 创建更紧凑的布局
        # 第一个顶点 (A)
        self.properties_layout.addWidget(QLabel("点 A:"), 0, 0)
        
        # X1坐标
        self.properties_layout.addWidget(QLabel("X:"), 1, 0)
        self.x1_spin = QDoubleSpinBox()
        self.x1_spin.setRange(-50.0, 50.0)
        self.x1_spin.setSingleStep(0.5)
        self.x1_spin.setValue(-2.0)
        self.properties_layout.addWidget(self.x1_spin, 1, 1)
        
        # Y1坐标
        self.properties_layout.addWidget(QLabel("Y:"), 2, 0)
        self.y1_spin = QDoubleSpinBox()
        self.y1_spin.setRange(-50.0, 50.0)
        self.y1_spin.setSingleStep(0.5)
        self.y1_spin.setValue(-2.0)
        self.properties_layout.addWidget(self.y1_spin, 2, 1)
        
        # 第二个顶点 (B)
        self.properties_layout.addWidget(QLabel("点 B:"), 3, 0)
        
        # X2坐标
        self.properties_layout.addWidget(QLabel("X:"), 4, 0)
        self.x2_spin = QDoubleSpinBox()
        self.x2_spin.setRange(-50.0, 50.0)
        self.x2_spin.setSingleStep(0.5)
        self.x2_spin.setValue(2.0)
        self.properties_layout.addWidget(self.x2_spin, 4, 1)
        
        # Y2坐标
        self.properties_layout.addWidget(QLabel("Y:"), 5, 0)
        self.y2_spin = QDoubleSpinBox()
        self.y2_spin.setRange(-50.0, 50.0)
        self.y2_spin.setSingleStep(0.5)
        self.y2_spin.setValue(-2.0)
        self.properties_layout.addWidget(self.y2_spin, 5, 1)
        
        # 第三个顶点 (C)
        self.properties_layout.addWidget(QLabel("点 C:"), 6, 0)
        
        # X3坐标
        self.properties_layout.addWidget(QLabel("X:"), 7, 0)
        self.x3_spin = QDoubleSpinBox()
        self.x3_spin.setRange(-50.0, 50.0)
        self.x3_spin.setSingleStep(0.5)
        self.x3_spin.setValue(0.0)
        self.properties_layout.addWidget(self.x3_spin, 7, 1)
        
        # Y3坐标
        self.properties_layout.addWidget(QLabel("Y:"), 8, 0)
        self.y3_spin = QDoubleSpinBox()
        self.y3_spin.setRange(-50.0, 50.0)
        self.y3_spin.setSingleStep(0.5)
        self.y3_spin.setValue(2.0)
        self.properties_layout.addWidget(self.y3_spin, 8, 1)
        
        # 周长显示（只读）
        self.properties_layout.addWidget(QLabel("周长:"), 9, 0)
        self.perimeter_label = QLabel("12.00 cm")
        self.perimeter_label.setStyleSheet("color: #311B92; background-color: #EDE7F6; padding: 2px 5px; border-radius: 2px;")
        self.properties_layout.addWidget(self.perimeter_label, 9, 1)
        
        # 面积显示（只读）
        self.properties_layout.addWidget(QLabel("面积:"), 10, 0)
        self.area_label = QLabel("8.00 cm²")
        self.area_label.setStyleSheet("color: #311B92; background-color: #EDE7F6; padding: 2px 5px; border-radius: 2px;")
        self.properties_layout.addWidget(self.area_label, 10, 1)
        
        # 连接值变化信号
        self.x1_spin.valueChanged.connect(self._update_derived_values)
        self.y1_spin.valueChanged.connect(self._update_derived_values)
        self.x2_spin.valueChanged.connect(self._update_derived_values)
        self.y2_spin.valueChanged.connect(self._update_derived_values)
        self.x3_spin.valueChanged.connect(self._update_derived_values)
        self.y3_spin.valueChanged.connect(self._update_derived_values)
        
        # 初始化计算派生值
        self._update_derived_values()
    
    def _update_derived_values(self):
        """更新派生值（面积和周长）"""
        # 获取坐标值
        x1 = self.x1_spin.value()
        y1 = self.y1_spin.value()
        x2 = self.x2_spin.value()
        y2 = self.y2_spin.value()
        x3 = self.x3_spin.value()
        y3 = self.y3_spin.value()
        
        # 计算三条边的长度
        side1 = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        side2 = ((x3 - x2)**2 + (y3 - y2)**2)**0.5
        side3 = ((x1 - x3)**2 + (y1 - y3)**2)**0.5
        
        # 计算周长
        perimeter = side1 + side2 + side3
        self.perimeter_label.setText(f"{perimeter:.2f} cm")
        
        # 计算面积（使用海伦公式）
        s = perimeter / 2
        try:
            area = (s * (s - side1) * (s - side2) * (s - side3)) ** 0.5
            self.area_label.setText(f"{area:.2f} cm²")
        except ValueError:
            # 处理无法形成三角形的情况
            self.area_label.setText("无效三角形")
        
        # 发送属性变化信号
        self._on_property_changed()
    
    def get_properties(self) -> Dict[str, Any]:
        """获取当前设置的属性"""
        return {
            'x1': self.x1_spin.value(),
            'y1': self.y1_spin.value(),
            'x2': self.x2_spin.value(),
            'y2': self.y2_spin.value(),
            'x3': self.x3_spin.value(),
            'y3': self.y3_spin.value()
        }
    
    def set_properties(self, properties: Dict[str, Any]) -> None:
        """设置面板属性值"""
        if 'x1' in properties:
            self.x1_spin.setValue(properties['x1'])
        if 'y1' in properties:
            self.y1_spin.setValue(properties['y1'])
        if 'x2' in properties:
            self.x2_spin.setValue(properties['x2'])
        if 'y2' in properties:
            self.y2_spin.setValue(properties['y2'])
        if 'x3' in properties:
            self.x3_spin.setValue(properties['x3'])
        if 'y3' in properties:
            self.y3_spin.setValue(properties['y3'])
        
        # 更新派生值
        self._update_derived_values()
