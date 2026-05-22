import math
import yaml

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from geometry_msgs.msg import PoseStamped

from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


class MissionCommander(Node):
    def __init__(self):
        super().__init__('mission_commander')

        self.declare_parameter('waypoints_file', '')
        self.waypoints_file = self.get_parameter('waypoints_file').value

        self.navigator = BasicNavigator()

        self.start_requested = False
        self.mission_running = False

        self.start_srv = self.create_service(
            Trigger,
            'start_mission',
            self.start_mission_callback
        )

        self.get_logger().info('Nodo mission_commander listo.')
        self.get_logger().info('Servicio disponible: /start_mission')
        self.get_logger().info(f'Archivo de waypoints: {self.waypoints_file}')

    def start_mission_callback(self, request, response):
        if self.mission_running:
            response.success = False
            response.message = 'Ya hay una misión en ejecución.'
            return response

        self.start_requested = True
        response.success = True
        response.message = 'Misión solicitada. Iniciando ejecución...'
        self.get_logger().info(response.message)
        return response

    def yaw_to_quaternion(self, yaw):
        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)
        return qz, qw

    def load_waypoints(self):
        if not self.waypoints_file:
            raise RuntimeError('No se especificó waypoints_file.')

        with open(self.waypoints_file, 'r') as file:
            data = yaml.safe_load(file)

        if data is None or 'waypoints' not in data:
            raise RuntimeError('El YAML debe tener una clave llamada waypoints.')

        poses = []

        for wp in data['waypoints']:
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.header.stamp = self.navigator.get_clock().now().to_msg()

            pose.pose.position.x = float(wp['x'])
            pose.pose.position.y = float(wp['y'])
            pose.pose.position.z = 0.0

            yaw = float(wp.get('yaw', 0.0))
            qz, qw = self.yaw_to_quaternion(yaw)

            pose.pose.orientation.x = 0.0
            pose.pose.orientation.y = 0.0
            pose.pose.orientation.z = qz
            pose.pose.orientation.w = qw

            poses.append(pose)

        return poses

    def run_mission(self):
        self.mission_running = True
        self.start_requested = False

        try:
            self.get_logger().info('Esperando a que Nav2 esté activo...')
            self.navigator.waitUntilNav2Active()

            poses = self.load_waypoints()

            if len(poses) == 0:
                self.get_logger().error('No hay waypoints en el archivo YAML.')
                return

            self.get_logger().info(f'Se cargaron {len(poses)} waypoints.')
            self.get_logger().info('Enviando misión a Nav2...')

            self.navigator.goThroughPoses(poses)

            while not self.navigator.isTaskComplete():
                feedback = self.navigator.getFeedback()

                if feedback:
                    try:
                        self.get_logger().info(
                            f'Distancia restante aproximada: {feedback.distance_remaining:.2f} m'
                        )
                    except Exception:
                        pass

            result = self.navigator.getResult()

            if result == TaskResult.SUCCEEDED:
                self.get_logger().info('Misión completada exitosamente.')

            elif result == TaskResult.CANCELED:
                self.get_logger().warn('La misión fue cancelada.')

            elif result == TaskResult.FAILED:
                self.get_logger().error('La misión falló.')

            else:
                self.get_logger().warn('Resultado desconocido.')

        except Exception as e:
            self.get_logger().error(f'Error ejecutando misión: {str(e)}')

        finally:
            self.mission_running = False


def main(args=None):
    rclpy.init(args=args)

    node = MissionCommander()

    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)

            if node.start_requested and not node.mission_running:
                node.run_mission()

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
