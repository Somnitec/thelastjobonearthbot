import cv2
import urllib 
import numpy as np

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
        cv2.imshow('output',cam)
        if cv2.waitKey(1) ==27:
            cv2.destroyAllWindows()
            exit(0)    
