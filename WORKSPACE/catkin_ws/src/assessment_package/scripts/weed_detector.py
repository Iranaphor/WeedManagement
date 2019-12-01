#!/usr/bin/env python

#ros libraries
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from nav_msgs.msg import OccupancyGrid

#common python libraries
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from time import sleep

#os libraries
import os
from sys import argv

#assessment_package
from assessment_package.msg import weed_location
from weed_logger import pixel2pos
from image_processing.weed_detection import basil, cabbage


class detector:

	def __init__(self, plant_type, robot_name, path):
		print("detector.__init("+plant_type+"|"+robot_name+")__")
		self.bridge = CvBridge()
		self.path = path
		self.plant_type = plant_type
		self.robot_name = robot_name
		if plant_type == "cabbage":
			self.strel_disk_35 = cv2.cvtColor(cv2.imread(path+"/image_processing/strel_disk_35.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
			self.strel_disk_25 = cv2.cvtColor(cv2.imread(path+"/image_processing/strel_disk_25.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)

		#Define Image publishers
		#self.pub_weed = rospy.Publisher("/"+self.robot_name+"/weed_detector/"+self.plant_type+"/WEED", Image, queue_size=10)
		self.pub_overlay = rospy.Publisher("/"+self.robot_name+"/weed_detector/"+self.plant_type+"/OVERLAY", Image, queue_size=10)
		
		#Weed Logger
		cam_frame = "/thorvald_001/kinect2_rgb_optical_frame"
		cam_info_topic = "/thorvald_001/kinect2_camera/hd/camera_info"
		self.pixel2pos = pixel2pos(cam_frame,cam_info_topic)
		self.pub_weed_loc = rospy.Publisher("/YAY", weed_location, queue_size=10)
		self.plot_point = rospy.Publisher("weed_killer/spray_topic", Point, queue_size=10)

		#Define Image Subscriber
#		self.map_taker = rospy.Subscriber("/map", OccupancyGrid, self.map_take)
		self.subscriber = rospy.Subscriber("/"+robot_name+"/kinect2_camera/hd/image_color_rect", Image, self.callback)

#	def map_take(self, data):
#		print(self.path)
#		self.MAP = cv2.resize(cv2.flip(cv2.rotate(np.reshape(data.data, newshape=(data.info.height, data.info.width)), cv2.ROTATE_90_COUNTERCLOCKWISE), 1),(12000,12000))
#		print("yy")
#		cv2.imwrite(self.path+"/thinggy.png",self.MAP)
#		print("yyy")
#		self.map_taker.unregister()


	def callback(self, data):
		IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		
		
		#Detect the weeds 
		if self.plant_type == "basil":
			OVERLAY,WEED,_,_ = basil(cv2.resize(IMG_RAW, (160,90)))
			#WEED = basil(cv2.resize(IMG_RAW, (160, 90)), "weed_only") #TODO smaller images plants disappear under erode
		elif self.plant_type == "cabbage":
			OVERLAY,WEED,_,_ = cabbage(cv2.resize(IMG_RAW, (960, 540)), self.strel_disk_25, self.strel_disk_35)
		
		#Publish Images
		a = self.bridge.cv2_to_imgmsg(WEED*255, "mono8")
		self.pub_weed.publish(a)
		b = self.bridge.cv2_to_imgmsg(OVERLAY,"bgr8")
		self.pub_overlay.publish(b)
		
		#Find Centre/Worldpoints of weed clusters
		centres = self.find_points(cv2.resize(WEED, (1920, 1080)))
		point=[]
		for c in centres:
			p=self.pixel2pos.get_position(c)
			point.append(p)
			
			P=Point()
			P.x=p[0]
			P.y=p[1]
			#self.plot_point.publish(P)
		
		self.subscriber.unregister()
		sleep(2)
		self.subscriber = rospy.Subscriber("/"+robot_name+"/kinect2_camera/hd/image_color_rect", Image, self.callback)

	#Adapted from https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
	def find_points(self, WEED): 
		
		centroids = []

		# find contours in the binary image
		im2, contours, hierarchy = cv2.findContours(WEED,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		for c in contours:
			# calculate moments for each contour
			M = cv2.moments(c)

			# calculate x,y coordinate of center
			if M["m00"] != 0:
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
			else:
				cX, cY = 0, 0	
			
			centroids.append((cX,cY))

		return centroids
		

if __name__ == '__main__':
	path = os.path.dirname(argv[0])
	plant_type = argv[1]
	robot_name = argv[2]

	print(plant_type+"_detector_initialised")
	rospy.init_node(plant_type+"_detector", anonymous=False)
	d = detector(plant_type, robot_name, path)
	rospy.spin()












