#!/usr/bin/env python
import os
import yaml
import rospy
import numpy as np
from sys import argv
from time import sleep, time
from std_srvs.srv import Empty
from assessment_package.msg import WeedList
from actionlib_msgs.msg import GoalStatusArray
from move_base_msgs.msg import MoveBaseActionGoal
from tf.transformations import quaternion_from_euler

class Hunter:
	def __init__(self, CONFIG):
		print("_HUNTER_init_")
		self.CONFIG = CONFIG
		ROB = CONFIG['sprayer_robot']
		
		self.weed_data = []
		self.movebase_stamp = []
		self.goal_send = 0
		
		self.spawner = rospy.ServiceProxy(CONFIG['spray_service'], Empty)
		self.weed_sub = rospy.Subscriber(ROB+CONFIG['row_data'], WeedList, self.scan_row)
		self.align = rospy.Publisher(ROB+CONFIG['movebase_goal'], MoveBaseActionGoal, queue_size = 2)
		self.waiter_for_status = rospy.Subscriber("/move_base/status", GoalStatusArray, self.waiter_status)
		self.waiter_for_publisher = rospy.Subscriber("/move_base/goal", MoveBaseActionGoal, self.waiter_publisher)
		#self.sway = rospy.Publisher(ROB+CONFIG['cmd_vel'], Twist, queue_size = 2)
		
		
		
		#when row detected, increment index
		#when row and sprayer are 2 apart, plot dijkstra against row data
		#move to each one in turn, 
		#when at the weed, 
		#move relative 0.5 forward, 
		#call sprayer
		#move to next node
		
		#Wait for thorvald_001 to complete the first 2 rows
		while not(rospy.is_shutdown()):
			if (len(self.weed_data) < 2):
				sleep(10)
				print("Row_count: " + str(len(self.weed_data)))
			else:
				print("yaya")
				lst = self.generate_list(self.weed_data.pop(0))
				
				print(lst)
				
				for weed in lst:
					self.move(weed)
					self.waiter()
					self.move_relative()
					self.waiter()
				
				
				
				
				
				
				
				
				
				
		
#--------------------------------------------------------------------------------------------------------	
	#Generate path list from CONFIG input
	def generate_list(self, weed_list):
		path = []
		w = weed_list.weeds.data
		
		for i in range(6):#len(w)):
			if (i%2):
				path.append((w[i], w[i-1], 0, weed_list.plant_type))
		
		return path
		
#--------------------------------------------------------------------------------------------------------	
	#Publisher for move_base/goal
	#INPUT: (position) must be a 3 element list defining [xcoord, ycoord, angle(degrees)]
	def move(self, position):
		print("------------------------------")
		print("Moving to: " + str(position[0]) + ", " + str(position[1]))
		goal = MoveBaseActionGoal()

		#Format Header
		goal.goal.target_pose.header.seq = 5
		goal.goal.target_pose.header.frame_id = CONFIG['map_frame']
		
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
		self.align.publish(goal)
		

	def move_relative(self):
		goal = MoveBaseActionGoal()
		goal.goal.target_pose.header.seq = 5 #optional (remove)
		goal.goal.target_pose.header.frame_id = self.CONFIG['sprayer_robot']+"/base_link"
		goal.goal.target_pose.pose.position.x = 0.5
		self.align.publish(goal)


#--------------------------------------------------------------------------------------------------------
	def waiter_status(self, data):
		self.status = data.status
		self.movebase_stamp = data.status_list[-1].goal_id.stamp.secs
	def waiter_publisher(self, data):
		self.goal_send = data.goal.target_pose.header.stamp.secs
	def waiter(self, time_publish=time()):
		print(time_publish)
		timeout = self.CONFIG['movebase_timeout']
		while True:
			print("tt")
			if (self.movebase_stamp == self.goal_send):
				if (self.status == 3):
					print("Goal Aborted: COMPLETED")
					return
				elif (self.status == 4):
					print("Goal Aborted: ABORTED")
					return
			if (time()-time_publish > timeout):
				print("Goal Aborted: TIMEOUT")
				return
		return
		
#--------------------------------------------------------------------------------------------------------
#	def twist_distance(self, d):
#		#twist takes velocity
#		#we want distance
#		#calculation:
#		# v=rw
#		d = 1
#
#		r = CONFIG['wheel_radius'] #radius
#		c = 1 #(2*np.pi*r) #circumfrance
#		
#		v = 1/c#m/s #CONFIG['const_velocity'] #velocity
#		t = d
#		
#	def twist(self, y, x=0):
#		t = Twist()
#		t.position.x = x
#		t.position.y = y
#		self.sway.publish(t)

#--------------------------------------------------------------------------------------------------------
	def scan_row(self, data):
		print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
		print("hihi")
		#print(data)
		self.weed_data.append(data)
		print(len(self.weed_data))
		
		
		
		
if __name__ == '__main__':
	yaml_path = argv[1]
	CONFIG = yaml.safe_load(open(yaml_path))
	
	rospy.init_node("HUNTER", anonymous=False)
	h = Hunter(CONFIG)
	rospy.spin()
