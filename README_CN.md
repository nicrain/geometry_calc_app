# 🧠 儿童几何与计算学习软件

一个面向小学阶段儿童的几何与计算学习软件，采用PyQt6开发，支持眼动控制和实时反馈。为儿童提供友好的交互界面，帮助他们掌握基础几何知识和数学计算技能。

## ✨ 项目亮点

- **直观交互**: 精心设计的法语界面适合儿童使用，色彩丰富、操作简单
- **教育价值**: 通过视觉化方式帮助理解抽象数学概念
- **多模态输入**: 支持传统鼠标/键盘控制，预留眼动追踪接口
- **即时反馈**: 操作结果实时呈现，强化学习效果
- **扩展性强**: 模块化设计，便于未来功能扩展
- **Metro风格**: 现代化的界面设计，清晰的视觉层次

## 📦 功能模块

### 几何绘图模块 (Module de Géométrie)
- 绘制基础几何图形：点(Point)、线段(Ligne)、圆(Cercle)、三角形(Triangle)、矩形(Rectangle)
- 测量图形属性：长度、角度、面积
- 支持图形变换：旋转、缩放、移动
- 实时绘图和交互式编辑

### 计算工具模块 (Calculatrice)
- 基础四则运算：加、减、乘、除
- 分数运算支持
- 直观的计算过程展示
- 友好的按钮式界面

### 眼动追踪接口（预留）
- 支持MediaPipe眼动追踪集成
- 兼容Tobii Eye Tracker 5等专业设备
- 提供可定制的眼控交互模式

### 反馈系统
- 视觉反馈：颜色变化、动画效果
- 声音反馈：操作提示音（pyttsx3）
- 成功/错误消息提示框

## 🛠️ 技术特性

### 当前使用的依赖
- **PyQt6 (≥6.5.0)** - 现代化的跨平台GUI框架，项目核心依赖
- **Python内置模块** - math、pathlib等，用于基础数学计算和文件操作

### 开发工具依赖
- **pytest (≥7.3.1)** - 单元测试框架
- **pytest-qt (≥4.2.0)** - PyQt6应用程序的测试支持
- **black (≥23.3.0)** - 代码格式化工具
- **flake8 (≥6.0.0)** - 代码质量检查工具
- **isort (≥5.12.0)** - 导入语句排序工具
- **pyinstaller (≥5.9.0)** - 创建独立可执行文件

### 预留功能依赖（暂未使用）
以下依赖已在requirements.txt中注释，用于未来功能扩展：

#### 高级数学计算
- **NumPy (≥1.24.0)** - 用于复杂数学运算和矩阵计算
  - *当前状态*：使用Python内置math模块
  - *计划用途*：几何变换、统计分析、高级数学函数

#### 眼动追踪技术
- **MediaPipe (≥0.10.0)** - Google的机器学习视觉库
  - *当前状态*：预留接口，未实现
  - *计划用途*：实时眼动追踪、眼控交互
- **OpenCV (≥4.7.0)** - 计算机视觉库
  - *当前状态*：未使用
  - *计划用途*：图像处理、眼动数据预处理

#### 图像处理功能
- **Pillow (≥9.5.0)** - Python图像处理库
  - *当前状态*：未使用
  - *计划用途*：图像编辑、格式转换、图形导出

#### 语音反馈系统
- **pyttsx3 (≥2.90)** - 文本转语音引擎
  - *当前状态*：预留功能
  - *计划用途*：语音提示、操作反馈、辅助学习

#### 数据可视化
- **Matplotlib (≥3.7.1)** - 科学计算可视化库
  - *当前状态*：未使用
  - *计划用途*：统计图表、学习进度可视化、数据分析

#### 国际化支持
- **python-i18n (≥0.3.9)** - 多语言支持库
  - *当前状态*：硬编码法语界面
  - *计划用途*：动态语言切换、多语言界面
- **pygettext (≥2.7)** - 国际化工具
  - *当前状态*：未使用
  - *计划用途*：翻译文件管理、本地化工具

## 🚀 快速开始

### 系统要求
- Python 3.8+ （推荐 3.9+）
- 操作系统：Windows 10+、macOS 10.14+、Linux（Ubuntu 18.04+）
- 内存：建议 4GB+ RAM
- 显卡：支持OpenGL 2.0+（用于图形渲染）

### 安装步骤

1. **克隆仓库**：

