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

class ImageAnalysis:

	#Subscriber Initiation
	def __init__(self):
		print("LISTENERS.__init()__")
		self.bridge = CvBridge()
		self.subscriberA = rospy.Subscriber("/thorvald_001/kinect2_camera/hd/image_color_rect", Image, self.callbackA)
		sc = SCRIPT_CONTROL()

		
		
#######################################################################################
	def callbackA(self, data):
		print("callbackA(Image Analysis)")
		IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		IMG_RAW_HSV = cv2.cvtColor(IMG_RAW, cv2.COLOR_BGR2HSV)
		
		self.pltB = plt.figure(15590)
		
		plt.subplot(411)
		plt.imshow(IMG_RAW)
		
		for i in range(0,3):
			#Display RGB graphs
			self.plotHist(IMG_RAW[:,:,i], 423+(2*i))

			#Display HSV graphs
			self.plotHist(IMG_RAW_HSV[:,:,i], 424+(2*i))


		plt.show();
		SCRIPT_CONTROLER.ender_loop = False
		


	def plotHist(self, data, subplot=111):
		#https://stackoverflow.com/questions/5328556/histogram-matplotlib
		plt.subplot(subplot)
		x = data
		bins, edges = np.histogram(x, 50, normed=1)
		left,right = edges[:-1],edges[1:]
		X = np.array([left,right]).T.flatten()
		Y = np.array([bins,bins]).T.flatten()
		plt.plot(X,Y, label=str("..."))



##########################################################################################################

class SCRIPT_CONTROLER:
	ender_loop = True

class SCRIPT_CONTROL:
	def __init__(self):	
		while SCRIPT_CONTROLER.ender_loop:
			if cv2.waitKey(0) == 27:
				break

##########################################################################################################

rospy.init_node('XXXX_IMAGE_ANALYSIS_XXXX', anonymous=False)
rate = rospy.Rate(10)



sub = ImageAnalysis()
cv2.destroyAllWindows()
plt.close(1)
sys.exit()








