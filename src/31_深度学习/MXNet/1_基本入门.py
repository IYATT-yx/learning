#!/usr/bin/env python3
"""
@file 1_基本入门.py

    MXNet 尝试

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
import mxnet as mx

if __name__ == '__main__':

    """
    命令式
    """
    a = mx.nd.array([1])
    b = mx.nd.array([2])
    c = mx.nd.array([3])

    d = (a + b) * c

    print(d.asnumpy())
    print(d.asscalar())


    """
    符号式
    """
    e = mx.sym.Variable('e')
    f = mx.sym.Variable('f')
    g = mx.sym.Variable('g')

    h = (e + f) * g

    inputArgs = {
        'e': mx.nd.array([1]),
        'f': mx.nd.array([2]),
        'g': mx.nd.array([3])
    }

    executor = h.bind(ctx=mx.cpu(0), args=inputArgs)
    executor.forward()
    print(executor.outputs[0].asnumpy())
    print(executor.outputs[0].asscalar())