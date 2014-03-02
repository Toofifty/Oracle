import threading
import time

class TimeThread(threading.Thread):
    def __init__(self, t, c):
        threading.Thread.__init__(self)
        self.t = t
        self.c = c
        self.stop = False
        
    def run(self):
        time.sleep(self.t)
        if not self.stop:
            self.c._runnable()
        
    def cancel(self):
        self.stop = True
        

class LoopTimeThread(threading.Thread):
    def __init__(self, t, c):
        threading.Thread.__init__(self)
        self.t = t
        self.c = c
        
    def run(self):
        running = True
        while running:
            time.sleep(self.t)
            if self.c._getdisabled():
                running = False
                break
            self.c._runnable()

class CountTimeThread(threading.Thread):
    def __init__(self, t, c):
        threading.Thread.__init__(self)
        self.t = t
        self.c = c
        self.current = 0
        
    def run(self):
        for i in range(0, t):
            time.sleep(1)
            self.current = i
            print i
        self.c._end()
        
class ParallelThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        self._runnable()