#import sharedvariables
from theLastJobOnEarthBot import *

#sharedvariables.init()

import cv2
import urllib 
import numpy as np
import random

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

screenwidth=1024
screenheight=1280
stream=urllib.urlopen('http://192.168.10.140:8080/video')
bytes=''
while True:
    bytes+=stream.read(16384)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        cam = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)

        height, width, channels = cam.shape
        
        desiredwidth=int(float(screenwidth)/screenheight*height)
        startpoint=int((width-desiredwidth)/2)

        #print screenwidth, screenheight,height, width,desiredwidth,startpoint
        crop=cam[0:height,startpoint:startpoint+desiredwidth]

        img=cv2.resize(crop,(screenwidth,screenheight))

        #facedetectionstuff
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            img = cv2.circle(img,(x+w/2,y+h/2),h/2,(255,255,255),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            eyepoints = []
            for (ex,ey,ew,eh) in eyes:
                #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,255),2)
                eyepoints.append([ex+ew/2,ey+eh/2])
                cv2.circle(roi_color,(ex+ew/2,ey+eh/2),ew/4, (255,255,255),-1)
            cv2.polylines(roi_color, np.int32([eyepoints]), 1, (255,255,255),2)

            smile = smile_cascade.detectMultiScale(roi_gray)
            points = []
            for (ex,ey,ew,eh) in smile:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,255),2)
                points.append([ex+ew/2,ey+eh/2])
            cv2.polylines(roi_color, np.int32([points]), 1, (255,255,255),1)

        #interface stuff
        font = cv2.FONT_HERSHEY_SIMPLEX

        for i in range(0, 30):
            cv2.putText(img,str(random.random()),((4*screenwidth/6)+10,30+(i*35)), font, 1,(255,255,255),1)
        
        cv2.rectangle(img,(0,0),(screenwidth,screenheight),(255,255,255),6)
        cv2.rectangle(img,((4*screenwidth/6),0),(screenwidth,(6*screenheight)/7),(255,255,255),6)
        cv2.rectangle(img,(0,(6*screenheight)/7),(screenwidth,screenheight),(0,0,0),-1)
        cv2.rectangle(img,(0,(6*screenheight)/7),(screenwidth,screenheight),(255,255,255),6)

        cv2.putText(img,'blabla',(10,screenheight-100),font,1,(255,255,255))
        

        cv2.namedWindow("output", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("output",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

        cv2.imshow('output',img)
        
    if cv2.waitKey(1) ==27:
        break
cv2.destroyAllWindows()
  
