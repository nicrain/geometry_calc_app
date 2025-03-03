import tkinter as tk
from math import pi, cos, sin

class MetroButton(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        # 提取自定义属性
        self.text = kwargs.pop('text', '')
        self._bg_color = kwargs.pop('bg', '#ffffff')
        self._fg_color = kwargs.pop('fg', '#000000')
        self.command = kwargs.pop('command', None)
        self._font = kwargs.pop('font', ('Arial', 14, 'bold'))
        
        # 尺寸设置
        width = kwargs.pop('width', 120)
        height = kwargs.pop('height', 36)
        
        # Canvas配置
        canvas_config = {
            'height': height,
            'width': width,
            'highlightthickness': 0,
            'bg': '#ffffff'
        }
        
        valid_keys = ['height', 'width', 'highlightthickness', 'bg']
        kwargs = {k: v for k, v in kwargs.items() if k in valid_keys}
        canvas_config.update(kwargs)
        
        super().__init__(master, **canvas_config)
        self.bind('<Configure>', self._on_resize)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
        self.bind('<ButtonRelease-1>', self._on_release)
        
        self._draw()
    
    def _on_resize(self, event):
        # 当大小改变时重新绘制
        self._draw()
        
    def _draw(self, state='normal'):
        self.delete('all')
        width = self.winfo_width()
        height = self.winfo_height()
        
        if state == 'hover':
            bg_color = self._lighten_color(self._bg_color)
        elif state == 'pressed':
            bg_color = self._darken_color(self._bg_color)
        else:
            bg_color = self._bg_color
            
        radius = min(height/6, 10)
        offset = 1
        
        # 阴影
        self.create_rectangle(
            offset, offset, width, height,
            fill='#444444', outline='#444444'
        )
        
        # 主体按钮
        self.create_rounded_rectangle(
            0, 0, width-offset, height-offset,
            radius, 
            fill=bg_color,
            outline=bg_color
        )
        
        # 文本
        self.create_text(
            width/2 - offset/2,
            height/2 - offset/2,
            text=self.text,
            fill=self._fg_color,
            font=self._font,
            tags='text'
        )
        
    def grid(self, **kwargs):
        if 'sticky' in kwargs:
            kwargs['sticky'] = 'nsew'  # 确保按钮填满网格
        super().grid(**kwargs)
        
    def pack(self, **kwargs):
        if 'fill' in kwargs:
            kwargs['fill'] = 'both'  # 确保按钮填满空间
        super().pack(**kwargs)

    def _on_enter(self, event):
        self._draw('hover')
        
    def _on_leave(self, event):
        self._draw('normal')
        
    def _on_click(self, event):
        self._draw('pressed')
        
    def _on_release(self, event):
        self._draw('hover')
        if self.command:
            self.command()
            
    def _lighten_color(self, color):
        color_map = {
            "#1B5E20": "#2E7D32",  # 深墨绿色 -> 浅一点的绿色
            "#1A237E": "#283593",  # 深靛蓝色 -> 浅一点的靛蓝
            "#311B92": "#4527A0",  # 深紫色 -> 浅一点的紫色
            "#B71C1C": "#D32F2F"   # 深红色 -> 浅一点的红色
        }
        return color_map.get(color, color)

    def _darken_color(self, color):
        # 加深颜色效果
        color_map = {
            "#1B5E20": "#0F4C12",  # 深墨绿色 -> 更深的绿色
            "#1A237E": "#0D1642",  # 深靛蓝色 -> 更深的蓝色
            "#311B92": "#1A0F4C",  # 深紫色 -> 更深的紫色
            "#B71C1C": "#7F1414"   # 深红色 -> 更深的红色
        }
        return color_map.get(color, color)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,  # 左上角开始
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def set_active(self, is_active=True):
        if is_active:
            self._draw('hover')
        else:
            self._draw('normal')

    def configure(self, **kwargs):
        if 'bg' in kwargs:
            self._bg_color = kwargs.pop('bg')
            self._draw()
        if 'fg' in kwargs:
            self._fg_color = kwargs.pop('fg')
            self._draw()
        super().configure(**kwargs)
