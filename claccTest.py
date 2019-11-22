##########################################################################################################
# change move base status listener to work off of data.status
# add another mapper for /move_base version of /odom
#
# h = LISTENERS_DATA.FULL_SCAN[p]
# IndexError: index 648 is out of bounds for axis 0 with size 640
#
##########################################################################################################

#ROSPY IMPORTS
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image, LaserScan, JointState
from nav_msgs.msg import Odometry, OccupancyGrid
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionFeedback
from geometry_msgs.msg import Twist, Quaternion, Pose, Point
from actionlib_msgs.msg import GoalStatusArray
from tf.transformations import quaternion_from_euler, euler_from_quaternion

#OPENCV IMPORTS
import cv2
from cv_bridge import CvBridge, CvBridgeError

#LIBRARIES IMPORTS
import numpy as np
import matplotlib.pyplot as plt

#PYTHON IMPORTS
import os
import subprocess
import sys
from sys import argv
import datetime
import time
from time import sleep





##########################################################################################################

class LISTENERS_DATA:
	IMG_RAW = Image()
	IMG_BLUE = Image()
	IMG_GREEN = Image()
	IMG_RED = Image()
	IMG_YELLOW = Image()
	ALL_IMG = Image()
	IMG_WIDTH = 0
	IMG_HEIGHT = 0
	
	MAP = []

	ODOM_PATH = []
	
	SCAN = -1
	FULL_SCAN = np.array([])
	LASER_PLOT = False

	GOAL_STATUS = ""
	GOAL_TIME = rospy.Time(0, 0)
	NEW_GOAL_ID = 0
	MOVE_PATH = []

	#insert subscriber data here




