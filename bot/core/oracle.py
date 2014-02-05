# -*- coding: utf-8 -*-

"""
~ ?Oracle Bot v1.0.0 ~ 
written by Toofifty, primarily for use of the Rapid Minecraft Server IRC
http://rapidcraftmc.com/
http://www.reddit.com/r/rapid/
#rapid on irc.esper.net

"""

import sys
import string
import urllib
import traceback
import time
import calendar
import os
import logging
from colorama import init, Fore, Back, Style
init(autoreset=True)

import connect as c
import mail as m
import events as e
import varcontrols as v
import notes as n
import youtube
import cleverbot
import spamhandler
import format
import misc
import translate
import gags
import logger
    
f = format.formats()

"""
Reload all modules except for oracle.py, connect.py and run.py
connect.py and run.py cannot be reloaded without restarting the bot,
and oracle.py needs to be reloaded from outside this module (run.py)
"""
def rl(nick):
    modules = [m, e, v, n, youtube, cleverbot, spamhandler, format, misc, translate, gags, logger]
    for mod in modules:
        reload(mod)
    
    action_log = logging.getLogger('action')
    action_log.info(Fore.RED + "RLD" + Fore.RESET + " Reload issued by " + nick)
        
    global do_reload
    do_reload = True

"""
Prints the commands and help list to the user
"""
def helpc(nick, args):
    rank = v.getrank(nick)
     
    if(args.lower() == "emotes"):
        c.whisper("~ " + f.BOLD + "Emotes" + f.BOLD + " ~", nick)
        c.whisper("- ?fliptable > (╯°□°)╯︵ ┻━┻ ", nick)
        c.whisper("- ?puttableback > ┬─┬﻿ ノ( ゜-゜ノ)", nick)
        c.whisper("- ?ohyou > ¯_(ツ)_/¯", nick)
        c.whisper("- ?fff > ლ(ಠ益ಠლ)", nick)
        c.whisper("- ?disapprove > ಠ_ಠ", nick)
        c.whisper("- ?crie > ಥ_ಥ", nick)
        c.whisper("- ?lenny > ( ͡° ͜ʖ ͡°)", nick)
        c.whisper("- ?dongers > ヽ༼ຈل͜ຈ༽ﾉ", nick)
        c.whisper("- ?butterfly > Ƹ̵̡Ӝ̵̨̄Ʒ", nick)
        c.whisper("- ?partytime > ┏(-_-)┛┗(-_-﻿ )┓┗(-_-)┛┏(-_-)┓", nick)
        c.whisper("- ?polarbear > ˁ˚ᴥ˚ˀ", nick)
        c.whisper("- ?gun > ︻╦╤─", nick)
        c.whisper("- ?pirate > ✌(◕‿-)✌", nick)
        c.whisper("- ?happybirthday > ¸¸♬·¯·♩¸¸♪·¯·♫¸¸Happy Birthday To You¸¸♬·¯·♩¸¸♪·¯·♫¸¸", nick)
        c.whisper("- ?sunglasses > ( •_•) ( •_•)>⌐■-■ (⌐■_■)", nick)
        c.whisper("- ?rage > t(ಠ益ಠt)", nick)
        c.whisper("- ?cards > [♥]]] [♦]]] [♣]]] [♠]]]", nick)
        c.whisper("- ?gimme > ༼ つ ◕_◕ ༽つ", nick)
        c.whisper("- ?monocle > ಠ_ರೃ", nick)
        c.whisper("- ?ghost > ‹’’›(Ͼ˳Ͽ)‹’’›", nick)
        c.whisper("- ?why > ლ(`◉◞౪◟◉‵ლ)", nick)
        c.whisper("- ?praise > し(*･∀･)／♡＼(･∀･*)ノ", nick)
    elif(args.lower() == "server"):
        c.whisper("~ " + f.BOLD + "Server" + f.BOLD + " ~", nick)
        c.whisper("- ?events > Next upcoming event", nick)
        c.whisper("- ?utc > Time now, in UTC", nick)
        c.whisper("- ?nether [x] [y] [z] > Convert xyz overworld coordinates to the corresponding nether coordinates", nick)
        c.whisper("- ?overworld [x] [y] [z] > Vice-versa of above", nick)
        c.whisper("x ?poll [time] [question] [answer 1] [answer 2] ... [answer n] > WIP, do not use", nick)
        c.whisper("x ?vote [answer] > WIP, do not use", nick)
    elif(args.lower() == "personal"):
        c.whisper("~ " + f.BOLD + "Personal" + f.BOLD + " ~", nick)
        c.whisper("- ?notes [new|edit|delete] [filename] [text] > Create and delete notes", nick)
        c.whisper("- ?notes [search|get] [searchterm|filename] > Search all notes for a specific term", nick)
        c.whisper("- ?notes listall > List all notes", nick)
        c.whisper("- ?mail send [recipient] [title] [message...] > Send mail to a player, who will be notified when they join", nick)
        c.whisper("- ?mail [read|delete] [mail] > Read the contents of the mail or delete it", nick)
        c.whisper("- ?mail check > List all mail addressed to you", nick)
    elif(args.lower() == "other"):
        c.whisper("~ " + f.BOLD + "Other" + f.BOLD + " ~", nick)
        c.whisper("- ?pick [choice 1] [choice 2] ... [choice n] > Picks a choice at random", nick)
        c.whisper("- ?cb [message] > Chat with cleverbot (experimental)", nick) 
        c.whisper("- ?diamonds [target] > Gives target 64 diamonds in-game", nick) 
        c.whisper("- ?ayylmao > Link to ayy lmao image", nick) 
    elif(args.lower() == "admin") and (rank >= 2):
        c.whisper("~ " + f.BOLD + "Admin" + f.BOLD + " ~", nick)
        c.whisper("- ?close > Turn off the Oracle bot", nick)
        c.whisper("- ?restart > Restart the bot, to reload settings or code", nick)
        c.whisper("- ?reload > Reload the bot, to reload settings or code without disconnecting", nick)
        c.whisper("- ?sreload > Reload the bot, silently", nick)
        c.whisper("- ?say [message] > Instruct Oracle to repeat the message", nick)
        c.whisper("- ?attention > Alert all users in irc", nick)
        c.whisper("- ?setrank [target] [rank] > Set a user's rank, allowing/restricting permission to certain actions. Use ?help ranks for more info", nick)
        c.whisper("- ?getrank [target] > Return user's rank", nick)
        c.whisper("- ?ban [target] > Set user's rank to 0. Oracle will auto-kick them if they join", nick)
    elif(args.lower() == "dev") and (rank >= 3):
        c.whisper("~ " + f.BOLD + "Developer" + f.BOLD + " ~", nick)
        c.whisper("- ?makevar [target] > Create a VAR file for target", nick)
        c.whisper("- ?getvar [target] [var] > Retrieves a specific value", nick)
        c.whisper("- ?setvar [target] [var] [value] > Sets a specific value", nick)
        c.whisper("- ?deletevar [target] > Deletes the VAR file for target", nick)
        c.whisper("- ?resetvar [target] > Combined command for both deletevar and makevar", nick)
        c.whisper("- ?cls > Clear console", nick)
        c.whisper("- ?sayr > Instruct Oracle to repeat the message (+ formats). See ?help formats", nick)
        c.whisper("- ?join > Imitate a join event", nick)
        c.whisper("- ?raw [args] > Send a raw message to IRC from Oracle", nick)
        c.whisper("- ?^[target] ?[cmd] > Sudo any command onto another user", nick)
    elif(args.lower() == "formats") and (rank >= 3):
        c.whisper("~ " + f.BOLD + "Formats" + f.BOLD + " ~", nick)
        c.whisper("- Formats are activated by using &N where N is 0-15 or b.", nick)
        c.whisper("- Can really only be used through hard-code or ?sayr", nick)
    elif(args.lower() == "ranks") and (rank >= 2):
        c.whisper("~ " + f.BOLD + "Ranks" + f.BOLD + " ~", nick)
        c.whisper("- 0 > Banned user. Will be kicked automatically after joining.", nick)
        c.whisper("- 1 > Default user. Can do most commands.", nick)
        c.whisper("- 2 > Moderator. Can instruct Oracle to kick, mute or ban (lower ranked) users.", nick)
        c.whisper("- 3 > Administrator. Access to almost all commands needed, can restart/close Oracle if necessary.", nick)
        c.whisper("- 4 > Developer. Access to specific debug commands. If need be, admins can set themselves to dev with ?setrank.", nick)
    else:
        c.whisper(f.LIGHTBLUE + "~ Welcome to the Oracle guide! Commands are categorised for neatness.", nick)
        c.whisper(f.LIGHTBLUE + "Use ?help [category] to list those commands. Categories:",nick)
        if rank >= 4:
            c.whisper(f.LIGHTBLUE + f.BOLD + "Emotes - Server - Personal - Other - Admin - Dev - Ranks - Formats", nick)  
        elif rank >= 3:
            c.whisper(f.LIGHTBLUE + f.BOLD + "Emotes - Server - Personal - Other - Admin - Ranks", nick)  
        else:
            c.whisper(f.LIGHTBLUE + f.BOLD + "Emotes - Server - Personal - Other", nick)  
 
