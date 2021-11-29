"""
file: client.py
brief: TCP 客户端程序

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
from socket import *
from time import *
from signal import *
from argparse import *


is_continue = True
def end(signum, frame):
    """退出程序
    Ctrl+C 结束程序
    """
    global is_continue
    is_continue = False
    c.close()
    exit(0)

"""参数解析
获取要连接的服务器地址和端口
"""
paser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                        description='端口号')
paser.add_argument('ip', type=str, help='要连接的服务器 IP 地址')
paser.add_argument('port', type=int, help='要连接的服务器的端口号')

c = socket(AF_INET, SOCK_STREAM)
c.connect((paser.parse_args().ip,
            paser.parse_args().port))

signal(SIGINT, end)  # 捕获 Ctrl+C

"""数据收发
发送一次再接收一次
发送的数据为从 0 递增的数字"""
i = 0
while is_continue:
    c.sendall(str(i).encode('utf-8'))
    print(c.recv(1024).decode('utf-8'))
    i = i + 1
    sleep(1)