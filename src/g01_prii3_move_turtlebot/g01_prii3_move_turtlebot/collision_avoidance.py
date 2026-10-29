import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan

from g01_prii3_interfaces.srv import DrawingControl

def create_twist(linear_x, angular_z):
    msg = TwistStamped()
    msg.twist.linear.x = linear_x
    msg.twist.angular.z = angular_z    
    return msg


class CollisionAvoidance(Node):
    def __init__(self):
        super().__init__('collision_avoidance')

        self.Angle = 60
        self.Dist = 5
        self.obstacle = False
        self.safety_distance = 0.20

        self.sub = self.create_subscription(
            LaserScan,
            'scan',
            self.laser_callback,
            10
        )

        base_movements = [
            create_twist(0.0, 0.9), create_twist(0.0, 0.8), create_twist(0.2, 0.0),
            create_twist(-0.2, 0.0), create_twist(-0.2, 0.0), create_twist(0.2, 0.0),
            create_twist(0.0, -0.9), create_twist(0.0, -0.8), create_twist(0.3, 0.0),
            create_twist(0.3, 0.0), create_twist(0.0, 0.9), create_twist(0.0, 0.9),
            create_twist(0.0, 0.9), create_twist(0.2, 0.0), create_twist(0.0, 0.0)
        ]

        self.movements = []
        for mov in base_movements:
            self.movements.extend([mov] * 10)

        self.publisher_ = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.msg_idx = 0
        self.running = True
        self.service_ = self.create_service(
            DrawingControl,
            '/drawing_control',
            self.drawing_control_callback
        )


    def laser_callback(self, data: LaserScan):
        newdata = LaserScan()
        newdata.header = data.header
        newdata.angle_min = data.angle_min
        newdata.angle_max = data.angle_max
        newdata.angle_increment = data.angle_increment
        newdata.time_increment = data.time_increment
        newdata.scan_time = data.scan_time
        newdata.range_min = data.range_min
        newdata.range_max = data.range_max

        # Convertir a listas modificables
        newdata.ranges = list(data.ranges)
        newdata.intensities = list(data.intensities)

        length = len(newdata.ranges)
        Index = int(self.Angle / 2 * length / 360)

        # Filtrado por distancia
        for i in range(length):
            if newdata.ranges[i] > self.Dist:
                newdata.ranges[i] = float('inf')
                if len(newdata.intensities) > i:
                    newdata.intensities[i] = 0.0

        # Filtrado por ángulo
        for i in range(Index, length - Index):
            newdata.ranges[i] = float('inf')
            if len(newdata.intensities) > i:
                newdata.intensities[i] = 0.0

        if newdata.ranges and min(newdata.ranges) < self.safety_distance:
            self.obstacle = True
        else:
            self.obstacle = False


    def timer_callback(self):
        if self.msg_idx < len(self.movements) and self.running:
            if not self.obstacle and self.movements[self.msg_idx].linear.x != 0.0:
                self.publisher_.publish(self.movements[self.msg_idx])
                self.msg_idx += 1
        else:
            self.publisher_.publish(self.movements[-1])

    def timer_callback(self):
        if self.msg_idx < len(self.movements) and self.running:
            current_move = self.movements[self.msg_idx]

            if self.obstacle and current_move.linear.x != 0.0:
                self.publisher_.publish(create_twist(0.0, 0.0))
            else:
                self.publisher_.publish(current_move)
                self.msg_idx += 1
        else:
            self.publisher_.publish(create_twist(0.0, 0.0))

    
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

    collision_avoidance = CollisionAvoidance()

    rclpy.spin(collision_avoidance)

    collision_avoidance.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
