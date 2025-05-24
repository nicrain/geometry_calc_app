"""
形状处理器基类
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class ShapeHandler(ABC):
    """形状处理器基类"""
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.properties_panel = None
        self.is_active = False
        
    def set_properties_panel(self, panel):
        """设置关联的属性面板"""
        self.properties_panel = panel
        
    def activate(self):
        """激活此处理器"""
        self.is_active = True
        self._reset_canvas_state()
        self._connect_canvas_events()
        
    def deactivate(self):
        """停用此处理器"""
        self.is_active = False
        self._disconnect_canvas_events()
    
    def _on_properties_changed(self, properties: Dict[str, Any]):
        """处理属性变化"""
        if not self.is_active:
            return
        
        self.preview_from_properties(properties)
    
    def _on_create_from_properties(self, properties: Dict[str, Any]):
        """从属性创建形状"""
        if not self.is_active:
            return
            
        # 具体实现由子类提供
        
    def preview_from_properties(self, properties: Dict[str, Any]):
        """根据属性预览形状"""
        # 具体实现由子类提供
        pass
    
    # 鼠标事件处理方法 - 子类可选择实现
    def handle_mouse_press(self, x: float, y: float):
        """处理鼠标按下事件"""
        pass
    
    def handle_mouse_move(self, x: float, y: float):
        """处理鼠标移动事件"""
        pass
    
    def handle_mouse_release(self, x: float, y: float):
        """处理鼠标释放事件"""
        pass
    
    @abstractmethod
    def _reset_canvas_state(self):
        """重置画布状态"""
        pass
    
    @abstractmethod
    def _connect_canvas_events(self):
        """连接画布事件"""
        pass
    
    @abstractmethod
    def _disconnect_canvas_events(self):
        """断开画布事件连接"""
        pass
    
    @property
    @abstractmethod
    def shape_type(self):
        """返回此处理器处理的形状类型"""
        pass
