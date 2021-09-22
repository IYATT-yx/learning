#!/usr/bin/env python3
"""
@file main.py
@brief 自定义 Python 扩展效果示例

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
try:
    import md5
except:
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system('python3 setup.py build_ext --inplace')
    import md5

# 123456789 的 32 位 MD5： 25f9e794323b453885f5181f1b624d0b
md = md5.md5_32('123456789')
print(md)

# 123456789 的 16 位 MD5: 323b453885f5181f
md16 = md5.md5_16(md)
print(md16)

# 123456789 以 123456789 作为密钥加密计算为： 3d88017cab7593b8d71dc5852211fad3
hmac = md5.hmac_md5('123456789', '123456789')
print(hmac)
