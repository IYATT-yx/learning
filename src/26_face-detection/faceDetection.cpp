/**
 * @file faceDetection.cpp
 * @author IYATT-yx 2514374431@qq.com
 * @brief 人脸检测
 * @copyright Copyright (C) 2021 IYATT-yx
 * 基于 AGPL-3.0 许可 <http://www.gnu.org/licenses/>
 */
#include <iostream>
#include <vector>
#include "opencv2/opencv.hpp"
#include "dlib/opencv.h"
#include "dlib/image_processing/frontal_face_detector.h"
#include "dlib/image_processing/render_face_detections.h"
#include "dlib/gui_widgets.h"
#include "dlib/image_processing.h"

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        std::cerr << "请指定人脸特征点模型 shape_predictor_68_face_landmarks.dat 的路径！\n";
        exit(EXIT_FAILURE);
    }

    dlib::frontal_face_detector detector = dlib::get_frontal_face_detector();

    cv::VideoCapture cam(0);
    if (!cam.isOpened())
    {
        std::cerr << "打开摄像头失败！" << std::endl;
        exit(EXIT_FAILURE);
    }

    // 加载人脸特征点模型
    dlib::shape_predictor predictor;
    try
    {
        dlib::deserialize(argv[1]) >> predictor;
    }
    catch (std::exception &e)
    {
        std::cerr << "打开人脸特征点模型失败： " << e.what() << "\n";
        exit(EXIT_FAILURE);
    }
    
    
    const int scale = 3; // 图像处理缩放比例
    std::vector<dlib::full_object_detection> shapes; // 存放特征点
    cv::Mat src, small;

    while (cam.read(src))
    {
        cv::resize(src, small, cv::Size(src.cols / scale, src.rows / scale)); // 减小识别时的运算量
        dlib::cv_image<dlib::bgr_pixel> rgbImg = small;
        std::vector<dlib::rectangle> faces = detector(rgbImg);

        for (auto i : faces)
        {
            cv::rectangle(src, cv::Rect(static_cast<int>(i.left()) * scale, static_cast<int>(i.top()) * scale,
                            static_cast<int>(i.width()) * scale, static_cast<int>(i.height()) * scale), cv::Scalar(0, 0, 255)); // 框出人脸
            shapes.push_back(predictor(rgbImg, i));
        }

        // 绘制特征点
        if (!shapes.empty())
        {  
            for (int i = 0; i < 68; i++)
            {  
                circle(src, cvPoint(static_cast<int>(shapes[0].part(i).x()) * scale, static_cast<int>(shapes[0].part(i).y()) * scale), 1, cv::Scalar(0, 0, 255), -1);  
                putText(src, std::to_string(i), cvPoint(static_cast<int>(shapes[0].part(i).x()) * scale, static_cast<int>(shapes[0].part(i).y()) * scale), cv::FONT_HERSHEY_PLAIN, 1, cv::Scalar(255, 0, 0),1,4);
            }  
        }

        shapes.resize(0);

        cv::imshow("摄像头", src);
        if (cv::waitKey(50) == 27)
        {
            break;
        }
    }

    cam.release();
}