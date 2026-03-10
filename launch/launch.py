from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    location = Node(
        package="rmcs_local_map",
        executable="local_map",
        parameters=[[FindPackageShare("rmcs_local_map"), "/config", "/local_map.yaml"]],
        output="log",
    )
    launch = LaunchDescription()
    launch.add_action(location)

    return launch
