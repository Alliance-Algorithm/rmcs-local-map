from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    config = [
        FindPackageShare("rmcs_local_map"), "/config", "/local_map.yaml"
    ]
    location = Node(
        package="rmcs_local_map",
        executable="local_map",
        parameters=[config],
        output="log",
    )
    launch = LaunchDescription()
    launch.add_action(location)

    return launch
