project(1_face-detection)

aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR} src)
add_executable(1_face-detection ${src})
target_link_libraries(1_face-detection dlib::dlib ${OpenCV_LIBS})