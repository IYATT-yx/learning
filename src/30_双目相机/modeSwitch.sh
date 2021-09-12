#!/usr/bin/bash
:<<head

@file modeSwitch.sh
@brief 双目摄像头模式设置
        1 左单目
        2 右单目
        3 红蓝3D
        4 双目

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

head
#######################################################################

# 安装依赖项
if [ -z `which uvcdynctrl` ]
then
    sudo apt update
    sudo apt install -y uvcdynctrl
fi
if [ -z `which uvcdynctrl` ]
then
    echo "安装依赖项失败，退出！"
    exit
fi

# 参数描述
function paraDes()
{
    echo -e "./modeSwitch.sh [camNum] [modeNum]\n"
    echo "[camNum] 双目摄像头的硬件序号,查看所有视频设备： ls /dev/video*"
    echo -e "[modeNum] 指定要设定的模式号：\n1 左单目\n2 右单目\n3 红蓝3D\n4 双目"
}

# 空参数
if [ $# -ne 2 ]
then
    paraDes
    exit
fi

# 摄像头设备验证
if [ ! -e "/dev/video$1" ]
then
    echo "不存在指定的视频设备！"
    exit
fi

# 视频设备
dev=/dev/video$1

# 初始化
function init()
{
    uvcdynctrl -d $dev -S 6:8  '(LE)0x50ff'
    uvcdynctrl -d $dev -S 6:15 '(LE)0x00f6'
    uvcdynctrl -d $dev -S 6:8  '(LE)0x2500'
    uvcdynctrl -d $dev -S 6:8  '(LE)0x5ffe'
    uvcdynctrl -d $dev -S 6:15 '(LE)0x0003'
    uvcdynctrl -d $dev -S 6:15 '(LE)0x0002'
    uvcdynctrl -d $dev -S 6:15 '(LE)0x0012'
    uvcdynctrl -d $dev -S 6:15 '(LE)0x0004'
    uvcdynctrl -d $dev -S 6:8  '(LE)0x76c3'
}


if [ $2 -eq 1 ]
then
    init
    uvcdynctrl -d $dev -S 6:10 '(LE)0x0100'
    echo "已设置左单目"
elif [ $2 -eq 2 ]
then
    init
    uvcdynctrl -d $dev -S 6:10 '(LE)0x0200'
    echo "已设置右单目"
elif [ $2 -eq 3 ]
then
    init
    uvcdynctrl -d $dev -S 6:10 '(LE)0x0300'
    echo "已设置红蓝3D"
elif [ $2 -eq 4 ]
then
    init
    uvcdynctrl -d $dev -S 6:10 '(LE)0x0400'
    echo "已设置双目"
else
    paraDes
    exit
fi
