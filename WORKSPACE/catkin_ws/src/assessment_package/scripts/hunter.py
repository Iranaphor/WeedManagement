#!/usr/bin/env python
import os
import yaml
import rospy
import numpy as np
from sys import argv
from time import sleep, time
from std_srvs.srv import Empty
from std_msgs.msg import String
from geometry_msgs.msg import Point
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
		self.total_rows_completed = 0

		#Sprayer Systems
		self.spawner = rospy.ServiceProxy(ROB+CONFIG['spray_service'], Empty)
		self.plot_type = rospy.Publisher(ROB+CONFIG['spray_type'], String, queue_size = 2)
		self.plot_point = rospy.Publisher(ROB+CONFIG['spray_point'], Point, queue_size = 2)

		#Data stream
		self.weed_sub = rospy.Subscriber(ROB+CONFIG['row_data'], WeedList, self.scan_row)

		#Movement Systems
		self.align = rospy.Publisher(ROB+CONFIG['movebase_goal'], MoveBaseActionGoal, queue_size = 2)
		self.waiter_for_status = rospy.Subscriber(ROB+CONFIG['movebase_status'], GoalStatusArray, self.waiter_status)
		self.waiter_for_publisher = rospy.Subscriber(ROB+CONFIG['movebase_goal'], MoveBaseActionGoal, self.waiter_publisher)
		sleep(1)
		
		#Begin at home station 
		self.move_home()
		self.waiter()
		
		#Wait for thorvald_001 to complete the first 2 rows
		self.move_through_weeds()			
		
		#Once complete, return to home station 
		self.move_home()
		self.waiter()
		rospy.shutdown()
		

#-------------------------------------------------------------------------------------------------------- Communications
	#Save input from detector
	def scan_row(self, data):
		print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
		print("Row Scan Incoming ...")
		#print(data)
		self.weed_data.append(data)
		print("Row Scan Complete | "+data.plant_type+" | len(self.weed_data)=" + str(len(self.weed_data)))
		
		
#-------------------------------------------------------------------------------------------------------- Path Generation
	#Generate path list from row_scan
	def generate_list(self, weed_list):
		path = []
		w = weed_list.weeds.data
		
		for i in range(len(w)):
			if (i%2):
				path.append((w[i-1], w[i], 0, weed_list.plant_type))
		
		return path

#-------------------------------------------------------------------------------------------------------- Navigation					
	def move_through_weeds(self):
		while not(rospy.is_shutdown()): #total_rows_completed < len(self.CONFIG['row_details'])
			#try:
			if (len(self.weed_data) < 2):
				if (len(self.weed_data) == 1):
					if self.weed_data[0].plant_type == "home":
						return
				sleep(10)
				print("----------------------")
				print("----------------------")
				print(self.weed_data)
				print("Row_count: " + str(len(self.weed_data)))
			else:
				print("\\(^,^)/ Node printing! :D  |  " + self.weed_data[0].plant_type)
				lst = self.generate_list(self.weed_data.pop(0))
				print(lst[0:10])
				for weed in lst:
					#print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
					self.plot_point.publish(Point(weed[0],weed[1],0))
					print("Moving to Weed")
					self.move(weed)
					self.waiter()
					print("Spraying ...")
					self.plot_type.publish(String(weed[3]))
					print("Spraying Complete")
					sleep(0.05)
					print("\\(^,^)/ next node! ")# + lst.plant_type)
			#except:
			#	print("Unknown Error")
				
	def move_home(self):
		home = self.CONFIG['sprayer_robot_base']
		self.move([home[1], home[0], 0, 'null'])
		
		
		
	#Publisher for move_base/goal
	#INPUT: (position) must be a 3 element list defining [xcoord, ycoord, angle(degrees)]
	def move(self, position):
		print("Moving to: " + str(position[0]) + ", " + str(position[1]))
		goal = MoveBaseActionGoal()

		#Format Header
		goal.goal.target_pose.header.seq = 5
		goal.goal.target_pose.header.frame_id = CONFIG['map_frame']
		
		#Add Publish-Time to Stamp
		self.timestamp = rospy.Time.now()
		goal.goal.target_pose.header.stamp = self.timestamp
		goal.goal_id.stamp = self.timestamp

		#Format Target-Pose Position
		goal.goal.target_pose.pose.position.x = position[0]+0.5
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


#-------------------------------------------------------------------------------------------------------- Movebase Progress Management
	def waiter_status(self, data):
		if len(data.status_list)>0:
			self.status = data.status_list[-1].status
			self.movebase_stamp = data.status_list[-1].goal_id.stamp.secs
	def waiter_publisher(self, data):
		self.goal_send = data.goal.target_pose.header.stamp.secs
	def waiter(self):
		time_publish=rospy.Time.now()
		timeout = self.CONFIG['movebase_timeout']
		try:
			while True:
				if (self.movebase_stamp == self.goal_send):
					if (self.status == 3):
						print("Goal Status: COMPLETED")
						break
					elif (self.status == 4):
						print("Goal Status: ABORTED")
						break
				if (rospy.Time.now()-time_publish > rospy.Duration.from_sec(timeout)):
					print("Goal Status: TIMEOUT")
					break
		except e:
			print(e)
			return
		return
		
#-------------------------------------------------------------------------------------------------------- Communications
	def scan_row(self, data):
		print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
		print("Row Scan Incoming ...")
		#print(data)
		self.weed_data.append(data)
		print("Row Scan Complete | "+data.plant_type+" |len(self.weed_data)=" + str(len(self.weed_data)))
		
		
		
		
		
if __name__ == '__main__':
	yaml_path = argv[1]
	CONFIG = yaml.safe_load(open(yaml_path))
	
	rospy.init_node("HUNTER", anonymous=False)
	h = Hunter(CONFIG)
	rospy.spin()
