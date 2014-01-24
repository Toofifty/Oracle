import math

def netherposition(x, y, z):
    return math.floor(x/8), y, math.floor(z/8)
    
def overworldposition(x, y, z):
    return x*8, y, z*8