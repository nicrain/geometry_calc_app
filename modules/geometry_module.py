import tkinter as tk
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from modules.base_module import BaseModule
from modules.ui_components import MetroButton

class GeometryModule(BaseModule):
    def __init__(self, parent):
        super().__init__(parent)
        
        # 初始化按钮引用
        self.circle_button = None
        self.square_button = None
        self.triangle_button = None
        self.point_button = None
        self.line_button = None
        self.active_button = None
        
        # 存储绘制的点和线段
        self.points = []
        self.lines = []
        self.line_texts = []  # 存储线段长度文本
        self.selected_line = None  # 当前选中的线段
        self.selected_line_text = None  # 当前选中线段的长度文本
        
        # 创建标题
        self.title = tk.Label(self.frame, text="Module de Géométrie", font=("Arial", 16))
        self.title.pack(pady=10)
        
        # 创建工具栏和画布区域的容器
        self.content = tk.Frame(self.frame)
        self.content.pack(fill="both", expand=True)
        
        # 当前选中的形状
        self.current_shape = None
        
        # 当前绘制模式
        self.draw_mode = None
        
        # 线段绘制的起始点
        self.line_start_point = None
        
        # 创建工具栏
        self.create_geometry_tools()
        
        # 创建画布
        self.create_canvas()
        
    def create_geometry_tools(self):
        tools_frame = tk.Frame(self.content)
        tools_frame.pack(side="left", fill="y", padx=5, pady=5)
        
        button_configs = {
            'width': 100,
            'height': 32,
            'font': ('Arial', 12, 'bold')
        }
        
        # 添加点按钮 (现在是第一个)
        self.point_button = MetroButton(
            tools_frame,
            text="Point",
            bg="#E65100",  # 橙色
            fg="#FFFFFF",
            command=lambda: self.select_draw_mode("point"),
            **button_configs
        )
        self.point_button.pack(pady=3, fill="x")
        
        # 添加线段按钮 (现在是第二个)
        self.line_button = MetroButton(
            tools_frame,
            text="Ligne",
            bg="#0277BD",  # 蓝色
            fg="#FFFFFF",
            command=lambda: self.select_draw_mode("line"),
            **button_configs
        )
        self.line_button.pack(pady=3, fill="x")
        
        # 正方形按钮 (现在是第三个)
        self.square_button = MetroButton(
            tools_frame,
            text="Carré",
            bg="#1A237E",
            fg="#FFFFFF",
            command=lambda: self.select_shape("square"),
            **button_configs
        )
        self.square_button.pack(pady=3, fill="x")
        
        # 圆形按钮 (现在是第四个)
        self.circle_button = MetroButton(
            tools_frame,
            text="Cercle",
            bg="#1B5E20",
            fg="#FFFFFF",
            command=lambda: self.select_shape("circle"),
            **button_configs
        )
        self.circle_button.pack(pady=3, fill="x")
        
        # 三角形按钮 (现在是第五个)
        self.triangle_button = MetroButton(
            tools_frame,
            text="Triangle",
            bg="#311B92",
            fg="#FFFFFF",
            command=lambda: self.select_shape("triangle"),
            **button_configs
        )
        self.triangle_button.pack(pady=3, fill="x")
        
        # 在清除按钮前添加额外的间距
        tk.Frame(tools_frame, height=10).pack(pady=5)
        
        # 清除按钮 (最后一个)
        MetroButton(
            tools_frame,
            text="Effacer",
            bg="#B71C1C",
            fg="#FFFFFF",
            command=self.clear_canvas,
            **button_configs
        ).pack(pady=3, fill="x")
    
    def create_canvas(self):
        # 创建画布容器
        canvas_frame = tk.Frame(self.content, bg="white")
        canvas_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # 创建画布
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="white",
            width=600,
            height=400,
            highlightthickness=1,
            highlightbackground="#ccc"
        )
        self.canvas.pack(fill="both", expand=True)
        
        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        
        # 存储当前绘制的临时形状
        self.temp_shape = None
        self.start_x = None
        self.start_y = None
    
    def select_shape(self, shape):
        self.current_shape = shape
        self.draw_mode = None  # 重置绘制模式
        
        # 先检查按钮是否存在
        if self.circle_button and self.square_button:
            # 重置所有按钮状态
            self.reset_all_buttons()
            
            # 更新按钮状态
            if shape == "circle":
                self.circle_button.set_active(True)
                self.active_button = self.circle_button
            elif shape == "square":
                self.square_button.set_active(True)
                self.active_button = self.square_button
            else:  # triangle
                self.triangle_button.set_active(True)
                self.active_button = self.triangle_button
            
        # 更新鼠标样式
        self.canvas.config(cursor="crosshair")
        
        # 添加提示标签
        self.show_instruction()
    
    def select_draw_mode(self, mode):
        self.draw_mode = mode
        self.current_shape = None  # 重置形状选择
        self.line_start_point = None  # 重置线段起点
        
        # 重置所有按钮状态
        self.reset_all_buttons()
        
        # 更新按钮状态
        if mode == "point":
            self.point_button.set_active(True)
            self.active_button = self.point_button
        elif mode == "line":
            self.line_button.set_active(True)
            self.active_button = self.line_button
        
        # 更新鼠标样式
        self.canvas.config(cursor="crosshair")
        
        # 添加提示标签
        self.show_instruction()
    
    def reset_all_buttons(self):
        # 重置所有按钮状态
        if self.circle_button:
            self.circle_button.set_active(False)
        if self.square_button:
            self.square_button.set_active(False)
        if self.triangle_button:
            self.triangle_button.set_active(False)
        if self.point_button:
            self.point_button.set_active(False)
        if self.line_button:
            self.line_button.set_active(False)
        
    def show_instruction(self):
        # 清除之前的提示
        for item in self.canvas.find_withtag("instruction"):
            self.canvas.delete(item)
        
        instruction_text = ""
        
        # 根据当前模式显示不同的提示
        if self.current_shape:
            shape_names = {
                "circle": "cercle",
                "square": "carré",
                "triangle": "triangle"
            }
            shape_name = shape_names.get(self.current_shape, "")
            instruction_text = f"Cliquez et faites glisser pour dessiner un {shape_name}"
        elif self.draw_mode == "point":
            instruction_text = "Cliquez pour placer un point"
        elif self.draw_mode == "line":
            if not self.line_start_point:
                instruction_text = "Cliquez pour définir le point de départ de la ligne"
            else:
                instruction_text = "Cliquez pour définir le point final de la ligne"
        
        if instruction_text:
            self.canvas.create_text(
                300, 200,
                text=instruction_text,
                font=("Arial", 14),
                fill="#666666",
                tags="instruction"
            )
    
    def start_draw(self, event):
        # 检查是否点击了线段（用于修改长度）
        if self.check_line_click(event.x, event.y):
            return
            
        # 如果是绘制形状模式
        if self.current_shape:
            self.start_x = event.x
            self.start_y = event.y
            return
        
        # 如果是绘制点模式
        if self.draw_mode == "point":
            self.draw_point(event.x, event.y)
            return
        
        # 如果是绘制线段模式
        if self.draw_mode == "line":
            if not self.line_start_point:
                # 设置线段起点
                self.line_start_point = (event.x, event.y)
                # 绘制起点（使用不同的颜色）
                point_radius = 5
                self.canvas.create_oval(
                    event.x - point_radius, 
                    event.y - point_radius, 
                    event.x + point_radius, 
                    event.y + point_radius, 
                    fill="#0277BD",  # 使用线段的蓝色
                    outline="#0277BD",
                    tags="line_point"
                )
                # 更新提示
                self.show_instruction()
            else:
                # 绘制线段
                self.draw_line(self.line_start_point[0], self.line_start_point[1], event.x, event.y)
                # 重置线段起点
                self.line_start_point = None
                # 更新提示
                self.show_instruction()
            return
        
        # 检查是否点击了线段（用于修改长度）
        self.check_line_click(event.x, event.y)
    
    def draw(self, event):
        if not self.current_shape or not self.start_x:
            # 如果当前有选中的线段，处理长度修改
            if self.selected_line is not None:
                self.modify_line_length(event.x, event.y)
                return
            return
            
        # 删除临时形状和提示文字
        if self.temp_shape:
            self.canvas.delete(self.temp_shape)
        self.canvas.delete("instruction")
            
        # 计算尺寸
        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        
        # 绘制临时形状
        if self.current_shape == "circle":
            radius = max(width, height)
            self.temp_shape = self.canvas.create_oval(
                self.start_x - radius,
                self.start_y - radius,
                self.start_x + radius,
                self.start_y + radius,
                outline="#2D89EF",
                fill="#ADD8E6",  # 淡蓝色填充
                width=2
            )
        elif self.current_shape == "square":
            size = max(width, height)
            self.temp_shape = self.canvas.create_rectangle(
                self.start_x,
                self.start_y,
                self.start_x + size,
                self.start_y + size,
                outline="#00A300",
                fill="#90EE90",  # 淡绿色填充
                width=2
            )
        elif self.current_shape == "triangle":
            size = max(width, height)
            # 创建等边三角形
            x1, y1 = self.start_x, self.start_y + size  # 左下角
            x2, y2 = self.start_x + size, self.start_y + size  # 右下角
            x3, y3 = self.start_x + size/2, self.start_y  # 顶点
            self.temp_shape = self.canvas.create_polygon(
                x1, y1, x2, y2, x3, y3,
                outline="#311B92",
                fill="#E6E6FA",  # 淡紫色填充
                width=2
            )
    
    def end_draw(self, event):
        if not self.current_shape or not self.start_x:
            # 如果有选中的线段，重置选中状态
            if self.selected_line is not None:
                self.canvas.itemconfig(self.selected_line, width=2, fill="#0277BD")
                self.selected_line = None
                self.selected_line_text = None
                self.show_instruction()
            return
        # 保持最终形状，但重置临时变量
        self.temp_shape = None
        self.start_x = None
        self.start_y = None
        
        # 重新显示提示
        self.show_instruction()
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []
        self.lines = []
        self.line_texts = []
        self.selected_line = None
        self.selected_line_text = None
        self.line_start_point = None
        self.show_instruction()
    
    def draw_point(self, x, y):
        # 绘制点（小圆）
        point_radius = 5
        point = self.canvas.create_oval(
            x - point_radius, 
            y - point_radius, 
            x + point_radius, 
            y + point_radius, 
            fill="#E65100",  # 橙色
            outline="#E65100",
            tags="point"
        )
        self.points.append((point, x, y))
    
    def draw_line(self, x1, y1, x2, y2):
        # 计算线段长度（像素）
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        
        # 绘制线段
        line = self.canvas.create_line(
            x1, y1, x2, y2,
            fill="#0277BD",  # 蓝色
            width=2,
            tags="line"
        )
        
        # 绘制终点
        point_radius = 5
        end_point = self.canvas.create_oval(
            x2 - point_radius, 
            y2 - point_radius, 
            x2 + point_radius, 
            y2 + point_radius, 
            fill="#0277BD",
            outline="#0277BD",
            tags="line_point"
        )
        
        # 计算文本位置（线段中点）
        text_x = (x1 + x2) / 2
        text_y = (y1 + y2) / 2 - 10  # 稍微上移，避免遮挡线段
        
        # 显示长度文本
        text = self.canvas.create_text(
            text_x, text_y,
            text=f"{length:.1f} px",
            font=("Arial", 10),
            fill="#0277BD",
            tags="line_text"
        )
        
        # 存储线段信息
        self.lines.append((line, x1, y1, x2, y2))
        self.line_texts.append((text, line))
    
    def check_line_click(self, x, y):
        # 检查是否点击了线段的端点
        point_radius = 5  # 端点半径
        for i, (line, x1, y1, x2, y2) in enumerate(self.lines):
            # 分别检查是否点击了起点或终点
            is_start_point = ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5 <= point_radius * 2
            is_end_point = ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5 <= point_radius * 2
            
            if is_start_point or is_end_point:
                # 设置为当前选中的线段
                self.selected_line = line
                # 记录是否点击的是起点
                self.is_dragging_start = is_start_point
                
                # 找到对应的文本
                for text, line_id in self.line_texts:
                    if line_id == line:
                        self.selected_line_text = text
                        break
                
                # 高亮显示选中的线段
                self.canvas.itemconfig(line, width=3, fill="#FF5722")
                
                # 显示修改长度的提示
                self.canvas.delete("instruction")
                self.canvas.create_text(
                    300, 200,
                    text="Faites glisser le point pour modifier la longueur de la ligne",
                    font=("Arial", 14),
                    fill="#666666",
                    tags="instruction"
                )
                return True
        return False
    
    def point_to_line_distance(self, x, y, x1, y1, x2, y2):
        # 计算点到线段的距离
        A = x - x1
        B = y - y1
        C = x2 - x1
        D = y2 - y1
        
        dot = A * C + B * D
        len_sq = C * C + D * D
        
        if len_sq == 0:
            return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
        
        param = dot / len_sq
        
        if param < 0:
            return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
        elif param > 1:
            return ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
        
        x_proj = x1 + param * C
        y_proj = y1 + param * D
        
        return ((x - x_proj) ** 2 + (y - y_proj) ** 2) ** 0.5
    
    def modify_line_length(self, x, y):
        # 修改选中线段的长度
        for i, (line, x1, y1, x2, y2) in enumerate(self.lines):
            if line == self.selected_line:
                if self.is_dragging_start:
                    # 如果拖动的是起点，以终点为固定点
                    new_x1, new_y1 = x, y
                    new_x2, new_y2 = x2, y2
                else:
                    # 如果拖动的是终点，以起点为固定点
                    new_x1, new_y1 = x1, y1
                    new_x2, new_y2 = x, y
                
                # 计算新的线段长度
                new_length = ((new_x2 - new_x1) ** 2 + (new_y2 - new_y1) ** 2) ** 0.5
                
                # 更新线段位置
                self.canvas.coords(line, new_x1, new_y1, new_x2, new_y2)
                
                # 更新线段端点
                point_radius = 5
                # 找到所有带有 line_point 标签的端点
                line_points = self.canvas.find_withtag("line_point")
                for point in line_points:
                    coords = self.canvas.coords(point)
                    center_x = coords[0] + point_radius
                    center_y = coords[1] + point_radius
                    
                    # 检查是否是当前线段的端点
                    if self.is_dragging_start and abs(center_x - x1) < 1 and abs(center_y - y1) < 1:
                        # 更新起点位置
                        self.canvas.coords(point,
                            new_x1 - point_radius,
                            new_y1 - point_radius,
                            new_x1 + point_radius,
                            new_y1 + point_radius)
                    elif not self.is_dragging_start and abs(center_x - x2) < 1 and abs(center_y - y2) < 1:
                        # 更新终点位置
                        self.canvas.coords(point,
                            new_x2 - point_radius,
                            new_y2 - point_radius,
                            new_x2 + point_radius,
                            new_y2 + point_radius)
                
                # 更新文本位置和内容
                if self.selected_line_text:
                    # 计算文本位置（线段中点）
                    text_x = (new_x1 + new_x2) / 2
                    text_y = (new_y1 + new_y2) / 2 - 10  # 稍微上移，避免遮挡线段
                    
                    # 更新文本位置和内容
                    self.canvas.coords(self.selected_line_text, text_x, text_y)
                    self.canvas.itemconfig(self.selected_line_text, text=f"{new_length:.1f} px")
                
                # 更新线段数据
                self.lines[i] = (line, new_x1, new_y1, new_x2, new_y2)