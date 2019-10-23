import cv2
import numpy as np
import matplotlib.pyplot as plt
from .generic import imreconstruct, imfill

def basil(IMG_RAW):
	IMG_RAW_HSV = cv2.cvtColor(IMG_RAW, cv2.COLOR_BGR2HSV)

	im = IMG_RAW.copy()
	im_hsv = IMG_RAW_HSV.copy()
	im_h = im_hsv[:,:,0].astype(float)/180
	im_s = im_hsv[:,:,1].astype(float)/256

	# Plant Mask
	im_plant_2 = im_h.copy();
	x=np.round(im_plant_2*100);
	im_plant_2[x!=24] = 0;
	im_plant_2[x==24] = 1;

	im_plant_3 = cv2.morphologyEx(im_plant_2, cv2.MORPH_OPEN, np.ones((10,10),np.uint8))
	im_plant_4 = imreconstruct(im_plant_3,im_plant_2, np.ones((10,10),np.uint8))
	plantMask = imfill(im_plant_4*255, 128)


	# Dirt Mask
	_,dirtMask1 = cv2.threshold(im_h,0.2,1,cv2.THRESH_BINARY);
	dirtMask = (dirtMask1==0)

	# Weed Mask
	weedMask = (im_h>im_s);

	# Weed Overlay
	Overlay = im.copy()
	Overlay[:,:,2] = Overlay[:,:,2]+weedMask*100;
	Overlay[:,:,1] = Overlay[:,:,1]+plantMask*100;
	Overlay[:,:,0] = Overlay[:,:,0]+dirtMask*100;

	cv2.imwrite('out/Overlay.png', Overlay)
	cv2.imwrite('out/plantMask.png', plantMask*255)
	cv2.imwrite('out/im_weedMask.png', weedMask*255)
	cv2.imwrite('out/im_dirtMask1.png', dirtMask*255)


def cabbage(IMG_RAW):
	IMG_RAW_HSV = cv2.cvtColor(IMG_RAW, cv2.COLOR_BGR2HSV)

	im = IMG_RAW.copy()
	im_hsv = IMG_RAW_HSV.copy()
	im_h = im_hsv[:,:,0].astype(float)/180

	
	# Dirt Mask
	im_dirt_1 = [1-im_h].*im_h;
	im_dirt_2 = cv2.threshold(im_h,.145,1,cv2.THRESH_BINARY)
	dirtMask = imfill(im_dirt_2, .5);

	# Plant Mask
	strel_disk_35 = cv2.imread("strel_disk_35.png");
	plantMask = imopen(~dirtMask, strel_disk_35);
	im_plant_3 = cv2.morphologyEx(im_plant_2, cv2.MORPH_OPEN, np.ones((10,10),np.uint8))


	

if __name__ == '__main__':
	main()
	basil(cv2.imread('image4.png'))



