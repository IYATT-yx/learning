#!/usr/bin/env python3
"""
@file main.py

Python 调用动态库演示

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
from ctypes import c_char_p, c_void_p, cdll
import os

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))

    # 生成动态库
    with os.popen('gcc -shared -fPIC -Wall -o' + path + '/libmd5.so ' + path + '/md5.c', 'r', 1) as f:
        print(f.read())

    # 导入动态库
    try:
        lib = cdll.LoadLibrary(path + '/libmd5.so')
    except Exception as result:
        print(result)
        exit()

    # 123456789 的 32 位 MD5： 25f9e794323b453885f5181f1b624d0b
    lib.md5_32.restype = c_char_p
    string = b'123456789'
    md5 = lib.md5_32(string, len(string))
    print(md5.decode('ascii'))

    # 123456789 的 16 位 MD5: 323b453885f5181f
    lib.md5_16.restype = c_char_p
    md5 = lib.md5_16(md5)
    print(md5.decode('ascii'))

    # 123456789 以 123456789 作为密钥加密计算为： 3d88017cab7593b8d71dc5852211fad3
    lib.hmac_md5.restype = c_char_p
    hmac = lib.hmac_md5(string, len(string), string, len(string))
    print(hmac.decode('ascii'))

