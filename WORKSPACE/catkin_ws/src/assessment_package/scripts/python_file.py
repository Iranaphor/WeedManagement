import rospy
from time import sleep
import os.path

class CONTROL:
	def __init__(self):
		while True:
			sleep(1)
			print(os.path.exists('myfile.txt'))
			if os.path.exists('myfile.txt')		
				return;

if __name__ == '__main__':
	rospy.init_node('python_file', anonymous=True)
	cs = CONTROL()
	rospy.spin()







