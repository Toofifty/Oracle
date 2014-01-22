# -*- coding: utf-8 -*-

"""
~ ?Oracle Bot v0.1 ~ #
written by Toofifty, primarily for use of the Rapidcraft Minecraft Server IRC
http://rapidcraftmc.com/
http://www.reddit.com/r/rapidcraft/
#rapidcraft on irc.esper.net

"""

import sys
import string
import urllib
import traceback
import time
import calendar
import random
import os
from colorama import init, Fore, Back
init(autoreset=True)

import connect as c
import mail as m
import events as e
import varcontrols as v
import notes as n
import youtube
import cleverbot
import spamhandler

"""
Prints the commands and help list to the user
"""
def helpc(nick, args):
    rank = v.getrank(nick)
    
    if(len(args) < 1):
        c.whisper("~ Welcome to the Oracle guide! Commands are categorised for neatness. Use ?help [category] to list those commands. ~",nick)
        c.whisper("Categories: Emotes - Server - Personal - Other - Admin", nick)        
    elif(args.lower() == "emotes"):
        c.whisper("~ Emotes ~", nick)
        c.whisper("- ?fliptable > (╯°□°)╯︵ ┻━┻ ", nick)
        c.whisper("- ?puttableback > ┬─┬﻿ ノ( ゜-゜ノ)", nick)
        c.whisper("- ?ohyou > ¯_(ツ)_/¯", nick)
        c.whisper("- ?fff > ლ(ಠ益ಠლ)", nick)
        c.whisper("- ?disapprove > ಠ_ಠ", nick)
        c.whisper("- ?crie > ಥ_ಥ", nick)
        c.whisper("- ?lenny > ( ͡° ͜ʖ ͡°)", nick)
        c.whisper("- ?dongers > ヽ༼ຈل͜ຈ༽ﾉ", nick)
    elif(args.lower() == "server"):
        c.whisper("~ Server ~", nick)
        c.whisper("- ?events > Next upcoming event", nick)
        c.whisper("- ?utc > Time now, in UTC", nick)
        c.whisper("- ?poll [time] [question] [answer 1] [answer 2] ... [answer n] > WIP, do not use", nick)
        c.whisper("- ?vote [answer] > WIP, do not use", nick)
    elif(args.lower() == "personal"):
        c.whisper("~ Personal ~", nick)
        c.whisper("- ?notes [new|edit|delete] [filename] [text]", nick)
        c.whisper("- ?notes [search|get] [searchterm|filename] > ", nick)
        c.whisper("- ?notes [listall] > List all notes", nick)
        c.whisper("- ?mail [check|send|read|delete] [mail] > WIP, do not use", nick)
    elif(args.lower() == "other"):
        c.whisper("~ Other ~", nick)
        c.whisper("- ?pick [choice 1] [choice 2] ... [choice n] > Picks a choice at random", nick)
        c.whisper("- ?cb [message] > Chat with cleverbot (experimental)", nick) 
        c.whisper("- ?diamonds [target] > Gives target 64 diamonds in-game", nick) 
    elif(args.lower() == "admin") and (rank >= 2):
        c.whisper("~ Admin ~", nick)
        c.whisper("- ?close > Turn off the Oracle bot", nick)
        c.whisper("- ?reload > Restart the bot, to reload settings or code", nick)
        c.whisper("- ?say [message] > Instruct Oracle to repeat the message", nick)
        c.whisper("- ?attention > Alert all users in irc", nick)
        c.whisper("- ?setrank [target] [rank] > Set a user's rank, allowing/restricting permission to certain actions. Use ?help ranks for more info.", nick)
    elif(args.lower() == "dev") and (rank >= 3):
        c.whisper("~ Developer ~", nick)
        c.whisper("- ?makevar [target] > Create a VAR file for target", nick)
        c.whisper("- ?getvar [target] [var] > Retrieves a specific value", nick)
        c.whisper("- ?setvar [target] [var] [value] > Sets a specific value", nick)
        c.whisper("- ?deletevar [target] > Deletes the VAR file for target", nick)
        c.whisper("- ?resetvar [target] > Combined command for both deletevar and makevar", nick)
    elif(args.lower() == "ranks") and (rank >= 2):
        c.whisper("~ Ranks ~", nick)
        c.whisper("- 0 > Banned user. Will be kicked automatically after joining.", nick)
        c.whisper("- 1 > Default user. Can do most commands.", nick)
        c.whisper("- 2 > Moderator. Can instruct Oracle to kick, mute or ban (lower ranked) users.", nick)
        c.whisper("- 3 > Administrator. Access to almost all commands needed, can reload/close Oracle if necessary.", nick)
        c.whisper("- 4 > Developer. Access to specific debug commands. If need be, admins can set themselves to dev with ?setrank.", nick)
    else:
        c.whisper("~ Welcome to the Oracle guide! Commands are categorised for neatness. Use ?help [category] to list those commands. ~",nick)
        if rank >= 4:
            c.whisper("Categories: Emotes - Server - Personal - Other - Admin - Ranks - Dev", nick) 
        elif rank >= 3:
            c.whisper("Categories: Emotes - Server - Personal - Other - Admin - Ranks", nick) 
        else:
            c.whisper("Categories: Emotes - Server - Personal - Other", nick) 
 
