# -*- coding: utf-8 -*-

"""
~ ?Oracle Bot v1.0.0 ~ 
written by Toofifty, primarily for use of the Rapid Minecraft Server IRC
http://rapidcraftmc.com/
http://www.reddit.com/r/rapid/
#rapid on irc.esper.net

"""

import string
import traceback
import time
import os
import yaml
import json
import urllib
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
import misc
import translate
import gags
import logger
import games
import base
import input
import score
import threads
from base import *
    
rps = None
t = None
trivia = None
spam = None
attention = False
ignore_list = []
acc_checked = False


"""
Reload all modules except for oracle.py, connect.py and run.py
connect.py and run.py cannot be reloaded without restarting the bot,
and oracle.py needs to be reloaded from outside this module (run.py)
"""
def rl():
    if spam != None:
        spam.disable()
    if trivia != None:
        trivia.disable()

    modules = [
        m, e, v, n, youtube, cleverbot, spamhandler,
        format, misc, translate, gags, logger, games,
        base, input, score, threads,
        ]
        
    for mod in modules:
        reload(mod)
        
    global do_reload
    do_reload = True
    
def custom_str_constructor(loader, node):
    return loader.construct_scalar(node).encode('utf-8')
    
yaml.add_constructor(u'tag:yaml.org,2002:str', custom_str_constructor)

"""
Prints the commands and help list to the user
"""
def helpc(nick, args):
    rank = v.getrank(nick)
    
    with open('help.yml', 'r') as help_file:
        help = yaml.load(help_file)
        
    ranks = {'dev': 4, 
        'formats': 4,
        'admin': 3, 
        'ranks': 2, 
        'other': 1,
        'personal': 1,
        'server': 1,
        'emotes': 1,
        'default': 1,
        'categories': 1,
        }
        
    try:
        if help.has_key(args.lower()):
            if rank >= ranks[args.lower()]:
                c.whisper(f.BLUE + "~ " + f.BOLD + args.title() + f.BOLD + " ~", nick)
                sorted_list = sorted(help[args.lower()]) 
                for command in sorted_list:
                    list = help[args.lower()][command]
                    if list.has_key('args'):
                        c.whisper(f.WHITE + "- " + f.CYAN + "" + command.upper().strip('123') + " " + list['args'] + f.WHITE + " > " + list['desc'], nick)
                    else:
                        c.whisper(f.WHITE + "- " + f.CYAN + "" + command.upper().strip('123') + f.WHITE + " > " + list['desc'], nick)
            else:
                raise Warning
        elif args.lower() != "no":
            done = False
            for set in help:
                if rank >= ranks[set]:
                    for command in help[set]:
                        if str(command).startswith(args.lower()):
                            list = help[set][command]
                            if list.has_key('args'):
                                c.whisper(f.WHITE + "- " + f.CYAN + "" + command.upper().strip('123') + " " + list['args'] + f.WHITE + " > " + list['desc'], nick)
                            else:
                                c.whisper(f.WHITE + "- " + f.CYAN + "" + command.upper().strip('123') + f.WHITE + " > " + list['desc'], nick)
                            done = True
            if not done:
                raise Warning
        # else:
            # raise Warning
    except:
        traceback.print_exc()
        for line in help['default']:
            c.whisper(format.replace(line), nick)
        c.whisper(format.replace(help['categories'][int(rank)]), nick)
 
"""
Asks cleverbot a question, and logs and says the response (broken)
Cleverbot API has been discontinued and so will probably no longer work
"""
def cb(ask, nick):
    if config.get('cleverbot'):
        cbot = cleverbot.Session()
        response = cbot.Ask(" ".join(ask))
        action_log.info(Fore.CYAN + "CBT" + Fore.RESET + " " + response)
        c.say(nick + ": " + response)
    else:
        c.whisper("Cleverbot is currently disabled.", nick)
        
"""
Check if a user is whitelisted through Jake's MetisWeb database
"""
def iswhitelisted(nick):
    try:
        content = urllib.urlopen(config.get('whitelist-location'))
        data = json.load(content)
        print data
        for name in data:
            action_log.info(name)
            if name == nick:
                return True
        return False
    except:
        traceback.print_exc()
        return False
        
def confirm_account(nick):
    acc_checked = True
    if config.get('use-json-whitelist'):
        if not iswhitelisted(nick):
            c.say("Kicking user: " + nick + ". Reason: Not on the whitelist.")
            #c.kick(nick, "NotWhitelisted")
        else:
            c.say(nick + " is whitelisted.")

