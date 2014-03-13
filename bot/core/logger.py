import logging
import connect
from colorama import init, Back
init(autoreset=True)

from base import config
        
def create_loggers():
    loggers = [
        'receive',
        'send',
        'action'
        ]
        
    for l in loggers:
        if config.get('chat-log'):
            logging.basicConfig(filename='chat_log.txt')

        # create logger
        logger = logging.getLogger(l)
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        
        if config.get('mode').lower() == 'debug':
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        
        # create formatter
        formatter = logging.Formatter(fmt=config.get('console-format'),datefmt=Back.BLUE + config.get(l + '-format') + Back.RESET)
        
        # add formatter to console
        console.setFormatter(formatter)
        
        # add console to logger
        logger.addHandler(console)
            
        logger.debug(l + ' logger initiated.')
