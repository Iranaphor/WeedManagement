#!/usr/bin/env python

#ros libraries
import rospy
from std_msgs.msg import String, Float64MultiArray
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from nav_msgs.msg import OccupancyGrid

#common python libraries
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from time import sleep
import yaml

#os libraries
import os
from sys import argv

#assessment_package
from assessment_package.msg import WeedList
from image_processing.camera_transformer import pixel2pos
from image_processing.weed_detection import basil, cabbage, onion
from image_processing.generic import imfindcentroids

class detector:

	def __init__(self, CONFIG, path=""):
		self.path = path
		print("_DETECTOR_init_")
		self.bridge = CvBridge()
		ROB = CONFIG['scanner_robot']
		self.plant_type = "null"
		self.P_List=[]
		self.CONFIG = CONFIG

		#Download map details
		self.map = rospy.Subscriber(CONFIG['map_topic'], OccupancyGrid, self.mapper)

		#Define Image publishers
		self.pub_weed = rospy.Publisher(ROB+CONFIG['weed_output'], Image, queue_size=10)
		self.pub_overlay = rospy.Publisher(ROB+CONFIG['overlay_output'], Image, queue_size=10)
		
		#Weed Logger
		cam_frame = ROB+CONFIG['camera_frame']
		cam_info_topic = ROB+CONFIG['camera_info']
		self.pixel2pos = pixel2pos(cam_frame, cam_info_topic, CONFIG['map_frame'])

		#Define Image Subscriber
		self.subscriber = rospy.Subscriber(ROB+CONFIG['camera_topic'], Image, self.callback)
		self.row_meta_subscriber = rospy.Subscriber(ROB+CONFIG['row_meta'], String, self.row_type_callback)
		self.row_data_publisher = rospy.Publisher(CONFIG['sprayer_robot']+CONFIG['row_data'], WeedList, queue_size=10)
		

#-------------------------------------------------------------------------------------------------------- Mapping	
	
	#Create a weed_map object based on the size of the /map
	def mapper(self, data):
		self.map.unregister()
		scale = 10
		#self.weed_map = np.array(255*np.ones((np.int((data.info.height*0.6)*scale), np.int((data.info.width*0.45)*scale))),dtype='uint8')
		self.weed_map = np.array(255*np.ones((np.int((data.info.height)*scale), np.int((data.info.width)*scale))),dtype='uint8')
		self.weed_map *= 0
		self.weed_map_resolution = data.info.resolution/scale #m/cell 0.5m/10 = 0.05 (5cm/cell) #DISTANCE PER CELL
		
		#print(self.map_to_coord(0.5*np.array(self.weed_map.shape,dtype='f')))

		#Plot row endpoints
		#rows = [-3.75, -2.75, -0.75, 0.25, 2.15, 3.25]
		#for r in rows:
		#	self.plot_to_map(( 5,r), 0.1)
		#	self.plot_to_map((-5,r), 0.1)
		
		#Write clean map
		self.print_map()

	#Print the map to a file defined by system_config.yaml
	def print_map(self):
		if self.CONFIG['map_path'] == "default":
			cv2.imwrite(self.path+"/mapp.png", cv2.rotate(self.weed_map, cv2.ROTATE_90_COUNTERCLOCKWISE))
		elif self.CONFIG['map_path'] == "none":
			pass
		else:
			cv2.imwrite(self.CONFIG['map_path']+"/mapp.png", cv2.rotate(self.weed_map, cv2.ROTATE_90_COUNTERCLOCKWISE))


	#Plot coordinates in respective position on map
	def plot_to_map(self, map_coord_tuple, radius, gray = 255):
		#Convert /map frame coordinates to pixel locations
		map_coord_tuple = np.divide(map_coord_tuple, self.weed_map_resolution) #(1.2,2.0)/0.05 = (24,40)
		center = 0.5*np.array(self.weed_map.shape)
		b=(center+map_coord_tuple)
		center_coordinates = np.array(b,dtype='uint32')
		
		#Convert /map frame radius to pixel locations
		map_radius = int(radius/self.weed_map_resolution)

		#Add circle to map
		self.weed_map = cv2.circle(self.weed_map, (center_coordinates[1],center_coordinates[0]), map_radius, gray, -1)
		

	#Plot coordinates in respective position on map
	def map_to_coord(self, pixt):
		pix = np.array([pixt[1],pixt[0]],dtype='float32')

		center = 0.5*np.array(self.weed_map.shape)
		rel_pix = (pix-center)
		pos = np.multiply(rel_pix, self.weed_map_resolution)

		#print(str(pix) + str(center) + str(rel_pix) + str(pos))
		return (str(np.around(pos[0],2)), str(np.around(pos[1],2)))


