import tkinter as tk
from tkinter import messagebox


def draw_point(canvas, x, y):
    canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")


def draw_line(canvas, x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2, fill="blue")


def draw_circle(canvas, x, y, r):
    canvas.create_oval(x-r, y-r, x+r, y+r, outline="green")


def calculate(operation, num1, num2):
    try:
        num1, num2 = float(num1), float(num2)
        if operation == "+":
            return num1 + num2
        elif operation == "-":
            return num1 - num2
        elif operation == "*":
            return num1 * num2
        elif operation == "/":
            return num1 / num2 if num2 != 0 else "Erreur : Division par zéro"
    except ValueError:
        return "Erreur : Entrée non valide"


# 创建界面
root = tk.Tk()
root.title("Logiciel de Géométrie & Calcul pour Enfants")

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

# 按钮和输入框
btn_point = tk.Button(root, text="Dessiner un point", command=lambda: draw_point(canvas, 300, 200))
btn_point.pack(side=tk.LEFT)

btn_line = tk.Button(root, text="Dessiner une ligne", command=lambda: draw_line(canvas, 100, 100, 300, 300))
btn_line.pack(side=tk.LEFT)

btn_circle = tk.Button(root, text="Dessiner un cercle", command=lambda: draw_circle(canvas, 400, 200, 50))
btn_circle.pack(side=tk.LEFT)


# 简单计算器
entry_num1 = tk.Entry(root)
entry_num1.pack(side=tk.LEFT)

entry_op = tk.Entry(root, width=3)
entry_op.pack(side=tk.LEFT)

entry_num2 = tk.Entry(root)
entry_num2.pack(side=tk.LEFT)

btn_calc = tk.Button(root, text="Calculer", command=lambda: messagebox.showinfo("Résultat", calculate(entry_op.get(), entry_num1.get(), entry_num2.get())))
btn_calc.pack(side=tk.LEFT)


root.mainloop()


# 这样，你就可以绘制基本几何图形，并用简单的加减乘除进行运算！
# 后续可以加入眼动追踪或更复杂的交互逻辑！ 🚀
