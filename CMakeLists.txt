cmake_minimum_required(VERSION 3.17)
project(rmcs_local_map)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_BUILD_TYPE "Release")

find_package(ament_cmake REQUIRED)
set(dependencies
    rclcpp
    nav_msgs
    sensor_msgs
    std_msgs
    pcl_conversions
    livox_ros_driver2
)
foreach(dependency ${dependencies})
    find_package(${dependency} REQUIRED)
endforeach()

find_package(Eigen3 REQUIRED)
find_package(fmt REQUIRED)
find_package(OpenCV REQUIRED COMPONENTS imgproc)
find_package(PCL REQUIRED COMPONENTS common io segmentation filters)

include_directories(src/)
include_directories(src/obstacle/)

file(GLOB_RECURSE LOCAL_MAP_SRC CONFIGURE_DEPENDS src/obstacle/*.cpp)
add_executable(local_map ${LOCAL_MAP_SRC})
ament_target_dependencies(local_map ${dependencies})
target_include_directories(
    local_map PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
    ${PCL_INCLUDE_DIRS}
)
target_link_libraries(
    local_map
    pcl_common
    pcl_io
    pcl_segmentation
    pcl_filters
    ${OpenCV_LIBRARIES}
    fmt::fmt
)

install(
  TARGETS local_map
  DESTINATION lib/${PROJECT_NAME}
)
install(
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
