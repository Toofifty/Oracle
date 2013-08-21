# -*- coding: utf-8 -*-

"""
                    ~ ?Oracle Bot v0.1 ~ #
written by Toofifty, primarily for use of the Rapidcraft Minecraft Server IRC
http://rapidcraftmc.com/
http://www.reddit.com/r/rapidcraft/
#rapidcraft on irc.esper.net
"""

from xml.dom import minidom
import sys
import string
import os
import urllib
from datetime import datetime
import time
import calendar

import connect
import youtube
import cleverbot
import varcontrols
import spamhandler

readbuffer=''
last_user=0

def say(msg):
    s.send("PRIVMSG " + str(CHANNELINIT) + " :" + str(msg) + "\r\n")

def whisper(msg, user):
    s.send("NOTICE " + user + " :" + str(msg) + "\r\n")

def stop(user):
    print "!!! - Stop command issued! Closing."
    say("Goodbye!")
    s.send("QUIT\r\n")
    sys.exit("!!! - " + user +" terminated session.")

def restart(user):
    print ("!!! - Restart command issued by " + user)
    say("Restarting!")
    s.send("QUIT\r\n")

    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def events(user):
    xmldoc = minidom.parse(urllib.urlopen('http://rapidcraftmc.com/api.php?events'))
    dname = xmldoc.getElementsByTagName('name')[0]
    dtime = xmldoc.getElementsByTagName('timestamp')[0]
    u_time = getText(dtime.childNodes)
    p_name = getText(dname.childNodes)
    #print u_time
    say("Event: " + p_name + " || Time: " + str(time.ctime(int(u_time))) + " UTC")

def timenow(user): #
    d = datetime.utcnow()
    say(str(time.ctime(calendar.timegm(d.utctimetuple()))) + " UTC")

def helpc(user, args): #whisper command help to user
    if(len(args) < 1):
        whisper("~ Welcome to the Oracle guide! Commands are categorised for neatness. Use ?help [category] to list those commands. ~",user)
        whisper("Categories: Emotes - Server - Personal - Other - Admin", user)        
    elif(args.lower() == "emotes"):
        whisper("~ Emotes ~", user)
        whisper("- ?fliptable > (╯°□°)╯︵ ┻━┻ ", user)
        whisper("- ?puttableback > ┬─┬﻿ ノ( ゜-゜ノ)", user)
        whisper("- ?ohyou > ¯_(ツ)_/¯", user)
        whisper("- ?fff > ლ(ಠ益ಠლ)", user)
        whisper("- ?disapprove > ಠ_ಠ", user)
        whisper("- ?crie > ಥ_ಥ", user)
        whisper("- ?lenny > ( ͡° ͜ʖ ͡°)", user)
    elif(args.lower() == "server"):
        whisper("~ Server ~", user)
        whisper("- ?events > Next upcoming event", user)
        whisper("- ?utc > Time now, in UTC", user)
    elif(args.lower() == "personal"):
        whisper("~ Personal ~", user)
        whisper("- Nothing here yet! Here will be messages, reports, etc.", user)
    elif(args.lower() == "other"):
        whisper("~ Other ~", user)
        whisper("- Nothing here yet! Here will be games, youtube linking, etc", user)
    elif(args.lower() == "admin") and (user == "Toofifty" or user == "Manyman" or user == "Huppatz"):
        whisper("~ Admin ~", user)
        whisper("- ?close > Turn off the Oracle bot", user)
        whisper("- ?reload > Restart the bot, to reload settings or code", user)
    else:
        whisper("~ Welcome to the Oracle guide! Commands are categorised for neatness. Use ?help [category] to list those commands. ~",user)
        whisper("Categories: Emotes - Server - Personal - Other - Admin", user) 

def cb(ask, user):
    cbot = cleverbot.Session()
    response = cbot.Ask(ask)
    say(response)
            
