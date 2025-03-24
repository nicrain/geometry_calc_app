import sys
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QGraphicsDropShadowEffect, QSizePolicy)
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QBrush

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# 导入自定义组件
from modules.ui_components_pyqt import BaseModule, MetroButton

class Canvas(QWidget):
    """自定义画布组件，用于绘制几何图形"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #CCCCCC;
                border-radius: 8px;
            }
        """)
        
        # 存储绘制的点和线段
        self.points = []
        self.lines = []
        self.line_texts = []  # 存储线段长度文本
        self.selected_line = None  # 当前选中的线段
        
        # 当前绘制的临时形状
        self.temp_shape = None
        self.start_x = None
        self.start_y = None
        
        # 当前选中的形状
        self.current_shape = None
        
        # 当前绘制模式
        self.draw_mode = None
        
        # 线段绘制的起始点
        self.line_start_point = None
        
        # 存储绘制的形状
        self.shapes = []
        
        # 坐标轴设置
        self.show_axes = True  # 是否显示坐标轴
        self.grid_spacing = 50  # 网格间距
        self.axis_color = "#555555"  # 坐标轴颜色
    
    def clear(self):
        """清除画布上的所有内容"""
        self.points = []
        self.lines = []
        self.line_texts = []
        self.selected_line = None
        self.temp_shape = None
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        self.draw_mode = None
        self.line_start_point = None
        self.update()  # 重绘画布
        
    def draw_coordinate_axes(self, painter):
        """绘制坐标轴"""
        # 获取画布中心点
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        # 设置坐标轴样式
        painter.setPen(QPen(QColor(self.axis_color), 1))
        
        # 绘制X轴
        painter.drawLine(0, center_y, self.width(), center_y)
        
        # 绘制Y轴
        painter.drawLine(center_x, 0, center_x, self.height())
        
        # 绘制刻度和标签
        painter.setFont(QFont("Arial", 8))
        
        # X轴刻度和标签
        for i in range(-10, 11):
            x = center_x + i * self.grid_spacing
            if 0 <= x <= self.width():
                # 绘制刻度线
                painter.drawLine(x, center_y - 5, x, center_y + 5)
                
                # 绘制标签，但跳过原点(0)
                if i != 0:
                    painter.drawText(QRect(x - 10, center_y + 10, 20, 15), 
                                    Qt.AlignmentFlag.AlignCenter, str(i))
        
        # Y轴刻度和标签
        for i in range(-10, 11):
            y = center_y + i * self.grid_spacing
            if 0 <= y <= self.height():
                # 绘制刻度线
                painter.drawLine(center_x - 5, y, center_x + 5, y)
                
                # 绘制标签，但跳过原点(0)，注意Y轴向下为正，所以标签要取负值
                if i != 0:
                    painter.drawText(QRect(center_x + 10, y - 10, 20, 20), 
                                    Qt.AlignmentFlag.AlignCenter, str(-i))
        
        # 在原点绘制O标记
        painter.drawText(QRect(center_x + 10, center_y + 10, 15, 15), 
                        Qt.AlignmentFlag.AlignCenter, "O")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制白色背景
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        
        # 绘制坐标轴
        if self.show_axes:
            self.draw_coordinate_axes(painter)
        
        # 绘制已保存的点
        for point in self.points:
            painter.setPen(QPen(QColor(point['color']), 2))
            painter.setBrush(QBrush(QColor(point['color'])))
            x = int(point['x'])
            y = int(point['y'])
            painter.drawEllipse(x - 5, y - 5, 10, 10)
        
        # 绘制已保存的线段
        for i, line in enumerate(self.lines):
            if self.selected_line == i:
                # 选中的线段用更粗的线
                painter.setPen(QPen(QColor(line['color']), 3))
            else:
                painter.setPen(QPen(QColor(line['color']), 2))
            
            painter.drawLine(int(line['x1']), int(line['y1']), int(line['x2']), int(line['y2']))
            
            # 绘制线段长度文本
            if i < len(self.line_texts):
                text = self.line_texts[i]
                mid_x = int((line['x1'] + line['x2']) / 2)
                mid_y = int((line['y1'] + line['y2']) / 2)
                painter.drawText(QRect(mid_x - 20, mid_y - 10, 40, 20), 
                                Qt.AlignmentFlag.AlignCenter, text)
        
        # 绘制临时形状
        if self.temp_shape and self.start_x is not None and self.start_y is not None:
            if self.current_shape == "square":
                painter.setPen(QPen(QColor("#1A237E"), 2))
                size = int(max(abs(self.temp_shape[0] - self.start_x), 
                           abs(self.temp_shape[1] - self.start_y)))
                painter.drawRect(int(self.start_x), int(self.start_y), size, size)
            
            elif self.current_shape == "circle":
                painter.setPen(QPen(QColor("#1B5E20"), 2))
                radius = int(((self.temp_shape[0] - self.start_x) ** 2 + 
                          (self.temp_shape[1] - self.start_y) ** 2) ** 0.5)
                painter.drawEllipse(int(self.start_x - radius), 
                                   int(self.start_y - radius), 
                                   radius * 2, radius * 2)
            
            elif self.current_shape == "triangle":
                painter.setPen(QPen(QColor("#311B92"), 2))
                # 等边三角形
                x1, y1 = int(self.start_x), int(self.start_y)
                x2, y2 = int(self.temp_shape[0]), int(self.temp_shape[1])
                # 计算第三个点，形成等边三角形
                x3 = int(x1 + (x2 - x1) * 0.5 - (y2 - y1) * 0.866)  # 0.866 = sqrt(3)/2
                y3 = int(y1 + (y2 - y1) * 0.5 + (x2 - x1) * 0.866)
                
                points = [QPoint(x1, y1), QPoint(x2, y2), QPoint(x3, y3)]
                painter.drawPolygon(points)
            
            elif self.draw_mode == "line" and self.line_start_point:
                painter.setPen(QPen(QColor("#0277BD"), 2))
                painter.drawLine(int(self.line_start_point[0]), int(self.line_start_point[1]),
                                int(self.temp_shape[0]), int(self.temp_shape[1]))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_x = event.position().x()
            self.start_y = event.position().y()
            
            if self.draw_mode == "point":
                # 添加一个点
                self.points.append({
                    'x': self.start_x,
                    'y': self.start_y,
                    'color': "#E65100"  # 橙色
                })
                self.update()
            
            elif self.draw_mode == "line":
                if self.line_start_point is None:
                    # 设置线段起点
                    self.line_start_point = (self.start_x, self.start_y)
                else:
                    # 完成线段绘制
                    x1, y1 = self.line_start_point
                    x2, y2 = self.start_x, self.start_y
                    
                    # 计算线段长度
                    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    length_text = f"{length:.1f}"
                    
                    # 添加线段
                    self.lines.append({
                        'x1': x1, 'y1': y1,
                        'x2': x2, 'y2': y2,
                        'color': "#0277BD"  # 蓝色
                    })
                    
                    # 添加长度文本
                    self.line_texts.append(length_text)
                    
                    # 重置起点
                    self.line_start_point = None
                    self.update()

