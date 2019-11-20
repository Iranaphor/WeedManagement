
import rospy
from time import sleep
import os.path

class CONTROL:
	def __init__(self):
		for i in range(10):
			sleep(1)
			print(os.path.exists('myfile.txt'))
			if os.path.exists('myfile.txt'):	
				return;

if __name__ == '__main__':
	print("hello")
	rospy.init_node('python_file_1', anonymous=True)
	c = CONTROL()
	rospy.spin()







