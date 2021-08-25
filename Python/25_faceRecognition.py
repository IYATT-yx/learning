#!/usr/bin/env python3
"""
@file faceRecognition.py
@brief 人脸识别
@details 使用
    1.首先在代码所在同级路径下创建一个文件夹名字为 resources;
    2.在 resources 文件夹下放置要识别对象的人脸图片;
    3.在 resources 文件夹下创建一个文本文件名为 lists.txt,并将上面要识别的
    人脸图片文件名写入 lists.txt 中，注意每行一个文件名，不能留空行;
    4.如果要退出程序，可按键盘左上角的 Esc 键。
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
import os
import cv2 as cv
import numpy as np
from tkinter.messagebox import *
from face_recognition import *

# 获取资源路径
pyPath = os.path.dirname(os.path.abspath(__file__)) + '/resources/'


def getImg():
    """获取人脸图片名"""
    global pyPath
    knownFaceNames = list()
    try:
        with open(pyPath + 'lists.txt', 'r') as f:
            for line in f:
                knownFaceNames.append(line.strip('\n'))
    except Exception as result:
        showerror('获取人脸图片名错误', result)
        exit()

    return knownFaceNames


def loadFaceData(faceNames):
    """获取人脸数据"""
    global pyPath

    try:
        return [face_encodings(load_image_file(pyPath + name))[0] for name in faceNames]
    except Exception as result:
        showerror('获取人脸数据出错', result)
        exit()


def recognition(knownFaceNames, knownFaceEncodings):
    """识别"""
    camera = cv.VideoCapture(0)
    if not camera.isOpened():
        showerror('打开摄像头失败', '请检查是否接入摄像头')
        exit()

    faceNames = list()
    faceEncodings = list()

    while True:
        ret, frame = camera.read()
        # 缩小图像，降低运算量提高速度
        smallFrame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgbImg = smallFrame[:, :, ::-1]

        # 检测人脸
        faceLocation = face_locations(rgbImg)
        faceEncodings = face_encodings(rgbImg, faceLocation)

        faceNames = []
        for faceEncoding in faceEncodings:
            # 将摄像头视频流中检出的人脸和提供的人脸图像比对
            matches = compare_faces(knownFaceEncodings, faceEncoding)
            name  = 'Unknow'

            # 计算欧式距离，寻找最相似的
            faceDistances = face_distance(knownFaceEncodings, faceEncoding)
            bestMatchIndex = np.argmin(faceDistances)
            if matches[bestMatchIndex]:
                name = knownFaceNames[bestMatchIndex].strip('.jpg')

            faceNames.append(name)


        for (top, right, bottom, left), name in zip(faceLocation, faceNames):
            # 坐标换算，检测人脸时得到的坐标是缩小的，框图时还原
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv.putText(frame, name, (left + 6, bottom - 6), cv.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        cv.imshow('video', frame)
        if cv.waitKey(40) == 27:
            break

    camera.release()    
    cv.destroyAllWindows()



if __name__ == '__main__':
    knownFaceNames = getImg()
    knownFaceEncodings = loadFaceData(knownFaceNames)
    recognition(knownFaceNames, knownFaceEncodings)