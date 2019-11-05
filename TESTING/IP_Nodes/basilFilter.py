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
		
		
		im = IMG_RAW;
		im_hsv = IMG_RAW_HSV;
		im_h = im_hsv(:,:,0);
		im_s = im_hsv(:,:,1);

		# Plant Mask
		im_plant_2 = im_h;
		im_plant_2(round(im_plant_2*100)~=24) = 0;
		im_plant_3 = imopen(im_plant_2,ones(10));
		im_plant_4 = imreconstruct(im_plant_3,im_plant_2);
		plantMask = logical(imfill(im_plant_4));
		
		# Dirt Mask
		dirtMask = ~imbinarize(im_h,.2);
		
		# Weed Mask
		weedMask = (im_h>im_s);
		
		# Weed Overlay
		Overlay = im;
		Overlay(:,:,1) = Overlay(:,:,1)+uint8(weedMask*100);
		Overlay(:,:,2) = Overlay(:,:,2)+uint8(plantMask*100);
		Overlay(:,:,3) = Overlay(:,:,3)+uint8(dirtMask*100);




##########################################################################################################

rospy.init_node('XXXX_IMAGE_ANALYSIS_XXXX', anonymous=False)
rate = rospy.Rate(10)



sub = ImageAnalysis()
cv2.destroyAllWindows()
plt.close(1)
sys.exit()








