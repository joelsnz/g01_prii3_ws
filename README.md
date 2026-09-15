# g01_prii3_ws
Se asume que todas las terminales usadas han obtenido el entorno ROS:
```
source /opt/ros/humble/setup.bash
```
Clonar el repo:
```
git clone git@github.com:joelsnz/g01_prii3_ws.git
```
Desde la raíz del proyecto (`g01_prii3_ws/`):
```
rosdep install -i --from-path src --rosdistro lyrical -y
colcon build
```
Desde la raíz del proyecto (`g01_prii3_ws/`) en otra terminal:
```
source install/local_setup.bash
ros2 run turtlesim turtlesim_node
```
