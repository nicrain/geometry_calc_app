"""
线段属性面板的实现
"""
import math
from typing import Dict, Any
from PyQt6.QtWidgets import QLabel, QDoubleSpinBox

from modules.property_panels import PropertyPanel

class LinePropertiesPanel(PropertyPanel):
    """线段属性面板，提供坐标设置"""
    
    def __init__(self, parent=None):
        super().__init__(
            title="Propriétés de la Ligne",
            bg_color="#E3F2FD",
            text_color="#0277BD",
            parent=parent
        )
        
        # 创建控件
        self._create_controls()
        
        # 添加属性网格到主布局
        self.main_layout.addLayout(self.properties_layout)
        
        # 添加按钮布局
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addStretch()
        
        # 初始化计算长度和角度
        self._update_length_and_angle()
    
    def _create_controls(self):
        """创建控件"""
        # 起始点X坐标
        self.properties_layout.addWidget(QLabel("X1:"), 0, 0)
        self.x1_spin = QDoubleSpinBox()
        self.x1_spin.setRange(-50.0, 50.0)
        self.x1_spin.setSingleStep(0.5)
        self.x1_spin.setValue(-2.0)
        self.properties_layout.addWidget(self.x1_spin, 0, 1)
        
        # 起始点Y坐标
        self.properties_layout.addWidget(QLabel("Y1:"), 1, 0)
        self.y1_spin = QDoubleSpinBox()
        self.y1_spin.setRange(-50.0, 50.0)
        self.y1_spin.setSingleStep(0.5)
        self.y1_spin.setValue(-1.0)
        self.properties_layout.addWidget(self.y1_spin, 1, 1)
        
        # 终点X坐标
        self.properties_layout.addWidget(QLabel("X2:"), 2, 0)
        self.x2_spin = QDoubleSpinBox()
        self.x2_spin.setRange(-50.0, 50.0)
        self.x2_spin.setSingleStep(0.5)
        self.x2_spin.setValue(2.0)
        self.properties_layout.addWidget(self.x2_spin, 2, 1)
        
        # 终点Y坐标
        self.properties_layout.addWidget(QLabel("Y2:"), 3, 0)
        self.y2_spin = QDoubleSpinBox()
        self.y2_spin.setRange(-50.0, 50.0)
        self.y2_spin.setSingleStep(0.5)
        self.y2_spin.setValue(1.0)
        self.properties_layout.addWidget(self.y2_spin, 3, 1)
        
        # 长度显示（只读）
        self.properties_layout.addWidget(QLabel("Longueur:"), 4, 0)
        self.length_label = QLabel("4.47 cm")
        self.length_label.setStyleSheet("color: #01579B; background-color: #E1F5FE; padding: 2px 5px; border-radius: 2px;")
        self.properties_layout.addWidget(self.length_label, 4, 1)
        
        # 角度显示（只读）
        self.properties_layout.addWidget(QLabel("Angle:"), 5, 0)
        self.angle_label = QLabel("45.0°")
        self.angle_label.setStyleSheet("color: #01579B; background-color: #E1F5FE; padding: 2px 5px; border-radius: 2px;")
        self.properties_layout.addWidget(self.angle_label, 5, 1)
        
        # 连接值变化信号
        self.x1_spin.valueChanged.connect(self._property_changed)
        self.y1_spin.valueChanged.connect(self._property_changed)
        self.x2_spin.valueChanged.connect(self._property_changed)
        self.y2_spin.valueChanged.connect(self._property_changed)
    
    def _property_changed(self):
        """属性值变化事件处理"""
        self._update_length_and_angle()
        self._on_property_changed()
    
    def _update_length_and_angle(self):
        """更新长度和角度显示"""
        x1 = self.x1_spin.value()
        y1 = self.y1_spin.value()
        x2 = self.x2_spin.value()
        y2 = self.y2_spin.value()
        
        # 计算长度
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        self.length_label.setText(f"{length:.2f} cm")
        
        # 计算角度（弧度）
        angle_rad = math.atan2(y2 - y1, x2 - x1)
        # 转换为度数 (0-360°)
        angle_deg = (angle_rad * 180 / math.pi) % 360
        self.angle_label.setText(f"{angle_deg:.1f}°")
    
    def get_properties(self) -> Dict[str, Any]:
        """获取当前设置的属性"""
        return {
            'x1': self.x1_spin.value(),
            'y1': self.y1_spin.value(),
            'x2': self.x2_spin.value(),
            'y2': self.y2_spin.value()
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
        
        # 更新长度和角度
        self._update_length_and_angle()
