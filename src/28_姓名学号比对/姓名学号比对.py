#!/usr/bin/env python3
"""
@file 28_姓名学号比对.py

受委托帮别人检查宿舍表的学号和名字是不是匹配的，就想到写程序来做，毕竟有几百个数据，
人工看的话不轻松，这也是我第一次用 Python 做表格处理，一边搜索表格读取用法，一边写的，有点杂。

写完后顺便总结一下：
1.表格部分数据不标准的情况，学号类型为数字，直接读取得到的类型是 float，若另一张表是文本类型，
  这种情况下比对也会视为不匹配；
2.安装 xlrd 库，建议版本不要超过 1.2.0，从这个版本后开始到目前最新版 2.0.1 都不能支持 xlsx 文件;

 * Copyright (C) 2021 IYATT-yx (Zhao Hongfei, 赵洪飞)，2514374431@qq.com
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import xlrd
import os

from xlrd.sheet import Cell

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    # 标准表格路径
    stPath = path + '/(标准)20210401各班最新名单：382人.xls'
    # 待比对表格路径
    comPath = path + '/(待比对)20级宿舍导入新.xls'

    # 读取标准表格 st - standard | sh - sheet
    st = xlrd.open_workbook(stPath)
    # 取第一张表
    stsh = st.sheet_by_index(0)
    # 用于保存标准信息的字典
    stdict = dict()
    # 生成标准表格的信息字典（学号：名字）
    # 第4行（下标3）开始含有学号和名字，截至行为385（下标384）
    for row in range(3, stsh.nrows):
        stdict[stsh.cell_value(row, 3)] = stsh.cell_value(row, 4)
    sorted(stdict)
    print('标准数据人数： %d' %len(stdict))


    # 读取待比对表格 com - compare
    com =xlrd.open_workbook(comPath)
    # 取第一张表
    comsh = com.sheet_by_index(0)
    # 用于保存待比对信息的字典
    comdict = dict()
    # 生成待比对表格的信息字典
    # 第2行（下标1）开始含有学号和名字，截至行383（下标282）
    for row in range(1, comsh.nrows):
        comid = comsh.cell_value(rowx=row, colx=0)
        comname = comsh.cell_value(rowx=row, colx=1)
        if comid in comdict.keys():
            print('待对比表录入时发现重复学号: %s %s, 在标准表中学号匹配名字为： %s' %(comname, comid, stdict.get(comid)))
            continue
        comdict[comid] = comname
    sorted(comdict)
    print('去重后录入待对比数据人数： %s' %len(comdict))

    # 比对两表，输出结果
    for stid, stname in stdict.items():
        if stid not in comdict.keys() or comdict.get(stid, 'None') != stname:
            print('{:<4}\t{:<11} 信息不匹配，比对匹配到的错误名字为： {:<4}'.format(stname, stid, comdict.get(stid, '[缺失或已被去重处理]')))