"""
Asks cleverbot a question, and logs and says the response (broken)
Cleverbot API has been discontinued and so will probably no longer work
"""
def cb(ask, nick):
    if c.loadconfig['cleverbot']:
        cbot = cleverbot.Session()
        response = cbot.Ask(" ".join(ask))
        action_log = logging.getLogger('action')
        action_log.info(Fore.CYAN + "CBT" + Fore.RESET + " " + response)
        c.say(nick + ": " + response)
    else:
        c.whisper("Cleverbot is currently disabled.", nick)

"""
Actions to perform on user join
"""
def join(nick):
    rank = v.getrank(nick)
    config = c.loadconfig()
    
    if not v.listvar(nick) and config['auto-add']:
        v.makevarfile(nick)
    
    if config['join-message']:
        c.say(f.LIGHTBLUE + "Welcome to the Rapid IRC, " + f.PURPLE + nick + f.LIGHTBLUE + ".")
    
    if rank == 0 and config['auto-kick']:
        c.kick(nick, "You were kicked by Oracle, possibly because you were not whitelisted in the IRC? Please talk to an admin about this.")
        
    elif rank >= 3:
        if config['auto-op']:
            c.mode(["+o", nick])
            c.whisper("You have been opped by Oracle", nick)
        else:
            c.whisper("Oracle auto-op is disabled. Identify with NickServ to receive op.", nick)
            
    else:
        c.mode(["+v", nick])
       
    if config['check-mail']:
        if not m.check(nick):
            c.whisper("You have no new mail.", nick)
        else:
            c.whisper("You have mail! Use '?mail check' to see.", nick)
        
    action_log = logging.getLogger('action')
    action_log.info(Fore.BLUE + "JNC" + Fore.RESET + " " + nick + " joined. Rank: " + str(rank))    
    
