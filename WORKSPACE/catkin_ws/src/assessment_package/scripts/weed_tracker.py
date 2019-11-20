#!/usr/bin/env python
import rospy
import os
from sys import argv
from std_srvs.srv import Empty
from std_msgs.msg import String

class CONTROL:
	def __init__(self, sprayer_robot_name):
		print("sprayer_init")
		self.spawner = rospy.ServiceProxy("weed_killer/spray", Empty)
		rospy.Subscriber("/spray", String, self.callback)

	def callback(self, data):
		print("Spraying Weed: " + str(data))
		self.spawner()


		

if __name__ == '__main__':
	print("hello")
	rospy.init_node("weed_tracker")
	c = CONTROL(argv[1])
	rospy.spin()


#os.system("rosservice call /thorvald_001/spray")




