"""
Oracle - Connect Script
~ Toofifty 
"""

import socket
import sys
import os
import traceback

from base import config, ACTION_LOG, SEND_LOG

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
        SEND_LOG.debug(raw_msg)
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
    ACTION_LOG.info("!!! - Stop command issued! Closing.")
    say("\00307\x02Goodbye!\00307\x02")
    _send_irc("QUIT\r\n")
    ACTION_LOG.info("!!! - " + nick +" terminated session.")
    sys.exit()

# Fully restart the bot
def restart(nick):
    ACTION_LOG.info("!!! - Restart command issued by " + nick)
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
        ACTION_LOG.warning("!!! - Error! Failed to connect to "
            + config.get('channel') + " on " + config.get('host'))
        return False
