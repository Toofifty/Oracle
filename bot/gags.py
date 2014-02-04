# -*- coding: utf-8 -*-

import format as f
import connect as c

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
		c.say(misc.pick(("No worries mate!","No problem!","T'was a pleasure.","You're welcome!")))
        
	elif(message.lower() == "nice work oracle" or message.lower() == "well done oracle" or message.lower() == "good job oracle"):
		c.say(misc.pick(("Thanks man!","Thanks, appreciate it.","Why, thank you sir!")))
        
	elif(message.lower() == "bye" or message.lower() == "later" or message.lower() == "cya" or message.lower() == "brb"):
		c.say(misc.pick(("Ciao!","Adios!","Tschüss!","Despedida!","Hasta la Vista!","Au Revoir!","Farewell!","Cya!")))
        
	elif("alrighty" in message):
		c.say("Alrightyroo")
        
	elif(message.lower() == "welcome"):
		c.say("Welcome " + nick + " to the server!")
        
	elif(message.lower() == "oracle"):
		c.say("Yes?")
        
	elif(message.lower() == "oh sweet baby jesus"):
		c.say("http://gfycat.com/ScientificUnawareAmericanwigeon")