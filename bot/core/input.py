from threads import ParallelThread
from connect import say
from base import *
import oracle

class cmd(ParallelThread):
    def __init__(self):
        ParallelThread.__init__(self)
        action_log.info("Command line initialized")
        self.start()
        
    def _runnable(self):
        nick = 'Oracle'
        while True:
            msg = format.replace(raw_input())
            cmd = False
            for char in config.get('command-chars'):
                    if msg.startswith(char):
                        # make sure to only get rid of one '?'
                        msg = msg.split(char, 1)[1]
                        oracle.processcmd(nick, msg)
                        cmd = True
            if not cmd:
                say(msg)