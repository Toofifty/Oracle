"""
Oracle - Connect Script
~ Toofifty 
"""

import socket
import sys
import os
import traceback
from colorama import init, Fore
init(autoreset=True)

from base import config, log

c = config

class GameChat(object):
    """ Class to recognise whether
    the last message was from in-game
    or in-irc.
    
    Is extremely pointless, will
    get rid of very soon.
    """
    def __init__(self):
        self.active = False
        
gc = GameChat()

def getactive():
    return gc.active
    
def set_active(bot):
    gc.active = bot
    
def set_inactive():
    gc.active = False

def _send_irc(raw_msg):
    try:
        s.send(raw_msg)
        log(raw_msg, m_type="RAWMESSAGE", colour=Fore.GREEN, lg='send', l_type=2)
        return True
    except Exception:
        traceback.print_exc()
    return False
    
# Ask for NAMES
def getusers():
    return _send_irc("NAMES "
                    + config.get('channel')
                    + "\r\n")
                    
# PRIVMSG a message to the channel
def say(msg):
    return _send_irc("PRIVMSG "
                    + str(config.get('channel')) + " :" + str(msg)
                    + "\r\n")
    
# PRIVMSG to a nick or NOTICE to a server bot
def msg(msg, nick):
    if (gc.active):
        return _send_irc("PRIVMSG "
                        + gc.active + " :" + nick + " " + str(msg)
                        + "\r\n")
        
    else:
        return _send_irc("NOTICE "
                        + nick + " :" + str(msg)
                        + "\r\n")
    
# KICK
def kick(nick, reason):
    return _send_irc("KICK "
                    + config.get('channel') + nick + reason
                    + "\r\n")

# Stop the bot, probably after ?close
def stop(nick):
    log("Stop command issued by " + nick + " - closing.", m_type="CLOSE", colour=Fore.YELLOW, reset=False)
    say("\00307\x02Goodbye!\00307\x02")
    _send_irc("QUIT\r\n")
    log(nick + " terminated the session.", m_type="CLOSE", colour=Fore.YELLOW, reset=False)
    sys.exit()

# Fully restart the bot
def restart(nick):
    log("Restart command issued by " + nick + ".", m_type="RESTART", colour=Fore.YELLOW, reset=False)
    say("\00307\x02Restarting!\00307\x02")
    _send_irc("QUIT\r\n")

    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)

# IDENTIFY to NickServ
def identify():
    return _send_irc("nickserv IDENTIFY Oracle "
                    + config.get('pass')
                    + "\r\n")

# PONG to reply to PINGs
def ping(code):
    return _send_irc("PONG "
                    + code
                    + "\r\n")

# JOIN the channel
def join():
    return _send_irc("JOIN "
                    + config.get('channel')
                    + "\r\n")
    
# MODE flags
def mode(args):
    return _send_irc("MODE "
                    + config.get('channel') + " " + " ".join(args)
                    + "\r\n")
    
# Send a completely raw message
def raw(args):
    return _send_irc(" ".join(args)
                    + "\r\n")
    
# Initial connect to server and channel
def start():    
    try:
        global s
        s = socket.socket()
        s.connect((config.get('host'), config.get('port')))
        _send_irc("NICK "
                + config.get('nick')
                + "\r\n")
        _send_irc("USER "
                + config.get('ident') + " " + config.get('host')
                + " bla :" + config.get('realname')
                + "\r\n")
        return s
    except Exception:
        traceback.print_exc()
        log("Could not connect to server.", m_type="WARNING", colour=Fore.RED, reset=False)
        return False
