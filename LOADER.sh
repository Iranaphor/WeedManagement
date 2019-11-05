#!/bin/sh

sudo apt-get update && sudo apt-get upgrade
sudo apt-get purge "*gazebo*"
sudo apt-get install ros-kinetic-uol-cmp9767m-base
sudo apt-get install ros-kinetic-uol-cmp9767m-tutorial
sudo apt-get install ros-kinetic-image-view
sudo apt-get install ros-kinetic-rqt-graph
sudo apt-get install ros-kinetic-rviz

sudo apt-get install \
    ros-kinetic-robot-localization \
    ros-kinetic-topological-navigation \
    ros-kinetic-amcl \
    ros-kinetic-fake-localization \
    ros-kinetic-carrot-planner

sudo python -m easy_install --upgrade pyOpenSSL
sudo python -m pip install --upgrade setuptools
sudo python -m pip install --upgrade pip
sudo python -m pip install matplotlib


cd ./Thorvald/WORKSPACE/catkin_ws
rm -rf build
catkin_make

source /opt/ros/kinetic/setup.bash &
roslaunch uol_cmp9767m_base thorvald-sim.launch obstacles:=false second_robot:=true map_server:=true &
roslaunch uol_cmp9767m_tutorial move_base.launch &

#rosrun rviz rviz

#https://github.com/LCAS/CMP9767M/wiki/Workshop-1---Introduction-and-ROS-Basics

#http://wiki.ros.org/rviz/UserGuide
#https://github.com/LCAS/teaching/wiki/CMP3103M
#http://wiki.ros.org/ROS/Tutorials/CreatingPackage
#http://wiki.ros.org/amcl
#https://github.com/ANYbotics/grid_map
