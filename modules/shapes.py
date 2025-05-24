"""
形状相关的基础类和枚举定义。
"""
from enum import Enum, auto
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import math
from abc import ABC, abstractmethod

class ShapeType(Enum):
    """几何形状类型枚举"""
    POINT = auto()
    LINE = auto()
    CIRCLE = auto()
    RECTANGLE = auto()
    TRIANGLE = auto()

@dataclass
class Point:
    """点的数据类"""
    x: float
    y: float
    color: str = "#E65100"  # 默认橙色
    name: Optional[str] = None
    
    def distance_to(self, other: 'Point') -> float:
        """计算到另一个点的距离"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

@dataclass
class Line:
    """线段数据类"""
    start: Point
    end: Point
    color: str = "#0277BD"  # 默认蓝色
    
    @property
    def length(self) -> float:
        """计算线段长度"""
        return self.start.distance_to(self.end)
    
    @property
    def angle(self) -> float:
        """计算线段角度（度数）"""
        angle_rad = math.atan2(self.end.y - self.start.y, self.end.x - self.start.x)
        return (angle_rad * 180 / math.pi) % 360

@dataclass
class Rectangle:
    """矩形数据类"""
    top_left: Point
    width: float
    height: float
    color: str = "#1A237E"  # 默认深蓝色
    
    @property
    def top_right(self) -> Point:
        return Point(self.top_left.x + self.width, self.top_left.y, self.color)
    
    @property
    def bottom_left(self) -> Point:
        return Point(self.top_left.x, self.top_left.y + self.height, self.color)
    
    @property
    def bottom_right(self) -> Point:
        return Point(self.top_left.x + self.width, self.top_left.y + self.height, self.color)
    
    @property
    def perimeter(self) -> float:
        """计算周长"""
        return 2 * (self.width + self.height)
    
    @property
    def area(self) -> float:
        """计算面积"""
        return self.width * self.height
    
    @property
    def vertices(self) -> List[Point]:
        """获取所有顶点"""
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left]

@dataclass
class Circle:
    """圆形数据类"""
    center: Point
    radius: float
    color: str = "#1B5E20"  # 默认深绿色
    
    @property
    def circumference(self) -> float:
        """计算周长"""
        return 2 * math.pi * self.radius
    
    @property
    def area(self) -> float:
        """计算面积"""
        return math.pi * self.radius * self.radius

@dataclass
class Triangle:
    """三角形数据类"""
    vertex1: Point
    vertex2: Point
    vertex3: Point
    color: str = "#311B92"  # 默认深紫色
    
    @property
    def sides(self) -> List[float]:
        """计算三条边的长度"""
        side1 = self.vertex1.distance_to(self.vertex2)
        side2 = self.vertex2.distance_to(self.vertex3)
        side3 = self.vertex3.distance_to(self.vertex1)
        return [side1, side2, side3]
    
    @property
    def perimeter(self) -> float:
        """计算周长"""
        return sum(self.sides)
    
    @property
    def area(self) -> float:
        """计算面积（海伦公式）"""
        sides = self.sides
        s = self.perimeter / 2
        try:
            return math.sqrt(s * (s - sides[0]) * (s - sides[1]) * (s - sides[2]))
        except ValueError:
            # 无法形成三角形的情况
            return 0.0
    
    @property
    def vertices(self) -> List[Point]:
        """获取所有顶点"""
        return [self.vertex1, self.vertex2, self.vertex3]

# 需要添加Shape抽象基类，因为代码可能在其他地方引用了这个类
class Shape(ABC):
    """形状的抽象基类"""
    
    def __init__(self, shape_type: ShapeType):
        self.shape_type = shape_type
    
    @abstractmethod
    def get_points(self) -> List[Point]:
        """获取形状上的所有点"""
        pass
    
    @abstractmethod
    def contains(self, x: float, y: float, tolerance: float = 5.0) -> bool:
        """判断给定点是否包含在形状中（或在形状附近）"""
        pass
    
    @abstractmethod
    def render(self, painter) -> None:
        """使用给定的QPainter绘制形状"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict:
        """转换为字典表示，用于序列化"""
        pass
