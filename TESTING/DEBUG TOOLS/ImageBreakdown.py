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
		self.sc = SCRIPT_CONTROL()
		
		
#######################################################################################
	def callbackA(self, data):
		print("callbackA(Image Analysis)")
		IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		IMG_RAW_HSV = cv2.cvtColor(IMG_RAW, cv2.COLOR_BGR2HSV)


		self.pltC = plt.figure(15591)
		

		GREENMAX = 84;
		HUEMAX = 0.14;
		st3 = np.ones((5,5),np.uint8)
		st6 = np.ones((11,11),np.uint8)
		st11 = np.ones((23,23),np.uint8)
		
		I = IMG_RAW ##
		I2 = IMG_RAW_HSV
		I3 = I2[:,:,0]
		I3 = cv2.inRange(I3, 50, 255)##
		imero = cv2.erode(I3,st3,iterations = 1)##
		
		plt.subplot(331), plt.imshow(I), plt.title("I")
		plt.subplot(332), plt.imshow(I3), plt.title("I3")
		plt.subplot(333), plt.imshow(imero), plt.title("imero")
		
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
		
		
		
		plt.show();
		SCRIPT_CONTROLER.ender_loop = False



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
		mx = np.max(labels)
		if mx==0:
			mx=1
		label_hue = np.uint8(179*labels/mx)
		blank_ch = 255*np.ones_like(label_hue)
		labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

		# cvt to BGR for display
		labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

		# set bg label to black
		labeled_img[label_hue==0] = 0

		return labeled_img




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

ender_loop = True

sub = ImageAnalysis() #This is the only time SUBSCRIBER is called as all functions within are automatic.

cv2.destroyAllWindows()
plt.close(1)
sys.exit()








