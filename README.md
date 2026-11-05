# Sprint 1
Paquete de control de `turtlesim`. `g01_prii3_turtlesim` contiene el nodo `turtlesim_control`, que dibuja automáticamente los números `01`. Este nodo funciona como servidor del servicio `drawing_control` para controlar la ejecución del dibujo según el comando del cliente.
## Requerimientos
- Ubuntu 22.04
- ROS Humble

## Funcionamiento
Todas las terminales que se abran deben obtener el entorno ROS underlay:
```bash
source /opt/ros/humble/setup.bash
```
1. Clonar el repositorio:
```bash
# por ssh
git clone git@github.com:joelsnz/g01_prii3_ws.git
# o por https
git clone https://github.com/joelsnz/g01_prii3_ws.git
```
2. En la raíz del proyecto, conseguir dependencias y construir:
```bash
rosdep install -i --from-path src --rosdistro humble -y
colcon build
```
3. Desde la raíz del proyecto (`g01_prii3_ws/`) en otra terminal, obtener el entorno overlay y ejecutar:
```bash
source install/local_setup.bash
ros2 launch src/g01_prii3_turtlesim/launch/turtlesim_control_launch.xml
```
4. Para controlar la ejecución del dibujo:
```bash
ros2 service call /drawing_control g01_prii3_interfaces/srv/DrawingControl "{command: <command>}"
```
Los comandos disponibles son `resume`, `restart` y `stop`.

# Sprint 2
Se han creado dos paquetes, `g01_prii3_move_jetbot` y `g01_prii3_move_turtlebot`. El primer paquete contiene programas relacionados con el robot real, el segundo con la simulación Gazebo.

Ambos paquetes contienen exactamente los mismos nodos, (`draw_number` para el movimiento autónomo del robot y `collision_avoidance` para la evitación de obstáculos), pues los programas son directamente trasladables del robot a la simulación.

1. Como en el Sprint 1, clonar el repositorio.
2. También como en el Sprint 1, compilar.
3. Desde la raíz del proyecto, obtener overlay y ejecutar:
```bash
source install local_setup.bash
```
- En el caso de la simulación:
    1. Ejecutar uno de los dos nodos:
```bash
ros2 launch src/g01_prii3_move_turtlebot/launch/turtlebot_draw_number.py
```
o
```bash
ros2 launch src/g01_prii3_move_turtlebot/launch/turtlebot_collision_avoidance.py
```

- En el caso del robot real:
1. Conectarse al robot por ssh:
```bash
ssh jetbot@<ip> # contraseña: jetbot
```
2. Realizar pasos 1, 2 y 3 dentro del robot.
3. Ejecutar el nodo de control del robot:
```bash
ros2 launch jetbot_pro_ros2 jetbot.py
```
4. Ejecutar uno de los dos nodos:
```bash
ros2 run g01_prii3_move_jetbot draw_number
```
o
```bash
ros2 run g01_prii3_move_turtlebot collision_avoidance
```

4. Como en el Sprint 1, se puede pausar, reanudar y reiniciar el dibujo:
```bash
ros2 service call /drawing_control g01_prii3_interfaces/srv/DrawingControl "{command: <command>}"
```
Los comandos disponibles son `resume`, `restart` y `stop`.
