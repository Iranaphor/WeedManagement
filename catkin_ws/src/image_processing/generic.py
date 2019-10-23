import cv2
import numpy as np


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
			

def imfill(im_in, n): #swap this out to only accept binary images
	h, w = im_in.shape[:2]
	
	#invert im_in (padd by 2)
	in2 = np.ones((h+2, w+2), np.uint8)
	in2[1:h+1,1:w+1] = im_in==0
	#cv2.imwrite('out/in2.png', in2*255)
	
	#make empty array (padd by 2)
	emptyMask = np.zeros((h+2, w+2), np.uint8)
	emptyMask[0,0] = 1
	#cv2.imwrite('out/emptyMask.png', emptyMask*255)
	
	#imreconstruct(emptyMask, im_in)
	rec = imreconstruct(emptyMask, in2, np.ones((3,3),np.uint8))
	#cv2.imwrite('out/rec.png', rec*255)
	
	RET = (rec[1:h+1,1:w+1]==0)
	#cv2.imwrite('out/RET.png', RET*255)

	#return not(reconstructed)
	return RET
	
