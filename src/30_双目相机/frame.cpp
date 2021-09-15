/**
 * @file frame.cpp
 * @brief 帧率获取与计算
 * 
 * 某期青年大学习的视频，可以用于测试： http://dxxsv.cyol.com/jcedfolaeb.mp4
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
#include <string>

#if defined(__linux) || defined(__linux__)
#include <getopt.h>
#elif
#error "只支持 Linux 系统下构建！"
#endif


/**
 * @brief 参数格式说明
 */
void formatWarn()
{
    std::cout << "\n-f [path]\n";
    std::cout << "指定要打开的视频文件路径。\n\n";
    std::cout << "-v [num]\n";
    std::cout << "指定要打开的视频设备编号。\n" << std::endl;
}


int main(int argc, char **argv)
{
    if (argc != 3)
    {
        formatWarn();
        exit(EXIT_FAILURE);
    }

    // 视频对象
    cv::VideoCapture video;

    // 位置参数分析
    int opt;
    while ((opt = getopt(argc, argv, "f:v:")) != -1)
    {
        switch (opt)
        {
            // 从文件/网络获取视频
            case 'f':
            {
                video.open(optarg);
                if (!video.isOpened())
                {
                    std::cerr << "视频打开失败，请检查是否存在！\n";
                    return 1; 
                }

                std::cout << "视频总帧数： " << video.get(cv::CAP_PROP_FRAME_COUNT) << std::endl;
                std::cout << "视频帧率： " << video.get(cv::CAP_PROP_FPS) << std::endl;  // 视频文件本身的帧率，实际播放不一定相同

                goto bre;
            }
            // 从摄像头获取视频
            case 'v':
            {
                video.open(atoi(optarg));
                if (!video.isOpened())
                {
                    std::cerr << "打开摄像头失败，请检查是否接入摄像头！\n";
                    return 1;
                }

                goto bre;
            }
            case '?':
            {
                std::cout << "未知参数：" << static_cast<char>(optopt) << std::endl;
                formatWarn();
                return 1;
            }
            default:
            {
                ;
            }
        }
    }

bre:
    std::cout << "视频分辨率： " << video.get(cv::CAP_PROP_FRAME_WIDTH) << "x" << video.get(cv::CAP_PROP_FRAME_HEIGHT) << std::endl;

    // 初始时间
    int64 last = cv::getTickCount();
    cv::Mat src;
    while (video.read(src))
    {
        // 帧率计算与显示
        int64 now = cv::getTickCount();
        double fps = cv::getTickFrequency() / static_cast<double>(now - last);
        last = now;
        cv::putText(src, "FPS: " + std::to_string(fps), cv::Point(50, 50), cv::FONT_HERSHEY_COMPLEX_SMALL, 1, cv::Scalar(0, 0, 255));

        cv::imshow("实时视频", src);
        if (cv::waitKey(1) == 27)
        {
            break;
        }
    }

    video.release();
}