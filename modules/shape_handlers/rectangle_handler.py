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
        # 矩形处理器的事件连接逻辑
        pass
    
    def _disconnect_canvas_events(self):
        """断开画布事件连接"""
        # 矩形处理器的事件断开逻辑
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
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        if not self.start_point:
            self.start_point = (screen_x, screen_y)
            self.canvas.line_start_point = self.start_point
            self.canvas.current_shape = "rectangle"
            self.canvas.temp_shape = None
            # 只在起点添加一个点，用于预览
            self.canvas.points.append({'x': screen_x, 'y': screen_y, 'color': self.color})
            self.canvas.update()
        else:
            # 完成矩形绘制
            self.handle_mouse_release(x, y)

    def handle_mouse_move(self, x: float, y: float):
        """处理鼠标移动事件"""
        if not self.start_point:
            # 未点击第一点时，显示当前位置作为起点
            if hasattr(self.canvas, 'shape_preview'):
                preview_data = {
                    'type': 'rectangle_preview_start',
                    'x': x, 'y': y
                }
                self.canvas.shape_preview.emit(preview_data)
            return
            
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 设置临时形状
        self.canvas.temp_shape = (screen_x, screen_y)
        
        # 发送实时矩形信息
        if hasattr(self.canvas, 'shape_preview'):
            x1, y1 = self.start_point
            grid_x1, grid_y1 = self.canvas.screen_to_grid(x1, y1)
            
            # 计算宽度和高度
            width = abs(x - grid_x1)
            height = abs(y - grid_y1)
            area = width * height
            
            preview_data = {
                'type': 'rectangle_preview',
                'x1': grid_x1, 'y1': grid_y1,
                'x2': x, 'y2': y,
                'width': width,
                'height': height,
                'area': area
            }
            self.canvas.shape_preview.emit(preview_data)
        
        self.canvas.update()

    def handle_mouse_release(self, x: float, y: float):
        """处理鼠标释放事件"""
        if not self.start_point:
            return
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        x1, y1 = self.start_point
        
        # 确保矩形有最小尺寸
        if abs(screen_x - x1) < 10 or abs(screen_y - y1) < 10:
            return
        
        # 计算四个顶点（确保顺序正确）
        min_x, max_x = min(x1, screen_x), max(x1, screen_x)
        min_y, max_y = min(y1, screen_y), max(y1, screen_y)
        
        vertices = [
            (min_x, min_y),  # 左上
            (max_x, min_y),  # 右上
            (max_x, max_y),  # 右下
            (min_x, max_y)   # 左下
        ]
        
        # 移除原来的起点，添加四个顶点
        if self.canvas.points and self.canvas.points[-1]['x'] == x1 and self.canvas.points[-1]['y'] == y1:
            self.canvas.points.pop()
        
        for vx, vy in vertices:
            self.canvas.points.append({'x': vx, 'y': vy, 'color': self.color})
        
        # 添加四条边
        for i in range(4):
            x1_line, y1_line = vertices[i]
            x2_line, y2_line = vertices[(i + 1) % 4]
            self.canvas.lines.append({
                'x1': x1_line, 'y1': y1_line, 
                'x2': x2_line, 'y2': y2_line, 
                'color': self.color
            })
        
        # 计算长宽
        grid_spacing = self.canvas.grid_spacing
        real_width = (max_x - min_x) / grid_spacing
        real_height = (max_y - min_y) / grid_spacing
        
        # 添加边长文本
        self.canvas.line_texts.extend([
            f"{real_width:.1f}",   # 上边
            f"{real_height:.1f}",  # 右边
            f"{real_width:.1f}",   # 下边
            f"{real_height:.1f}"   # 左边
        ])
        
        # 计算面积和周长
        area = real_width * real_height
        perimeter = 2 * (real_width + real_height)
        
        self.canvas.shapes.append({
            'type': 'rectangle',
            'vertices': vertices,
            'width': max_x - min_x,
            'height': max_y - min_y,
            'area': area,
            'perimeter': perimeter,
            'color': self.color
        })
        
        # 发射信号
        grid_x1, grid_y1 = self.canvas.screen_to_grid(min_x, min_y)
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
        
        # 清除状态
        self.start_point = None
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        self.canvas.update()
    
    def deactivate(self):
        """停用矩形处理器"""
        super().deactivate()
        # 清除Canvas相关状态
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        self.canvas.current_shape = None
        self.start_point = None
    
    def activate(self):
        """激活矩形处理器"""
        super().activate()
        self.canvas.draw_mode = "rectangle"
        self.canvas.current_shape = "rectangle"
        # 确保清除之前的临时状态
        self.start_point = None
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
