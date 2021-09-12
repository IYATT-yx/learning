project(stereovision)

# 标定板角点提取
add_executable(chessboard ${CMAKE_CURRENT_SOURCE_DIR}/chessboard.cpp)
target_link_libraries(chessboard ${OpenCV_LIBS})