import tkinter as tk
import sys
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

from modules.geometry_module import GeometryModule
from modules.calculator_module import CalculatorModule
from modules.eye_tracker_module import EyeTrackerModule
from modules.feedback_module import show_feedback
from modules.ui_components import MetroButton

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logiciel de Géométrie & Calcul pour Enfants")
        self.root.geometry("1024x768")  # 更大的窗口尺寸
        
        # Metro风格的颜色
        self.colors = {
            'geometry': '#00A300',  # 绿色
            'calculator': '#2D89EF',  # 蓝色
        }
        
        # 创建主容器
        self.main_container = tk.Frame(self.root, bg='#FFFFFF')
        self.main_container.pack(side="top", fill="both", expand=True)
        
        # 创建网格布局的按钮区域
        self.button_frame = tk.Frame(self.main_container, bg='#FFFFFF')
        self.button_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
        # 创建内容区域
        self.content_frame = tk.Frame(self.main_container, bg='#FFFFFF')
        self.content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
        # 初始化模块
        self.geometry_module = GeometryModule(self.content_frame)
        self.calculator_module = CalculatorModule(self.content_frame)
        
        self.create_metro_buttons()
        self.show_geometry()

    def create_metro_buttons(self):
        # 使用网格布局创建Metro风格按钮
        MetroButton(
            self.button_frame,
            text="Géométrie",
            bg=self.colors['geometry'],
            fg="white",
            command=self.show_geometry
        ).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        MetroButton(
            self.button_frame,
            text="Calculatrice",
            bg=self.colors['calculator'],
            fg="white",
            command=self.show_calculator
        ).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # 配置网格列的权重，使按钮均匀分布
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

    def show_geometry(self):
        self.calculator_module.hide()
        self.geometry_module.show()

    def show_calculator(self):
        self.geometry_module.hide()
        self.calculator_module.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()