```bash
git clone https://github.com/nicrain/geometry_calc_app.git
cd geometry_calc_app
```

2. **创建并激活虚拟环境**（强烈推荐）：

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

3. **安装依赖**：

```bash
# 基础安装（仅安装当前使用的依赖）
pip install -r requirements.txt

# 验证安装
python -c "import PyQt6; print('PyQt6 安装成功')"
```

4. **可选：启用预留功能**

如需启用特定的预留功能，请编辑requirements.txt文件，取消注释相应的依赖行：

```bash
# 启用眼动追踪功能
pip install mediapipe>=0.10.0 opencv-python>=4.7.0

# 启用语音反馈
pip install pyttsx3>=2.90

# 启用高级数学计算
pip install numpy>=1.24.0

# 启用数据可视化
pip install matplotlib>=3.7.1

# 启用多语言支持
pip install python-i18n>=0.3.9
```

5. **运行程序**：

```bash
python main.py
```

### 常见问题解决

**Q: 出现 "Impossible d'importer les modules PyQt6" 错误**
```bash
# 解决方案：重新安装PyQt6
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PyQt6>=6.5.0
```

**Q: 模块导入失败**
```bash
# 确保在正确的目录中运行
ls modules/  # 应该看到 .py 文件
python -c "import sys; print(sys.path)"
```

**Q: 想要启用眼动追踪功能**
```bash
# 取消注释requirements.txt中的相关行，然后安装
pip install mediapipe>=0.10.0 opencv-python>=4.7.0
# 注意：此功能目前为预留接口，需要额外开发
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

## 🎯 使用指南

### 启动界面
- 应用程序启动后显示主菜单，包含两个大按钮
- **Géométrie（几何）**: 绿色按钮，进入几何绘图模块
- **Calculatrice（计算器）**: 蓝色按钮，进入计算工具模块

### 几何模块使用
1. 选择绘图工具（点、线、圆、三角形、矩形）
2. 在画布上点击或拖拽创建图形
3. 使用测量工具查看图形属性
4. 支持撤销/重做操作

### 计算器模块使用
1. 点击数字和运算符按钮
2. 实时显示计算过程
3. 支持连续运算和结果重用

## 💻 开发指南

### 开发环境设置

```bash
# 克隆并进入项目目录
git clone <repository-url>
cd geometry_calc_app

# 安装开发依赖
pip install -r requirements.txt

# 代码格式化
black .

# 代码质量检查
flake8 --max-line-length=88 --extend-ignore=E203

# 导入排序
isort .

# 运行测试
pytest tests/ -v
```

### 项目结构

```
📂 geometry_calc_app/
├── 📄 main.py                           # 🚀 主程序入口
├── 📄 requirements.txt                  # 📦 依赖包列表
├── 📄 README.md                         # 📖 项目说明文档
├── 📄 README_CN.md                      # 📖 中文详细文档
└── 📂 modules/                          # 🧩 功能模块目录
    ├── 📄 __init__.py                   # Python包标识文件
    ├── 📄 ui_components_pyqt.py         # 🎨 UI组件模块（按钮、基础组件）
    ├── 📄 geometry_module_refactored.py # 📐 几何绘图模块（重构版）
    ├── 📄 calculator_module_pyqt.py     # 🔢 计算器模块
    ├── 📄 eye_tracker_module.py         # 👁️ 眼动追踪模块（预留接口）
    ├── 📄 canvas.py                     # 🎨 绘图画布组件
    ├── 📄 shapes.py                     # 📋 形状定义和枚举
    ├── 📄 factories.py                  # 🏭 工厂类（处理器和面板）
    ├── 📂 shape_handlers/               # 🔧 形状处理器目录
    │   ├── 📄 __init__.py               # 基础处理器类
    │   ├── 📄 point_handler.py          # 点形状处理器
    │   ├── 📄 line_handler.py           # 线形状处理器
    │   ├── 📄 rectangle_handler.py      # 矩形处理器
    │   ├── 📄 circle_handler.py         # 圆形处理器
    │   └── 📄 triangle_handler.py       # 三角形处理器
    ├── 📂 property_panels/              # 🏷️ 属性面板目录
    │   ├── 📄 __init__.py               # 基础属性面板类
    │   ├── 📄 point_properties_panel.py # 点属性面板
    │   ├── 📄 line_properties_panel.py  # 线属性面板
    │   ├── 📄 rectangle_properties_panel.py # 矩形属性面板
    │   ├── 📄 circle_properties_panel.py # 圆形属性面板
    │   └── 📄 triangle_properties_panel.py # 三角形属性面板
    └── 📂 shapes/                       # 📐 形状定义目录
        ├── 📄 __init__.py               # 形状类型和枚举
        └── 📄 point.py                  # 点类专门定义
