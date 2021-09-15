project(stereovision)

# 标定板角点提取
add_executable(chessboard ${CMAKE_CURRENT_SOURCE_DIR}/chessboard.cpp)
target_link_libraries(chessboard ${OpenCV_LIBS})

# 双目图像采集
add_executable(collect ${CMAKE_CURRENT_SOURCE_DIR}/collect.cpp)
target_link_libraries(collect ${OpenCV_LIBS})

# 帧率获取与计算
add_executable(frame ${CMAKE_CURRENT_SOURCE_DIR}/frame.cpp)
target_link_libraries(frame ${OpenCV_LIBS})