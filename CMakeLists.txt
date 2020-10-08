cmake_minimum_required(VERSION 2.8)
project( test1 )
add_subdirectory(glad/)
add_executable( test1 test.cpp )

# finds OpenGL, GLU and X11
find_package(OpenGL REQUIRED)
find_package(glfw3 REQUIRED)
find_package(glm REQUIRED)
target_include_directories(test1 PUBLIC
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/include>
                           $<INSTALL_INTERFACE:include>)
target_link_libraries(test1 PRIVATE glad PUBLIC glfw OpenGL::GL ${CMAKE_DL_LIBS})