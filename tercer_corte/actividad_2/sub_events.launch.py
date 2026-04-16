from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    # Recibe el namespace desde main.launch.py
    t_ns = LaunchConfiguration('t_ns')

    return LaunchDescription([

        # Declaración del argumento
        DeclareLaunchArgument(
            't_ns',
            default_value='default_ns'
        ),

        # Nodo que SÍ aparecerá en ros2 node list
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            namespace=t_ns,
            name='sim_node'
        )
    ])
``

