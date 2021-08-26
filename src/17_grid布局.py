#!/usr/bin/env python3
"""
@file 17_grid布局.py
@brief grid布局
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
from tkinter import *


class GridApplication(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__master = master
        self.pack()

    def createWidget(self):
        Label(self, text='用户名').grid(column=0, row=0)
        self.entry1 = Entry(self)
        self.entry1.grid(column=1, row=0)

        Label(self, text='密码').grid(column=0, row=1)
        self.entry2 = Entry(self, show='*')
        self.entry2.grid(column=1, row=1)

        Button(self, text='登录').grid(column=1, row=2, sticky=EW)
        Button(self, text='退出', command=self.__master.destroy).grid(
            column=2, row=2, sticky=E
        )


# 计算器布局
class Calculator(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__master = master
        self.pack()

    def createWidget(self):
        # 计算式显示框
        Text(self, height=3).grid(column=0, row=0, columnspan=4, sticky=EW)
        Button(self, text='7').grid(column=0, row=1, sticky=EW)
        Button(self, text='8').grid(column=1, row=1, sticky=EW)
        Button(self, text='9').grid(column=2, row=1, sticky=EW)
        Button(self, text='÷').grid(column=3, row=1, sticky=EW)
        Button(self, text='4').grid(column=0, row=2, sticky=EW)
        Button(self, text='5').grid(column=1, row=2, sticky=EW)
        Button(self, text='6').grid(column=2, row=2, sticky=EW)
        Button(self, text='×').grid(column=3, row=2, sticky=EW)
        Button(self, text='1').grid(column=0, row=3, sticky=EW)
        Button(self, text='2').grid(column=1, row=3, sticky=EW)
        Button(self, text='3').grid(column=2, row=3, sticky=EW)
        Button(self, text='-').grid(column=3, row=3, sticky=EW)
        Button(self, text='0').grid(column=0, row=4, sticky=EW)
        Button(self, text='.').grid(column=1, row=4, sticky=EW)
        Button(self, text='=').grid(column=2, row=4, sticky=EW)
        Button(self, text='+').grid(column=3, row=4, sticky=EW)


if __name__ == '__main__':
    grid = Tk()
    grid.geometry('300x100+300+400')
    grid.title('grid布局演示')
    gridApp = GridApplication(grid)
    gridApp.createWidget()

    calc = Tk()
    calc.geometry('700x200+700+400')
    calc.title('计算器布局')
    calcApp = Calculator(calc)
    calcApp.createWidget()

    mainloop()
