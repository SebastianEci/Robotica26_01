from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    pkg_path = get_package_share_directory('dif_bot')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    map_file = os.path.join(pkg_path, 'maps', 'mapa_laberinto.yaml')
    params_file = os.path.join(pkg_path, 'config', 'nav2_params.yaml')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
            ),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'true',
                'params_file': params_file,
                'autostart': 'true'
            }.items()
        )
    ])