class LISTENERS:

	#Listener Initiation
	def __init__(self):
		print("LISTENERS.__init()__")
		self.bridge = CvBridge()
		#insert subscribers here
		self.firstErr = True
		
		#TEST IS ASSIGNMENT NECCESSARY
		self.subscriberA = rospy.Subscriber("/camera/rgb/image_raw", Image, self.listenerA)
		self.publisher_depth = rospy.Publisher("/15591313/depth", Image, queue_size = 2)
				
		self.subscriberB = rospy.Subscriber("/map", OccupancyGrid, self.listenerB)
		
		self.subscriberD = rospy.Subscriber("/odom", Odometry, self.listenerD)
		
		self.subscriberE = rospy.Subscriber("/scan", LaserScan, self.listenerE)
		
		self.subscriberF1 = rospy.Subscriber("/move_base/status", GoalStatusArray, self.listenerF1)
		self.subscriberF2 = rospy.Subscriber("/move_base/goal", MoveBaseActionGoal, self.listenerF2)
		self.subscriberF2 = rospy.Subscriber("/move_base/feedback", MoveBaseActionFeedback, self.listenerF3)



		
		
		
	def listenerA(self, data):
		print("listenerA()")
		LISTENERS_DATA.IMG_RAW = self.bridge.imgmsg_to_cv2(data, "bgr8")
		LISTENERS_DATA.IMG_BLUE = cv2.medianBlur(cv2.inRange(LISTENERS_DATA.IMG_RAW, np.array((95, 0, 0)), np.array((255, 15, 15))),5)
		LISTENERS_DATA.IMG_GREEN = cv2.medianBlur(cv2.inRange(LISTENERS_DATA.IMG_RAW, np.array((0, 95, 0)), np.array((15, 255, 15))),5)
		LISTENERS_DATA.IMG_RED = cv2.medianBlur(cv2.inRange(LISTENERS_DATA.IMG_RAW, np.array((0, 0, 95)), np.array((15, 15, 255))),5)
		LISTENERS_DATA.IMG_YELLOW = cv2.medianBlur(cv2.inRange(LISTENERS_DATA.IMG_RAW, np.array((0, 95, 95)), np.array((15, 255, 255))),5)
		LISTENERS_DATA.ALL_IMG = LISTENERS_DATA.IMG_BLUE + LISTENERS_DATA.IMG_GREEN + LISTENERS_DATA.IMG_RED + LISTENERS_DATA.IMG_YELLOW
		LISTENERS_DATA.IMG_WIDTH = data.width
		LISTENERS_DATA.IMG_HEIGHT = data.height
		self.publisher_depth.publish(self.bridge.cv2_to_imgmsg(LISTENERS_DATA.ALL_IMG, "mono8"))
		

	def listenerB(self, data):
		print("listenerB()")
		cv2.imwrite('map.png', cv2.flip(cv2.rotate(np.reshape(data.data, newshape=(data.info.height, data.info.width)), cv2.ROTATE_90_COUNTERCLOCKWISE), 1))
		LISTENERS_DATA.MAP = cv2.imread('map.png')
		
		
		
		
	def listenerD(self, data):
		print("listenerD()")
		LISTENERS_DATA.ODOM_PATH.append([data.pose.pose.position.x, data.pose.pose.position.y])



	
	def listenerE(self, data):
		print("listenerE()")
		LISTENERS_DATA.SCAN = data.ranges[320]
		LISTENERS_DATA.FULL_SCAN = np.array(data.ranges)#[::-1]
		
		#if LISTENERS_DATA.LASER_PLOT:
		#	#print("Update LaserScan Graph")
		#	self.laser_scan.set_ydata(LISTENERS_DATA.FULL_SCAN[::-1])
		#	plt.ylim(0, 10)
		#	self.fig.canvas.draw()
		#	self.fig.canvas.flush_events()

		#else:
		#	#print("Setup LaserScan Plot")
		#	LISTENERS_DATA.LASER_PLOT = True
		#	plt.ion()
		#	self.fig = plt.figure()
		#	self.ax = self.fig.add_subplot(111)
		#	self.laser_scan, = self.ax.plot(np.linspace(0, LISTENERS_DATA.FULL_SCAN.shape[0], LISTENERS_DATA.FULL_SCAN.shape[0]), LISTENERS_DATA.FULL_SCAN)



	
	def listenerF1(self, data):
		#print("listenerF1()")
		#http://docs.ros.org/melodic/api/actionlib_msgs/html/msg/GoalStatus.html
		try:
			LISTENERS_DATA.GOAL_STATUS = data.status_list[len(data.status_list)-1].text
			LISTENERS_DATA.GOAL_TIME = data.status_list[len(data.status_list)-1].goal_id.stamp
			self.firstErr = True
		except:
			if self.firstErr:
				print("Error with status_list[] index")
				self.firstErr = False
						
				
	def listenerF2(self, data):
		print("listenerF2()")
		LISTENERS_DATA.NEW_GOAL_ID = data.goal.target_pose.header.seq + 1
		
	def listenerF3(self, data):
		print("listenerF3()")
		LISTENERS_DATA.MOVE_PATH.append([data.feedback.base_position.pose.position.x, data.feedback.base_position.pose.position.y])
		
		
		
		
		
##########################################################################################################
class PUBLISHERS_LOG:
	GOAL_SEND = rospy.Time(1, 0)


