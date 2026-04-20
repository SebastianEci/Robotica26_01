from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
import os

def generate_launch_description():

    pkg_share = FindPackageShare('dif_bot_description').find('dif_bot_description')

    urdf_file = os.path.join(
        pkg_share,
        'description',
        'dif_bot_description.urdf.xacro'
    )

    robot_description = ParameterValue(
        Command(['xacro ', urdf_file]),
        value_type=str
    )

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description
            }]
        )
    ])

