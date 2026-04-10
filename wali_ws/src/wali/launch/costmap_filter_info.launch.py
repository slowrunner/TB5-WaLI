"""
costmap_filter_info.launch.py  (wali package)

Launches the costmap_filter_info map_server for keepout zones.
Assumes the primary costmap map_server is already running.

Command-line arguments:
  keepout_map         -- full path to the keepout filter map yaml file
  keepout_params_file -- full path to the keepout filter params yaml file
  use_sim_time        -- use simulation time (default: false)

Example:
  ros2 launch wali costmap_filter_info.launch.py \
      keepout_map:=/path/to/keepout_map.yaml \
      keepout_params_file:=/path/to/keepout_params.yaml
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # ------------------------------------------------------------------ #
    #  Launch arguments                                                    #
    # ------------------------------------------------------------------ #

    declare_keepout_map = DeclareLaunchArgument(
        'keepout_map',
        description='Full path to the keepout / speed-filter map yaml file.'
    )

    declare_keepout_params_file = DeclareLaunchArgument(
        'keepout_params_file',
        description='Full path to the keepout costmap filter info params yaml.'
    )

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true. Default: false.'
    )

    # ------------------------------------------------------------------ #
    #  Convenience substitutions                                           #
    # ------------------------------------------------------------------ #

    keepout_map         = LaunchConfiguration('keepout_map')
    keepout_params_file = LaunchConfiguration('keepout_params_file')
    use_sim_time        = LaunchConfiguration('use_sim_time')

    # ------------------------------------------------------------------ #
    #  costmap_filter_info server — keepout filter                         #
    # ------------------------------------------------------------------ #
    #
    #  Publishes /costmap_filter_info so the keepout layer knows which
    #  map topic to read and how to interpret it.
    #
    #  The companion map_server (below) serves the actual keepout mask.
    # ------------------------------------------------------------------ #

    costmap_filter_info_server = Node(
        package='nav2_map_server',
        executable='costmap_filter_info_server',
        name='costmap_filter_info_server',
        output='screen',
        emulate_tty=True,
        parameters=[
            keepout_params_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    # ------------------------------------------------------------------ #
    #  map_server — serves the keepout / speed filter mask map             #
    # ------------------------------------------------------------------ #
    #
    #  This is a *separate* map_server from the one serving the main
    #  navigation map.  It is namespaced to avoid topic collisions.
    #  The costmap_filter_info_server params file should point its
    #  filter_info_topic and mask_topic at the topics published here.
    # ------------------------------------------------------------------ #

    filter_mask_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='filter_mask_server',
        output='screen',
        emulate_tty=True,
        parameters=[
            keepout_params_file,        # contains filter mask map topic name
            {'use_sim_time': use_sim_time,
             'yaml_filename':  keepout_map}
        ],
        remappings=[('/map', '/keepout_filter_mask')],    # added b/c map_server defaults to /map
    )

    # ------------------------------------------------------------------ #
    #  lifecycle manager — manages both filter nodes                       #
    # ------------------------------------------------------------------ #
    #
    #  Does NOT include the main map_server (assumed already running).
    # ------------------------------------------------------------------ #

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_costmap_filters',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'use_sim_time':  use_sim_time,
            'autostart':     True,
            'node_names': [
                'costmap_filter_info_server',
                'filter_mask_server',
            ]
        }]
    )

    # ------------------------------------------------------------------ #
    #  LaunchDescription                                                   #
    # ------------------------------------------------------------------ #

    return LaunchDescription([
        declare_keepout_map,
        declare_keepout_params_file,
        declare_use_sim_time,

        costmap_filter_info_server,
        filter_mask_server,
        lifecycle_manager,
    ])
