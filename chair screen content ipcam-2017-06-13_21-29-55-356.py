import cv2
import urllib 
import numpy as np

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
        
        desiredwidth=screenwidth/screenheight*height
        startpoint=(width-desiredwidth)/2

        print screenwidth, screenheight,height, width,desiredwidth,startpoint
        img=cam[0:height,startpoint:startpoint+desiredwidth]

        
        cv2.imshow('output',img)
        
    if cv2.waitKey(1) ==27:
        break

cv2.destroyAllWindows()
  
