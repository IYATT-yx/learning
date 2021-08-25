#!/usr/bin/env python3
"""
@file tkinter预览摄像头.py
@brief 使用 OpenCV 打开摄像头，并在 tkinter 中预览
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
import cv2 as cv
from tkinter import *
from PIL import Image, ImageTk
from threading import *


class ShowVideo(Thread):
    def __init__(self, camera, movie):
        super().__init__()
        self.__camera = camera
        self.__movie = movie

    def run(self):
        while self.__camera.isOpened():
            ret, frame = self.__camera.read()

            if ret:
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
                img = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.__movie.config(image=img)
                self.__movie.image = img


class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.__master = master

        self.__camera = cv.VideoCapture(0)

        self.__movie = Label(self.__master)
        self.__movie.pack()

        self.__master.protocol('WM_DELETE_WINDOW', self.__release)

    def createWidgets(self):
        ShowVideo(self.__camera, self.__movie).start()

    def __release(self):
        self.__camera.release()
        self.__master.destroy()


if __name__ == '__main__':
    root = Tk()
    root.title('预览视频')
    app = Application(root)
    app.createWidgets()
    root.mainloop()
