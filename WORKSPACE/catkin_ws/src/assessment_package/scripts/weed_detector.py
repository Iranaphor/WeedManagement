#!/usr/bin/env python

#ros libraries
import rospy
from std_msgs.msg import String
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
from image_processing.weed_detection import basil, cabbage, onion


class detector:

	def __init__(self, robot_name, path):
		print("detector.__init("+robot_name+")__")
		self.bridge = CvBridge()
		self.path = path
		self.robot_name = robot_name
		self.plant_type = "null"
		self.P_List=[]

		#
		self.map = rospy.Subscriber("/map", OccupancyGrid, self.mapper)

		#Define Image publishers
		self.pub_weed = rospy.Publisher("/"+self.robot_name+"/weed_detector/WEED", Image, queue_size=10)
		self.pub_overlay = rospy.Publisher("/"+self.robot_name+"/weed_detector/OVERLAY", Image, queue_size=10)
		
		#Weed Logger
		cam_frame = "/thorvald_001/kinect2_rgb_optical_frame"
		cam_info_topic = "/thorvald_001/kinect2_camera/hd/camera_info"
		self.pixel2pos = pixel2pos(cam_frame,cam_info_topic)

		#Define Image Subscriber
		self.subscriber = rospy.Subscriber("/"+robot_name+"/kinect2_camera/hd/image_color_rect", Image, self.callback)
		self.row_type_subscriber = rospy.Subscriber("/"+robot_name+"/row_type", String, self.row_type_callback)
		
		

	def mapper(self, data):
		self.map.unregister()
		scale = 10
		self.weed_map = np.array(np.zeros(((data.info.height*0.75)*scale, (data.info.width*0.75)*scale)),dtype='uint8')
		self.weed_map_resolution = data.info.resolution/scale #m/cell 0.5m/10 = 0.05 (5cm/cell) #DISTANCE PER CELL
		self.plot_to_map(( 6.5,-3.75), 0.1)
		self.plot_to_map(( 6.5,-2.75), 0.1)
		self.plot_to_map(( 6.5,-0.75), 0.1)
		self.plot_to_map(( 6.5, 0.25), 0.1)
		self.plot_to_map(( 6.5, 2.25), 0.1)
		self.plot_to_map(( 6.5, 3.25), 0.1)
		self.plot_to_map((-6.5,-3.75), 0.1)
		self.plot_to_map((-6.5,-2.75), 0.1)
		self.plot_to_map((-6.5,-0.75), 0.1)
		self.plot_to_map((-6.5, 0.25), 0.1)
		self.plot_to_map((-6.5, 2.25), 0.1)
		self.plot_to_map((-6.5, 3.25), 0.1)
		

		#cv2.imshow('MAP', self.weed_map)
		#cv2.waitKey(10)

	def plot_to_map(self, map_coord_tuple, radius):
		#Convert /map frame coordinates to pixel locations
		map_coord_tuple = np.divide(map_coord_tuple, self.weed_map_resolution) #(1.2,2.0)/0.05 = (24,40)
		center = 0.5*np.array(self.weed_map.shape)
		b=(center+map_coord_tuple)
		center_coordinates = np.array(b,dtype='uint32')
		
		#Convert /map frame radius to pixel locations
		map_radius = 0#int(radius/self.weed_map_resolution)

		#Add circle to map
		self.weed_map = cv2.circle(self.weed_map, (center_coordinates[0],center_coordinates[1]), map_radius, 255, -1)
		

	#Save the current row
	def row_type_callback(self, data):
		if self.plant_type != data.data:
			if self.plant_type != "null":

				#Colate list of coordinates
				xx = list(set(self.P_List))
				#print(xx)
				print(self.plant_type + "::" + str(len(xx)) + "|" + str(len(self.P_List)))
				
				#P=Point()
				for p in xx:
					self.plot_to_map((float(p[0]), float(p[1])), 0.1)
					
					#P.x=float(p[0])
					#P.y=float(p[1])
					#self.plot_point.publish(P)
				
				self.P_List = []

			self.plant_type = data.data
			
			cv2.imwrite('mapp.png', self.weed_map)
			
			#cv2.imshow('MAP', self.weed_map)
			#cv2.waitKey(10)
			

	def callback(self, data):
		IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		t = rospy.Time.now()	

		#DEBUG TOOL
		#self.plant_type = "onion"

		#Detect the weeds 
		if self.plant_type == "basil":
			OVERLAY,WEED,_,_ = basil(cv2.resize(IMG_RAW, (160,90)))
		elif self.plant_type == "cabbage":
			OVERLAY,WEED,_,_ = cabbage(cv2.resize(IMG_RAW, (480, 270)))
		elif self.plant_type == "onion":
			OVERLAY,WEED,_,_ = onion(cv2.resize(IMG_RAW, (240, 135)),0)

		#Publish Images
		if self.plant_type != "null":
		
			#Find Centre/Worldpoints of weed clusters
			centres = self.find_points(cv2.resize(WEED, (1920, 1080)))
			point=[]
			#print(len(centres))
			for c in centres:
				p=self.pixel2pos.get_position(c,t)
				point.append(p)
				P=Point()
				P.x=np.around(p[0], 2)
				P.y=np.around(p[1], 2)
				self.P_List.append((str(P.x),str(P.y)))

			self.pub_weed.publish(self.bridge.cv2_to_imgmsg(WEED*255, "mono8"))
			self.pub_overlay.publish(self.bridge.cv2_to_imgmsg(OVERLAY,"bgr8"))

	#Adapted from https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
	def find_points(self, WEED):
		centroids = []

		# Find contours in the binary image
		_,contours,_ = cv2.findContours(WEED, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

		# Calculate centrepoint of each blob
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
	robot_name = argv[1]

	print("weed_detector_initialised")
	rospy.init_node("weed_detector", anonymous=False)
	d = detector(robot_name, path)
	rospy.spin()













