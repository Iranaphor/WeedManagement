#!/usr/bin/env python

import rospy
import os
from sys import argv
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest, DeleteModel, DeleteModelRequest
from std_srvs.srv import Empty
from std_msgs.msg import String
from uuid import uuid4
from geometry_msgs.msg import Point
import yaml

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
		  <ixx>0.00083</ixx>	   <!-- for a box: ixx = 0.083 * mass * (y*y + z*z) -->
		  <ixy>0.0</ixy>		 <!-- for a box: ixy = 0 -->
		  <ixz>0.0</ixz>		 <!-- for a box: ixz = 0 -->
		  <iyy>0.00083</iyy>	   <!-- for a box: iyy = 0.083 * mass * (x*x + z*z) -->
		  <iyz>0.0</iyz>		 <!-- for a box: iyz = 0 -->
		  <izz>0.0000083</izz>	   <!-- for a box: izz = 0.083 * mass * (x*x + y*y) -->
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


class Killer:

	def __init__(self, CONFIG):
		print("_KILLER_init_")
		self.CONFIG = CONFIG
		self.robot_name = CONFIG['sprayer_robot']

		#Spawnable object XML data
		self.sdf = BOX_SDF
		self.sdf2 = BOX_SDF2

		#Define Service System for Spraying
		rospy.Service(self.robot_name+CONFIG['spray_service'], Empty, self.spray) #Define service listener
		self.spawner = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnModel) #Define service publisher

		#Subscriber to plot box on defined coordinate
		self.plot_point = rospy.Subscriber(self.robot_name+CONFIG['spray_point'], Point, self.plot_point)


		#Defunct Code (Systems related to the automated removal of killboxes)
		#self.allmodels = []
		#self.remover = rospy.ServiceProxy("/gazebo/delete_model", DeleteModel)
		#self.plot_point = rospy.Subscriber("weed_killer/reset", String, self.reset)

	#def reset(self, data):
		#print(self.allmodels)
		#d = DeleteModelRequest()
		#for model in self.allmodels:
			#d.model_name = model
			#self.remover(model)


	def spray(self, r):
		print("uwu")
		try:
			request = SpawnModelRequest()
			request.model_name = 'killbox_%s' % uuid4()
			request.model_xml = self.sdf
			request.reference_frame = 'thorvald_002/base_link'
			request.initial_pose.position.z = 0.005
			request.initial_pose.position.x = -0.45
			request.initial_pose.orientation.w = 1.0
			self.spawner(request)
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
		print("owo")
		return []

	def plot_point(self, r):
		request = SpawnModelRequest()
		request.model_name = 'killbox_%s' % uuid4()#"point_"+str(r.x)+"_"+str(r.y)+"_"+str(uuid4())
		#self.allmodels.append(str(request.model_name))
		#print("PLOT: " + request.model_name)
		request.model_xml = self.sdf2
		request.reference_frame = "map"#self.CONFIG['map_frame']
		request.initial_pose.position.x = r.x
		request.initial_pose.position.y = r.y
		request.initial_pose.position.z = 0.2
		request.initial_pose.orientation.w = 1.0
		self.spawner(request)


if __name__ == "__main__":

	yaml_path = argv[1]
	CONFIG = yaml.safe_load(open(yaml_path))

	rospy.init_node("KILLER", anonymous=False)
	k = Killer(CONFIG)
	rospy.spin()


#os.system("rosservice call /thorvald_001/spray")







