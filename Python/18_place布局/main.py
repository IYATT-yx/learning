#!/usr/bin/env python3
"""
@file main.py
@brief place布局
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
from tkinter import *
import os


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.__master = master
        self.pack()

    def createWidgets(self):
        # 获取代码的绝对路径，则无论运行路径如何，都能正确找到图片
        abspath = os.path.dirname(os.path.abspath(__file__))

        self.photo = [
            PhotoImage(file=abspath + '/resources/' + str(i) + '.png') for i in range(9)
        ]
        self.label = [Label(self.__master, image=self.photo[i]) for i in range(9)]

        for i in range(0, 9):
            self.label[i].place(x=30 + i * 30, y=120)

        # 事件 - 鼠标左键
        self.label[0].bind_class('Label', '<Button-1>', self.play)

    # 出牌
    def play(self, event):
        if event.widget.winfo_y() == 120:
            event.widget.place(y=90)
        else:
            event.widget.place(y=120)


if __name__ == '__main__':
    root = Tk()
    root.geometry('400x400+400+400')
    root.title('place布局 - 扑克牌')
    app = Application(root)
    app.createWidgets()
    root.mainloop()
