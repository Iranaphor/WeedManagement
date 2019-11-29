#!/bin/sh

sudo apt-get purge "*gazebo*"
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install \
	ros-kinetic-uol-cmp9767m-base \
	ros-kinetic-uol-cmp9767m-tutorial

sudo apt-get install \
	ros-kinetic-image-view \
	ros-kinetic-rqt-graph \
	ros-kinetic-rviz

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

sudo chmod +777 LOADER.sh
./LOADER.sh
