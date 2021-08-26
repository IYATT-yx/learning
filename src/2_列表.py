#!/usr/bin/env python3
"""
@file 2_列表.py
@brief 列表
@author IYATT-yx
@copyright Copyright (C) 2021 IYATT-yx
            基于 AGPL-3.0 许可
"""

list1 = ['apple', 'orange', 'banana']
list3 = [4, 5, 3, 2, 9, 8, 6]

# index 查找
# count 统计
# len 列表长度
# 略......

# 判断存在
print('apple' in list1)
print('pineapple' not in list1)


print(list1)

list1.append('pineapple')  # 追加单个元素
print(list1)

list1.extend(['watermelon', 'grape'])  # 支持追加列表
print(list1)

list1.insert(1, 'pear')  # 指定位置插入数据
print(list1)

list1.pop(1)  # 删除指定下标的数据
print(list1)

list1.remove('apple')  # 移除指定数据
print(list1)

list2 = list1  # 浅拷贝，对 list2 操作会修改 list1
print(list2)

list4 = list1.copy()  # 深拷贝 - 数据拷贝副本
print(list4)

list2.clear()  # 清空内容
print(list2)
print(list1)  # 输出结果同 list1 被置空，浅拷贝，list1 和 list2 指向同一数据
print(list4)  # 深拷贝含有数据副本

del list2
# print(list2) # 使用已删除的对象，会出错


print(list3)
list3.reverse()  # 逆置
print(list3)

list3.sort()  # 默认升序排序
print(list3)

list3.sort(reverse=True)  # 降序排序
print(list3)

# 遍历
for _ in list4:
    print(_)

list5 = [list3, list4]  # 列表嵌套
print(list5)
print(list5[1])
print(list5[1][3])
