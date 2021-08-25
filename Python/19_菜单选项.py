#!/usr/bin/env python3
"""
@file 19_菜单选项.py
@brief 菜单选项
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

    def createWidgets(self):
        var = StringVar()
        var.set('第一个选项')
        self.__om = OptionMenu(self.__master, var, '第一个选项', '第二个选项', '第三个选项')
        self.__om['width'] = 50
        self.__om.pack()


if __name__ == '__main__':
    root = Tk()
    root.geometry('300x100+400+400')
    root.title('选项菜单')
    app = Application(root)
    app.createWidgets()
    root.mainloop()
