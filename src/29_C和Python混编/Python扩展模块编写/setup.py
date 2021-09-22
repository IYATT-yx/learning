#!/usr/bin/env python3
"""
@file setup.py
@brief 为 Python 构建 MD5 扩展

已测试 Windows 10 下使用 MSBuild 和 Ubuntu 20.04 下使用 GNU GCC 构建扩展成功 （都是使用 64 位编译器）

Copyright (C) 2021 IYATT-yx (Zhao Hongfei, 赵洪飞)，2514374431@qq.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from distutils.core import setup, Extension
import sys

if sys.platform == 'win32':
       module1 = Extension('md5',
                            sources=['md5.c'],
                            extra_compile_args=['/utf-8', '/std:c17'])
elif sys.platform == 'linux': 
       module1 = Extension('md5',
                            sources=['md5.c'],
                            extra_compile_args=['-std=c17'])

setup (name='MD5',
       version='1.0',
       description='MD5 库',
       author='IYATT-yx',
       author_email='2514374431@qq.com',
       license='AGPL-3.0',
       url='iyatt.com',
       platforms='Ubuntu 21.04',
       ext_modules=[module1])