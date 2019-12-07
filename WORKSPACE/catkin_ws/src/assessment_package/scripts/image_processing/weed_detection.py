import cv2
import numpy as np
import matplotlib.pyplot as plt
from generic import *
from sys import argv
import os

def basil(IMG_RAW, filter_type=""):
	im_hsv = bgr2hsv(IMG_RAW)
	
	im = IMG_RAW.copy()
	im_hsv = im_hsv.copy()
	im_h = im_hsv[:,:,0].astype(float)/180
	im_s = im_hsv[:,:,1].astype(float)/255

	# Weed Mask
	im_weed_1 = np.array(im_h>im_s, dtype='uint8')
	im_weed_1 = imclose(im_weed_1, strel('disk',5))
	im_weed_2 = imopen(im_weed_1, strel('disk',5))
	im_weed_3 = imerode(im_weed_2, strel('disk',5))
	#im_weed_4 = (im_weed_2+im_weed_3)*125
	weedMask = imclearborder(imreconstruct(im_weed_3, im_weed_2, strel('disk',10)),2) #adjust border size
	
	if filter_type=="weed_only":
                return (weedMask)
        
	# Dirt Mask
	dirtMask1 = iminvert(imbinarize(im_h, 0.2))
	dirtMask = ((dirtMask1+weedMask)>0)-weedMask
	
	
	# Plant Mask 2
	plantMask = iminvert(dirtMask+weedMask)

	# Overlay
	Overlay = im.copy()
	Overlay[:,:,2] = Overlay[:,:,2]+weedMask*100;
	Overlay[:,:,1] = Overlay[:,:,1]+plantMask*100;
	Overlay[:,:,0] = Overlay[:,:,0]+dirtMask*100;

	return (Overlay, weedMask, plantMask, dirtMask)


def cabbage(IMG_RAW):

	im_hsv = bgr2hsv(IMG_RAW)
	im_h = im_hsv[:,:,0].astype(float)/180

	
	# Dirt Mask
	im_dirt_1 = (1-im_h)*im_h; #reference using im_dirt_1[0,:,:]
	im_dirt_1 = np.array(im_dirt_1*255,dtype='uint8')*255
	im_dirt_1 = imbinarizerange(im_dirt_1, 150,215)
	#im_dirt_1 = imbinarize(im_h, .2)
	dirtMask1 = imclearborder(imfill(im_dirt_1),2)
	#dirtMask2 = imerode(dirtMask1,strel('disk', 7))
	dirtMask3 = iminvert(dirtMask1)
	dirtMask = addborder(dirtMask3, 20)
	
	# Plant Mask
	plantMask = np.array(imopen(dirtMask1.astype(np.uint8), strel('disk',35)), dtype='uint8')
	
	# Weed Mask
	im_weed_1 = imdilate(plantMask, strel('disk',25)) + dirtMask
	weedMask1 = imbinarize(im_weed_1,0)
	weedMask2 = imopen(weedMask1,strel('disk',2))
	weedMask3 = iminvert(imerode(weedMask2,strel('disk',10)))
	weedMask = imclearborder(weedMask3)
	
	# Overlay
	Overlay = IMG_RAW.copy()
	Overlay[:,:,2] = Overlay[:,:,2]+weedMask*100;
	Overlay[:,:,1] = Overlay[:,:,1]+plantMask*100;
	Overlay[:,:,0] = Overlay[:,:,0]+dirtMask*100;
	
	return (Overlay, weedMask, plantMask, dirtMask)


def onion(IMG_RAW,n):

	im_hsv = bgr2hsv(IMG_RAW)
	im_r = IMG_RAW[:,:,2].astype(float)
	im_g = IMG_RAW[:,:,1].astype(float)
	im_b = IMG_RAW[:,:,0].astype(float)
	im_h = im_hsv[:,:,0].astype(float)/180

	# Plant Mask
	x = np.array(np.ceil(im_r/2)+np.ceil(im_g/2), dtype='uint8')
	im_plant_1 = np.array(x<im_b, dtype='uint8')
	im_plant_rot = imrotate(im_plant_1,n,'bilinear','crop') #DOES NOT WORK THE SAME AS MATLAB
	im_plant_2 = T(T(im_plant_rot)*T(summ(im_plant_rot,'column')))
	np.seterr(divide='ignore', invalid='ignore')
	im_plant_3 = np.divide(im_plant_2.astype(float),np.amax(im_plant_2)) #Normalize image
	im_plant_4 = imbinarize(im_plant_3,0.35)
	im_plant_5 = imdilate(im_plant_4, strel('disk',25))
	plantMask = imrotate(im_plant_5,-n,'bilinear','crop')

	# Dirt Mask
	dirtMask1 = imbinarize(im_h, .17);
	dirtMask = np.array(dirtMask1==0, dtype='uint8')

	# Weed Mask
	weedMask1 = plantMask+dirtMask;
	weedMask = imerode(iminvert(weedMask1), strel('disk',3))
	im_weed_target_1b = imfill(weedMask);
	im_weed_target_2b = imclearborder(imerode(im_weed_target_1b, strel('disk',10)))

	# Overlay
	Overlay = IMG_RAW.copy()
	Overlay[:,:,2] = Overlay[:,:,2]+im_weed_target_2b*100;
	Overlay[:,:,1] = Overlay[:,:,1]+plantMask*100;
	Overlay[:,:,0] = Overlay[:,:,0]+dirtMask*100;
	Overlay[:,:,0] = Overlay[:,:,0]+im_weed_target_2b*255
	Overlay[:,:,1] = Overlay[:,:,1]+im_weed_target_2b*255
	Overlay[:,:,2] = Overlay[:,:,2]+im_weed_target_2b*255

	return (Overlay, im_weed_target_2b, plantMask, dirtMask)








if __name__ == '__main__':
	print("hi")	
	#onion(cv2.imread('Analysis1a.png'),179)
	#cabbage(cv2.imread('Analysis2.png'))
	#basil(cv2.imread('Analysis3.png'),'')



