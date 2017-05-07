import aiml
import os


from bottle import route, request, run

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")

botbrain = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    botbrain.bootstrap(brainFile = "bot_brain.brn")
else:
    #botbrain.bootstrap(learnFiles = "aiml/startup.xml", commands = "load aiml b")
    botbrain.bootstrap(learnFiles = "aiml/std-startup.xml", commands = "load aiml b")
    botbrain.saveBrain("bot_brain.brn")

def replaceChar(string):
    stringList = list(string)
    for i, c in enumerate(stringList):
        if stringList[i]=='"':
            stringList[i]= ''
    result = ''.join(stringList)
    return result

@route('/bot')
def login():
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
            height: 100%;
            width: 100%;
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
  $("#inputbox").fadeOut("fast");
});
</script>

</body>
</html>
    '''

@route('/bot', method='POST')
def do_bot():
    
    say = request.forms.get('say')
    print("input:    "+ say )
    response = botbrain.respond(say)
    speak.Speak(response)
    print("response: " + response ) 
    #response = replaceChar(response) #without this, sentances with " will not be said for some reason
  
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
            height: 100%;
            width: 100%;
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
  $("#inputbox").fadeOut("fast");
});
</script>
</body>
</html>
        
    '''
    
run(host='0.0.0.0', port=8080)
