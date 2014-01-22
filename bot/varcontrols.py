'''
Oracle - nick variable control script
~ Toofifty 
'''

import os
import json
from pprint import pprint

def makevarfile(nick, target):
    if not(os.path.exists('../bot/users/' + target + '.json')):
        f = file('../bot/users/' + target + '.json', 'w')
        f.write('{\"spam\": 0, \"kicks\": 0, \"banned\": false, \"rank\": 1, \"ircp\": 0}')
        f.close()
        return True
    else:
        return False
    
def setvar(nick, target, var, val): #set specific values for users
    try:
        if not(os.path.exists('../bot/users/' + target + '.json')):
            makevarfile(target)    
        with open('../bot/users/' + target + '.json', 'r') as data_file:    
            data = json.load(data_file)
        data[var] = val
        with open('../bot/users/' + target + '.json', 'w') as out_file:
            json.dump(data, out_file)
        return True
    except:
        return False

def getvar(nick, target, var):
    try:
        if not(os.path.exists('../bot/users/' + target + '.json')):
            makevarfile(nick, target)
            getvar(nick, target, var)
        else:
            with open('../bot/users/' + target + '.json') as data_file:    
                data = json.load(data_file)
        return data[var]
    except:
        return False
        
def deletevarfile(nick, target):
    if os.path.exists('../bot/users/' + target + '.json'):
        os.remove('../bot/users/' + target + '.json')
        return True
    else:
        return False
        
def getrank(nick):
    if os.path.exists('../bot/users/' + nick + '.json'):
        with open('../bot/users/' + nick + '.json') as data_file:    
            data = json.load(data_file)
        return data["rank"]
    else:
        return 0