#-------------------------------------------------------------------------------------------------------- Weed Management
		
	#Called at End of Row 
	def row_type_callback(self, data):
		if self.plant_type != data.data:
			if data == "home":
				print("hooome")
				array=WeedList()
				array.plant_type = self.plant_type
				self.row_data_publisher.publish(array)

			elif self.plant_type != "null":
				
				#Filter out Overlaying Points
				self.cluster_data()

				#Write Map of Current Row
				self.print_map()
			
				#Reset for Next Row
				self.weed_map *= 0
				self.P_List = []

			self.plant_type = data.data


	#Cluster all the points discovered on the row
	def cluster_data(self):
		#Filter duplicates in list of coordinates
		xx = list(set(self.P_List))
		
		#For each remaining point, plot it on the map
		for p in xx:
			self.plot_to_map((float(p[0]), float(p[1])), float(p[2]), 128)
		
		#Filter the blobs in the map to find the weeds coords
		weed_list = imfindcentroids(self.weed_map)#*self.weed_map_resolution

		#Convert pixel positions to world coordinates
		point_list = []
		for c in weed_list:
			point_list.append(self.map_to_coord(c))
			self.plot_to_map((float(point_list[-1][0]), float(point_list[-1][1])), float(xx[0][2])/2, 255)

		#Display Results
		print(self.plant_type + ":: Detect~"+str(len(self.P_List))+"|Filter~"+str(len(xx))+"|Cluster~"+str(len(weed_list)))
		
		#Publish to Sprayer_Robot
		array=WeedList()
		array.plant_type = self.plant_type
		for p in point_list:
			array.weeds.data.append(float(p[0]))
			array.weeds.data.append(float(p[1]))
		self.row_data_publisher.publish(array)

#-------------------------------------------------------------------------------------------------------- Image Processing
	#Image Callback
	def callback(self, data):
		IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		t = rospy.Time.now()
		p=self.plant_type

		#Detect the weeds
		if p == "basil":
			OVERLAY,WEED,_,_ = basil(cv2.resize(IMG_RAW, (160,90)))
		elif p == "cabbage":
			OVERLAY,WEED,_,_ = cabbage(cv2.resize(IMG_RAW, (480, 270)))
		elif p == "onion":
			OVERLAY,WEED,_,_ = onion(cv2.resize(IMG_RAW, (240, 135)),0)
		
		#Publish Images
		if p != "null" and p != "home" and p != "shutdown":
			
			#Find Centre/Worldpoints of weed clusters
			centres = imfindcentroids(cv2.resize(WEED, (1920, 1080)))
			point=[]

			#Identify size of spray region
			rad = self.CONFIG['plant_management'][p]['nozel_radius']

			for c in centres:
				p=self.pixel2pos.get_position(c,t)
				point.append(p)
				P=Point()
				P.x=np.around(p[0], 2)
				P.y=np.around(p[1], 2)
				self.P_List.append( (str(P.x), str(P.y), str(rad)) )

			#self.pub_weed.publish(self.bridge.cv2_to_imgmsg(WEED*255, "mono8"))
			self.pub_overlay.publish(self.bridge.cv2_to_imgmsg(OVERLAY,"bgr8"))
		else:
			self.pub_overlay.publish(self.bridge.cv2_to_imgmsg(IMG_RAW,"bgr8"))



if __name__ == '__main__':
	path = os.path.dirname(argv[0])
	yaml_path = argv[1]
	CONFIG = yaml.safe_load(open(yaml_path))

	rospy.init_node("DETECTOR", anonymous=False)
	d = detector(CONFIG, path)
	rospy.spin()













