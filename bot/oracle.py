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
import urllib
from datetime import datetime
import time
import calendar
from colorama import init, Fore, Back
init(autoreset=True)

import connect
import youtube
import cleverbot
import varcontrols
import spamhandler

c = connect
readbuffer=''
last_nick=0

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def events(nick):
    try:
        xmldoc = minidom.parse(urllib.urlopen('http://rapidcraftmc.com/api.php?events'))
        dname = xmldoc.getElementsByTagName('name')[0]
        dtime = xmldoc.getElementsByTagName('timestamp')[0]
        u_time = getText(dtime.childNodes)
        p_name = getText(dname.childNodes)
        #print u_time
        c.say("\x02Event\x02: " + p_name + " || \x02Time\x02: " + str(time.ctime(int(u_time))) + " UTC")
    except:
        c.say("\x02No events found\x02 - there may be none planned.")
def timenow(nick): #
    d = datetime.utcnow()
    c.say(str(time.ctime(calendar.timegm(d.utctimetuple()))) + " UTC")

def helpc(nick, args): #whisper command help to nick
    if(len(args) < 1):
        c.whisper("~ Welcome to the Oracle guide! Commands are categorised for neatness. Use ?help [category] to list those commands. ~",nick)
        c.whisper("Categories: Emotes - Server - Personal - Other - Admin", nick)        
    elif(args.lower() == "emotes"):
        c.whisper("~ Emotes ~", nick)
        c.whisper("- ?fliptable > (?°?°)?? ??? ", nick)
        c.whisper("- ?puttableback > ---? ?( ?-??)", nick)
        c.whisper("- ?ohyou > ¯_(?)_/¯", nick)
        c.whisper("- ?fff > ?(????)", nick)
        c.whisper("- ?disapprove > ?_?", nick)
        c.whisper("- ?crie > ?_?", nick)
        c.whisper("- ?lenny > ( ?° ?? ?°)", nick)
    elif(args.lower() == "server"):
        c.whisper("~ Server ~", nick)
        c.whisper("- ?events > Next upcoming event", nick)
        c.whisper("- ?utc > Time now, in UTC", nick)
    elif(args.lower() == "personal"):
        c.whisper("~ Personal ~", nick)
        c.whisper("- Nothing here yet! Here will be messages, reports, etc.", nick)
    elif(args.lower() == "other"):
        c.whisper("~ Other ~", nick)
        c.whisper("- Nothing here yet! Here will be games, youtube linking, etc", nick)
    elif(args.lower() == "admin") and (nick == "Toofifty" or nick == "Manyman" or nick == "Huppatz"):
        c.whisper("~ Admin ~", nick)
        c.whisper("- ?close > Turn off the Oracle bot", nick)
        c.whisper("- ?reload > Restart the bot, to reload settings or code", nick)
    else:
        c.whisper("~ Welcome to the Oracle guide! Commands are categorised for neatness. Use ?help [category] to list those commands. ~",nick)
        c.whisper("Categories: Emotes - Server - Personal - Other - Admin", nick) 

def cb(ask, nick):
    cbot = cleverbot.Session()
    response = cbot.Ask(ask)
    c.say(nick + ": \x0309" + response)
            