class GeometryModule(BaseModule):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建标题
        title_label = QLabel("Module de Géométrie")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # 创建内容区域的水平布局
        content_layout = QHBoxLayout()
        self.main_layout.addLayout(content_layout)
        
        # 创建工具栏容器
        tools_frame = QWidget()
        tools_frame.setFixedWidth(240)  # 增加宽度以适应两列按钮
        tools_frame.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                border-right: 1px solid #CCCCCC;
            }
        """)
        tools_layout = QGridLayout(tools_frame)
        tools_layout.setContentsMargins(5, 5, 5, 5)
        tools_layout.setHorizontalSpacing(5)
        tools_layout.setVerticalSpacing(5)
        content_layout.addWidget(tools_frame)
        
        # 创建画布区域容器
        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(10, 0, 10, 10)
        content_layout.addWidget(canvas_container)
        
        # 初始化画布
        self.canvas = Canvas()
        canvas_layout.addWidget(self.canvas)
        
        # 初始化按钮引用
        self.circle_button = None
        self.square_button = None
        self.triangle_button = None
        self.point_button = None
        self.line_button = None
        self.active_button = None
        
        # 创建工具栏
        self.create_geometry_tools(tools_frame)
        
    def create_geometry_tools(self, tools_frame):
        # 添加返回主界面按钮
        return_button = MetroButton("Retour", "#757575", "#FFFFFF")
        return_button.setMinimumSize(110, 110)
        return_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        return_button.clicked.connect(self.back_to_home)
        tools_frame.layout().addWidget(return_button, 0, 0)
        
        # 添加点按钮
        self.point_button = MetroButton("Point", "#E65100", "#FFFFFF")
        self.point_button.setMinimumSize(110, 110)
        self.point_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.point_button.clicked.connect(lambda: self.select_draw_mode("point"))
        tools_frame.layout().addWidget(self.point_button, 0, 1)
        
        # 添加线段按钮
        self.line_button = MetroButton("Ligne", "#0277BD", "#FFFFFF")
        self.line_button.setMinimumSize(110, 110)
        self.line_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.line_button.clicked.connect(lambda: self.select_draw_mode("line"))
        tools_frame.layout().addWidget(self.line_button, 1, 0)
        
        # 添加正方形按钮
        self.square_button = MetroButton("Carré", "#1A237E", "#FFFFFF")
        self.square_button.setMinimumSize(110, 110)
        self.square_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.square_button.clicked.connect(lambda: self.select_shape("square"))
        tools_frame.layout().addWidget(self.square_button, 1, 1)
        
        # 添加圆形按钮
        self.circle_button = MetroButton("Cercle", "#1B5E20", "#FFFFFF")
        self.circle_button.setMinimumSize(110, 110)
        self.circle_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.circle_button.clicked.connect(lambda: self.select_shape("circle"))
        tools_frame.layout().addWidget(self.circle_button, 2, 0)
        
        # 添加三角形按钮
        self.triangle_button = MetroButton("Triangle", "#311B92", "#FFFFFF")
        self.triangle_button.setMinimumSize(110, 110)
        self.triangle_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.triangle_button.clicked.connect(lambda: self.select_shape("triangle"))
        tools_frame.layout().addWidget(self.triangle_button, 2, 1)
        
        # 添加清除按钮
        clear_button = MetroButton("Effacer", "#B71C1C", "#FFFFFF")
        clear_button.setMinimumSize(110, 110)
        clear_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        clear_button.clicked.connect(self.canvas.clear)
        tools_frame.layout().addWidget(clear_button, 3, 0)
        
        # 添加坐标轴切换按钮
        self.axes_button = MetroButton("Axes", "#607D8B", "#FFFFFF")
        self.axes_button.setMinimumSize(110, 110)
        self.axes_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.axes_button.clicked.connect(self.toggle_axes)
        self.axes_button.set_active(self.canvas.show_axes)  # 根据当前状态设置按钮状态
        tools_frame.layout().addWidget(self.axes_button, 3, 1)
        
        # 添加弹性空间
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        tools_frame.layout().addWidget(spacer)
        
    def select_draw_mode(self, mode):
        self.canvas.draw_mode = mode
        self.canvas.current_shape = None
        
        # 重置所有按钮状态
        for button in [self.point_button, self.line_button, self.square_button, 
                      self.circle_button, self.triangle_button]:
            if button:
                button.set_active(False)
        
        # 设置当前按钮状态
        if mode == "point":
            self.point_button.set_active(True)
        elif mode == "line":
            self.line_button.set_active(True)
    
    def select_shape(self, shape):
        self.canvas.current_shape = shape
        self.canvas.draw_mode = None
        self.canvas.line_start_point = None
        
        # 重置所有按钮状态
        for button in [self.point_button, self.line_button, self.square_button, 
                      self.circle_button, self.triangle_button]:
            if button:
                button.set_active(False)
        
        # 设置当前按钮状态
        if shape == "square":
            self.square_button.set_active(True)
        elif shape == "circle":
            self.circle_button.set_active(True)
        elif shape == "triangle":
            self.triangle_button.set_active(True)
    
    def back_to_home(self):
        # 获取主应用程序实例并调用返回主页面方法
        parent = self.parent()
        while parent:
            if hasattr(parent, 'back_to_home'):
                parent.back_to_home()
                break
            parent = parent.parent()
    
    def toggle_axes(self):
        """切换坐标轴显示状态"""
        self.canvas.show_axes = not self.canvas.show_axes
        self.axes_button.set_active(self.canvas.show_axes)
        self.canvas.update()  # 重绘画布
