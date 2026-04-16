from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declaramos el argumento que el archivo 'main' nos enviará
    t_ns_launch_arg = DeclareLaunchArgument('t_ns', default_value='turtlesim_default')

    return LaunchDescription([
        t_ns_launch_arg,
        Node(
            package='turtlesim',
            namespace=LaunchConfiguration('t_ns'), # Usa el valor del argumento
            executable='turtlesim_node',
            name='sim_node'
        )
    ])

