import cv2
import random
import numpy as np

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        #ret_val, img = cam.read()
        img = np.zeros((1024,1280,3), np.uint8)
        if mirror: 
            img = cv2.flip(img, 1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        value = random.random()
        cv2.putText(img,str(value),(10,30), font, 1,(255,255,255),2)
        cv2.line(img,(0,0),(1000,1000),(255,0,0),5)
        
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("window", img)
        
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()

def main():
	show_webcam(mirror=True)

if __name__ == '__main__':
	main()
