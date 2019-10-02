##########################################################################################################
# change move base status listener to work off of data.status
# add another mapper for /move_base version of /odom
#
# h = LISTENERS_DATA.FULL_SCAN[p]
# IndexError: index 648 is out of bounds for axis 0 with size 640
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

class SUBSCRIBER_DATA:
	IMG_RAW = Image()
	IMG_RAW_CSV = Image()
	#insert subscriber data here




class SUBSCRIBER:

	#Subscriber Initiation
	def __init__(self):
		print("LISTENERS.__init()__")
		self.bridge = CvBridge()
		#plt.show()
		self.singletonCondition_B = True
		self.axisLabelCounter = 0
		#insert subscribers here
		self.subscriberA = rospy.Subscriber("/thorvald_001/kinect2_camera/hd/image_color_rect", Image, self.callbackA)
		self.subscriberB = rospy.Subscriber("/15591313/image_breakdown", Int8, self.callbackB)


		
	def callbackA(self, data):
		#print("callbackA(Image Filter)")
		SUBSCRIBER_DATA.IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		SUBSCRIBER_DATA.IMG_RAW_HSV = cv2.cvtColor(SUBSCRIBER_DATA.IMG_RAW, cv2.COLOR_BGR2HSV)
		

	
	def callbackB(self, data):
		print("callbackB(PlotData)")
		plt.figure(1559131301)
		plt.show(block=False)


		plt.subplot(411)
		plt.imshow(SUBSCRIBER_DATA.IMG_RAW)
		
		#https://stackoverflow.com/questions/5328556/histogram-matplotlib
		for i in range(0,3):
			#Display RGB graphs
			self.plotHist(SUBSCRIBER_DATA.IMG_RAW[:,:,i], 423+(2*i))

			#Display HSV graphs
			self.plotHist(SUBSCRIBER_DATA.IMG_RAW_HSV[:,:,i], 424+(2*i))

		plt.draw()
		print("78")
		if (self.singletonCondition_B):
			self.singletonCondition_B = False
			plt.show()



	def plotHist(self, data, subplot=111):
		plt.subplot(subplot)
		x = data
		bins, edges = np.histogram(x, 50, normed=1)
		left,right = edges[:-1],edges[1:]
		X = np.array([left,right]).T.flatten()
		Y = np.array([bins,bins]).T.flatten()
		plt.plot(X,Y, label=str(self.axisLabelCounter))
		self.axisLabelCounter=self.axisLabelCounter+1;
		
		#TODO: Fix the error appearing after overlaying the plots



		
##########################################################################################################
class PUBLISHERS_LOG:
	GOAL_SEND = rospy.Time(1, 0)


class PUBLISHERS:

	#Publisher Creation
	def __init__(self):
		print("PUBLISHERS.__init()__")
		
		#insert publishers here
			#self.publisher_GOAL = rospy.Publisher("/move_base/goal", MoveBaseActionGoal, queue_size = 2)

		
		
		
	#def publish_GOAL2(self, new_x, new_y, angle, move_type="move"):
		#self.publisher_GOAL.publish(goal)
		
	#insert publish functions here
	
	
	
	
	
	
	
##########################################################################################################
class CONTROL_DATA:

	debug = False


class CONTROL:
	
	def __init__(self):
		#Delay to allow motors to rev up
		sleep(2)
		
		
		#http://momori.animenfo.com:8080/listen.pls


		#Run Main Script
		self.main()
		
		
#---------------------------------------------------------------------------------------------------------
	def main(self):
		
		while True:
			#cv2.imshow('CAM_VIEW', SUBSCRIBER_DATA.IMG_RAW)
			#cv2.waitKey(1)
	        	if cv2.waitKey(0) == 27:
				break

		

##########################################################################################################

#?If errors occur try the following...
#sudo python -m easy_install --upgrade pyOpenSSL
#sudo python -m pip install matplotlib
#sudo python -m pip install numpy


#Reset Thorvald_001
#os.system("rosservice call /gazebo/reset_simulation '{}'")
#os.system("rosrun image_view image_view image:=/thorvald_001/kinect2_sensor/sd/image_ir_rect &")
#os.system("rosservice call /thorvald_001/spray")

rospy.init_node('XXXX_CONTROL_SYSTEM_XXXX', anonymous=False)
rate = rospy.Rate(10)



#TODO: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
sub = SUBSCRIBER() #This is the only time LISTENERS is called as all functions within are automatic.
pub = PUBLISHERS() #This is used to send messages to publishers.
controlSystem = CONTROL() #This initiates the system.


cv2.destroyAllWindows()
plt.close(1)
sys.exit()








