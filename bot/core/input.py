import oracle

from threads import ParallelThread
from connect import say
from base import ACTION_LOG, config
from format import replace

class CommandLine(ParallelThread):
    """ Allows input of commands through
    the terminal window in a separate thread
    rather than only though IRC commands.
    
    """
    def __init__(self):
        ParallelThread.__init__(self)
        ACTION_LOG.info("Command line initialized")
        self.start()
        
    def _runnable(self):
        nick = 'Oracle'
        while True:
            msg = replace(raw_input())
            cmd = False
            for char in config.get('command-chars'):
                    if msg.startswith(char):
                        # make sure to only get rid of one '?'
                        msg = msg.split(char, 1)[1]
                        oracle.process_cmd(nick, msg)
                        cmd = True
            if not cmd:
                say(msg)
