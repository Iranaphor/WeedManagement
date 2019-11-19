#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sys import argv

#assessment_package
from image_processing.weed_detection import cabbage

class detector:
	def __init__(self):
		print("LISTENERS.__init()__")
		self.bridge = CvBridge()
		self.strel_disk_35 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_35.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
		self.strel_disk_25 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_25.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
		self.subscriber = rospy.Subscriber("/arg1/kinect2_camera/hd/image_color_rect", Image, self.callback)
	
	def callback(self, data):
		IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		OVERLAY,_,_,_ = cabbage(cv2.resize(SUBSCRIBER_DATA.IMG_RAW, (480, 270)), self.strel_disk_25, self.strel_disk_35)
		cv2.imshow('Cabbage', OVERLAY)
		cv2.waitKey(1)

		#apply weeds image to map
		#publish transformations
		


if __name__ == '__main__':
	print("cabbage_detector_initialised")
	rospy.init_node('cabbage_detector', anonymous=False)
	d = detector()
	rospy.spin()







