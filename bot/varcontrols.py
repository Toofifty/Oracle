"""
Oracle - nick variable control script
~ Toofifty 
"""

import os
import json
from pprint import pprint

def makevarfile(nick, target):
    if not(os.path.exists("../bot/users/" + target + ".json")):
        f = file("../bot/users/" + target + ".json", 'w")
        f.write("{\"spam\" : 0, \"kicks\" : 0, \"banned\" : False, \"rank\" : 0, \"ircp\" : 0 }")
        f.close()
        return True
    else:
        return False
    
def setvar(nick, target, var, val): #set specific values for users
    try:
        if not(os.path.exists("../bot/users/" + target + ".json")):
            makevarfile(target)    
        with open("../bot/users/" + target + ".json", 'r') as data_file:    
            data = json.load(data_file)
        pprint(data)
        data[var] = val
        pprint(data)
        with open("../bot/users/" + target + ".json", 'w') as out_file:
            json.dump(data, out_file)
        return True
    except:
        return False

def getvar(nick, target, var):
    try:
        if not(os.path.exists("../bot/users/" + target + ".json")):
            #whisper("Target does not have a file.", nick)
            return False
        else:
            with open("../bot/users/" + target + ".json") as data_file:    
                data = json.load(data_file)
            #pprint(data)
        print data[var]
        return data[var]
    except:
        return False