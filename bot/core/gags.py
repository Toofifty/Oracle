# -*- coding: utf-8 -*-

import time

import connect as c
from varcontrols import getrank
from misc import pick
from base import f

def get_response(nick, message):
    if(message.lower() == "nope nope"):
        c.say("nope.avi - http://www.youtube.com/watch?v=gvdf5n-zI14")

    elif(message.lower() == "nice"):
        c.say("nice - http://www.youtube.com/watch?v=jjtkMCLRf-M")

    elif(message.lower() == "alrighty then"):
        c.say("alrighty then - http://www.youtube.com/watch?v=hS1okqbnePQ")

    elif(message.lower() == "noice"):
        c.say("noice - http://www.youtube.com/watch?v=rQnYi3z56RE")

    elif(message.lower() == "sad"):
        c.say("sad - http://www.youtube.com/watch?v=CwK74w4VwgQ")

    elif(message.lower() == "hello my baby"):
        c.say("hello my baby - http://www.youtube.com/watch?v=49EoV50oba0")

    elif(message.lower() == "thanks oracle"):
        c.say(pick(("No worries mate!","No problem!","T'was a pleasure.","You're welcome!")))

    elif(message.lower() == "nice work oracle" or message.lower() == "well done oracle" or message.lower() == "good job oracle"):
        c.say(pick(("Thanks man!","Thanks, appreciate it.","Why, thank you sir!")))

    elif(message.lower() == "bye" or message.lower() == "later" or message.lower() == "cya" or message.lower() == "brb"):
        c.say(pick(("Ciao!","Adios!","Tsch�ss!","Despedida!","Hasta la Vista!","Au Revoir!","Farewell!","Cya!")))

    elif(message.lower().startswith('should ') and '?' in message):
        c.say(pick(('Yes.','No.','It depends.','Please ask again.','No, fuck you')))
        
    elif(message.lower().startswith('will ') and '?' in message):
        c.say(pick(('Of course!','Never.','No.','Yes.','Maybe.','Impossible.','Never going to happen, buster.')))
        
    elif('fuck' in message.lower() and 'you' in message.lower() and 'oracle' in message.lower()):
        c.say(pick(('That\'s not very nice!','Fuck you too, my good sir!','Come at me bro!','Do you want a punch-on?!')))
        
    elif("alrighty" in message):
        c.say("Alrightyroo")

    elif(message.lower() == "welcome"):
        c.say("Welcome " + nick + " to the server!")

    elif(message.lower() == "oracle"):
        c.say("Yes?")

    elif(message.lower() == "oh sweet baby jesus"):
        c.say("http://gfycat.com/ScientificUnawareAmericanwigeon")

def rick_roll(nick, name):
    if not v.getrank(nick) == 4:
        name = nick

    c.whisper("Well done, " + nick + ".", nick)

    rickroll = [
        "We're no strangers to love",
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
        if nick == "Manyman":
            c.whisper("< " + name + " > " + f.random() + line, nick)
        else:
            c.say("< " + name + " > " + f.random() + line)

        time.sleep(2)

    c.say(f.PINK + "This Rick-Roll brought to you by " + f.CYAN + nick + f.PINK + ".")