"""
Splits the message, processes the commands and does all the relevant
functions required. Should reverse the 'rank' if statements but it's
not much of a problem.
"""
def processcmd(nick, msg):
    action_log = logging.getLogger('action')
    
    cmd = msg.split(" ")
    rank = v.getrank(nick)
    action_log.info(Fore.MAGENTA + "CMD" + Fore.RESET + " " + cmd[0] + " | nick: " + nick)
    
    try:
        # regular user
        # rank = 1
        if rank >= 1:
            # emotes #
            if cmd[0] == "fliptable": c.say("(╯°□°)╯︵ ┻━┻")
            elif cmd[0] == "puttableback": c.say("┬─┬﻿ ノ( ゜-゜ノ)")
            elif cmd[0] == "ohyou": c.say("¯_(ツ)_/¯")
            elif cmd[0] == "FLIPTABLE": c.say("(ノಠ益ಠ)ノ彡┻━┻")
            elif cmd[0] == "fff": c.say("ლ(ಠ益ಠლ)")
            elif cmd[0] == "disapprove": c.say("ಠ_ಠ")
            elif cmd[0] == "crie": c.say("ಥ_ಥ")
            elif cmd[0] == "lenny": c.say("( ͡° ͜ʖ ͡°)")
            elif cmd[0] == "dongers": c.say("ヽ༼ຈل͜ຈ༽ﾉ")
            elif cmd[0] == "raise": c.say("ヽ༼ຈل͜ຈ༽ﾉ")
            elif cmd[0] == "butterfly": c.say("Ƹ̵̡Ӝ̵̨̄Ʒ")
            elif cmd[0] == "partytime": c.say("┏(-_-)┛┗(-_-﻿ )┓┗(-_-)┛┏(-_-)┓")
            elif cmd[0] == "fliptables": c.say("┻━┻︵ \(°□°)/ ︵ ┻━┻")
            elif cmd[0] == "polarbear": c.say("ˁ˚ᴥ˚ˀ")
            elif cmd[0] == "gun": c.say("︻╦╤─")
            elif cmd[0] == "pirate": c.say("✌(◕‿-)✌")
            elif cmd[0] == "happybirthday": c.say("¸¸♬·¯·♩¸¸♪·¯·♫¸¸Happy Birthday To You¸¸♬·¯·♩¸¸♪·¯·♫¸¸")
            elif cmd[0] == "sunglasses": c.say("( •_•) ( •_•)>⌐■-■ (⌐■_■)")
            elif cmd[0] == "rage": c.say("t(ಠ益ಠt)")
            elif cmd[0] == "cards": c.say("[♥]]] [♦]]] [♣]]] [♠]]]")
            elif cmd[0] == "gimme": c.say("༼ つ ◕_◕ ༽つ")
            elif cmd[0] == "monocle": c.say("ಠ_ರೃ")
            elif cmd[0] == "ghost": c.say("‹’’›(Ͼ˳Ͽ)‹’’›")
            elif cmd[0] == "why": c.say("ლ(`◉◞౪◟◉‵ლ)")
            elif cmd[0] == "praise": c.say("し(*･∀･)／♡＼(･∀･*)ノ")
            elif cmd[0] == "lennyy": c.say(" ̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\з=( ͡° ͜ʖ ͡°)=ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿ ")
            # tears can be potentially dangerous, limited to admin +
            elif cmd[0] == "tears" and rank >= 3: c.say(" Ỏ̷͖͈̞̩͎̻̫̫̜͉̠̫͕̭̭̫̫̹̗̹͈̼̠̖͍͚̥͈̮̼͕̠̤̯̻̥̬̗̼̳̤̳̬̪̹͚̞̼̠͕̼̠̦͚̫͔̯̹͉͉̘͎͕̼̣̝͙̱̟̹̩̟̳̦̭͉̮̖̭̣̣̞̙̗̜̺̭̻̥͚͙̝̦̲̱͉͖͉̰̦͎̫̣̼͎͍̠̮͓̹̹͉̤̰̗̙͕͇͔̱͕̭͈̳̗̭͔̘̖̺̮̜̠͖̘͓̳͕̟̠̱̫̤͓͔̘̰̲͙͍͇̙͎̣̼̗̖͙̯͉̠̟͈͍͕̪͓̝̩̦̖̹̼̠̘̮͚̟͉̺̜͍͓̯̳̱̻͕̣̳͉̻̭̭̱͍̪̩̭̺͕̺̼̥̪͖̦̟͎̻̰_á»")
            
            # other #
            elif cmd[0] == "help" or cmd[0] == "what":
                if(len(cmd) < 2): helpc(nick, "no")
                else: helpc(nick, cmd[1])
                
            elif cmd[0] == "cb": cb(cmd[1:], nick)
            
            elif cmd[0] == "pick":
                c.say(nick + ": " + misc.pick(cmd[1:]))
                
            elif cmd[0] == "diamonds":
                if c.loadconfig()['rick-roll']:
                    gags.rick_roll(nick, cmd[1])
                else:
                    c.whisper(f.WHITE + "64 diamonds have been credited to the Minecraft account " + f.RED + nick + f.WHITE + ".", nick)
                    time.sleep(5)
                    c.whisper("Just kidding.", nick)
                    c.whisper("This command has been disabled in the config.", nick)
                    
            elif cmd[0] == "ayylmao":
                c.say("http://puu.sh/6wo5D.png")
                
            # server #
            elif cmd[0] == "events":
                results = e.get()
                
                if results:
                    c.say(f.BOLD + "Event: " + results[0] + " || " + f.BOLD + "Time" + f.BOLD + ": " + results[1] + " UTC")
                else:
                    c.say(f.BOLD + "No events found" + f.BOLD + " - there may be none planned.")
                    
            elif cmd[0] == "utc":
                c.say(e.utc() + " UTC")
                
            elif cmd[0] == "nether":
                c.whisper(misc.netherposition(int(cmd[1]), int(cmd[2]), int(cmd[3])), nick)
                
            elif cmd[0] == "overworld":
                c.whisper(misc.overworldposition(int(cmd[1]), int(cmd[2]), int(cmd[3])), nick)
      
            # personal #
            elif cmd[0] == "mail":
                try:
                    if cmd[1].lower() == "check":
                        if not m.check(nick):
                            c.whisper("You have no mail.", nick)
                        else:
                            c.whisper("Use ?mail read [mail]: "+ ", ".join(m.check(nick)), nick)
                            
                    elif cmd[1].lower() == "send":
                        text = " ".join(cmd[4:])
                        if m.send(nick, cmd[2], cmd[3], text):
                            c.whisper("Message sent.", nick)
                        else:
                            c.whisper("Message failed to send.", nick)
                            
                    elif cmd[1].lower() == "read":
                        c.whisper(m.read(nick, cmd[2]), nick)
                        
                    elif cmd[1].lower() == "delete" or cmd[1].lower() == "del":
                        if m.delete(nick, cmd[2]):
                            c.whisper("Message deleted.", nick)
                        else:
                            c.whisper("Message not deleted.", nick)
                            
                    else:
                        c.whisper("Usage: ?mail [check|send|read|delete]", nick)
                        
                except:
                    traceback.print_exc()
                    c.whisper("Usage: ?mail [check|send|read|delete]", nick)
                    
            elif cmd[0] == "notes":
                try:
                    if cmd[1].lower() == "new":
                        text = " ".join(cmd[3:])
                        if n.new(cmd[2], text):
                            c.whisper("Note successfully created.", nick)
                        else:
                            c.whisper("Note already exists with that file name", nick)
                            
                    elif cmd[1].lower() == "delete":
                        if n.delete(cmd[2]):
                            c.whisper("Note successfully deleted.", nick)
                        else:
                            c.whisper("Deletion failed", nick)
                            
                    elif cmd[1].lower() == "edit":
                        text = " ".join(cmd[3:])
                        n.edit(cmd[2], text[1])
                        
                    elif cmd[1].lower() == "listall":
                        c.whisper(" ".join(n.listall()), nick)
                        
                    elif cmd[1].lower() == "search" or cmd[1].lower() == "list":
                        c.whisper(" ".join(n.find(cmd[2])), nick)
                        
                    elif cmd[1].lower() == "get":
                        c.whisper(nick + ": " + n.get(cmd[2]), nick)
                        
                    else:
                        c.whisper("Usage: ?notes [new|delete|edit|listall|search|get]", nick)
                except:
                    traceback.print_exc()
                    c.whisper("Usage: ?notes [new|delete|edit|listall|search|get]", nick)
            
        # moderator
        # rank = 2
        if rank >= 2:
            if cmd[0] == "say":
                c.say(format.replace(" ".join(cmd[1:])))
            
            elif cmd[0] == "attention":
                c.getusers()
                
            elif cmd[0] == "ban" :
                v.setvar(nick, cmd[1], "rank", 0)
                c.whisper("User: " + cmd[1] + " has been banned.", nick)
                
            elif cmd[0] == "kick":
                if len(cmd) < 3:
                    c.kick(cmd[1], "")
                    c.whisper("User kicked.", nick)
                else:
                    c.kick(cmd[1], " ".join(cmd[2:]))
                    c.whisper("User kicked for " + " ".join(cmd[2:]) + ".", nick)
        
        # admin
        # rank = 3
        if rank >= 3:
            if cmd[0] == "close":
                c.stop(nick)
                
            elif cmd[0] == "restart" :
                c.restart(nick)
                
            elif cmd[0] == "reload":
                rl(nick)
                c.say(f.YELLOW + "Reload complete.")
                
            elif cmd[0] == "sreload":
                rl(nick)
                c.whisper(f.YELLOW + "Silent reload complete.", nick)
                
            elif cmd[0] == "setrank":
                v.setvar(cmd[1], "rank", int(cmd[2]))
                c.whisper(cmd[1] + "'s rank set to " + cmd[2] + ".", nick)
                
            elif cmd[0] == "mode":
                c.mode(cmd[1:])
                
            elif cmd[0] == "getrank":
                c.whisper(cmd[1] + "'s rank is " + str(v.getvar(cmd[1], "rank")) + ".", nick)
            
        # developer
        # rank = 4
        if rank >= 4:
            if cmd[0] == "makevar":
                target = cmd[1]
                
                if(v.makevarfile(target)):
                    action_log.info(Fore.RED + "!!!" + Fore.RESET + " - New var file created for " + target + " by " + nick)
                    c.whisper("VAR file successfully created for " + target, nick)
                else:
                    action_log.info(Fore.RED + "!!!" + Fore.RESET + " - Var file creation failed - " + nick)
                    c.whisper("VAR file failed to create for " + target, nick)
                    
            elif cmd[0] == "getvar":
                response = v.getvar( cmd[1], cmd[2])
                c.whisper("VAR: %s = %s" % (cmd[2], response),nick)
                    
            elif cmd[0] == "listvar":
                response = v.listvar(cmd[1])
                c.whisper(response, nick)
                
            elif cmd[0] == "setvar":
                if(v.setvar(cmd[1], cmd[2], int(cmd[3]))):
                    c.whisper("VAR: %s set to %s for %s" % (cmd[2], cmd[3], cmd[1]), nick)
                else:
                    c.whisper("Setting of variable failed.", nick)
                    
            elif cmd[0] == "deletevar":
                if(v.deletevarfile(cmd[1])):
                    c.whisper("VAR file successfully deleted.", nick)
                else:
                    c.whisper("VAR file deletion failed.", nick)
                
            elif cmd[0] == "resetvar":
                target = cmd[1]
                
                if(v.deletevarfile(target)):
                    c.whisper("VAR file successfully deleted.", nick)
                else:
                    c.whisper("VAR file deletion failed.")
                    
                if(v.makevarfile(target)):
                    action_log.info(Fore.RED + "!!!" + Fore.RESET + " - New var file created for " + target + " by " + nick)
                    c.whisper("VAR file successfully created for " + target, nick)
                else:
                    action_log.info(Fore.RED + "!!!" + Fore.RESET + " - Var file creation failed - " + nick)
                    c.whisper("VAR file failed to create for " + target, nick)
                    
            elif cmd[0] == "formats" :
                c.say(vars(f))
                    
            elif cmd[0] == "cls":
                os.system("cls")
                
            elif cmd[0] == "join":
                join(nick)
                
            elif cmd[0] == "joinn":
                join(cmd[1])
                
            elif cmd[0] == "raw":
                c.raw(cmd[1:])
                    
                
        else:
            c.whisper("Unknown command, or you don't have permission.", nick)
        
    except:
        # any and every error will throw this
        traceback.print_exc()
        c.whisper("I didn't understand that. Please contact an admin for help.",nick)

