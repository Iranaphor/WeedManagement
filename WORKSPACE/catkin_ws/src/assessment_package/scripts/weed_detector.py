#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sys import argv
import numpy as np
#assessment_package
from image_processing.weed_detection import basil, cabbage

class detector:

	def __init__(self, plant_type, robot_name):
		print("detector.__init("+plant_type+"|"+robot_name+")__")
		self.bridge = CvBridge()
		self.plant_type = plant_type
		self.robot_name = robot_name
		if plant_type == "cabbage":
			self.strel_disk_35 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_35.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
			self.strel_disk_25 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_25.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
		self.pub_weed = rospy.Publisher("/"+self.robot_name+"/weed_detector/"+self.plant_type+"/WEED", Image, queue_size=10)
		self.pub_overlay = rospy.Publisher("/"+self.robot_name+"/weed_detector/"+self.plant_type+"/OVERLAY", Image, queue_size=10)
		self.subscriber = rospy.Subscriber("/"+robot_name+"/kinect2_camera/hd/image_color_rect", Image, self.callback)
		

	def callback(self, data):
		IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")

		#Detect the weeds 
		if self.plant_type == "basil":
			OVERLAY,WEED,_,_ = basil(cv2.resize(IMG_RAW, (480, 270)))
		elif self.plant_type == "cabbage":
			OVERLAY,WEED,_,_ = cabbage(cv2.resize(IMG_RAW, (480, 270)), self.strel_disk_25, self.strel_disk_35)

		#Publish Images
		a = self.bridge.cv2_to_imgmsg(WEED*255, "mono8")
		self.pub_weed.publish(a)

		b = self.bridge.cv2_to_imgmsg(OVERLAY,"bgr8")
		self.pub_overlay.publish(b)

		
		#calculate list of weed locations in local space
		#calculate list of weed locations in global space 
		
		#apply weeds image to map
		# 

		#publish transformations
		# how?


if __name__ == '__main__':

	plant_type = argv[1]
	robot_name = argv[2]

	print(plant_type+"_detector_initialised")
	rospy.init_node(plant_type+"_detector", anonymous=False)
	d = detector(plant_type, robot_name)
	rospy.spin()







