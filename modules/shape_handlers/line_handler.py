"""
线段形状处理器的实现。
"""
from typing import Dict, Any, Optional, Tuple
import math

from modules.canvas import Canvas
from modules.shape_handlers import ShapeHandler
from modules.shapes import ShapeType

class LineHandler(ShapeHandler):
    """处理线段的创建和交互"""
    
    def __init__(self, canvas: Canvas):
        super().__init__(canvas)
        self._shape_type = ShapeType.LINE
        self.color = "#0277BD"  # 蓝色
        self.start_point = None
    
    @property
    def shape_type(self):
        return self._shape_type
    
    def _reset_canvas_state(self):
        """重置画布状态"""
        self.canvas.draw_mode = "line"
        self.canvas.current_shape = None
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        self.start_point = None
    
    def _connect_canvas_events(self):
        """连接画布事件"""
        # 在实际应用中，我们应该保存连接的引用以便稍后断开连接
        pass
    
    def _disconnect_canvas_events(self):
        """断开画布事件连接"""
        # 与_connect_canvas_events类似，这里简化处理
        pass
    
    def activate(self):
        """激活线段处理器"""
        super().activate()
        # 设置Canvas的绘制模式为线段
        self.canvas.draw_mode = "line"
        self.canvas.current_shape = None
    
    def _on_properties_changed(self, properties):
        """属性面板值改变时的响应方法"""
        if not self.is_active:
            return
        
        # 计算坐标系中的实际位置
        center_x = self.canvas.width() // 2
        center_y = self.canvas.height() // 2
        grid_spacing = self.canvas.grid_spacing or 1
        
        # 计算线段的起点和终点
        x1 = center_x + properties['x1'] * grid_spacing
        y1 = center_y - properties['y1'] * grid_spacing  # 反转Y轴，符合数学坐标系
        x2 = center_x + properties['x2'] * grid_spacing
        y2 = center_y - properties['y2'] * grid_spacing  # 反转Y轴，符合数学坐标系
        
        # 设置临时状态用于预览显示
        self.canvas.line_start_point = (x1, y1)
        self.canvas.temp_shape = (x2, y2)
        
        # 添加临时端点的预览
        if not hasattr(self.canvas, 'temp_endpoints'):
            self.canvas.temp_endpoints = []
        
        # 清空之前的临时端点
        self.canvas.temp_endpoints = []
        
        # 添加两个端点作为临时点
        self.canvas.temp_endpoints.append({
            'x': x1, 
            'y': y1, 
            'color': "#0277BD", 
            'name': 'A'
        })
        self.canvas.temp_endpoints.append({
            'x': x2, 
            'y': y2, 
            'color': "#0277BD", 
            'name': 'B'
        })
        
        # 更新画布
        self.canvas.update()
    
    def _on_create_from_properties(self, properties):
        """从属性面板创建线段"""
        if not self.is_active:
            return
        
        # 计算坐标系中的实际位置
        center_x = self.canvas.width() // 2
        center_y = self.canvas.height() // 2
        grid_spacing = self.canvas.grid_spacing or 1
        
        # 计算线段的起点和终点
        x1 = center_x + properties['x1'] * grid_spacing
        y1 = center_y - properties['y1'] * grid_spacing  # 反转Y轴，符合数学坐标系
        x2 = center_x + properties['x2'] * grid_spacing
        y2 = center_y - properties['y2'] * grid_spacing  # 反转Y轴，符合数学坐标系
        
        # 添加起点和终点
        self.canvas.points.append({'x': x1, 'y': y1, 'color': "#0277BD"})
        self.canvas.points.append({'x': x2, 'y': y2, 'color': "#0277BD"})
        
        # 计算线段长度
        length = ((x2 - x1) ** 2 + (y1 - y2) ** 2) ** 0.5  # 注意y轴方向是相反的
        real_length = length / grid_spacing
        length_text = f"{real_length:.1f}"
        
        # 添加线段
        self.canvas.lines.append({
            'x1': x1, 'y1': y1,
            'x2': x2, 'y2': y2,
            'color': "#0277BD"
        })
        
        # 添加长度文本
        self.canvas.line_texts.append(length_text)
        
        # 清除临时端点
        if hasattr(self.canvas, 'temp_endpoints'):
            self.canvas.temp_endpoints = []
        
        # 更新画布
        self.canvas.update()
        
        # 计算角度（弧度）
        angle_rad = math.atan2(y1 - y2, x2 - x1)  # 注意y轴向下为正，需要反转
        # 转换为度数 (0-360°)
        angle_deg = (angle_rad * 180 / math.pi) % 360
        
        # 发射形状创建信号
        shape_data = {
            'type': 'line',
            'x1': properties['x1'],
            'y1': properties['y1'],
            'x2': properties['x2'],
            'y2': properties['y2'],
            'length': real_length,
            'angle': angle_deg
        }
        
        # 如果Canvas有canvas_data_changed信号，则发射
        if hasattr(self.canvas, 'shape_created'):
            self.canvas.shape_created.emit(shape_data)
    
    def deactivate(self):
        """停用线段处理器"""
        super().deactivate()
        # 清除Canvas相关状态
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        if hasattr(self.canvas, 'temp_endpoints'):
            self.canvas.temp_endpoints = []
