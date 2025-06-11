import sys
import os

# 添加模块路径到sys.path
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from tkinter import Label, Entry, StringVar, font, Text  # 增加Text
from src.calculator import Calculator
from src.utils import validate_number, format_result
from ttkbootstrap import Window, Button, Frame  # 用ttkbootstrap的控件


class YI_ZHONG_JI_SUAN_QI:
    def __init__(self, master):
        """
        初始化YI_ZHONG_JI_SUAN_QI类的实例。
        参数:
        master (Tk): 主窗口对象。
        """
        self.master = master
        master.title("计算器_v1")
        master.configure(bg="#f0f0f0")  # 设置窗口背景色
        # master.geometry("600x600")  # 设置窗口大小
        # master.resizable(False, False)  # 禁止调整窗口大小
        master.iconbitmap("python-calculator-app\src\ico\output.ico")  # 设置窗口图标
        master.wm_attributes("-topmost", True)  # 窗口置顶

        # 设置统一字体
        self.default_font = font.Font(family="微软雅黑", size=14)

        self.calculator = Calculator()
        self.result_var = StringVar()

        self.create_widgets()

    def create_widgets(self):
        # 记录框
        self.log_text = Text(self.master, height=8, font=self.default_font, state='disabled', bg="#f8f8f8")
        self.log_text.pack(fill='x', padx=20, pady=(10, 0))

        # 输入框
        self.entry = Entry(self.master, background="lightblue", width=30, font=self.default_font,
                           textvariable=self.result_var, justify='center')
        self.entry.pack(fill='x', padx=20, pady=20)


        # 数字按钮区域
        num_frame = Frame(self.master)
        num_frame.pack(side='top', fill='both', expand=True,padx=20, pady=(0, 20))

        btn_texts = [
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
                        )
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

    def equal(self):
        # 只在有待运算时才执行
        if hasattr(self, 'first_number') and hasattr(self, 'pending_operation'):
            input_text = self.entry.get().strip()
            if not validate_number(input_text):
                self.entry.delete(0, 'end')
                self.entry.insert(0, "请输入第二个数字。")
                return
            second_number = float(input_text)
            try:
                result = self.pending_operation(self.first_number, second_number)
                self.log(f"{self.first_number} {self._get_op_symbol()} {second_number} = {result}")
                self.entry.delete(0, 'end')
                self.entry.insert(0, str(result))
            except ValueError as e:
                self.entry.delete(0, 'end')
                self.entry.insert(0, str(e))
            del self.first_number
            del self.pending_operation

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

    def calculate(self, operation):
        if not hasattr(self, 'first_number'):
            input_text = self.entry.get().strip()
            if not validate_number(input_text):
                self.entry.delete(0, 'end')
                self.entry.insert(0, "请输入第一个数字。")
                return
            self.first_number = float(input_text)
            self.entry.delete(0, 'end')
            self.entry.insert(0, "请输入第二个数字，然后再次点击运算按钮。")
            self.pending_operation = operation
            return

        input_text = self.entry.get().strip()
        if not validate_number(input_text):
            self.entry.delete(0, 'end')
            self.entry.insert(0, "请输入第二个数字。")
            return
        second_number = float(input_text)
        try:
            result = self.pending_operation(self.first_number, second_number)
            self.entry.delete(0, 'end')
            self.entry.insert(0, str(result))
        except ValueError as e:
            self.entry.delete(0, 'end')
            self.entry.insert(0, str(e))
        del self.first_number
        del self.pending_operation

if __name__ == "__main__":
    root = Window(themename="cosmo")  # 使用ttkbootstrap的Window和主题
    root.geometry("600x600")
    root.configure(bg="#FFFFFF")
    # root.iconbitmap("calculator.ico")  # 可选

    calculator_gui = YI_ZHONG_JI_SUAN_QI(root)
    root.mainloop()