"""
Asks cleverbot a question, and prints and says the response (broken)
"""
def cb(ask, nick):
    cbot = cleverbot.Session()
    response = cbot.Ask(ask)
    print (Fore.CYAN + "CBT" + Fore.RESET + " - " + response)
    c.say(nick + ": " + response)

"""
Processes commands that begin with a ?
"""
def processcmd(nick, msg):
    cmd = msg.split(" ")
    args = msg.split(" ",1)
    rank = v.getrank(nick)
    print (Fore.MAGENTA + "CMD" + Fore.RESET + " - " + cmd[0] + " | nick: " + nick)
    
    try:
        # emotes #
        if cmd[0] == "?fliptable": c.say("(╯°□°)╯︵ ┻━┻")
        elif cmd[0] == "?puttableback": c.say("┬─┬﻿ ノ( ゜-゜ノ)")
        elif cmd[0] == "?ohyou": c.say("¯_(ツ)_/¯")
        elif cmd[0] == "?FLIPTABLE": c.say("(ノಠ益ಠ)ノ彡┻━┻")
        elif cmd[0] == "?fff": c.say("ლ(ಠ益ಠლ)")
        elif cmd[0] == "?disapprove": c.say("ಠ_ಠ")
        elif cmd[0] == "?crie": c.say("ಥ_ಥ")
        elif cmd[0] == "?lenny": c.say("( ͡° ͜ʖ ͡°)")
        elif cmd[0] == "?dongers": c.say("ヽ༼ຈل͜ຈ༽ﾉ")
        
        # other #
        elif cmd[0] == "?help":
            if(len(cmd) < 2): helpc(nick, "no")
            else: helpc(nick, cmd[1])
            
        elif cmd[0] == "?cb": cb(args[1], nick)
        
        elif cmd[0] == "?pick":
            choice = random.randint(1, len(cmd))
            c.say(nick + ": " + cmd[choice] + " (" + str(choice) + ") ")
            
        elif cmd[0] == "?diamonds":
            c.whisper("Well done, " + nick + ".", nick)
            rickroll = ["We're no strangers to love",
                "You know the rules, and so do I",
                "A full commitment's what I'm thinking of",
                "You wouldn't get this from any other guy",
                "I just wanna tell you how I'm feeling",
                "Gotta make you understand",
                "Never gonna give you up",
                "Never gonna let you down",
                "Never gonna run around and desert you",
                "Never gonna make you cry",
                "Never gonna say goodbye",
                "Never gonna tell a lie and hurt you",
                "We've known each other for so long",
                "Your heart's been aching, but",
                "You're too shy to say it",
                "Inside, we both know what's been going on",
                "We know the game and we're gonna play it",
                "And if you ask me how I'm feeling",
                "Don't tell me you're too blind to see",
                "Never gonna give you up",
                "Never gonna let you down",
                "Never gonna run around and desert you",
                "Never gonna make you cry",
                "Never gonna say goodbye",
                "Never gonna tell a lie and hurt you"
                ]
            for line in rickroll:
                c.say("< " + nick + " > " + line)
                time.sleep(2)
            c.say("\x0313This Rick-Roll brought to you by \x0311" + nick + "\x0311")
        
        # moderator #
        elif cmd[0] == "?say" and (rank >= 2): c.say(args[1])
        elif cmd[0] == "?attention" and (rank >= 2): c.getusers()
        
        # admin #
        elif cmd[0] == "?close" and (rank >= 3): c.stop(nick)
        elif cmd[0] == "?reload" and (rank >= 3): c.restart(nick)
        elif cmd[0] == "?setrank" and (rank >= 3):
            v.setvar(nick, cmd[1], "rank", int(cmd[2]))
            c.whisper(cmd[1] + "'s rank set to " + cmd[2] + ".", nick)
            
        # server #
        elif cmd[0] == "?events":
            results = e.get()
            if results:
                c.say("\x02Event\x02: " + results[0] + " || \x02Time\x02: " + results[1] + " UTC")
            else:
                c.say("\x02No events found\x02 - there may be none planned.")
                
        elif cmd[0] == "?utc":
            c.say(e.utc() + " UTC")
            
        # dev #
        elif cmd[0] == "?makevar" and (rank >= 4):
            target = cmd[1]
            if(v.makevarfile(nick, target)):
                print (Fore.RED + "!!!" + Fore.RESET + " - New var file created for " + target + " by " + nick)
                c.whisper("VAR file successfully created for " + target, nick)
            else:
                print (Fore.RED + "!!!" + Fore.RESET + " - Var file creation failed - " + nick)
                c.whisper("VAR file failed to create for " + target, nick)
                
        elif cmd[0] == "?getvar" and (rank >= 4):
            response = v.getvar(nick, cmd[1], cmd[2])
            c.whisper("VAR: %s = %s" % (cmd[2], response),nick)
            
        elif cmd[0] == "?setvar":
            if(v.setvar(nick, cmd[1], cmd[2], int(cmd[3]))):
                c.whisper("VAR: %s set to %s for %s" % (cmd[2], cmd[3], cmd[1]), nick)
            else:
                c.whisper("Setting of variable failed.", nick)
                
        elif cmd[0] == "?deletevar" and (rank >= 4):
            if(v.deletevarfile(nick, cmd[1])):
                c.whisper("VAR file successfully deleted.", nick)
            else:
                c.whisper("VAR file deletion failed.", nick)
            
        elif cmd[0] == "?resetvar" and (rank >= 4):
            target = cmd[1]
            if(v.deletevarfile(nick, target)):
                c.whisper("VAR file successfully deleted.", nick)
            else:
                c.whisper("VAR file deletion failed.")
            if(v.makevarfile(nick, target)):
                print (Fore.RED + "!!!" + Fore.RESET + " - New var file created for " + target + " by " + nick)
                c.whisper("VAR file successfully created for " + target, nick)
            else:
                print (Fore.RED + "!!!" + Fore.RESET + " - Var file creation failed - " + nick)
                c.whisper("VAR file failed to create for " + target, nick)
                
        elif cmd[0] == "?formats" and (rank >= 4):
            c.say("\x02x02\x02 \x37xx37\x37 \x26x26\x26 \x17x17\x17 \x0301,02x0301,02\x0301,02 "
                + "\x0303,04x0303,04\x0303,04 \x0305,06x0305,06\x0305,06 \x0307,08x0307,08\x0307,08 "
                + "\x0309,10x0309,10\x0309,10 \x0311,12x0311,12\x0311,12 \x0313,14x0313,14\x0313,14 "
                + "\x0315,00x0315,00\x0315,00")
                
        elif cmd[0] == "?cls" and (rank >= 4):
            os.system("cls")
          
        # personal #
        elif cmd[0] == "?mail":
            try:
                if cmd[1].lower() == "check":
                    m.check(nick)
                elif cmd[1].lower() == "send":
                    msg = " ".join(cmd[3:(len(cmd)-1)])
                    m.send(nick, cmd[2], msg)
                elif cmd[1].lower() == "read":
                    m.read(nick, cmd[2])
                elif cmd[1].lower() == "delete" or cmd[1].lower() == "del":
                    m.delete(nick, cmd[2])
                else:
                    c.say("Usage: ?mail [check|send|read]")
            except:
                traceback.print_exc()
                c.say("Usage: ?mail [check|send|read]")
                
        elif cmd[0] == "?notes":
            try:
                if cmd[1].lower() == "new":
                    text = msg.split(cmd[2] + " ", 1)
                    if n.new(cmd[2], text[1]):
                        c.say("Note successfully created.")
                    else:
                        c.say("Note already exists with that file name")
                elif cmd[1].lower() == "delete":
                    if n.delete(cmd[2]):
                        c.say("Note successfully deleted.")
                    else:
                        c.say("Deletion failed")
                elif cmd[1].lower() == "edit":
                    text = msg.split(cmd[2] + " ", 1)
                    print text
                    n.edit(cmd[2], text[1])
                elif cmd[1].lower() == "listall":
                    c.say(" ".join(n.list()))
                elif cmd[1].lower() == "search" or cmd[1].lower() == "list":
                    c.say(" ".join(n.find(cmd[2])))
                elif cmd[1].lower() == "get":
                    c.say(nick + ": " + n.get(cmd[2]))
                else:
                    c.say("Usage: ?notes [new|delete|edit|listall|search|get]")
            except:
                traceback.print_exc()
                c.say("Usage: ?notes [new|delete|edit|listall|search|get]")
                
        else:
            c.whisper("Unknown command.", nick)
        
    except:
        traceback.print_exc()
        c.whisper("I didn't understand that. Please contact an admin for help.",nick)
