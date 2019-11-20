#!/usr/bin/env python
import rospy

class CONTROL:
	def __init__(self):
		print("sprayer_init")

if __name__ == '__main__':
	print("hello")
	rospy.init_node('sprayer')
	c = CONTROL()
	rospy.spin()


#os.system("rosservice call /thorvald_001/spray")




