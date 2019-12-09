#!/usr/bin/env python
import rospy
import os
import yaml
from sys import argv
from std_srvs.srv import Empty
from assessment_package.msg import WeedList
from move_base_msgs.msg import MoveBaseActionGoal

class Hunter:
	def __init__(self, CONFIG):
		print("_HUNTER_init_")
		self.CONFIG = CONFIG
		ROB = CONFIG['sprayer_robot']
		self.spawner = rospy.ServiceProxy(CONFIG['spray_service'], Empty)
		self.weed_data = rospy.Subscriber(ROB+CONFIG['row_data'], WeedList, self.scan_row)
		self.align = rospy.Publisher(ROB+CONFIG['movebase_goal'], MoveBaseActionGoal, queue_size = 2)

	def move(self, position):
		goal = MoveBaseActionGoal()
		goal.goal.target_pose.header.seq = 5 #optional (remove)
		goal.goal.target_pose.header.frame_id = self.CONFIG['sprayer_robot']+"/base_link"
		goal.goal.target_pose.pose.position.x = 0.5
		self.align.publish(goal)

	def scan_row(self, data):
		print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
		print("hihi")
		print(data)
		
		
		#when row detected, increment index
		#when row and sprayer are 2 apart, plot dijkstra against row data
		#move to each one in turn, 
		#when at the weed, 
		#move relative 0.5 forward, 
		#call sprayer
		#move to next node
		
		
		
if __name__ == '__main__':
	yaml_path = argv[1]
	CONFIG = yaml.safe_load(open(yaml_path))
	
	rospy.init_node("HUNTER", anonymous=False)
	h = Hunter(CONFIG)
	rospy.spin()