class PUBLISHERS:

	#Publisher Creation
	def __init__(self):
		print("PUBLISHERS.__init()__")
		
		#insert publishers here
		self.publisher_GOAL = rospy.Publisher("/move_base/goal", MoveBaseActionGoal, queue_size = 2)

		
		
	def publish_GOAL(self, new_x, new_y, angle, move_type="move"):
		print("PUBLISHERS.publish_GOAL()")
		
		
		if move_type == "move":
			print(" ")
		print("Moving to: " + str(np.round(new_x,1)) + ", " + str(np.round(new_y,1)) + ", " + str(angle))
			
		#Angel ranges from [0:359.9]
		if np.mod(angle+180, 360) == 0:
			print("Error with angle Inf handled!")
			angle = 179.99
		
		 
		orientat = quaternion_from_euler(0, 0, angle*(np.pi/180))
		
		
		goal = MoveBaseActionGoal()
		
		goal.goal.target_pose.header.seq = LISTENERS_DATA.NEW_GOAL_ID
		PUBLISHERS_LOG.GOAL_SEND = rospy.Time.now()
		goal.goal.target_pose.header.stamp = PUBLISHERS_LOG.GOAL_SEND
		goal.goal.target_pose.header.frame_id = 'map'
		
		goal.goal.target_pose.pose.position.x = new_x
		goal.goal.target_pose.pose.position.y = new_y
		goal.goal.target_pose.pose.orientation.x = orientat[0]
		goal.goal.target_pose.pose.orientation.y = orientat[1]
		goal.goal.target_pose.pose.orientation.z = orientat[2]
		goal.goal.target_pose.pose.orientation.w = orientat[3]
		
		
		self.publisher_GOAL.publish(goal)




		
	def publish_GOAL2(self, new_x, new_y, angle, move_type="move"):
		
		goal = MoveBaseActionGoal()
		
		goal.goal.target_pose.header.seq = 0
		goal.goal.target_pose.header.stamp = rospy.Time.now()
		goal.goal.target_pose.header.frame_id = 'map'
		print("Goal Two")
		goal.goal.target_pose.pose.position.x = new_x
		goal.goal.target_pose.pose.position.y = new_y
		goal.goal.target_pose.pose.orientation.w = 1
		
		
		self.publisher_GOAL.publish(goal)

		
		
		
		
	def publish_GOAL_RELATIVE(self, new_x, new_y, angle, move_type="move"):
		print("PUBLISHERS.publish_GOAL()")
		
		
		if move_type == "move":
			print("2 ")
		print("Moving relatively to: " + str(np.round(new_x,1)) + ", " + str(np.round(new_y,1)) + ", " + str(angle))
	
			
		#Angle ranges from [0:359.9]
		if np.mod(angle+180, 360) == 0:
			print("Error with angle Inf handled!2")
			angle = 179.99
		
		
		orientat = quaternion_from_euler(0, 0, angle*(np.pi/180))
		
		
		goal = MoveBaseActionGoal()
		
		goal.goal.target_pose.header.seq = LISTENERS_DATA.NEW_GOAL_ID
		PUBLISHERS_LOG.GOAL_SEND = rospy.Time.now()
		goal.goal.target_pose.header.stamp = PUBLISHERS_LOG.GOAL_SEND
		goal.goal.target_pose.header.frame_id = 'base_link'
		
		goal.goal.target_pose.pose.position.x = new_x
		goal.goal.target_pose.pose.position.y = new_y
		goal.goal.target_pose.pose.orientation.x = orientat[0]
		goal.goal.target_pose.pose.orientation.y = orientat[1]
		goal.goal.target_pose.pose.orientation.z = orientat[2]
		goal.goal.target_pose.pose.orientation.w = orientat[3]
		
		
		self.publisher_GOAL.publish(goal)
		
		
		
		
		
		

	#insert publish functions here
	
	
	
	
	
	
	
##########################################################################################################
class CONTROL_DATA:

	poles = {"Red": False, "Blue": False, "Green": False, "Yellow": False}
	walls = {"top":5, "bot":-5, "lef":6, "rig":-6}
	dimen = [3, 3]
	wall_buff = 1.2
	nodes = []
	debug = False


class CONTROL:
	
	def __init__(self):
		#Delay to allow motors to rev up
		sleep(2)
		
		#Reset Turtlebot
		#os.system("rosservice call /gazebo/reset_simulation '{}'")
		
		pub.publish_GOAL(1, 0, np.random.randint(0, 360))
		self.waiter()
		pub.publish_GOAL(0, 0, 0)
		self.waiter()
		
		print("heyyy")
		#os.system("rosrun image_view image_view image:=/camera/rgb/image_raw &")
		#http://momori.animenfo.com:8080/listen.pls


		#Run Main Script
		#while not ([CONTROL_DATA.poles[k] == True for k in CONTROL_DATA.poles]==[True]*4):
		self.main()
		
		
		
		
#---------------------------------------------------------------------------------------------------------	
	def waiter(self, time_publish = 0):
		
		if time_publish == 0:
			time_publish = time.time()

		
		#Define State Conditions for /move_base/status
		#status 1
		pending = "This goal has been accepted by the simple action server."
		#status 2
		preempted = "This goal was canceled because another goal was recieved by the simple action server"
		#status 3
		succeeded = "Goal reached."
		#status 4
		aborted = "Failed to find a valid plan. Even after executing recovery behaviors."
		
		print("stats")
		exit = "NO"
		timeout = 30
		
		while True:
			cv2.waitKey(1)#keep progress chart updated
			if (LISTENERS_DATA.GOAL_TIME.secs == PUBLISHERS_LOG.GOAL_SEND.secs):
				
				#End movement if goal reached
				if (LISTENERS_DATA.GOAL_STATUS == succeeded):
					exit = "Succeeded"
					break
				
				#End movement if goal unreachable
				elif (LISTENERS_DATA.GOAL_STATUS == aborted):
					exit = "Aborted"
					break
			
			#End movement if took too long
			if (time.time()-time_publish > timeout):
				exit = "Timeout"
				break
		
		return (exit)
		

