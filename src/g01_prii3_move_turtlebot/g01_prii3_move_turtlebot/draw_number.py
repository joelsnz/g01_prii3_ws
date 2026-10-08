import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TwistStamped

from g01_prii3_interfaces.srv import DrawingControl
from std_srvs.srv import Empty
from turtlesim.srv import TeleportAbsolute


class DrawNumber(Node):
    def __init__(self):
        super().__init__('draw_number')
        self.publisher_ = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.create_timer(0.1, self.timer_callback)


    def timer_callback(self):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.twist.linear.x = 0.5
        msg.twist.angular.z = 1.5
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    draw_number = DrawNumber()
    rclpy.spin(draw_number)
    draw_number.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
