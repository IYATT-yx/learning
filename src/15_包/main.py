#!/usr/bin/env python3
"""
@file main.py
@brief 包示例
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""
from package import *

m1.fun1()

try:
    m2.fun2()
except Exception as result:
    print(result)
