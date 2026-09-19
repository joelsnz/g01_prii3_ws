import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


def create_twist(linear_x, angular_z):
    msg = Twist()
    msg.linear.x = float(linear_x)
    msg.angular.z = float(angular_z)
    return msg


class TurtlesimControl(Node):
    msgs = [
        create_twist(2.0, 1.56),
        create_twist(2.0, 1.56),
        create_twist(2.0, 1.56),
        create_twist(2.0, 1.56),
        create_twist(2.6, 0.0),
        create_twist(0.0, 1.55),
        create_twist(2.3, 0.0),
        create_twist(0.0, 2.5),
        create_twist(1.0, 0.0)
    ]

    def __init__(self):
        super().__init__('turtlesim_control')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        timer_period = 2.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        if self.i < len(self.msgs):
            self.publisher_.publish(self.msgs[self.i])
            self.get_logger().info('Publishing: "%s"' % self.msgs[self.i])
            self.i += 1


def main(args=None):
    rclpy.init(args=args)

    turtlesim_control = TurtlesimControl()

    rclpy.spin(turtlesim_control)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    turtlesim_control.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
