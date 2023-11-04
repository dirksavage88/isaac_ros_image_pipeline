# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import launch
from launch_ros.actions import ComposableNodeContainer, Node
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    disparity_node = ComposableNode(
        name='disparity',
        package='isaac_ros_stereo_image_proc',
        plugin='isaac_ros::stereo_image_proc::DisparityNode',
        parameters=[{
                'backends': 'CUDA',
                'max_disparity': 64,
        }],
        remappings=[('/left/image_rect', '/left/image_raw'),('/right/image_rect', '/right/image_raw')])

    pointcloud_node = ComposableNode(
        package='isaac_ros_stereo_image_proc',
        plugin='isaac_ros::stereo_image_proc::PointCloudNode',
        parameters=[{
                'use_color': True,
        }],
        remappings=[('/left/image_rect_color', '/left/image_raw')])

    container = ComposableNodeContainer(
        name='disparity_container',
        namespace='disparity',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[disparity_node, pointcloud_node],
        output='screen'
    )

    return (launch.LaunchDescription([container]))
