import traceback
import operator as op
from varcontrols import *

def add(nick, val):
    try:
        initial_val = getvar(nick, 'ircp')
        end_val = initial_val + int(val)
        setvar(nick, 'ircp', end_val)
        return end_val
    except:
        traceback.print_exc()
        return False
    
def get(nick):
    return getvar(nick, 'ircp')
    
def reset(nick):
    return setvar(nick, 'ircp', 0)
    
def get_leader_boards():
    all_scores = {}
    for file in os.listdir('../bot/users/'):
        name = file.replace('.json', '')
        all_scores[name] = get(name)
    sorted_scores = sorted(all_scores.iteritems(), key = op.itemgetter(1), reverse = True)
    return sorted_scores