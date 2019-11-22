#!/usr/bin/env python
import rospy
import os
import tf
import geometry_msgs.msg
from time import sleep

if __name__ == '__main__':
	rospy.init_node("f_testing")

	tf_listener = tf.TransformListener()
	sleep(1)
	try:
		(trans,rot) = tf_listener.lookupTransform('thorvald_001/odom', 'thorvald_001/kinect2_rgb_optical_frame', rospy.Time())
		print(trans)
		print(rot)
	except (tf.Exception) as e:
		print(e)

	#rospy.spin()
