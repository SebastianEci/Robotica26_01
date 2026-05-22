from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    pkg_path = get_package_share_directory('dif_bot')
    world_file = os.path.join(pkg_path, 'worlds', 'dif_world.sdf')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': f'-r {world_file}'
        }.items()
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ]
    )

    odom_tf = Node(
        package='dif_bot',
        executable='odom_tf',
        output='screen'
    )

    lidar_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        output='screen',
        arguments=[
            '0.15', '0', '0.18',
            '0', '0', '0',
            'base_link',
            'lidar_link'
        ]
    )

    return LaunchDescription([
        gazebo,
        bridge,
        odom_tf,
        lidar_tf
    ])
