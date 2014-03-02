import format
import logging
import yaml
    
f = format.formats()
receive_log = logging.getLogger('receive')
action_log = logging.getLogger('action')
send_log = logging.getLogger('send')

class config:
    def __init__(self):
        self.load()
        
    def load(self):
        with open('config.yml', 'r') as conf_file:
            self.data = yaml.load(conf_file)
        action_log.debug("!!! - Config loaded")
        
    def set(self, key, value):
        self.data[key] = value
        with open('data.yml', 'w') as o:
            o.write( yaml.dump(self.data, default_flow_style=False) )
            
    def reload(self):
        del self.data
        self.load()
        
    def get(self, key):
        return self.data[key]
        
config = config()