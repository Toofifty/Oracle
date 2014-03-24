'''
Oracle - Spam Handler
~ Toofifty 
'''
import traceback
from colorama import init, Fore, Back, Style
init(autoreset=True)

import connect
from base import config, log, f
from threads import LoopTimeThread
    
class Handler:
    def __init__(self):
        self.FLOOD = {}
        self.last_msg = ""
        self.thread = LoopTimeThread(config.get('interval'), self)
        self.thread.start()
        self.disabled = False
        
    def _runnable(self):
        self.decrement()
        
    def _getdisabled(self):
        return self.disabled
        
    def disable(self):
        self.disabled = True
        
    # Add one to nick's flood amount
    def increment(self, nick, msg):
        if 'esper.net' in nick:
            return False
        if not self.FLOOD.has_key(nick):
            self.FLOOD[nick] = 1
            
        elif msg == self.last_msg:
            self.FLOOD[nick] += 2
            
        else:
            self.FLOOD[nick] += 1
            
        self.handle(nick, self.FLOOD[nick])
        return True
            
    def clear_empties(self):
        for nick, val in self.FLOOD:
            if val == 0:
                del self.FLOOD[nick]
                
    def clear(self):
        self.FLOOD = {}
                
    def decrement(self):
        try:
            keys = self.FLOOD.keys()
            for nick in keys:
                self.FLOOD[nick] -= 1
                if self.FLOOD[nick] == 0:
                    del self.FLOOD[nick]
            
            say = False
            for nick, val in self.FLOOD.iteritems():
                log(nick + ': ' + str(val), m_type='SPAMHANDLR') 
                #ACTION_LOG.info(Style.BRIGHT + Fore.BLUE + 'SPAMHDLR ' + Fore.RESET + nick + ': ' + str(val))
                say = True
            if say:
                log('Decremented FLOOD dict', m_type='SPAMHANDLR')
                #ACTION_LOG.info(Style.BRIGHT + Fore.BLUE + 'SPAMHDLR ' + Fore.RESET + ' Decremented FLOOD dict')
                
        except:
            traceback.print_exc()
        
    def handle(self, nick, val):
        if val > config.get('kick'):
            connect.kick(nick, "Spamming")
            connect.say(f.YELLOW + 'User ' + f.RED + nick + f.YELLOW + ' was kicked for spamming.')
            log('User: ' + nick + ' was kicked for spamming', m_type='SPAMHANDLR', reset=False)
            #ACTION_LOG.info(Fore.RED + 'KCK' + Fore.RESET + ' User: ' + nick + ' was kicked for spamming')
            del self.FLOOD[nick]
            
        elif val > config.get('warn'):
            connect.msg(f.YELLOW + 'Please slow down with your messages, or else you\'ll be kicked.',nick)