import aiml
import os


from bottle import route, request, run

kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    #kernel.bootstrap(learnFiles = "aiml/startup.xml", commands = "load aiml b")
    kernel.bootstrap(learnFiles = "aiml/std-startup.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")

def replaceChar(string):
    stringList = list(string)
    for i, c in enumerate(stringList):
        if stringList[i]=='"':
            stringList[i]= ''
    result = ''.join(stringList)
    return result
    
    
#    for char in string:
#        print(char)
#        if searchExp in char:
#            char = char.replace(searchExp,replaceExp)
#        newstring += char
#    return newstring



@route('/bot')
def login():
    return '''
        <body style="background-color:#000000;">
        <form action="/bot" method="post">
        <input name="say" type="text" autofocus autocomplete="off" placeholder="write to the bot here" style="
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
        </body>
    '''

@route('/bot', method='POST')
def do_bot():
    
    say = request.forms.get('say')
    print("input:    "+ say )
    response = kernel.respond(say)
    print("response: " + response ) 
    response = replaceChar(response) #without this, sentances with " will not be said for some reason
  
    return '''
        <script>
            var msg = new SpeechSynthesisUtterance();
            msg.rate = 0.80;
            //msg.text = "testing.";
            msg.text = "'''+response+'''";
            window.speechSynthesis.speak(msg);
            //window.speechSynthesis.speak('Hello, I'm talking.');
        </script>
        <head>
        <title>Marie's chatbot</title>
        </head>
        <body style="background-color:#000000;">
        <form action="/bot" method="post">
        <input name="say" type="text" autofocus  autocomplete="off" style="
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
        
    '''
    
run(host='0.0.0.0', port=8080)
