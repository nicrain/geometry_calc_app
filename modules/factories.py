"""
工厂类，用于创建形状处理器和属性面板
"""
from typing import Dict, Any, Optional, Type

from modules.canvas import Canvas
from modules.shapes import ShapeType
from modules.shape_handlers import ShapeHandler
from modules.shape_handlers.point_handler import PointHandler
from modules.shape_handlers.line_handler import LineHandler
from modules.shape_handlers.rectangle_handler import RectangleHandler
from modules.shape_handlers.circle_handler import CircleHandler
from modules.shape_handlers.triangle_handler import TriangleHandler

from modules.property_panels import PropertyPanel
from modules.property_panels.point_properties_panel import PointPropertiesPanel
from modules.property_panels.line_properties_panel import LinePropertiesPanel
from modules.property_panels.rectangle_properties_panel import RectanglePropertiesPanel
from modules.property_panels.circle_properties_panel import CirclePropertiesPanel
from modules.property_panels.triangle_properties_panel import TrianglePropertiesPanel

class ShapeHandlerFactory:
    """形状处理器工厂类"""
    
    _handlers: Dict[ShapeType, Type[ShapeHandler]] = {
        ShapeType.POINT: PointHandler,
        ShapeType.LINE: LineHandler,
        ShapeType.RECTANGLE: RectangleHandler,
        ShapeType.CIRCLE: CircleHandler,
        ShapeType.TRIANGLE: TriangleHandler
    }
    
    @classmethod
    def create(cls, shape_type: ShapeType, canvas: Canvas) -> Optional[ShapeHandler]:
        """创建形状处理器"""
        handler_class = cls._handlers.get(shape_type)
        if handler_class:
            return handler_class(canvas)
        return None

class PropertyPanelFactory:
    """属性面板工厂类"""
    
    _panels: Dict[ShapeType, Type[PropertyPanel]] = {
        ShapeType.POINT: PointPropertiesPanel,
        ShapeType.LINE: LinePropertiesPanel,
        ShapeType.RECTANGLE: RectanglePropertiesPanel,
        ShapeType.CIRCLE: CirclePropertiesPanel,
        ShapeType.TRIANGLE: TrianglePropertiesPanel
    }
    
    @classmethod
    def create(cls, shape_type: ShapeType, parent=None) -> Optional[PropertyPanel]:
        """创建属性面板"""
        panel_class = cls._panels.get(shape_type)
        if panel_class:
            return panel_class(parent)
        return None
