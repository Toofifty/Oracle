"""
Oracle - Connect Script
~ Toofifty 
"""

import socket
import sys
import json
import os
import spamhandler
from colorama import init, Fore, Back
init(autoreset=True)

class gamechat(object):
    def __init__(self):
        self.active = False
        
    def __active(self):
        self.active = True
        
    def __inactive(self):
        self.active = False
        
    def __get(self):
        return self.active
        
gc = gamechat()

def setactive():
    gc.active = True
    #gc.__active()
def setinactive():
    gc.active = False
    #gc.__inactive()
def getactive():
    #return gc.__get()
    return gc.active

def loadconfig():
    with open('../bot/config/config.json', 'r') as conf_file:
        c = json.load(conf_file)   
    return c

def getusers():
    c = loadconfig()
    s.send("NAMES " + c["channel"] + "\r\n")
    
def say(msg):
    s.send("PRIVMSG " + str(c["channel"]) + " :" + str(msg) + "\r\n")
    
    
def whisper(msg, nick):
    if (gc.active):
        s.send("PRIVMSG RapidIRC :" + nick + " " + str(msg) + "\r\n")
    else:
        s.send("NOTICE " + nick + " :" + str(msg) + "\r\n")
    
def kick(nick):
    c= loadconfig()
    s.send("KICK %s %s\r\n" % (c["channel"],nick))

def stop(nick):
    print "!!! - Stop command issued! Closing."
    say("\00307\x02Goodbye!\00307\x02")
    s.send("QUIT\r\n")
    sys.exit("!!! - " + nick +" terminated session.")

def restart(nick):
    print ("!!! - Restart command issued by " + nick)
    say("\00307\x02Restarting!\00307\x02")
    s.send("QUIT\r\n")

    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)

def identify():
    s.send("MSG nickserv IDENTIFY %s\r\n" % c["pass"])
    print ("identified")

def ping(id):
    s.send("PONG %s\r\n" % id)
    
def join():
    s.send("JOIN %s\r\n" % c["channel"])
    
def mode(args):
    c= loadconfig()
    s.send("MODE " + c["channel"] + " " + " ".join(args) + "\r\n")
    
def raw(args):
    s.send(" ".join(args) + "\r\n")
    
def start():
    global c
    c = loadconfig()
    try:
        global s
        s = socket.socket()
        s.connect((c["host"], c["port"]))
        s.send('NICK '+c["nick"]+'\r\n')
        s.send('USER '+c["ident"]+' '+c["host"]+' bla :'+c["realname"]+'\r\n')
        return s, c["channel"]
    except:
        print ("!!! - Error! Failed to connect to " + c["channel"] + " on " + c["host"])
        return False
        
start()