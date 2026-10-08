from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():
    launch_dir = PathJoinSubstitution([FindPackageShare('turtlebot3_gazebo'), 'launch'])
    
    return LaunchDescription([
        SetEnvironmentVariable(
            name = 'TURTLEBOT3_MODEL',
            value = 'burger'
        ),

        IncludeLaunchDescription([
            PathJoinSubstitution([launch_dir, 'empty_world.launch.py'])
        ]),

        Node(
            package = 'g01_prii3_move_turtlebot',
            executable = 'draw_number',
            parameters=[{'use_sim_time': True}]
        )
    ])
