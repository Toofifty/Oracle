import core.oracle
import core.connect
import core.logger
import traceback
import sys

def run():

    core.logger.create_loggers()

    try:
        s, c = core.connect.start()
    except:
        sys.exit("There was an error connecting to the server.")
        
    while True:
        try:
            rel = core.oracle.main(s, c)
            if rel:
                reload(core.oracle) 
                print("!!! - Reload complete")
            else:
                print("Process quit.")
        except:
            traceback.print_exc()
            
run()