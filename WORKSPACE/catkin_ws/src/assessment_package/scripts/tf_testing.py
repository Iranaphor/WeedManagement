#!/usr/bin/env python
import rospy
import os
import tf
import geometry_msgs.msg
from time import sleep
from sensor_msgs.msg import CameraInfo
from geometry_msgs.msg import PoseStamped

class pixel2pos:

	def __init__(self, cam_frame, cam_info_topic, pixel_x, pixel_y):
		self.tf_listener = tf.TransformListener()
		sleep(1)
		self.pixel_x = pixel_x
		self.pixel_y = pixel_y
		self.caminfo = rospy.Subscriber(cam_info_topic, CameraInfo, self.info)		
		
	def info(self, data):
		try:
			#Get position of camera relative to map
			(trans,rot) = self.tf_listener.lookupTransform('map', cam_frame, rospy.Time())
			print(trans)
			print(rot)
			
			#Get depth as position of pixel relative to camera
			image_depth = trans[2];
			
			#Calculate Position of pixel in 3D Space
			K=data.K;
			fx=K[0]
			fy=K[4]
			cx=K[2]
			cy=K[5]
			PIXEL = [self.pixel_x,self.pixel_y]
			PRINC = [cx,cy]
			FOCAL = [fx,fy]
			print("focal")
			print(FOCAL)
			print("princ")
			print(PRINC)
			X = (PIXEL[0]-PRINC[0])/FOCAL[0]
			Y = (PIXEL[1]-PRINC[1])/FOCAL[1]
			Z = -0.5 #will always be 0
			pixel_relative_camera = [X,Y,Z]
			print("Pix_rel_cam")
			print(pixel_relative_camera)
			
			#Calculate position of pixel in world space
			print("Trans+")
			print([trans[0]+X,trans[1]+Y,0])
			
			#We must factor in rot, with our calculations
			p_robot = PoseStamped()
			p_robot.header.frame_id = cam_frame
			p_robot.pose.position.x = X
			p_robot.pose.position.y = Y
			p_robot.pose.position.z = Z
			print(p_robot)
			p_cam = self.tf_listener.transformPose('map', p_robot)
			print("pcam")
			print(p_cam)
			
			
			
		except (tf.Exception) as e:
			print(e)
		self.caminfo.unregister()
		

if __name__ == '__main__':
	rospy.init_node("f_testing")

	#Initialise Topic
	cam_frame = '/thorvald_001/kinect2_rgb_optical_frame'
	cam_info_topic = '/thorvald_001/kinect2_camera/hd/camera_info'
	p2p = pixel2pos(cam_frame,cam_info_topic,960*2,540)


	rospy.spin()






