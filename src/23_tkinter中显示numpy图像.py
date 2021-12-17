#!/usr/bin/env python3
"""
@file tkinter中显示numpy图像.py
@brief 在 tk 库构建的 GUI 中显示 numpy 数组图像/直接打开图片
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
from io import BytesIO
from tkinter import *
from PIL import ImageTk, Image # sudo apt install python3-pil python3-pil.imagetk
from face_recognition import *
import numpy as np
import sys
import cv2 as cv
import tensorflow as tf
from tensorflow.python.ops.gen_math_ops import Imag


class Application(Frame):
    def __init__(self, master, path):
        super().__init__(master)
        self.__master = master
        self.__path = path

    def createWidgets(self, openWay):
        global img

        try:
            if openWay == 'cv':  # OpenCV
                src = cv.imread(self.__path, cv.IMREAD_COLOR)
                if src is None:
                    raise FileNotFoundError
                src = cv.cvtColor(src, cv.COLOR_BGR2RGBA)
                img = ImageTk.PhotoImage(image=Image.fromarray(src))
            elif openWay == 'fr':  # face_recognition
                src = load_image_file(self.__path)
                img = ImageTk.PhotoImage(image=Image.fromarray(src))

            elif openWay == 'pil':  # PIL
                img = ImageTk.PhotoImage(image=Image.open(self.__path))
        except FileNotFoundError:
            print('指定的图片路径无法打开，请确认图片是否存在！')
            exit()

        Label(self.__master, image=img).pack()


if __name__ == '__main__':
    if not(len(sys.argv) == 2):
        print('请在参数中制定要打开的图片')
        exit()

    root = Tk()
    root.title(sys.argv[1])
    app = Application(root, sys.argv[1])
    app.createWidgets('pil')
    root.mainloop()
