# -*- coding: utf-8 -*-

import connect as c
import yaml
import random
import time
import score
from threads import TimeThread, LoopTimeThread, ParallelThread
from base import *

class rps:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.g1 = "none"
        self.p2 = p2.title()
        self.g2 = "none"
        self.start_timer(30)
        self.done = False
        
    def get_opponent(self, player):
        if player == self.p1:
            return self.p2
        else:
            return self.p1
        
    def start_timer(self, time):
        self.t = TimeThread(time, self)
        self.t.start()
        
    def guess(self, guess, nick):
        if nick == self.p1:
            self.g1 = guess
            guess = True
            
        elif nick.lower() == self.p2.lower():
            self.g2 = guess
            guess = True
        
        if guess:
            if self.g1 != "none" and self.g2 != "none":
                self._runnable()
                self.t.cancel()
            return True
        return False
        
    def get_done(self):
        return self.done
        
    def _runnable(self):
        text = self.result()
        c.say(self.p1 + ": " + self.g1 + ", " + self.p2 + ": " + self.g2)
        c.say(f.YELLOW + text)
        
    def result(self):
        points = config.get('rps-points')
        strp = str(points)
        if self.g1 == "rock":
            if self.g2 == "rock":
                return "Tie!"
            elif self.g2 == "paper":
                score.add(self.p2, points)
                return self.p2 + " wins! +" + strp
            elif self.g2 == "scissors":
                score.add(self.p1, points)
                return self.p1 + " wins! +" + strp
                
        elif self.g1 == "paper":
            if self.g2 == "rock":
                score.add(self.p1, points)
                return self.p1 + " wins! +" + strp
            elif self.g2 == "paper":
                return "Tie!"
            elif self.g2 == "scissors":
                score.add(self.p2, points)
                return self.p2 + " wins! +" + strp
                
        elif self.g1 == "scissors":
            if self.g2 == "rock":
                score.add(self.p2, points)
                return self.p2 + " wins! +" + strp
            elif self.g2 == "paper":
                score.add(self.p1, points)
                return self.p1 + " wins! +" + strp
            elif self.g2 == "scissors":
                return "Tie!"
                
        self.done = True        
        return "Somebody didn't decide!"
        
class trivia:
    def __init__(self):
        self.questions = self.load_trivia()
        self.current = ""
        self.trivia_time = LoopTimeThread(config.get('trivia-interval'), self)
        self.trivia_time.start()
        self.f = f.WHITE + "[" + f.PURPLE + "Trivia" + f.WHITE + "] "
        self.disabled = False
        action_log.info("Trivia initialized")
        
    def load_trivia(self):
        with open('../bot/trivia.yml', 'r') as triv:
            c = yaml.load(triv)
        return c
        
    def get_question(self):
        return random.choice(self.questions.keys())
            
    def get_answer(self):
        for k, v in self.questions.iteritems():
            if k == self.current:
                return str(v).lower()
        
    def guess(self, guess, nick):
        if self.check(guess):
            c.say(self.f + nick + " got the answer! +" + str(config.get('trivia-points')) + " points!")
            self.current = ""
            score.add(nick, config.get('trivia-points'))
        else:
            c.whisper(self.f + "Incorrect!", nick)
        
    def check(self, guess):
        g = str(" ".join(guess))
        for k, v in self.questions.iteritems():
            if k == self.current:
                if g.lower() == str(v).lower():
                    return True
        return False
        
    def disable(self):
        self.disabled = True
        
    def getinfo(self):
        n = 0
        for k in self.questions:
            n += 1
        int = config.get('trivia-interval')
        return self.f + "Time interval: " + str(int) + " seconds (" + str(int/60) + " minutes), " + str(n) + " questions listed."
        
    def _getdisabled(self):
        return self.disabled
        
    def _runnable(self):
        if not self.current == "":
            c.say(self.f + "Nobody got it! New round.")
        self.current = self.get_question()
        self.answer = self.get_answer()
        c.say(self.f + self.current + " (" + str(len(self.answer.split(" "))) + ")")
        c.say(self.f + "Use ?a [answer] to answer")
        
class rp(ParallelThread):
    def __init__(self):
        ParallelThread.__init__(self)
        action_log.info("Random points initialized")
        self.users = []
        self.start()
        
    def add_users(self, users):
        userlist = users.strip("\x0f").strip(" ").split(" ")
        for user in userlist:
            if not user in self.users:
                self.users.append(user)
                
    def poll_users(self):
        c.say("~players")
        c.getusers()
        
    def _runnable(self):
        while True:
            self.sleep()
            self.reward()  

    def reward(self):
        self.poll_users()
        for user in self.users:
            score.add(user, config.get('random-points'))
        c.say("Random giveaway of points! " + str(config.get('random-points')) + " points given to:")
        c.say(" ".join(self.users))
            
    def sleep(self):
        interval = random.randint(config.get('random-min-interval'),config.get('random-max-interval'))
        time.sleep(interval)
        