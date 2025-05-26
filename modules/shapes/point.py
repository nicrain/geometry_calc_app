"""
点形状的实现。
"""
from typing import Dict, Any, List, Tuple
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt6.QtCore import QRect

# 修正导入语句使用正确的路径
from modules.shapes import Shape, ShapeType

class PointShape(Shape):
    """表示一个点的形状"""
    
    def __init__(self, x: float, y: float, name: str = None, color: str = "#E65100"):
        super().__init__(ShapeType.POINT)
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.radius = 5  # 点的半径
    
    def get_points(self) -> List[Point]:
        """获取形状上的所有点"""
        return [Point(self.x, self.y, self.color, self.name)]
    
    def contains(self, x: float, y: float, tolerance: float = 5.0) -> bool:
        """判断给定点是否包含在形状中（或在形状附近）"""
        distance = ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5
        return distance <= self.radius + tolerance
    
    def render(self, painter: QPainter) -> None:
        """使用给定的QPainter绘制形状"""
        # 设置点的颜色
        painter.setPen(QPen(QColor(self.color), 2))
        painter.setBrush(QBrush(QColor(self.color)))
        
        # 绘制点
        painter.drawEllipse(int(self.x) - self.radius, int(self.y) - self.radius, 
                            self.radius * 2, self.radius * 2)
        
        # 绘制点的名称标签
        if self.name:
            painter.setPen(QPen(QColor("#000000")))
            font = QFont("Arial", 10)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(int(self.x) - 5, int(self.y) - 10, self.name)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示，用于序列化"""
        result = {
            'type': 'point',
            'x': self.x,
            'y': self.y,
            'color': self.color
        }
        if self.name:
            result['name'] = self.name
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PointShape':
        """从字典创建形状实例，用于反序列化"""
        return cls(
            x=data['x'],
            y=data['y'],
            name=data.get('name'),
            color=data.get('color', "#E65100")
        )

"""
点类的实现，表示二维平面上的一个点。
"""
from typing import Tuple, Dict, Any, Optional
import math

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
    
    def angle_to(self, other: 'Point') -> float:
        """计算到另一个点的角度（弧度）"""
        dx = other.x - self.x
        dy = other.y - self.y
        return math.atan2(dy, dx)
    
    def angle_to_degrees(self, other: 'Point') -> float:
        """计算到另一个点的角度（度数，0-360°）"""
        angle_rad = self.angle_to(other)
        angle_deg = (angle_rad * 180 / math.pi) % 360
        return angle_deg
    
    def midpoint(self, other: 'Point') -> 'Point':
        """计算与另一个点的中点"""
        mid_x = (self.x + other.x) / 2
        mid_y = (self.y + other.y) / 2
        return Point(mid_x, mid_y, self.color)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示"""
        return {
            'x': self.x,
            'y': self.y,
            'color': self.color,
            'name': self.name
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Point':
        """从字典创建点"""
        return Point(
            x=data.get('x', 0.0),
            y=data.get('y', 0.0),
            color=data.get('color', "#000000"),
            name=data.get('name', "")
        )
    
    def __eq__(self, other: object) -> bool:
        """判断两个点是否相等"""
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    def __repr__(self) -> str:
        """返回点的字符串表示"""
        return f"Point({self.x}, {self.y})"
