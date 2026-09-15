# g01_prii3_ws
Se asume que todas las terminales usadas han obtenido el entorno ROS:
```sh
source /opt/ros/humble/setup.bash
```
1. Clonar el repo:
```sh
git clone git@github.com:joelsnz/g01_prii3_ws.git
```
2. Desde la raíz del proyecto (`g01_prii3_ws/`):
```sh
rosdep install -i --from-path src --rosdistro lyrical -y
colcon build
```
3. Desde la raíz del proyecto (`g01_prii3_ws/`) en otra terminal:
```sh
source install/local_setup.bash
ros2 run turtlesim turtlesim_node
```
