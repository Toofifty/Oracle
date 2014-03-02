"""
Oracle - Connect Script
~ Toofifty 
"""

import socket
import sys
import json
import os
import spamhandler
import yaml
import logging
import traceback
from base import *

c = config

class gamechat(object):
    def __init__(self):
        self.active = False
        
gc = gamechat()

def getactive():
    return gc.active
    
def set_active(bot):
    gc.active = bot
    
def set_inactive():
    gc.active = False

def getusers():
    s.send("NAMES " + config.get('channel') + "\r\n")
    send_log.debug("NAMES " + config.get('channel') + "\r\n")
    
def say(msg):
    s.send("PRIVMSG " + str(config.get('channel')) + " :" + str(msg) + "\r\n")
    send_log.debug("PRIVMSG " + str(config.get('channel')) + " :" + str(msg))
    
    
def whisper(msg, nick):
    if not (gc.active):
        s.send("NOTICE " + nick + " :" + str(msg) + "\r\n")
        send_log.debug("NOTICE " + nick + " :" + str(msg))
    else:
        s.send("PRIVMSG " + gc.active + " :" + nick + " " + str(msg) + "\r\n")
        send_log.debug("PRIVMSG " + gc.active + " :" + nick + " " + str(msg))
    
def kick(nick, reason):
    s.send("KICK %s %s %s\r\n" % (config.get('channel'),nick, reason))
    send_log.debug("KICK %s %s %s\r\n" % (config.get('channel'),nick, reason))

def stop(nick):
    action_log.info("!!! - Stop command issued! Closing.")
    say("\00307\x02Goodbye!\00307\x02")
    s.send("QUIT\r\n")
    send_log.debug("QUIT\r\n")
    action_log.info("!!! - " + nick +" terminated session.")
    sys.exit()

def restart(nick):
    action_log.info("!!! - Restart command issued by " + nick)
    say("\00307\x02Restarting!\00307\x02")
    s.send("QUIT\r\n")
    send_log.debug("QUIT\r\n")

    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)

def identify():
    s.send("nickserv IDENTIFY Oracle %s\r\n" % config.get('pass'))
    send_log.debug("nickserv IDENTIFY Oracle %s" % config.get('pass'))

def ping(i):
    s.send("PONG %s\r\n" % i)
    send_log.debug("PONG %s\r\n" % i)
    
def join():
    s.send("JOIN %s\r\n" % config.get('channel'))
    send_log.debug("JOIN %s" % config.get('channel'))
    
def mode(args):
    s.send("MODE " + config.get('channel') + " " + " ".join(args) + "\r\n")
    send_log.debug("MODE " + config.get('channel') + " " + " ".join(args))
    
def raw(args):
    s.send(" ".join(args) + "\r\n")
    send_log.debug(" ".join(args))
    
def start():    
    try:
        global s
        s = socket.socket()
        s.connect((config.get('host'), config.get('port')))
        s.send('NICK '+config.get('nick')+'\r\n')
        s.send('USER '+config.get('ident')+' '+config.get('host')+' bla :'+config.get('realname')+'\r\n')
        return s, c
    except:
        traceback.print_exc()
        action_log.warning("!!! - Error! Failed to connect to " + config.get('channel') + " on " + config.get('host'))
        return False
        
start()