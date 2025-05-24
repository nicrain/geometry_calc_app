#!/usr/bin/env python3
"""
几何计算应用程序 - 为儿童设计的几何和计算工具

这个应用程序集成了几何模块和计算器模块，
提供了简单直观的界面，适合儿童学习使用。
"""

import sys
import os

# 安装与导入依赖检查
try:
    # 尝试导入核心PyQt6模块
    from PyQt6.QtCore import QLibraryInfo
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                QGridLayout, QMessageBox)
    from PyQt6.QtGui import QFont
    
    # 设置Qt插件路径 - 确保插件可以被正确加载
    plugins_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugins_path
    
    # 导入应用程序自定义模块
    try:
        from modules.ui_components_pyqt import MetroButton, BaseModule
        # 从重构后的几何模块导入GeometryModuleRefactored类
        from modules.geometry_module_refactored import GeometryModuleRefactored
        from modules.calculator_module_pyqt import CalculatorModule
        # 可以添加一个调试打印
        print("Modules importés avec succès")
    except ImportError as e:
        print(f"Erreur: Impossible d'importer les modules de l'application: {e}")
        print("Veuillez vous assurer que le répertoire modules existe et contient les fichiers .py requis")
        sys.exit(1)
        
except ImportError as e:
    print(f"Erreur: Impossible d'importer les modules PyQt6: {e}")
    print("Veuillez installer PyQt6: pip install PyQt6")
    sys.exit(1)

class MainApp(QMainWindow):
    """主应用程序类，管理应用程序的主界面和模块切换"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logiciel de Géométrie & Calcul pour Enfants")
        self.resize(1024, 768)
        
        # Metro 风格的颜色方案
        self.colors = {
            'geometry': '#1B5E20',  # 深墨绿色
            'calculator': '#1A237E',  # 深靛蓝色
            'back': '#757575',       # 返回按钮灰色
            'undo': '#FF5722',       # 撤销按钮橙色
        }
        
        self._setup_ui()
        
    def _setup_ui(self):
        """设置用户界面"""
        # 创建主容器
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setStyleSheet("background-color: #FFFFFF;")
        
        # 创建主页面和模块页面容器
        self.home_widget = QWidget()
        self.home_layout = QVBoxLayout(self.home_widget)
        self.main_layout.addWidget(self.home_widget)
        
        self.module_widget = QWidget()
        self.module_layout = QVBoxLayout(self.module_widget)
        self.module_widget.hide()
        self.main_layout.addWidget(self.module_widget)
        
        # 初始化模块 - 使用正确的类名
        self.geometry_module = GeometryModuleRefactored()
        self.calculator_module = CalculatorModule()
        
        self.module_layout.addWidget(self.geometry_module)
        self.module_layout.addWidget(self.calculator_module)
        self.geometry_module.hide()
        self.calculator_module.hide()
        
        # 创建主页面按钮
        self._create_home_buttons()

    def _create_home_buttons(self):
        """创建主页面的大按钮"""
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
        """显示主页面"""
        self.module_widget.hide()
        self.home_widget.show()
        
    def show_geometry_module(self):
        """显示几何模块"""
        self.home_widget.hide()
        self.module_widget.show()
        self.calculator_module.hide_module()
        self.geometry_module.show_module()
        
    def show_calculator_module(self):
        """显示计算器模块"""
        self.home_widget.hide()
        self.module_widget.show()
        self.geometry_module.hide_module()
        self.calculator_module.show_module()
        
    def back_to_home(self):
        """返回主页面"""
        self.module_widget.hide()
        self.home_widget.show()

if __name__ == "__main__":
    try:
        # 添加更多错误检查
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "modules")):
            print("Erreur: Le répertoire modules n'existe pas")
            sys.exit(1)
            
        # 检查必要模块文件
        required_modules = [
            "ui_components_pyqt.py", 
            "geometry_module_refactored.py",  # 更新为新模块名称
            "calculator_module_pyqt.py"
        ]
        
        for module in required_modules:
            if not os.path.exists(os.path.join(os.path.dirname(__file__), "modules", module)):
                print(f"Erreur: Fichier de module requis manquant {module}")
                sys.exit(1)
                
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application: {str(e)}")
        import traceback
        traceback.print_exc()  # 打印详细错误信息
        sys.exit(1)