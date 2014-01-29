import oracle
import connect
import traceback

def run():
    try:
        s, chan = connect.start()
    except:
        sys.exit("There was an error connecting to the server.")
    w = False
    while True:
        try:
            rel = oracle.main(s, chan, w)
            if rel:
                reload(oracle) 
                print("!!! - Reload complete")
            else:
                print("Process quit.")
        except:
            traceback.print_exc()
            
run()