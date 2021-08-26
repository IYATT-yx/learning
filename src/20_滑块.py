#!/usr/bin/env python3
"""
@file 20_滑块.py
@brief 滑块
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
from tkinter import *


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__master = master
        self.pack()

    def showVar(self, value):
        print('滑块值：', value)

    def createWidgets(self):
        Scale(
            self.__master,
            from_=0,
            to=50,
            length=500,
            tickinterval=5,
            orient=HORIZONTAL,
            command=self.showVar,
        ).pack()


if __name__ == '__main__':
    root = Tk()
    root.geometry('600x100+400+400')
    root.title('滑块')
    app = Application(root)
    app.createWidgets()
    root.mainloop()
