#!/usr/bin/env python3
"""
@file 9_高阶函数.py
@brief 高阶函数
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
########################################
# 对列表中每个元素处理后保存在结果到新的列表
def fun1(arg):
    return arg ** 2


list1 = [1, 2, 3, 4, 5]

list2 = list(map(fun1, list1))
print(list2)

##########################################
# 累计
# 列表含有元素 e1,e2,e3,e4,e5,e6,e7,e8,e9
# 则 e1 和 e2 传入函数进行处理，返回值又和 e3 再次传入函数处理， 返回值再和 e4 传入函数进行处理 ...... 直到处理完，返回最终返回值
import functools


def fun2(arg1, arg2):
    return arg1 * arg2


def fun3(arg1, arg2):
    return arg1 + arg2


print(functools.reduce(fun2, list1))
print(functools.reduce(fun3, list1))

##########################################
# 过滤
# 函数为判断条件，返回 True 则提取
def fun4(arg):
    return arg % 2 == 0


list3 = list(filter(fun4, list1))
print(list3)
