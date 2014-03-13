import math
import random

def netherposition(x, y, z):
    return math.floor(x/8), y, math.floor(z/8)
    
def overworldposition(x, y, z):
    return x*8, y, z*8
    
def pick(args):
    choice = random.randint(1, len(args)) - 1
    return args[choice]
    
def get_poll_results(poll):
    pass

class Poll:
    def __init__(self, options):
        # Transfer options list to dict so
        # we can give them values
        self.options = {}
        for o in options:
            self.options[o] = 0
        
    def vote(self, choice, nick):
        pass
        
    def _add_vote(self, choice):
        pass
        
    def check_votes(self):
        pass
        
    def finish(self):
        pass
        
    def save(self):
        pass
    
class ShortPoll(Poll):
    """ Poll class, ready and
    rearing to go
    
    """
    def __init__(self, options, time=30):
        Poll.__init__(self, options)
        
    def vote(self, choice):
        pass
        
    def finish(self):
        pass

class ExtendedPoll(Poll):
    """OP/Admin only poll, useful for
    polling events and such.
    
    Poll times are in days and not seconds
    unlike ShortPolls.
    """
    def __init__(self):
        Poll.__init__(self, options)