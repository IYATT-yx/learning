/**
 * @file monocular-undistortion.cpp
 * @brief 单目相机标定与矫正
 * 
 * 运行程序时，位置参数需要指定摄像头设备序号，然后会打开一个预览窗口，按空格键拍照（要拍摄棋盘），按 Esc 退出，
 * 程序会计算相机内参和畸变系数，并再次打开摄像头进行预览，可观看原图和校正后的实时视频。
 * 
 * 注意如果使用的标定板不同（内角点有9列6行，格子边长19mm），程序中的参数需要自行修改，否则运行时会抛出错误。
 * 
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
#include <string>
#include <ctime>
#include <sstream>

#if defined(__linux) || defined(__linux__)
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#elif
#error "请在 Linux 下进行构建！"
#endif


int main(int argc, char **argv)
{
    if (argc != 2)
    {
        std::cerr << "请指定相机索引!\n";
        exit(EXIT_FAILURE);
    }

    cv::VideoCapture cam(atoi(argv[1]));
    if (!cam.isOpened())
    {
        std::cerr << "相机打开失败，请检查是否存在！\n";
        exit(EXIT_FAILURE);
    }

    /**
     * 采集图片存放到 /tmp/boardImg 路径下
     * 先检测是否存在这个文件夹，不存在就创建，存在就清空下面的图片
     */
    if (access("/tmp/boardImg", F_OK) == -1)  // 不存在
    {
        std::cout << "a" << std::endl;
        mkdir("/tmp/boardImg", 0770);
    }
    else
    {
        int ret = system("rm /tmp/boardImg/*");
        (void)ret;
    }

    /**
     * 标定板图片采集
     * 图片文件名由拍摄的时间生成
     */
    cv::Mat frame;
    std::vector<std::string> paths;
    while (cam.read(frame))
    {
        cv::imshow("预览摄像头（按空格拍照）， Esc 退出", frame);
        int key = cv::waitKey(40);
        if (key == 27)
        {
            cv::destroyAllWindows();
            break;
        }
        else if (key == 32)
        {
            time_t now;
            time(&now);
            struct tm *local = localtime(&now);
            std::stringstream pathStream;
            pathStream << "/tmp/boardImg/" << local->tm_year + 1900 << local->tm_mon + 1 << local->tm_mday << local->tm_hour << local->tm_min << local->tm_sec << ".jpg";
            std::string path = pathStream.str();
            paths.push_back(path);  // 图片路径储存

            if (cv::imwrite(path, frame))
            {
                std::cout << "已保存： " << path << std::endl;
            }
            else
            {
                std::cout << "保存失败： " << path << std::endl;
            }
        }
    }
    //////////////////////////////////////////////////// 标定板图片采集

    /**
     * 相机标定
     * 获取相机的内参矩阵和畸变系数
     */
    // 标定板图片
    std::vector<cv::Mat> imgs;
    for (std::string path : paths)
    {
        cv::Mat src = cv::imread(path);
        cv::Mat gray;
        cv::cvtColor(src, gray, cv::COLOR_BGR2GRAY);
        imgs.push_back(gray);
    }

    cv::Size boardSize = cv::Size(9, 6);  // 标定板内角点数据: 9列6行 （根据实际使用的标定板而定）
    
    // 提取内角点
    std::vector<std::vector<cv::Point2f>> imgsPoints;
    for (auto img : imgs)
    {
        std::vector<cv::Point2f> imgPoints;
        cv::findChessboardCorners(img, boardSize, imgPoints);
        // cv::find4QuadCornerSubpix(img, imgPoints, boardSize);
        imgsPoints.push_back(imgPoints);
    }

    // 生成内角点三维坐标
    cv::Size squareSize = cv::Size(19, 19);  // 目录下标定板图片用 A4 纸打印，方格边长 19mm
    std::vector<std::vector<cv::Point3f>> objectPoints;
    for (size_t i = 0; i < imgsPoints.size(); ++i)
    {
        std::vector<cv::Point3f> tempPointSet;
        for (int j = 0; j < boardSize.height; ++j)
        {
            for (int k = 0; k < boardSize.width; ++k)
            {
                cv::Point3f realPoint;

                // 假定标定板为世界坐标系的 z 平面，即 z = 0
                realPoint.x = static_cast<float>(j * squareSize.width);
                realPoint.y = static_cast<float>(k * squareSize.height);
                realPoint.z = 0;

                tempPointSet.push_back(realPoint);
            }
        }
        objectPoints.push_back(tempPointSet);
    }

    // 初始化每幅图像中的角点数量，假定每幅图像中都可以看到完整的标定板
    std::vector<int> pointNumber;
    for (size_t i = 0; i < imgsPoints.size(); ++i)
    {
        pointNumber.push_back(boardSize.width * boardSize.height);
    }

    // 图像尺寸
    cv::Size imageSize;
    imageSize.width = imgs[0].cols;
    imageSize.height = imgs[0].rows;

    cv::Mat cameraMatrix = cv::Mat(3, 3, CV_32FC1, cv::Scalar::all(0));  // 相机内参矩阵

    // 5 个畸变系数
    cv::Mat distCoeffs = cv::Mat(1, 5, CV_32FC1, cv::Scalar::all(0));
    std::vector<cv::Mat> rvecs;  // 每幅图像的旋转向量
    std::vector<cv::Mat> tvecs;  // 每幅图像的平移向量
    
    cv::calibrateCamera(objectPoints, imgsPoints, imageSize, cameraMatrix, distCoeffs, rvecs, tvecs);

    std::cout << "相机内参矩阵：\n" << cameraMatrix << std::endl;
    std::cout << "畸变系数：\n" << distCoeffs << std::endl;

    // 保存相机标定结果 - 同一个摄像头后面可以直接使用这个数据，而不用每次使用前都标定
    cv::FileStorage calibrateResult("/tmp/calibrateResult.xml", cv::FileStorage::WRITE);
    calibrateResult.write("cameraMatrix", cameraMatrix);
    calibrateResult.write("distCoeffs", distCoeffs);
    calibrateResult.release();
    //////////////////////////////////////////////////////// 相机标定

    /**
     * 图像矫正
     * 方案一： 使用 initUndistortRectifyMap 和 remap
     * 方案二： 使用 undistort 计算矫正
     */
    while (cam.read(frame))
    {
        // 原图
        cv::imshow("原图", frame);

        cv::Mat undistImg;

        // 第一种方案
        ///////////
        // 计算坐标矫正映射矩阵
        cv::Mat R = cv::Mat::eye(3, 3, CV_32F);
        cv::Mat mapX = cv::Mat(imageSize, CV_32FC1);
        cv::Mat mapY = cv::Mat(imageSize, CV_32FC1);
        cv::initUndistortRectifyMap(cameraMatrix, distCoeffs, R, cameraMatrix, imageSize, CV_32FC1, mapX, mapY);
        // 矫正图像
        cv::remap(frame, undistImg, mapX, mapY, cv::INTER_LINEAR);
        cv::imshow("第一种校正预览", undistImg);
        /////////////////////////////////////////// 第一种方案

        // 第二种方案
        ///////////
        cv::undistort(frame, undistImg, cameraMatrix, distCoeffs);
        cv::imshow("第二种校正预览", undistImg);
        /////////////////////////////////////////// 第二种方案

        if (cv::waitKey(40) == 27)
        {
            break;
        }
    }
    //////////////////////////////////////////////////////// 图像矫正

    cam.release();
}