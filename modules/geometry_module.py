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
        self.active_button = None
        
        # 创建标题
        self.title = tk.Label(self.frame, text="Module de Géométrie", font=("Arial", 16))
        self.title.pack(pady=10)
        
        # 创建工具栏和画布区域的容器
        self.content = tk.Frame(self.frame)
        self.content.pack(fill="both", expand=True)
        
        # 当前选中的形状
        self.current_shape = None
        
        # 创建工具栏
        self.create_geometry_tools()
        
        # 创建画布
        self.create_canvas()
        
    def create_geometry_tools(self):
        # 工具按钮区域
        tools_frame = tk.Frame(self.content)
        tools_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # 存储按钮引用以便后续更新状态
        self.circle_button = MetroButton(
            tools_frame,
            text="Cercle",
            bg="#00A300",
            fg="white",
            command=lambda: self.select_shape("circle")
        )
        self.circle_button.pack(pady=5, fill="x")
        
        self.square_button = MetroButton(
            tools_frame,
            text="Carré",
            bg="#2D89EF",
            fg="white",
            command=lambda: self.select_shape("square")
        )
        self.square_button.pack(pady=5, fill="x")
        
        MetroButton(
            tools_frame,
            text="Effacer",
            bg="#E51400",
            fg="white",
            command=self.clear_canvas
        ).pack(pady=5, fill="x")
    
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
        
        # 先检查按钮是否存在
        if self.circle_button and self.square_button:
            # 更新按钮状态
            if shape == "circle":
                self.circle_button.set_active(True)
                self.square_button.set_active(False)
                self.active_button = self.circle_button
            else:
                self.circle_button.set_active(False)
                self.square_button.set_active(True)
                self.active_button = self.square_button
            
        # 更新鼠标样式
        self.canvas.config(cursor="crosshair")
        
        # 添加提示标签
        self.show_instruction()
        
    def show_instruction(self):
        # 清除之前的提示
        for item in self.canvas.find_withtag("instruction"):
            self.canvas.delete(item)
            
        # 添加新提示
        shape_name = "cercle" if self.current_shape == "circle" else "carré"
        self.canvas.create_text(
            300, 200,
            text=f"Cliquez et faites glisser pour dessiner un {shape_name}",
            font=("Arial", 14),
            fill="#666666",
            tags="instruction"
        )
    
    def start_draw(self, event):
        if not self.current_shape:
            return
        self.start_x = event.x
        self.start_y = event.y
    
    def draw(self, event):
        if not self.current_shape or not self.start_x:
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
    
    def end_draw(self, event):
        if not self.current_shape or not self.start_x:
            return
        # 保持最终形状，但重置临时变量
        self.temp_shape = None
        self.start_x = None
        self.start_y = None
        
        # 重新显示提示
        self.show_instruction()
    
    def clear_canvas(self):
        self.canvas.delete("all")