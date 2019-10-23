##########################################################################################################
# Error with reaccessing subplots within a figure, is understood and is fine.
# This is caused by similar behaviour between plt.subplot() and plt.add_subplot().
# The latter will be modified in v3.0, so this wil,l have no impact on this system.
# 
# 
# 
# 
# 
# 
##########################################################################################################

#ROSPY IMPORTS
import rospy
from std_msgs.msg import String, Int8
from sensor_msgs.msg import Image, LaserScan, JointState
from nav_msgs.msg import Odometry, OccupancyGrid
from geometry_msgs.msg import Twist, Quaternion, Pose, Point
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from src.image_processing.weed_detection import basil as _basil #, imreconstruct

#OPENCV IMPORTS
import cv2
from cv_bridge import CvBridge, CvBridgeError

#LIBRARIES IMPORTS
import numpy as np
import matplotlib.pyplot as plt

#PYTHON IMPORTS
import os
import subprocess
import sys
from sys import argv
import datetime
import time
from time import sleep





##########################################################################################################

class SUBSCRIBER_DATA:
	IMG_RAW = Image()
	IMG_RAW_CSV = Image()
	#insert subscriber data here




class SUBSCRIBER:

	#Subscriber Initiation
	def __init__(self):
		print("LISTENERS.__init()__")
		self.bridge = CvBridge()
		#insert subscribers here
		self.subscriberA = rospy.Subscriber("/thorvald_001/kinect2_camera/hd/image_color_rect", Image, self.callbackA)
		
		
#######################################################################################
	def callbackA(self, data):
		SUBSCRIBER_DATA.IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		SUBSCRIBER_DATA.IMG_RAW_HSV = cv2.cvtColor(SUBSCRIBER_DATA.IMG_RAW, cv2.COLOR_BGR2HSV)
		
		SUBSCRIBER_DATA.BASIL = _basil(SUBSCRIBER_DATA.IMG_RAW);

##########################################################################################################
##########################################################################################################
class PUBLISHERS_LOG:
	GOAL_SEND = rospy.Time(1, 0)


class PUBLISHERS:

	#Publisher Creation
	def __init__(self):
		print("PUBLISHERS.__init()__")



	
##########################################################################################################
##########################################################################################################
class CONTROL_DATA:
	debug = False


class CONTROL:
	def __init__(self):
		#Delay to allow motors to rev up
		sleep(2)
		
		
		#http://momori.animenfo.com:8080/listen.pls

		
		while True:
			if cv2.waitKey(0) == 27:
				break

		

##########################################################################################################

#?If errors occur try the following...
#sudo python -m easy_install --upgrade pyOpenSSL
#sudo python -m pip install matplotlib


#Reset Thorvald_001
#os.system("rosservice call /gazebo/reset_simulation '{}'")
#os.system("rosrun image_view image_view image:=/thorvald_001/kinect2_camera/hd/image_color_rect &")
#os.system("rosservice call /thorvald_001/spray")

rospy.init_node('XXXX_CONTROL_SYSTEM_XXXX', anonymous=False)
rate = rospy.Rate(10)



#TODO: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
sub = SUBSCRIBER() #This is the only time SUBSCRIBER is called as all functions within are automatic.
pub = PUBLISHERS() #Used to send messages to publishers.
controlSystem = CONTROL() #This initiates the system.


cv2.destroyAllWindows()
plt.close(1)
sys.exit()








