# 🧠 儿童几何与计算学习软件

一个面向小学阶段儿童的几何与计算学习软件，采用PyQt6开发，支持眼动控制和实时反馈。为儿童提供友好的交互界面，帮助他们掌握基础几何知识和数学计算技能。

## ✨ 项目亮点

- **直观交互**: 精心设计的界面适合儿童使用，色彩丰富、操作简单
- **教育价值**: 通过视觉化方式帮助理解抽象数学概念
- **多模态输入**: 支持传统鼠标/键盘控制，预留眼动追踪接口
- **即时反馈**: 操作结果实时呈现，强化学习效果
- **扩展性强**: 模块化设计，便于未来功能扩展

## 📦 功能模块

### 几何绘图模块
- 绘制基础几何图形：点、线段、圆、三角形
- 测量图形属性：长度、角度、面积
- 支持图形变换：旋转、缩放、移动

### 计算工具模块
- 基础四则运算：加、减、乘、除
- 分数运算支持
- 直观的计算过程展示

### 眼动追踪接口（预留）
- 支持MediaPipe眼动追踪集成
- 兼容Tobii Eye Tracker 5等专业设备
- 提供可定制的眼控交互模式

### 反馈系统
- 视觉反馈：颜色变化、动画效果
- 声音反馈：操作提示音
- 成功/错误消息提示框

## 🛠️ 技术特性

- **前端框架**: PyQt6
- **图形处理**: OpenCV、Pillow
- **数学计算**: NumPy
- **眼动技术**: MediaPipe（预留接口）
- **语音反馈**: pyttsx3

## 🚀 快速开始

### 系统要求
- Python 3.8+
- 建议使用虚拟环境
- 支持Windows、macOS和Linux

### 安装步骤

1. 克隆仓库：

```bash
git clone https://github.com/nicrain/geometry_calc_app.git
cd geometry_calc_app
```

2. 创建并激活虚拟环境（推荐）：

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境 (macOS/Linux)
source .venv/bin/activate

# 激活虚拟环境 (Windows)
# venv\Scripts\activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 运行程序：

```bash
python main.py
```

### 运行选项

程序支持以下命令行参数：

```bash
# 基础运行
python main.py

# 调试模式
python main.py --debug

# 指定窗口大小
python main.py --width 1280 --height 800

# 禁用动画效果（适用于低性能设备）
python main.py --no-animations

# 指定语言（如支持）
python main.py --lang fr

# 查看帮助信息
python main.py --help
```

## 💻 开发指南

### 开发环境设置

```bash
# 安装所有开发依赖
pip install -r requirements.txt

# 代码格式化
black .

# 检查代码质量
flake8

# 运行测试
pytest
```

### 项目结构

```
📂 geometry_calc_app/
├── 📂 modules/                    # 功能模块目录
│   ├── geometry_module_pyqt.py    # 几何绘图模块
│   ├── calculator_module_pyqt.py  # 运算模块
│   ├── ui_components_pyqt.py      # UI组件模块
│   └── eye_tracker_module.py      # 眼动追踪模块（预留接口）
├── 📂 tests/                      # 测试目录
│   ├── test_geometry.py           # 几何模块测试
│   └── test_calculator.py         # 计算器模块测试
├── 📂 docs/                       # 文档目录
│   └── 📂 images/                 # 截图和图示
├── 📂 resources/                  # 资源文件（图标、音效等）
├── main.py                        # 主程序入口
├── requirements.txt               # 依赖包列表
└── README.md                      # 项目说明文件
```


## 🔮 未来规划

- **更多几何图形**: 支持梯形、多边形等复杂图形
- **高级计算功能**: 方程求解、简易统计功能
- **眼动追踪集成**: 完整支持眼控操作
- **多语言支持**: 中文、英语、法语界面切换
- **教学模式**: 添加引导式学习功能
- **游戏化元素**: 融入数学挑战任务和奖励机制

## 📄 许可证

MIT License

---

<p align="center">
    <i>为儿童打造的数学学习之旅</i>
</p>