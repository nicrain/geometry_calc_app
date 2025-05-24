"""
点形状处理器
"""
from typing import Dict, Any

from modules.shapes import ShapeType
from modules.shape_handlers import ShapeHandler

class PointHandler(ShapeHandler):
    """处理点相关操作的类"""
    
    def __init__(self, canvas):
        super().__init__(canvas)
        self._shape_type = ShapeType.POINT
        self.color = "#E65100"  # 橙色
    
    @property
    def shape_type(self):
        return self._shape_type
    
    def _reset_canvas_state(self):
        """重置画布状态"""
        self.canvas.draw_mode = "point"
        self.canvas.current_shape = None
        self.canvas.temp_point = None
        
    def _connect_canvas_events(self):
        """连接画布事件"""
        # 点处理器不需要特殊的事件连接
        pass
    
    def _disconnect_canvas_events(self):
        """断开画布事件连接"""
        # 点处理器不需要特殊的事件断开
        pass

    def activate(self):
        """激活点处理器"""
        super().activate()
        self.canvas.draw_mode = "point"
        
    def preview_from_properties(self, properties: Dict[str, Any]):
        """根据属性预览点"""
        if not self.is_active:
            return
            
        # 获取属性值
        x = properties.get('x', 0)
        y = properties.get('y', 0)
        
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 设置临时点
        self.canvas.temp_point = (screen_x, screen_y)
        
        # 更新画布
        self.canvas.update()
    
    def _on_create_from_properties(self, properties: Dict[str, Any]):
        """从属性创建点"""
        if not self.is_active:
            return
        
        # 获取属性值
        x = properties.get('x', 0)
        y = properties.get('y', 0)
        
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 添加点
        self.canvas.points.append({
            'x': screen_x,
            'y': screen_y,
            'color': self.color
        })
        
        # 清除临时点
        self.canvas.temp_point = None
        
        # 更新画布
        self.canvas.update()
        
        # 发送点创建信号
        point_data = {'x': x, 'y': y, 'color': self.color}
        self.canvas.point_created.emit(point_data)
    
    def handle_mouse_press(self, x: float, y: float):
        """处理鼠标按下事件"""
        # 转换为屏幕坐标
        screen_x, screen_y = self.canvas.grid_to_screen(x, y)
        
        # 添加点
        self.canvas.points.append({
            'x': screen_x,
            'y': screen_y,
            'color': self.color
        })
        
        # 更新画布
        self.canvas.update()
        
        # 发送点创建信号
        point_data = {'x': x, 'y': y, 'color': self.color}
        self.canvas.point_created.emit(point_data)
    
    def handle_mouse_move(self, x: float, y: float):
        """处理鼠标移动事件"""
        # 在点处理器中通常不需要特殊处理鼠标移动
        pass
    
    def handle_mouse_release(self, x: float, y: float):
        """处理鼠标释放事件"""
        # 在点处理器中通常不需要特殊处理鼠标释放
        pass
