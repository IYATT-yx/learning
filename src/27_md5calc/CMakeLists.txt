project(md5calc)

add_executable(md5calc ${CMAKE_CURRENT_SOURCE_DIR}/md5calc.c)
target_link_libraries(md5calc ${OPENSSL_LIBRARIES})