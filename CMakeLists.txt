cmake_minimum_required(VERSION 3.16.3)
project(learning)

if (${CMAKE_CXX_COMPILER_ID} STREQUAL "GNU" AND ${CMAKE_SYSTEM_NAME} STREQUAL "Linux")
    set(CMAKE_CXX_FLAGS_RELEASE "-no-pie --std=c++17 -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Werror=format-security -Wextra -pedantic -Wimplicit-fallthrough -Wsequence-point -Wswitch-default -Wswitch-unreachable -Wswitch-enum -Wstringop-truncation -Wbool-compare -Wtautological-compare -Wfloat-equal -Wshadow=global -Wpointer-arith -Wpointer-compare -Wcast-align -Wcast-qual -Wwrite-strings -Wdangling-else -Wlogical-op -Wconversion -O3")
    set(CMAKE_CXX_FLAGS_DEBUG "-no-pie --std=c++17 -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Werror=format-security -Wextra -pedantic -Wimplicit-fallthrough -Wsequence-point -Wswitch-default -Wswitch-unreachable -Wswitch-enum -Wstringop-truncation -Wbool-compare -Wtautological-compare -Wfloat-equal -Wshadow=global -Wpointer-arith -Wpointer-compare -Wcast-align -Wcast-qual -Wwrite-strings -Wdangling-else -Wlogical-op -Wconversion -g -O0 -DDEBUG")
    set(CMAKE_C_FLAGS_RELEASE "-no-pie -std=c17 -Wall -Werror=return-type -Werror=address -Werror=sequence-point -Werror=format-security -Wextra -pedantic -Wimplicit-fallthrough -Wsequence-point -Wswitch-default -Wswitch-unreachable -Wswitch-enum -Wstringop-truncation -Wbool-compare -Wtautological-compare -Wfloat-equal -Wshadow=global -Wpointer-arith -Wpointer-compare -Wcast-align -Wcast-qual -Wwrite-strings -Wdangling-else -Wlogical-op -Wconversion -O3")
    set(CMAKE_C_FLAGS_DEBUG "-no-pie -std=c17 -Wall -Werror=return-type -Werror=address -Werror=sequence-point -Werror=format-security -Wextra -pedantic -Wimplicit-fallthrough -Wsequence-point -Wswitch-default -Wswitch-unreachable -Wswitch-enum -Wstringop-truncation -Wbool-compare -Wtautological-compare -Wfloat-equal -Wshadow=global -Wpointer-arith -Wpointer-compare -Wcast-align -Wcast-qual -Wwrite-strings -Wdangling-else -Wlogical-op -Wconversion -g -O0 -DDEBUG")

    set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/bin)

    find_package(OpenCV 4.5.3 REQUIRED)
    find_package(dlib 19.22.0 REQUIRED)
    find_package(OpenSSL 1.1.1 REQUIRED)

    add_subdirectory(${CMAKE_SOURCE_DIR}/src/26_face-detection) # 人脸检测
    add_subdirectory(${CMAKE_SOURCE_DIR}/src/27_md5calc) # md5 计算
    add_subdirectory(${CMAKE_SOURCE_DIR}/src/30_双目相机)

else ()
    message(FATAL_ERROR "请在 Linux 下使用 GNU gcc/g++ 构建")
endif ()