import sys
import math
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# 导入PyQt6模块
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QFrame, QGraphicsDropShadowEffect, QSizePolicy,
                             QDoubleSpinBox, QPushButton)
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QBrush

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
        
        # 当前鼠标位置
        self.current_mouse_x = None
        self.current_mouse_y = None
        
        # 启用鼠标跟踪
        self.setMouseTracking(True)
    
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
        
        # 绘制X轴和Y轴
        painter.drawLine(0, center_y, self.width(), center_y)  # X轴
        painter.drawLine(center_x, 0, center_x, self.height()) # Y轴
        
        # 绘制刻度和标签
        painter.setFont(QFont("Arial", 8))
        
        # 绘制X轴和Y轴刻度
        self._draw_axis_ticks(painter, center_x, center_y, True)  # X轴刻度
        self._draw_axis_ticks(painter, center_x, center_y, False) # Y轴刻度
        
        # 在原点绘制O标记
        painter.drawText(QRect(center_x + 10, center_y + 10, 15, 15), 
                        Qt.AlignmentFlag.AlignCenter, "O")
    
    def _draw_axis_ticks(self, painter, center_x, center_y, is_x_axis):
        """绘制坐标轴刻度和标签
        
        Args:
            painter: QPainter对象
            center_x: 中心点X坐标
            center_y: 中心点Y坐标
            is_x_axis: 是否是X轴
        """
        for i in range(-10, 11):
            if i == 0:  # 跳过原点
                continue
                
            if is_x_axis:
                # X轴刻度和标签
                x = center_x + i * self.grid_spacing
                if 0 <= x <= self.width():
                    # 绘制刻度线
                    painter.drawLine(x, center_y - 5, x, center_y + 5)
                    # 绘制标签
                    painter.drawText(QRect(x - 10, center_y + 10, 20, 15), 
                                    Qt.AlignmentFlag.AlignCenter, str(i))
            else:
                # Y轴刻度和标签，注意Y轴向下为正，所以标签要取负值
                y = center_y + i * self.grid_spacing
                if 0 <= y <= self.height():
                    # 绘制刻度线
                    painter.drawLine(center_x - 5, y, center_x + 5, y)
                    # 绘制标签
                    painter.drawText(QRect(center_x + 10, y - 10, 20, 20), 
                                    Qt.AlignmentFlag.AlignCenter, str(-i))
                                    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制白色背景
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        
        # 绘制坐标轴
        if self.show_axes:
            self.draw_coordinate_axes(painter)
        
        # 绘制已保存的点
        for i, point in enumerate(self.points):
            # 设置点的颜色
            painter.setPen(QPen(QColor(point['color']), 2))
            painter.setBrush(QBrush(QColor(point['color'])))
            x = int(point['x'])
            y = int(point['y'])
            
            # 绘制点
            painter.drawEllipse(x - 5, y - 5, 10, 10)
            
            # 绘制点的名称标签 (A, B, C, ...)
            point_name = 'ABCDEFGHIJKLMN'[i % 14]
            
            # 设置标签文本颜色和字体
            painter.setPen(QPen(QColor("#000000")))
            font = QFont("Arial", 10)
            font.setBold(True)
            painter.setFont(font)
            
            # 在点上方绘制标签
            painter.drawText(x - 5, y - 10, point_name)
        
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
        if self.temp_shape:
            if self.current_shape == "square" and self.line_start_point is not None:
                # 优化后的正方形绘制逻辑
                # 使用虚线绘制正方形预览
                dash_pen = QPen(QColor("#1A237E"), 2, Qt.PenStyle.DashLine)
                painter.setPen(dash_pen)
                # 明确设置空白画刷，确保不填充
                painter.setBrush(Qt.BrushStyle.NoBrush)
                
                # 获取起点和鼠标当前位置
                x1, y1 = self.line_start_point
                end_x, end_y = self.temp_shape
                
                # 计算边长（取横向和纵向距离的最大值）
                side_length = max(abs(end_x - x1), abs(end_y - y1))
                
                # 根据鼠标位置确定正方形的方向
                dx = 1 if end_x >= x1 else -1
                dy = 1 if end_y >= y1 else -1
                
                # 计算正方形的四个顶点
                # x1, y1 已经是起始点
                x2, y2 = x1 + side_length * dx, y1   # 右/左上角
                x3, y3 = x1 + side_length * dx, y1 + side_length * dy  # 右/左下角
                x4, y4 = x1, y1 + side_length * dy   # 左/右下角
                
                # 绘制正方形轮廓，不填充
                points = [QPoint(int(x1), int(y1)), QPoint(int(x2), int(y2)), 
                         QPoint(int(x3), int(y3)), QPoint(int(x4), int(y4))]
                # 使用drawPolygon绘制时可能会填充，改为drawPolyline确保只绘制轮廓
                closed_points = points + [points[0]]  # 添加第一个点以闭合图形
                painter.drawPolyline(closed_points)
                
                # 绘制对角顶点
                painter.setPen(QPen(QColor("#FF5722"), 2))
                painter.setBrush(QBrush(QColor("#FF5722")))
                painter.drawEllipse(int(x3) - 5, int(y3) - 5, 10, 10)
                
                # 可选：显示边长
                mid_x = (x1 + x3) / 2
                mid_y = (y1 + y3) / 2
                
                # 计算实际边长（相对于坐标系）
                real_side = side_length / self.grid_spacing if self.grid_spacing else side_length
                side_text = f"{real_side:.1f}"
                
                # 设置文本样式
                painter.setPen(QPen(QColor("#000000")))
                font = QFont("Arial", 9)
                painter.setFont(font)
                
                # 绘制边长文本
                painter.drawText(QRect(int(mid_x - 20), int(mid_y - 10), 40, 20), 
                                Qt.AlignmentFlag.AlignCenter, side_text)
            
            elif self.current_shape == "circle" and self.line_start_point is not None:
                painter.setPen(QPen(QColor("#1B5E20"), 2))
                x1, y1 = self.line_start_point
                radius = int(((self.temp_shape[0] - x1) ** 2 + 
                          (self.temp_shape[1] - y1) ** 2) ** 0.5)
                painter.drawEllipse(int(x1 - radius), 
                                   int(y1 - radius), 
                                   radius * 2, radius * 2)
            
            elif self.current_shape == "triangle" and self.line_start_point is not None:
                painter.setPen(QPen(QColor("#311B92"), 2))
                # 等边三角形
                x1, y1 = int(self.line_start_point[0]), int(self.line_start_point[1])
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
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件，用于实时显示坐标和临时线段"""
        self.current_mouse_x = event.position().x()
        self.current_mouse_y = event.position().y()
        
        # 如果有父组件的方法来更新鼠标位置信息，则调用它
        parent = self.parent()
        while parent:
            if hasattr(parent, 'update_mouse_position_info'):
                parent.update_mouse_position_info(self.current_mouse_x, self.current_mouse_y)
                break
            parent = parent.parent()
        
        # 如果在线段绘制模式下且已有起点，则更新临时线段
        if self.draw_mode == "line" and self.line_start_point is not None:
            self.temp_shape = (self.current_mouse_x, self.current_mouse_y)
            self.update()  # 重绘画布以显示临时线段
            
            # 更新线段信息
            parent = self.parent()
            while parent:
                if hasattr(parent, 'update_line_info'):
                    x1, y1 = self.line_start_point
                    x2, y2 = self.current_mouse_x, self.current_mouse_y
                    length = ((x2 - x1) ** 2 + (y1 - y2) ** 2) ** 0.5
                    parent.update_line_info(x1, y1, x2, y2, length)
                    break
                parent = parent.parent()
        
        # 如果在正方形绘制模式下且已有起点，则更新临时正方形
        elif self.current_shape == "square" and self.line_start_point is not None:
            self.temp_shape = (self.current_mouse_x, self.current_mouse_y)
            self.update()  # 重绘画布以显示临时正方形
            
            # 计算正方形的边长（取横向和纵向距离的最大值，确保是正方形）
            x1, y1 = self.line_start_point
            size = max(abs(self.current_mouse_x - x1), abs(self.current_mouse_y - y1))
            
            # 更新正方形信息
            parent = self.parent()
            while parent:
                if hasattr(parent, 'update_square_info'):
                    parent.update_square_info(x1, y1, size)
                    break
                parent = parent.parent()
        
        # 调用父类的mouseMoveEvent
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """鼠标释放事件，用于重置临时状态或完成形状绘制"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 如果在正方形绘制模式下且有起点和临时形状，则完成正方形绘制
            if self.current_shape == "square" and self.line_start_point is not None and self.temp_shape is not None:
                # 获取起点和终点
                x1, y1 = self.line_start_point
                end_x, end_y = self.temp_shape
                
                # 计算边长（取横向和纵向距离的最大值）
                side_length = max(abs(end_x - x1), abs(end_y - y1))
                
                # 根据鼠标位置确定正方形的方向
                dx = 1 if end_x >= x1 else -1
                dy = 1 if end_y >= y1 else -1
                
                # 计算正方形的四个顶点
                # x1, y1 已经是起始点
                x2, y2 = x1 + side_length * dx, y1   # 右/左上角
                x3, y3 = x1 + side_length * dx, y1 + side_length * dy  # 右/左下角
                x4, y4 = x1, y1 + side_length * dy   # 左/右下角
                
                # 添加第二个点（对角顶点）
                self.points.append({'x': x3, 'y': y3, 'color': "#1A237E"})
                
                # 添加其他两个顶点
                self.points.append({'x': x2, 'y': y2, 'color': "#1A237E"})
                self.points.append({'x': x4, 'y': y4, 'color': "#1A237E"})
                
                # 添加四条边作为线段
                self.lines.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': "#1A237E"})
                self.lines.append({'x1': x2, 'y1': y2, 'x2': x3, 'y2': y3, 'color': "#1A237E"})
                self.lines.append({'x1': x3, 'y1': y3, 'x2': x4, 'y2': y4, 'color': "#1A237E"})
                self.lines.append({'x1': x4, 'y1': y4, 'x2': x1, 'y2': y1, 'color': "#1A237E"})
                
                # 计算实际边长（相对于坐标系）
                real_side = side_length / self.grid_spacing if self.grid_spacing else side_length
                side_text = f"{real_side:.1f}"
                
                # 添加边长文本
                for _ in range(4):
                    self.line_texts.append(side_text)
                
                # 计算和存储正方形的属性：面积和周长
                area = side_length ** 2
                perimeter = 4 * side_length
                
                # 存储到形状属性中
                self.shapes.append({
                    'type': 'square',
                    'vertices': [(x1, y1), (x2, y2), (x3, y3), (x4, y4)],
                    'side': side_length,
                    'area': area,
                    'perimeter': perimeter,
                    'color': "#1A237E"
                })
                
                # 重置临时状态
                self.line_start_point = None
                self.temp_shape = None
                
                # 更新坐标信息
                parent = self.parent()
                while parent:
                    if hasattr(parent, 'update_square_info_complete'):
                        parent.update_square_info_complete(real_side, (real_side ** 2) / self.grid_spacing)
                        break
                    elif hasattr(parent, 'update_coordinate_info'):
                        parent.update_coordinate_info()
                        break
                    parent = parent.parent()
                
                self.update()
            # 如果不在线段绘制模式下，或者已经完成了一条线段的绘制，则重置临时形状
            elif self.draw_mode != "line" or self.line_start_point is None:
                self.temp_shape = None
                self.update()  # 重绘画布以清除临时线段
        
        # 调用父类的mouseReleaseEvent
        super().mouseReleaseEvent(event)
    
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
                # 如果有父组件的方法来更新坐标信息，则调用它
                parent = self.parent()
                while parent:
                    if hasattr(parent, 'update_coordinate_info'):
                        parent.update_coordinate_info()
                        break
                    parent = parent.parent()
                self.update()
            
            # 在正方形绘制模式下，使用与线段相同的交互方式
            elif self.current_shape == "square":
                if self.line_start_point is None:
                    # 设置正方形起点
                    self.line_start_point = (self.start_x, self.start_y)
                    # 重置临时形状
                    self.temp_shape = None
                    # 添加起点作为一个点
                    self.points.append({
                        'x': self.start_x,
                        'y': self.start_y,
                        'color': "#1A237E"  # 深蓝色
                    })
                    # 更新坐标信息
                    parent = self.parent()
                    while parent:
                        if hasattr(parent, 'update_coordinate_info'):
                            parent.update_coordinate_info()
                            break
                        parent = parent.parent()
                    self.update()
                else:
                    # 完成正方形绘制
                    self.temp_shape = (self.start_x, self.start_y)
                    # 触发mouseReleaseEvent中的正方形绘制逻辑
                    self.mouseReleaseEvent(event)
            
            elif self.draw_mode == "line":
                if self.line_start_point is None:
                    # 设置线段起点
                    self.line_start_point = (self.start_x, self.start_y)
                    # 重置临时形状，避免与上一条线段连接
                    self.temp_shape = None
                    # 添加起点作为一个点
                    self.points.append({
                        'x': self.start_x,
                        'y': self.start_y,
                        'color': "#0277BD"  # 蓝色
                    })
                    # 更新坐标信息
                    parent = self.parent()
                    while parent:
                        if hasattr(parent, 'update_coordinate_info'):
                            parent.update_coordinate_info()
                            break
                        parent = parent.parent()
                    self.update()
                else:
                    # 完成线段绘制
                    x1, y1 = self.line_start_point
                    x2, y2 = self.start_x, self.start_y
                    
                    # 添加终点作为一个点
                    self.points.append({
                        'x': x2,
                        'y': y2,
                        'color': "#0277BD"  # 蓝色
                    })
                    
                    # 计算线段长度
                    length = ((x2 - x1) ** 2 + (y1 - y2) ** 2) ** 0.5
                    length_text = f"{length:.1f}"
                    
                    # 添加线段
                    self.lines.append({
                        'x1': x1, 'y1': y1,
                        'x2': x2, 'y2': y2,
                        'color': "#0277BD"  # 蓝色
                    })
                    
                    # 添加长度文本
                    self.line_texts.append(length_text)
                    
                    # 重置起点和临时形状
                    self.line_start_point = None
                    self.temp_shape = None
                    
                    # 更新坐标信息
                    parent = self.parent()
                    while parent:
                        if hasattr(parent, 'update_coordinate_info'):
                            parent.update_coordinate_info()
                            break
                        parent = parent.parent()
                    self.update()

