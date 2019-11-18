##########################################################################################################
# 
# Required: 
# 	Speedup of basil and cabbage functions
# 	Implementation of spring onion function
# 	Refactor Mask sizes to make dynamic based on image size (10/25/35 good for 1080*1920)
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

#Own Functions
from image_processing.weed_detection import basil, cabbage

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
	
	LASER_PLOT = False



class SUBSCRIBER:

	#Subscriber Initiation
	def __init__(self):
		print("LISTENERS.__init()__")
		self.bridge = CvBridge()
		self.strel_disk_35 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_35.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
		self.strel_disk_25 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_25.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)

		#insert subscribers here
		#self.subscriberIP_a = rospy.Subscriber("/thorvald_001/kinect2_camera/hd/image_color_rect", Image, self.callbackIP_a) #Basil
		#self.subscriberIP_b = rospy.Subscriber("/thorvald_001/kinect2_camera/hd/image_color_rect", Image, self.callbackIP_b) #Cabbage
		#self.subscriberIP_c = rospy.Subscriber("/thorvald_001/kinect2_camera/hd/image_color_rect", Image, self.callbackIP_c) #Onion
		self.subscriberSCAN = rospy.Subscriber("/thorvald_001/scan", LaserScan, self.callbackSCAN)
		
	
	def callbackIP_a(self, data):
		IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		BASIL,_,_,_ = basil(cv2.resize(SUBSCRIBER_DATA.IMG_RAW, (960, 540)));
		cv2.imshow('Basil', BASIL)
		cv2.waitKey(1)

		markclusters()

	def callbackIP_b(self, data):
		IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		CABBAGE,_,_,_ = cabbage(cv2.resize(SUBSCRIBER_DATA.IMG_RAW, (480, 270)), self.strel_disk_25, self.strel_disk_35);
		cv2.imshow('Cabbage', CABBAGE)
		cv2.waitKey(1)


	def callbackSCAN(self, data):
		print("listenerE()")
		a=np.array(data.ranges)
		
		if SUBSCRIBER_DATA.LASER_PLOT:
			print("Update LaserScan Graph")

			if self.y == 10:
				self.y=0;
				self.laser_scan.set_ydata(a)
				self.fig.canvas.draw()
				self.fig.canvas.flush_events()

		else:
			print("Setup LaserScan Plot")
			SUBSCRIBER_DATA.LASER_PLOT = True
			plt.ion()
			self.fig = plt.figure()
			self.ax = self.fig.add_subplot(111)
			self.laser_scan, = self.ax.plot(np.linspace(0, a.shape[0], a.shape[0]), a)
			plt.ylim(0, 30)
			self.y = 0;

		self.y= self.y+1;




##########################################################################################################
class PUBLISHERS_LOG:
	GOAL_SEND = rospy.Time(1, 0)


class PUBLISHERS:

	#Publisher Creation
	def __init__(self):
		print("PUBLISHERS.__init()__")



	
##########################################################################################################
class CONTROL_DATA:
	debug = False


class CONTROL:
	def __init__(self):
		#Delay to allow motors to rev up
		sleep(2)
		
		
		#http://momori.animenfo.com:8080/listen.pls

		
		while True:
			sleep(1)

		

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








