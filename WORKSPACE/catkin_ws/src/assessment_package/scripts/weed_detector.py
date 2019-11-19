#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sys import argv

#assessment_package
from image_processing.weed_detection import basil, cabbage

class detector:
	def __init__(self, plant_type, robot_name):
		print("detector.__init("+plant_name+"|"+robot_name+")__")
		self.bridge = CvBridge()
		self.plant_type = plant_type
		self.robot_name = robot_name
		if PLANT == "cabbage":
			self.strel_disk_35 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_35.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
			self.strel_disk_25 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_25.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
		self.subscriber = rospy.Subscriber("/"+robot_name+"/kinect2_camera/hd/image_color_rect", Image, self.callback)
		

	def callback(self, data):
		IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")

		#Detect the 
		if self.plant_name == "basil":
			OVERLAY,WEED,_,_ = basil(cv2.resize(SUBSCRIBER_DATA.IMG_RAW, (480, 270)))
		elif self.plant_name == "cabbage":
			OVERLAY,WEED,_,_ = cabbage(cv2.resize(SUBSCRIBER_DATA.IMG_RAW, (480, 270)), self.strel_disk_25, self.strel_disk_35)

		cv2.imshow(self.plant_type, OVERLAY)
		cv2.waitKey(1)
		
		
		#calculate list of weed locations in local space
		#calculate list of weed locations in global space 
		
		#apply weeds image to map
		# 

		#publish transformations
		# how?


if __name__ == '__main__':

	plant_type = sys.argv[1]
	robot_name = sys.argv[2]

	print(plant_type+"_detector_initialised")
	rospy.init_node(plant_type+"_detector", anonymous=False)
	d = detector(plant_type, robot_name)
	rospy.spin()







