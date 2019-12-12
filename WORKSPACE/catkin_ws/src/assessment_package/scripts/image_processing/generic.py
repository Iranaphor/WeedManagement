import cv2
import numpy as np

#Reconstrust any blobs in the img, compariging against their relative locations in the mask
def imreconstruct(img, mask, st): #img is dilated
	_,mask = cv2.threshold(mask,0.5,1, cv2.THRESH_BINARY)
	#cv2.imwrite('out/MASK.png', mask*255)
	#cv2.imwrite('out/IMG.png', img*255)
	img_new = img.copy()

	#i=0
	while True:
		#i+=1;
		#print(i)
		img = mask*cv2.dilate(img, st, iterations=1)
		#if i%100==0:
			#cv2.imwrite("out/IMG_"+str(i)+".png", img*255)
		if (np.array_equal(img_new,img)):
			#cv2.imwrite("out/IMG_"+str(i)+".png", img*255)
			return img
		img_new = img
			
#Fill empty regions within the image
def imfill(im_in): #swap this out to only accept binary images
	h, w = im_in.shape[:2]
	
	#invert im_in (padd by 2)
	in2 = np.ones((h+2, w+2), np.uint8)
	in2[1:h+1,1:w+1] = im_in==0
	
	#make empty array (padd by 2)
	emptyMask = np.zeros((h+2, w+2), np.uint8)
	emptyMask[0,0] = 1
	
	#imreconstruct(emptyMask, im_in)
	rec = imreconstruct(emptyMask, in2, np.ones((3,3),np.uint8))
	
	RET = (rec[1:h+1,1:w+1]==0)

	return RET

#Convert the image into a binary image
def imbinarize(im_in, threshold, maxvalue=1):
	if maxvalue==1:
		_,bina = cv2.threshold(im_in.astype(np.double),threshold,maxvalue,cv2.THRESH_BINARY)
	else:
		_,bina = cv2.threshold(im_in.astype(np.uint8),threshold,maxvalue,cv2.THRESH_BINARY)
	return bina

#Convert the image into a binary image given a range of values
def imbinarizerange(im_in, minthreshold, maxthreshold):
	bina1 = np.array(im_in>minthreshold,dtype='uint8')
	bina2 = np.array(im_in<maxthreshold,dtype='uint8')
	return bina1*bina2

#Invert the image
def iminvert(I):
	return np.array(I==0, dtype='uint8')

#Dilate the image
def imdilate(I, kernel):
	return np.array(cv2.dilate(I.astype(np.uint8),  kernel, iterations=1), dtype='uint8')

#Erode the image
def imerode(I, kernel):
	return np.array(cv2.erode(I.astype(np.uint8),  kernel, iterations=1), dtype='uint8')

#Erode then Dilate the image
def imclose(I, kernel):
	return np.array(cv2.morphologyEx(I.astype(np.uint8), cv2.MORPH_CLOSE, kernel), dtype='uint8')

#Dilate then Erode the image
def imopen(I, kernel):
	return np.array(cv2.morphologyEx(I.astype(np.uint8), cv2.MORPH_OPEN, kernel), dtype='uint8')

#Convert to bgr
def bgr2hsv(I):
	return np.array(cv2.cvtColor(I.astype(np.uint8), cv2.COLOR_BGR2HSV), dtype='uint8')

#Rotate the image
def imrotate(image, angle, null_1, null_2): #https://stackoverflow.com/a/9042907
	image_center = tuple(np.array(image.shape[1::-1]) / 2)
	rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
	result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
	return result

#Create a structuring element
def strel(style, size):
	if style == "disk":
		return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
	elif style == "square":
		return np.ones((size,size),np.uint8)

#Transpose the image
def T(I):
	return cv2.transpose(np.array(I))

#Take the sum across a defined dimension
def summ(I,dimension='column'):
	if dimension == 'all':
		return sum([sum(row) for row in I])
	else:
		if dimension=='row':
			I = cv2.transpose(I)
		return [sum(row) for row in I]

#Clear blobs from the border
def imclearborder(I, border=10):

	# Ensure type definition
	I = np.array(I, dtype='uint8')
	
	# Create Border
	Mask = genborder(I, border)

	# Extract Intersections of blobs and border
	Intersections = np.array(Mask & I, dtype='uint8')
	
	# Reconstruct the mask containing only edges
	rec = imreconstruct(Intersections, I, strel('square',10))
	
	# InputMask - Edgepieces
	filtered = np.array(I - rec, dtype='uint8');
	
	return filtered

#Generate a border around the image
def genborder(I, border=20):
	s=(I.shape[0], I.shape[1])
	Mask = np.ones(s,dtype='uint8')
	Mask[border:s[0]-border,border:s[1]-border]=0
	return Mask

#Apply a border to an image
def addborder(I, border=20):
	return I|genborder(I, border)

#Find the centroids of each image
#Adapted from https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
def imfindcentroids(I):
	centroids = []
	
	# Find contours in the binary image
	_,contours,_ = cv2.findContours(I, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	
	# Calculate centrepoint of each blob
	for c in contours:
		# calculate moments for each contour
		M = cv2.moments(c)
		
		# calculate x,y coordinate of center
		if M["m00"] != 0:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
		else:
			cX, cY = 0, 0
		
		centroids.append((cX,cY))
		
	return centroids

































