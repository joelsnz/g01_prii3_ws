# Sprint 1
# Requerimientos
- Ubuntu 22.04
- ROS Jazzy

# Funcionamiento
Todas las terminales que se abran deben obtener el entorno ROS underlay:
```bash
source /opt/ros/jazzy/setup.bash
```
1. Clonar el repositorio:
```bash
# por ssh
git clone git@github.com:joelsnz/g01_prii3_ws.git
# o por https
git clone https://github.com/joelsnz/g01_prii3_ws.git
```
2. Ir a la raíz del proyecto, conseguir dependencias y construir:
```bash
cd g01_prii3_ws/
rosdep install -i --from-path src --rosdistro jazzy -y
colcon build
```
3. Desde la raíz del proyecto (`g01_prii3_ws/`) en otra terminal, obtener el entorno overlay y ejecutar:
```bash
source install/local_setup.zsh
ros2 launch src/g01_prii3_turtlesim/launch/turtlesim_control_launch.xml
```
4. Para controlar la ejecución del dibujo:
```bash
ros2 service call /drawing_control g01_prii3_interfaces/srv/DrawingControl "{command: <command>}"
```
Los comandos disponibles son `resume`, `restart` y `stop`.
