import cv2
import numpy as np
import matplotlib.pyplot as plt
from generic import imreconstruct, imfill, imbinarize, imdilate, imerode, imclose, imopen, bgr2hsv, imrotate, strel, T, summ
from sys import argv
import os

def basil(IMG_RAW, filter_type=""):
	im_hsv = bgr2hsv(IMG_RAW)
	
	im = IMG_RAW.copy()
	im_hsv = im_hsv.copy()
	im_h = im_hsv[:,:,0].astype(float)/180
	im_s = im_hsv[:,:,1].astype(float)/256

	# Weed Mask
	im_weed_1 = np.array(im_h>im_s, dtype='uint8')
	im_weed_2 = imclose(im_weed_1, strel('square',5))
	im_weed_3 = imerode(im_weed_2, strel('square',5))
	weedMask = imreconstruct(im_weed_3, im_weed_2, strel('square',3))

	if filter_type=="weed_only":
                return (weedMask)
        
	# Dirt Mask
	dirtMask1 = 1-imbinarize(im_h, 0.2)
	dirtMask = ((dirtMask1+weedMask)>0)-weedMask
	
	
	# Plant Mask 2
	plantMask = 1-(dirtMask+weedMask)

	# Overlay
	Overlay = im.copy()
	Overlay[:,:,2] = Overlay[:,:,2]+weedMask*100;
	Overlay[:,:,1] = Overlay[:,:,1]+plantMask*100;
	Overlay[:,:,0] = Overlay[:,:,0]+dirtMask*100;

	cv2.imwrite('/media/computing/141E-156D/GITHUB REPOSITORIES/MODULES/ROBOT PROGRAMMING/Weed Extraction/Overlay.png', Overlay)
	#cv2.imwrite('out/plantMask.png', plantMask*255)
	#cv2.imwrite('out/weedMask.png', weedMask*255)
	#cv2.imwrite('out/dirtMask.png', dirtMask*255)

	return (Overlay, weedMask, plantMask, dirtMask)


def cabbage(IMG_RAW):

	im_hsv = bgr2hsv(IMG_RAW)
	im_h = im_hsv[:,:,0].astype(float)/180

	
	# Dirt Mask
	#im_dirt_1 = [1-im_h]*im_h; #reference using im_dirt_1[0,:,:]
	im_dirt_2 = imbinarize(im_h, .145)
	dirtMask1 = imfill(im_dirt_2, .5);
	dirtMask = np.array(dirtMask1==0, dtype='uint8')

	# Plant Mask
	plantMask = np.array(cv2.morphologyEx(dirtMask1.astype(np.uint8), cv2.MORPH_OPEN, strel('disk',35)), dtype='uint8')


	# Weed Mask
	im_weed_1 = imdilate(plantMask, strel('disk',25)) + dirtMask
	weedMask1 = imbinarize(im_weed_1,0)
	weedMask = np.array(weedMask1==0, dtype='uint8')

	# Overlay
	Overlay = IMG_RAW.copy()
	Overlay[:,:,2] = Overlay[:,:,2]+weedMask*100;
	Overlay[:,:,1] = Overlay[:,:,1]+plantMask*100;
	Overlay[:,:,0] = Overlay[:,:,0]+dirtMask*100;

	cv2.imwrite('/media/computing/141E-156D/GITHUB REPOSITORIES/MODULES/ROBOT PROGRAMMING/Weed Extraction/Overlay.png', Overlay)
	#cv2.imwrite('out/plantMask.png', plantMask*255)
	#cv2.imwrite('out/weedMask.png', weedMask*255)
	#cv2.imwrite('out/dirtMask.png', dirtMask*255)

	return (Overlay, weedMask, plantMask, dirtMask)


def onion(IMG_RAW,n):
	im_hsv = bgr2hsv(IMG_RAW)
	im_r = IMG_RAW[:,:,0].astype(int)
	im_g = IMG_RAW[:,:,1].astype(int)
	im_b = IMG_RAW[:,:,2].astype(int)
	im_h = im_hsv[:,:,0].astype(float)/180


	# Dirt Mask
	dirtMask1 = imbinarize(im_h, .17);
	dirtMask = np.array(dirtMask1==0, dtype='uint8')


	# Plant Mask
	print(np.amax(im_r))
	print(np.amax(im_g))
	x = np.array((im_r+im_g)*2, dtype='uint8')
	cv2.imwrite('/media/computing/141E-156D/GITHUB REPOSITORIES/MODULES/ROBOT PROGRAMMING/Weed Extraction/im_plant_1a.png', x)

	print(np.amax(x))
	print(np.amax(im_b))
	im_plant_1 = np.array(x<im_b, dtype='uint8')
	print(summ(im_plant_1,'all'))
	cv2.imwrite('/media/computing/141E-156D/GITHUB REPOSITORIES/MODULES/ROBOT PROGRAMMING/Weed Extraction/im_plant_1b.png', im_plant_1*255)

	im_plant_rot = imrotate(im_plant_1,n,'bilinear','crop');
	#cv2.imwrite('/media/computing/141E-156D/GITHUB REPOSITORIES/MODULES/ROBOT PROGRAMMING/Weed Extraction/im_plant_rot.png', im_plant_rot*255)

	im_plant_2 = T(T(im_plant_rot)*T(summ(im_plant_rot,'column')));
	#cv2.imwrite('/media/computing/141E-156D/GITHUB REPOSITORIES/MODULES/ROBOT PROGRAMMING/Weed Extraction/im_plant_2.png', im_plant_2)
	

	im_plant_3 = im_plant_2/np.amax(im_plant_2)
	print(np.amax(im_plant_2))
	#cv2.imwrite('/media/computing/141E-156D/GITHUB REPOSITORIES/MODULES/ROBOT PROGRAMMING/Weed Extraction/im_plant_3.png', im_plant_3*255)
	

	im_plant_4 = imbinarize(im_plant_3,0.35);
	im_plant_5 = imdilate(im_plant_4, strel('disk',45));
	plantMask = imrotate(im_plant_5,-n,'bilinear','crop');
	#cv2.imwrite('/media/computing/141E-156D/GITHUB REPOSITORIES/MODULES/ROBOT PROGRAMMING/Weed Extraction/plantMask.png', plantMask*255)

	# Weed Mask
	weedMask1 = plantMask+dirtMask;
	weedMask = np.array(weedMask1==0, dtype='uint8')
	im_weed_target_1b = imfill(weedMask, .5);
	im_weed_target_2b = imerode(im_weed_target_1b, strel('disk',50))

	# Overlay
	Overlay = IMG_RAW.copy()
	Overlay[:,:,2] = Overlay[:,:,2]+weedMask*100;
	Overlay[:,:,1] = Overlay[:,:,1]+plantMask*100;
	Overlay[:,:,0] = Overlay[:,:,0]+dirtMask*100;
	Overlay[:,:,2] = Overlay[:,:,2]+im_weed_target_2b*255

	cv2.imwrite('/media/computing/141E-156D/GITHUB REPOSITORIES/MODULES/ROBOT PROGRAMMING/Weed Extraction/Overlay.png', Overlay)
	#cv2.imwrite('out/plantMask.png', plantMask*255)
	#cv2.imwrite('out/weedMask.png', weedMask*255)
	#cv2.imwrite('out/dirtMask.png', dirtMask*255)

	return (Overlay, weedMask, plantMask, dirtMask)








if __name__ == '__main__':
	onion(cv2.imread('Analysis1a.png'),179)
	#cabbage(cv2.imread('Analysis2.png'))
	#basil(cv2.imread('Analysis3.png'),'')



