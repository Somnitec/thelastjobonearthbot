from threading import Thread
import cv2
import urllib 
import numpy as np
import random

stream=urllib.urlopen('http://192.168.10.140:8080/video')
bytes=''

def botthings():
    while True:
        bytes+=stream.read(16384)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            rawcam = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            cv2.imshow('output',rawcam)
        
        if cv2.waitKey(1) ==27:
            break
    cv2.destroyAllWindows()


def screenthings():
    while True:
        #print 'B\n'
        val = 1

if __name__ == "__main__":
    t1 = Thread(target = botthings)
    t2 = Thread(target = screenthings)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    while True:
        pass
