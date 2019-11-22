#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from assessment_package.msg import weed_location
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionFeedback

from sys import argv
import os
import yaml

class navigation_manager:

	def __init__(self, yaml_path):
		print("navigation_manager.__init()__")

		#with open(yaml_path) as file:
			#documents = yaml.safe_load(file)
		path_details = yaml.safe_load(open(yaml_path))
		path = self.generate_list(path_details)
		print(path)
		self.weed_found = rospy.Publisher('/weed_found', weed_location)
		self.move_base_goal = rospy.Publisher("/move_base/goal", MoveBaseActionGoal, queue_size = 2)
		self.subscriberF1 = rospy.Subscriber("/move_base/status", GoalStatusArray, self.movebase_status)
	
	def generate_list(self, path_details):
		path = []
		for row in enumerate(path_details['row_location_x']):
			if (row[0]%2==0):
				path.append((row[1],path_details['row_start_y']))
				path.append((row[1],path_details['row_end_y']))
			else:
				path.append((row[1],path_details['row_end_y']))
				path.append((row[1],path_details['row_start_y']))	
		return path
		
	def move_in_path(self):
		#movebase(self.path[0])
		#self.goal_time = movebase.goal_time
		
	def movebase_status(self, data):
		#http://docs.ros.org/melodic/api/actionlib_msgs/html/msg/GoalStatus.html
		#if(len(data.status_list)>0):
			#self.GOAL_STATUS = data.status_list[-1].text
			#self.GOAL_TIME = data.status_list[-1].goal_id.stamp
			
			#if data.status == 'completed' && self.goal_time!=data.goal_time
				#self.path[0]=[]
				#self.move_in_path()

		
			

if __name__ == '__main__':
	print("---------------------------------------")
	path = os.path.dirname(argv[0])
	#robot_name = argv[1]
	rospy.init_node("navigator", anonymous=False)
	
	#nm = navigation_manager(argv[2])
	nm = navigation_manager('/home/computing/Thorvald/WORKSPACE/catkin_ws/src/assessment_package/config/navigation_targets.yaml')
	rospy.spin()


