#---------------------------------------------------------------------------------------------------------
	def identify_colour(self):
		middle = 320
		if (not CONTROL_DATA.poles["Blue"]) and np.any(LISTENERS_DATA.IMG_BLUE[middle,:] == 255): 
			im = LISTENERS_DATA.IMG_BLUE
			colour = "Blue"
			print("blue")
		elif (not CONTROL_DATA.poles["Green"]) and np.any(LISTENERS_DATA.IMG_GREEN[middle,:] == 255): 
			im = LISTENERS_DATA.IMG_GREEN
			colour = "Green"
			print("green")
		elif (not CONTROL_DATA.poles["Red"]) and np.any(LISTENERS_DATA.IMG_RED[middle,:] == 255): 
			im = LISTENERS_DATA.IMG_RED
			colour = "Red"
			print("red")
		elif (not CONTROL_DATA.poles["Yellow"]) and np.any(LISTENERS_DATA.IMG_YELLOW[middle,:] == 255): 
			im = LISTENERS_DATA.IMG_YELLOW
			colour = "Yellow"
			print("blue")
		else:
			im = LISTENERS_DATA.IMG_YELLOW*0
			colour = "NONE"
			print("nope")
			
		if not (colour == "NONE"):
		        cv2.imwrite(str("items/" + str(argv[1]) + "/run/" + colour + "_identified.png"), LISTENERS_DATA.IMG_RAW)
			print("write img")
		return (colour, im)	


#---------------------------------------------------------------------------------------------------------
	def GeoLocatePole(self, h, global_angle, x, y):
		
		#print("*****************************")
		#print("*****************************")
		#print("** " + str(h))
		#print("** " + str(global_angle))
		#print("** " + str(x))
		#print("** " + str(y))
		
		cardinal_angle = np.floor(global_angle/90)*90
		print("** " + str(cardinal_angle))
		
		local_angle = global_angle - cardinal_angle
		print("** " + str(local_angle))

		a = (h)*np.cos(local_angle * (np.pi/180))
		b = (h)*np.sin(local_angle * (np.pi/180))
		
		
		if ((cardinal_angle/90) == 0):
			disp = [b, a]
		elif ((cardinal_angle/90) == 1):
			disp = [-b, a]
		elif ((cardinal_angle/90) == 2):
			disp = [-b, -a]
		elif ((cardinal_angle/90) == 3):
			disp = [b, -a]
	
		disp[0] = (disp[0] + x)-1 #Displacement
		disp[1] = disp[1] + y
		
		#print("*****************************")
		#print("*****************************")
		#print("**" + str(disp))
		#print("*****************************")
		
		return disp
		
