#!/bin/sh

cd WORKSPACE/catkin_ws
rm -rf build
catkin_make

#source /opt/ros/kinetic/setup.bash
source ./WORKSPACE/catkin_ws/devel/setup.bash

#roslaunch uol_cmp9767m_base thorvald-sim.launch obstacles:=false second_robot:=true map_server:=true
#NO MORE #roslaunch uol_cmp9767m_tutorial move_base.launch
#roslaunch assessment_package setup.launch

#rosrun rviz rviz

#https://github.com/LCAS/CMP9767M/wiki/Workshop-1---Introduction-and-ROS-Basics

#http://wiki.ros.org/rviz/UserGuide
#https://github.com/LCAS/teaching/wiki/CMP3103M
#http://wiki.ros.org/ROS/Tutorials/CreatingPackage
#http://wiki.ros.org/amcl
#https://github.com/ANYbotics/grid_map
