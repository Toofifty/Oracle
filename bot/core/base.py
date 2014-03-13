import format
import logging
import yaml
    
f = format.Formats()
RECEIVE_LOG = logging.getLogger('receive')
ACTION_LOG = logging.getLogger('action')
SEND_LOG = logging.getLogger('send')

class Config:
    def __init__(self):
        self.load()
        
    def load(self):
        with open('config.yml', 'r') as conf_file:
            self.data = yaml.load(conf_file)
        ACTION_LOG.debug("!!! - Config loaded")
        
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