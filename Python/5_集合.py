#!/usr/bin/env python3
"""
@file 5_集合.py
@brief 集合
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""

set1 = {1, 8, 2, 3, 4, 5, 5, 5, 6, 7, 8, 2}  # 集合去重,无序
print(set1)

set2 = set('abjhsaabcdwdw')
print(set2)

# 创建空集合
set3 = set()

# 集合增加单个数据
set3.add(100)
set3.add(200)
set3.add(100)
print(set3)

# 集合增加序列
set3.update([988, 677, 344, 200, 100, 100])
print(set3)
set3.update('nhcdaas')
print(set3)

# 删除数据
set3.remove(988)  # 不存在会报错
print(set3)
set3.discard(200)  # 不存在不会报错
print(set3)
set3.pop()  # 随机删除一个元素
print(set3)

# 查找
print(100 in set3)
