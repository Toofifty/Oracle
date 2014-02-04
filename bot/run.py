import oracle
import connect
import traceback

def run():
    try:
        s, c = connect.start()
    except:
        sys.exit("There was an error connecting to the server.")
        
    while True:
        try:
            rel = oracle.main(s, c)
            if rel:
                reload(oracle) 
                print("!!! - Reload complete")
            else:
                print("Process quit.")
        except:
            traceback.print_exc()
            
run()