class SimpleSquarePropertiesPanel(QFrame):
    """简化的正方形属性面板，只提供边长和位置设置"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: #E8F5E9;
                border-radius: 8px;
                border: 1px solid #A5D6A7;
            }
            QLabel {
                color: #1B5E20;
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
        title_label = QLabel("Propriétés du Carré", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1B5E20;")
        layout.addWidget(title_label)
        
        # 创建属性设置网格
        properties_layout = QGridLayout()
        properties_layout.setVerticalSpacing(10)
        properties_layout.setHorizontalSpacing(8)
        
        # 边长设置
        properties_layout.addWidget(QLabel("Côté:"), 0, 0)
        self.side_length_spin = QDoubleSpinBox()
        self.side_length_spin.setRange(0.1, 50.0)
        self.side_length_spin.setSingleStep(0.5)
        self.side_length_spin.setValue(5.0)
        self.side_length_spin.setSuffix(" cm")
        properties_layout.addWidget(self.side_length_spin, 0, 1)
        
        # X坐标
        properties_layout.addWidget(QLabel("X:"), 1, 0)
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(-50.0, 50.0)
        self.x_spin.setSingleStep(1.0)
        self.x_spin.setValue(0.0)
        properties_layout.addWidget(self.x_spin, 1, 1)
        
        # Y坐标
        properties_layout.addWidget(QLabel("Y:"), 2, 0)
        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(-50.0, 50.0)
        self.y_spin.setSingleStep(1.0)
        self.y_spin.setValue(0.0)
        properties_layout.addWidget(self.y_spin, 2, 1)
        
        layout.addLayout(properties_layout)
        
        # 创建按钮
        buttons_layout = QHBoxLayout()
        
        # 应用按钮
        self.apply_button = QPushButton("Appliquer")
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: #1B5E20; 
                color: white; 
                border-radius: 4px; 
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2E7D32;
            }
        """)
        buttons_layout.addWidget(self.apply_button)
        
        # 创建按钮
        self.create_button = QPushButton("Créer")
        self.create_button.setStyleSheet("""
            QPushButton {
                background-color: #1A237E; 
                color: white; 
                border-radius: 4px; 
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #303F9F;
            }
        """)
        buttons_layout.addWidget(self.create_button)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        # 设置尺寸策略
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedWidth(220)
    
    def get_properties(self):
        """获取当前设置的属性"""
        return {
            'side': self.side_length_spin.value(),
            'x': self.x_spin.value(),
            'y': self.y_spin.value()
        }
    
    def set_properties(self, properties):
        """设置面板属性值"""
        if 'side' in properties:
            self.side_length_spin.setValue(properties['side'])
        if 'x' in properties:
            self.x_spin.setValue(properties['x'])
        if 'y' in properties:
            self.y_spin.setValue(properties['y'])

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
        
        # 创建信息显示栏 - 改进GeoGebra风格
        self.info_panel = QLabel("坐标信息")
        self.info_panel.setFont(QFont("Arial", 10))
        self.info_panel.setStyleSheet("""
            QLabel {
                background-color: #F8F9FA;
                color: #212529;
                border: 1px solid #DEE2E6;
                border-radius: 3px;
                padding: 2px 8px;
            }
        """)
        self.info_panel.setMinimumHeight(24)
        self.info_panel.setMaximumHeight(60)  # 增加最大高度以容纳多行文本
        # 不设置固定宽度，而是让它自适应父容器宽度
        self.info_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.info_panel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.info_panel.setTextFormat(Qt.TextFormat.RichText)  # 启用富文本支持
        self.info_panel.setWordWrap(True)  # 启用自动换行
        canvas_layout.addWidget(self.info_panel)
        
        # 确保在窗口大小变化时信息面板宽度自适应但不改变窗口大小
        canvas_container.setMinimumWidth(600)  # 设置画布容器的最小宽度
        
        # 初始化画布
        self.canvas = Canvas()
        canvas_layout.addWidget(self.canvas)
        
        # 连接画布的点更新信号
        self.canvas.mousePressEvent = self.custom_mouse_press_event
        
        # 初始化按钮引用
        self.circle_button = None
        self.square_button = None
        self.triangle_button = None
        self.point_button = None
        self.line_button = None
        self.active_button = None
        
        # 创建工具栏
        self.create_geometry_tools(tools_frame)
        
        # 创建简化的正方形属性面板
        self.square_properties_panel = SimpleSquarePropertiesPanel()
        self.square_properties_panel.hide()  # 默认隐藏
        
        # 连接按钮信号
        self.square_properties_panel.apply_button.clicked.connect(self._apply_square_properties)
        self.square_properties_panel.create_button.clicked.connect(self._create_square_from_properties)
        
        # 添加到布局中
        tools_layout.addWidget(self.square_properties_panel)
    
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
        
        # 添加正方形属性按钮
        self.square_props_button = MetroButton("Propriétés", "#388E3C", "#FFFFFF")
        self.square_props_button.setMinimumSize(110, 40)
        self.square_props_button.setFont(QFont("Arial", 10))
        self.square_props_button.clicked.connect(self._toggle_square_properties)
        tools_frame.layout().addWidget(self.square_props_button, 3, 0, 1, 2)  # 修改为跨两列
        self.square_props_button.hide()  # 默认隐藏
        
        # 添加弹性空间
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        tools_frame.layout().addWidget(spacer, 4, 0, 1, 2)  # 修改为跨两列
        
        # 将清除和坐标轴按钮移到最下面
        # 添加清除按钮
        clear_button = MetroButton("Effacer", "#B71C1C", "#FFFFFF")
        clear_button.setMinimumSize(110, 110)
        clear_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        clear_button.clicked.connect(self.canvas.clear)
        tools_frame.layout().addWidget(clear_button, 5, 0)
        
        # 添加坐标轴切换按钮
        self.axes_button = MetroButton("Axes", "#607D8B", "#FFFFFF")
        self.axes_button.setMinimumSize(110, 110)
        self.axes_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.axes_button.clicked.connect(self.toggle_axes)
        self.axes_button.set_active(self.canvas.show_axes)  # 根据当前状态设置按钮状态
        tools_frame.layout().addWidget(self.axes_button, 5, 1)
    
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
            
        # 隐藏正方形属性按钮
        self.square_props_button.hide()
    
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
            # 显示正方形属性按钮
            self.square_props_button.show()
        elif shape == "circle":
            self.circle_button.set_active(True)
            # 隐藏正方形属性按钮
            self.square_props_button.hide()
        elif shape == "triangle":
            self.triangle_button.set_active(True)
            # 隐藏正方形属性按钮
            self.square_props_button.hide()
    
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
    
    def update_coordinate_info(self):
        """更新坐标信息显示栏"""
        if not self.canvas.points:
            self.info_panel.setText("坐标信息")
            return
            
        # 计算相对于坐标轴的坐标
        center_x = self.canvas.width() // 2
        center_y = self.canvas.height() // 2
        grid_spacing = self.canvas.grid_spacing
        
        # 构建点坐标信息 - 按线段分组显示
        points_info = ""
        
        # 如果有线段，则按线段分组显示点
        if self.canvas.lines:
            # 创建已显示点的集合，用于跟踪哪些点已经显示过
            displayed_points = set()
            
            # 首先显示构成线段的点
            for i, line in enumerate(self.canvas.lines):
                # 找到线段的两个端点
                start_point = None
                end_point = None
                start_index = None
                end_index = None
                
                # 查找与线段端点匹配的点
                for j, point in enumerate(self.canvas.points):
                    if abs(point['x'] - line['x1']) < 1 and abs(point['y'] - line['y1']) < 1:
                        start_point = point
                        start_index = j
                    elif abs(point['x'] - line['x2']) < 1 and abs(point['y'] - line['y2']) < 1:
                        end_point = point
                        end_index = j
                
                if start_point and end_point:
                    # 计算相对坐标
                    start_px = (start_point['x'] - center_x) / grid_spacing
                    start_py = (center_y - start_point['y']) / grid_spacing
                    end_px = (end_point['x'] - center_x) / grid_spacing
                    end_py = (center_y - end_point['y']) / grid_spacing
                    
                    # 获取点名称
                    start_name = 'ABCDEFGHIJKLMN'[start_index % 14]
                    end_name = 'ABCDEFGHIJKLMN'[end_index % 14]
                    
                    # 添加分隔符
                    if i > 0:
                        points_info += " | "
                    
                    # 使用与update_line_info相同的样式，将点两两分组显示
                    points_info += f"<span style='background-color:#E3F2FD; border:1px solid #BBDEFB; border-radius:3px; padding:1px 4px; margin-right:5px;'>"
                    points_info += f"<b style='color:#0277BD; font-size:11pt;'>{start_name}{end_name}</b>: "
                    points_info += f"({start_px:.1f}, {start_py:.1f}) → ({end_px:.1f}, {end_py:.1f})"
                    points_info += f"</span>"
                    
                    # 标记这些点已显示
                    displayed_points.add(start_index)
                    displayed_points.add(end_index)
            
            # 然后显示未构成线段的点
            for i, point in enumerate(self.canvas.points):
                if i not in displayed_points:
                    px = (point['x'] - center_x) / grid_spacing
                    py = (center_y - point['y']) / grid_spacing
                    point_name = 'ABCDEFGHIJKLMN'[i % 14]
                    
                    # 添加分隔符
                    if points_info:
                        points_info += " | "
                    
                    # 使用原来的样式显示单独的点
                    points_info += f"<b style='color:#E65100; font-size:11pt;'>{point_name}</b>({px:.1f}, {py:.1f})"
        else:
            # 如果没有线段，则按原来的方式显示所有点
            for i, point in enumerate(self.canvas.points):
                if i > 0:
                    points_info += " | "
                px = (point['x'] - center_x) / grid_spacing
                py = (center_y - point['y']) / grid_spacing
                point_name = 'ABCDEFGHIJKLMN'[i % 14]
                
                # 使用HTML格式化点名称，使其更加突出
                points_info += f"<b style='color:#E65100; font-size:11pt;'>{point_name}</b>({px:.1f}, {py:.1f})"
            
        # 更新信息显示栏
        self.info_panel.setText(points_info)
        
    def update_mouse_position_info(self, x, y):
        """更新鼠标位置坐标信息"""
        if self.canvas.draw_mode != "point":
            return
            
        # 计算相对于坐标轴的坐标
        center_x = self.canvas.width() // 2
        center_y = self.canvas.height() // 2
        grid_spacing = self.canvas.grid_spacing
        
        # 计算实际坐标值（相对于坐标系原点）
        real_x = (x - center_x) / grid_spacing
        real_y = (center_y - y) / grid_spacing  # 注意Y轴方向是相反的
        
        # 构建鼠标位置信息 - GeoGebra风格简洁显示，使用HTML格式化
        if not self.canvas.points:
            # 如果没有点，下一个点是A
            next_point_name = 'A'
            mouse_info = f"<b style='color:#3F51B5; font-size:11pt;'>{next_point_name}</b>: <span style='color:#2196F3;'>({real_x:.1f}, {real_y:.1f})</span>"
        else:
            # 构建点坐标信息
            points_info = ""
            for i, point in enumerate(self.canvas.points):
                if i > 0:
                    points_info += " | "
                px = (point['x'] - center_x) / grid_spacing
                py = (center_y - point['y']) / grid_spacing
                point_name = 'ABCDEFGHIJKLMN'[i % 14]
                
                # 使用HTML格式化点名称，使其更加突出
                points_info += f"<b style='color:#E65100; font-size:11pt;'>{point_name}</b>({px:.1f}, {py:.1f})"
            
            # 计算下一个点的名称
            next_point_index = len(self.canvas.points) % 14
            next_point_name = 'ABCDEFGHIJKLMN'[next_point_index]
            
            # 添加鼠标位置，使用不同颜色显示下一个点的名称和坐标
            mouse_info = f"{points_info} | <b style='color:#3F51B5; font-size:11pt;'>{next_point_name}</b>: <span style='color:#2196F3;'>({real_x:.1f}, {real_y:.1f})</span>"
        
        # 更新信息显示栏
        self.info_panel.setText(mouse_info)
        
    def update_line_info(self, x1, y1, x2, y2, length):
        """更新线段信息，显示端点坐标和长度"""
        if self.canvas.draw_mode != "line":
            return
            
        # 计算相对于坐标轴的坐标
        center_x = self.canvas.width() // 2
        center_y = self.canvas.height() // 2
        grid_spacing = self.canvas.grid_spacing
        
        # 计算实际坐标值（相对于坐标系原点）
        real_x1 = (x1 - center_x) / grid_spacing
        real_y1 = (center_y - y1) / grid_spacing  # 注意Y轴方向是相反的
        real_x2 = (x2 - center_x) / grid_spacing
        real_y2 = (center_y - y2) / grid_spacing
        
        # 计算实际长度（相对于坐标系单位）
        real_length = length / grid_spacing
        
        # 构建线段信息 - 显示端点坐标和长度
        # 确定端点的名称
        point_count = len(self.canvas.points)
        if self.canvas.line_start_point is not None:
            # 如果正在绘制线段，起点是最后一个点
            start_index = point_count - 1
            end_index = point_count
        else:
            # 如果没有正在绘制的线段，使用默认索引
            start_index = point_count
            end_index = point_count + 1
            
        start_name = 'ABCDEFGHIJKLMN'[start_index % 14]
        end_name = 'ABCDEFGHIJKLMN'[end_index % 14]
        
        # 构建线段信息，使用HTML格式化，将点两两分组显示
        # 使用不同的背景色和边框来区分不同的线段
        line_info = f"<span style='background-color:#E3F2FD; border:1px solid #BBDEFB; border-radius:3px; padding:1px 4px; margin-right:5px;'>"
        line_info += f"<b style='color:#0277BD; font-size:11pt;'>{start_name}{end_name}</b>: "
        line_info += f"({real_x1:.1f}, {real_y1:.1f}) → ({real_x2:.1f}, {real_y2:.1f})"
        line_info += f"</span> "
        line_info += f"<span style='color:#01579B; font-weight:bold;'>Length:</span> {real_length:.2f}"
        
        # 更新信息显示栏
        self.info_panel.setText(line_info)
        
    def update_square_info(self, start_x, start_y, size):
        """更新正方形信息，显示顶点坐标、边长、面积和周长"""
        if self.canvas.current_shape != "square":
            return
            
        # 计算相对于坐标轴的坐标
        center_x = self.canvas.width() // 2
        center_y = self.canvas.height() // 2
        grid_spacing = self.canvas.grid_spacing
        
        # 计算实际边长（相对于坐标系单位）
        real_size = size / grid_spacing if grid_spacing else size
        
        # 计算面积和周长
        area = real_size ** 2
        perimeter = 4 * real_size
        
        # 构建正方形信息，使用HTML格式化
        square_info = f"<span style='background-color:#E8EAF6; border:1px solid #C5CAE9; border-radius:3px; padding:1px 4px; margin-right:5px;'>"
        square_info += f"<b style='color:#1A237E; font-size:11pt;'>Carré</b></span> "
        square_info += f"<span style='color:#1A237E; font-weight:bold;'>Côté:</span> {real_size:.2f} | "
        square_info += f"<span style='color:#1A237E; font-weight:bold;'>Aire:</span> {area:.2f} | "
        square_info += f"<span style='color:#1A237E; font-weight:bold;'>Périmètre:</span> {perimeter:.2f}"
        
        # 更新信息显示栏
        self.info_panel.setText(square_info)
    
    def update_square_info_complete(self, side_length, area):
        """正方形绘制完成后，显示正方形的特性"""
        square_info = f"<span style='background-color:#E8EAF6; border:1px solid #C5CAE9; border-radius:3px; padding:1px 4px; margin-right:5px;'>"
        square_info += f"<b style='color:#1A237E; font-size:11pt;'>Carré</b></span> "
        square_info += f"<span style='color:#1A237E; font-weight:bold;'>Côté:</span> {side_length:.2f} | "
        square_info += f"<span style='color:#1A237E; font-weight:bold;'>Aire:</span> {area:.2f} | "
        square_info += f"<span style='color:#1A237E; font-weight:bold;'>Périmètre:</span> {side_length * 4:.2f}"
        
        # 更新信息显示栏
        self.info_panel.setText(square_info)
    
    def custom_mouse_press_event(self, event):
        """自定义鼠标点击事件处理函数，用于捕获点的坐标并更新信息显示栏"""
        # 调用原始的鼠标点击事件处理函数
        Canvas.mousePressEvent(self.canvas, event)
        
        # 更新坐标信息
        if event.button() == Qt.MouseButton.LeftButton and self.canvas.draw_mode == "point":
            self.update_coordinate_info()
    
    def _apply_square_properties(self):
        """应用属性面板中的设置到选中的正方形"""
        properties = self.square_properties_panel.get_properties()
        # 如果有选中的正方形，更新它的属性
        # 此处可以添加选中图形的逻辑
        
        # 更新信息面板
        self.update_square_info_complete(properties['side'], properties['side']**2)

    def _create_square_from_properties(self):
        """根据属性面板中的设置创建新的正方形"""
        properties = self.square_properties_panel.get_properties()
        
        # 计算坐标系中的实际位置
        center_x = self.canvas.width() // 2
        center_y = self.canvas.height() // 2
        grid_spacing = self.canvas.grid_spacing or 1
        
        x = center_x + properties['x'] * grid_spacing
        y = center_y - properties['y'] * grid_spacing  # 反转Y轴，符合数学坐标系
        
        # 计算正方形顶点
        side_px = properties['side'] * grid_spacing
        half_side = side_px / 2
        
        x1, y1 = x - half_side, y - half_side  # 左上
        x2, y2 = x + half_side, y - half_side  # 右上
        x3, y3 = x + half_side, y + half_side  # 右下
        x4, y4 = x - half_side, y + half_side  # 左下
        
        # 添加四个顶点
        color = "#1A237E"  # 使用默认蓝色
        self.canvas.points.append({'x': x1, 'y': y1, 'color': color})
        self.canvas.points.append({'x': x2, 'y': y2, 'color': color})
        self.canvas.points.append({'x': x3, 'y': y3, 'color': color})
        self.canvas.points.append({'x': x4, 'y': y4, 'color': color})
        
        # 添加四条边
        for i in range(4):
            self.canvas.line_texts.append(f"{properties['side']:.1f}")
        
        self.canvas.lines.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': color})
        self.canvas.lines.append({'x1': x2, 'y1': y2, 'x2': x3, 'y2': y3, 'color': color})
        self.canvas.lines.append({'x1': x3, 'y1': y3, 'x2': x4, 'y2': y4, 'color': color})
        self.canvas.lines.append({'x1': x4, 'y1': y4, 'x2': x1, 'y2': y1, 'color': color})
        
        # 更新画布
        self.canvas.update()
        
        # 更新信息面板
        self.update_square_info_complete(properties['side'], properties['side']**2)
    
    def _toggle_square_properties(self):
        """切换正方形属性面板的显示状态"""
        if self.square_properties_panel.isVisible():
            self.square_properties_panel.hide()
        else:
            # 显示属性面板
            self.square_properties_panel.show()
            # 激活正方形绘制模式
            self.select_shape("square")
