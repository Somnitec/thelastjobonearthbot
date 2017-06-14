import os
from threading import Thread
from time import sleep
from timeit import default_timer as timer
import thread
import cv2
import urllib
import numpy as np
import random
from bottle import route, request, run,template
import aiml
import serial
import sys
sys.coinit_flags = 0
import pythoncom
import win32com.client

####screenstuff
minframerate = 10#fps

screenwidth=1024
screenheight=1280
stream=urllib.urlopen('http://172.21.101.198:8080/video')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

###

####botstuff
textFadeOutTime = 1000 #in milliseconds
ser = serial.Serial('COM5', 9600)


speak = win32com.client.Dispatch("SAPI.SpVoice")



say=''

botbrain = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    botbrain.bootstrap(brainFile = "bot_brain.brn")
else:
    #botbrain.bootstrap(learnFiles = "aiml/startup.xml", commands = "load aiml b")
    botbrain.bootstrap(learnFiles = "aiml/std-startup.xml", commands = "load aiml b")
    botbrain.saveBrain("bot_brain.brn")

            

def sayThis(text):
    global say
    ser.write('0')#make it vibrate and start loading bar
    speak.Speak(text)
    #say=''
    ser.write('a')#stop the loading bar
###

def screenthings():
    lasttime=timer()
    bytes=''
    while True:
        #print 'A\n'
        urllib.urlcleanup()
        bytes+=stream.read(16384)
        
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')        


        
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            
            

            #stream.flush()
            #currenttime=timer()
            #print currenttime-lasttime, 1./minframerate
            #if currenttime-lasttime > 1./minframerate:
                #continue
                #print 'skipping'
            #lasttime=currenttime
            
            rawcam = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            cam=cv2.flip(rawcam,1)
            height, width, channels = cam.shape
        
            desiredwidth=int(float(screenwidth)/screenheight*height)
            startpoint=int((width-desiredwidth)/2)

            crop=cam[0:height,startpoint:startpoint+desiredwidth]
            img=cv2.resize(crop,(screenwidth,screenheight))

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

            #for i in range(0, 30):
                #cv2.putText(img,str(random.random()),((4*screenwidth/6)+10,30+(i*35)), font, 1,(255,255,255),1)
            
            cv2.rectangle(img,(0,0),(screenwidth,screenheight),(255,255,255),6)
            #cv2.rectangle(img,((4*screenwidth/6),0),(screenwidth,(6*screenheight)/7),(255,255,255),6)
            cv2.rectangle(img,(0,(6*screenheight)/7),(screenwidth,screenheight),(0, 0, 0),-1)
            cv2.rectangle(img,(0,(6*screenheight)/7),(screenwidth,screenheight),(255,255,255),6)

            cv2.putText(img,'the human expert is finding a response to:',(40,screenheight-120),font,0.5,(255, 231, 179))
            cv2.putText(img,say,(40,screenheight-80),font,1,(0,0,0))
            
            #cv2.putText(img,say,(10,100),font,1,(255,255,255))
            

            cv2.namedWindow("output", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("output",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

            cv2.imshow('output',img)
        
        if cv2.waitKey(1) ==27:
            break
    cv2.destroyAllWindows()



def botthings():
    
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)    
    
    while True:
        print 'B\n'

@route('/bot')
def startpage():
    return '''
<html>
<head>
    <title>Marie's chatbot</title>
</head>
<body style="background-color:#000000;overflow:hidden;">
    <form action="/bot" method="post" id="masterform">
        <input name="say" type="text" id="inputbox" autofocus autocomplete="off" placeholder="write to the bot here" style="
            color:white;
            background-color:#000000;
            padding-left:5%;
            height: 95%;
            width: 95%;
            position:absolute;
            border: none;
            border-color: transparent;
            outline:none;
            font-size: 500%;
            ">            
        </form>
        
    <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script>

    <script>
    
$("#masterform").submit(function(e) {
  $("#inputbox").fadeOut('''+str(textFadeOutTime)+''');
});
</script>

</body>
</html>
    '''

@route('/bot', method='POST')
def do_bot():
    global say
    
    say = request.forms.get('say')
    
    #sharedvariables.myList.insert(0,say)
    print("input:    "+ say )
    response = botbrain.respond(say)
    #speak.Speak(response)
    thread.start_new_thread(sayThis,(response,))
    sleep(textFadeOutTime/1000.)
    
    print("response: " + response ) 
  
    return '''
        <html>
        <head>
        <title>Marie's chatbot</title>
        </head>
        <body style="background-color:#000000;overflow:hidden;">
        <form action="/bot" method="post" id="masterform">
        <input name="say" type="text" id="inputbox" autofocus  autocomplete="off" style="
            color:white;
            background-color:#000000;
            padding-left:5%;
            height: 95%;
            width: 95%;
            position:absolute;
            border: none;
            border-color: transparent;
            outline:none;
            font-size: 500%;
            ">
        </form>
<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script>

    <script>
$("#masterform").submit(function(e) {
  $("#inputbox").fadeOut('''+str(textFadeOutTime)+''');
});
</script>
</body>
</html>
        
    '''


if __name__ == "__main__":
    
    t1 = Thread(target = botthings)
    t2 = Thread(target = screenthings)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    
    
    while True:
        pass
