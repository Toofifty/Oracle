"""
Oracle - Spam Handler
~ Toofifty 
"""

import json
import sys
import connect
import threading
import time

flood={}
global active
active=False

class timeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        c = loadconfig()
        flood={}
        while 1:
            print flood
            flood={}
            time.sleep(c["interval"])

def loadconfig():
    with open('..\\bot\config\spam.json', 'r') as conf_file:
        c = json.load(conf_file)   
    return c

def handler(nick):
    if(nick) and not "esper.net" in nick:
        if flood.has_key(nick):
            c = loadconfig()
            flood[nick] += 1
            if flood[nick] > c["kick"]:
                connect.kick(nick)
                print ("KIC - User: " + nick + " was kicked for spamming")
        else:
            timeThread().start()
            flood[nick] = 1
    