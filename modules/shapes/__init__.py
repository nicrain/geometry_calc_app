"""
形状模块，定义了基本的几何形状类型和类。
"""
from enum import Enum, auto
from typing import Tuple, List, Optional, Dict, Any

class ShapeType(Enum):
    """形状类型枚举"""
    POINT = auto()
    LINE = auto()
    RECTANGLE = auto()
    CIRCLE = auto()
    TRIANGLE = auto()

class Point:
    """表示二维平面上的一个点"""
    def __init__(self, x: float, y: float, color: str = "#000000", name: str = ""):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
    
    def to_screen(self, center_x: float, center_y: float, grid_spacing: float) -> Tuple[float, float]:
        """转换为屏幕坐标"""
        screen_x = center_x + self.x * grid_spacing
        screen_y = center_y - self.y * grid_spacing  # 反转Y轴，符合数学坐标系
        return screen_x, screen_y
    
    @staticmethod
    def from_screen(screen_x: float, screen_y: float, center_x: float, center_y: float, grid_spacing: float) -> 'Point':
        """从屏幕坐标创建点"""
        x = (screen_x - center_x) / grid_spacing
        y = (center_y - screen_y) / grid_spacing  # 反转Y轴，符合数学坐标系
        return Point(x, y)
    
    def distance_to(self, other: 'Point') -> float:
        """计算到另一个点的距离"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示"""
        return {
            'x': self.x,
            'y': self.y,
            'color': self.color,
            'name': self.name
        }
