#!/usr/bin/env python3
"""
@file 4_字典.py
@brief 字典
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""

# 创建含数据的字典
dict1 = {'name': 'A', 'age': '20', 'gender': 'male'}
print(dict1)

# 创建空字典
dict2 = {}
dict3 = dict()

# 新增数据 - key不存在则创建
dict2['B'] = '21'
dict2['C'] = '19'
print(dict2)

# 修改 - key存在则修改
dict2['B'] = 30
print(dict2)

# 查找
print(dict1['gender'])
print(dict1.get('gender'))
print(dict1.get('height', 'none'))  # 不存在的key返回指定值

print('keys:')
for key in dict1.keys():  # 遍历所有key
    print(key)

print('values:')
for value in dict1.values():  # 遍历所有value
    print(value)

print('items')
for item in dict1.items():  # 遍历所有键值对
    print(item)

for key, value in dict1.items():
    print(key, ": ", end=' ')
    print(value)
