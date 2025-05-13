"""
圆形形状处理器的实现。
"""
from typing import Dict, Any, Optional, Tuple
import math

from modules.canvas import Canvas
from modules.shape_handlers import ShapeHandler
from modules.shapes import ShapeType

class CircleHandler(ShapeHandler):
    """处理圆形的创建和交互"""
    
    def __init__(self, canvas: Canvas):
        super().__init__(canvas)
        self._shape_type = ShapeType.CIRCLE
        self.color = "#1B5E20"  # 深绿色
        self.center_point = None
    
    @property
    def shape_type(self):
        return self._shape_type
    
    def _reset_canvas_state(self):
        """重置画布状态"""
        self.canvas.current_shape = "circle"
        self.canvas.draw_mode = None
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        self.center_point = None
    
    def _connect_canvas_events(self):
        """连接画布事件"""
        # 在实际应用中，我们应该保存连接的引用以便稍后断开连接
        pass
    
    def _disconnect_canvas_events(self):
        """断开画布事件连接"""
        pass
    
    def preview_from_properties(self, properties: Dict[str, Any]):
        """根据属性预览圆形"""
        if not self.is_active:
            return
            
        # 获取属性值
        x = properties.get('x', 0)
        y = properties.get('y', 0)
        radius = properties.get('radius', 1)
        
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 计算屏幕上的半径长度
        screen_radius = radius * self.canvas.grid_spacing
        
        # 设置临时状态用于预览显示
        self.canvas.current_shape = "circle_preview"
        self.canvas.line_start_point = (screen_x, screen_y)
        # 计算圆上的一个点作为临时形状
        self.canvas.temp_shape = (screen_x + screen_radius, screen_y)
        
        # 更新画布
        self.canvas.update()
    
    def _on_create_from_properties(self, properties: Dict[str, Any]):
        """从属性创建圆形"""
        if not self.is_active:
            return
        
        # 获取属性值
        x = properties.get('x', 0)
        y = properties.get('y', 0)
        radius = properties.get('radius', 1)
        
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 计算屏幕上的半径长度
        screen_radius = radius * self.canvas.grid_spacing
        
        # 添加圆心作为一个点
        self.canvas.points.append({
            'x': screen_x,
            'y': screen_y,
            'color': self.color
        })
        
        # 计算圆的周长和面积
        circumference = 2 * math.pi * screen_radius
        area = math.pi * (screen_radius ** 2)
        
        # 存储到形状属性中
        self.canvas.shapes.append({
            'type': 'circle',
            'center': (screen_x, screen_y),
            'radius': screen_radius,
            'circumference': circumference,
            'area': area,
            'color': self.color
        })
        
        # 清除临时状态
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        
        # 更新画布
        self.canvas.update()
        
        # 发送圆形创建信号
        circle_data = {
            'type': 'circle',
            'x': x,
            'y': y,
            'radius': radius,
            'circumference': 2 * math.pi * radius,
            'area': math.pi * (radius ** 2),
            'color': self.color
        }
        self.canvas.shape_created.emit(circle_data)
    
    def handle_mouse_press(self, x: float, y: float):
        """处理鼠标按下事件"""
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        if not self.center_point:
            # 设置圆心
            self.center_point = (screen_x, screen_y)
            self.canvas.line_start_point = self.center_point
            
            # 添加圆心作为一个点
            self.canvas.points.append({
                'x': screen_x,
                'y': screen_y,
                'color': self.color
            })
            self.canvas.update()
        else:
            # 完成圆形绘制
            # 这部分逻辑在handle_mouse_release中处理
            pass
    
    def handle_mouse_move(self, x: float, y: float):
        """处理鼠标移动事件"""
        if not self.center_point:
            return
            
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 设置临时形状
        self.canvas.temp_shape = (screen_x, screen_y)
        self.canvas.update()
    
    def handle_mouse_release(self, x: float, y: float):
        """处理鼠标释放事件"""
        if not self.center_point:
            return
            
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 获取圆心
        center_x, center_y = self.center_point
        
        # 计算半径
        radius = math.sqrt((screen_x - center_x) ** 2 + (screen_y - center_y) ** 2)
        
        # 计算实际半径（相对于坐标系）
        grid_spacing = self.canvas.grid_spacing
        real_radius = radius / grid_spacing
        
        # 计算圆的周长和面积
        circumference = 2 * math.pi * radius
        area = math.pi * (radius ** 2)
        
        # 存储到形状属性中
        self.canvas.shapes.append({
            'type': 'circle',
            'center': (center_x, center_y),
            'radius': radius,
            'circumference': circumference,
            'area': area,
            'color': self.color
        })
        
        # 清除临时状态
        self.center_point = None
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        
        # 更新画布
        self.canvas.update()
        
        # 发送圆形创建信号
        grid_x, grid_y = self.canvas.screen_to_grid(center_x, center_y)
        circle_data = {
            'type': 'circle',
            'x': grid_x,
            'y': grid_y,
            'radius': real_radius,
            'circumference': 2 * math.pi * real_radius,
            'area': math.pi * (real_radius ** 2),
            'color': self.color
        }
        self.canvas.shape_created.emit(circle_data)