"""
Actions to perform on user join
"""
def join(nick):
    rank = v.getrank(nick)    
    if not v.listvar(nick) and config.get('auto-add'):
        v.makevarfile(nick)
        
    c.raw("WHOIS " + nick)
    acc_checked = False
    
    if config.get('join-message'):
        c.whisper(f.LIGHTBLUE + "Welcome to the Rapid IRC, " + f.PURPLE + nick + f.LIGHTBLUE + ".", nick)
    
    if rank == 0 and config.get('auto-kick'):
        c.kick(nick, "NotWhitelisted")
        
    elif rank >= 3:
        if config.get('auto-op'):
            c.mode(["+o", nick])
            c.whisper("You have been opped by Oracle", nick)
        else:
            c.whisper("Oracle auto-op is disabled. Identify with NickServ to receive op.", nick)
            
    else:
        c.mode(["+v", nick])
       
    if config.get('check-mail'):
        if not m.check(nick):
            c.whisper("You have no new mail.", nick)
        else:
            c.whisper("You have mail! Use '?mail check' to see.", nick)
        
    action_log.info(Fore.BLUE + "JNC" + Fore.RESET + " " + nick + " joined. Rank: " + str(rank))    
    
"""
Splits the message, processes the commands and does all the relevant
functions required. Should reverse the 'rank' if statements but it's
not much of a problem.
"""
def processcmd(nick, msg):    
    cmd = msg.split(" ")
    rank = v.getrank(nick)
    if len(cmd) == 1:
        action_log.info(Fore.MAGENTA + "CMD" + Fore.RESET + " " + cmd[0] + " | nick: " + nick)
    else:
        action_log.info(Fore.MAGENTA + "CMD" + Fore.RESET + " " + cmd[0] + " | args: " + " ".join(cmd[1:]) + " | nick: " + nick)
    
    try:
        # regular user
        # rank = 1
        if rank >= 1:
            #! emotes !#
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
            
            #! other !#
            elif cmd[0] == "rps":
                target = cmd[1]
                global rps
                rps = games.rps(nick, target)
                c.whisper(nick + " has challenged you to a game of rock, paper scissors.", target)
                c.whisper("To participate, use " + f.BLUE + "/msg Oracle ?[rock/paper/scissors] (use /imsg if you're in-game)", target)
                c.whisper("You have 30 seconds.", target)
                c.whisper("You have challenged " + target + " to a game of rock, paper scissors.", nick)
                c.whisper("To participate, use " + f.BLUE + "/msg Oracle ?[rock/paper/scissors] (use /imsg if you're in-game)", nick)
                c.whisper("You have 30 seconds.", nick)
                
            
            elif cmd[0] == "rock" or cmd[0] == "paper" or cmd[0] == "scissors":
                if rps != None:
                    if rps.guess(cmd[0], nick):
                        c.whisper("Decision accepted", nick)
                        c.whisper("Your opponent has made a decision", rps.get_opponent(nick))
                    else:
                        c.whisper("You're not in this RPS game!", nick)
                else:
                    c.whisper("There is no RPS game at the moment.", nick)
                    
            elif cmd[0] == "a":
                global trivia
                trivia.guess(cmd[1:], nick)
            
            elif cmd[0] == "help" or cmd[0] == "what":
                if(len(cmd) < 2): helpc(nick, "no")
                else: helpc(nick, cmd[1])
                
            elif cmd[0] == "cb": cb(cmd[1:], nick)
            
            elif cmd[0] == "pick":
                c.say(nick + ": " + misc.pick(cmd[1:]))
                
            elif cmd[0] == "diamonds":
                if config.get('rick-roll'):
                    gags.rick_roll(nick, cmd[1])
                else:
                    c.whisper(f.WHITE + "64 diamonds have been credited to the Minecraft account " + f.RED + nick + f.WHITE + ".", nick)
                    time.sleep(5)
                    c.whisper("Just kidding.", nick)
                    c.whisper("This command has been disabled in the config.", nick)
                    
            elif cmd[0] == "ayylmao":
                c.say("http://puu.sh/6wo5D.png")
                
            elif cmd[0] == "score":
                if cmd[1] == "check":
                    if len(cmd) > 2 and rank >= 3:
                        c.whisper(cmd[2] + " has " + str(score.get(cmd[2])) + " points.", nick)
                    else:
                        c.whisper("Your have " + str(score.get(nick)) + " points.", nick)
                elif cmd[1] == "top":                        
                    list = score.get_leader_boards()
                    amount = int(cmd[2]) if len(cmd) > 2 else 5
                    i = 1
                    for line in list:
                        c.whisper(str(i) + ". " + line[0] + " - " + str(line[1]), nick)
                        i += 1
                        if i > amount:
                            break
                
            #! server !#
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
      
            #! personal !#
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
        else:
            c.whisper("Seems like you don't have access to these commands. Message an admin for help.", nick)
            
        #! moderator !#
        # rank = 2
        if rank >= 2:
            if cmd[0] == "say":
                c.say(format.replace(" ".join(cmd[1:])))
            
            elif cmd[0] == "attention":
                global attention
                attention = True
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
        
        #! admin !#
        # rank = 3
        if rank >= 3:
            if cmd[0] == "close":
                c.stop(nick)
                do_exit = True
                
            elif cmd[0] == "restart" :
                c.restart(nick)
                
            elif cmd[0] == "reload":
                action_log.info(Fore.RED + "RLD" + Fore.RESET + " Reload issued by " + nick)
                rl()
                c.say(f.YELLOW + "Reload complete.")
                
            elif cmd[0] == "sreload":
                rl()
                c.whisper(f.YELLOW + "Silent reload complete.", nick)
                
            elif cmd[0] == "setrank":
                v.setvar(cmd[1], "rank", int(cmd[2]))
                c.whisper(cmd[1] + "'s rank set to " + cmd[2] + ".", nick)
                
            elif cmd[0] == "mode":
                c.mode(cmd[1:])
                
            elif cmd[0] == "getrank":
                c.whisper(cmd[1] + "'s rank is " + str(v.getvar(cmd[1], "rank")) + ".", nick)
                
            elif cmd[0] == "flood":
                if cmd[1] == "reset":
                    spam.clear()
                    c.whisper("Cleared FLOOD dictionary", nick)
                elif cmd[1] == "decrement":
                    spam.decrement()
                    c.whisper("FLOOD decrement performed", nick)
                    
            elif cmd[0] == "randompoints":
                if cmd[1] == "run":
                    randompoints.poll_users()
                    time.sleep(1)
                    randompoints.reward()
                
            elif cmd[0] == "trivia":
                if cmd[1] == "new":
                    c.say("[" + f.PURPLE + "Trivia" + f.WHITE + "] New round started by " + f.BLUE + nick)
                    trivia._runnable()
                elif cmd[1] == "off":
                    trivia.disable()
                    c.say("[" + f.PURPLE + "Trivia" + f.WHITE + "] Disabled by " + f.BLUE + nick)
                elif cmd[1] == "on":
                    if trivia._getdisabled():  
                        del trivia
                        trivia = games.trivia()
                        c.say("[" + f.PURPLE + "Trivia" + f.WHITE + "] Re-enabled by " + f.BLUE + nick)
                elif cmd[1] == "info":
                    c.whisper(trivia.getinfo(), nick)
                    
            elif cmd[0] == "score":
                if cmd[1] == "reset":
                    if score.reset(cmd[2]):
                        c.whisper("Successfully reset " + cmd[2] + "'s score.", nick)
                    else:
                        c.whisper("Reset failed.", nick)
                elif cmd[1] == "add":
                    points = score.add(cmd[2], cmd[3])
                    if not points:
                        c.whisper("Points failed to add.", nick)
                    else:
                        c.whisper("Sucessfully added points, " + cmd[2] + " now has " + str(points) + " points.", nick)
                        
            elif cmd[0] == "ignore":
                try:
                    ignore_list.append(cmd[1])
                    c.whisper("Successfuly added " + cmd[1] + " to ignore list.", nick)
                except:
                    c.whisper("Ignore unsuccessful.", nick)
                
            elif cmd[0] == "pardon":
                try:
                    del ingore_list[cmd[1]]
                    c.whisper("Successfully pardoned " + cmd[1] + ".", nick)
                except:
                    c.whisper("Pardon unsuccessful. Perhaps " + cmd[1] + " is not currently being ignored.", nick)
                        
        #! developer !#
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
                
            elif cmd[0] == "config":
                if cmd[1] == "reload":
                    try:
                        config.reload()
                        c.whisper("Config reloaded.", nick)
                    except:
                        traceback.print_exc()
                        c.whisper("Error reloading config", nick)
                elif cmd[1] == "set":
                    try:
                        config.set(cmd[2], cmd[3:])
                        c.whisper("Config set.", nick)
                    except:
                        traceback.print_exc()
                        c.whisper("Error setting config", nick)
                elif cmd[1] == "get":
                    try:
                        c.whisper(config.get(cmd[2]), nick)
                    except:
                        traceback.print_exc()
                        c.whisper("Error getting config", nick)
                        
        
    except:
        # any and every error will throw this
        traceback.print_exc()
        c.whisper("Oops! Something went wrong. Please contact an admin for help.",nick)