"""
Main function, everything happens through this loop
"""
def main():
    readbuffer = ""
    last_nick = 0
    welcomed = False 
    
    try:
        s, chan = c.start()
    except:
        sys.exit(Fore.RED + "There was an error connecting to the server.")
    
    while True:
        readbuffer = readbuffer+s.recv(1024)
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            line = string.split(string.rstrip(line)) # line is an array of words
            msgo = " ".join(line) # joins words into one string
                 
            if(line[0] == "PING"): c.ping(line[1]) # handle server pings
            elif(line[1] == "376" and line[2] == c.loadconfig()["ident"]): c.join() # join channel
            elif(line[1] == "333" and line[3].startswith("#")): c.identify() # identify
            elif(line[1] == "353" and welcomed): c.say(msgo.split(":")[2]) # ?attention NAMES response
            elif(line[1] == "366" and not welcomed): # welcome message
                c.say("\x0311Oracle bot has joined the session. Use \x0313?help\x0311 for guidance.\x0311")
                welcomed = True
            
            #print msgo
            
            if (len(line) > 2):
                col_split = line[0].split(":", 1)
                if (len(col_split) >= 2):
                    nick = col_split[1].split("!", 1)[0]
                else:
                    nick = "null"
                    
                if (line[2].startswith("#")):
                    msg = msgo.split(chan+" :", 1)
                else:
                    msg = msgo.split("Oracle :", 1)
            else:
                nick = "null"
            
            if nick == "null": break
            
            if (len(msg) >= 2):
                com = msg[1]
                print (Fore.CYAN + "MSG" + Fore.RESET + " - [" + nick + "]: " + com)
            else:
                com = "none"

            if(nick == last_nick):
                spamhandler.handler(nick,msg) 
                
            if(com.startswith("?^") and v.getrank(nick) >= 3): # ?^target ?cmd args | nick
                comm = com.replace("?^","") # target ?cmd args
                pseudo = comm.split(" ",1) # target, ?cmd args
                processcmd(pseudo[0],pseudo[1]) # process(nick: target, cmd: ?cmd args)
                
            elif(com.startswith("?")):
                processcmd(nick, com) # ?cmd | nick
            
            if(com == "nope"):
                c.say("\x02nope.avi\x02 - http://www.youtube.com/watch?v=gvdf5n-zI14") # gag
                
            if(com.startswith("http://www.youtube.com/")):
                try:
                    author, title = youtube.processlink(com)
                    c.say("\x0304\x02YouTube Video\x02\x03 - " + title + " by " + author + " - " + com.split(" ",1)[0])
                except:
                    c.say("\x0304Youtube video failed\x0304 - 404 Not Found")
                    
            last_nick = nick

    connect.stop("Auto")
    
main()