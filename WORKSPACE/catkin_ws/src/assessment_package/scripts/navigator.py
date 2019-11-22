#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from assessment_package.msg import weed_location
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionFeedback
from actionlib_msgs.msg import GoalStatusArray

from sys import argv
import os
import yaml
from time import sleep

class navigation_manager:

	def __init__(self, yaml_path):
		print("navigation_manager.__init()__")

		path_details = yaml.safe_load(open(yaml_path))
		self.path = self.generate_list(path_details)
		print(self.path)
		self.goal_send = rospy.Time.now()
		self.move_base_goal = rospy.Publisher("/thorvald_001/move_base/goal", MoveBaseActionGoal, queue_size = 2)
		self.move_base_status = rospy.Subscriber("/thorvald_001/move_base/goal", MoveBaseActionGoal, self.movebase_goal_tracker)
		self.move_base_status = rospy.Subscriber("/thorvald_001/move_base/status", GoalStatusArray, self.movebase_status)
		sleep(1) #sleep to enable the movebase publisher to respond
		self.move(self.path.pop(0))
	
	def generate_list(self, path_details):
		path = []
		for row in enumerate(path_details['row_location_x']):
			if (row[0]%2==0):
				path.append((path_details['row_start_y'],row[1]))
				path.append((path_details['row_end_y'],row[1])) #TODO add angle definition based on the direction
			else:
				path.append((path_details['row_end_y'],row[1]))
				path.append((path_details['row_start_y'],row[1])) #TODO add angle definition based on the direction
		return path
	
	#Send message to mobve_base/goal
	def move(self, position):
		print("------------------------------")
		print("Moving to: " + str(position[0]) + ", " + str(position[1]))
		goal = MoveBaseActionGoal()
		goal.goal.target_pose.header.seq = 5
		goal.goal.target_pose.header.frame_id = 'map'
		goal.goal.target_pose.pose.position.x = position[0]
		goal.goal.target_pose.pose.position.y = position[1]
		goal.goal.target_pose.pose.orientation.w = 0.1 #TODO add angle definition based on the direction
		a = rospy.Time.now()
		print(a)
		goal.goal.target_pose.header.stamp = a
		goal.goal_id.stamp = a
		self.move_base_goal.publish(goal)
		#print(self.path)
		
	def movebase_goal_tracker(self, data):
		self.goal_send = data.goal.target_pose.header.stamp
		print("tracker: " + str(self.goal_send))
	
	def movebase_status(self, data):
		#http://docs.ros.org/melodic/api/actionlib_msgs/html/msg/GoalStatus.html
		if(len(self.path)>0):
			#print(data.status_list[-1].goal_id.stamp)
			if data.status_list[-1].status == 3:
				if self.goal_send == data.status_list[-1].goal_id.stamp:
					if (len(self.path) > 0):
						self.move(self.path.pop(0)) #move the pop till only when the target is met




if __name__ == '__main__':
	print("---------------------------------------")
	path = os.path.dirname(argv[0])
	#robot_name = argv[1]
	rospy.init_node("navigator", anonymous=False)
	
	#nm = navigation_manager(argv[2])
	nm = navigation_manager('/home/computing/Thorvald/WORKSPACE/catkin_ws/src/assessment_package/config/navigation_targets.yaml')
	rospy.spin()


























