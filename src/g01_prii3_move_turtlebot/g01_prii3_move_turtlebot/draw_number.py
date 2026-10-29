import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

from g01_prii3_interfaces.srv import DrawingControl

def create_twist(linear_x, angular_z):
    msg = Twist()
    msg.linear.x = linear_x
    msg.angular.z = angular_z    
    return msg


class DrawNumber(Node):
    def __init__(self):
        super().__init__('draw_number')

        self.movements = [
            create_twist(0.0, 0.9), create_twist(0.0, 0.8), create_twist(0.2, 0.0),
            create_twist(-0.2, 0.0), create_twist(-0.2, 0.0), create_twist(0.2, 0.0),
            create_twist(0.0, -0.9), create_twist(0.0, -0.8), create_twist(0.3, 0.0),
            create_twist(0.3, 0.0), create_twist(0.0, 0.9), create_twist(0.0, 0.9),
            create_twist(0.0, 0.9), create_twist(0.2, 0.0), create_twist(0.0, 0.0)
        ]

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(1, self.timer_callback)
        self.msg_idx = 0
        self.running = True
        self.service_ = self.create_service(
            DrawingControl,
            '/drawing_control',
            self.drawing_control_callback
        )


    def timer_callback(self):
        if self.msg_idx < len(self.movements) and self.running:
            self.publisher_.publish(self.movements[self.msg_idx])
            self.msg_idx += 1
        else:
            self.publisher_.publish(self.movements[-1])

    
    def drawing_control_callback(self, request, response):
        if request.command == 'stop':
            self.running = False
            response.message = 'Dibujo detenido'
        elif request.command == 'resume':
            self.running = True
            response.message = 'Dibujo reanudado'
        elif request.command == 'restart':
            self.msg_idx = 0
            self.running = True
            response.message = 'Dibujo reiniciado'
        else:
            response.message = 'Comando desconocido'

        return response
     

def main(args=None):
    rclpy.init(args=args)

    draw_number = DrawNumber()

    rclpy.spin(draw_number)

    draw_number.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
