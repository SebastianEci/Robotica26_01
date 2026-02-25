find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(turtlesim REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(rclcpp_action REQUIRED)

add_executable(turtle_controller src/turtle_controller.cpp)
target_link_libraries(turtle_controller rclcpp geometry_msgs turtlesim example_interfaces rclcpp_action)
