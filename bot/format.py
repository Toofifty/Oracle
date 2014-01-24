import random

class formats(object):
    def __init__(self):
        self.BOLD = "\x02"
        self.BLACK = "\x0301"
        self.DARKBLUE = "\x0302"
        self.DARKGREEN = "\x0303"
        self.RED = "\x0304"
        self.DARKRED = "\x0305"
        self.PURPLE = "\x0306"
        self.ORANGE = "\x0307"
        self.YELLOW = "\x0308"
        self.GREEN = "\x0309"
        self.CYAN = "\x0310"
        self.LIGHTBLUE = "\x0311"
        self.BLUE = "\x0312"
        self.PINK = "\x0313"
        self.DARKGREY = "\x0314"
        self.GREY = "\x0315"
        self.WHITE = "\x0300"
        
    def random(self):
        return "\x03" + str(random.randint(0, 15))
        
def replace(string):
    f = formats()
    array = [
        ["&b", f.BOLD],
        ["&15", f.GREY],
        ["&14", f.DARKGREY],
        ["&13", f.PINK],
        ["&12", f.BLUE],
        ["&11", f.LIGHTBLUE],
        ["&10", f.CYAN],
        ["&9", f.GREEN],
        ["&8", f.YELLOW],
        ["&7", f.ORANGE],
        ["&6", f.PURPLE],
        ["&5", f.DARKRED],
        ["&4", f.RED],
        ["&3", f.DARKGREEN],
        ["&2", f.DARKBLUE],
        ["&1", f.BLACK],
        ["&0", f.WHITE],
        ]
        
    for format in array:
        string = string.replace(format[0], format[1])
    
    print string
    return string