import sys
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

# 添加项目根目录到Python路径
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

# 导入UI组件
from modules.ui_components_pyqt import MetroButton, BaseModule

# 导入功能模块
from modules.geometry_module_pyqt import GeometryModule
from modules.calculator_module_pyqt import CalculatorModule
# from modules.eye_tracker_module import EyeTrackerModule
# from modules.feedback_module import show_feedback

# MetroButton和BaseModule类已移动到modules/ui_components_pyqt.py

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logiciel de Géométrie & Calcul pour Enfants")
        self.resize(1024, 768)  # 更大的窗口尺寸
        
        # 更新 Metro 风格的颜色，使用更深的色调
        self.colors = {
            'geometry': '#1B5E20',  # 深墨绿色
            'calculator': '#1A237E',  # 深靛蓝色
            'back': '#757575',       # 返回按钮灰色
            'undo': '#FF5722',       # 撤销按钮橙色
        }
        
        # 创建主容器
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setStyleSheet("background-color: #FFFFFF;")
        
        # 创建主页面容器
        self.home_widget = QWidget()
        self.home_layout = QVBoxLayout(self.home_widget)
        self.main_layout.addWidget(self.home_widget)
        
        # 创建模块页面容器
        self.module_widget = QWidget()
        self.module_layout = QVBoxLayout(self.module_widget)
        self.module_widget.hide()  # 初始隐藏模块页面
        self.main_layout.addWidget(self.module_widget)
        
        # 初始化模块
        self.geometry_module = GeometryModule()
        self.calculator_module = CalculatorModule()
        
        # 将模块添加到模块页面布局中，但初始时都隐藏
        self.module_layout.addWidget(self.geometry_module)
        self.module_layout.addWidget(self.calculator_module)
        self.geometry_module.hide()
        self.calculator_module.hide()
        
        # 创建主页面大按钮
        self.create_home_buttons()

    def create_home_buttons(self):
        # 创建主页面的大按钮
        button_frame = QWidget()
        button_layout = QGridLayout(button_frame)
        button_layout.setContentsMargins(50, 50, 50, 50)
        self.home_layout.addWidget(button_frame)
        
        # 创建大尺寸的按钮
        font = QFont("Arial", 24)
        font.setBold(True)
        
        # 几何按钮
        geometry_button = MetroButton("Géométrie", self.colors['geometry'], "white")
        geometry_button.setFont(font)
        geometry_button.setMinimumSize(300, 200)
        geometry_button.clicked.connect(self.show_geometry_module)
        button_layout.addWidget(geometry_button, 0, 0)
        
        # 计算器按钮
        calculator_button = MetroButton("Calculatrice", self.colors['calculator'], "white")
        calculator_button.setFont(font)
        calculator_button.setMinimumSize(300, 200)
        calculator_button.clicked.connect(self.show_calculator_module)
        button_layout.addWidget(calculator_button, 0, 1)
        
        # 设置网格布局的间距
        button_layout.setHorizontalSpacing(30)
        button_layout.setVerticalSpacing(30)

    def show_home(self):
        # 隐藏模块页面，显示主页面
        self.module_widget.hide()
        self.home_widget.show()
        
    def show_geometry_module(self):
        # 隐藏主页面，显示模块页面
        self.home_widget.hide()
        self.module_widget.show()
        
        # 显示几何模块
        self.calculator_module.hide_module()
        self.geometry_module.show_module()
        
    def show_calculator_module(self):
        # 隐藏主页面，显示模块页面
        self.home_widget.hide()
        self.module_widget.show()
        
        # 显示计算器模块
        self.geometry_module.hide_module()
        self.calculator_module.show_module()
        
    def back_to_home(self):
        # 返回主页面
        self.module_widget.hide()
        self.home_widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())