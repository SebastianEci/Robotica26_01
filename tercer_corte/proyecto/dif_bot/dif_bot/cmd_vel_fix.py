import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CmdVelFix(Node):
    def __init__(self):
        super().__init__('cmd_vel_fix')

        self.declare_parameter('linear_sign', -1.0)
        self.declare_parameter('angular_sign', -1.0)
        self.declare_parameter('linear_scale', 0.5)
        self.declare_parameter('angular_scale', 0.7)

        self.linear_sign = float(self.get_parameter('linear_sign').value)
        self.angular_sign = float(self.get_parameter('angular_sign').value)
        self.linear_scale = float(self.get_parameter('linear_scale').value)
        self.angular_scale = float(self.get_parameter('angular_scale').value)

        self.sub = self.create_subscription(
            Twist,
            '/cmd_vel_raw',
            self.callback,
            10
        )

        self.pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info(
            f'cmd_vel_fix activo | linear_sign={self.linear_sign}, '
            f'angular_sign={self.angular_sign}, '
            f'linear_scale={self.linear_scale}, '
            f'angular_scale={self.angular_scale}'
        )

    def callback(self, msg):
        fixed = Twist()

        fixed.linear.x = self.linear_sign * self.linear_scale * msg.linear.x
        fixed.angular.z = self.angular_sign * self.angular_scale * msg.angular.z

        self.pub.publish(fixed)


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelFix()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
