import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (Command, FindExecutable, LaunchConfiguration,
                                  PathJoinSubstitution)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from datetime import date
from datetime import datetime


def generate_launch_description():

    # Husky Base/Navigation launch
    nav_launch_path = os.path.join(get_package_share_directory('trailbot_bringup'),'launch','nav.launch.py')
    nav_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource([nav_launch_path]))


    fsm_node = Node(
        package='fsm',
        executable='trailbot_fsm',
        name='fsm',
        output='screen'
    )

    navigator_node = Node(
        package='fsm',
        executable='navigator_node',
        name='test_cmd_vel_node',
        output='screen'
    )

    # Launch voice_assistant/voice_assistant.launch.py which is voice interaction.
    launch_voice_assistant = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution(
            [FindPackageShare("voice_assistant"), 'launch', 'voice_assistant.launch.py'])))

    # Launch human detection
    human_detection_node = Node(
        package='human_detection',
        executable='human_detection_node'
    )

    # Launch file logging
    current_date = date.today()
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    file_logging = ExecuteProcess(
        cmd=['ros2', 'bag', 'record', '-o', f'/home/trailbot/bags/{current_date}-{formatted_time}','-a','-x','/camera'],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(nav_launch)
    ld.add_action(fsm_node)
    ld.add_action(navigator_node)
    ld.add_action(launch_voice_assistant)
    ld.add_action(human_detection_node)
    ld.add_action(file_logging)

    return ld
