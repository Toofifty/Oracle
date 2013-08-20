"""
Oracle - Connect Script
~ Toofifty 
"""

import socket
import sys
import json

def loadconfig():
    with open('..\irc\config\config.json', 'r') as conf_file:
        c = json.load(conf_file)   
    return c

def getsocket():
    s = socket.socket()
    return s

def start():
    c = loadconfig()
    try:
        s = socket.socket()
        s.connect((c["host"], c["port"]))
        s.send('NICK '+c["nick"]+'\r\n')
        s.send('USER '+c["ident"]+' '+c["host"]+' bla :'+c["realname"]+'\r\n')
        s.send('JOIN '+c["channel"]+'\r\n')
        return s, c["channel"], c["pass"]
    except:
        print ("!!! - Error! Failed to connect to " + c["channel"] + " on " + c["host"])
        return False
        
