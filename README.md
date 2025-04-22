# 🧠 Logiciel de Géométrie & Calcul pour Enfants

一个面向小学阶段的几何与计算软件，支持眼动控制和实时反馈。前期实现基础功能，后期无缝升级眼动追踪！

## 📦 功能模块

- **几何绘图**：绘制点、线段、圆、三角形，支持基础属性标注。
- **运算工具**：执行基础加减乘除，支持分数运算。
- **眼动追踪**：预留接口，支持未来接入 MediaPipe 或 Tobii Eye Tracker 5。
- **交互反馈**：成功/错误消息框，支持语音反馈（未来扩展）。
- **工具库**：包括数值检查、几何计算等常用工具函数。

## 🚀 快速启动

1. 克隆仓库：

```bash
git clone https://github.com/nicrain/geometry_calc_app.git
cd geometry_calc_app
```

2. 安装依赖：

```bash
# 创建虚拟环境（可选但推荐）
python -m venv venv

# 在 macOS/Linux 上激活虚拟环境
source venv/bin/activate

# 在 Windows 上激活虚拟环境
# venv\Scripts\activate

# 安装所有依赖
pip install -r requirements.txt
```

3. 运行程序：

```bash
# 基础运行
python main.py

# 调试模式（显示更详细的日志）
python main.py --debug

# 指定语言（如果支持）
python main.py --lang fr
```

## 💻 详细命令说明

### 开发者工具

```bash
# 运行所有测试
pytest

# 代码格式化
black .

# 检查代码质量
flake8

# 安装开发依赖
pip install -r requirements-dev.txt
```

### 可选参数

程序支持以下命令行参数：

```bash
# 指定窗口大小
python main.py --width 1280 --height 800

# 禁用动画效果（性能较低的设备）
python main.py --no-animations

# 帮助信息
python main.py --help
```

## 📂 项目结构

```
📂 geometry_calc_app/
├── 📂 modules/                    # 功能模块目录
│   ├── geometry_module_pyqt.py    # 几何绘图模块
│   ├── calculator_module_pyqt.py  # 运算模块
│   ├── ui_components_pyqt.py      # UI组件模块
│   └── eye_tracker_module.py      # 眼动追踪模块（预留接口）
├── main.py                        # 主程序入口
├── requirements.txt               # 依赖包列表
└── README.md                      # 项目说明文件
```

## 🛠️ 未来扩展

- **更复杂的图形**：支持梯形、多边形、面积/周长计算。
- **眼动追踪集成**：支持 MediaPipe 眼控、Tobii Eye Tracker 5。
- **多语言支持**：添加英语/法语界面切换。

## 📄 许可证

MIT License