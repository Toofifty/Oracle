"""
Oracle - Connect Script
~ Toofifty 
"""

import socket
import sys
import json

def loadconfig():
    with open('..\\bot\config\config.json', 'r') as conf_file:
        c = json.load(conf_file)   
    return c
    
def start():
    c = loadconfig()
    try:
        global s
        s = socket.socket()
        s.connect((c["host"], c["port"]))
        s.send('NICK '+c["nick"]+'\r\n')
        s.send('USER '+c["ident"]+' '+c["host"]+' bla :'+c["realname"]+'\r\n')
        s.send('JOIN '+c["channel"]+'\r\n')
        return s, c["channel"], c["pass"]
    except:
        print ("!!! - Error! Failed to connect to " + c["channel"] + " on " + c["host"])
        return False
        
start()
  
def raw_send(msg):
    if(s.send(msg)):
        return True
    else:
        return False

def say(msg):
    s.send("PRIVMSG " + str(chan) + " :" + str(msg) + "\r\n")
    
def kick(nick):
    c= loadconfig()
    s.send("KICK %s %s\r\n" % (c["channel"],nick))