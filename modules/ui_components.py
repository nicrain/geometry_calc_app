import tkinter as tk

class MetroButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        # 保存原始颜色
        self._original_color = kwargs.get('bg', '#ffffff')
        
        # Metro风格默认配置
        default_config = {
            'width': 15,
            'height': 6,
            'font': ('Arial', 14),
            'borderwidth': 0,
            'relief': 'flat',
            'cursor': 'hand2'
        }
        # 更新配置
        default_config.update(kwargs)
        super().__init__(master, **default_config)
        
        # 绑定悬停效果
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        
    def _on_enter(self, e):
        # 存储当前颜色
        current_color = self['bg']
        self._original_color = current_color
        # 使颜色变亮
        self.config(bg=self._lighten_color(current_color))
        
    def _on_leave(self, e):
        # 恢复原始颜色
        self.config(bg=self._original_color)
        
    def _lighten_color(self, color):
        # 简单的颜色变亮效果
        if color == "#00A300":  # 绿色
            return "#45FF45"
        elif color == "#2D89EF":  # 蓝色
            return "#45B6FF"
        return color

    def set_active(self, is_active=True):
        if is_active:
            self.config(bg=self._lighten_color(self._original_color))
        else:
            self.config(bg=self._original_color)
