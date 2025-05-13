"""
三角形形状处理器的实现。
"""
from typing import Dict, Any, Optional, Tuple, List
import math

from modules.canvas import Canvas
from modules.shape_handlers import ShapeHandler
from modules.shapes import ShapeType

class TriangleHandler(ShapeHandler):
    """处理三角形的创建和交互"""
    
    def __init__(self, canvas: Canvas):
        super().__init__(canvas)
        self._shape_type = ShapeType.TRIANGLE
        self.color = "#311B92"  # 深紫色
        self.vertices = []
    
    @property
    def shape_type(self):
        return self._shape_type
    
    def _reset_canvas_state(self):
        """重置画布状态"""
        self.canvas.current_shape = "triangle"
        self.canvas.draw_mode = None
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        self.canvas.triangle_points = []
        self.vertices = []
    
    def _connect_canvas_events(self):
        """连接画布事件"""
        # 在实际应用中，我们应该保存连接的引用以便稍后断开连接
        pass
    
    def _disconnect_canvas_events(self):
        """断开画布事件连接"""
        pass
    
    def preview_from_properties(self, properties: Dict[str, Any]):
        """根据属性预览三角形"""
        if not self.is_active:
            return
            
        # 获取属性值
        x1 = properties.get('x1', 0)
        y1 = properties.get('y1', 0)
        x2 = properties.get('x2', 0)
        y2 = properties.get('y2', 0)
        x3 = properties.get('x3', 0)
        y3 = properties.get('y3', 0)
        
        # 转换为屏幕坐标
        screen_x1, screen_y1 = self.canvas.grid_to_screen(x1, y1)
        screen_x2, screen_y2 = self.canvas.grid_to_screen(x2, y2)
        screen_x3, screen_y3 = self.canvas.grid_to_screen(x3, y3)
        
        # 设置特殊预览模式标识
        self.canvas.current_shape = "triangle_preview"
        
        # 清空现有三角形点
        self.canvas.triangle_points = []
        
        # 设置三角形的顶点用于预览
        self.canvas.line_start_point = (screen_x1, screen_y1)  # 第一个点
        self.canvas.triangle_points = [(screen_x2, screen_y2)]  # 第二个点
        self.canvas.temp_shape = (screen_x3, screen_y3)  # 第三个点
        
        # 添加临时端点的预览
        self.canvas.temp_endpoints = []
        
        # 添加三个端点作为临时点
        self.canvas.temp_endpoints.append({
            'x': screen_x1, 'y': screen_y1, 
            'color': self.color, 'name': 'A'
        })
        self.canvas.temp_endpoints.append({
            'x': screen_x2, 'y': screen_y2, 
            'color': self.color, 'name': 'B'
        })
        self.canvas.temp_endpoints.append({
            'x': screen_x3, 'y': screen_y3, 
            'color': self.color, 'name': 'C'
        })
        
        # 更新画布
        self.canvas.update()
    
    def _on_create_from_properties(self, properties: Dict[str, Any]):
        """从属性创建三角形"""
        if not self.is_active:
            return
        
        # 获取三个顶点属性
        x1 = properties.get('x1', 0)
        y1 = properties.get('y1', 0)
        x2 = properties.get('x2', 0)
        y2 = properties.get('y2', 0)
        x3 = properties.get('x3', 0)
        y3 = properties.get('y3', 0)
        
        # 转换为屏幕坐标
        screen_x1, screen_y1 = self.canvas.grid_to_screen(x1, y1)
        screen_x2, screen_y2 = self.canvas.grid_to_screen(x2, y2)
        screen_x3, screen_y3 = self.canvas.grid_to_screen(x3, y3)
        
        # 添加三个顶点
        self.canvas.points.append({'x': screen_x1, 'y': screen_y1, 'color': self.color})
        self.canvas.points.append({'x': screen_x2, 'y': screen_y2, 'color': self.color})
        self.canvas.points.append({'x': screen_x3, 'y': screen_y3, 'color': self.color})
        
        # 计算三条边的长度
        side1 = math.sqrt((screen_x2 - screen_x1)**2 + (screen_y2 - screen_y1)**2)
        side2 = math.sqrt((screen_x3 - screen_x2)**2 + (screen_y3 - screen_y2)**2)
        side3 = math.sqrt((screen_x1 - screen_x3)**2 + (screen_y1 - screen_y3)**2)
        
        # 转换为相对坐标系的长度
        grid_spacing = self.canvas.grid_spacing
        real_side1 = side1 / grid_spacing
        real_side2 = side2 / grid_spacing
        real_side3 = side3 / grid_spacing
        
        # 添加三条边
        self.canvas.lines.append({'x1': screen_x1, 'y1': screen_y1, 'x2': screen_x2, 'y2': screen_y2, 'color': self.color})
        self.canvas.lines.append({'x1': screen_x2, 'y1': screen_y2, 'x2': screen_x3, 'y2': screen_y3, 'color': self.color})
        self.canvas.lines.append({'x1': screen_x3, 'y1': screen_y3, 'x2': screen_x1, 'y2': screen_y1, 'color': self.color})
        
        # 添加边长文本
        self.canvas.line_texts.append(f"{real_side1:.1f}")
        self.canvas.line_texts.append(f"{real_side2:.1f}")
        self.canvas.line_texts.append(f"{real_side3:.1f}")
        
        # 计算三角形周长
        perimeter = side1 + side2 + side3
        real_perimeter = perimeter / grid_spacing
        
        # 计算三角形面积（使用海伦公式）
        s = perimeter / 2
        area = math.sqrt(s * (s - side1) * (s - side2) * (s - side3))
        real_area = area / (grid_spacing ** 2)
        
        # 存储到形状属性中
        self.canvas.shapes.append({
            'type': 'triangle',
            'vertices': [(screen_x1, screen_y1), (screen_x2, screen_y2), (screen_x3, screen_y3)],
            'sides': [side1, side2, side3],
            'area': area,
            'perimeter': perimeter,
            'color': self.color
        })
        
        # 清除临时端点和临时状态
        self.canvas.temp_endpoints = []
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        self.canvas.triangle_points = []
        
        # 更新画布
        self.canvas.update()
        
        # 发送三角形创建信号
        triangle_data = {
            'type': 'triangle',
            'x1': x1, 'y1': y1,
            'x2': x2, 'y2': y2,
            'x3': x3, 'y3': y3,
            'sides': [real_side1, real_side2, real_side3],
            'perimeter': real_perimeter,
            'area': real_area,
            'color': self.color
        }
        self.canvas.shape_created.emit(triangle_data)
    
    def handle_mouse_press(self, x: float, y: float):
        """处理鼠标按下事件"""
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        if len(self.vertices) == 0:
            # 添加第一个点
            self.vertices.append((screen_x, screen_y))
            self.canvas.line_start_point = (screen_x, screen_y)
            self.canvas.points.append({
                'x': screen_x, 'y': screen_y, 'color': self.color
            })
            self.canvas.update()
        elif len(self.vertices) == 1:
            # 添加第二个点
            self.vertices.append((screen_x, screen_y))
            self.canvas.triangle_points.append((screen_x, screen_y))
            self.canvas.points.append({
                'x': screen_x, 'y': screen_y, 'color': self.color
            })
            
            # 创建第一条边
            x1, y1 = self.vertices[0]
            self.canvas.lines.append({
                'x1': x1, 'y1': y1, 
                'x2': screen_x, 'y2': screen_y, 
                'color': self.color
            })
            self.canvas.update()
        elif len(self.vertices) == 2:
            # 添加第三个点，完成三角形
            self.vertices.append((screen_x, screen_y))
            self.canvas.points.append({
                'x': screen_x, 'y': screen_y, 'color': self.color
            })
            
            # 获取三个点的坐标
            x1, y1 = self.vertices[0]
            x2, y2 = self.vertices[1]
            x3, y3 = screen_x, screen_y
            
            # 添加剩余两条边
            self.canvas.lines.append({
                'x1': x2, 'y1': y2, 
                'x2': x3, 'y2': y3, 
                'color': self.color
            })
            self.canvas.lines.append({
                'x1': x3, 'y1': y3, 
                'x2': x1, 'y2': y1, 
                'color': self.color
            })
            
            # 计算三条边的长度
            side1 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            side2 = math.sqrt((x3 - x2)**2 + (y3 - y2)**2)
            side3 = math.sqrt((x1 - x3)**2 + (y1 - y3)**2)
            
            # 转换为相对坐标系的长度
            grid_spacing = self.canvas.grid_spacing
            real_side1 = side1 / grid_spacing
            real_side2 = side2 / grid_spacing
            real_side3 = side3 / grid_spacing
            
            # 添加边长文本
            self.canvas.line_texts.append(f"{real_side1:.1f}")
            self.canvas.line_texts.append(f"{real_side2:.1f}")
            self.canvas.line_texts.append(f"{real_side3:.1f}")
            
            # 计算三角形周长
            perimeter = side1 + side2 + side3
            real_perimeter = perimeter / grid_spacing
            
            # 计算三角形面积（使用海伦公式）
            s = perimeter / 2
            area = math.sqrt(s * (s - side1) * (s - side2) * (s - side3))
            real_area = area / (grid_spacing ** 2)
            
            # 存储到形状属性中
            self.canvas.shapes.append({
                'type': 'triangle',
                'vertices': [(x1, y1), (x2, y2), (x3, y3)],
                'sides': [side1, side2, side3],
                'area': area,
                'perimeter': perimeter,
                'color': self.color
            })
            
            # 发送三角形创建信号
            grid_x1, grid_y1 = self.canvas.screen_to_grid(x1, y1)
            grid_x2, grid_y2 = self.canvas.screen_to_grid(x2, y2)
            grid_x3, grid_y3 = self.canvas.screen_to_grid(x3, y3)
            
            triangle_data = {
                'type': 'triangle',
                'x1': grid_x1, 'y1': grid_y1,
                'x2': grid_x2, 'y2': grid_y2,
                'x3': grid_x3, 'y3': grid_y3,
                'sides': [real_side1, real_side2, real_side3],
                'perimeter': real_perimeter,
                'area': real_area,
                'color': self.color
            }
            self.canvas.shape_created.emit(triangle_data)
            
            # 重置状态，准备下一个三角形
            self.vertices = []
            self.canvas.line_start_point = None
            self.canvas.triangle_points = []
            self.canvas.temp_shape = None
            
            self.canvas.update()
    
    def handle_mouse_move(self, x: float, y: float):
        """处理鼠标移动事件"""
        if not self.vertices:
            return
            
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 设置临时形状
        self.canvas.temp_shape = (screen_x, screen_y)
        
        # 更新画布
        self.canvas.update()
    
    def handle_mouse_release(self, x: float, y: float):
        """处理鼠标释放事件"""
        # 三角形的逻辑已在press事件中处理
        pass
