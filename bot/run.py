import core.oracle
import core.connect
import core.logger
import traceback
import sys
from time import time
from colorama import init, Fore, Back, Style
init(autoreset=True)

from core.base import log

def run():

    core.logger.create_loggers()

    try:
        socket = core.connect.start()
    except:
        sys.exit("There was an error connecting to the server.")
        
    while True:
        try:
            RELOAD = core.oracle.main(socket)
            if RELOAD:
                log("Reloading... ", m_type="RELOAD", colour=Fore.YELLOW, reset=False)
                
                time_now = time()
                reload(core.oracle) 
                new_time = time() - time_now
                
                log("Done! Completed in " + str(new_time) + "ms", m_type="RELOAD", colour=Fore.YELLOW, reset=False)
            else:
                core.connect.stop("Administrator")
                break
        except Exception:
            traceback.print_exc()
            
if __name__ == "__main__":
    run()