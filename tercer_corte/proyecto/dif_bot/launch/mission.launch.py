from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    pkg_path = get_package_share_directory('dif_bot')
    waypoints_file = os.path.join(pkg_path, 'config', 'waypoints.yaml')

    mission_node = Node(
        package='dif_bot',
        executable='mission_commander',
        name='mission_commander',
        output='screen',
        parameters=[
            {'waypoints_file': waypoints_file}
        ]
    )

    return LaunchDescription([
        mission_node
    ])
