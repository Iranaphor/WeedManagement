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
    
    #make empty array (padd by 2)
    emptyMask = np.zeros((h+2, w+2), np.uint8)
    emptyMask[0,0] = 1
    
    #imreconstruct(emptyMask, im_in)
    rec = imreconstruct(emptyMask, in2, np.ones((3,3),np.uint8))
    
    RET = (rec[1:h+1,1:w+1]==0)

    #return not(reconstructed)
    return RET

def imbinarize(im_in, threshold, maxvalue=1):
    if maxvalue==1:
        _,bina = cv2.threshold(im_in.astype(np.double),threshold,maxvalue,cv2.THRESH_BINARY)
    else:
        _,bina = cv2.threshold(im_in.astype(np.uint8),threshold,maxvalue,cv2.THRESH_BINARY)
    return bina

def imdilate(I, kernel):
    return cv2.dilate(I.astype(np.uint8),  kernel, iterations=1)

def imerode(I, kernel):
    return cv2.erode(I.astype(np.uint8),  kernel, iterations=1)

def imclose(I, kernel):
    return cv2.morphologyEx(I.astype(np.uint8), cv2.MORPH_CLOSE, kernel)

def imopen(I, kernel):
    return cv2.morphologyEx(I.astype(np.uint8), cv2.MORPH_OPEN, kernel)

def bgr2hsv(I):
    return cv2.cvtColor(I.astype(np.uint8), cv2.COLOR_BGR2HSV)

def imrotate(image, angle, e,x): #https://stackoverflow.com/a/9042907
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def strel(style, size):
    if style == "disk":
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
    elif style == "square":
        return np.ones((size,size),np.uint8)

def T(I):
    return cv2.transpose(np.array(I))

def summ(I,dimension='column'):
    if dimension == 'all':
	return sum([sum(row) for row in I])
    else:
        if dimension=='row':
            I = cv2.transpose(I)
        return [sum(row) for row in I]




