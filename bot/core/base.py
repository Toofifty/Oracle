import format
import logging
import yaml
from colorama import init, Fore, Back, Style
init(autoreset=True)
    
f = format.Formats()
RECEIVE_LOG = logging.getLogger('receive')
ACTION_LOG = logging.getLogger('action')
SEND_LOG = logging.getLogger('send')

def log(msg, m_type="", colour=Fore.BLUE, lg='action', l_type=0, reset=True):
    if reset:
        built_string = (Style.BRIGHT + "|" + colour + " " 
            + m_type.upper().ljust(11) + Fore.RESET + "| " + msg)
    else:
        built_string = (Style.BRIGHT + "|" + colour + " " 
            + m_type.upper().ljust(11) + Fore.RESET + "| " + colour + msg)
            
    if l_type == 0:
        logging.getLogger(lg).info(built_string)
    elif l_type == 1:
        logging.getLogger(lg).warning(built_string)
    elif l_type == 2:
        logging.getLogger(lg).debug(built_string)

class Config:
    def __init__(self):
        self.load()
        
    def load(self):
        with open('config.yml', 'r') as conf_file:
            self.data = yaml.load(conf_file)
        log("Config loaded", m_type="DEBUG", l_type=2)
        
    def set(self, key, value):
        self.data[key] = value
        with open('data.yml', 'w') as o:
            o.write( yaml.dump(self.data, default_flow_style=False) )
            
    def reload(self):
        del self.data
        self.load()
        
    def get(self, key):
        return self.data[key]
        
config = Config()