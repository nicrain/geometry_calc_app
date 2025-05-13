"""
矩形形状处理器的实现。
"""
from typing import Dict, Any, Optional, Tuple
import math

from modules.canvas import Canvas
from modules.shape_handlers import ShapeHandler
from modules.shapes import ShapeType

class RectangleHandler(ShapeHandler):
    """处理矩形的创建和交互"""
    
    def __init__(self, canvas: Canvas):
        super().__init__(canvas)
        self._shape_type = ShapeType.RECTANGLE
        self.color = "#1A237E"  # 深蓝色
        self.start_point = None
    
    @property
    def shape_type(self):
        return self._shape_type
    
    def _reset_canvas_state(self):
        """重置画布状态"""
        self.canvas.current_shape = "rectangle"
        self.canvas.draw_mode = None
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        self.start_point = None
    
    def _connect_canvas_events(self):
        """连接画布事件"""
        # 在实际应用中，我们应该保存连接的引用以便稍后断开连接
        pass
    
    def _disconnect_canvas_events(self):
        """断开画布事件连接"""
        pass
    
    def preview_from_properties(self, properties: Dict[str, Any]):
        """根据属性预览矩形"""
        if not self.is_active:
            return
            
        # 获取属性值
        x = properties.get('x', 0)
        y = properties.get('y', 0)
        width = properties.get('length', 2)
        height = properties.get('width', 1)
        
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 计算矩形的另一个角点
        screen_w = width * self.canvas.grid_spacing
        screen_h = height * self.canvas.grid_spacing
        
        # 设置临时状态用于预览显示
        self.canvas.current_shape = "rectangle_preview"
        self.canvas.line_start_point = (screen_x, screen_y)
        self.canvas.temp_shape = (screen_x + screen_w, screen_y + screen_h)
        
        # 更新画布
        self.canvas.update()
    
    def _on_create_from_properties(self, properties: Dict[str, Any]):
        """从属性创建矩形"""
        if not self.is_active:
            return
        
        # 获取属性值
        x = properties.get('x', 0)
        y = properties.get('y', 0)
        width = properties.get('length', 2)
        height = properties.get('width', 1)
        
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 计算矩形的四个顶点
        screen_w = width * self.canvas.grid_spacing
        screen_h = height * self.canvas.grid_spacing
        
        x1, y1 = screen_x, screen_y  # 左上角
        x2, y2 = screen_x + screen_w, screen_y  # 右上角
        x3, y3 = screen_x + screen_w, screen_y + screen_h  # 右下角
        x4, y4 = screen_x, screen_y + screen_h  # 左下角
        
        # 添加四个顶点
        self.canvas.points.append({'x': x1, 'y': y1, 'color': self.color})
        self.canvas.points.append({'x': x2, 'y': y2, 'color': self.color})
        self.canvas.points.append({'x': x3, 'y': y3, 'color': self.color})
        self.canvas.points.append({'x': x4, 'y': y4, 'color': self.color})
        
        # 添加四条边
        self.canvas.lines.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': self.color})
        self.canvas.lines.append({'x1': x2, 'y1': y2, 'x2': x3, 'y2': y3, 'color': self.color})
        self.canvas.lines.append({'x1': x3, 'y1': y3, 'x2': x4, 'y2': y4, 'color': self.color})
        self.canvas.lines.append({'x1': x4, 'y1': y4, 'x2': x1, 'y2': y1, 'color': self.color})
        
        # 添加边长文本
        self.canvas.line_texts.append(f"{width:.1f}")
        self.canvas.line_texts.append(f"{height:.1f}")
        self.canvas.line_texts.append(f"{width:.1f}")
        self.canvas.line_texts.append(f"{height:.1f}")
        
        # 计算面积和周长
        area = width * height
        perimeter = 2 * (width + height)
        
        # 添加形状信息
        self.canvas.shapes.append({
            'type': 'rectangle',
            'vertices': [(x1, y1), (x2, y2), (x3, y3), (x4, y4)],
            'width': screen_w,
            'height': screen_h,
            'area': area * (self.canvas.grid_spacing ** 2),
            'perimeter': perimeter * self.canvas.grid_spacing,
            'color': self.color
        })
        
        # 清除临时状态
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        
        # 更新画布
        self.canvas.update()
        
        # 发送矩形创建信号
        rectangle_data = {
            'type': 'rectangle',
            'x': x,
            'y': y,
            'length': width,
            'width': height,
            'area': area,
            'perimeter': perimeter,
            'color': self.color
        }
        self.canvas.shape_created.emit(rectangle_data)
    
    def handle_mouse_press(self, x: float, y: float):
        """处理鼠标按下事件"""
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        if not self.start_point:
            # 设置矩形起点
            self.start_point = (screen_x, screen_y)
            self.canvas.line_start_point = self.start_point
            
            # 添加起点作为一个点
            self.canvas.points.append({
                'x': screen_x,
                'y': screen_y,
                'color': self.color
            })
            self.canvas.update()
        else:
            # 完成矩形绘制
            # 这部分逻辑在handle_mouse_release中处理
            pass
    
    def handle_mouse_move(self, x: float, y: float):
        """处理鼠标移动事件"""
        if not self.start_point:
            return
            
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 设置临时形状
        self.canvas.temp_shape = (screen_x, screen_y)
        self.canvas.update()
    
    def handle_mouse_release(self, x: float, y: float):
        """处理鼠标释放事件"""
        if not self.start_point:
            return
            
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 获取起点
        x1, y1 = self.start_point
        
        # 计算宽度和高度
        width = abs(screen_x - x1)
        height = abs(screen_y - y1)
        
        # 根据鼠标位置确定矩形的方向
        dx = 1 if screen_x >= x1 else -1
        dy = 1 if screen_y >= y1 else -1
        
        # 计算矩形的四个顶点
        x2, y2 = x1 + width * dx, y1
        x3, y3 = x1 + width * dx, y1 + height * dy
        x4, y4 = x1, y1 + height * dy
        
        # 添加其他三个顶点
        self.canvas.points.append({'x': x2, 'y': y2, 'color': self.color})
        self.canvas.points.append({'x': x3, 'y': y3, 'color': self.color})
        self.canvas.points.append({'x': x4, 'y': y4, 'color': self.color})
        
        # 添加四条边
        self.canvas.lines.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': self.color})
        self.canvas.lines.append({'x1': x2, 'y1': y2, 'x2': x3, 'y2': y3, 'color': self.color})
        self.canvas.lines.append({'x1': x3, 'y1': y3, 'x2': x4, 'y2': y4, 'color': self.color})
        self.canvas.lines.append({'x1': x4, 'y1': y4, 'x2': x1, 'y2': y1, 'color': self.color})
        
        # 计算实际长度和宽度（相对于坐标系）
        grid_spacing = self.canvas.grid_spacing
        real_width = width / grid_spacing
        real_height = height / grid_spacing
        
        # 添加边长文本
        self.canvas.line_texts.append(f"{real_width:.1f}")
        self.canvas.line_texts.append(f"{real_height:.1f}")
        self.canvas.line_texts.append(f"{real_width:.1f}")
        self.canvas.line_texts.append(f"{real_height:.1f}")
        
        # 计算面积和周长
        area = width * height / (grid_spacing ** 2)
        perimeter = 2 * (width + height) / grid_spacing
        
        # 添加形状信息
        self.canvas.shapes.append({
            'type': 'rectangle',
            'vertices': [(x1, y1), (x2, y2), (x3, y3), (x4, y4)],
            'width': width,
            'height': height,
            'area': area,
            'perimeter': perimeter,
            'color': self.color
        })
        
        # 清除临时状态
        self.start_point = None
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        
        # 更新画布
        self.canvas.update()
        
        # 发送矩形创建信号
        grid_x1, grid_y1 = self.canvas.screen_to_grid(x1, y1)
        rectangle_data = {
            'type': 'rectangle',
            'x': grid_x1,
            'y': grid_y1,
            'length': real_width,
            'width': real_height,
            'area': area,
            'perimeter': perimeter,
            'color': self.color
        }
        self.canvas.shape_created.emit(rectangle_data)
