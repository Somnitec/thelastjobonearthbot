import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')



class Cam():

  def __init__(self, url):
    
    self.stream = requests.get(url, stream=True)
    self.thread_cancelled = False
    self.thread = Thread(target=self.run)
    print "camera initialised"

    
  def start(self):
    self.thread.start()
    print "camera stream started"
    
  def run(self):
    bytes=''
    while not self.thread_cancelled:
      try:
        bytes+=self.stream.raw.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
          jpg = bytes[a:b+2]
          bytes= bytes[b+2:]
          img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
 
          gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

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
            cv2.polylines(roi_color, np.int32([points]), 1, (255,255,255),3)

     

          cv2.imshow('cam',img)
          if cv2.waitKey(1) ==27:
            exit(0)
      except ThreadError:
        self.thread_cancelled = True
        
        
  def is_running(self):
    return self.thread.isAlive()
      
    
  def shut_down(self):
    self.thread_cancelled = True
    #block while waiting for thread to terminate
    while self.thread.isAlive():
      time.sleep(1)
    return True

  
    
if __name__ == "__main__":
  url = 'http://192.168.10.140:8080/video'
  cam = Cam(url)
  cam.start()
