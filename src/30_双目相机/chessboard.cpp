/**
 * @file chessboard.cpp
 * @brief 标定板角点提取
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
#include <vector>

int main()
{
    cv::Mat src = cv::imread("标定板.jpg");
    if (!src.data)
    {
        std::cerr << "读取标定板图片失败，请检查图片是否存在于运行路径下！\n";
        exit(EXIT_FAILURE);
    }

    cv::Mat gray;
    cv::cvtColor(src, gray, cv::COLOR_BGR2GRAY);

    cv::Size size = cv::Size(6, 9);  // 6行9列内角点

    std::vector<cv::Point2f> points;
    cv::findChessboardCorners(gray, size, points);
    
    cv::find4QuadCornerSubpix(gray, points, size);

    cv::drawChessboardCorners(src, size, points, true);

    cv::imshow("标定角点", src);
    cv::waitKey(0);
}
