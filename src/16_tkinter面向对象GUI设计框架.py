#!/usr/bin/env python3
"""
@file 16_tkinter面向对象GUI设计框架.py
@brief tkinter面向对象GUI设计框架
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
from tkinter import *
import tkinter.messagebox as messagebox


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)  # 父类
        self.__master = master
        self.pack()

        self.createWidget()

    def createWidget(self):
        # 标签组件
        self.label = Label(
            self, text='这是一个标签', width=10, height=1, bg='red', fg='black'
        )
        self.label.pack()

        # 按钮组件
        self.btn1 = Button(self)
        self.btn1['text'] = '按钮'
        self.btn1['command'] = self.doWork
        self.btn1['anchor'] = NE  # 文字在按钮中的位置 north east
        self.btn1.config(width=5, height=5)
        self.btn1.pack()

        # 单行输入框
        self.entryVar = StringVar()
        self.entry = Entry(self, textvariable=self.entryVar)
        self.entry.pack()

        self.btn2 = Button(self, text='查看单行框', command=self.viewEntry)
        self.btn2.pack()

        # 多行输入框
        self.text = Text(self, width=40, height=5, bg='gray')
        self.text.pack()

        self.btn3 = Button(self, text='查看多行框', command=self.viewText)
        self.btn3.pack()

        # 单选框
        self.radioVar = StringVar()
        self.radioVar.set('单选一')  # 默认初始选中
        self.radio1 = Radiobutton(self, text='单选一', value='单选一', variable=self.radioVar)
        self.radio2 = Radiobutton(self, text='单选二', value='单选二', variable=self.radioVar)
        self.radio1.pack(side='left')
        self.radio2.pack(side='left')

        # 多选框
        self.checkVar1 = IntVar()
        self.checkVar2 = IntVar()
        self.check1 = Checkbutton(
            self, text='选项一', variable=self.checkVar1, onvalue=1, offvalue=0
        )
        self.check2 = Checkbutton(
            self, text='选项二', variable=self.checkVar2, onvalue=1, offvalue=0
        )
        self.check1.pack(side='right')
        self.check2.pack(side='right')

        # 画布
        self.canvas = Canvas(self, width=100, height=100, bg='green')
        self.canvas.pack()
        self.canvas.create_line(10, 10, 30, 30, 50, 50, 70, 10, 90, 90)
        self.canvas.create_rectangle(20, 20, 80, 90)

        # 退出按钮
        self.btnQuit = Button(self, text='退出', command=self.__master.destroy)
        self.btnQuit.pack()

    def doWork(self):
        messagebox.showinfo('提示', '按钮被点击')

    # 查看你单行输入框的值
    def viewEntry(self):
        self.text.insert(INSERT, self.entryVar.get())
        # messagebox.showinfo('查看单行框', self.entryVar.get())
        messagebox.showinfo('查看单行框', self.entry.get())

    def viewText(self):
        messagebox.showinfo('查看多行框', self.text.get(1.0, END))


if __name__ == '__main__':
    root = Tk()
    root.geometry('400x500+300+200')  # 400x200 左距300 上距200
    root.title('面向对象设计GUI框架')
    app = Application(master=root)

    root.mainloop()
