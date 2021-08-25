#!/usr/bin/env python3
"""
@file 8_lambda.py
@brief lambda
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""

# 加法
a, b, c = 4, 5, 8
f1 = lambda a1, a2, a3=6: a1 + a2 + a3
print(f1(a, b))
print(f1(a, b, c))

# 可变参数
f2 = lambda *args: args
print(f2(a, b, c))

f3 = lambda **kwargs: kwargs
print(f3(name='Tom', age=20, gender='male'))

# 应用,取最大值
f4 = lambda a1, a2: a1 if a1 > a2 else a2
print(f4(a, b))
