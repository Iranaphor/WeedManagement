import cv2
import numpy as np
import matplotlib.pyplot as plt
from generic import imreconstruct, imfill, imbinarize

def basil(IMG_RAW, filter_type=""):
	IMG_RAW_HSV = cv2.cvtColor(IMG_RAW, cv2.COLOR_BGR2HSV)

	im = IMG_RAW.copy()
	im_hsv = IMG_RAW_HSV.copy()
	im_h = im_hsv[:,:,0].astype(float)/180
	im_s = im_hsv[:,:,1].astype(float)/256

	if filter_type=="weed_only":
		im_weed_1 = np.array(im_h>im_s, dtype='uint8')
		im_weed_2 = cv2.morphologyEx(im_weed_1, cv2.MORPH_CLOSE, np.ones((5,5)))
		im_weed_3 = cv2.erode(im_weed_2, np.ones((5,5)), iterations=1)
		weedMask = imreconstruct(im_weed_3, im_weed_2, np.ones((3,3),np.uint8))
		return (weedMask)

	# Weed Mask
	im_weed_1 = np.array(im_h>im_s, dtype='uint8')
	im_weed_2 = cv2.morphologyEx(im_weed_1, cv2.MORPH_CLOSE, np.ones((5,5)))
	im_weed_3 = cv2.erode(im_weed_2, np.ones((5,5)), iterations=1)
	weedMask = imreconstruct(im_weed_3, im_weed_2, np.ones((3,3),np.uint8))
	
	
	# Dirt Mask
	dirtMask1 = 1-imbinarize(im_h, 0.2)
	dirtMask = ((dirtMask1+weedMask)>0)-weedMask
	
	
	# Plant Mask 2
	plantMask = 1-(dirtMask+weedMask);

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
	dirtMask = np.array(dirtMask1==0, dtype='uint8')

	# Plant Mask
	#strel_disk_35 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_35.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
	plantMask = np.array(cv2.morphologyEx(dirtMask1.astype(np.uint8), cv2.MORPH_OPEN, strel_disk_35), dtype='uint8')


	# Weed Mask
	#strel_disk_25 = cv2.cvtColor(cv2.imread("image_processing/strel_disk_25.png").astype(np.uint8), cv2.COLOR_BGR2GRAY)
	im_weed_1 = cv2.dilate(plantMask, strel_disk_25, iterations=1) + dirtMask
	weedMask1 = imbinarize(im_weed_1,0)
   	weedMask = np.array(weedMask1==0, dtype='uint8')

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