#---------------------------------------------------------------------------------------------------------
	def CalculateGlobalAngle(self, colour, im, spin_centre):
		#print(" ")
		#print("###############################")
		#print("######### MATHSY PART #########")
		#print("###############################")

		#print(LISTENERS_DATA.FULL_SCAN)
		#print(im[240,:])



                #Find middle of pole (calc global_angle)
		middle = 240
		mask_row = np.array(im[middle,:])
		if np.sum(mask_row == 255) == 0: print("Mask empty."); return (np.nan, 0)

		idx = np.where(mask_row == 255)[0]
		indeces1 = idx[0]
		indeces2 = idx[0] + len(np.split(mask_row[idx],np.where(np.diff(idx) != 255)[0]+1)[0])-1
		pole_middle = np.round((indeces1+indeces2)/2)
		print("## Identifying object at rgb column: " + str(pole_middle))


		
		



		#Image Angle Conversion 		#https://smeenk.com/kinect-field-of-view-comparison/
		width = im.shape[1]
		IMG_FOV = 48.6
		
		pos = pole_middle
		inv_base_angle = pos * (IMG_FOV / width)
		base_angle = IMG_FOV - inv_base_angle
		local_angle = base_angle - (IMG_FOV/2)
		global_angle = local_angle + spin_centre
		#print("# Spin_Centre:     " + str(spin_centre))
		#print("# Width:           " + str(width))
		#print("# IMG_FOV:         " + str(IMG_FOV))
		#print("# Pos:             " + str(pos))
		#print("# Inv_base_angle:  " + str(inv_base_angle))
		#print("# Base_angle:      " + str(base_angle))
		#print("# Local_angle:     " + str(local_angle))
		#print("# Global_angle:    " + str(global_angle))
		
		
		
		F1 = IMG_FOV/2
		angle_from_spin_right = (2*F1) - ((2*pole_middle*F1)/width)
		angle_from_spin_centre = angle_from_spin_right - F1
		global_angle = spin_centre + angle_from_spin_centre
		#print("## Calculated angle_from_spin_right as: " + str(angle_from_spin_right))
		#print("## Calculated angle_from_spin_centre as: " + str(angle_from_spin_centre))
		#print("## Calculated global_angle as: " + str(global_angle))
		
		
		
		
		
		
		
#####################################		
####Laser Scan Functions NEW & FAIL
		
		len_laser_scan = len(LISTENERS_DATA.FULL_SCAN)
		LASER_FOV = 46.6
		
		inv_laser_angle = local_angle + (LASER_FOV/2)
		laser_angle = LASER_FOV - inv_laser_angle
		local_laser_index = laser_angle * (len_laser_scan/LASER_FOV)
		
		
		
		if len_laser_scan - local_laser_index > len(LISTENERS_DATA.FULL_SCAN):
			local_laser_index = np.nan
			distance_to_angle = -1
		else:
			distance_to_angle = LISTENERS_DATA.FULL_SCAN[int(len_laser_scan - local_laser_index)]
			if np.isnan(distance_to_angle):
				distance_to_angle = 0.001
		print("laserscan")

		LASER_FOV = 46.6
		q = len(LISTENERS_DATA.FULL_SCAN)
		F2 = LASER_FOV/2
		angle_from_left = angle_from_spin_centre + F2
		p = int(angle_from_left * (q/(2*F2)))
		
		if p > len(LISTENERS_DATA.FULL_SCAN)-1:
			p = np.nan
			h = -1
		else:
			h = LISTENERS_DATA.FULL_SCAN[p]
			if np.isnan(h):
				h = 0.001

		h = distance_to_angle

		
		
		return(global_angle, h)
		
		
		
		
		
		
		
		
		
		
		
		
