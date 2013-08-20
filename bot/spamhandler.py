"""
Oracle - Spam Handler
~ Toofifty 
"""

import json
import sys
import connect

users={}

def loadconfig():
    with open('..\irc\config\spam.json', 'r') as conf_file:
        c = json.load(conf_file)   
    return c

def add_points(user, i):
    try:
        users[user] = users[user] + i
    except:
        users[user] = i

def get_points(user):
    try:
        return users[user]
    except:
        return 0

def start(user):
    s = connect.getsocket()
    c = loadconfig()
    add_points(user, c["interval"])
    if(get_points(user) >= c["kick"] * c["interval"]):
        s.send("KICK %s" % user)
        print ("KIC - User %s was kicked for spamming." % user)        
