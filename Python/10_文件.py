#!/usr/bin/env python3
"""
@file 10_文件.py
@brief 文件
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""

f1 = open('README.md', 'r')

# content1 = f1.read()  # 读取所有
# print(content1)

# # seek(偏移量，起始位置)
# # 起始位置：
# # 0 开头
# # 1 当前位置
# # 2 尾部
# f1.seek(0)

# # readline 调用一次读取一行
content2 = f1.readlines()  # 读取所有并返回一个按行作为元素的列表
print(content2)

f1.close()
