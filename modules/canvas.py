"""
画布组件，用于绘制几何图形
"""
import math
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QRect, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont

class Canvas(QWidget):
    """自定义画布组件，用于绘制几何图形"""
    
    # 信号定义
    mouse_position_changed = pyqtSignal(float, float)  # 传递网格坐标
    point_created = pyqtSignal(dict)  # 传递点数据
    line_created = pyqtSignal(dict)  # 传递线段数据
    shape_created = pyqtSignal(dict)  # 传递形状数据
    canvas_cleared = pyqtSignal()  # 画布清除信号
    
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
        self.shapes = []  # 存储其他形状
        
        # 临时绘制状态
        self.temp_shape = None
        self.temp_point = None
        self.temp_endpoints = []  # 临时端点集合
        self.line_start_point = None
        self.triangle_points = []
        
        # 当前选中的项
        self.selected_item = None
        
        # 坐标轴设置
        self.show_axes = True
        self.grid_spacing = 50  # 每单位网格线间的像素距离
        self.axis_color = "#555555"
        
        # 启用鼠标跟踪
        self.setMouseTracking(True)
    
    def clear(self):
        """清除画布上的所有内容"""
        self.points = []
        self.lines = []
        self.line_texts = []
        self.shapes = []
        self.temp_shape = None
        self.temp_point = None
        self.temp_endpoints = []
        self.line_start_point = None
        self.triangle_points = []
        self.selected_item = None
        self.update()
        self.canvas_cleared.emit()
    
    def grid_to_screen(self, grid_x, grid_y):
        """将网格坐标转换为屏幕坐标"""
        center_x = self.width() // 2
        center_y = self.height() // 2
        screen_x = center_x + grid_x * self.grid_spacing
        screen_y = center_y - grid_y * self.grid_spacing  # Y轴方向相反
        return screen_x, screen_y
    
    def screen_to_grid(self, screen_x, screen_y):
        """将屏幕坐标转换为网格坐标"""
        center_x = self.width() // 2
        center_y = self.height() // 2
        grid_x = (screen_x - center_x) / self.grid_spacing
        grid_y = (center_y - screen_y) / self.grid_spacing  # Y轴方向相反
        return grid_x, grid_y
    
    def paintEvent(self, event):
        """绘制事件处理"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制白色背景
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        
        # 绘制坐标轴
        if self.show_axes:
            self._draw_coordinate_axes(painter)
        
        # 绘制已保存的点
        self._draw_points(painter)
        
        # 绘制已保存的线段
        self._draw_lines(painter)
        
        # 绘制保存的形状
        self._draw_shapes(painter)
        
        # 绘制临时形状
        self._draw_temp_shapes(painter)
        
        # 绘制临时点
        if self.temp_point:
            self._draw_temp_point(painter)
        
        # 绘制临时端点集合
        if self.temp_endpoints:
            self._draw_temp_endpoints(painter)
    
    def _draw_coordinate_axes(self, painter):
        """绘制坐标轴"""
        # 获取画布中心点
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        # 设置坐标轴样式
        painter.setPen(QPen(QColor(self.axis_color), 1))
        
        # 绘制X轴和Y轴
        painter.drawLine(0, center_y, self.width(), center_y)  # X轴
        painter.drawLine(center_x, 0, center_x, self.height())  # Y轴
        
        # 绘制刻度和标签
        painter.setFont(QFont("Arial", 8))
        
        # 绘制X轴刻度
        for i in range(-10, 11):
            if i == 0:  # 跳过原点
                continue
            
            x = center_x + i * self.grid_spacing
            if 0 <= x <= self.width():
                painter.drawLine(x, center_y - 5, x, center_y + 5)
                painter.drawText(QRect(x - 10, center_y + 10, 20, 15), 
                                Qt.AlignmentFlag.AlignCenter, str(i))
        
        # 绘制Y轴刻度
        for i in range(-10, 11):
            if i == 0:  # 跳过原点
                continue
            
            y = center_y + i * self.grid_spacing
            if 0 <= y <= self.height():
                painter.drawLine(center_x - 5, y, center_x + 5, y)
                painter.drawText(QRect(center_x + 10, y - 10, 20, 20), 
                                Qt.AlignmentFlag.AlignCenter, str(-i))
        
        # 在原点绘制O标记
        painter.drawText(QRect(center_x + 10, center_y + 10, 15, 15), 
                        Qt.AlignmentFlag.AlignCenter, "O")
    
    def _draw_points(self, painter):
        """绘制已保存的点"""
        for i, point in enumerate(self.points):
            # 设置点的颜色
            painter.setPen(QPen(QColor(point['color']), 2))
            painter.setBrush(QBrush(QColor(point['color'])))
            x = int(point['x'])
            y = int(point['y'])
            
            # 绘制点
            painter.drawEllipse(x - 5, y - 5, 10, 10)
            
            # 绘制点的名称标签
            point_name = 'ABCDEFGHIJKLMN'[i % 14]
            
            painter.setPen(QPen(QColor("#000000")))
            font = QFont("Arial", 10)
            font.setBold(True)
            painter.setFont(font)
            
            painter.drawText(x - 5, y - 10, point_name)
    
    def _draw_lines(self, painter):
        """绘制已保存的线段"""
        for i, line in enumerate(self.lines):
            if self.selected_item == ('line', i):
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
    
    def _draw_shapes(self, painter):
        """绘制保存的形状"""
        for shape in self.shapes:
            if shape['type'] == 'circle':
                # 绘制圆形
                painter.setPen(QPen(QColor(shape['color']), 2))
                painter.setBrush(Qt.BrushStyle.NoBrush)  # 不填充
                
                center_x, center_y = shape['center']
                radius = shape['radius']
                painter.drawEllipse(int(center_x - radius), int(center_y - radius), 
                                   int(radius * 2), int(radius * 2))
    
    def _draw_temp_shapes(self, painter):
        """绘制临时形状"""
        # 根据不同的临时形状类型进行绘制
        if not self.temp_shape:
            return
        
        # 实现临时形状绘制逻辑
        # ...
    
    def _draw_temp_point(self, painter):
        """绘制临时点"""
        painter.setPen(QPen(QColor("#E65100"), 2))
        painter.setBrush(QBrush(QColor("#E65100")))
        x, y = self.temp_point
        painter.drawEllipse(int(x) - 5, int(y) - 5, 10, 10)
        
        point_name = 'ABCDEFGHIJKLMN'[len(self.points) % 14]
        painter.setPen(QPen(QColor("#000000")))
        font = QFont("Arial", 10)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(int(x) - 5, int(y) - 10, point_name)
    
    def _draw_temp_endpoints(self, painter):
        """绘制临时端点集合"""
        for i, point in enumerate(self.temp_endpoints):
            # 设置点的颜色
            painter.setPen(QPen(QColor(point['color']), 2))
            painter.setBrush(QBrush(QColor(point['color'])))
            x = int(point['x'])
            y = int(point['y'])
            
            # 绘制点
            painter.drawEllipse(x - 5, y - 5, 10, 10)
            
            # 绘制点的名称标签
            point_name = point.get('name', 'ABCDEFGHIJKLMN'[i % 14])
            
            painter.setPen(QPen(QColor("#000000")))
            font = QFont("Arial", 10)
            font.setBold(True)
            painter.setFont(font)
            
            painter.drawText(x - 5, y - 10, point_name)
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件处理"""
        x, y = event.position().x(), event.position().y()
        grid_x, grid_y = self.screen_to_grid(x, y)
        
        # 发送鼠标位置变化信号
        self.mouse_position_changed.emit(grid_x, grid_y)
        
        # 调用父类方法
        super().mouseMoveEvent(event)
    
    def mousePressEvent(self, event):
        """鼠标按下事件，用于处理形状创建的起始点"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_x = event.position().x()
            self.start_y = event.position().y()
            
            # 更具体的处理逻辑将移到形状处理器中
            # 这里仅保留基本框架
            if self.draw_mode == "point":
                # 添加一个点
                new_point = {
                    'x': self.start_x,
                    'y': self.start_y,
                    'color': "#E65100"  # 橙色
                }
                self.points.append(new_point)
                self.update()
                # 发送点创建信号
                grid_x, grid_y = self.screen_to_grid(self.start_x, self.start_y)
                point_data = {'x': grid_x, 'y': grid_y, 'color': "#E65100"}
                self.point_created.emit(point_data)
        
        # 调用父类的mousePressEvent
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件，用于完成形状的创建"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 具体逻辑将移到形状处理器中
            # 这里仅保留基本框架
            pass
        
        # 调用父类的mouseReleaseEvent
        super().mouseReleaseEvent(event)