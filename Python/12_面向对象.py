#!/usr/bin/env python3
"""
@file 12_面向对象.py
@brief 面向对象
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""


class A:
    def __init__(self, a, b):  # 类似于 C++ 构造函数
        self.a = a
        self.b = b

    def __str__(self):
        return '这是 A 类'

    def __del__(self):  # 类似于 C++ 析构函数
        print('A类实例化对象被释放')

    def fun(self):
        print(self.a, self.b)


# 继承
class B(A):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __del__(self):
        print('B类实例化对象被释放')


# 多态
class Color:
    def show(self):
        print('颜色')


class Red(Color):
    def show(self):
        print('红色')


class Blue(Color):
    def show(self):
        print('蓝色')


class Exe:
    def do(self, color):
        color.show()


if __name__ == '__main__':
    print('实例一'.center(20, '-'))
    c1 = A(8, 9)
    print(c1)
    c1.fun()
    del c1

    print('实例二'.center(20, '-'))
    c2 = B(1, 2)
    c2.fun()
    print(B.__mro__)  # 查看继承父类
    del c2

    print('实例三'.center(20, '-'))  # 多态

    exe = Exe()
    red = Red()
    blue = Blue()

    exe.do(red)
    exe.do(blue)
