'''
Oracle - Spam Handler
~ Toofifty 
'''

import json
import sys
import connect
import threading
import time
import os
from colorama import init, Fore, Back
init(autoreset=True)

global flood
flood={}
global active
active = False
global last_msg
last_msg = ''

class timeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        c = loadconfig()
        global active
        active = True
        while 1:
            flood_('reset','null')
            time.sleep(c['interval'])

def loadconfig():
    with open('../bot/config/spam.json', 'r') as conf_file:
        c = json.load(conf_file)   
    return c
    
def flood_(type, nick):
    global flood
    
    if not 'flood' in globals():
        flood = {}
    elif type == 'add':
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
        if not flood == {}:
            print flood
        flood = {}
        return True
    print flood
    
def handler(nick,msg):
    global last_msg
    if(nick) and not 'esper.net' in nick:
        if flood_('check',nick):
            c = loadconfig()
            r = flood_('add',nick)
            if (msg == last_msg):
                r = flood_('add',nick)
                print (nick + ' repeated a message.')
            if r > c['kick']:
                connect.kick(nick)
                connect.say('\x0308User \x0304' + nick + ' \x0308was kicked for spamming.')
                print (Fore.RED + 'KCK' + Fore.RESET + ' - User: ' + nick + ' was kicked for spamming')
            elif r > c['warn']:
                connect.whisper('\x0308Please slow down with your messages, or else you'll be kicked.\x0308',nick)
        else:
            global active
            if not active:
                timeThread().start()
            flood_('new',nick)
    last_msg = msg