```

### 架构设计

```
┌─────────────────────────────────────────┐
│                MainApp                  │  ← 主应用程序类
│  ┌─────────────────────────────────────┐│
│  │           Home Widget               ││  ← 主页面容器
│  │  ┌─────────────┐ ┌─────────────────┐││
│  │  │ Géométrie   │ │ Calculatrice    │││  ← 功能入口按钮
│  │  │   Button    │ │     Button      │││
│  │  └─────────────┘ └─────────────────┘││
│  └─────────────────────────────────────┘│
│  ┌─────────────────────────────────────┐│
│  │          Module Widget              ││  ← 功能模块容器
│  │  ┌─────────────────────────────────┐││
│  │  │    GeometryModuleRefactored     │││  ← 几何模块
│  │  └─────────────────────────────────┘││
│  │  ┌─────────────────────────────────┐││
│  │  │      CalculatorModule           │││  ← 计算器模块
│  │  └─────────────────────────────────┘││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

### 编码规范

- **代码格式**: 使用 black 进行格式化
- **导入排序**: 使用 isort 排序导入语句
- **代码质量**: 使用 flake8 检查代码质量
- **文档字符串**: 所有公共方法必须包含docstring
- **类型提示**: 推荐使用类型提示提高代码可读性

### 贡献指南

1. Fork 项目仓库
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 提交 Pull Request

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定模块测试
pytest tests/test_geometry.py -v

# 运行测试并生成覆盖率报告
pytest --cov=modules tests/

# 运行GUI测试
pytest tests/test_ui_components.py::TestMetroButton -v
```

## 🔮 未来规划

### 短期目标（3个月内）
- [ ] 完成几何模块的图形编辑功能
- [ ] 添加计算器的高级运算功能
- [ ] 实现基础的声音反馈系统（启用pyttsx3）
- [ ] 完善单元测试覆盖率（目标80%+）

### 中期目标（6个月内）
- [ ] 集成MediaPipe眼动追踪功能
- [ ] 添加多语言支持（启用python-i18n，支持中文、英语、法语）
- [ ] 实现数据持久化（保存用户进度）
- [ ] 添加更多几何图形：梯形、多边形等
- [ ] 集成NumPy进行高级数学计算

### 长期目标（1年内）
- [ ] 开发教学模式和引导式学习
- [ ] 添加游戏化元素和奖励机制
- [ ] 支持网络协作功能
- [ ] 开发移动端版本（PyQt for Mobile）
- [ ] 集成AI辅助学习功能
- [ ] 添加数据可视化功能（启用Matplotlib）

## 📊 依赖管理说明

### 核心依赖（必需）
当前版本只需要安装PyQt6，所有其他功能都基于Python内置模块实现。

### 可选依赖（按需启用）
根据需要的功能，可以选择性安装预留依赖：

- **眼动追踪**: `mediapipe`, `opencv-python`
- **语音反馈**: `pyttsx3`
- **高级数学**: `numpy`
- **数据可视化**: `matplotlib`
- **多语言支持**: `python-i18n`, `pygettext`
- **图像处理**: `pillow`

### 开发依赖
用于代码质量保证和测试的工具已包含在requirements.txt中。

## 🐛 已知问题

- 在某些Linux发行版上可能需要额外安装Qt平台插件
- 眼动追踪功能目前为预留接口，需要额外开发
- 高DPI显示器上可能存在界面缩放问题
- 预留的NumPy、MediaPipe等依赖暂未集成到代码中

## 📞 支持与反馈

- **问题报告**: 请在GitHub Issues中提交
- **功能建议**: 欢迎提交Feature Request
- **开发交流**: 可以通过Discussions进行讨论

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢以下开源项目：
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - 强大的GUI框架
- [NumPy](https://numpy.org/) - 科学计算基础
- [OpenCV](https://opencv.org/) - 计算机视觉库
- [MediaPipe](https://mediapipe.dev/) - 机器学习解决方案

---

<p align="center">
    <i>🌟 为儿童打造的数学学习之旅 🌟</i><br>
    <sub>让学习变得有趣而富有成效</sub>
</p>