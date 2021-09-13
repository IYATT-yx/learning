/**
 * @file collect.cpp
 * @brief 双目图像采集
 * 
 * 运行本程序后，再需要使用 modeSwitch.sh 脚本切换模式为 4 （双目）
 * 
 * Copyright (C) 2021 IYATT-yx (Zhao Hongfei, 赵洪飞)，2514374431@qq.com
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * 
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
#include "opencv2/opencv.hpp"

#include <iostream>

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        std::cerr << "请指定视频设备编号！\n";
        exit(EXIT_FAILURE);
    }

    cv::VideoCapture cam(atoi(argv[1]));
    if (!cam.isOpened())
    {
        std::cerr << "摄像头打开失败，请检查指定摄像头编号是否存在！\n";
        exit(EXIT_FAILURE);
    }

    cv::Mat frame, dst;
    while (cam.read(frame))
    {
        /**
         * 该双目摄像头输出的视频流尺寸固定为 640x480
         * 在双目模式下，两个摄像头采集的视频以左右两个图像的方式衔合在一起，
         * 而尺寸还是 640x480，这时候每个摄像头的视频宽带都会被压缩一半，
         * 因此将图像高度也压缩一半来保持图像原有比例。
         */
        cv::resize(frame, dst, cv::Size(640, 240));
        cv::imshow("dst", dst);

        /**
         * 拆分图像
         * 获得左右摄像头的图像
         * 经过处理后，单个摄像头视频尺寸为 320x240
         */
        cv::Mat left = dst(cv::Rect(0, 0, 320, 240));
        cv::Mat right = dst(cv::Rect(320, 0, 320, 240));

        cv::imshow("left", left);
        cv::imshow("right", right);

        if (cv::waitKey(40) == 27)
        {
            break;
        }
    }
}