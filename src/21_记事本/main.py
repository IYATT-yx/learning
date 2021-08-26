#!/usr/bin/env python3
"""
@file main.py
@brief 执行入口
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
from tkinter import *
import os
import Notepad


def main():
    root = Tk()
    root.geometry('600x400+300+300')
    root.title('记事本')

    # 设置图标
    absPath = os.path.dirname(os.path.abspath(__file__))
    icon = PhotoImage(file=absPath + '/notepad.png')
    root.iconphoto(False, icon)

    # 记事本界面实例化
    app = Notepad.Notepad(root)
    app.createWidgets()

    root.mainloop()


if __name__ == '__main__':
    main()
