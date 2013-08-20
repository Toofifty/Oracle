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
last_nick=0

def say(msg):
    s.send("PRIVMSG " + str(chan) + " :" + str(msg) + "\r\n")
    
def sayf(msg, format):
    s.send("PRIVMSG %s :%s%s\r\n" % (str(chan),str(format),str(msg)))   
    
def kick(nick):
    s.send("KICK %s\r\n" % nick)

def whisper(msg, nick):
    s.send("NOTICE " + nick + " :" + str(msg) + "\r\n")

def stop(nick):
    print "!!! - Stop command issued! Closing."
    say("Goodbye!")
    s.send("QUIT\r\n")
    sys.exit("!!! - " + nick +" terminated session.")

def restart(nick):
    print ("!!! - Restart command issued by " + nick)
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

def events(nick):
    xmldoc = minidom.parse(urllib.urlopen('http://rapidcraftmc.com/api.php?events'))
    dname = xmldoc.getElementsByTagName('name')[0]
    dtime = xmldoc.getElementsByTagName('timestamp')[0]
    u_time = getText(dtime.childNodes)
    p_name = getText(dname.childNodes)
    #print u_time
    say("Event: " + p_name + " || Time: " + str(time.ctime(int(u_time))) + " UTC")

def timenow(nick): #
    d = datetime.utcnow()
    say(str(time.ctime(calendar.timegm(d.utctimetuple()))) + " UTC")

def helpc(nick, args): #whisper command help to nick
    if(len(args) < 1):
        whisper("~ Welcome to the Oracle guide! Commands are categorised for neatness. Use ?help [category] to list those commands. ~",nick)
        whisper("Categories: Emotes - Server - Personal - Other - Admin", nick)        
    elif(args.lower() == "emotes"):
        whisper("~ Emotes ~", nick)
        whisper("- ?fliptable > (╯°□°)╯︵ ┻━┻ ", nick)
        whisper("- ?puttableback > ┬─┬﻿ ノ( ゜-゜ノ)", nick)
        whisper("- ?ohyou > ¯_(ツ)_/¯", nick)
        whisper("- ?fff > ლ(ಠ益ಠლ)", nick)
        whisper("- ?disapprove > ಠ_ಠ", nick)
        whisper("- ?crie > ಥ_ಥ", nick)
        whisper("- ?lenny > ( ͡° ͜ʖ ͡°)", nick)
    elif(args.lower() == "server"):
        whisper("~ Server ~", nick)
        whisper("- ?events > Next upcoming event", nick)
        whisper("- ?utc > Time now, in UTC", nick)
    elif(args.lower() == "personal"):
        whisper("~ Personal ~", nick)
        whisper("- Nothing here yet! Here will be messages, reports, etc.", nick)
    elif(args.lower() == "other"):
        whisper("~ Other ~", nick)
        whisper("- Nothing here yet! Here will be games, youtube linking, etc", nick)
    elif(args.lower() == "admin") and (nick == "Toofifty" or nick == "Manyman" or nick == "Huppatz"):
        whisper("~ Admin ~", nick)
        whisper("- ?close > Turn off the Oracle bot", nick)
        whisper("- ?reload > Restart the bot, to reload settings or code", nick)
    else:
        whisper("~ Welcome to the Oracle guide! Commands are categorised for neatness. Use ?help [category] to list those commands. ~",nick)
        whisper("Categories: Emotes - Server - Personal - Other - Admin", nick) 

def cb(ask, nick):
    cbot = cleverbot.Session()
    response = cbot.Ask(ask)
    say(response)
            
def parsecmd(nick, msg): #command listing
    cmd = msg.split(" ")
    args = msg.split(" ",1)
    print ("CMD - " + cmd[0] + " | nick: " + nick)
    if cmd[0] == "?fliptable":
        say("(╯°□°)╯︵ ┻━┻")
    elif cmd[0] == "?puttableback":
        say("┬─┬﻿ ノ( ゜-゜ノ)")
    elif cmd[0] == "?help":
        if(len(cmd) < 2):
            helpc(nick, "no")
        else:
            helpc(nick, cmd[1])
    elif cmd[0] == "?close" and (nick == "Toofifty" or nick == "Manyman" or nick == "Huppatz"):
        stop(nick)
    elif cmd[0] == "?reload" and (nick == "Toofifty" or nick == "Manyman" or nick == "Huppatz"):
        restart(nick)
    elif cmd[0] == "?events":
        events(nick)
    elif cmd[0] == "?utc":
        timenow(nick)
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
        if(varcontrols.makevarfile(nick, target)):
            print ("!!! - New var file created for " + target + " by " + nick)
            whisper("VAR file successfully created for " + target, nick)
        else:
            print ("!!! - Var file creation failed - " + nick)
            whisper("VAR file failed to create for " + target, nick)
            
    elif cmd[0] == "?getvar":
        response = varcontrols.getvar(nick, cmd[1], cmd[2])
        whisper("VAR: %s = %s" % (response, cmd[2]),nick)
        
    elif cmd[0] == "?setvar":
        if(varcontrols.setvar(nick, cmd[1], cmd[2], cmd[3])):
            whisper("VAR: %s set to %s for %s" % (cmd[1], cmd[2], cmd[3]), nick)
        else:
            whisper("Setting of variable failed.")
        
    elif cmd[0] == "?cb":
        cb(args[1], nick)
        
    elif cmd[0] == "?attention":
        attention(nick)
        
    elif cmd[0] == "?say":
        say(args[1])
        
    else:
        whisper("Unknown command.", nick)
    print "CMD - Command parsed!"
    #except:
    #    e = sys.exc_info()[0]
    #    print ( "!!! - Error: %s" % e )
    #    whisper("I didn't understand that. Please contact an admin for help.",nick)
       
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
        
        if (len(line) > 2):
        
            no_colon_line = line[0].split(":", 1)
            
            if (len(no_colon_line) >= 2):
                nick = no_colon_line[1].split("!", 1)[0]
            else:
                nick = "null"
                
            if (line[2].startswith("#")):    
                msg=msgo.split(chan+" :", 1)
            else:
                msg=msgo.split("Oracle :", 1)
                
        else:
            nick = "null"
            
        if (len(msg) >= 2):
            com = msg[1]
            print ("MSG - [" + nick + "]: " + com)
        else:
            com = "none"
            print line

        if(nick == last_nick):
            print "NCK - " + nick
            spamhandler.handler(nick)    
        if(com.startswith("?^")): #?^target ?do do | nick
            comm = com.replace("?^","") #target ?do do
            pseudo = comm.split(" ",1) #target, ?do do
            parsecmd(pseudo[0],pseudo[1]) #parse(nick: target, cmd: ?do do)
        elif(com.startswith("?")): #?do | nick
            parsecmd(nick, com)
        
        if(com == "nope"):
            say("\x02nope.avi\x02 - http://www.youtube.com/watch?v=gvdf5n-zI14")
        if(com.startswith("http://www.youtube.com/")):
            try:
                author, title = youtube.parselink(com)
                say("\00304\x02YouTube\x02\003 Video - " + title + " by " + author + " - " + com.split(" ",1)[0])
            except:
                say("Youtube video failed - 404 Not Found")
        last_nick = nick
