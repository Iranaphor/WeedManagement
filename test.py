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
		self.singletonCondition_C = True
		self.axisLabelCounter = 0
		#insert subscribers here
		self.subscriberA = rospy.Subscriber("/thorvald_001/kinect2_camera/hd/image_color_rect", Image, self.callbackA)
		self.subscriberB = rospy.Subscriber("/15591313/image_breakdown", Int8, self.callbackB)
		self.subscriberC = rospy.Subscriber("/15591313/image_analysis", Int8, self.callbackC)
		
		
#######################################################################################
	def callbackA(self, data):
		#print("callbackA(Image Filter)")
		SUBSCRIBER_DATA.IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		SUBSCRIBER_DATA.IMG_RAW_HSV = cv2.cvtColor(SUBSCRIBER_DATA.IMG_RAW, cv2.COLOR_BGR2HSV)
		
		
#######################################################################################
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

#######################################################################################
	def callbackC(self, data):
		print("callbackC(AnalyseData)")
		plt.figure(1559131302)
		plt.show(block=False)
		
		
		GREENMAX = 84;
		HUEMAX = 0.14;
		st3 = np.ones((5,5),np.uint8)
		st6 = np.ones((11,11),np.uint8)
		st11 = np.ones((23,23),np.uint8)
	
	
##	I=imread(d(i).name);
#	I2 = rgb2hsv(I);
#	I3 = I2(:,:,1);
##	I3(I3 > 0.5) = 0;
##	I3(I3 < 0.14) = 0;
#	I3(I3 ~= 0) = 1;
##	imero = imerode(I3,st);
	
		I = SUBSCRIBER_DATA.IMG_RAW ##
		I2 = SUBSCRIBER_DATA.IMG_RAW_HSV
		I3 = I2[:,:,0]
		I3 = cv2.inRange(I3, 50, 255)##
		imero = cv2.erode(I3,st3,iterations = 1)##
		
		plt.subplot(331), plt.imshow(I), plt.title("I")
		plt.subplot(332), plt.imshow(I3), plt.title("I3")
		plt.subplot(333), plt.imshow(imero), plt.title("imero")
		
		
#	G = I(:,:,2);
#	G2 = G;
#	G2(G2<=GREENMAX)=0;
##	G2(G2~=0)=1;
#	bwm = bwmorph(G2, 'skel', 2);
#	med = medfilt2(bwm);
#	sk = bwmorph(med, 'skel', 2);
##	fin = medfilt2(sk, [6,6]);
##	rec2 = imreconstruct(fin, logical(imero));
##	lab = bwlabel(fin);

#########https://uk.mathworks.com/matlabcentral/answers/164349-how-to-calculate-the-curvature-of-a-boundaries-in-binary-images
		
		G = I[:,:,1]
		_,G2 = cv2.threshold(G,GREENMAX,255,cv2.THRESH_BINARY)##
		ero = cv2.erode(G2,st11)
		ero = cv2.erode(ero,st11)
		ero = cv2.erode(ero,st11)
		rec = self.imreconstruct(ero, imero, st3)##
		lab = self.bwlabel(rec)##
		
		plt.subplot(334), plt.imshow(G2), plt.title("G2")
		plt.subplot(335), plt.imshow(ero), plt.title("ero")
		plt.subplot(339), plt.imshow(rec), plt.title("rec")
		
		
		
		
		#Singleton Instance to prevent issues with multilple windows
		plt.draw()
		if (self.singletonCondition_C):
			self.singletonCondition_C = False
			plt.show()
			

	def bwskel(self, img, recursions=-1):
		#https://stackoverflow.com/questions/33095476/is-there-any-build-in-function-can-do-skeletonization-in-opencv
		return img
		#Preprocess image
		_,img = cv2.threshold(img,127,255,0)
		plt.figure(), plt.imshow(img), plt.show()
		
		#Define containers and structuring element
		skel = np.zeros(img.shape,np.uint8)
		element = cv2.getStructuringElement(cv2.MORPH_CROSS,(11,11))
		
		#Recursively skel the image
		i = 0;
		while True:
			i+=1;
			
			eroded = cv2.erode(img,element)
			plt.figure(), plt.imshow(eroded), plt.title("erode"), plt.show()
			
			dilate = cv2.dilate(eroded,element)
			plt.figure(), plt.imshow(dilate), plt.title("dilate"), plt.show()
			
			sub = cv2.subtract(dilate, img)
			plt.figure(), plt.imshow(sub), plt.title("subtract"), plt.show()
			
			skel = cv2.bitwise_or(skel,sub)
			plt.figure(), plt.imshow(skel), plt.title("bitwise"), plt.show()
			
			img = eroded.copy()
			
			print("-"+str(i))
			#If met total recursions or if the is nothing left to skel; return the img
			if (i == recursions or cv2.countNonZero(img) == 0):
				return skel




	def imreconstruct(self, img, mask, st):
		_,mask = cv2.threshold(mask,127,255,0)
		img_new = img
		
		while True:
			img = mask*cv2.erode(img, st, iterations=1)
			if (np.array_equal(img_new,img)):
				return img
			img_new = img
		
		
	def bwlabel(self, img):
		#https://docs.opencv.org/3.1.0/d3/dc0/group__imgproc__shape.html#gac2718a64ade63475425558aa669a943a

		#Label components
		_, labels = cv2.connectedComponents(img)
		
		# Map component labels to hue val
		label_hue = np.uint8(179*labels/np.max(labels))
		blank_ch = 255*np.ones_like(label_hue)
		labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

		# cvt to BGR for display
		labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

		# set bg label to black
		labeled_img[label_hue==0] = 0

		return labeled_img


		
##########################################################################################################
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


#Reset Thorvald_001
#os.system("rosservice call /gazebo/reset_simulation '{}'")
#os.system("rosrun image_view image_view image:=/thorvald_001/kinect2_sensor/sd/image_ir_rect &")
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








