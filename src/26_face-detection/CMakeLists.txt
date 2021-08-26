project(26_face-detection)

aux_source_directory(${CMAKE_CURRENT_SOURCE_DIR} src)
add_executable(26_face-detection ${src})
target_link_libraries(26_face-detection dlib::dlib ${OpenCV_LIBS})