"""
Main loop, everything happens through this loop
Data received from s is placed in the readbuffer, which is then split into
lines that are iterated over as incoming messages.
Returning false will close Oracle, and true will reload oracle.py
"""       
def mainloop(s, config):
    readbuffer = ""
    
    global do_reload
    global do_exit
    do_reload = do_exit = False
    
    if config.get('trivia'):
        global trivia
        trivia = games.trivia()
        
    if config.get('command-line'):
        global commandline
        commandline = input.cmd()
        
    if config.get('random-points'):
        global randompoints
        randompoints = games.rp()
        
    
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
            elif(line[1] == "376" and line[2] == config.get('ident')): 
                c.join()
                
            # identify with nickserv after being prompted
            elif("NickServ!" in line[0] and line[4] == "nickname"):
                c.identify()
                action_log.info(Fore.GREEN + "!!! " + Fore.WHITE + "Identified")
                
            # return of NAMES list
            elif(line[1] == "353"): 
                nicks = "".join(message.split(":")[2].replace("@","").replace("+","").replace("Oracle ",""))
                global attention
                if attention:
                    c.say(nicks)
                    attention = False
                users = nicks.replace(config.get('server-bots')[0],"").replace(config.get('server-bots')[1],"")
                if config.get('random-points'):
                    randompoints.add_users(users)
                
            # realise that Orace just joined, say welcome
            elif("JOIN" in line) and ("Oracle" in message):
                # if welcome-message == false
                if not config.get('welcome-message'):
                    pass
                else:
                    c.say(format.replace(config.get('welcome-message')))
                
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
                
            # reply from WHOIS
            if "is logged in as" in msg and ".esper.net" in nick:
                confirm_account(msg.split(" ",2)[1])
                
            # reset variable that tells connect if it is a
            # message from a server bot
            if c.getactive():
                c.set_inactive()
            
            # throw msg and nick to spamhandler
            if config.get('spam-handler'):
                if spam == None:
                    global spam
                    spam = spamhandler.handler()
                sh = True
                for bot in config.get('server-bots'):
                    if nick == bot:
                        sh = False
                if nick == config.get('nick'):
                    sh = False
                if sh:
                    spam.increment(nick, msg) 
                
            # ignore list doesn't work properly, but meh
            if not nick in ignore_list or nick == 'Toofifty':
                # check if the nick is one of the RapidIRC bots
                # change nick and msg accordingly
                for bot in config.get('server-bots'):
                    if nick == bot:
                        if msg.startswith("<"):
                            nick, msg = msg.split("<",1)[1].split("> ",1)
                            c.set_active(bot)
                            
                        elif msg.split(" ")[1] == "whispers":
                            nick, msg = msg.split(" whispers ", 1)
                            c.set_active(bot)
                            
                        elif msg.startswith("Online Players:"):
                            users = msg.replace("Online Players:", "")
                            if not users == "":
                                randompoints.add_users(users)

                # handle sudo commands
                if msg.startswith(str(config.get('sudo-char'))) and v.getrank(nick) >= 4:
                    msg = msg.replace(config.get('sudo-char'),"")
                    nick, msg = msg.split(" ",1)

                # identify commands from msg
                for char in config.get('command-chars'):
                    if msg.startswith(char):
                        # make sure to only get rid of one '?'
                        msg = msg.split(char, 1)[1]
                        processcmd(nick, msg)

                # throw msg to translator
                if config.get('translate'):
                    if translate.requires_translate(msg):
                        action_log.info("TRN Translating...")
                        c.say("I think you mean: " + translate.translate_result(msg))

                # throw msg and nick to gags
                if config.get('say-responses'):
                    gags.get_response(nick, msg)
      
                # check and handle youtube links
                if config.get('youtube-links'):
                    if(msg.startswith("http://www.youtube.com/")):
                        try:
                            author, title = youtube.processlink(msg)
                            c.say(f.BOLD + f.RED + "YouTube Video" + f.BOLD + f.WHITE + " - " + title + " by " + author)
                        except:
                            c.say(f.BOLD + f.RED + "Youtube video failed" + f.BOLD + f.WHITE + " - 404 Not Found")
            
            # tell run.py to reload or exit
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