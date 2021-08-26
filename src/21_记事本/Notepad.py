"""
@file Notepad.py
@brief 记事本的具体实现
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.colorchooser import *


class Notepad(Frame):
    """
    记事本实现封装类
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.__master = master
        self.pack()

        self.__saveType = 'newFile'

        self.__master.protocol("WM_DELETE_WINDOW", self.__onClosing)

    def createWidgets(self):
        """
        创建窗口组件
        """

        # 主菜单栏
        self.__menubar = Menu(self.__master)
        self.__master.config(menu=self.__menubar)

        # 文件
        self.__fileMenu = Menu(self.__menubar)
        self.__menubar.add_cascade(label='文件', menu=self.__fileMenu)
        # 设置
        self.__setMenu = Menu(self.__master)
        self.__menubar.add_cascade(label='设置', menu=self.__setMenu)
        # 帮助
        self.__aboutMenu = Menu(self.__master)
        self.__menubar.add_cascade(label='帮助', menu=self.__aboutMenu)

        # 文件 - 子选项
        self.__fileMenu.add_command(label='新建', command=self.__newFile)
        self.__fileMenu.add_command(label='打开', command=self.__openFile)
        self.__fileMenu.add_command(label='保存', command=self.__saveFile)
        self.__fileMenu.add_command(label='另存为', command=self.__saveAs)
        # 设置 - 子选项
        self.__setMenu.add_command(label='背景颜色', command=self.__setBg)
        # 帮助 - 子选项
        self.__aboutMenu.add_command(label='关于', command=self.__about)

        # 文本框
        self.__text = Text()
        self.__text.place(relx=0.001, rely=0.001, relwidth=0.998, relheight=0.998)

        # 检测文本框内容修改 - 待完善
        # 按任意键皆被视为修改文本框内容
        self.__isChanged = False
        self.__text.bind('<KeyPress>', self.__changeFlag)

    def __newFile(self):
        """
        新建文件
        """
        self.__saveType = 'newFile'

        if self.__isChanged == True:
            if askyesnocancel(title='提示', message='是否保存？'):
                self.__saveFile()
            else:
                return

        self.__text.delete(1.0, END)

    def __openFile(self):
        """
        打开文件
        """
        self.__saveType = 'openFile'

        if self.__isChanged == True:
            if self.__isChanged == True:
                confirm = askyesnocancel(title='提示', message='是否保存？')
                if confirm == True:
                    self.__saveFile()
                elif confirm == None:
                    return
                else:
                    pass

        self.__fileName = askopenfilename(title='打开文件')

        if not self.__fileName:
            return

        with open(self.__fileName, 'r') as f:
            self.__text.delete(1.0, END)
            self.__text.insert(INSERT, f.read())

        self.__isChanged = False

    def __saveFile(self):
        """
        保存文件
        """
        if self.__saveType == 'newFile' or self.__saveType == 'saveAs':
            self.__fileName = asksaveasfilename(
                title='新建文件',
                initialfile='未命名.txt',
                filetypes=[('文本文档', '*.txt')],
                defaultextension='*.txt',
            )
        elif self.__saveType == 'openFile':
            pass

        if not self.__fileName:
            return

        with open(self.__fileName, 'w') as f:
            f.write(self.__text.get(1.0, END))

        self.__isChanged = False

    def __saveAs(self):
        """
        另存为
        """
        self.__saveType = 'saveAs'
        self.__saveFile()

    def __changeFlag(self, key):
        """
        文本框修改标志
        """
        self.__isChanged = True

    def __onClosing(self):
        """
        关闭程序时检查是否已经保存
        """
        if self.__isChanged == True:
            confirm = askyesnocancel(title='提醒', message='是否保存？')
            if confirm == True:
                self.__saveFile()
            elif confirm == None:
                return
            else:
                pass

        self.__master.destroy()

    def __setBg(self):
        """
        设置背景颜色
        """
        self.__bg = askcolor(color='white', title='选择背景颜色')
        self.__text.config(bg=self.__bg[1])

    def __about(self):
        """
        关于
        """
        showinfo('关于', 'Copyright (C) 2021 IYATT-yx\n2514374431@qq.com')
