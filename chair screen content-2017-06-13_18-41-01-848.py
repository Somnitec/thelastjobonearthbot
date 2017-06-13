import cv2
import numpy as np
import random

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

linethickness = 5

#img is 516x720
def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    cam.set(3,1280)
    cam.set(4,720)
    while True:
      
        ret_val, image = cam.read()

      
        
        crop = image[0:720,382:382+516] # full size
        crop = cv2.flip(crop, 1)#flip image
        height, width, channels = crop.shape

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            crop = cv2.ellipse(crop,(x,y),(x+w,y+h)),0,0,360,(255,255,255),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = crop[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,255),2)
            smile = smile_cascade.detectMultiScale(roi_gray)
            points = []
            for (ex,ey,ew,eh) in smile:
                #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,255),2)
                points.append([ex+ew/2,ey+eh/2])
            cv2.polylines(roi_color, np.int32([points]), 1, (255,255,255),3)

            
                

        #points = [[100, 100], [100, 200], [123, 48], [58, 45]]
        #points.dtype => 'int64'
        #cv2.polylines(crop, np.int32([points]), 1, (255,255,255))
        
        font = cv2.FONT_HERSHEY_SIMPLEX

        for i in range(0, 30):
            cv2.putText(crop,str(random.random()),((4*width/6)+10,30+(i*20)), font, 0.5,(255,255,255),1)
        
        cv2.rectangle(crop,(0,0),(width,height),(255,255,255),linethickness)
        cv2.rectangle(crop,((4*width/6),0),(width,(6*height)/7),(255,255,255),linethickness)
        cv2.rectangle(crop,(0,(6*height)/7),(width,height),(0,0,0),-1)
        cv2.rectangle(crop,(0,(6*height)/7),(width,height),(255,255,255),linethickness)

        
        

        cv2.namedWindow("Result", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Result",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        
        cv2.imshow('Result', crop)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()


def main():
	show_webcam(mirror=True)

if __name__ == '__main__':
	main()