#---------------------------------------------------------------------------------------------------------
	def main(self):
		
		
		
		#Start timer and reset path for Visual Object Search
		print(":: ----------------------------------")
		print(":: START TIMER")
		t0 = time.time()
		LISTENERS_DATA.ODOM_PATH = []
		LISTENERS_DATA.MOVE_PATH = []
		
		
		#Define boundary walls
		topwall = CONTROL_DATA.walls["top"]
		bottomwall = CONTROL_DATA.walls["bot"]
		leftwall = CONTROL_DATA.walls["lef"]
		rightwall = CONTROL_DATA.walls["rig"]
		
	

		#Define node coordinates
		x_val = np.round(np.linspace(topwall-CONTROL_DATA.wall_buff, CONTROL_DATA.wall_buff+bottomwall, CONTROL_DATA.dimen[0]), 1)
		y_val = np.round(np.linspace(leftwall-CONTROL_DATA.wall_buff, CONTROL_DATA.wall_buff+rightwall, CONTROL_DATA.dimen[1]), 1)
		


		#Generate pixel conversion for progress graph
		progress_chart = LISTENERS_DATA.MAP
		xpoint = np.round((x_val + bottomwall)*(progress_chart.shape[0]/(bottomwall-topwall)), 0)
		ypoint = np.round((y_val + rightwall)*(progress_chart.shape[1]/(rightwall-leftwall)), 0)
		
		

		#Add nodes to control data
		#Flipping the y like this allows for snacking, reducing wasted movement
		y_val = np.fliplr([y_val])[0]
		ypoint = np.fliplr([ypoint])[0]
		for i in range(len(x_val)):
			y_val = np.fliplr([y_val])[0]
			ypoint = np.fliplr([ypoint])[0]
			print("map")
			for j in range(len(y_val)):
				CONTROL_DATA.nodes.append({"x":x_val[i], "y":y_val[j], "xp":xpoint[i], "yp":ypoint[j]})
				print("points")
		
		
		
		#Loop through each node
		for i in range(len(CONTROL_DATA.nodes)):
		#for i in range(1):

			if [CONTROL_DATA.poles[k] == True for k in CONTROL_DATA.poles]==[True]*4:
				break

			
			
			#Define more readable variables for the new node
			x = CONTROL_DATA.nodes[i]['x']
			y = CONTROL_DATA.nodes[i]['y']
			xp = CONTROL_DATA.nodes[i]['xp']
			yp = CONTROL_DATA.nodes[i]['yp']

			print(" ")
			print(" ")
			print(" ")
			print("}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{")
			print(" ")
			print(" ")
			print(" ")
			


			#Mark destination node on progress_map
			cv2.circle(progress_chart, (int(yp), int(xp)), 4, (255,255,255), -1)
			cv2.imshow('Map', progress_chart)
			cv2.waitKey(1)
			
			


			#Publish the movement coordinates
			pub.publish_GOAL(x, y, 0)
			time_publish = time.time()
			exit = self.waiter(time_publish)
			print(":: Node [" + str(i) + "] - (" + str(x) + ", " + str(y) + ") - " + exit + " - " + str(time.time()-time_publish))
			
			
			#Update progress_map
			if (exit == "Succeeded"):
				cv2.circle(progress_chart, (int(yp), int(xp)), 4, (0,255,0), -1)
			else:
				cv2.circle(progress_chart, (int(yp), int(xp)), 4, (0,0,255), -1)
			cv2.imshow('Map', progress_chart)
			cv2.waitKey(1)
			
			
			#Try to solve any route problems
			if (exit == "Timeout"):
			
			        #Define new positions
			        x = (x-0.25) if (x>0) else (x+0.25)
			        y = (y-0.25) if (y>0) else (y+0.25)
			        
			        
			        pub.publish_GOAL(x, y, 0)
			        time_publish = time.time()
			        exit = self.waiter(time_publish)
			        print(":: Node [" + str(i) + "] - (" + str(x) + ", " + str(y) + ") - " + exit + " - " + str(time.time()-time_publish))
			        
			        
	                        xp = np.round((x + bottomwall)*(progress_chart.shape[0]/(bottomwall-topwall)), 0)
	                        yp = np.round((y + rightwall)*(progress_chart.shape[1]/(rightwall-leftwall)), 0)
			        
			
			        #Update progress_map
			        if (exit == "Succeeded"):
				        cv2.circle(progress_chart, (int(yp), int(xp)), 4, (0,255,0), -1)
			        else:
				        cv2.circle(progress_chart, (int(yp), int(xp)), 4, (0,0,255), -1)
			        cv2.imshow('Map', progress_chart)
			        cv2.waitKey(1)
			

			
			#If node reached; search for poles
			if (exit == "Succeeded"):
			

				#Spin 360 degrees in 45 degree increments (chosen based on rgb fov)
				for l in range(9):
					cv2.waitKey(1)
					pub.publish_GOAL(x, y, l*45, "spin")
					self.waiter()
					
					
					#If a pole is detected in middle row of the mask; identify pole colour
					(colour, im) = self.identify_colour()
					if colour != "NONE":
						print(" ")
						print("|==============================")
						print("Idetified Colour in " + str(l*45) + " degree arc: " + colour)
						
						
						#while the pole is not focused
						global_angle = (l*45);
						while LISTENERS_DATA.ALL_IMG[240, 320] == 0:
							print("LISTENERS_DATA.ALL_IMG[240, 320] = " + str(LISTENERS_DATA.ALL_IMG[240, 320]))
							cv2.waitKey(1)
							#Geolocate the pole
							(global_angle2, _) = self.CalculateGlobalAngle(colour, LISTENERS_DATA.ALL_IMG, global_angle)
							
							if global_angle2 == np.nan:
								##Spin to find pole
								pub.publish_GOAL_RELATIVE(0, 0, 10)
								exit = self.waiter()
								print("Cant find pole :(")
								global_angle = global_angle + 10
							else:
								##Focus on the pole
								pub.publish_GOAL(x, y, global_angle)
								exit = self.waiter()
								cv2.imwrite(str("items/" + str(argv[1]) + "/run/" + colour + "_aligning.png"), LISTENERS_DATA.IMG_RAW)
								global_angle = global_angle2
							
							
						
						##Calculate new position
						h = LISTENERS_DATA.SCAN
						
						
						#Move closer if the focus is over 1m away
						if not(np.isnan(h) or h < 1):
							print("Pole in view: Colour - " + colour)
							cv2.imwrite(str("items/" + str(argv[1]) + "/run/" + colour + "_moving.png"), LISTENERS_DATA.IMG_RAW)
							#(newX, newY) = self.CalculateRelativePosition(x, y, angle, h)
							pub.publish_GOAL_RELATIVE(h-0.5, 0, 0)
							exit = self.waiter()
						
						
						#After moving, focus should be within 1m
						print(":: Pole Found: Colour - " + colour)
						cv2.imwrite(str("items/" + str(argv[1]) + "/run/" + colour + "_found.png"), LISTENERS_DATA.IMG_RAW)
						CONTROL_DATA.poles[colour] = True;

						 
						
						
		print(":: Time Taken: " + str(datetime.timedelta(seconds=int(time.time()-t0))))
		print(":: Poles: "+ str(CONTROL_DATA.poles))
		
		
		cv2.imshow('Map', progress_chart)
		
		for pos in range(len(LISTENERS_DATA.ODOM_PATH)):
			#if np.mod(pos,20) == 0:
			#Plot /odom positions
			px = np.round((LISTENERS_DATA.ODOM_PATH[pos][0] + bottomwall)*(progress_chart.shape[0]/(bottomwall-topwall)), 0)
			py = np.round((LISTENERS_DATA.ODOM_PATH[pos][1] + rightwall)*(progress_chart.shape[1]/(rightwall-leftwall)), 0)
			cv2.circle(progress_chart,(int(py), int(px)), 1, (0,255,255), -1)
			print("you think i know")	
				
		for pos in range(len(LISTENERS_DATA.MOVE_PATH)):
			#Plot /move_base/feedback positions
			px = np.round((LISTENERS_DATA.MOVE_PATH[pos][0] + bottomwall)*(progress_chart.shape[0]/(bottomwall-topwall)), 0)
			py = np.round((LISTENERS_DATA.MOVE_PATH[pos][1] + rightwall)*(progress_chart.shape[1]/(rightwall-leftwall)),0)				
			cv2.circle(progress_chart,(int(py), int(px)), 1, (255,0,255), -1)
			print("i dont")

		cv2.imshow('PathMap', progress_chart)
		cv2.waitKey(1)


		t = str(datetime.datetime.now().time())[0:8].replace(':', '_')
		cv2.imwrite(str("items/" + str(argv[1]) + "/path_" + t + "_.png"), progress_chart)
		print("end")
		#while True:
	        #	if cv2.waitKey(0) == 27:
		#		break
		

##########################################################################################################
#CONTROL_DATA.poles = "POLES INITIATED" #No functions associated to CONTROL_DATA, just variables.

rospy.init_node('XXXX_CONTROL_SYSTEM_XXXX', anonymous=True)
rate = rospy.Rate(10)

if not os.path.exists('items/'): os.mkdir("items/")
if not os.path.exists('items/' + str(argv[1]) + "/"): os.mkdir("items/" + str(argv[1]) + "/")
if not os.path.exists('items/' + str(argv[1]) + "/run/"): os.mkdir("items/" + str(argv[1]) + "/run/")

lis = LISTENERS() #This is the only time LISTENERS is called as all functions within are automatic.

pub = PUBLISHERS() #This is used to send messages to publishers.

controlSystem = CONTROL() #This initiates the system.

cv2.destroyAllWindows()

plt.close(1)

sys.exit()


