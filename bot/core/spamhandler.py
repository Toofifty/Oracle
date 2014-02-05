'''
Oracle - Spam Handler
~ Toofifty 
'''

import yaml
import sys
import threading
import time
import os
import logging
from colorama import init, Fore, Back
init(autoreset=True)

import format
import connect

global last_msg

f = format.formats()
flood = {}
active = False
last_msg = ''
action_log = logging.getLogger('action')

"""
Creates a parallel time thread which resets the flood every [interval]
"""
class timeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        c = loadconfig()
        global active
        active = True
        while 1:
            flood_('reset', 'null')
            time.sleep(c['interval'])

"""
Load config from config.yml as c
"""
def loadconfig():
    with open('../bot/config.yml', 'r') as conf_file:
        c = yaml.load(conf_file)
    return c
    
"""
Grab / change user 'flood' values
"""
def flood_(type, nick):
    global flood
    
    if type == 'add':
        flood[nick] += 1
        return flood[nick]
        
    elif type == 'new':
        flood[nick] = 2
        return flood[nick]
        
    elif type == 'check':
        if flood.has_key(nick):
            return True
        else:
            return False
            
    else:
        flood = {}
        return True
    print flood
    
"""
Handler determines what users will be added to flood, and kicks if over certain amounts
"""    
def handler(nick, msg):
    global last_msg
    c = loadconfig()
    
    if nick and not 'esper.net' in nick:
        if flood_('check', nick):
            r = flood_('add',nick)
            
            if (msg == last_msg):
                r = flood_('add', nick)
                action_log.info(Fore.RED + 'SPM' + Fore.RESET + ' - ' + nick + ' repeated a message.')
                
            if r > c['kick']:
                connect.kick(nick, "lol")
                connect.say(f.YELLOW + 'User ' + f.RED + nick + f.YELLOW + ' was kicked for spamming.')
                action_log.info(Fore.RED + 'KCK' + Fore.RESET + ' - User: ' + nick + ' was kicked for spamming')
                
            elif r > c['warn']:
                connect.whisper(f.YELLOW + 'Please slow down with your messages, or else you\'ll be kicked.',nick)
                
        else:
            if not active:
                timeThread().start()
            flood_('new', nick)
            
    last_msg = msg
    