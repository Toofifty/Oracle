"""
Oracle - User variable control script
~ Toofifty 
"""

import os
import json
from pprint import pprint

def makevarfile(user, target):
    if not(os.path.exists("..\irc\users\\" + target + ".json")):
        f = file("..\irc\users\\" + target + ".json", "w")
        f.write("{\"spam\" : 0, \"kicks\" : 0, \"banned\" : False, \"rank\" : 0, \"ircp\" : 0 }")
        f.close()
        return True
    else:
        return False
    
def setvar(user, target, var, val): #set specific values for users
    try:
        if not(os.path.exists("..\irc\users\\" + target + ".json")):
            makevarfile(target)    
        with open('..\irc\users\\' + target + '.json', 'r') as data_file:    
            data = json.load(data_file)
        pprint(data)
        data[var] = val
        pprint(data)
        with open('..\irc\users\\' + target + '.json', 'w') as out_file:
            json.dump(data, out_file)
        return True
    except:
        return False

def getvar(user, target, var):
    try:
        if not(os.path.exists("..\irc\users\\" + target + ".json")):
            #whisper("Target does not have a file.", user)
            return False
        else:
            with open('..\irc\users\\' + target + '.json') as data_file:    
                data = json.load(data_file)
            #pprint(data)
        print data[var]
        return data[var]
    except:
        return False
        