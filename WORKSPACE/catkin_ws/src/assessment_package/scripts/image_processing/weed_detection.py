import cv2
import numpy as np
import matplotlib.pyplot as plt
from generic import imreconstruct, imfill, imbinarize

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
	dirtMask1 = imbinarize(im_h, 0.2)
	dirtMask = (dirtMask1==0)

	# Weed Mask
	weedMask = np.array(im_h>im_s, dtype='uint8');

	# Overlay
	Overlay = im.copy()
	Overlay[:,:,2] = Overlay[:,:,2]+weedMask*100;
	Overlay[:,:,1] = Overlay[:,:,1]+plantMask*100;
	Overlay[:,:,0] = Overlay[:,:,0]+dirtMask*100;

	#cv2.imwrite('out/Overlay.png', Overlay)
	#cv2.imwrite('out/plantMask.png', plantMask*255)
	#cv2.imwrite('out/weedMask.png', weedMask*255)
	#cv2.imwrite('out/dirtMask.png', dirtMask*255)

	return (Overlay, weedMask, plantMask, dirtMask)


def cabbage(IMG_RAW, strel_disk_25, strel_disk_35):

	im_hsv = cv2.cvtColor(IMG_RAW, cv2.COLOR_BGR2HSV)
	im_h = im_hsv[:,:,0].astype(float)/180

	
	# Dirt Mask
	#im_dirt_1 = [1-im_h]*im_h; #reference using im_dirt_1[0,:,:]
	im_dirt_2 = imbinarize(im_h, .145)
	dirtMask1 = imfill(im_dirt_2, .5);
	dirtMask = (dirtMask1==0)

	# Plant Mask
	#strel_disk_35 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_35.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
	plantMask = cv2.morphologyEx(dirtMask1.astype(np.uint8), cv2.MORPH_OPEN, strel_disk_35)


	# Weed Mask
	#strel_disk_25 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_25.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
	im_weed_1 = cv2.dilate(plantMask, strel_disk_25, iterations=1) + dirtMask
	weedMask1 = imbinarize(im_weed_1,0)
   	weedMask = (weedMask1==0);

	# Overlay
	Overlay = IMG_RAW.copy()
	Overlay[:,:,2] = Overlay[:,:,2]+weedMask*100;
	Overlay[:,:,1] = Overlay[:,:,1]+plantMask*100;
	Overlay[:,:,0] = Overlay[:,:,0]+dirtMask*100;

	#cv2.imwrite('out/Overlay.png', Overlay)
	#cv2.imwrite('out/plantMask.png', plantMask*255)
	#cv2.imwrite('out/weedMask.png', weedMask*255)
	#cv2.imwrite('out/dirtMask.png', dirtMask*255)

	return (Overlay, weedMask, plantMask, dirtMask)

if __name__ == '__main__':
	cabbage(cv2.imread('image9.png'))



