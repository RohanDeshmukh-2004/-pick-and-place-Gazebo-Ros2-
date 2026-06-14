import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Get package paths
    pick_and_place_dir = get_package_share_directory('pick_and_place')
    ur_simulation_dir = get_package_share_directory('ur_simulation_gazebo')

    # World file path
    world_file = os.path.join(pick_and_place_dir, 'worlds', 'pick_world.sdf')

    # Launch UR5 simulation with our custom world
    ur_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ur_simulation_dir, 'launch', 'ur_sim_control.launch.py')
        ),
        launch_arguments={
            'ur_type': 'ur5',
            'launch_rviz': 'false',
            'world_file': world_file,
        }.items()
    )

    return LaunchDescription([
        ur_sim_launch,
    ])
