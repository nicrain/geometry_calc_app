"""
重构后的几何模块，整合了Canvas、形状处理器和属性面板
"""
from typing import Dict, Any, List, Optional
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from modules.ui_components_pyqt import BaseModule, MetroButton
from modules.canvas import Canvas
from modules.shapes import ShapeType
from modules.factories import ShapeHandlerFactory, PropertyPanelFactory

class GeometryModuleRefactored(BaseModule):
    """重构后的几何模块"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建标题
        title_label = QLabel("Module de Géométrie")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # 创建内容区域的水平布局
        content_layout = QHBoxLayout()
        self.main_layout.addLayout(content_layout)
        
        # 创建工具栏容器
        self.tools_frame = QWidget()
        self.tools_frame.setFixedWidth(240)
        self.tools_frame.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                border-right: 1px solid #CCCCCC;
            }
        """)
        self.tools_layout = QGridLayout(self.tools_frame)
        self.tools_layout.setContentsMargins(5, 5, 5, 5)
        self.tools_layout.setHorizontalSpacing(5)
        self.tools_layout.setVerticalSpacing(5)
        content_layout.addWidget(self.tools_frame)
        
        # 创建画布区域容器
        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(10, 0, 10, 10)
        content_layout.addWidget(canvas_container)
        
        # 创建信息显示栏
        self.info_panel = QLabel("Informations de coordonnées")
        self.info_panel.setFont(QFont("Arial", 10))
        self.info_panel.setStyleSheet("""
            QLabel {
                background-color: #F8F9FA;
                color: #212529;
                border: 1px solid #DEE2E6;
                border-radius: 3px;
                padding: 2px 8px;
            }
        """)
        self.info_panel.setMinimumHeight(24)
        self.info_panel.setMaximumHeight(60)
        self.info_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.info_panel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.info_panel.setTextFormat(Qt.TextFormat.RichText)
        self.info_panel.setWordWrap(True)
        canvas_layout.addWidget(self.info_panel)
        
        # 设置画布容器的最小宽度
        canvas_container.setMinimumWidth(600)
        
        # 初始化画布
        self.canvas = Canvas()
        canvas_layout.addWidget(self.canvas)
        
        # 连接画布信号
        self.canvas.mouse_position_changed.connect(self.update_mouse_position_info)
        self.canvas.point_created.connect(self.update_coordinate_info)
        self.canvas.shape_created.connect(self.update_shape_info)
        self.canvas.shape_preview.connect(self.update_shape_preview_info)
        self.canvas.canvas_cleared.connect(self.reset_info_panel)
        
        # 初始化形状处理器和属性面板
        self.shape_handlers = {}
        self.property_panels = {}
        
        # 初始化当前活动的处理器和面板
        self.active_handler = None
        self.active_panel = None

        # 关键：初始化时将canvas.shape_handler设为None
        self.canvas.shape_handler = None
        
        # 创建属性面板开关按钮
        self.properties_button = MetroButton("Propriétés", "#030d03", "#FFFFFF")
        self.properties_button.setMinimumSize(220, 40)
        self.properties_button.setFont(QFont("Arial", 10))
        self.properties_button.clicked.connect(self._toggle_properties)
        self.tools_layout.addWidget(self.properties_button, 3, 0, 1, 2)
        self.properties_button.hide()  # 默认隐藏
        
        # 属性是否启用
        self.properties_enabled = False
        
        # 创建工具栏
        self._create_geometry_tools()
        
        # 初始化形状处理器和属性面板
        self._init_handlers_and_panels()
    
    def _create_geometry_tools(self):
        """创建几何工具按钮"""
        # 返回主界面按钮
        return_button = MetroButton("Retour", "#757575", "#FFFFFF")
        return_button.setMinimumSize(110, 110)
        return_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        return_button.clicked.connect(self.back_to_home)
        self.tools_layout.addWidget(return_button, 0, 0)
        
        # 点按钮
        self.point_button = MetroButton("Point", "#E65100", "#FFFFFF")
        self.point_button.setMinimumSize(110, 110)
        self.point_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.point_button.clicked.connect(lambda: self.select_shape(ShapeType.POINT))
        self.tools_layout.addWidget(self.point_button, 0, 1)
        
        # 线段按钮
        self.line_button = MetroButton("Ligne", "#0277BD", "#FFFFFF")
        self.line_button.setMinimumSize(110, 110)
        self.line_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.line_button.clicked.connect(lambda: self.select_shape(ShapeType.LINE))
        self.tools_layout.addWidget(self.line_button, 1, 0)
        
        # 矩形按钮
        self.rectangle_button = MetroButton("Rectangle", "#1A237E", "#FFFFFF")
        self.rectangle_button.setMinimumSize(110, 110)
        self.rectangle_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.rectangle_button.clicked.connect(lambda: self.select_shape(ShapeType.RECTANGLE))
        self.tools_layout.addWidget(self.rectangle_button, 1, 1)
        
        # 圆形按钮
        self.circle_button = MetroButton("Cercle", "#1B5E20", "#FFFFFF")
        self.circle_button.setMinimumSize(110, 110)
        self.circle_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.circle_button.clicked.connect(lambda: self.select_shape(ShapeType.CIRCLE))
        self.tools_layout.addWidget(self.circle_button, 2, 0)
        
        # 三角形按钮
        self.triangle_button = MetroButton("Triangle", "#311B92", "#FFFFFF")
        self.triangle_button.setMinimumSize(110, 110)
        self.triangle_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.triangle_button.clicked.connect(lambda: self.select_shape(ShapeType.TRIANGLE))
        self.tools_layout.addWidget(self.triangle_button, 2, 1)
        
        # 添加弹性空间
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.tools_layout.addWidget(spacer, 9, 0, 1, 2)
        
        # 添加清除按钮
        clear_button = MetroButton("Effacer", "#B71C1C", "#FFFFFF")
        clear_button.setMinimumSize(110, 110)
        clear_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        clear_button.clicked.connect(self.canvas.clear)
        self.tools_layout.addWidget(clear_button, 10, 0)
        
        # 添加坐标轴切换按钮
        self.axes_button = MetroButton("Axes", "#607D8B", "#FFFFFF")
        self.axes_button.setMinimumSize(110, 110)
        self.axes_button.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))
        self.axes_button.clicked.connect(self.toggle_axes)
        self.axes_button.set_active(self.canvas.show_axes)
        self.tools_layout.addWidget(self.axes_button, 10, 1)
    
    def _init_handlers_and_panels(self):
        """初始化所有形状处理器和属性面板"""
        # 为每种形状类型创建处理器和面板
        for shape_type in ShapeType:
            # 创建处理器
            handler = ShapeHandlerFactory.create(shape_type, self.canvas)
            if handler:
                self.shape_handlers[shape_type] = handler
            
            # 创建面板
            panel = PropertyPanelFactory.create(shape_type, self)
            if panel:
                # 连接面板信号到处理器
                if handler and panel:
                    panel.property_changed.connect(handler._on_properties_changed)
                    panel.create_requested.connect(handler._on_create_from_properties)
                
                self.property_panels[shape_type] = panel
                # 将面板添加到工具布局
                self.tools_layout.addWidget(panel, 4 + shape_type.value, 0, 1, 2)
                panel.hide()  # 默认隐藏
    
    def back_to_home(self):
        """返回主界面"""
        # 获取主应用程序实例并调用返回主页面方法
        parent = self.parent()
        while parent:
            if hasattr(parent, 'back_to_home'):
                parent.back_to_home()
                break
            parent = parent.parent()
    
    def select_shape(self, shape_type: ShapeType):
        """选择一个形状类型进行绘制"""
        # 重置所有按钮状态
        self._reset_all_buttons()
        
        # 停用当前活动的处理器
        if self.active_handler:
            self.active_handler.deactivate()
        
        # 隐藏所有属性面板
        self._hide_all_panels()
        
        # 获取对应的处理器
        handler = self.shape_handlers.get(shape_type)
        if not handler:
            # 处理器不存在，简单返回
            return
        
        # 获取对应的面板
        panel = self.property_panels.get(shape_type)
        
        # 激活新的处理器
        handler.activate()
        self.active_handler = handler

        # 关键：将当前handler赋值给canvas.shape_handler
        self.canvas.shape_handler = handler
        
        # 显示属性面板（如果存在）
        if panel:
            panel.set_enabled(False)  # 默认禁用
            panel.show()
            self.active_panel = panel
            self.properties_button.show()
            self.properties_button.setText("Activer Propriétés")
        
        # 设置对应按钮为激活状态
        self._activate_button_for_shape(shape_type)
    
    def _reset_all_buttons(self):
        """重置所有按钮状态"""
        buttons = {
            ShapeType.POINT: self.point_button,
            ShapeType.LINE: self.line_button,
            ShapeType.RECTANGLE: self.rectangle_button,
            ShapeType.CIRCLE: self.circle_button,
            ShapeType.TRIANGLE: self.triangle_button
        }
        
        for button in buttons.values():
            if button:
                button.set_active(False)
    
    def _hide_all_panels(self):
        """隐藏所有属性面板"""
        for panel in self.property_panels.values():
            panel.hide()
        self.properties_button.hide()
        self.active_panel = None
        self.properties_enabled = False
    
    def _activate_button_for_shape(self, shape_type: ShapeType):
        """激活对应形状的按钮"""
        buttons = {
            ShapeType.POINT: self.point_button,
            ShapeType.LINE: self.line_button,
            ShapeType.RECTANGLE: self.rectangle_button,
            ShapeType.CIRCLE: self.circle_button,
            ShapeType.TRIANGLE: self.triangle_button
        }
        
        button = buttons.get(shape_type)
        if button:
            button.set_active(True)
    
    def _toggle_properties(self):
        """切换属性面板的启用状态"""
        if not self.active_panel:
            return
        
        self.properties_enabled = not self.properties_enabled
        self.active_panel.set_enabled(self.properties_enabled)
        
        if self.properties_enabled:
            self.properties_button.setText("Désactiver Propriétés")
        else:
            self.properties_button.setText("Activer Propriétés")
    
    def toggle_axes(self):
        """切换坐标轴显示状态"""
        self.canvas.show_axes = not self.canvas.show_axes
        self.axes_button.set_active(self.canvas.show_axes)
        self.canvas.update()
    
    def update_mouse_position_info(self, x: float, y: float):
        """更新鼠标位置信息"""
        if not self.active_handler:
            return
        
        if self.active_handler.shape_type == ShapeType.POINT:
            # 显示鼠标当前坐标
            self.info_panel.setText(f"<b>Coordonnées:</b> ({x:.2f}, {y:.2f})")

    def update_shape_preview_info(self, preview_data: Dict[str, Any]):
        """更新形状预览信息"""
        if preview_data.get('type') == 'line_preview_start':
            # 显示线段起点实时坐标
            x1 = preview_data.get('x1', 0)
            y1 = preview_data.get('y1', 0)
            info = f"<b>Point de départ:</b> ({x1:.2f}, {y1:.2f})"
            self.info_panel.setText(info)
            
        elif preview_data.get('type') == 'line_preview':
            # 显示完整线段信息
            x1 = preview_data.get('x1', 0)
            y1 = preview_data.get('y1', 0)
            x2 = preview_data.get('x2', 0)
            y2 = preview_data.get('y2', 0)
            length = preview_data.get('length', 0)
            angle = preview_data.get('angle', 0)
            
            info = f"<b>Ligne:</b> Début({x1:.2f}, {y1:.2f}) → Fin({x2:.2f}, {y2:.2f}) | "
            info += f"<b>Longueur:</b> {length:.2f} | <b>Angle:</b> {angle:.1f}°"
            self.info_panel.setText(info)
        elif preview_data.get('type') == 'rectangle_preview_start':
            # 显示矩形起点实时坐标
            x = preview_data.get('x', 0)
            y = preview_data.get('y', 0)
            info = f"<b>Coin de départ:</b> ({x:.2f}, {y:.2f})"
            self.info_panel.setText(info)
        elif preview_data.get('type') == 'rectangle_preview':
            # 显示完整矩形信息
            x1 = preview_data.get('x1', 0)
            y1 = preview_data.get('y1', 0)
            x2 = preview_data.get('x2', 0)
            y2 = preview_data.get('y2', 0)
            width = preview_data.get('width', 0)
            height = preview_data.get('height', 0)
            area = preview_data.get('area', 0)
            
            info = f"<b>Rectangle:</b> ({x1:.2f}, {y1:.2f}) → ({x2:.2f}, {y2:.2f}) | "
            info += f"<b>Largeur:</b> {width:.2f} | <b>Hauteur:</b> {height:.2f} | "
            info += f"<b>Aire:</b> {area:.2f}"
            self.info_panel.setText(info)
        elif preview_data.get('type') == 'circle_preview_start':
            # 显示圆心实时坐标
            x = preview_data.get('x', 0)
            y = preview_data.get('y', 0)
            info = f"<b>Centre du cercle:</b> ({x:.2f}, {y:.2f})"
            self.info_panel.setText(info)
        elif preview_data.get('type') == 'circle_preview':
            # 显示完整圆形信息
            center_x = preview_data.get('center_x', 0)
            center_y = preview_data.get('center_y', 0)
            radius = preview_data.get('radius', 0)
            area = preview_data.get('area', 0)
            
            info = f"<b>Cercle:</b> Centre({center_x:.2f}, {center_y:.2f}) | "
            info += f"<b>Rayon:</b> {radius:.2f} | "
            info += f"<b>Aire:</b> {area:.2f}"
            self.info_panel.setText(info)
        elif preview_data.get('type') == 'triangle_preview_start':
            # 显示三角形第一点实时坐标
            x1 = preview_data.get('x1', 0)
            y1 = preview_data.get('y1', 0)
            info = f"<b>Premier point:</b> A({x1:.2f}, {y1:.2f})"
            self.info_panel.setText(info)
            
        elif preview_data.get('type') == 'triangle_preview_side1':
            # 显示三角形第一条边信息
            x1 = preview_data.get('x1', 0)
            y1 = preview_data.get('y1', 0)
            x2 = preview_data.get('x2', 0)
            y2 = preview_data.get('y2', 0)
            side1 = preview_data.get('side1', 0)
            
            info = f"<b>Triangle:</b> A({x1:.2f}, {y1:.2f}), B({x2:.2f}, {y2:.2f}) | "
            info += f"<b>Côté AB:</b> {side1:.2f}"
            self.info_panel.setText(info)
            
        elif preview_data.get('type') == 'triangle_preview':
            # 显示完整三角形信息
            x1 = preview_data.get('x1', 0)
            y1 = preview_data.get('y1', 0)
            x2 = preview_data.get('x2', 0)
            y2 = preview_data.get('y2', 0)
            x3 = preview_data.get('x3', 0)
            y3 = preview_data.get('y3', 0)
            sides = preview_data.get('sides', [0, 0, 0])
            area = preview_data.get('area', 0)
            perimeter = sum(sides)  # 计算周长
            
            info = f"<b>Triangle:</b> A({x1:.2f}, {y1:.2f}), B({x2:.2f}, {y2:.2f}), C({x3:.2f}, {y3:.2f}) | "
            info += f"<b>Côtés:</b> {sides[0]:.2f}, {sides[1]:.2f}, {sides[2]:.2f} | "
            info += f"<b>Périmètre:</b> {perimeter:.2f} | <b>Aire:</b> {area:.2f}"
            self.info_panel.setText(info)

    def update_coordinate_info(self, point_data: Dict[str, Any]):
        """更新坐标信息"""
        x = point_data.get('x', 0)
        y = point_data.get('y', 0)
        self.info_panel.setText(f"<b>Point:</b> ({x:.2f}, {y:.2f})")
    
    def update_shape_info(self, shape_data: Dict[str, Any]):
        """更新形状信息"""
        shape_type = shape_data.get('type', '')
        
        if shape_type == 'line':
            x1 = shape_data.get('x1', 0)
            y1 = shape_data.get('y1', 0)
            x2 = shape_data.get('x2', 0)
            y2 = shape_data.get('y2', 0)
            length = shape_data.get('length', 0)
            angle = shape_data.get('angle', 0)
            
            info = f"<b>Ligne:</b> ({x1:.2f}, {y1:.2f}) → ({x2:.2f}, {y2:.2f}) | "
            info += f"<b>Longueur:</b> {length:.2f} | <b>Angle:</b> {angle:.1f}°"
            self.info_panel.setText(info)
        
        elif shape_type == 'rectangle':
            x = shape_data.get('x', 0)
            y = shape_data.get('y', 0)
            width = shape_data.get('length', 0)
            height = shape_data.get('width', 0)
            area = shape_data.get('area', 0)
            
            info = f"<b>Rectangle:</b> Coin sup. gauche ({x:.2f}, {y:.2f}) | "
            info += f"<b>Largeur:</b> {width:.2f} | <b>Hauteur:</b> {height:.2f} | "
            info += f"<b>Aire:</b> {area:.2f}"
            self.info_panel.setText(info)
        
        elif shape_type == 'circle':
            x = shape_data.get('x', 0)
            y = shape_data.get('y', 0)
            radius = shape_data.get('radius', 0)
            
            import math
            info = f"<b>Cercle:</b> Centre ({x:.2f}, {y:.2f}) | "
            info += f"<b>Rayon:</b> {radius:.2f} | "
            info += f"<b>Aire:</b> {math.pi * radius * radius:.2f}"
            self.info_panel.setText(info)
        
        elif shape_type == 'triangle':
            x1 = shape_data.get('x1', 0)
            y1 = shape_data.get('y1', 0)
            x2 = shape_data.get('x2', 0)
            y2 = shape_data.get('y2', 0)
            x3 = shape_data.get('x3', 0)
            y3 = shape_data.get('y3', 0)
            sides = shape_data.get('sides', [0, 0, 0])
            perimeter = shape_data.get('perimeter', 0)
            area = shape_data.get('area', 0)  # 获取面积数据
            
            info = f"<b>Triangle:</b> A({x1:.2f}, {y1:.2f}), B({x2:.2f}, {y2:.2f}), C({x3:.2f}, {y3:.2f}) | "
            info += f"<b>Côtés:</b> {sides[0]:.2f}, {sides[1]:.2f}, {sides[2]:.2f} | "
            info += f"<b>Périmètre:</b> {perimeter:.2f} | <b>Aire:</b> {area:.2f}"
            self.info_panel.setText(info)

    def reset_info_panel(self):
        """重置信息面板"""
        self.info_panel.setText("Informations de coordonnées")