def parsecmd(nick, msg): #command listing
    cmd = msg.split(" ")
    args = msg.split(" ",1)
    print (Fore.MAGENTA + "CMD" + Fore.RESET + " - " + cmd[0] + " | nick: " + nick)
    if cmd[0] == "?fliptable":
        c.say("(?°?°)?? ???")
        
    elif cmd[0] == "?puttableback":
        c.say("---? ?( ?-??)")
        
    elif cmd[0] == "?help":
        if(len(cmd) < 2):
            helpc(nick, "no")
        else:
            helpc(nick, cmd[1])
            
    elif cmd[0] == "?close" and (nick == "Toofifty" or nick == "Manyman" or nick == "Huppatz"):
        c.stop(nick)
        
    elif cmd[0] == "?reload" and (nick == "Toofifty" or nick == "Manyman" or nick == "Huppatz"):
        c.restart(nick)
        
    elif cmd[0] == "?events":
        events(nick)
        
    elif cmd[0] == "?utc":
        timenow(nick)
        
    elif cmd[0] == "?ohyou":
        c.say("¯_(?)_/¯")
        
    elif cmd[0] == "?FLIPTABLE":
        c.say("(????)?????")
        
    elif cmd[0] == "?fff":
        c.say("?(????)")
        
    elif cmd[0] == "?disapprove":
        c.say("?_?")
        
    elif cmd[0] == "?crie":
        c.say("?_?")
        
    elif cmd[0] == "?lenny":
        c.say("( ?° ?? ?°)")
        
    elif cmd[0] == "?makevar":
        target = cmd[1]
        if(varcontrols.makevarfile(nick, target)):
            print (Fore.RED + "!!!" + Fore.RESET + " - New var file created for " + target + " by " + nick)
            c.whisper("VAR file successfully created for " + target, nick)
        else:
            print (Fore.RED + "!!!" + Fore.RESET + " - Var file creation failed - " + nick)
            c.whisper("VAR file failed to create for " + target, nick)
            
    elif cmd[0] == "?getvar":
        response = varcontrols.getvar(nick, cmd[1], cmd[2])
        c.whisper("VAR: %s = %s" % (response, cmd[2]),nick)
        
    elif cmd[0] == "?setvar":
        if(varcontrols.setvar(nick, cmd[1], cmd[2], cmd[3])):
            c.whisper("VAR: %s set to %s for %s" % (cmd[1], cmd[2], cmd[3]), nick)
        else:
            c.whisper("Setting of variable failed.")
        
    elif cmd[0] == "?cb":
        cb(args[1], nick)
        
    elif cmd[0] == "?attention":
        attention(nick)
        
    elif cmd[0] == "?say":
        c.say(args[1])
        
    elif cmd[0] == "?formats":
        c.say("\x02x02\x02 \x37xx37\x37 \x26x26\x26 \x17x17\x17 \x0301,02x0301,02\x0301,02 \x0303,04x0303,04\x0303,04  \x0305,06x0305,06\x0305,06  \x0307,08x0307,08\x0307,08 \x0309,10x0309,10\x0309,10 \x0311,12x0311,12\x0311,12 \x0313,14x0313,14\x0313,14  \x0315,00x0315,00\x0315,00")
    
    else:
        c.whisper("Unknown command.", nick)
    print (Fore.MAGENTA + "CMD" + Fore.RESET + " - Command parsed!")
    #except:
    #    e = sys.exc_info()[0]
    #    print ( "!!! - Error: %s" % e )
    #    whisper("I didn't understand that. Please contact an admin for help.",nick)
   
try:   
    s, chan = c.start()
except:
    sys.exit(Fore.RED + "There was an error connecting to the server.")
       
while 1: #listen looop
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)

        if(line[0]=="PING"): #handle the occasional pings from the irc server
            c.ping(line[1])
                        
        elif(line[1]=="376" and line[2]=="Oracle"): #autojoin the channel
            c.join()

        elif(line[1]=="333" and line[3].startswith("#")): #identify once the channel is joined
            c.identify()
            
        elif(line[1]=="366"): #welcome message once joined
            c.say("\x0311Oracle bot has joined the session. Use \x0313?help\x0311 for guidance.\x0311")
            
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
        
        if nick == "null":
            break
        
        if (len(msg) >= 2):
            com = msg[1]
            print (Fore.CYAN + "MSG" + Fore.RESET + " - [" + nick + "]: " + com)
        else:
            com = "none"

        if(nick == last_nick):
            #print "NCK - " + nick
            spamhandler.handler(nick,msg)    
        if(com.startswith("?^")): #?^target ?do do | nick
            comm = com.replace("?^","") #target ?do do
            pseudo = comm.split(" ",1) #target, ?do do
            parsecmd(pseudo[0],pseudo[1]) #parse(nick: target, cmd: ?do do)
        elif(com.startswith("?")): #?do | nick
            parsecmd(nick, com)
        
        if(com == "nope"):
            c.say("\x02nope.avi\x02 - http://www.youtube.com/watch?v=gvdf5n-zI14")
        if(com.startswith("http://www.youtube.com/")):
            try:
                author, title = youtube.parselink(com)
                c.say("\x0304\x02YouTube Video\x02\x03 - " + title + " by " + author + " - " + com.split(" ",1)[0])
            except:
                c.say("\x0304Youtube video failed\x0304 - 404 Not Found")
                
        last_nick = nick

connect.stop("Auto")