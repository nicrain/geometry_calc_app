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
    
    def activate(self):
        """激活线段处理器"""
        super().activate()
        self.canvas.draw_mode = "line"
        self.canvas.current_shape = "line"
        
    def preview_from_properties(self, properties: Dict[str, Any]):
        """根据属性预览线段"""
        if not self.is_active:
            return
            
        # 获取属性值
        x1 = properties.get('x1', 0)
        y1 = properties.get('y1', 0)
        x2 = properties.get('x2', 0)
        y2 = properties.get('y2', 0)
        
        # 转换为屏幕坐标
        screen_x1, screen_y1 = self.canvas.grid_to_screen(x1, y1)
        screen_x2, screen_y2 = self.canvas.grid_to_screen(x2, y2)
        
        # 设置临时状态用于预览显示
        self.canvas.current_shape = "line_preview"
        self.canvas.line_start_point = (screen_x1, screen_y1)
        self.canvas.temp_shape = (screen_x2, screen_y2)
        
        # 添加临时端点的预览
        self.canvas.temp_endpoints = [
            {'x': screen_x1, 'y': screen_y1, 'color': self.color, 'name': 'A'},
            {'x': screen_x2, 'y': screen_y2, 'color': self.color, 'name': 'B'}
        ]
        
        # 更新画布
        self.canvas.update()

    def _on_properties_changed(self, properties):
        """属性面板值改变时的响应方法"""
        if not self.is_active:
            return
        
        # 获取属性值
        x1 = properties.get('x1', 0)
        y1 = properties.get('y1', 0)
        x2 = properties.get('x2', 0)
        y2 = properties.get('y2', 0)
        
        # 转换为屏幕坐标
        screen_x1, screen_y1 = self.canvas.grid_to_screen(x1, y1)
        screen_x2, screen_y2 = self.canvas.grid_to_screen(x2, y2)
        
        # 设置临时状态用于预览显示
        self.canvas.line_start_point = (screen_x1, screen_y1)
        self.canvas.temp_shape = (screen_x2, screen_y2)
        
        # 添加临时端点的预览
        if not hasattr(self.canvas, 'temp_endpoints'):
            self.canvas.temp_endpoints = []
        
        # 清空之前的临时端点
        self.canvas.temp_endpoints = []
        
        # 添加两个端点作为临时点
        self.canvas.temp_endpoints.append({
            'x': screen_x1, 
            'y': screen_y1, 
            'color': "#0277BD", 
            'name': 'A'
        })
        self.canvas.temp_endpoints.append({
            'x': screen_x2, 
            'y': screen_y2, 
            'color': "#0277BD", 
            'name': 'B'
        })
        
        # 更新画布
        self.canvas.update()

    def _on_create_from_properties(self, properties):
        """从属性面板创建线段"""
        if not self.is_active:
            return
        
        # 获取属性值
        x1 = properties.get('x1', 0)
        y1 = properties.get('y1', 0)
        x2 = properties.get('x2', 0)
        y2 = properties.get('y2', 0)
        
        # 转换为屏幕坐标
        screen_x1, screen_y1 = self.canvas.grid_to_screen(x1, y1)
        screen_x2, screen_y2 = self.canvas.grid_to_screen(x2, y2)
        
        # 添加起点和终点
        self.canvas.points.append({'x': screen_x1, 'y': screen_y1, 'color': "#0277BD"})
        self.canvas.points.append({'x': screen_x2, 'y': screen_y2, 'color': "#0277BD"})
        
        # 计算线段长度
        length = math.sqrt((screen_x2 - screen_x1) ** 2 + (screen_y2 - screen_y1) ** 2)
        real_length = length / self.canvas.grid_spacing
        length_text = f"{real_length:.1f}"
        
        # 添加线段
        self.canvas.lines.append({
            'x1': screen_x1, 'y1': screen_y1,
            'x2': screen_x2, 'y2': screen_y2,
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
        angle_rad = math.atan2(y2 - y1, x2 - x1)
        # 转换为度数 (0-360°)
        angle_deg = (angle_rad * 180 / math.pi) % 360
        
        # 发射形状创建信号
        shape_data = {
            'type': 'line',
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'length': real_length,
            'angle': angle_deg
        }
        
        # 如果Canvas有shape_created信号，则发射
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
    
    def _connect_canvas_events(self):
        """连接画布事件"""
        # 线段处理器的事件连接逻辑
        pass
    
    def _disconnect_canvas_events(self):
        """断开画布事件连接"""
        # 线段处理器的事件断开逻辑
        pass

    def handle_mouse_press(self, x: float, y: float):
        """处理鼠标按下事件"""
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        if not self.start_point:
            # 设置线段起点
            self.start_point = (screen_x, screen_y)
            self.canvas.line_start_point = self.start_point
            self.canvas.current_shape = "line"
            
            # 添加起点
            self.canvas.points.append({
                'x': screen_x,
                'y': screen_y,
                'color': self.color
            })
            self.canvas.update()
        else:
            # 完成线段绘制
            self.handle_mouse_release(x, y)
    
    def handle_mouse_move(self, x: float, y: float):
        """处理鼠标移动事件"""
        # 发送实时线段信息信号
        if hasattr(self.canvas, 'shape_preview'):
            if not self.start_point:
                # 未点击第一点时，显示当前位置作为起点
                preview_data = {
                    'type': 'line_preview_start',
                    'x1': x, 'y1': y
                }
                self.canvas.shape_preview.emit(preview_data)
            else:
                # 已点击第一点，显示完整线段信息
                screen_x, screen_y = self.canvas.grid_to_screen(x, y)
                self.canvas.temp_shape = (screen_x, screen_y)
                
                x1, y1 = self.start_point
                grid_x1, grid_y1 = self.canvas.screen_to_grid(x1, y1)
                grid_x2, grid_y2 = x, y
                
                # 计算实时长度
                length = math.sqrt((grid_x2 - grid_x1)**2 + (grid_y2 - grid_y1)**2)
                
                # 计算实时角度
                angle_rad = math.atan2(grid_y2 - grid_y1, grid_x2 - grid_x1)
                angle_deg = (angle_rad * 180 / math.pi) % 360
                
                preview_data = {
                    'type': 'line_preview',
                    'x1': grid_x1, 'y1': grid_y1,
                    'x2': grid_x2, 'y2': grid_y2,
                    'length': length,
                    'angle': angle_deg
                }
                self.canvas.shape_preview.emit(preview_data)
                
                self.canvas.update()

    def handle_mouse_release(self, x: float, y: float):
        """处理鼠标释放事件"""
        if not self.start_point:
            return
            
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        x1, y1 = self.start_point
        
        # 检查最小长度
        if math.sqrt((screen_x - x1)**2 + (screen_y - y1)**2) < 10:
            return
        
        # 添加终点
        self.canvas.points.append({
            'x': screen_x,
            'y': screen_y,
            'color': self.color
        })
        
        # 计算长度
        length = math.sqrt((screen_x - x1)**2 + (screen_y - y1)**2)
        real_length = length / self.canvas.grid_spacing
        
        # 添加线段
        self.canvas.lines.append({
            'x1': x1, 'y1': y1,
            'x2': screen_x, 'y2': screen_y,
            'color': self.color
        })
        
        # 添加长度文本
        self.canvas.line_texts.append(f"{real_length:.1f}")
        
        # 发送线段创建信号
        grid_x1, grid_y1 = self.canvas.screen_to_grid(x1, y1)
        grid_x2, grid_y2 = self.canvas.screen_to_grid(screen_x, screen_y)
        
        angle_rad = math.atan2(grid_y2 - grid_y1, grid_x2 - grid_x1)
        angle_deg = (angle_rad * 180 / math.pi) % 360
        
        line_data = {
            'type': 'line',
            'x1': grid_x1, 'y1': grid_y1,
            'x2': grid_x2, 'y2': grid_y2,
            'length': real_length,
            'angle': angle_deg,
            'color': self.color
        }
        self.canvas.shape_created.emit(line_data)
        
        # 清除临时状态
        self.start_point = None
        self.canvas.line_start_point = None
        self.canvas.temp_shape = None
        self.canvas.update()
