"""
@file module.py
@brief 模块示例
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""

# 只要定义了该变量，导入时使用 from xxx import * 则以该变量内容为准。则fun2不会被导入。
__all__ = ['fun1']


def fun1():
    print('功能一')


def fun2():
    print('功能二')
