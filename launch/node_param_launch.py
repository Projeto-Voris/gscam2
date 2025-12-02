"""Launch a Node with parameters and remappings."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    camera_param = PathJoinSubstitution([FindPackageShare('gscam2'), 'cfg','bluerov2.ini'])

    return LaunchDescription([

        DeclareLaunchArgument('namespace', default_value='bluerov2', description='namespace'),
        DeclareLaunchArgument('image_topic', default_value='image_raw', description='image topic'),
        DeclareLaunchArgument('camera_info', default_value='camera_info', description='camera info topic'),
        DeclareLaunchArgument('camera_config', default_value=['file://', camera_param], description='Number of images to acquire'),
        DeclareLaunchArgument('param_file', default_value=PathJoinSubstitution([FindPackageShare('gscam2'), 'cfg', 'params.yaml'])),
        
        Node(
            package='gscam2',
            executable='gscam_main',
            output='screen',
            name='gscam_publisher',
            namespace=LaunchConfiguration('namespace'),
            parameters=[
                # Some parameters from a yaml file
                LaunchConfiguration('param_file'),
                # A few more parameters
                {
                    'camera_name': LaunchConfiguration('namespace'),  # Camera Name
                    'camera_info_url': LaunchConfiguration('camera_config'),  # Camera calibration information
                },
            ],
            # Remap outputs to the correct namespace
            remappings=[
                ('/image_raw', LaunchConfiguration('image_topic')),
                ('/camera_info', LaunchConfiguration('camera_info')),
            ],
        )
    ])
