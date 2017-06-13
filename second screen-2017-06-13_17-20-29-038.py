import cv2
import numpy as np


cam = cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,720)
#create image
image = cam.read()

#draw rectangle into original image
cv2.rectangle(image,(100,100),(300,300),(0,0,255),3)

#crop image
crop = image[100:300,100:300].copy()

#draw rectangle into cropped image
cv2.rectangle(crop,(0,50),(150,150),(0,255,255),3)
cv2.imshow('Result', crop)
cv2.waitKey()    

cv2.destroyAllWindows()
