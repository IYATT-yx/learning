#!/usr/bin/env python3
"""
@file main.py
@brief 模块示例
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
from module import *

fun1()

try:
    fun2()
except Exception as result:
    print(result)
