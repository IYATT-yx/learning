#!/usr/bin/env python3
"""
@file 13_异常处理.py
@brief 异常处理
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""

# 捕获单个错误
from typing import Final


try:
    print(x)
except NameError as result:
    print(result)

# 同时检测多个错误
try:
    print(1 / 0)
except (NameError, ZeroDivisionError) as result:
    print(result)

# 捕获所有异常
try:
    print(y)
except Exception as result:
    print(result)
finally:
    print('无论是否有异常都会执行')

# 无异常执行
try:
    a = 9
except Exception as result:
    print(result)
else:
    print('无异常发生')

# 自定义异常
class Error(Exception):
    def __str__(self):
        return '触发自定义异常'


try:
    raise Error
except Error as result:
    print(result)
