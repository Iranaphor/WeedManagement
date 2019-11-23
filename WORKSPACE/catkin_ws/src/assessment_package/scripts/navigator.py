#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from assessment_package.msg import weed_location
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionFeedback
from actionlib_msgs.msg import GoalStatusArray
from tf.transformations import quaternion_from_euler

from sys import argv
import os
import yaml
from time import sleep
import numpy as np

class navigation_manager:

	def __init__(self, robot_name, yaml_path):
		print("navigation_manager.__init()__")

		#Save inputs
		self.robot_name = robot_name
		self.yaml_path = yaml_path
		
		#Variable initialisation
		self.s=""
		self.goal_send = rospy.Time.now()

		#Read and format the robot path from the yaml
		path_details = yaml.safe_load(open(yaml_path)) #TODO: Add condition to skip this and just input the path as a yaml itself
		self.path_raw = self.generate_list(path_details)
		self.path = self.path_raw[:]
		print(self.path)

		#Initialise Publishers and Subscribers
		self.move_base_goal = rospy.Publisher("/"+robot_name+"/move_base/goal", MoveBaseActionGoal, queue_size = 2)
		self.move_base_status = rospy.Subscriber("/"+robot_name+"/move_base/goal", MoveBaseActionGoal, self.movebase_goal_tracker)
		self.move_base_status = rospy.Subscriber("/"+robot_name+"/move_base/status", GoalStatusArray, self.movebase_status)
		sleep(1) #sleep to enable the movebase publisher to respond

		#Move to first position
		self.move(self.path[0])
	
	#Generate path list from yaml input
	def generate_list(self, path_details):
		path = []
		for row in enumerate(path_details['row_location_x']):
			#Switch to enable snaking through rows
			if (row[0]%2==0):
				path.append((path_details['row_start_y'],row[1],180))
				path.append((path_details['row_end_y'],row[1],0)) #TODO add angle definition based on the direction
			else:
				path.append((path_details['row_end_y'],row[1],0))
				path.append((path_details['row_start_y'],row[1],180)) #TODO add angle definition based on the direction
		return path
	

	#Publisher for move_base/goal
	#INPUT: (position) must be a 3 element list defining [xcoord, ycoord, angle(degrees)]
	def move(self, position):
		print("------------------------------")
		print("Moving to: " + str(position[0]) + ", " + str(position[1]))
		goal = MoveBaseActionGoal()

		#Format Header
		goal.goal.target_pose.header.seq = 5
		goal.goal.target_pose.header.frame_id = 'map'
		
		#Add Publish-Time to Stamp
		a = rospy.Time.now()
		goal.goal.target_pose.header.stamp = a
		goal.goal_id.stamp = a

		#Format Target-Pose Position
		goal.goal.target_pose.pose.position.x = position[0]
		goal.goal.target_pose.pose.position.y = position[1]
		
		#Format Target-Pose Orientation
		#Resolve issues with invalid quarternians
		angle = position[2]
		angle = 179.99 if np.mod(angle+180, 360)==0 else angle
		orientat = quaternion_from_euler(0, 0, angle*(np.pi/180))
		goal.goal.target_pose.pose.orientation.x = orientat[0]
		goal.goal.target_pose.pose.orientation.y = orientat[1]
		goal.goal.target_pose.pose.orientation.z = orientat[2]
		goal.goal.target_pose.pose.orientation.w = orientat[3]
		
		#Publish Goal
		self.move_base_goal.publish(goal)
	
	#Subscriber to track the publish time for the goal
	#This is used to manage external move_base goals
	def movebase_goal_tracker(self, data): #TODO: ISSUE FOUND - When a new path is passed, the existing path does not continue from where it left off.
		self.goal_send = data.goal.target_pose.header.stamp.secs
		print("tracker: " + str(self.goal_send))
	
	#Tracker to see if the goal has been reached, and move the robot to the next goal
	def movebase_status(self, data):
		#http://docs.ros.org/melodic/api/actionlib_msgs/html/msg/GoalStatus.html

		if (len(data.status_list)>0):

			#Debug printout			
			sn="(" + str(len(data.status_list)) + ")("+ str(data.status_list[-1].status)+")("+str(self.goal_send)+":"+str(data.status_list[-1].goal_id.stamp.secs)+")("+str(len(self.path))+")"
			if (self.s != sn):
				print(self.s)
				self.s = sn

			#If goal completed and goal observed is goal of interest
			if (data.status_list[-1].status == 3) and (self.goal_send == data.status_list[-1].goal_id.stamp.secs):
				self.path.pop(0)

				#If loop completed, restart loop
				if (len(self.path) == 0):
					print("(6|PATH_LIST_EMPTY)")
					self.path = self.path_raw[:]
				
				#Move to next position
				self.move(self.path[0])
		else:
			print("(6|STATUS_LIST_EMPTY)")


if __name__ == '__main__':
	print("---------------------------------------")
	path = os.path.dirname(argv[0])
	
	#Manage args
	robot_name = "thorvald_001"
	yamlpath = '/home/computing/Thorvald/WORKSPACE/catkin_ws/src/assessment_package/config/navigation_targets.yaml'
	#robot_name = argv[1]
	#yamlpath = argv[2]
	
	rospy.init_node("navigator", anonymous=False)
	nm = navigation_manager(robot_name, yamlpath)
	rospy.spin()


























