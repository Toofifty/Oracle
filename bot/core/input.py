from threads import ParallelThread
from connect import say
from base import *

class cmd(ParallelThread):
    def __init__(self):
        ParallelThread.__init__(self)
        action_log.info("Command line initialized")
        self.start()
        
    def _runnable(self):
        while True:
            say(format.replace(raw_input()))