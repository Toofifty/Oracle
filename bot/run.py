import core.oracle
import core.connect
import core.logger
import traceback
import sys

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
                reload(core.oracle) 
                print("!!!!!!!!!!!!!!!!!!! !!! Reload complete")
            else:
                core.connect.stop("Administrator")
        except Exception:
            traceback.print_exc()
            
run()