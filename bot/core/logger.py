import logging
import connect
from colorama import init, Back
init(autoreset=True)
        
def create_loggers():
    loggers = [
        'receive',
        'send',
        'action'
        ]
        
    c = connect.loadconfig()
        
    for l in loggers:
        if c['chat-log']:
            logging.basicConfig(filename='chat_log.txt')

        # create logger
        logger = logging.getLogger(l)
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        
        if c['mode'].lower() == 'debug':
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        
        # create formatter
        formatter = logging.Formatter(fmt=c['console-format'],datefmt=Back.BLUE + c[l + '-format'] + Back.RESET)
        
        # add formatter to console
        console.setFormatter(formatter)
        
        # add console to logger
        logger.addHandler(console)
            
        logger.debug(l + ' logger initiated.')