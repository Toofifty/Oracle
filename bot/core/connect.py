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
send_log = logging.getLogger('send')
action_log = logging.getLogger('action')

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

def loadconfig():
    with open('../bot/config.yml', 'r') as conf_file:
        c = yaml.load(conf_file)
    action_log.debug("!!! - Config loaded")
    return c

def getusers():
    c = loadconfig()
    s.send("NAMES " + c['channel'] + "\r\n")
    send_log.debug("NAMES " + c['channel'] + "\r\n")
    
def say(msg):
    s.send("PRIVMSG " + str(c['channel']) + " :" + str(msg) + "\r\n")
    send_log.debug("PRIVMSG " + str(c['channel']) + " :" + str(msg))
    
    
def whisper(msg, nick):
    if not (gc.active):
        s.send("NOTICE " + nick + " :" + str(msg) + "\r\n")
        send_log.debug("NOTICE " + nick + " :" + str(msg))
    else:
        s.send("PRIVMSG " + gc.active + " :" + nick + " " + str(msg) + "\r\n")
        send_log.debug("PRIVMSG " + gc.active + " :" + nick + " " + str(msg))
    
def kick(nick, reason):
    c= loadconfig()
    s.send("KICK %s %s %s\r\n" % (c['channel'],nick, reason))
    send_log.debug("KICK %s %s %s\r\n" % (c['channel'],nick, reason))

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
    s.send("nickserv IDENTIFY Oracle %s\r\n" % c['pass'])
    send_log.debug("nickserv IDENTIFY Oracle %s" % c['pass'])

def ping(i):
    s.send("PONG %s\r\n" % i)
    send_log.debug("PONG %s\r\n" % i)
    
def join():
    s.send("JOIN %s\r\n" % c['channel'])
    send_log.debug("JOIN %s" % c['channel'])
    
def mode(args):
    c= loadconfig()
    s.send("MODE " + c['channel'] + " " + " ".join(args) + "\r\n")
    send_log.debug("MODE " + c['channel'] + " " + " ".join(args))
    
def raw(args):
    s.send(" ".join(args) + "\r\n")
    send_log.debug(" ".join(args))
    
def start():
    global c
    c = loadconfig()
    
    try:
        global s
        s = socket.socket()
        s.connect((c["host"], c['port']))
        s.send('NICK '+c['nick']+'\r\n')
        s.send('USER '+c['ident']+' '+c['host']+' bla :'+c['realname']+'\r\n')
        return s, c
    except:
        action_log.warning("!!! - Error! Failed to connect to " + c['channel'] + " on " + c['host'])
        return False
        
start()