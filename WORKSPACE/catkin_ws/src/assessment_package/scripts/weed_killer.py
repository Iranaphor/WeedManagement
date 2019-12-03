#!/usr/bin/env python

import rospy
import os
from sys import argv
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest
from std_srvs.srv import Empty
from uuid import uuid4
from geometry_msgs.msg import Point

BOX_SDF="""
<?xml version='1.0'?>
<sdf version="1.4">
<model name="killbox">
  <pose>0 0 0 0 0 0</pose>
  <static>true</static>
    <link name="link">
      <inertial>
        <mass>1.0</mass>
        <inertia> <!-- inertias are tricky to compute -->
          <!-- http://gazebosim.org/tutorials?tut=inertia&cat=build_robot -->
          <ixx>0.00083</ixx>       <!-- for a box: ixx = 0.083 * mass * (y*y + z*z) -->
          <ixy>0.0</ixy>         <!-- for a box: ixy = 0 -->
          <ixz>0.0</ixz>         <!-- for a box: ixz = 0 -->
          <iyy>0.00083</iyy>       <!-- for a box: iyy = 0.083 * mass * (x*x + z*z) -->
          <iyz>0.0</iyz>         <!-- for a box: iyz = 0 -->
          <izz>0.0000083</izz>       <!-- for a box: izz = 0.083 * mass * (x*x + y*y) -->
        </inertia>
      </inertial>
      <visual name="visual">
        <geometry>
          <box>
            <size>.1 .1 .01</size>
          </box>
        </geometry>
        <material>
            <ambient>1 0 0 1</ambient>
        </material>
      </visual>
    </link>
  </model>
</sdf>
"""
BOX_SDF2="""


<?xml version="1.0" encoding="UTF-8"?>
<sdf version="1.4">
   <model name="killbox">
      <pose>0 0 0 0 0 0</pose>
      <static>true</static>
      <link name="link_box">
         <visual name="visual">
            <geometry>
               <box>
                  <size>.01 .01 .01</size>
               </box>
            </geometry>
            <material>
               <ambient>0 0 0 1</ambient>
               <diffuse>0 0 0 1</diffuse>
               <specular>0 0 0 0</specular>
               <emissive>1 1 0 1</emissive>
            </material>
         </visual>
      </link>
      
   </model>
</sdf>


"""


class Sprayer:

    def __init__(self, robot_name):
	self.robot_name = robot_name
        self.sdf = BOX_SDF
        self.sdf2 = BOX_SDF2
        rospy.Service("weed_killer/spray", Empty, self.spray)
	self.plot_point = rospy.Subscriber("weed_killer/spray_topic", Point, self.plot_point)
        self.spawner = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnModel)

    def spray(self, r):
        request = SpawnModelRequest()
        request.model_name = 'killbox_%s' % uuid4()
        request.model_xml = self.sdf
        request.reference_frame = self.robot_name+"/base_link"
        request.initial_pose.position.z = 0.005
        request.initial_pose.position.x = -0.45
        request.initial_pose.orientation.w = 1.0
        self.spawner(request)
        return []

    def plot_point(self, r):
	print("Spraying")
        request = SpawnModelRequest()
        request.model_name = 'killbox_%s' % uuid4()
        request.model_xml = self.sdf2
        request.reference_frame = "/map"
        request.initial_pose.position.x = r.x
        request.initial_pose.position.y = r.y
        request.initial_pose.position.z = 0.2
        request.initial_pose.orientation.w = 1.0
        self.spawner(request)
        return []


if __name__ == "__main__":
    rospy.init_node("weed_killer")
    m2s = Sprayer(argv[1])
    rospy.spin()


#os.system("rosservice call /thorvald_001/spray")







