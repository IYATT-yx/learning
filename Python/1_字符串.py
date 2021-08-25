#!/usr/bin/env python3
"""
@file 1_字符串.py
@brief 字符串
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""

str1 = '012345678901234567890'
str3 = '            there is a red apple growing on the tree.'

# 切片
# 左闭右开
print('——————————切片——————————')
print(str1[2:8:2])  # 246
print(str1[:5])  # 01234
print(str1[::-1])  # 9876543210
print(str1[-3:-1:])  # 78
print('——————————切片end——————————')

# 查找
# 可指定查找下标范围
# find 查到返回下标，否则 -1
# index 查到返回下标，否则报异常
# count 统计出现次数
# rfind 从右往左
# rindex 从右往左
print('——————————查找——————————')
print(str1.find('45'))  # 4
print(str1.find('6', 0, 7))  # 6
print(str1.index('3'))  # 3
print(str1.count('345'))  # 2
print(str1.rfind('5'))
print('——————————查找end——————————')

# 修改

# replace 替换 旧，新，次数
print('——————————替换——————————')
# str2 = str1.replace('0', 'A', str1.count('0'))    # 省略次数全部替换
str2 = str1.replace('0', 'A')
print(str2)
print('——————————替换end——————————')

# split 分割
# 生成一个列表
print('——————————分割——————————')
list1 = str1.split('5')
print(list1)
print('——————————分割end——————————')

# join 拼接
print('——————————拼接——————————')
list2 = '$$$$$$$$'.join(list1)
print(list2)
print('——————————拼接end——————————')

# 大小写处理
print('——————————大小写处理————————————')
print('原句：', str3)
print('句首大写：', str3.capitalize())
print('词首大写：', str3.title())
str4 = str3.upper()
print('全部大写：', str4)
print('全部小写：', str4.lower())
print('——————————大小写处理end——————————')

# 空格字符处理
# lstrip 删除左侧空格
# rstrip 删除右侧空格
# strip 删除两侧空格
print('——————————空格字符处理——————————')
print(str3.lstrip())
print('——————————空格字符处理end——————————')

# 对齐
# ljust 左对齐
# rjust 右对齐
# center 居中
# 设置对齐后的总字符长度，不足则填充指定的字符
print('对齐'.center(100, '—'))
print(str1.center(100, '*'))
print('对齐end'.center(100, '—'))

# 判断
# startwith 是否以指定字符串开头
# endwith
# isalpha 判断是否含有字母
# isdigit 判断是否含有数字
# isalnum 含有字母或数字
print('判断'.center(40, '—'))
print(str1.startswith('012'))
print(str1.endswith('890', 0, 9))
print(str1.isalpha())
print(str1.isdigit())
print(str1.isalnum())
print('判断end'.center(40, '—'))
