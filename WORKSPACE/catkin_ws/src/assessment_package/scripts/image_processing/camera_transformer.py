#!/usr/bin/env python
import rospy
import os
import tf
import tf2_ros
import numpy as np
import geometry_msgs.msg
from time import sleep
from sensor_msgs.msg import CameraInfo
from geometry_msgs.msg import PoseStamped, Quaternion, Point
from tf.transformations import quaternion_from_euler, euler_from_quaternion
#import image_geometry

class pixel2pos:

	def __init__(self, cam_frame, cam_info_topic, global_frame):
		self.cam_frame = cam_frame
		
		self.tfBuffer = tf2_ros.Buffer()
		self.tfListener = tf2_ros.TransformListener(self.tfBuffer)
		
		self.global_frame = global_frame;
		sleep(1)
		
		self.caminfo = rospy.Subscriber(cam_info_topic, CameraInfo, self.info)


	# Get Camera info
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

		except (tf.Exception) as e:
			print(e)

		self.caminfo.unregister()


	# Get coordinate relative to camera
	def pix2base(self,PIXEL):
		#Calculate ray vector
		Z = 0.5 #depth
		X = (PIXEL[0]-self.PRINC[0])/self.FOCAL[0]*Z #vertical
		Y = (PIXEL[1]-self.PRINC[1])/self.FOCAL[1]*Z #horizontal
		
		return [X,Y,Z]

	# Get baselink relative to map at time t
	def base2map(self, t):
		#Calculate position of base_link at time t
		return self.tfBuffer.lookup_transform('map', 'thorvald_001/kinect2_rgb_optical_frame', t, rospy.Duration(1.0))

	#Locate position of each coordinate in coordinate_list
	def geolocate_positions(self, coordinate_list, t, rad):
		t2 = self.base2map(t)
		t22 = [t2.transform.translation.x,t2.transform.translation.y,t2.transform.translation.z]
		print(t2)
		quaternion = (
			t2.transform.rotation.x,
			t2.transform.rotation.y,
			t2.transform.rotation.z,
			t2.transform.rotation.w)
		angle = tf.transformations.euler_from_quaternion(quaternion)
		feta = angle[2] * np.pi / 180.
		RRR = [[np.cos(feta), -np.sin(feta), 0], [np.sin(feta), np.cos(feta), 0], [0, 0, 1]]
		
		P_List=[]
		for c in coordinate_list:
			t1 = self.pix2base(c)
			yawCorrected_t2 = np.matmul(t22,np.array(RRR))
			base2pix =  t1 + yawCorrected_t2
			
			print(feta)
			print(t1)
			print(yawCorrected_t2)
			print(base2pix)
			print
			
			x=np.around(base2pix[0], 2)
			y=np.around(base2pix[1], 2)
			P_List.append( (str(x), str(y), str(rad)) )
		
		print(P_List)
		return P_List
		

if __name__ == '__main__':
	rospy.init_node("tf_testing")

	#Initialise Topic
	cam_frame = '/thorvald_001/kinect2_rgb_optical_frame'
	cam_info_topic = '/thorvald_001/kinect2_camera/hd/camera_info'
	p2p = pixel2pos(cam_frame,cam_info_topic)

	rospy.spin()






