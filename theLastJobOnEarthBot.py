textFadeOutTime = 1000 #in milliseconds

import re
import thread

import aiml
import os
import serial

from bottle import route, request, run

from time import sleep

import sys

from googletrans import Translator
translator = Translator()

sys.coinit_flags = 0
#import pythoncom
import win32com.client
speak = win32com.client.Dispatch("SAPI.SpVoice")

#ser = serial.Serial('COM3', 9600)


botbrain = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    botbrain.bootstrap(brainFile = "bot_brain.brn")
else:
    #botbrain.bootstrap(learnFiles = "aiml/startup.xml")
    botbrain.bootstrap(learnFiles = "aiml/std-startup.xml", commands = "load aiml b")
    botbrain.saveBrain("bot_brain.brn")

def sayThis(text):
    #ser.write('0')#make it vibrate and start loading bar
    #speak.Speak(text)
    #ser.write('a')#stop the loading bar
    print("\n"+text+" is said\n")

@route('/bot-en')
def startpage():
    return '''
<html>
<head>
    <title>Marie's chatbot</title>
<style>
.button {
color: grey;
border: 1px solid grey;
padding: 5.5px 11px;
margin: 10px;
border-radius: 8px;
font-size: 150%;
text-decoration: none;
font-family:"Lucida Console", Monaco, monospace;;
</style>
        
</head>
<body style="background-color:#000000;overflow:hidden; }">
        <p style="
            text-align: center;z-index:1000;position:absolute;
            margin: auto;
            width: 100%;
            padding: 10px;padding-top:100px;">
            <a href='http://localhost:8080/bot-en' class='button' style='text-decoration: underline'>EN</a><a href='http://localhost:8080/bot-it' class='button'>IT</a>
            </p>
    <form action="/bot-en" method="post" id="masterform">
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

@route('/bot-en', method='POST')
def do_bot():
    
    say = request.forms.get('say')
    say =re.sub(r'[^\w\s\\?\\!\\,\\.]','',say)
    print("input:    "+ say )
    response = botbrain.respond(say)
    response =re.sub(r'[^\w\s\\?\\!\\,\\.]','',response)
    #speak.Speak(response)
    thread.start_new_thread(sayThis,(response,))
    sleep(textFadeOutTime/1000.)
    
    print("response: " + response ) 
  
    return '''
        <html>
        <head>
        
        <title>Marie's chatbot</title>

<style>
.button {
color: grey;
border: 1px solid grey;
padding: 5.5px 11px;
margin: 10px;
border-radius: 8px;
font-size: 150%;
text-decoration: none;
font-family:"Lucida Console", Monaco, monospace;;
</style>
        
        </head>
        <body style="background-color:#000000;overflow:hidden;">
                <p style="
            text-align: center;z-index:1000;position:absolute;
            margin: auto;
            width: 100%;
            padding: 10px;padding-top:100px;">
            <a href='http://localhost:8080/bot-en' class='button'  style='text-decoration: underline'>EN</a><a href='http://localhost:8080/bot-it' class='button'>IT</a>
            </p>
        <form action="/bot-en" method="post" id="masterform">
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
            speechSynthesis.cancel()
            var msg = new SpeechSynthesisUtterance();
            msg.lang = 'en-EN';
            //msg.rate = 0.80;
            msg.text = "'''+response+'''";
            var t;
            msg.onstart = function (event) {
                t = event.timeStamp;
                console.log('started talking at '+t);
            };

            msg.onend = function (event) {
                t = event.timeStamp - t;
                console.log(event.timeStamp);
                console.log('finished talking at '+(t / 1000) + " seconds");
            };

            speechSynthesis.speak(msg);



    
  
    
$("#masterform").submit(function(e) {
  $("#inputbox").fadeOut('''+str(textFadeOutTime)+''');
});
</script>
</body>
</html>
        
    '''
@route('/bot-it')
def startpage():
    return '''
<html>
<head>
    <title>Marie's chatbot</title>
<style>
.button {
color: grey;
border: 1px solid grey;
padding: 5.5px 11px;
margin: 10px;
border-radius: 8px;
font-size: 150%;
text-decoration: none;
font-family:"Lucida Console", Monaco, monospace;;
</style>
        
</head>
<body style="background-color:#000000;overflow:hidden; }">
        <p style="
            text-align: center;z-index:1000;position:absolute;
            margin: auto;
            width: 100%;
            padding: 10px;padding-top:100px;">
            <a href='http://localhost:8080/bot-en' class='button'>EN</a><a href='http://localhost:8080/bot-it' class='button'  style='text-decoration: underline'>IT</a>
            </p>
    <form action="/bot-it" method="post" id="masterform">
        <input name="say" type="text" id="inputbox" autofocus autocomplete="off" placeholder="scrivi al bot qui" style="
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

@route('/bot-it', method='POST')
def do_bot():
    
    say = request.forms.get('say')
    say =re.sub(r'[^\w\s\\?\\!\\,\\.]','',say)
    print("input:    "+ say )
    saytranslated = translator.translate(say, dest='en').text
    print("input english:    "+ saytranslated )
    responsedry = botbrain.respond(saytranslated)
    print("response english:    "+ responsedry )
    response = translator.translate(responsedry, dest='it').text
    response =re.sub(r'[^\w\s\\?\\!\\,\\.]','',response)
    #speak.Speak(response)
    thread.start_new_thread(sayThis,(response,))
    sleep(textFadeOutTime/1000.)
    
    print("response: " + response ) 
  
    return '''
        <html>
        <head>
        
        <title>Marie's chatbot</title>

<style>
.button {
color: grey;
border: 1px solid grey;
padding: 5.5px 11px;
margin: 10px;
border-radius: 8px;
font-size: 150%;
text-decoration: none;
font-family:"Lucida Console", Monaco, monospace;;
</style>
        
        </head>
        <body style="background-color:#000000;overflow:hidden;">
                <p style="
            text-align: center;z-index:1000;position:absolute;
            margin: auto;
            width: 100%;
            padding: 10px;padding-top:100px;">
            <a href='http://localhost:8080/bot-en' class='button'>EN</a><a href='http://localhost:8080/bot-it' class='button'  style='text-decoration: underline'>IT</a>
            </p>
        <form action="/bot-it" method="post" id="masterform">
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
            speechSynthesis.cancel()
            var msg = new SpeechSynthesisUtterance();
            msg.lang = 'it-IT';
            //msg.rate = 0.80;
            msg.text = "'''+response+'''";
            var t;
            msg.onstart = function (event) {
                t = event.timeStamp;
                console.log('started talking at '+t);
            };

            msg.onend = function (event) {
                t = event.timeStamp - t;
                console.log(event.timeStamp);
                console.log('finished talking at '+(t / 1000) + " seconds");
            };

            speechSynthesis.speak(msg);



    
  
    
$("#masterform").submit(function(e) {
  $("#inputbox").fadeOut('''+str(textFadeOutTime)+''');
});
</script>
</body>
</html>
        
    '''
    
run(host='0.0.0.0', port=8080)
