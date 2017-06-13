import time
import threading

bar = False

def foo():
    global bar
    while True:
        if bar == True:
            print "Success!"
        else:
            print "Not yet!"
    time.sleep(1)

def example():
    global bar
    while True:
        time.sleep(5)
        bar = True

t1 = threading.Thread(target=foo)


t2 = threading.Thread(target=example)

t1.start()
t2.start()
