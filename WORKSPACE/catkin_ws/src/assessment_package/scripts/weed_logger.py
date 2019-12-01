#!/usr/bin/env python
import rospy
import os
import tf
import geometry_msgs.msg
from time import sleep
from sensor_msgs.msg import CameraInfo
from geometry_msgs.msg import PoseStamped, Quaternion, Point
from tf.transformations import quaternion_from_euler, euler_from_quaternion
#import image_geometry

class pixel2pos:

	def __init__(self, cam_frame, cam_info_topic):
		self.cam_frame = cam_frame
		self.tf_listener = tf.TransformListener()
		sleep(1)
		self.caminfo = rospy.Subscriber(cam_info_topic, CameraInfo, self.info)

	def info(self, data):
		try:
			#Calculate Position of pixel in 3D Space
			K=data.K;
			fx=K[0]
			fy=K[4]
			cx=K[2]
			cy=K[5]
			self.PRINC = [cx,cy]
			self.FOCAL = [fx,fy]
			print("princ " + str(self.PRINC))
			print("focal " + str(self.FOCAL))

		except (tf.Exception) as e:
			print(e)

		self.caminfo.unregister()

	def get_position(self,PIXEL):
		#print("pixel " + str(PIXEL))

		#Calculate ray vector
		X = (PIXEL[0]-self.PRINC[0])/self.FOCAL[0] #vertical
		Y = (PIXEL[1]-self.PRINC[1])/self.FOCAL[1] #horizontal
		Z = 0.5 #depth
		
		#Transform to world frame
		p_robot = PoseStamped()
		p_robot.header.frame_id = self.cam_frame
		p_robot.pose.position = Point(X*Z,Y*Z,Z)

		p_cam = self.tf_listener.transformPose('map', p_robot)
		pos = p_cam.pose.position;

		return [pos.x, pos.y]
			
			
			
		

if __name__ == '__main__':
	rospy.init_node("f_testing")

	#Initialise Topic
	cam_frame = '/thorvald_001/kinect2_rgb_optical_frame'
	cam_info_topic = '/thorvald_001/kinect2_camera/hd/camera_info'
	p2p = pixel2pos(cam_frame,cam_info_topic)

	rospy.spin()