def parsecmd(user, msg): #command listing
    cmd = msg.split(" ")
    args = msg.split(" ",1)
    print ("CMD - " + msg + " | User: " + user)
    try:
        if cmd[0] == "?fliptable":
            say("(╯°□°)╯︵ ┻━┻")
        elif cmd[0] == "?puttableback":
            say("┬─┬﻿ ノ( ゜-゜ノ)")
        elif cmd[0] == "?help":
            if(len(cmd) < 2):
                helpc(user, "no")
            else:
                helpc(user, cmd[1])
        elif cmd[0] == "?close" and (user == "Toofifty" or user == "Manyman" or user == "Huppatz"):
            stop(user)
        elif cmd[0] == "?reload" and (user == "Toofifty" or user == "Manyman" or user == "Huppatz"):
            restart(user)
        elif cmd[0] == "?events":
            events(user)
        elif cmd[0] == "?utc":
            timenow(user)
        elif cmd[0] == "?ohyou":
            say("¯_(ツ)_/¯")
        elif cmd[0] == "?FLIPTABLE":
            say("(ノಠ益ಠ)ノ彡┻━┻")
        elif cmd[0] == "?fff":
            say("ლ(ಠ益ಠლ)")
        elif cmd[0] == "?disapprove":
            say("ಠ_ಠ")
        elif cmd[0] == "?crie":
            say("ಥ_ಥ")
        elif cmd[0] == "?lenny":
            say("( ͡° ͜ʖ ͡°)")
            
        elif cmd[0] == "?makevar":
            target = cmd[1]
            if(varcontrols.makevarfile(user, target)):
                print ("!!! - New var file created for " + target + " by " + user)
                whisper("VAR file successfully created for " + target, user)
            else:
                print ("!!! - Var file creation failed - " + user)
                whisper("VAR file failed to create for " + target, user)
                
        elif cmd[0] == "?getvar":
            response = varcontrols.getvar(user, cmd[1], cmd[2])
            whisper("VAR: %s = %s" % (response, cmd[2]),user)
            
        elif cmd[0] == "?setvar":
            if(varcontrols.setvar(user, cmd[1], cmd[2], cmd[3])):
                whisper("VAR: %s set to %s for %s" % (cmd[1], cmd[2], cmd[3]), user)
            else:
                whisper("Setting of variable failed.")
            
        elif cmd[0] == "?cb":
            cb(args[1], user)
            
        elif cmd[0] == "?attention":
            attention(user)
            
        elif cmd[0] == "?repeat":
            say(str(args[1]))
            
        else:
            whisper("Unknown command.", user)
        print "CMD - Command parsed!"
    except:
        e = sys.exc_info()[0]
        print ( "!!! - Error: %s" % e )
        whisper("I didn't understand that. Please contact an admin for help.",user)
       
s, chan, pwd = connect.start()
       
while 1: #listen looop
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)

        if(line[0]=="PING"): #handle the occasional pings from the irc server
            s.send("PONG %s\r\n" % line[1])
                        
        if(line[1]=="376" and line[2]=="Oracle"): #autojoin the channel
            s.send("JOIN %s\r\n" % chan)

        if(line[1]=="333" and line[3].startswith("#")):
            s.send("IDENTIFY Oracle "+pwd+"\r\n")
            print "Identified"
            
        msgo=" ".join(line) #split and interpret raw messages
        msg=msgo.split(chan+" :", 1)
        
        if (len(line) > 2):
            no_colon_line = line[0].split(":", 1)
            if (len(no_colon_line) >= 2):
                user = no_colon_line[1].split("!", 1)[0]
            
        if (len(msg) >= 2):
            com = msg[1]
            print ("MSG - [" + user + "]: " + com)
        else:
            com = "none"
            print ("SMG - " + msgo)

        if(user == last_user):
            spamhandler.start(user)    
        if(com.startswith("?^")): #?^target ?do do | user
            comm = com.replace("?^","") #target ?do do
            pseudo = comm.split(" ",1) #target, ?do do
            parsecmd(pseudo[0],pseudo[1]) #parse(user: target, cmd: ?do do)
        elif(com.startswith("?")): #?do | user
            parsecmd(user, com)

        if(com.startswith("http://www.youtube.com/")):
            try:
                author, title = youtube.parselink(com)
                say("\x02YouTube\x02 Video - " + title + " by " + author + " - " + com.split(" ",1)[0])
            except:
                say("Youtube video failed - 404 Not Found")
        last_user = user
