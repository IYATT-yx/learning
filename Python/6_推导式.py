#!/usr/bin/env python3
"""
@file 6_推导式.py
@brief 推导式
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""

# 列表推导式
list1 = [_ for _ in range(0, 10, 2)]
print(list1)

list2 = [_ for _ in range(10) if _ % 2 == 0]
print(list2)

list3 = [(i, j) for i in range(3) for j in range(2)]
print(list3)

# 字典推导式
dict1 = {_: _ ** 2 for _ in range(1, 7)}
print(dict1)

list3 = ['name', 'age', 'gender']
list4 = ['A', '20', 'male']
dict2 = {list3[i]: list4[i] for i in range(len(list3))}
print(dict2)

# 提取字典中目标数据
dict3 = {'A': 900, 'B': 234, 'C': 543, 'D': 239, 'E': 874}
dict4 = {key: value for key, value in dict3.items() if value > 600}
print(dict4)

# 集合推导式
set1 = {i ** 2 for i in range(10)}
print(set1)
