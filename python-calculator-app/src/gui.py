import os
import sys

# 将项目根目录添加到 sys.path，方便模块导入
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from tkinter import Label, Entry, StringVar, font, Text
from ttkbootstrap import Window, Button, Frame  # 第三方库
from src.calculator import Calculator           # 项目内模块
from src.utils import validate_number, format_result

class YI_ZHONG_JI_SUAN_QI:
    def __init__(self, master):
        """
        初始化 YI_ZHONG_JI_SUAN_QI 类的实例。
        参数:
            master (Tk): 主窗口对象。
        """
        self.master = master
        master.title("计算器_v1")
        master.configure(bg="#f0f0f0")  # 设置窗口背景色
        master.geometry("600x600")  # 设置窗口大小
        master.resizable(False, False)  # 禁止调整窗口大小
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ico', 'output.ico'))
        master.iconbitmap(icon_path)  # 设置窗口图标
        master.wm_attributes("-topmost", True)  # 窗口置顶

        # 设置统一字体
        self.default_font = font.Font(family="微软雅黑", size=14)

        # 初始化计算器实例
        self.calculator = Calculator()
        self.result_var = StringVar(self.master)

        self.create_widgets()

    def create_widgets(self):
        # 记录框
        self.log_text = Text(self.master, height=3, font=self.default_font, state='disabled',
                             bg="#f8f8f8", bd=0, highlightthickness=0)
        self.log_text.pack(fill='x', padx=20, pady=(10, 0), ipady=3)

        # 输入框
        self.entry = Entry(self.master, background="lightblue", width=30, font=self.default_font,
                           textvariable=self.result_var, justify='center')
        self.entry.pack(fill='x', padx=20, pady=20)


        # 数字按钮区域
        num_frame = Frame(self.master)
        num_frame.pack(side='top', fill='both', expand=True,padx=20, pady=(0, 20))

        btn_texts = [
            ('C'),
            ('1/x', 'x^2', '√', '÷'),
            ('7', '8', '9', '×'),
            ('4', '5', '6', '-'),
            ('1', '2', '3', '+'),
            ('±', '0', '.','='),
        ]
        for r, row in enumerate(btn_texts):
            for c, text in enumerate(row):
                if text:  # 只创建非空按钮
                    if text in ('+', '-', '×', '÷'):
                        cmd = {
                            '+': self.add,
                            '-': self.subtract,
                            '×': self.multiply,
                            '÷': self.divide
                        }[text]
                        btn = Button(
                            num_frame,
                            text=text,
                            width=6,
                            bootstyle="secondary",
                            command=cmd
                        )
                    elif text == '=':
                        btn = Button(
                            num_frame,
                            text=text,
                            width=6,
                            bootstyle="success",  # 让等于号为绿色
                            command=self.equal
                        )
                    else:
                        btn = Button(
                            num_frame, 
                            text=text, 
                            width=6, 
                            bootstyle="secondary", 
                            command=lambda t=text: self.on_number_button(t)
                        )                        pip show notebook                        pip show notebook
                    btn.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
        for i in range(4):
            num_frame.columnconfigure(i, weight=1)
        for i in range(len(btn_texts)):
            num_frame.rowconfigure(i, weight=1)  # 行数要和btn_texts一致


    def on_number_button(self, text):
        if text == '清空':
            self.entry.delete(0, 'end')
        else:
            self.entry.insert('end', text)

    def log(self, msg):
        self.log_text.config(state='normal')
        self.log_text.insert('end', msg + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def add(self):
        self.log(f"输入：{self.entry.get()}  操作：+")
        self.calculate(self.calculator.add)

    def subtract(self):
        self.log(f"输入：{self.entry.get()}  操作：-")
        self.calculate(self.calculator.subtract)

    def multiply(self):
        self.log(f"输入：{self.entry.get()}  操作：×")
        self.calculate(self.calculator.multiply)

    def divide(self):
        self.log(f"输入：{self.entry.get()}  操作：÷")
        self.calculate(self.calculator.divide)

    def on_equal(self):
        expr = self.result_var.get()
        try:
            result = self.calculator.calculate(expr)
            self.result_var.set(result)
            # 添加计算过程到记录框
            self.log_text.config(state='normal')
            self.log_text.insert('end', f"{expr} = {result}\n")
            self.log_text.see('end')  # 滚动到最后
            self.log_text.config(state='disabled')
        except Exception as e:
            self.result_var.set("错误")

    def _get_op_symbol(self):
        # 辅助方法，返回当前运算符号
        if hasattr(self, 'pending_operation'):
            if self.pending_operation == self.calculator.add:
                return '+'
            elif self.pending_operation == self.calculator.subtract:
                return '-'
            elif self.pending_operation == self.calculator.multiply:
                return '×'
            elif self.pending_operation == self.calculator.divide:
                return '÷'
        return '?'



if __name__ == "__main__":
    root = Window(themename="cosmo")  # 使用ttkbootstrap的Window和主题
    root.geometry("600x600")
    root.configure(bg="#FFFFFF")
    # root.iconbitmap("calculator.ico")  # 可选

    calculator_gui = YI_ZHONG_JI_SUAN_QI(root)
    root.mainloop()

