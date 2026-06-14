import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pick_and_place_dir = get_package_share_directory('pick_and_place')
    ur_simulation_dir = get_package_share_directory('ur_simulation_gazebo')
    ur_moveit_dir = get_package_share_directory('ur_moveit_config')

    world_file = os.path.join(pick_and_place_dir, 'worlds', 'pick_world.sdf')

    # 1 — Launch Gazebo + UR5
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

    # 2 — Launch MoveIt2 (after 5 seconds — wait for Gazebo to start)
    moveit_launch = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(ur_moveit_dir, 'launch', 'ur_moveit.launch.py')
                ),
                launch_arguments={
                    'ur_type': 'ur5',
                    'launch_rviz': 'true',
                }.items()
            )
        ]
    )

    # 3 — Launch Object Detector (after 8 seconds)
    object_detector = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='pick_and_place',
                executable='object_detector',
                name='object_detector',
                output='screen',
            )
        ]
    )

    # 4 — Launch Pick and Place Node (after 10 seconds)
    pick_and_place_node = TimerAction(
        period=10.0,
        actions=[
            Node(
                package='pick_and_place',
                executable='pick_and_place_node',
                name='pick_and_place_node',
                output='screen',
            )
        ]
    )

    return LaunchDescription([
        ur_sim_launch,
        moveit_launch,
        object_detector,
        pick_and_place_node,
    ])
