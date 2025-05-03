import math
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QDoubleSpinBox, QPushButton, QSizePolicy,
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

class LinePropertiesPanel(QFrame):
    """线段属性面板，提供长度、角度和起点位置设置"""
    
    # 定义信号
    line_created = pyqtSignal(float, float, float, float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: #E3F2FD;
                border-radius: 8px;
                border: 1px solid #90CAF9;
            }
            QLabel {
                color: #0277BD;
                font-weight: bold;
            }
        """)
        
        # 设置阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor("#CCCCCC"))
        shadow.setOffset(2, 2)
        self.setGraphicsEffect(shadow)
        
        # 设置布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # 标题
        title_label = QLabel("Propriétés de la Ligne", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #0277BD;")
        layout.addWidget(title_label)
        
        # 创建属性设置网格
        properties_layout = QGridLayout()
        properties_layout.setVerticalSpacing(10)
        properties_layout.setHorizontalSpacing(8)
        
        # 长度设置
        properties_layout.addWidget(QLabel("Longueur:"), 0, 0)
        self.length_spin = QDoubleSpinBox()
        self.length_spin.setRange(0.1, 50.0)
        self.length_spin.setSingleStep(0.5)
        self.length_spin.setValue(5.0)
        self.length_spin.setSuffix(" cm")
        properties_layout.addWidget(self.length_spin, 0, 1)
        
        # 角度设置
        properties_layout.addWidget(QLabel("Angle:"), 1, 0)
        self.angle_spin = QDoubleSpinBox()
        self.angle_spin.setRange(0, 359.9)
        self.angle_spin.setSingleStep(5.0)
        self.angle_spin.setValue(0.0)
        self.angle_spin.setSuffix("°")
        properties_layout.addWidget(self.angle_spin, 1, 1)
        
        # X坐标（起点）
        properties_layout.addWidget(QLabel("X:"), 2, 0)
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(-50.0, 50.0)
        self.x_spin.setSingleStep(1.0)
        self.x_spin.setValue(0.0)
        properties_layout.addWidget(self.x_spin, 2, 1)
        
        # Y坐标（起点）
        properties_layout.addWidget(QLabel("Y:"), 3, 0)
        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(-50.0, 50.0)
        self.y_spin.setSingleStep(1.0)
        self.y_spin.setValue(0.0)
        properties_layout.addWidget(self.y_spin, 3, 1)
        
        layout.addLayout(properties_layout)
        
        # 创建按钮
        buttons_layout = QHBoxLayout()
        
        # 创建线段按钮
        self.create_button = QPushButton("Créer")
        self.create_button.setStyleSheet("""
            QPushButton {
                background-color: #0277BD; 
                color: white; 
                border-radius: 4px; 
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0288D1;
            }
        """)
        self.create_button.clicked.connect(self.create_line)
        buttons_layout.addWidget(self.create_button)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        # 设置尺寸策略
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedWidth(220)
    
    def create_line(self):
        """根据输入的参数创建线段"""
        # 获取输入参数
        length = self.length_spin.value()
        angle_deg = self.angle_spin.value()
        x1 = self.x_spin.value()
        y1 = self.y_spin.value()
        
        # 将角度转换为弧度
        angle_rad = math.radians(angle_deg)
        
        # 计算终点坐标
        # 注意：在屏幕坐标系中，y轴向下为正，所以sin前要加负号
        x2 = x1 + length * math.cos(angle_rad)
        y2 = y1 - length * math.sin(angle_rad)  # 减号是因为屏幕坐标系y轴向下为正
        
        # 发射信号，传递线段的起点和终点坐标
        self.line_created.emit(x1, y1, x2, y2)
    
    def get_properties(self):
        """获取当前设置的属性"""
        return {
            'length': self.length_spin.value(),
            'angle': self.angle_spin.value(),
            'x': self.x_spin.value(),
            'y': self.y_spin.value()
        }
    
    def set_properties(self, properties):
        """设置面板属性值"""
        if 'length' in properties:
            self.length_spin.setValue(properties['length'])
        if 'angle' in properties:
            self.angle_spin.setValue(properties['angle'])
        if 'x' in properties:
            self.x_spin.setValue(properties['x'])
        if 'y' in properties:
            self.y_spin.setValue(properties['y'])