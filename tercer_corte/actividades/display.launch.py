from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():

    pkg_share = FindPackageShare(package="dif_bot_description").find("dif_bot_description")
    urdf_path = os.path.join(pkg_share, "description", "dif_bot_description.urdf.xacro")

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': Command(['xacro ', urdf_path])
            }]
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2'
        )
    ])
