import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TwistStamped

from g01_prii3_interfaces.srv import DrawingControl
from std_srvs.srv import Empty
from turtlesim.srv import TeleportAbsolute


def create_twist(linear_x, angular_z):
    msg = TwistStamped()
    msg.twist.linear.x = float(linear_x)
    msg.twist.angular.z = float(angular_z)
    return msg


class DrawNumber(Node):
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
        super().__init__('draw_number')
        self.publisher_ = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        timer_period = 2.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.running = True
        self.service = self.create_service(DrawingControl, '/drawing_control', self.drawing_control_callback)
        self.clear_client = self.create_client(
            Empty,
            '/clear'
        )

        self.teleport_client = self.create_client(
            TeleportAbsolute,
            '/turtle1/teleport_absolute'
        )

    def timer_callback(self):
        if self.i < len(self.msgs) and self.running:
            self.publisher_.publish(self.msgs[self.i])
            self.get_logger().info('Publishing: "%s"' % self.msgs[self.i])
            self.i += 1

    
    def drawing_control_callback(self, request, response):
        if request.command == 'stop':
            self.running = False
            response.message = 'Dibujo detenido'
        elif request.command == 'resume':
            self.running = True
            response.message = 'Dibujo reanudado'
        elif request.command == 'restart':
            self.restart()
            response.message = 'Dibujo reiniciado'
        else:
            response.message = 'Comando desconocido'

        return response

    def restart(self):
        teleport_request = TeleportAbsolute.Request()
        teleport_request.x = 5.5
        teleport_request.y = 5.5
        teleport_request.theta = 0.0

        self.teleport_client.call_async(teleport_request)

        clear_request = Empty.Request()
        self.clear_client.call_async(clear_request)

        self.i = 0
        self.running = True


def main(args=None):
    rclpy.init(args=args)

    draw_number = DrawNumber()

    rclpy.spin(draw_number)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    draw_number.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
