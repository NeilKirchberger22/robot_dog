from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description(): 

    config = os.path.join(
    get_package_share_directory('robot_description'),
    'config',
    'controllers.yaml'
    )

    controller_manager = Node(
        package= 'controller_manager', 
        executable='ros2_control_node',
        parameters=[config],
        output= 'screen'
    )

    joint_states_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen'
    )

    leg_controller = Node(
        package='controller_manager', 
        executable= 'spawner',
        arguments=['leg1_controller'],
        output='screen'

    )

    input_node = Node(
        package= 'robot_description', 
        executable= 'inputs', 
        name='input_node',
        output='screen'

    )

    walk_node = Node(
        package= 'robot_description', 
        executable= 'walk', 
        name='walk_node',
        output='screen'

    )

    return LaunchDescription([
        controller_manager, 
        joint_states_broadcaster, 
        leg_controller,
        input_node, 
        walk_node
    ])