# g01_prii3_ws
Se asume que todas las terminales usadas han obtenido el entorno ROS:
```bash
source /opt/ros/jazzy/setup.bash
```
1. Clonar el repo:
```bash
git clone git@github.com:joelsnz/g01_prii3_ws.git
```
2. Desde la raíz del proyecto (`g01_prii3_ws/`):
```bash
rosdep install -i --from-path src --rosdistro jazzy -y
colcon build
```
3. Desde la raíz del proyecto (`g01_prii3_ws/`) en otra terminal:
```bash
source install/local_setup.zsh
```