"""
Main loop, everything happens through this loop
Data received from s is placed in the readbuffer, which is then split into
lines that are iterated over as incoming messages.
Returning false will close Oracle, and true will reload oracle.py
"""       
def mainloop(s, config):
    
    # get the loggers
    receive_log = logging.getLogger('receive')
    action_log = logging.getLogger('action')
        
    readbuffer = ""
    
    global do_reload
    global do_exit
    do_reload = do_exit = False
    
    while True:
        try:
            # get messages from the server
            readbuffer = readbuffer + s.recv(1024)
        except:
            # this only happens when the server throttles the connection
            action_log.info(Fore.RED + "THR" + Fore.RESET + " Cannot connect, throttled by server.")
            action_log.info(Fore.RED + "THR" + Fore.RESET + " Will try again in 20 seconds...")
            time.sleep(20)
            break
            
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            line = string.split(string.rstrip(line))
            message = " ".join(line)
                 
            # reply to every periodic PING event
            if(line[0] == "PING"): 
                c.ping(line[1])
                
            # join the channel
            elif(line[1] == "376" and line[2] == config['ident']): 
                c.join()
                
            # identify with nickserv after being prompted
            elif("NickServ!" in line[0] and line[4] == "nickname"):
                c.identify()
                action_log.info(Fore.GREEN + "!!! " + Fore.WHITE + "Identified")
                
            # return of NAMES list
            elif(line[1] == "353"): 
                c.say("".join(message.split(":")[2].replace("@","").replace("+","").replace("Oracle ","")))
                
            # realise that Orace just joined, say welcome
            elif("JOIN" in line) and ("Oracle" in message):
                # if welcome-message == false
                if not config['welcome-message']:
                    pass
                else:
                    c.say(format.replace(config['welcome-message']))
                
            # throw nick to join() after they join
            elif ("JOIN" in line or ":JOIN" in line) and not ("Oracle" in message):
                join(line[0].split(":",1)[1].split("!",1)[0])
            
            # possible 'line(s)'
            # ':Foo!foo@bar.com', 'PRIVMSG', '#rapid', ': [message]'
            # ':Foo!foo@bar.com', 'PRIVMSG', 'Oracle', ': [message]'
            # ':nova.esper.net', 'NOTICE', '*' ':***', 'foo', 'is', 'bar'
            # 'PING', ':nova.esper.net'
            # ':ChanServ!ChanServ@bar.com', 'MODE', '#rapid', '+o', 'Oracle'
            # ':nova.esper.net', '001', 'Oracle', '[thing]'
            
            if (len(line) > 2):     
                # grab nick from first string in line
                # grab message from fourth string onwards
                try:
                    nick = line[0].replace(":","").split("!",1)[0]
                    msg = " ".join(line[3:]).replace(":","",1)
                except:
                    nick = "null"
                    break
                
                receive_log.info(Fore.CYAN + "MSG" + Fore.RESET + " <" + nick + "> " + msg)
            else:
                # the message is bad
                break
                
            # reset variable that tells connect if it is a
            # message from a server bot
            if c.getactive():
                c.set_inactive()
                
            # check if the nick is one of the RapidIRC bots
            # change nick and msg accordingly
            for bot in config['server-bots']:
                if nick == bot and msg.startswith("<"):
                    nick, msg = msg.split("<",1)[1].split("> ",1)
                    c.set_active(bot)
            
            # throw msg and nick to spamhandler
            if config['spam-handler']:
                if not c.getactive():
                    spamhandler.handler(nick, msg) 

            # handle sudo commands
            if msg.startswith(config['sudo-char']) and v.getrank(nick) >= 4:
                msg = msg.replace(config['sudo-char'],"")
                nick, msg = msg.split(" ",1)

            # identify commands from msg
            for char in config['command-chars']:
                if msg.startswith(char):
                    msg = msg.lower().replace(char,"")
                    processcmd(nick, msg)

            # throw msg to translator
            if config['translate']:
                if translate.requires_translate(msg):
                    action_log.info("TRN Translating...")
                    c.say("I think you mean: " + translate.translate_result(msg))

            # throw msg and nick to gags
            if config['say-responses']:
                gags.get_response(nick, msg)
  
            # check and handle youtube links
            if config['youtube-links']:
                if(msg.startswith("http://www.youtube.com/")):
                    try:
                        author, title = youtube.processlink(msg)
                        c.say(f.BOLD + f.RED + "YouTube Video" + f.BOLD + f.WHITE + " - " + title + " by " + author)
                    except:
                        c.say(f.BOLD + f.RED + "Youtube video failed" + f.BOLD + f.WHITE + " - 404 Not Found")
            
            if do_reload:
                return True
            if do_exit:
                return False

"""
Main function, initiates code
Probably doesn't have to be here but I'm too lazy
to fix this kind of thing
"""
def main(s, c):
    return mainloop(s, c)