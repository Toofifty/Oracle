import logging
from colorama import init, Fore, Back, Style
init(autoreset=True)

class L(logging.Logger):
    def __init__(self, c):
        #logging.basicConfig(level=logging.DEBUG,
        #    format=c['console-format'],
        #    datefmt='' + Back.BLUE + '>> [%d/%m %H:%M:%S]' + Back.RESET + '')
        logging.Logger.__init__(self, 'main')

        if c['chat-log']:
            logging.basicConfig(filename='chat_log.txt')

        # create logger
        logger = logging.getLogger('receive')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter(fmt=c['console-format'],datefmt=Back.BLUE + c['receive-format'] + Back.RESET)
        
        # add formatter to console
        console.setFormatter(formatter)
        
        # add console to logger
        logger.addHandler(console)
        
        if c['mode'].lower() == 'debug':
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            
        logger.debug('Logger initiated.')
        
def create_loggers(c):
    loggers = [
        'receive',
        'send',
        'action'
        ]
        
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